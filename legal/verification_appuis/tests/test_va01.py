from legal.verification_appuis.commun import Refus
from legal.verification_appuis.constat import capturer, enregistrer_constat, lire_fixture
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.source_django import lire_source_reelle


class VA01(CasVA):
    def test_aucun_acces_reel_sans_accord(self):
        with self.assertRaisesRegex(Refus, "accord explicite"):
            lire_source_reelle(None)

    def test_deux_generations_et_numero_imprime_decale(self):
        constat = capturer(lire_fixture(self.base), self.concordance)
        enregistrer_constat(constat, self.repertoire / "a")
        enregistrer_constat(capturer(lire_fixture(self.base), self.concordance), self.repertoire / "b")
        for nom in ("constat.json", "SHA256SUMS"):
            self.assertEqual((self.repertoire / "a" / nom).read_bytes(), (self.repertoire / "b" / nom).read_bytes())
        self.assertEqual(len(constat["enonces"]), 3)
        self.assertEqual(len(constat["liens"]), 4)
        self.assertEqual(constat["enonces"][0]["numero_imprime"], "41")
        self.assertEqual(constat["enonces"][0]["numero_md"], "43")

    def test_numero_stocke_identique_a_limprime_accepte(self):
        self.source["enonces"][0]["numero_stocke"] = "41"
        constat = capturer(self.source, self.concordance)
        self.assertEqual(constat["enonces"][0]["numero_stocke"], "41")
        self.assertEqual(constat["enonces"][0]["numero_imprime"], "41")
        self.assertEqual(constat["enonces"][0]["numero_md"], "43")

    def test_numero_stocke_divergent_refuse_et_enonce_nomme(self):
        self.source["enonces"][0]["numero_stocke"] = "43"
        with self.assertRaisesRegex(Refus, "Numéro stocké divergent pour l'énoncé 1 : 43 / 41"):
            capturer(self.source, self.concordance)

    def test_refuse_ecrasement_et_appariement_ambigu(self):
        constat = capturer(self.source, self.concordance)
        enregistrer_constat(constat, self.repertoire / "a")
        constat["enonces"][0]["texte"] += " altération"
        with self.assertRaisesRegex(Refus, "écrasement"):
            enregistrer_constat(constat, self.repertoire / "a")
        self.concordance["lignes"].append(self.concordance["lignes"][0].copy())
        with self.assertRaisesRegex(Refus, "ambigu"):
            capturer(self.source, self.concordance)
