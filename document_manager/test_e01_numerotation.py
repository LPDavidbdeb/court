"""
Epic E01 — le moteur, sur fixtures.

CE QUE CE MODULE NE DÉMONTRE PAS. La fidélité de la reprise du dossier réel.
Une égalité obtenue sur des données inventées ici ne dit rien des 198 numéros
du papier : ce contrôle-là se fait sur une copie fidèle de la base, par
`reprendre_numeros_imprimes`, et ses résultats sont rapportés à part.

Les attentes sont écrites à la main, jamais produites par la fonction testée.
"""
import json
import os
import tempfile

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from contextlib import contextmanager

from django.db import transaction
from django.test import TestCase

from document_manager import concordance as svc
from document_manager import numerotation, referent as referent_service
from document_manager import reprise_numeros as rn
from document_manager.models import (
    Correspondance, Document, DocumentSource, EtatConfirmation,
    ExtremiteCorrespondance, FormatNumero, LibraryNode, NoeudArchive, Niveau,
    NumberingMode, PorteeNumero, ReferentHistorique, RoleExtremite, RoleNiveau,
    SchemaNiveaux, Statement, TraitementEditorial, VersionTexte,
)
from document_manager.protection import (
    ModificationRefusee, SuppressionRefusee, metadonnees_autorisees,
)


# ---------------------------------------------------------------------------
# Construction des fixtures
# ---------------------------------------------------------------------------

def schema_acte():
    """Racine, puis des paragraphes décimaux continus, puis des sous-items."""
    s = SchemaNiveaux.objects.create(nom="Acte de test")
    Niveau.objects.create(schema=s, profondeur=1, role=RoleNiveau.RACINE)
    Niveau.objects.create(schema=s, profondeur=2, role=RoleNiveau.PARAGRAPHE,
                          format_numero=FormatNumero.DECIMAL,
                          portee=PorteeNumero.DOCUMENT)
    Niveau.objects.create(schema=s, profondeur=3, role=RoleNiveau.SOUS_ITEM,
                          format_numero=FormatNumero.LETTRE_MIN,
                          portee=PorteeNumero.PARENT)
    return s


def faire_document(titre, source_type=DocumentSource.PRODUCED, schema=None,
                   mode=NumberingMode.AUTO):
    return Document.objects.create(title=titre, source_type=source_type,
                                   schema=schema, numbering_mode=mode)


def racine_de(document):
    return LibraryNode.add_root(document=document, item="Racine")


def ajouter(parent, document, item, texte, numero="", statement=None):
    ct = ContentType.objects.get_for_model(Statement)
    st = statement or Statement.objects.create(text=texte, is_user_created=True)
    return parent.add_child(document=document, item=item, content_type=ct,
                            object_id=st.pk, paragraph_number=numero)


@contextmanager
def refus_attendu(testcase, exception):
    """
    Attend un refus, et rend la transaction utilisable ensuite.

    Une garde qui lève dans `pre_delete` rompt la transaction que le collecteur
    de Django a ouverte — c'est précisément ce qui garantit l'absence de
    suppression partielle. Mais un `TestCase` enveloppe tout le test dans une
    seule transaction : sans point de reprise, la première assertion de refus
    empêcherait toutes les requêtes suivantes du même test.
    """
    with testcase.assertRaises(exception):
        with transaction.atomic():
            yield


class BaseE01(TestCase):
    def setUp(self):
        self.schema = schema_acte()


# ---------------------------------------------------------------------------
# T05 — les deux modes et le champ conservé
# ---------------------------------------------------------------------------

class T05ModesEtChamp(BaseE01):
    """AUTO par défaut, STORED explicite, suffixes et répétitions admis."""

    def test_auto_est_le_defaut_quel_que_soit_le_type_de_source(self):
        for st in (DocumentSource.PRODUCED, DocumentSource.REPRODUCED):
            d = faire_document(f"doc {st}", source_type=st)
            self.assertEqual(d.numbering_mode, NumberingMode.AUTO,
                             "Le mode ne se déduit pas de DocumentSource.")

    def test_stored_est_explicite(self):
        d = faire_document("acte", schema=self.schema, mode=NumberingMode.STORED)
        self.assertEqual(
            Document.objects.get(pk=d.pk).numbering_mode, NumberingMode.STORED)

    def test_suffixes_et_numeros_repetes_sont_admis(self):
        d = faire_document("acte", schema=self.schema, mode=NumberingMode.STORED)
        r = racine_de(d)
        ajouter(r, d, "a", "un", numero="22-A")
        ajouter(r, d, "b", "deux", numero="22-A")   # répété : la source le porte
        ajouter(r, d, "c", "trois", numero="7")
        index = numerotation.index_par_noeud(d)
        self.assertEqual(sorted(index.values()), ["22-A", "22-A", "7"])

    def test_le_numero_appartient_au_noeud_pas_au_statement(self):
        """Un même énoncé dans deux actes y porte deux numéros."""
        st = Statement.objects.create(text="énoncé partagé")
        d1 = faire_document("acte 1", schema=self.schema, mode=NumberingMode.STORED)
        d2 = faire_document("acte 2", schema=self.schema, mode=NumberingMode.STORED)
        n1 = ajouter(racine_de(d1), d1, "a", "", numero="41", statement=st)
        n2 = ajouter(racine_de(d2), d2, "a", "", numero="7", statement=st)
        self.assertEqual(numerotation.index_par_noeud(d1)[n1.pk], "41")
        self.assertEqual(numerotation.index_par_noeud(d2)[n2.pk], "7")


# ---------------------------------------------------------------------------
# T06, T07, T08, T09 — la résolution
# ---------------------------------------------------------------------------

class T06AutoSuitLaStructure(BaseE01):
    def test_inserer_et_deplacer_renumerote_en_auto(self):
        d = faire_document("cible", schema=self.schema)
        r = racine_de(d)
        a = ajouter(r, d, "a", "alpha")
        b = ajouter(r, d, "b", "beta")
        self.assertEqual(numerotation.index_par_noeud(d)[a.pk], "1")
        self.assertEqual(numerotation.index_par_noeud(d)[b.pk], "2")

        nouveau = ajouter(r, d, "c", "gamma")
        nouveau.move(a, pos='left')
        index = numerotation.index_par_noeud(d)
        self.assertEqual(index[LibraryNode.objects.get(pk=nouveau.pk).pk], "1")
        self.assertEqual(index[a.pk], "2")
        self.assertEqual(index[b.pk], "3")

    def test_une_valeur_conservee_ne_prend_pas_la_main_en_auto(self):
        d = faire_document("cible", schema=self.schema)   # AUTO
        n = ajouter(racine_de(d), d, "a", "alpha", numero="999")
        self.assertEqual(numerotation.index_par_noeud(d)[n.pk], "1")

    def test_la_lecture_ne_reecrit_pas_la_valeur_conservee(self):
        d = faire_document("cible", schema=self.schema)
        n = ajouter(racine_de(d), d, "a", "alpha", numero="999")
        numerotation.index_par_noeud(d)
        self.assertEqual(LibraryNode.objects.get(pk=n.pk).paragraph_number, "999")


class T07GenresConserventLeurTraitement(BaseE01):
    def test_enumeration_ne_recoit_pas_de_seconde_puce(self):
        d = faire_document("acte", schema=self.schema)
        p = ajouter(racine_de(d), d, "1", "un paragraphe")
        enum = ajouter(p, d, "", "a) Alexia David, née le 6 octobre 2009")
        scission = ajouter(p, d, "", "une scission de travail, sans puce")
        resolus = {r.noeud.pk: r for r in numerotation.resoudre(d)}
        self.assertEqual(resolus[enum.pk].genre, "enumeration")
        self.assertEqual(resolus[enum.pk].numero, "",
                         "La puce est déjà dans le texte.")
        self.assertEqual(resolus[scission.pk].genre, "sous_paragraphe")
        self.assertEqual(resolus[scission.pk].numero, "1a")

    def test_conclusion_et_mention_ne_recoivent_pas_de_faux_numero(self):
        d = faire_document("acte", schema=self.schema, mode=NumberingMode.STORED)
        r = racine_de(d)
        ajouter(r, d, "1", "paragraphe", numero="1")
        concl = ajouter(r, d, "C-1", "PAR CES MOTIFS…")
        mention = ajouter(r, d, "", "Montréal, le 24 juillet 2026")
        resolus = {x.noeud.pk: x for x in numerotation.resoudre(d)}
        self.assertEqual(resolus[concl.pk].genre, "conclusion")
        self.assertFalse(resolus[concl.pk].manquant,
                         "Une conclusion n'est pas un numéro manquant.")
        self.assertEqual(resolus[mention.pk].genre, "mention")
        self.assertFalse(resolus[mention.pk].manquant)


class T08FiltrerNeChangePasLeNumero(BaseE01):
    def test_le_sous_ensemble_porte_les_numeros_du_document_complet(self):
        from document_manager.views.new_views import _format_nodes_for_new_display
        d = faire_document("acte", schema=self.schema)
        r = racine_de(d)
        a = ajouter(r, d, "a", "alpha")
        piece = ajouter(r, d, "b", "une pièce")
        piece.is_evidence = True
        piece.save()
        c = ajouter(r, d, "c", "gamma")

        complet = numerotation.index_par_noeud(d)
        self.assertEqual(complet[c.pk], "3")

        filtres = _format_nodes_for_new_display(
            d.nodes.filter(depth__gt=1, is_evidence=False).order_by('path'), d)
        par_pk = {n.pk: n.numbering for n in filtres}
        # Le point est une ponctuation de liste, pas un second compteur.
        self.assertEqual(par_pk[a.pk], "1.")
        self.assertEqual(par_pk[c.pk], "3.",
                         "Masquer la pièce ne doit pas remonter gamma en 2.")


class T09DocumentSansSchema(BaseE01):
    """La grammaire héritée des vues, documentée, et non déduite d'`item`."""

    def test_la_grammaire_de_repli_est_celle_des_vues(self):
        d = faire_document("sans schéma", schema=None)
        r = racine_de(d)
        p1 = ajouter(r, d, "x", "premier")
        s1 = ajouter(p1, d, "y", "enfant")
        s2 = ajouter(p1, d, "z", "second enfant")
        pp = ajouter(s1, d, "w", "petit-enfant")
        p2 = ajouter(r, d, "v", "deuxième")

        index = numerotation.index_par_noeud(d)
        self.assertEqual(index[p1.pk], "1")
        self.assertEqual(index[s1.pk], "a")
        self.assertEqual(index[s2.pk], "b")
        self.assertEqual(index[pp.pk], "i")
        self.assertEqual(index[p2.pk], "2")

    def test_item_ne_fournit_aucun_numero(self):
        d = faire_document("sans schéma", schema=None)
        n = ajouter(racine_de(d), d, "43", "un texte")
        self.assertEqual(numerotation.index_par_noeud(d)[n.pk], "1",
                         "Le numéro vient de la structure, pas de `item`.")


# ---------------------------------------------------------------------------
# T10 — l'adaptateur par Statement
# ---------------------------------------------------------------------------

class T10IndexParStatement(BaseE01):
    def test_un_statement_repete_rend_l_index_ambigu(self):
        st = Statement.objects.create(text="répété")
        d = faire_document("acte", schema=self.schema, mode=NumberingMode.STORED)
        r = racine_de(d)
        ajouter(r, d, "a", "", numero="4", statement=st)
        ajouter(r, d, "b", "", numero="9", statement=st)

        with self.assertRaises(numerotation.AmbiguiteOccurrence):
            numerotation.index_par_statement(d)

        index, ambigus = numerotation.index_par_statement(d, strict=False)
        self.assertEqual(ambigus, {st.pk})
        self.assertNotIn(st.pk, index,
                         "Une ambiguïté ne se tranche pas par la première occurrence.")

    def test_numero_plaide_exige_un_document_quand_l_enonce_est_repris(self):
        from argument_manager.models import Axe, Fait
        st = Statement.objects.create(text="plaidé deux fois")
        d1 = faire_document("acte 1", schema=self.schema, mode=NumberingMode.STORED)
        d2 = faire_document("acte 2", schema=self.schema, mode=NumberingMode.STORED)
        ajouter(racine_de(d1), d1, "a", "", numero="41", statement=st)
        ajouter(racine_de(d2), d2, "a", "", numero="7", statement=st)

        Axe.objects.create(nom="axe de test")
        fait = Fait.objects.create(enonce="un fait", ordre=1, statement=st)
        self.assertIsNone(fait.numero_plaide(),
                          "Sans document, aucune occurrence ne doit être choisie.")
        self.assertEqual(fait.numero_plaide(document=d1), "41")
        self.assertEqual(fait.numero_plaide(document=d2), "7")


# ---------------------------------------------------------------------------
# T02, T11, T12, T13, T14, T15 — la reprise
# ---------------------------------------------------------------------------

class BaseReprise(BaseE01):
    """Un acte de 4 paragraphes dont les numéros du papier décalent."""

    LIGNES = [
        {"numero_md": "1", "numero_imprime": "1", "concorde": True, "suffixe": False},
        {"numero_md": "43", "numero_imprime": "41", "concorde": False, "suffixe": False},
        {"numero_md": "22-A", "numero_imprime": "22-A", "concorde": True, "suffixe": True},
        {"numero_md": "72", "numero_imprime": "67", "concorde": False, "suffixe": False},
    ]
    TEXTES = {
        "1": "La présente demande vise à faire declarer abusives les representations.",
        "43": "Le 26 juin 2013, le demandeur a ecrit a sa procureure.",
        "22-A": "Un paragraphe ajoute en cours de redaction.",
        "72": "Cette lettre refusait la garde partagee.",
    }

    def setUp(self):
        super().setUp()
        self.doc = faire_document("acte déposé", schema=self.schema)
        r = racine_de(self.doc)
        self.noeuds = {}
        for ligne in self.LIGNES:
            cle = ligne["numero_md"]
            self.noeuds[cle] = ajouter(r, self.doc, cle, self.TEXTES[cle])
        self.titre = ajouter(r, self.doc, "", "une mention de clôture")

        self.rep = tempfile.mkdtemp()
        self.chemin_conc = os.path.join(self.rep, "concordance.json")
        with open(self.chemin_conc, "w", encoding="utf-8") as f:
            json.dump({"lignes": [dict(l, incipit=self.TEXTES[l["numero_md"]][:40])
                                  for l in self.LIGNES]}, f)
        self.chemin_md = os.path.join(self.rep, "source.md")
        with open(self.chemin_md, "w", encoding="utf-8") as f:
            for cle, texte in self.TEXTES.items():
                f.write(f"{cle}. {texte}\n\n")

    def designer(self):
        ref = ReferentHistorique.objects.create(
            document=self.doc, libelle="acte déposé de test")
        return ref, referent_service.prendre_instantane(ref, "avant reprise")


class T12ModeRapport(BaseReprise):
    def test_le_controle_n_ecrit_rien(self):
        avant = list(LibraryNode.objects.filter(document=self.doc)
                     .values_list('pk', 'paragraph_number', 'item'))
        rapport = rn.verifier(self.doc, self.chemin_conc, self.chemin_md)
        apres = list(LibraryNode.objects.filter(document=self.doc)
                     .values_list('pk', 'paragraph_number', 'item'))
        self.assertTrue(rapport.conforme)
        self.assertEqual(avant, apres, "Le contrôle préalable ne doit rien écrire.")
        self.assertEqual(rapport.ecritures, 0)

    def test_l_application_ne_touche_pas_un_autre_document(self):
        autre = faire_document("autre acte", schema=self.schema)
        n = ajouter(racine_de(autre), autre, "43", "un texte voisin")
        self.designer()
        rn.appliquer(self.doc, self.chemin_conc, self.chemin_md)
        self.assertEqual(LibraryNode.objects.get(pk=n.pk).paragraph_number, "")


class T13DivergenceLegitime(BaseReprise):
    def test_item_43_devient_paragraph_number_41_sans_conflit(self):
        self.designer()
        rapport = rn.appliquer(self.doc, self.chemin_conc, self.chemin_md)
        n = LibraryNode.objects.get(pk=self.noeuds["43"].pk)
        self.assertEqual(n.item, "43", "`item` reste le numéro du Markdown.")
        self.assertEqual(n.paragraph_number, "41")
        self.assertEqual(rapport.conflits, [],
                         "La divergence item/numéro imprimé est légitime.")

    def test_les_suffixes_sont_conserves(self):
        self.designer()
        rn.appliquer(self.doc, self.chemin_conc, self.chemin_md)
        self.assertEqual(
            LibraryNode.objects.get(pk=self.noeuds["22-A"].pk).paragraph_number,
            "22-A")

    def test_mention_et_titre_ne_recoivent_pas_de_numero(self):
        self.designer()
        rn.appliquer(self.doc, self.chemin_conc, self.chemin_md)
        self.assertEqual(
            LibraryNode.objects.get(pk=self.titre.pk).paragraph_number, "")


class T14Idempotence(BaseReprise):
    def test_la_seconde_application_est_sans_effet(self):
        self.designer()
        premier = rn.appliquer(self.doc, self.chemin_conc, self.chemin_md)
        second = rn.appliquer(self.doc, self.chemin_conc, self.chemin_md)
        self.assertEqual(premier.ecritures, 4)
        self.assertEqual(second.ecritures, 0)

    def test_un_conflit_bloque_sans_ecrasement_ni_ecriture_partielle(self):
        self.designer()
        n = LibraryNode.objects.get(pk=self.noeuds["43"].pk)
        with metadonnees_autorisees():
            n.paragraph_number = "999"
            n.save(update_fields=['paragraph_number'])

        with self.assertRaises(rn.RattachementRefuse):
            rn.appliquer(self.doc, self.chemin_conc, self.chemin_md)

        self.assertEqual(
            LibraryNode.objects.get(pk=self.noeuds["43"].pk).paragraph_number,
            "999", "Le numéro présent ne doit pas être écrasé.")
        self.assertEqual(
            LibraryNode.objects.get(pk=self.noeuds["1"].pk).paragraph_number,
            "", "Aucune écriture partielle.")


class T04Refus(BaseReprise):
    """Chaque anomalie, prise séparément, bloque et n'écrit rien."""

    def _attendre_refus(self):
        with self.assertRaises(rn.RattachementRefuse):
            rn.appliquer(self.doc, self.chemin_conc, self.chemin_md)
        restants = set(LibraryNode.objects.filter(document=self.doc)
                       .values_list('paragraph_number', flat=True))
        self.assertEqual(restants, {""}, "Aucune écriture partielle.")

    def test_ligne_sans_noeud(self):
        self.designer()
        with open(self.chemin_conc, "w", encoding="utf-8") as f:
            json.dump({"lignes": self.LIGNES + [
                {"numero_md": "500", "numero_imprime": "480",
                 "concorde": False, "suffixe": False}]}, f)
        rapport = rn.verifier(self.doc, self.chemin_conc, self.chemin_md)
        self.assertEqual(len(rapport.manquantes), 1)
        self._attendre_refus()

    def test_correspondance_ambigue(self):
        self.designer()
        racine = LibraryNode.objects.get(document=self.doc, depth=1)
        ajouter(racine, self.doc, "43", "un homonyme de numéro")
        rapport = rn.verifier(self.doc, self.chemin_conc, self.chemin_md)
        self.assertEqual(len(rapport.ambigues), 1)
        self._attendre_refus()

    def test_contenu_modifie(self):
        self.designer()
        with open(self.chemin_md, "w", encoding="utf-8") as f:
            for cle, texte in self.TEXTES.items():
                altere = texte if cle != "43" else "Un texte entierement different."
                f.write(f"{cle}. {altere}\n\n")
        rapport = rn.verifier(self.doc, self.chemin_conc, self.chemin_md)
        self.assertEqual(len(rapport.contenus_incompatibles), 1)
        self._attendre_refus()

    def test_paragraphe_admissible_oublie(self):
        self.designer()
        r = LibraryNode.objects.get(document=self.doc, depth=1)
        ajouter(r, self.doc, "900", "un paragraphe que la table ignore")
        rapport = rn.verifier(self.doc, self.chemin_conc, self.chemin_md)
        self.assertEqual(len(rapport.oublies), 1)
        self._attendre_refus()

    def test_etat_change_entre_controle_et_application(self):
        ref, _ = self.designer()
        prealable = rn.verifier(self.doc, self.chemin_conc, self.chemin_md)
        self.assertTrue(prealable.conforme)

        # L'arbre change après le contrôle : l'appariement vérifié ne vaut plus.
        r = LibraryNode.objects.get(document=self.doc, depth=1)
        ajouter(r, self.doc, "43", "un second nœud portant le même item")

        with self.assertRaises(rn.RattachementRefuse):
            rn.appliquer(self.doc, self.chemin_conc, self.chemin_md,
                         rapport_prealable=prealable)
        restants = set(LibraryNode.objects.filter(document=self.doc)
                       .values_list('paragraph_number', flat=True))
        self.assertEqual(restants, {""})


class T15NouvelleImportation(BaseReprise):
    def test_sans_association_verifiee_aucun_numero_imprime(self):
        d = faire_document("import sans association", schema=self.schema)
        n = ajouter(racine_de(d), d, "43", "un texte importé")
        self.assertEqual(n.paragraph_number, "",
                         "Le libellé du Markdown n'est pas un numéro imprimé.")
        d.numbering_mode = NumberingMode.STORED
        d.save()
        resolus = {x.noeud.pk: x for x in numerotation.resoudre(d)}
        self.assertTrue(resolus[n.pk].manquant)
        self.assertEqual(resolus[n.pk].numero, "",
                         "Un numéro manquant n'est pas comblé par le calcul.")


class T03ControleApresReprise(BaseReprise):
    def test_chaque_valeur_est_controlee(self):
        self.designer()
        rn.appliquer(self.doc, self.chemin_conc, self.chemin_md)
        res = rn.controler_apres_reprise(self.doc, self.chemin_conc, self.chemin_md)
        self.assertEqual(res['controles'], 4)
        self.assertEqual(res['verifies'], 4)
        self.assertEqual(res['ecarts'], [])
        self.assertEqual(res['suffixes'], 1)
        self.assertEqual(res['divergents_du_markdown'], 2)


class T02ProtectionDuReferent(BaseReprise):
    def test_le_referent_produced_est_protege_comme_un_reproduced(self):
        self.designer()
        self.assertEqual(self.doc.source_type, DocumentSource.PRODUCED)
        n = LibraryNode.objects.get(pk=self.noeuds["1"].pk)
        with refus_attendu(self, SuppressionRefusee):
            n.delete()
        with refus_attendu(self, ModificationRefusee):
            st = n.content_object
            st.text = "un texte réécrit"
            st.save()

    def test_un_noeud_reproduced_est_protege_sans_referent(self):
        d = faire_document("acte reproduit", source_type=DocumentSource.REPRODUCED,
                           schema=self.schema)
        n = ajouter(racine_de(d), d, "1", "une citation")
        with refus_attendu(self, SuppressionRefusee):
            n.delete()
        with refus_attendu(self, SuppressionRefusee):
            LibraryNode.objects.filter(pk=n.pk).delete()

    def test_la_cascade_depuis_document_est_refusee(self):
        d = faire_document("acte reproduit", source_type=DocumentSource.REPRODUCED,
                           schema=self.schema)
        n = ajouter(racine_de(d), d, "1", "une citation")
        with refus_attendu(self, SuppressionRefusee):
            d.delete()
        self.assertTrue(LibraryNode.objects.filter(pk=n.pk).exists(),
                        "Aucune suppression partielle.")

    def test_item_et_arborescence_restent_figes(self):
        self.designer()
        n = LibraryNode.objects.get(pk=self.noeuds["1"].pk)
        n.item = "autre chose"
        with refus_attendu(self, ModificationRefusee):
            n.save()

    def test_le_numero_ne_s_ecrit_que_dans_un_bloc_autorise(self):
        self.designer()
        n = LibraryNode.objects.get(pk=self.noeuds["1"].pk)
        n.paragraph_number = "1"
        with refus_attendu(self, ModificationRefusee):
            n.save()
        with metadonnees_autorisees():
            n.save()
        self.assertEqual(LibraryNode.objects.get(pk=n.pk).paragraph_number, "1")

    def test_l_instantane_constate_que_seuls_les_numeros_ont_change(self):
        ref, inst = self.designer()
        rn.appliquer(self.doc, self.chemin_conc, self.chemin_md)
        ecarts = referent_service.comparer(inst)
        self.assertTrue(referent_service.contenu_intact(ecarts))
        self.assertEqual(len(ecarts['numeros']), 4)
        self.assertEqual(ecarts['textes'], [])
        self.assertEqual(ecarts['arborescence'], [])

    def test_les_antecedences_s_enregistrent_sans_T01(self):
        """Un lien se pose dès que les occurrences sont identifiées et protégées."""
        ref, _ = self.designer()
        cible = faire_document("version 2", schema=self.schema)
        nc = ajouter(racine_de(cible), cible, "1", "le même fait, réécrit")
        corr = svc.relier(self.doc, cible,
                          sources=[LibraryNode.objects.get(pk=self.noeuds["43"].pk)],
                          cibles=[nc], traitement=TraitementEditorial.REFORMULE)
        self.assertEqual(len(corr.noeuds_source()), 1)
        self.assertEqual(
            LibraryNode.objects.get(pk=self.noeuds["43"].pk).paragraph_number, "",
            "Aucun numéro n'est annoncé avant la reprise.")


class T11Migration(BaseE01):
    def test_les_champs_existent_avec_leurs_defauts(self):
        d = faire_document("doc")
        n = ajouter(racine_de(d), d, "1", "texte")
        self.assertEqual(d.numbering_mode, NumberingMode.AUTO)
        self.assertEqual(n.paragraph_number, "")
        champ = LibraryNode._meta.get_field('paragraph_number')
        self.assertEqual(champ.max_length, 30)
        self.assertTrue(champ.blank)


# ---------------------------------------------------------------------------
# T16, T18, T19, T20, T21, T22 — la concordance
# ---------------------------------------------------------------------------

class BaseConcordance(BaseE01):
    """La démonstration intégrée du cahier : source STORED, cible AUTO."""

    def setUp(self):
        super().setUp()
        self.source = faire_document("acte déposé", schema=self.schema,
                                     mode=NumberingMode.STORED)
        rs = racine_de(self.source)
        self.s = {}
        for item, numero, texte in (("1", "1", "le premier fait"),
                                    ("2", "2", "le deuxième fait"),
                                    ("4", "4", "un fait qui sera scindé"),
                                    ("4-A", "4-A", "un fait suffixé"),
                                    ("9", "9", "un fait à fusionner"),
                                    ("10", "10", "un fait retiré"),
                                    ("11", "11", "un fait sans décision")):
            self.s[item] = ajouter(rs, self.source, item, texte, numero=numero)

        self.ref = ReferentHistorique.objects.create(
            document=self.source, libelle="acte déposé de démonstration")

        self.cible = faire_document("version 2", schema=self.schema)
        rc = racine_de(self.cible)
        self.c = {}
        for i in range(1, 8):
            # `item` porte le numéro du brouillon de travail. Un item VIDE à la
            # profondeur des paragraphes désigne une mention de clôture, par la
            # convention de l'importateur : elle ne se numérote pas.
            self.c[i] = ajouter(rc, self.cible, str(i), f"paragraphe cible {i}")


class T18TraitementEditorial(BaseConcordance):
    def test_reformulation_deplacee_reste_descriptible(self):
        corr = svc.relier(self.source, self.cible, [self.s["2"]], [self.c[1]],
                          traitement=TraitementEditorial.REFORMULE, deplace=True)
        self.assertEqual(corr.traitement, TraitementEditorial.REFORMULE)
        self.assertTrue(corr.deplace,
                        "Déplacé ET reformulé : les deux doivent tenir ensemble.")

    def test_une_reecriture_fait_retomber_le_traitement_en_reexamen(self):
        corr = svc.relier(self.source, self.cible, [self.s["1"]], [self.c[3]],
                          traitement=TraitementEditorial.CONSERVE)
        svc.confirmer_traitement(corr, TraitementEditorial.CONSERVE,
                                 motif="texte identique")
        self.assertEqual(corr.etat_courant(), EtatConfirmation.CONFIRME)

        svc.detacher_pour_edition(self.c[3], "un texte V2, entièrement réécrit")
        corr.refresh_from_db()
        self.assertEqual(corr.etat_courant(), EtatConfirmation.A_REEXAMINER)
        self.assertEqual(corr.etat, EtatConfirmation.CONFIRME,
                         "La décision historique reste consultable.")
        self.assertTrue(corr.versions_cible_examinees.exists(),
                        "La version V1 examinée reste accessible.")

    def test_reconfirmer_les_appuis_ne_confirme_pas_le_traitement(self):
        from case_manager.models import ConfirmationAppui, EtatAppui
        corr = svc.relier(self.source, self.cible, [self.s["1"]], [self.c[3]],
                          traitement=TraitementEditorial.CONSERVE)
        svc.confirmer_traitement(corr, TraitementEditorial.CONSERVE)
        svc.detacher_pour_edition(self.c[3], "texte V2")

        noeud = LibraryNode.objects.get(pk=self.c[3].pk)
        ConfirmationAppui.objects.create(
            noeud=noeud, entree=None, etat=EtatAppui.SANS_APPUI,
            motif="aucune pièce n'est nécessaire",
            version_examinee=VersionTexte.capter(noeud.content_object))

        corr.refresh_from_db()
        self.assertEqual(corr.etat_courant(), EtatConfirmation.A_REEXAMINER,
                         "Les appuis ne valent pas décision éditoriale.")

        svc.confirmer_traitement(corr, TraitementEditorial.REFORMULE,
                                 motif="décision explicite sur le texte V2")
        corr.refresh_from_db()
        self.assertEqual(corr.etat_courant(), EtatConfirmation.CONFIRME)

    def test_une_renumerotation_d_affichage_conserve_la_confirmation(self):
        corr = svc.relier(self.source, self.cible, [self.s["1"]], [self.c[3]],
                          traitement=TraitementEditorial.CONSERVE)
        svc.confirmer_traitement(corr, TraitementEditorial.CONSERVE)
        avant = numerotation.index_par_noeud(self.cible)[self.c[3].pk]

        nouveau = ajouter(LibraryNode.objects.get(document=self.cible, depth=1),
                          self.cible, "0", "un paragraphe inséré en tête")
        nouveau.move(self.c[1], pos='left')

        apres = numerotation.index_par_noeud(self.cible)[self.c[3].pk]
        self.assertNotEqual(avant, apres, "Le numéro calculé a bien changé.")
        corr.refresh_from_db()
        self.assertEqual(corr.etat_courant(), EtatConfirmation.CONFIRME,
                         "Un déplacement n'est pas une réécriture.")
        self.assertEqual(len(corr.noeuds_cible()), 1, "Le lien tient.")


class T19Scission(BaseConcordance):
    def test_une_source_vers_deux_cibles(self):
        corr = svc.relier(self.source, self.cible, [self.s["4"]],
                          [self.c[4], self.c[5]],
                          traitement=TraitementEditorial.SCINDE)
        self.assertTrue(corr.est_scission)
        self.assertEqual(len(corr.noeuds_cible()), 2)
        for nc in corr.noeuds_cible():
            self.assertEqual([a.pk for a in svc.antecedents_de(nc)],
                             [self.s["4"].pk])


class T20Fusion(BaseConcordance):
    def test_deux_sources_vers_une_cible_sans_perte(self):
        corr = svc.relier(self.source, self.cible, [self.s["4-A"], self.s["9"]],
                          [self.c[2]], traitement=TraitementEditorial.FUSIONNE)
        self.assertTrue(corr.est_fusion)
        antecedents = {a.pk for a in svc.antecedents_de(self.c[2])}
        self.assertEqual(antecedents, {self.s["4-A"].pk, self.s["9"].pk},
                         "Un FK unique en aurait perdu un.")


class T21AjoutRetraitEtAbsenceDeDecision(BaseConcordance):
    def test_ajout_et_retrait_sont_des_decisions_explicites(self):
        ajout = svc.relier(self.source, self.cible, [], [self.c[6]],
                           traitement=TraitementEditorial.AJOUT,
                           motif="fait nouveau, décidé le 14 octobre")
        retrait = svc.relier(self.source, self.cible, [self.s["10"]], [],
                             traitement=TraitementEditorial.RETRAIT,
                             motif="retiré du récit")
        self.assertEqual(ajout.noeuds_source(), [])
        self.assertEqual(retrait.noeuds_cible(), [])

    def test_l_absence_de_lien_reste_a_etablir(self):
        from document_manager import export_concordance as exp
        restitution = exp.construire(self.source, self.cible)
        sans_decision = [l for l in restitution['lignes']
                         if l['correspondance'] is None]
        self.assertTrue(sans_decision)
        for l in sans_decision:
            self.assertEqual(l['etat_traitement'], EtatConfirmation.A_ETABLIR)
            self.assertNotIn(l['traitement'],
                             (TraitementEditorial.AJOUT, TraitementEditorial.RETRAIT))


class T22VoiesDeSuppression(BaseConcordance):
    def setUp(self):
        super().setUp()
        self.reproduit = faire_document("acte reproduit",
                                        source_type=DocumentSource.REPRODUCED,
                                        schema=self.schema)
        self.partage = Statement.objects.create(text="un énoncé cité partout")
        self.n_reproduit = ajouter(racine_de(self.reproduit), self.reproduit,
                                   "1", "", statement=self.partage)
        self.n_produit = ajouter(LibraryNode.objects.get(document=self.cible, depth=1),
                                 self.cible, "9", "", statement=self.partage)

    def test_noeud_reproduced_refuse_par_instance_lot_et_cascade(self):
        with refus_attendu(self, SuppressionRefusee):
            self.n_reproduit.delete()
        with refus_attendu(self, SuppressionRefusee):
            LibraryNode.objects.filter(pk=self.n_reproduit.pk).delete()
        with refus_attendu(self, SuppressionRefusee):
            self.reproduit.delete()
        self.assertTrue(LibraryNode.objects.filter(pk=self.n_reproduit.pk).exists())

    def test_statement_utilise_par_reproduced_est_refuse(self):
        with refus_attendu(self, SuppressionRefusee):
            self.partage.delete()
        with refus_attendu(self, SuppressionRefusee):
            Statement.objects.filter(pk=self.partage.pk).delete()
        self.assertTrue(Statement.objects.filter(pk=self.partage.pk).exists())

    def test_occurrence_produced_partagee_se_supprime_sans_perdre_le_statement(self):
        res = svc.supprimer_occurrence(self.n_produit, motif="retrait décidé")
        self.assertIn(self.n_produit.pk, res['noeuds_supprimes'])
        self.assertEqual(res['statements_supprimes'], [],
                         "Le Statement partagé avec REPRODUCED est conservé.")
        self.assertTrue(Statement.objects.filter(pk=self.partage.pk).exists())
        self.assertTrue(LibraryNode.objects.filter(pk=self.n_reproduit.pk).exists())

    def test_statement_exclusivement_produced_est_supprimable(self):
        noeud = self.c[7]
        sid = noeud.object_id
        res = svc.supprimer_occurrence(noeud, motif="retrait décidé")
        self.assertEqual(res['statements_supprimes'], [sid])
        self.assertFalse(Statement.objects.filter(pk=sid).exists())

    def test_un_bloc_contenant_un_noeud_protege_est_refuse_en_entier(self):
        bloc = ajouter(LibraryNode.objects.get(document=self.cible, depth=1),
                       self.cible, "8", "un bloc produit")
        enfant = ajouter(bloc, self.cible, "8a", "un enfant")
        # On rend le bloc protégé en le rattachant au référent par un détour :
        # un nœud du document source ne peut pas être supprimé.
        with refus_attendu(self, SuppressionRefusee):
            svc.supprimer_occurrence(self.s["1"])
        self.assertTrue(LibraryNode.objects.filter(pk=self.s["1"].pk).exists())
        self.assertTrue(LibraryNode.objects.filter(pk=enfant.pk).exists())

    def test_la_trace_d_une_suppression_reste_consultable(self):
        corr = svc.relier(self.source, self.cible, [self.s["1"]], [self.c[7]],
                          traitement=TraitementEditorial.CONSERVE)
        texte = self.c[7].content_object.text
        svc.supprimer_occurrence(self.c[7], motif="retrait décidé le 14 octobre")

        archive = NoeudArchive.objects.get(noeud_pk=self.c[7].pk)
        self.assertEqual(archive.texte, texte)
        self.assertEqual(archive.motif, "retrait décidé le 14 octobre")
        self.assertEqual(archive.document_id, self.cible.pk)

        extremite = ExtremiteCorrespondance.objects.get(
            correspondance=corr, role=RoleExtremite.CIBLE)
        self.assertIsNone(extremite.noeud_id)
        self.assertEqual(extremite.archive_id, archive.pk)

        corr.refresh_from_db()
        self.assertEqual([n.pk for n in corr.noeuds_source()], [self.s["1"].pk],
                         "L'antécédent n'est pas réputé retiré.")
        self.assertEqual(corr.traitement, TraitementEditorial.CONSERVE)


class T16EditionPartagee(BaseConcordance):
    def test_modifier_la_cible_cree_un_nouveau_statement(self):
        st = self.s["1"].content_object
        noeud_cible = self.c[1]
        noeud_cible.object_id = st.pk
        noeud_cible.save(update_fields=['object_id'])

        nouveau = svc.detacher_pour_edition(
            LibraryNode.objects.get(pk=noeud_cible.pk), "un texte V2")
        self.assertNotEqual(nouveau.pk, st.pk)
        self.assertEqual(Statement.objects.get(pk=st.pk).text, "le premier fait",
                         "Le texte de l'acte déposé est préservé.")
        self.assertEqual(
            LibraryNode.objects.get(pk=self.s["1"].pk).object_id, st.pk,
            "L'occurrence source continue de désigner le texte d'origine.")
