"""Après l'envoi : retrouver le message, l'attacher, estamper le bordereau définitif.

    python manage.py confirmer_transmission --transmission 1
    python manage.py confirmer_transmission --transmission 1 --message-id <id> --ecrire

POURQUOI CETTE SECONDE ÉTAPE EXISTE. L'art. 134 C.p.c. exige que le bordereau
indique « le lieu, la date et **l'heure et les minutes** de la transmission ».
Un bordereau rédigé avant l'envoi ne peut pas les connaître : il serait faux, ou
approximatif, ce qui revient au même quand une partie le demande au greffe.

L'horodatage n'est donc pas repris de l'horloge locale ni de la mémoire du
demandeur, mais de l'**en-tête `Date` du message réellement envoyé** — le même
en-tête qui, sur les courriels reçus d'Élise et de Timmons, a permis d'établir
la séquence à la minute. Ce qui vaut comme preuve contre eux vaut comme preuve
pour nous.

La ligne `Email` ainsi rattachée **est** l'entrée du journal des transmissions,
et le `.eml` archivé en est la pièce. Une ligne de `journal.md` est une
affirmation ; un message signé `dkim`/`spf`/`dmarc` est une preuve.
"""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from case_manager.models import Transmission
from case_manager.transmission_service import bordereau
from email_manager.models import Email


class Command(BaseCommand):
    help = "Rattache le message envoyé à sa transmission et estampe le bordereau définitif."

    def add_arguments(self, parser):
        parser.add_argument("--transmission", type=int, required=True)
        parser.add_argument("--message-id", help="Message-ID du courriel envoyé, si connu.")
        parser.add_argument("--ecrire", action="store_true")

    def handle(self, *args, **o):
        try:
            t = Transmission.objects.get(pk=o["transmission"])
        except Transmission.DoesNotExist:
            raise CommandError(f"Aucune transmission pk={o['transmission']}.")

        if t.bloquee:
            raise CommandError(
                "Cette transmission porte des blocages non levés. Elle n'aurait pas dû partir. "
                "Relancer `preparer_transmission` avant toute chose."
            )

        courriel = self._retrouver(t, o.get("message_id"))
        if courriel is None:
            self.stdout.write(self.style.ERROR(
                "\n⛔ Message introuvable en base.\n"
                "   L'ingestion du courrier sortant n'est pas faite. Deux voies :\n"
                "   • `python manage.py sync_threads` (ou la commande d'ingestion du projet),\n"
                "   • puis relancer, ou fournir --message-id."))
            return

        self.stdout.write(self.style.MIGRATE_HEADING(f"\n{t.nature}"))
        self.stdout.write(f"  destinataire : {t.destinataire}")
        self.stdout.write(f"  message      : {courriel.message_id}")
        self.stdout.write(f"  envoyé le    : {courriel.date_sent}")
        self.stdout.write(f"  à            : {courriel.recipients_to}")
        if courriel.recipients_cc:
            self.stdout.write(self.style.WARNING(f"  ⚠️  en copie  : {courriel.recipients_cc}"))

        # --- contrôle a posteriori : est-ce bien parti à la bonne adresse ? ---
        attendu = t.destinataire.courriel.lower()
        reel = (courriel.recipients_to or "").lower()
        if attendu not in reel:
            self.stdout.write(self.style.ERROR(
                f"\n⛔ Le message n'a pas été adressé à {attendu}. "
                "Le rattachement est refusé : vérifier le --message-id."))
            return

        # --- contrôle a posteriori : aucune partie étrangère en copie ---
        from case_manager.models import DestinataireInstance
        cible = t.destinataire.pour_le_compte_de or t.destinataire.partie
        tous = f"{courriel.recipients_to or ''} {courriel.recipients_cc or ''}".lower()
        etrangeres = {
            (d.pour_le_compte_de or d.partie)
            for d in DestinataireInstance.objects.all()
            if d.courriel.lower() in tous
        } - {cible}
        if etrangeres:
            self.stdout.write(self.style.ERROR(
                "\n⛔ MISE EN COPIE CROISÉE CONSTATÉE : " + ", ".join(sorted(etrangeres)) +
                f" figurait au message destiné à {cible}.\n"
                "   Le fait est acquis ; il est consigné tel quel. Le signaler au journal."))

        texte = bordereau(t, horodatage=courriel.date_sent)

        if not o["ecrire"]:
            self.stdout.write("\n--- BORDEREAU DÉFINITIF (non persisté) ---\n")
            self.stdout.write(texte)
            self.stdout.write(self.style.WARNING("\nRelancer avec --ecrire pour persister."))
            return

        t.email = courriel
        t.envoyee_le = courriel.date_sent
        t.etat = "ENVOYEE"
        t.bordereau = texte
        t.save(update_fields=["email", "envoyee_le", "etat", "bordereau"])

        source = Path(t.fichier_source)
        dossier = source.parent / "bordereaux"
        dossier.mkdir(exist_ok=True)
        chemin = dossier / f"{source.stem}_T{t.pk}_bordereau.md"
        chemin.write_text(texte, encoding="utf-8")
        provisoire = dossier / f"{source.stem}_T{t.pk}_bordereau_provisoire.md"
        if provisoire.exists():
            provisoire.unlink()

        self.stdout.write(self.style.SUCCESS(f"\n✅ Transmission {t.pk} confirmée."))
        self.stdout.write(f"   Bordereau définitif : {chemin}")
        self.stdout.write(
            "   ⚠️ Reste à faire à la main : la ligne dans `legal/instance/journal.md`.")

    # ------------------------------------------------------------------
    def _retrouver(self, t, message_id):
        if message_id:
            return Email.objects.filter(message_id=message_id).first()
        qs = Email.objects.filter(
            recipients_to__icontains=t.destinataire.courriel,
            date_sent__gte=t.preparee_le,
        ).order_by("date_sent")
        n = qs.count()
        if n > 1:
            self.stdout.write(self.style.WARNING(
                f"{n} messages candidats depuis la préparation ; le plus ancien est retenu. "
                "Utiliser --message-id pour lever l'ambiguïté."))
        return qs.first()
