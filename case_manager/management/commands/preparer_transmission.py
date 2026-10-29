"""Préparer un envoi : empreinter, vérifier, produire le bordereau provisoire.

    python manage.py preparer_transmission --destinataires
    python manage.py preparer_transmission \
        --fichier legal/instance/sortants/2026-10-13_elise_information-et-communication-pieces.md \
        --nature "Lettre — information des parties et communication des pièces" \
        --destinataire 2 \
        --atteste delai,relu_a_froid,aucun_fait_nouveau,aucun_engagement,ton \
        --ecrire

La commande **n'envoie rien** et ne le pourra jamais : le scope OAuth du projet
est `gmail.readonly`. L'envoi reste un geste manuel, et c'est le point — la
règle n° 2 du dossier est « jamais de réponse sur le fond le jour même ».

Ce qu'elle fait : elle refuse de produire un bordereau tant que les contrôles
objectifs ne passent pas, et elle exige que les jugements qu'elle ne peut pas
porter soient portés nommément, par `--atteste`. Une attestation est une
signature, pas une case : ne pas la donner sans avoir relu.

Sans `--ecrire`, rien n'est persisté : la commande rapporte et s'arrête.
"""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from case_manager.models import DestinataireInstance, FichierTransmis, Transmission
from case_manager.transmission_service import (
    ATTESTATIONS, bordereau, destinataires_valides, empreinte, verifier,
)


class Command(BaseCommand):
    help = "Vérifie un envoi et produit son bordereau provisoire (art. 134 C.p.c.)."

    def add_arguments(self, parser):
        parser.add_argument("--destinataires", action="store_true",
                            help="Lister les destinataires et leurs fenêtres de validité.")
        parser.add_argument("--fichier", help="Le .md de `legal/instance/sortants/`.")
        parser.add_argument("--nature", help="Nature du document, au sens de l'art. 134.")
        parser.add_argument("--destinataire", type=int, help="pk d'un DestinataireInstance.")
        parser.add_argument("--piece", action="append", default=[],
                            help="Pièce jointe, répétable. Forme : chemin ou cote=chemin.")
        parser.add_argument("--copie", action="append", default=[],
                            help="Adresse en copie, répétable. Bloque si elle appartient "
                                 "à une autre partie.")
        parser.add_argument("--atteste", default="",
                            help="Clés d'attestation, séparées par des virgules. "
                                 f"Disponibles : {', '.join(ATTESTATIONS)}")
        parser.add_argument("--ecrire", action="store_true", help="Persister la transmission.")

    def handle(self, *args, **o):
        if o["destinataires"]:
            return self._lister()

        for requis in ("fichier", "nature", "destinataire"):
            if not o.get(requis):
                raise CommandError(f"--{requis} est requis (ou utilisez --destinataires).")

        try:
            dest = DestinataireInstance.objects.get(pk=o["destinataire"])
        except DestinataireInstance.DoesNotExist:
            raise CommandError(f"Aucun destinataire pk={o['destinataire']}. Voir --destinataires.")

        source = Path(o["fichier"])
        if not source.exists():
            raise CommandError(f"Fichier introuvable : {source}")

        t = Transmission(
            nature=o["nature"], destinataire=dest, fichier_source=str(source),
        )
        if o["ecrire"]:
            t.save()

        pieces = []
        for brut in o["piece"]:
            cote, _, chemin = brut.partition("=")
            if not chemin:
                cote, chemin = "", brut
            p = Path(chemin)
            if not p.exists():
                raise CommandError(f"Pièce jointe introuvable : {p}")
            f = FichierTransmis(
                transmission=t if o["ecrire"] else None, chemin=str(p),
                nom_transmis=p.name, cote=cote,
                octets=p.stat().st_size, sha256=empreinte(p),
            )
            if o["ecrire"]:
                f.save()
            pieces.append(f)

        attestations = [a.strip() for a in o["atteste"].split(",") if a.strip()]
        inconnues = set(attestations) - set(ATTESTATIONS)
        if inconnues:
            raise CommandError(f"Clés d'attestation inconnues : {', '.join(sorted(inconnues))}")

        rapport = verifier(t, attestations=attestations, fichiers=pieces, copies=o["copie"])
        self._rapporter(t, rapport, pieces)

        if rapport["blocages"]:
            if o["ecrire"]:
                t.verification = rapport
                t.save(update_fields=["verification"])
            self.stdout.write(self.style.ERROR(
                "\n⛔ RIEN NE PART. Lever les blocages ci-dessus, puis relancer."))
            return

        texte = bordereau(t, fichiers=pieces)
        if o["ecrire"]:
            t.verification = rapport
            t.bordereau = texte
            t.save(update_fields=["verification", "bordereau"])
            dossier = source.parent / "bordereaux"
            dossier.mkdir(exist_ok=True)
            # Une lettre peut partir vers plusieurs destinataires : le pk distingue les bordereaux.
            chemin = dossier / f"{source.stem}_T{t.pk}_bordereau_provisoire.md"
            chemin.write_text(texte, encoding="utf-8")
            self.stdout.write(self.style.SUCCESS(f"\n✅ Transmission {t.pk} préparée."))
            self.stdout.write(f"   Bordereau provisoire : {chemin}")
            self.stdout.write(
                "   Après l'envoi : python manage.py confirmer_transmission "
                f"--transmission {t.pk}")
        else:
            self.stdout.write("\n--- BORDEREAU PROVISOIRE (non persisté) ---\n")
            self.stdout.write(texte)
            self.stdout.write(self.style.WARNING("\nRelancer avec --ecrire pour persister."))

    # ------------------------------------------------------------------
    def _lister(self):
        from datetime import date
        aujourdhui = date.today()
        valides = {d.pk for d in destinataires_valides(aujourdhui)}
        self.stdout.write(self.style.MIGRATE_HEADING(
            f"Destinataires de l'instance — validité au {aujourdhui.isoformat()}\n"))
        for d in DestinataireInstance.objects.all():
            marque = self.style.SUCCESS("✅") if d.pk in valides else self.style.ERROR("⛔")
            self.stdout.write(f"{marque} [{d.pk}] {d}")
            if d.qualite == "AVOCAT":
                self.stdout.write(f"       avocats de {d.pour_le_compte_de}")
            if d.source:
                self.stdout.write(f"       établie par : {d.source}")
        if not DestinataireInstance.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Aucun destinataire. Peupler avec `python manage.py init_destinataires`."))

    def _rapporter(self, t, rapport, pieces):
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n{t.nature}"))
        self.stdout.write(f"  destinataire : {t.destinataire}")
        self.stdout.write(f"  source       : {t.fichier_source}")
        for f in pieces:
            self.stdout.write(f"  pièce        : {f.cote or '—'} {f.nom_transmis} "
                              f"({f.octets} o) {f.sha256[:16]}…")

        if rapport["signalements"]:
            self.stdout.write(self.style.WARNING(
                f"\n⚠️  {len(rapport['signalements'])} signalement(s) — à regarder, pas à craindre :"))
            for s in rapport["signalements"]:
                self.stdout.write(f"   • {s['motivation']}")
                self.stdout.write(f"     …{s['extrait']}…")

        if rapport["blocages"]:
            self.stdout.write(self.style.ERROR(
                f"\n⛔ {len(rapport['blocages'])} blocage(s) :"))
            for b in rapport["blocages"]:
                self.stdout.write(f"   • {b}")
