"""
La démonstration intégrée du cahier, bâtie puis exportée.

ELLE VÉRIFIE LE MOTEUR, PAS LE DOSSIER. Les identifiants et les cotes produits
ici sont ceux d'une fixture ; ils ne disent rien des 198 numéros du papier ni
des 106 cotes du dépôt, qui se contrôlent sur les données réelles.

La commande écrit dans une base de démonstration et doit donc rester hors de la
base du dossier : elle refuse de s'exécuter si un référent historique y est déjà
déclaré, sauf `--je-sais-ce-que-je-fais`.
"""
import datetime
import json
import os

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from case_manager import citations, cotes_concordance as cc
from case_manager.models import (
    AncrageCitation, AppuiDepotJuillet, BordereauDepotJuillet, ConfirmationAppui,
    EtatAppui,
)
from document_manager import concordance as svc
from document_manager import export_concordance as exp
from document_manager import numerotation, referent as referent_service
from document_manager.models import (
    Document, DocumentSource, FormatNumero, LibraryNode, Niveau, NumberingMode,
    PorteeNumero, ReferentHistorique, RoleNiveau, SchemaNiveaux, Statement,
    TraitementEditorial, VersionTexte,
)
from events.models import Event


class Command(BaseCommand):
    help = "Construit la démonstration intégrée E01 et exporte sa concordance."

    def add_arguments(self, parser):
        parser.add_argument("--sortie", default="legal/amendements/01_avant_notification/preuves_E01")
        parser.add_argument("--je-sais-ce-que-je-fais", action="store_true")

    @transaction.atomic
    def handle(self, *args, **o):
        w = self.stdout.write
        if ReferentHistorique.objects.exists() and not o["je_sais_ce_que_je_fais"]:
            raise CommandError(
                "Un référent historique est déclaré dans cette base : c'est "
                "celle du dossier. La démonstration écrit des données de "
                "fixture et ne doit pas s'y mêler."
            )
        os.makedirs(o["sortie"], exist_ok=True)

        schema = self._schema()
        source, s = self._source(schema)
        cible, c = self._cible(schema)
        ref = ReferentHistorique.objects.create(
            document=source, libelle="DÉMONSTRATION — acte déposé de fixture")

        pieces = self._registre()
        self._appuis(s, c, pieces)

        # L'INSTANTANÉ SE PREND QUAND L'ACTE EST COMPLET, appuis compris : pris
        # plus tôt, il rapporterait comme une dérive l'enregistrement même de ce
        # que l'acte déposé invoquait.
        referent_service.prendre_instantane(ref, "démonstration E01 — acte complet")

        self._liens(source, cible, s, c)
        self._citations(c, pieces)

        w("=" * 78)
        w("DÉMONSTRATION INTÉGRÉE E01  (fixture — pas le dossier)")
        w("=" * 78)
        self._montrer_numeros(source, cible, s, c)

        # --- 1. restitution DIAGNOSTIQUE : il manque des décisions ---
        controle_ref, rapport_lock = self._controles(ref, pieces, o["sortie"])
        r1 = exp.construire(source, cible, rapport_lock, controle_ref)
        w("")
        w("  AVANT DÉCISIONS — export strict :")
        for v in r1['verdicts']:
            if not v['satisfait']:
                w(f"    BLOQUE {v['condition']} ({v['nombre_de_motifs']} motif(s))")
        self._ecrire(o["sortie"], "demo_concordance_diagnostique", r1)

        # --- 2. on décide tout, puis on exporte en strict ---
        self._confirmer_tout(source, cible, s, c, pieces)
        r2 = exp.construire(source, cible, rapport_lock, controle_ref)
        w("")
        w("  APRÈS DÉCISIONS — export strict : "
          + ("POSSIBLE" if r2['strict_possible'] else "REFUSÉ"))
        for v in r2['verdicts']:
            if not v['satisfait']:
                w(f"    BLOQUE {v['condition']}")
                for m in v['motifs'][:4]:
                    w(f"       · {m}")
        if r2['strict_possible']:
            self._ecrire(o["sortie"], "demo_concordance", r2, strict=True)

        # --- 3. le reclassement P-12 → P-13 ---
        self._reclassement(c, pieces, o["sortie"])

        # --- 4. la table autonome des cotes ---
        table = cc.table_des_cotes(rapport_lock=rapport_lock)
        chemin = os.path.join(o["sortie"], "demo_table_cotes.json")
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(table, f, ensure_ascii=False, indent=2, default=str)
        w(f"\n  Table des cotes (fixture) : {chemin}")
        w(f"    état : {table['empreinte_etat'][:16]}…  "
          f"{table['nombre']} lignes  fidélité : {table['fidelite_historique']}")

        # Cette commande ne doit rien laisser : la démonstration est une preuve,
        # pas un jeu de données.
        if not o["je_sais_ce_que_je_fais"]:
            transaction.set_rollback(True)
            w("")
            w(self.style.WARNING(
                "  Transaction annulée : la base est inchangée. Les fichiers "
                "produits restent."))

    # -- construction ----------------------------------------------------
    def _schema(self):
        s = SchemaNiveaux.objects.create(nom="DÉMO — acte E01")
        Niveau.objects.create(schema=s, profondeur=1, role=RoleNiveau.RACINE)
        Niveau.objects.create(schema=s, profondeur=2, role=RoleNiveau.PARAGRAPHE,
                              format_numero=FormatNumero.DECIMAL,
                              portee=PorteeNumero.DOCUMENT)
        return s

    def _noeud(self, parent, doc, item, texte, numero=""):
        ct = ContentType.objects.get_for_model(Statement)
        st = Statement.objects.create(text=texte, is_user_created=True)
        return parent.add_child(document=doc, item=item, content_type=ct,
                                object_id=st.pk, paragraph_number=numero)

    def _source(self, schema):
        doc = Document.objects.create(
            title="DÉMO — acte déposé", source_type=DocumentSource.PRODUCED,
            schema=schema, numbering_mode=NumberingMode.STORED)
        r = LibraryNode.add_root(document=doc, item="Racine")
        s = {}
        for item, texte in (("1", "le fait conservé, déplacé"),
                            ("2", "le fait reformulé et déplacé"),
                            ("4", "le fait qui sera scindé en deux"),
                            ("4-A", "le premier fait à fusionner"),
                            ("9", "le second fait à fusionner"),
                            ("10", "le fait retiré du récit"),
                            ("11", "le fait laissé sans décision")):
            s[item] = self._noeud(r, doc, item, texte, numero=item)
        return doc, s

    def _cible(self, schema):
        doc = Document.objects.create(
            title="DÉMO — version modifiée", source_type=DocumentSource.PRODUCED,
            schema=schema, numbering_mode=NumberingMode.AUTO)
        r = LibraryNode.add_root(document=doc, item="Racine")
        c = {}
        textes = {
            1: "le fait reformulé et déplacé, réécrit",
            2: "les deux faits fusionnés en un seul",
            3: "le fait conservé, déplacé",
            4: "la première moitié du fait scindé",
            5: "la seconde moitié du fait scindé",
            6: "un fait nouveau, décidé",
            7: "un paragraphe cible sans décision, citant la pièce P-12",
        }
        for i in range(1, 8):
            c[i] = self._noeud(r, doc, str(i), textes[i])
        return doc, c

    def _registre(self):
        """Onze pièces anciennes, la pièce citée en douzième, une liasse."""
        pieces = {}
        for i in range(11):
            e = Event.objects.create(date=datetime.date(2010, 1, 1 + i),
                                     explanation=f"pièce ancienne {i + 1}")
            pieces[f"P-{i + 1}"] = self._entree(f"P-{i + 1}", e, i + 1)
        e12 = Event.objects.create(date=datetime.date(2015, 4, 20),
                                   explanation="la pièce citée au § 7")
        pieces["P-12"] = self._entree("P-12", e12, 12)
        # Une liasse de juillet, que l'ordre chronologique dispersera.
        a = Event.objects.create(date=datetime.date(2016, 3, 7),
                                 explanation="composant ancien de la liasse")
        b = Event.objects.create(date=datetime.date(2019, 8, 1),
                                 explanation="composant tardif de la liasse")
        pieces["P-13.1"] = self._entree("P-13.1", a, 13, sous_rang=1,
                                        racine="P-13")
        pieces["P-13.2"] = self._entree("P-13.2", b, 13, sous_rang=2,
                                        racine="P-13")
        return pieces

    def _entree(self, cote, obj, rang, sous_rang=None, racine=None):
        ct = ContentType.objects.get_for_model(obj)
        return BordereauDepotJuillet.objects.create(
            cote=cote, cote_racine=racine or cote, rang=rang, sous_rang=sous_rang,
            content_type=ct, object_id=obj.pk, source_type=ct.model,
            description=obj.explanation, resolu=True)

    def _liens(self, source, cible, s, c):
        svc.relier(source, cible, [s["1"]], [c[3]],
                   traitement=TraitementEditorial.CONSERVE, deplace=True)
        svc.relier(source, cible, [s["2"]], [c[1]],
                   traitement=TraitementEditorial.REFORMULE, deplace=True)
        svc.relier(source, cible, [s["4"]], [c[4], c[5]],
                   traitement=TraitementEditorial.SCINDE)
        svc.relier(source, cible, [s["4-A"], s["9"]], [c[2]],
                   traitement=TraitementEditorial.FUSIONNE)
        svc.relier(source, cible, [], [c[6]],
                   traitement=TraitementEditorial.AJOUT,
                   motif="fait nouveau, décidé explicitement")
        svc.relier(source, cible, [s["10"]], [],
                   traitement=TraitementEditorial.RETRAIT,
                   motif="retiré du récit, décidé explicitement")
        # s["11"] et c[7] restent sans décision : « à établir ».

    def _appuis(self, s, c, pieces):
        for noeud, cote in ((s["2"], "P-12"), (s["4"], "P-1"),
                            (s["4-A"], "P-2"), (s["9"], "P-3")):
            AppuiDepotJuillet.objects.create(
                statement=noeud.content_object, entree=pieces[cote],
                cote_citee=cote)

    def _citations(self, c, pieces):
        noeud = LibraryNode.objects.get(pk=c[7].pk)
        texte = noeud.content_object.text
        pos = texte.index("P-12")
        AncrageCitation.objects.create(noeud=noeud, entree=pieces["P-12"],
                                       libelle_ecrit="P-12",
                                       debut=pos, fin=pos + 4)

    def _confirmer_tout(self, source, cible, s, c, pieces):
        from document_manager.models import Correspondance
        for corr in Correspondance.objects.filter(document_source=source,
                                                  document_cible=cible):
            svc.confirmer_traitement(corr, corr.traitement,
                                     motif=corr.motif or "décision de démonstration")
        # Les deux occurrences sans décision reçoivent la leur.
        svc.confirmer_traitement(
            svc.relier(source, cible, [s["11"]], [],
                       traitement=TraitementEditorial.RETRAIT,
                       motif="retrait décidé à la relecture"),
            TraitementEditorial.RETRAIT, motif="retrait décidé à la relecture")
        svc.confirmer_traitement(
            svc.relier(source, cible, [], [c[7]],
                       traitement=TraitementEditorial.AJOUT,
                       motif="ajout décidé à la relecture"),
            TraitementEditorial.AJOUT, motif="ajout décidé à la relecture")

        for i, noeud in c.items():
            n = LibraryNode.objects.get(pk=noeud.pk)
            if i == 7:
                ConfirmationAppui.objects.create(
                    noeud=n, entree=pieces["P-12"],
                    version_examinee=VersionTexte.capter(n.content_object),
                    etat=EtatAppui.CONFIRME, role="attestation",
                    portee="la transmission de la lettre",
                    portee_sha256=ConfirmationAppui.empreinte_portee(
                        "la transmission de la lettre"))
            else:
                ConfirmationAppui.objects.create(
                    noeud=n, entree=None,
                    version_examinee=VersionTexte.capter(n.content_object),
                    etat=EtatAppui.SANS_APPUI,
                    motif="démonstration : absence d'appui explicitement décidée")

    def _controles(self, ref, pieces, sortie):
        """
        Le contrôle du référent et celui du lock — tous deux de FIXTURE.

        Un export strict qui ne les porterait pas serait refusé par EX01 et
        EX04, et c'est voulu : la complétude se démontre, elle ne se suppose pas.
        """
        inst = ref.instantanes.first()
        ecarts = referent_service.comparer(inst)
        controle_ref = {
            'instantane': inst.pk,
            'empreinte': inst.empreinte_globale,
            'intact': referent_service.contenu_intact(ecarts),
            'ecarts': {k: len(v) for k, v in ecarts.items() if isinstance(v, list)},
            'portee': "FIXTURE — ne vaut pas pour le dossier",
        }

        # Un lock de fixture, écrit depuis le registre de fixture : il démontre
        # le MÉCANISME du contrôle, non la fidélité du dépôt réel.
        cts = {ct.id: ct for ct in ContentType.objects.all()}
        par_racine = {}
        for e in BordereauDepotJuillet.objects.exclude(cote__isnull=True):
            ct = cts.get(e.content_type_id)
            par_racine.setdefault(e.cote_racine, []).append(
                f"{ct.model.capitalize() if ct else '?'}:{e.object_id}")
        lock = {"schema": "cotes.lock/1", "genere_le": "fixture",
                "cotes": [{"cote": k, "identites_attendues": " | ".join(sorted(v)),
                           "description": "fixture"}
                          for k, v in sorted(par_racine.items())]}
        chemin = os.path.join(sortie, "demo_cotes.lock.json")
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(lock, f, ensure_ascii=False, indent=2)
        return controle_ref, cc.reconcilier(chemin)

    # -- restitution -----------------------------------------------------
    def _montrer_numeros(self, source, cible, s, c):
        w = self.stdout.write
        ns = numerotation.index_par_noeud(source)
        nc = numerotation.index_par_noeud(cible)
        w("  SOURCE (STORED) — le numéro du papier")
        w("    " + "  ".join(f"{k}→{ns[v.pk]}" for k, v in s.items()))
        w("  CIBLE (AUTO) — le numéro calculé")
        w("    " + "  ".join(f"c{k}→{nc[v.pk]}" for k, v in c.items()))

    def _reclassement(self, c, pieces, sortie):
        w = self.stdout.write
        noeud = LibraryNode.objects.get(pk=c[7].pk)
        avant = citations.rendre(noeud)
        etat_avant = cc.etat_de_cotation()

        anterieure = Event.objects.create(
            date=datetime.date(2009, 10, 6),
            explanation="pièce antérieure versée après le dépôt")
        ajout = BordereauDepotJuillet.objects.create(
            cote=None, content_type=ContentType.objects.get_for_model(Event),
            object_id=anterieure.pk, source_type="event",
            description=anterieure.explanation, resolu=True)
        apres = citations.rendre(noeud)
        etat_apres = cc.etat_de_cotation()
        index = cc.index_cote_cible()

        w("")
        w("  RECLASSEMENT P-12 → P-13")
        w(f"    texte stocké   : …{avant['texte_stocke'][-46:]}")
        w(f"    rendu avant    : …{avant['texte_rendu'][-46:]}")
        w(f"    rendu après    : …{apres['texte_rendu'][-46:]}")
        w(f"    même source    : entrée {pieces['P-12'].pk} dans les deux cas")
        w(f"    P-12 désigne désormais : entrée "
          f"{[k for k, v in index.items() if v == 'P-12']}")
        w(f"    état avant/après : {etat_avant['empreinte_etat'][:12]}… / "
          f"{etat_apres['empreinte_etat'][:12]}…")

        conf = ConfirmationAppui.objects.filter(noeud=noeud).first()
        if conf:
            w(f"    confirmation applicable : {conf.etat_courant()}")

        chemin = os.path.join(sortie, "demo_reclassement_P12_P13.json")
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump({
                'texte_stocke': avant['texte_stocke'],
                'rendu_avant': avant['texte_rendu'],
                'rendu_apres': apres['texte_rendu'],
                'entree_citee': pieces['P-12'].pk,
                'nouvelle_cote': index.get(pieces['P-12'].pk),
                'entree_occupant_P12_apres': [k for k, v in index.items()
                                              if v == 'P-12'],
                'etat_cotation_avant': etat_avant['empreinte_etat'],
                'etat_cotation_apres': etat_apres['empreinte_etat'],
                'confirmation_etat_courant': conf.etat_courant() if conf else None,
                'remplacements': apres['remplacements'],
            }, f, ensure_ascii=False, indent=2)
        w(f"    écrit : {chemin}")

    def _ecrire(self, sortie, base, restitution, strict=False):
        cj = os.path.join(sortie, base + ".json")
        cc_ = os.path.join(sortie, base + ".csv")
        with open(cj, "w", encoding="utf-8") as f:
            f.write(exp.en_json(restitution, strict=strict))
        with open(cc_, "w", encoding="utf-8", newline="") as f:
            f.write(exp.en_csv(restitution, strict=strict))
        self.stdout.write(f"    écrit : {cj}")
        self.stdout.write(f"    écrit : {cc_}")
