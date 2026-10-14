"""
Epic E01 — cotes, appuis, citations et export, sur fixtures.

Les attentes sont calculées à la main. Un test qui demanderait au service testé
quel ordre il produit, puis vérifierait que c'est bien celui-là, ne démontrerait
rien.
"""
import datetime
import json
import os
import tempfile
from contextlib import contextmanager

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.test import TestCase
from django.utils import timezone

from case_manager import citations, cotes_concordance as cc
from case_manager.models import (
    AncrageCitation, AppuiDepotJuillet, BordereauDepotJuillet, ConfirmationAppui,
    EtatAppui,
)
from document_manager import concordance as svc
from document_manager import export_concordance as exp
from document_manager import numerotation
from document_manager.models import (
    Document, DocumentSource, EtatConfirmation, LibraryNode, NumberingMode,
    ReferentHistorique, Statement, TraitementEditorial, VersionTexte,
)
from document_manager.test_e01_numerotation import (
    ajouter, faire_document, racine_de, schema_acte,
)
from events.models import Event


@contextmanager
def refus_attendu(testcase, exception):
    with testcase.assertRaises(exception):
        with transaction.atomic():
            yield


def un_evenement(titre, quand):
    """Une pièce datable, pour éprouver le classement chronologique."""
    return Event.objects.create(date=quand, explanation=titre)


def entree(cote, obj, description="", atemporel=False, rang=None, sous_rang=None,
           cote_racine=None, parent=None, rang_precision=None):
    ct = ContentType.objects.get_for_model(obj) if obj is not None else None
    return BordereauDepotJuillet.objects.create(
        cote=cote, cote_racine=cote_racine or cote,
        rang=rang, sous_rang=sous_rang, parent=parent,
        rang_precision=rang_precision,
        content_type=ct, object_id=obj.pk if obj is not None else None,
        source_type=(ct.model if ct else ""), description=description,
        atemporel=atemporel, resolu=obj is not None,
    )


class BaseCotes(TestCase):
    def setUp(self):
        self.d2013 = datetime.date(2013, 6, 11)
        self.d2015 = datetime.date(2015, 4, 20)
        self.d2019 = datetime.date(2019, 10, 15)


# ---------------------------------------------------------------------------
# T24 — le contrôle historique et la table chronologique
# ---------------------------------------------------------------------------

class T24ControleDuLock(BaseCotes):
    def setUp(self):
        super().setUp()
        self.e1 = un_evenement("plan de 2013", self.d2013)
        self.e2 = un_evenement("lettre de 2015", self.d2015)
        self.p1 = entree("P-1", self.e1, "le plan", rang=1)
        self.p2 = entree("P-2", self.e2, "la lettre", rang=2)
        self.rep = tempfile.mkdtemp()

    def _lock(self, cotes):
        chemin = os.path.join(self.rep, "cotes.lock.json")
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump({"schema": "cotes.lock/1", "genere_le": "2026-07-27",
                       "cotes": cotes}, f)
        return chemin

    def _identite(self, obj):
        return f"{obj.__class__.__name__}:{obj.pk}"

    def test_lock_absent_bloque_sans_reconstituer_depuis_la_base(self):
        with self.assertRaises(cc.LockIndisponible):
            cc.reconcilier(os.path.join(self.rep, "inexistant.json"))

    def test_concordance_complete(self):
        chemin = self._lock([
            {"cote": "P-1", "identites_attendues": self._identite(self.e1)},
            {"cote": "P-2", "identites_attendues": self._identite(self.e2)},
        ])
        r = cc.reconcilier(chemin)
        self.assertTrue(r['conforme'])
        self.assertEqual(r['concordantes'], 2)

    def test_association_manquante_est_diagnostiquee(self):
        chemin = self._lock([
            {"cote": "P-1", "identites_attendues": self._identite(self.e1)},
            {"cote": "P-99", "identites_attendues": "Event:9999",
             "description": "une cote que le registre ignore"},
        ])
        r = cc.reconcilier(chemin)
        self.assertFalse(r['conforme'])
        self.assertEqual([m['cote'] for m in r['manquantes']], ["P-99"])

    def test_association_divergente_est_diagnostiquee_sans_correction(self):
        chemin = self._lock([
            {"cote": "P-1", "identites_attendues": self._identite(self.e2)},
        ])
        r = cc.reconcilier(chemin)
        self.assertFalse(r['conforme'])
        self.assertEqual(len(r['divergentes']), 1)
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.object_id, self.e1.pk,
                         "Aucune correction silencieuse du registre.")

    def test_identite_illisible_est_ambigue(self):
        chemin = self._lock([{"cote": "P-1", "identites_attendues": "n'importe quoi"}])
        r = cc.reconcilier(chemin)
        self.assertEqual(len(r['ambigues']), 1)
        self.assertFalse(r['conforme'])

    def test_les_ajouts_sans_cote_ne_sont_pas_des_manques(self):
        e3 = un_evenement("pièce versée après le dépôt", self.d2019)
        entree(None, e3, "ajout", cote_racine=None)
        chemin = self._lock([
            {"cote": "P-1", "identites_attendues": self._identite(self.e1)},
            {"cote": "P-2", "identites_attendues": self._identite(self.e2)},
        ])
        r = cc.reconcilier(chemin)
        self.assertTrue(r['conforme'])
        self.assertEqual(r['ajouts_sans_cote_de_juillet'], 1)

    def test_une_liasse_repond_par_ses_composants(self):
        """Le lock porte des cotes principales, le registre leur détail."""
        BordereauDepotJuillet.objects.all().delete()
        a = un_evenement("courriel a", self.d2013)
        b = un_evenement("courriel b", self.d2015)
        entree("P-43.1", a, rang=43, sous_rang=1, cote_racine="P-43")
        entree("P-43.2", b, rang=43, sous_rang=2, cote_racine="P-43")
        chemin = self._lock([{
            "cote": "P-43",
            "identites_attendues": f"{self._identite(a)} | {self._identite(b)}",
        }])
        r = cc.reconcilier(chemin)
        self.assertTrue(r['conforme'],
                        "Deux lignes de registre répondent à une cote du lock.")


class T24TableChronologique(BaseCotes):
    def setUp(self):
        super().setUp()
        self.e2013 = un_evenement("pièce de 2013", self.d2013)
        self.e2019 = un_evenement("pièce de 2019", self.d2019)
        entree("P-1", self.e2013, rang=1)
        entree("P-2", self.e2019, rang=2)

    def test_la_cotation_suit_la_date_et_non_la_cote(self):
        table = cc.table_des_cotes()
        attendu = [("P-1", "P-1"), ("P-2", "P-2")]
        self.assertEqual([(l['ancienne_cote'], l['nouvelle_cote'])
                          for l in table['lignes']], attendu)

    def test_une_piece_anterieure_ajoutee_decale_les_cotes_cibles(self):
        """La pièce versée après le dépôt n'a pas de cote de juillet, et
        pourtant elle prend le premier rang si sa date l'y place."""
        e2009 = un_evenement("pièce de 2009", datetime.date(2009, 10, 6))
        entree(None, e2009, "versée après le dépôt")

        table = cc.table_des_cotes()
        lignes = [(l['ancienne_cote'], l['nouvelle_cote']) for l in table['lignes']]
        self.assertEqual(lignes, [
            ("(sans cote de juillet)", "P-1"),
            ("P-1", "P-2"),
            ("P-2", "P-3"),
        ])

    def test_aucune_obligation_de_commencer_les_ajouts_a_P107(self):
        e2009 = un_evenement("ajout ancien", datetime.date(2009, 10, 6))
        entree(None, e2009)
        table = cc.table_des_cotes()
        ajout = [l for l in table['lignes'] if l['sans_cote_de_juillet']][0]
        self.assertEqual(ajout['nouvelle_cote'], "P-1")

    def test_les_associations_historiques_restent_intactes(self):
        avant = list(BordereauDepotJuillet.objects.values_list(
            'pk', 'cote', 'content_type_id', 'object_id'))
        cc.table_des_cotes()
        cc.etat_de_cotation()
        self.assertEqual(
            list(BordereauDepotJuillet.objects.values_list(
                'pk', 'cote', 'content_type_id', 'object_id')), avant)

    def test_deux_lectures_donnent_le_meme_etat(self):
        self.assertEqual(cc.etat_de_cotation()['empreinte_etat'],
                         cc.etat_de_cotation()['empreinte_etat'])


class T25LiassesDatesEtDepartage(BaseCotes):
    def test_une_liasse_se_disperse_et_sa_composition_est_preservee(self):
        tot = un_evenement("composant ancien", self.d2013)
        tard = un_evenement("composant tardif", self.d2019)
        intercale = un_evenement("pièce intercalée", self.d2015)
        entree("P-43.1", tot, rang=43, sous_rang=1, cote_racine="P-43")
        entree("P-43.2", tard, rang=43, sous_rang=2, cote_racine="P-43")
        entree("P-50", intercale, rang=50)

        table = cc.table_des_cotes()
        par_ancienne = {l['ancienne_cote']: l['nouvelle_cote']
                        for l in table['lignes']}
        self.assertEqual(par_ancienne["P-43.1"], "P-1")
        self.assertEqual(par_ancienne["P-50"], "P-2")
        self.assertEqual(par_ancienne["P-43.2"], "P-3")

        dispersion = cc.dispersion_des_liasses(table)
        liasse = [d for d in dispersion if d['cote_racine_juillet'] == "P-43"][0]
        self.assertEqual(liasse['composants'], 2)
        self.assertTrue(liasse['dispersee'])
        self.assertEqual([c['ancienne_cote'] for c in liasse['detail']],
                         ["P-43.1", "P-43.2"])

    def test_le_departage_est_deterministe_a_horodatage_egal(self):
        """Deux entrées visant la MÊME source : l'ordre ne peut pas flotter."""
        e = un_evenement("une seule source", self.d2013)
        a = entree("P-10", e, rang=10)
        b = entree("P-10.1", e, rang=10, sous_rang=1, cote_racine="P-10")
        ordres = []
        for _ in range(3):
            ordre = [x[1].pk for x in cc.cotation_chronologique()]
            ordres.append(ordre)
        self.assertEqual(ordres[0], ordres[1])
        self.assertEqual(ordres[1], ordres[2])
        self.assertLess(ordres[0].index(a.pk), ordres[0].index(b.pk),
                        "À source et date égales, le sous-rang départage.")

    def test_un_passage_prend_la_date_de_sa_piece(self):
        """Sans cette règle, un extrait saisi aujourd'hui se rangerait en 2026."""
        piece = un_evenement("le courriel de 2013", self.d2013)
        recent = un_evenement("un repère de 2019", self.d2019)
        mere = entree("P-98", piece, rang=98)
        passage = entree("P-98.1", piece, rang=98, sous_rang=1,
                         cote_racine="P-98", parent=mere, rang_precision=1)
        entree("P-99", recent, rang=99)

        rangs = {e.pk: r for r, e, _d, _g in cc.cotation_chronologique()}
        self.assertLess(rangs[passage.pk], rangs[
            BordereauDepotJuillet.objects.get(cote="P-99").pk],
            "Le passage suit la date de sa pièce, pas celle de sa saisie.")


class T26GroupesEtDatation(BaseCotes):
    def test_les_trois_groupes_se_suivent(self):
        datee = un_evenement("datée", self.d2013)
        sans = un_evenement("à dater", datetime.date(1900, 1, 1))
        atemp = un_evenement("atemporelle", self.d2019)
        entree("P-1", datee, rang=1)
        entree("P-2", sans, rang=2)
        entree("P-3", atemp, rang=3, atemporel=True)

        groupes = [g for _r, _e, _d, g in cc.cotation_chronologique()]
        self.assertEqual(groupes, ['datee', 'a_dater', 'atemporelle'])

    def test_dater_une_piece_recalcule_sans_toucher_aux_cotes_historiques(self):
        tard = un_evenement("datée tardivement", self.d2019)
        floue = un_evenement("à dater", datetime.date(1900, 1, 1))
        entree("P-1", tard, rang=1)
        e_floue = entree("P-2", floue, rang=2)

        avant = cc.table_des_cotes()
        self.assertEqual(
            [l['nouvelle_cote'] for l in avant['lignes']
             if l['ancienne_cote'] == "P-2"], ["P-2"])
        export_anterieur = json.dumps(avant)

        floue.date = self.d2013
        floue.save()

        apres = cc.table_des_cotes()
        self.assertEqual(
            [l['nouvelle_cote'] for l in apres['lignes']
             if l['ancienne_cote'] == "P-2"], ["P-1"],
            "Datée, la pièce reprend son rang d'elle-même.")
        e_floue.refresh_from_db()
        self.assertEqual(e_floue.cote, "P-2",
                         "La cote de juillet ne se réaffecte jamais.")
        self.assertNotEqual(avant['empreinte_etat'], apres['empreinte_etat'])
        self.assertEqual(json.loads(export_anterieur)['empreinte_etat'],
                         avant['empreinte_etat'],
                         "L'export antérieur reste tel qu'il a été produit.")


# ---------------------------------------------------------------------------
# T28 — les citations rendues
# ---------------------------------------------------------------------------

class T28CitationsRendues(BaseCotes):
    def setUp(self):
        super().setUp()
        self.schema = schema_acte()
        self.doc = faire_document("version 2", schema=self.schema)
        self.racine = racine_de(self.doc)

        # ONZE PIÈCES ANTÉRIEURES, pour que la pièce citée occupe réellement le
        # douzième rang chronologique. Sans elles, « P-12 » se traduirait en
        # « P-1 » et le scénario ne dirait rien du reclassement.
        for i in range(11):
            entree(f"P-{i + 1}", un_evenement(f"pièce antérieure {i + 1}",
                                              datetime.date(2010, 1, 1 + i)),
                   rang=i + 1)
        self.source_p12 = un_evenement("la pièce citée", self.d2015)
        self.e12 = entree("P-12", self.source_p12, "la pièce du § 44", rang=12)

        self.noeud = ajouter(
            self.racine, self.doc, "44",
            "Le 20 avril 2015, le demandeur a transmis la lettre, "
            "tel qu'il appert de la pièce P-12.")
        pos = self.noeud.content_object.text.index("P-12")
        self.ancrage = AncrageCitation.objects.create(
            noeud=self.noeud, entree=self.e12, libelle_ecrit="P-12",
            debut=pos, fin=pos + 4)

    def test_avant_ajout_la_citation_rend_P12(self):
        rendu = citations.rendre(self.noeud)
        self.assertIn("pièce P-12.", rendu['texte_rendu'])
        self.assertEqual(rendu['remplacements'], [])

    def test_apres_ajout_d_une_piece_anterieure_la_citation_rend_P13(self):
        avant = citations.rendre(self.noeud)['texte_rendu']
        export_anterieur = cc.table_des_cotes()

        anterieure = un_evenement("pièce antérieure versée après le dépôt",
                                  self.d2013)
        entree(None, anterieure, "ajout antérieur")
        # Datée de 2013, elle s'intercale entre les onze de 2010 et celle de
        # 2015 : elle occupe donc P-12, et la pièce citée passe à P-13.

        rendu = citations.rendre(self.noeud)
        self.assertIn("pièce P-13.", rendu['texte_rendu'])
        self.assertEqual(rendu['remplacements'],
                         [{'de': "P-12", 'vers': "P-13", 'entree': self.e12.pk}])

        self.assertIn("P-12", rendu['texte_stocke'],
                      "Le texte stocké n'est jamais réécrit.")
        self.assertIn("P-12", avant)
        self.assertIn("P-12", [l['nouvelle_cote'] for l in export_anterieur['lignes']
                               if l['entree_pk'] == self.e12.pk],
                      "L'export antérieur porte toujours P-12.")

    def test_la_citation_suit_la_source_et_non_le_libelle(self):
        """P-12 ne doit pas se mettre à désigner la pièce qui occupe ce rang."""
        autre = un_evenement("une autre pièce, plus ancienne", self.d2013)
        autre_entree = entree(None, autre, "celle qui occupera P-12")

        rendu = citations.rendre(self.noeud)
        index = cc.index_cote_cible()
        self.assertEqual(index[self.e12.pk], "P-13")
        self.assertEqual(index[autre_entree.pk], "P-12",
                         "Une AUTRE pièce occupe désormais P-12.")
        self.assertIn("P-13", rendu['texte_rendu'])
        self.ancrage.refresh_from_db()
        self.assertEqual(self.ancrage.entree_id, self.e12.pk,
                         "L'ancrage désigne toujours la même source.")

    def test_une_citation_historique_litterale_reste_intacte(self):
        noeud = ajouter(self.racine, self.doc, "103",
                        "Au paragraphe 18, la défenderesse invoquait la pièce P-12.")
        pos = noeud.content_object.text.index("P-12")
        AncrageCitation.objects.create(
            noeud=noeud, entree=self.e12, libelle_ecrit="P-12",
            debut=pos, fin=pos + 4, litterale=True,
            note="cote rapportée d'un acte adverse")
        entree(None, un_evenement("ajout antérieur", self.d2013))

        rendu = citations.rendre(noeud)
        self.assertIn("pièce P-12.", rendu['texte_rendu'])
        self.assertEqual(rendu['remplacements'], [])
        self.assertEqual(rendu['litterales_preservees'], ["P-12"])

    def test_aucun_nombre_hors_citation_n_est_remplace(self):
        noeud = ajouter(self.racine, self.doc, "50",
                        "Le 19 juillet 2013, il a versé 12 000 $ "
                        "et cité le paragraphe 12 de la requête.")
        entree(None, un_evenement("ajout antérieur", self.d2013))
        rendu = citations.rendre(noeud)
        self.assertEqual(rendu['texte_rendu'], rendu['texte_stocke'])

    def test_une_reference_non_ancree_bloque(self):
        ajouter(self.racine, self.doc, "60",
                "Un paragraphe qui cite la pièce P-12 sans ancrage.")
        blocages = citations.citations_non_resolues(self.doc)
        self.assertTrue(any("sans ancrage" in b['motif'] for b in blocages))

    def test_une_reference_ambigue_bloque_jusqu_a_resolution(self):
        self.ancrage.ambigu = True
        self.ancrage.save()
        blocages = citations.citations_non_resolues(self.doc)
        self.assertTrue(any(b['motif'] == 'ambigu' for b in blocages))

        self.ancrage.ambigu = False
        self.ancrage.save()
        blocages = citations.citations_non_resolues(self.doc)
        self.assertEqual([b for b in blocages if b['noeud'] == self.noeud.pk], [])

    def test_un_texte_modifie_perime_les_positions_de_l_ancrage(self):
        st = self.noeud.content_object
        st.text = "Un texte entièrement réécrit, sans cote."
        st.save()
        rendu = citations.rendre(LibraryNode.objects.get(pk=self.noeud.pk))
        self.assertTrue(any("positions périmées" in n['motif']
                            for n in rendu['non_resolus']))

    def test_les_accents_et_guillemets_survivent_au_csv(self):
        restitution = {'lignes': [{
            'paragraphe_depose': "1", 'paragraphe_modifie': "2",
            'ancienne_cote': "P-12", 'nouvelle_cote': "P-13",
            'traitement': "REFORMULE", 'etat_traitement': "CONFIRME",
            'deplace': True, 'noeud_source': 1, 'noeud_cible': 2,
            'source_archivee': None, 'cible_archivee': None,
            'appuis_origine': [], 'appuis_retenus': [],
            'citations_non_resolues': [],
            'motif': 'des « guillemets », un accent é\net un saut de ligne',
            'note': "",
        }], 'verdicts': [], 'strict_possible': True, 'perimetre': {}}
        texte = exp.en_csv(restitution)
        import csv as csvmod
        import io as iomod
        lu = list(csvmod.DictReader(iomod.StringIO(texte)))
        self.assertEqual(lu[0]['motif'],
                         'des « guillemets », un accent é\net un saut de ligne')


# ---------------------------------------------------------------------------
# T23 — le cycle probatoire
# ---------------------------------------------------------------------------

class T23CycleProbatoire(BaseCotes):
    def setUp(self):
        super().setUp()
        self.schema = schema_acte()
        self.cible = faire_document("version 2", schema=self.schema)
        self.noeud = ajouter(racine_de(self.cible), self.cible, "1",
                             "un énoncé à appuyer")
        self.piece = entree("P-5", un_evenement("une pièce", self.d2015), rang=5)

    def _confirmer(self, portee="la date du fait"):
        st = LibraryNode.objects.get(pk=self.noeud.pk).content_object
        c = ConfirmationAppui.objects.create(
            noeud=self.noeud, entree=self.piece,
            version_examinee=VersionTexte.capter(st),
            etat=EtatAppui.CONFIRME, role="attestation", portee=portee,
            portee_sha256=ConfirmationAppui.empreinte_portee(portee),
            decide_le=timezone.now())
        return c

    def test_confirmer_V1_puis_reecrire_fait_retomber_en_reexamen(self):
        c = self._confirmer()
        self.assertEqual(c.etat_courant(), EtatAppui.CONFIRME)

        svc.detacher_pour_edition(LibraryNode.objects.get(pk=self.noeud.pk),
                                  "un énoncé V2")
        c.refresh_from_db()
        self.assertEqual(c.etat_courant(), EtatAppui.A_REEXAMINER)
        self.assertEqual(c.etat, EtatAppui.CONFIRME,
                         "La confirmation historique reste consultable.")
        self.assertEqual(c.version_examinee.texte, "un énoncé à appuyer",
                         "V1 reste lisible.")

    def test_reconfirmer_porte_sur_la_nouvelle_version(self):
        c = self._confirmer()
        svc.detacher_pour_edition(LibraryNode.objects.get(pk=self.noeud.pk),
                                  "un énoncé V2")
        nouveau = LibraryNode.objects.get(pk=self.noeud.pk).content_object
        c.version_examinee = VersionTexte.capter(nouveau)
        c.save()
        self.assertEqual(c.etat_courant(), EtatAppui.CONFIRME)

    def test_changer_la_portee_perime_la_confirmation(self):
        c = self._confirmer()
        c.portee = "la véracité de tout l'énoncé"
        c.save()
        self.assertEqual(c.etat_courant(), EtatAppui.A_REEXAMINER)

    def test_une_sauvegarde_sans_changement_conserve_la_confirmation(self):
        c = self._confirmer()
        st = LibraryNode.objects.get(pk=self.noeud.pk).content_object
        st.save()
        c.refresh_from_db()
        self.assertEqual(c.etat_courant(), EtatAppui.CONFIRME)

    def test_une_renumerotation_d_affichage_conserve_la_confirmation(self):
        c = self._confirmer()
        racine = LibraryNode.objects.get(document=self.cible, depth=1)
        nouveau = ajouter(racine, self.cible, "0", "un paragraphe en tête")
        nouveau.move(LibraryNode.objects.get(pk=self.noeud.pk), pos='left')
        c.refresh_from_db()
        self.assertEqual(c.etat_courant(), EtatAppui.CONFIRME)

    def test_une_absence_d_appui_documentee_suit_la_meme_regle(self):
        st = LibraryNode.objects.get(pk=self.noeud.pk).content_object
        c = ConfirmationAppui.objects.create(
            noeud=self.noeud, entree=None,
            version_examinee=VersionTexte.capter(st),
            etat=EtatAppui.SANS_APPUI,
            motif="l'énoncé est une qualification juridique, pas un fait")
        self.assertEqual(c.etat_courant(), EtatAppui.SANS_APPUI)
        svc.detacher_pour_edition(LibraryNode.objects.get(pk=self.noeud.pk), "V2")
        c.refresh_from_db()
        self.assertEqual(c.etat_courant(), EtatAppui.A_REEXAMINER)

    def test_les_appreciations_copiees_ne_valent_pas_confirmation(self):
        st = LibraryNode.objects.get(pk=self.noeud.pk).content_object
        self.assertTrue(st.is_true, "Valeur par défaut, non examinée.")
        c = ConfirmationAppui.objects.create(noeud=self.noeud, entree=self.piece)
        self.assertEqual(c.etat_courant(), EtatAppui.A_EXAMINER)

    def test_les_appuis_d_origine_restent_consultables_et_identifies(self):
        source = faire_document("acte déposé", schema=self.schema,
                                mode=NumberingMode.STORED)
        n_source = ajouter(racine_de(source), source, "44", "le fait d'origine",
                           numero="41")
        AppuiDepotJuillet.objects.create(
            statement=n_source.content_object, entree=self.piece,
            cote_citee="P-5")
        svc.relier(source, self.cible, [n_source], [self.noeud],
                   traitement=TraitementEditorial.REFORMULE)

        origines = svc.appuis_dorigine(self.noeud)
        self.assertEqual(len(origines), 1)
        self.assertEqual(origines[0]['cote_de_juillet'], "P-5")
        self.assertIn("VERSION SOURCE", origines[0]['origine'])
        self.assertEqual(
            ConfirmationAppui.objects.filter(noeud=self.noeud).count(), 0,
            "Un appui d'origine ne confirme pas automatiquement le nouveau texte.")

    def test_une_scission_ne_confirme_pas_automatiquement_ses_cibles(self):
        source = faire_document("acte déposé", schema=self.schema,
                                mode=NumberingMode.STORED)
        n_source = ajouter(racine_de(source), source, "4", "un fait scindé",
                           numero="4")
        AppuiDepotJuillet.objects.create(
            statement=n_source.content_object, entree=self.piece, cote_citee="P-5")
        c2 = ajouter(LibraryNode.objects.get(document=self.cible, depth=1),
                     self.cible, "2", "la seconde moitié")
        svc.relier(source, self.cible, [n_source], [self.noeud, c2],
                   traitement=TraitementEditorial.SCINDE)

        for n in (self.noeud, c2):
            self.assertEqual(len(svc.appuis_dorigine(n)), 1)
            self.assertEqual(
                ConfirmationAppui.objects.filter(noeud=n, etat=EtatAppui.CONFIRME)
                .count(), 0)


# ---------------------------------------------------------------------------
# T27 / T29 — les conditions de l'export strict
# ---------------------------------------------------------------------------

class T27ConditionsStrictes(BaseCotes):
    def setUp(self):
        super().setUp()
        self.schema = schema_acte()
        self.source = faire_document("acte déposé", schema=self.schema,
                                     mode=NumberingMode.STORED)
        self.n_source = ajouter(racine_de(self.source), self.source, "44",
                                "le fait d'origine", numero="41")
        self.ref = ReferentHistorique.objects.create(
            document=self.source, libelle="acte déposé de test")

        self.cible = faire_document("version 2", schema=self.schema)
        self.n_cible = ajouter(racine_de(self.cible), self.cible, "1",
                               "le fait réécrit")
        self.piece = entree("P-5", un_evenement("une pièce", self.d2015), rang=5)

        self.rep = tempfile.mkdtemp()
        self.chemin_lock = os.path.join(self.rep, "cotes.lock.json")
        ct = ContentType.objects.get_for_model(Event)
        with open(self.chemin_lock, "w", encoding="utf-8") as f:
            json.dump({"schema": "cotes.lock/1", "cotes": [
                {"cote": "P-5",
                 "identites_attendues": f"Event:{self.piece.object_id}"}]}, f)

    def _controle_referent(self, intact=True):
        return {'instantane': 1, 'empreinte': "x", 'intact': intact, 'ecarts': {}}

    def _tout_confirmer(self):
        corr = svc.relier(self.source, self.cible, [self.n_source], [self.n_cible],
                          traitement=TraitementEditorial.REFORMULE)
        svc.confirmer_traitement(corr, TraitementEditorial.REFORMULE,
                                 motif="réécriture décidée")
        st = LibraryNode.objects.get(pk=self.n_cible.pk).content_object
        ConfirmationAppui.objects.create(
            noeud=self.n_cible, entree=self.piece,
            version_examinee=VersionTexte.capter(st),
            etat=EtatAppui.CONFIRME, role="attestation", portee="la date",
            portee_sha256=ConfirmationAppui.empreinte_portee("la date"))
        return corr

    def _construire(self, intact=True):
        rapport = cc.reconcilier(self.chemin_lock)
        return exp.construire(self.source, self.cible, rapport,
                              self._controle_referent(intact))

    def test_chaque_condition_bloque_separement_puis_se_resout(self):
        # --- EX02 : aucune décision ---
        r = self._construire()
        self.assertFalse(self._satisfait(r, 'EX02'))
        corr = self._tout_confirmer()
        r = self._construire()
        self.assertTrue(self._satisfait(r, 'EX02'))
        self.assertTrue(self._satisfait(r, 'EX05'))

        # --- EX01 : référent dérivé ---
        r = self._construire(intact=False)
        self.assertFalse(self._satisfait(r, 'EX01'))

        # --- EX03 : numéro conservé manquant ---
        ajouter(LibraryNode.objects.get(document=self.source, depth=1),
                self.source, "45", "un paragraphe sans numéro conservé")
        r = self._construire()
        self.assertFalse(self._satisfait(r, 'EX03'))

    def _satisfait(self, restitution, code):
        return [v for v in restitution['verdicts']
                if v['condition'] == code][0]['satisfait']

    def test_EX04_bloque_sur_une_citation_non_ancree(self):
        self._tout_confirmer()
        st = LibraryNode.objects.get(pk=self.n_cible.pk).content_object
        st.text = "un énoncé citant la pièce P-5 sans ancrage"
        st.save()
        r = self._construire()
        self.assertFalse(self._satisfait(r, 'EX04'))

        noeud = LibraryNode.objects.get(pk=self.n_cible.pk)
        pos = noeud.content_object.text.index("P-5")
        AncrageCitation.objects.create(noeud=noeud, entree=self.piece,
                                       libelle_ecrit="P-5", debut=pos, fin=pos + 3)
        # Le texte a changé : il faut reconfirmer traitement et appuis.
        corr = svc.relier.__self__ if False else None
        from document_manager.models import Correspondance
        c = Correspondance.objects.get(document_source=self.source,
                                       document_cible=self.cible)
        svc.confirmer_traitement(c, TraitementEditorial.REFORMULE)
        conf = ConfirmationAppui.objects.get(noeud=noeud)
        conf.version_examinee = VersionTexte.capter(noeud.content_object)
        conf.save()

        r = self._construire()
        self.assertTrue(self._satisfait(r, 'EX04'))

    def test_EX05_refuse_une_confirmation_perimee_et_accepte_une_absence_motivee(self):
        corr = self._tout_confirmer()
        svc.detacher_pour_edition(LibraryNode.objects.get(pk=self.n_cible.pk), "V2")
        r = self._construire()
        self.assertFalse(self._satisfait(r, 'EX05'))
        self.assertFalse(self._satisfait(r, 'EX02'),
                         "Le traitement éditorial retombe aussi.")

        noeud = LibraryNode.objects.get(pk=self.n_cible.pk)
        ConfirmationAppui.objects.filter(noeud=noeud).delete()
        ConfirmationAppui.objects.create(
            noeud=noeud, entree=None,
            version_examinee=VersionTexte.capter(noeud.content_object),
            etat=EtatAppui.SANS_APPUI,
            motif="qualification juridique : aucune pièce ne l'établit")
        svc.confirmer_traitement(corr, TraitementEditorial.REFORMULE)

        r = self._construire()
        self.assertTrue(self._satisfait(r, 'EX05'),
                        "Une absence d'appui documentée est recevable.")

    def test_sans_appui_documente_exige_un_motif(self):
        self._tout_confirmer()
        noeud = LibraryNode.objects.get(pk=self.n_cible.pk)
        ConfirmationAppui.objects.filter(noeud=noeud).delete()
        ConfirmationAppui.objects.create(
            noeud=noeud, entree=None,
            version_examinee=VersionTexte.capter(noeud.content_object),
            etat=EtatAppui.SANS_APPUI, motif="")
        r = self._construire()
        self.assertFalse(self._satisfait(r, 'EX05'),
                         "Un champ vide ne vaut pas décision motivée.")

    def test_l_export_strict_est_refuse_puis_accepte(self):
        r = self._construire()
        self.assertFalse(r['strict_possible'])
        with self.assertRaises(exp.ExportStrictRefuse):
            exp.en_json(r, strict=True)
        self.assertTrue(exp.en_json(r, strict=False),
                        "Le diagnostique reste disponible.")

        self._tout_confirmer()
        r = self._construire()
        self.assertTrue(r['strict_possible'], r['verdicts'])
        self.assertTrue(exp.en_json(r, strict=True))
        self.assertTrue(exp.en_csv(r, strict=True))

    def test_deux_exports_du_meme_etat_sont_identiques(self):
        self._tout_confirmer()
        a = exp.en_json(self._construire())
        b = exp.en_json(self._construire())
        self.assertEqual(a, b)

    def test_la_table_ne_fabrique_pas_d_associations_probatoires(self):
        AppuiDepotJuillet.objects.create(
            statement=self.n_source.content_object, entree=self.piece,
            cote_citee="P-5")
        svc.relier(self.source, self.cible, [self.n_source], [self.n_cible],
                   traitement=TraitementEditorial.REFORMULE)
        r = self._construire()
        ligne = [l for l in r['lignes'] if l['noeud_cible'] == self.n_cible.pk][0]
        self.assertEqual(len(ligne['appuis_origine']), 1)
        self.assertEqual(ligne['appuis_retenus'], [],
                         "L'appui d'origine ne devient pas un appui retenu.")
        self.assertIsNone(ligne['nouvelle_cote'])


class T29DemonstrationIntegree(T27ConditionsStrictes):
    def test_le_parcours_complet(self):
        """Diagnostique → décisions → strict, avec les preuves à chaque étape."""
        r = self._construire()
        self.assertFalse(r['strict_possible'])
        bloquantes = {v['condition'] for v in r['verdicts'] if not v['satisfait']}
        self.assertIn('EX02', bloquantes)
        self.assertIn('EX05', bloquantes)

        corr = self._tout_confirmer()
        r = self._construire()
        self.assertTrue(r['strict_possible'])

        # Une réécriture rouvre les deux confirmations, séparément.
        svc.detacher_pour_edition(LibraryNode.objects.get(pk=self.n_cible.pk),
                                  "le fait, reformulé une seconde fois")
        r = self._construire()
        self.assertFalse(self._satisfait(r, 'EX02'))
        self.assertFalse(self._satisfait(r, 'EX05'))

        # Reconfirmer les seuls appuis ne lève pas EX02.
        noeud = LibraryNode.objects.get(pk=self.n_cible.pk)
        conf = ConfirmationAppui.objects.get(noeud=noeud)
        conf.version_examinee = VersionTexte.capter(noeud.content_object)
        conf.save()
        r = self._construire()
        self.assertTrue(self._satisfait(r, 'EX05'))
        self.assertFalse(self._satisfait(r, 'EX02'),
                         "La décision éditoriale est une décision distincte.")

        svc.confirmer_traitement(corr, TraitementEditorial.REFORMULE,
                                 motif="seconde reformulation décidée")
        r = self._construire()
        self.assertTrue(r['strict_possible'])
        self.assertTrue(exp.en_json(r, strict=True))
