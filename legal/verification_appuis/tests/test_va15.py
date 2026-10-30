from legal.verification_appuis.commun import Refus
from legal.verification_appuis.constat import capturer
from legal.verification_appuis.fragments import liste_paragraphes_fragments
from legal.verification_appuis.tests.aide import CasVA


class VA15(CasVA):
    def test_deux_fragments_figurent_un_seul_ny_figure_pas(self):
        c = capturer(self.source, self.concordance)
        fs = []
        for identifiant, sid, a, b in (("f1", 1, 0, 5), ("f2", 1, 6, 14), ("f3", 2, 0, 4)):
            e = c["enonces"][sid-1]
            fs.append({"id": identifiant, "statement_id": sid, "debut": a, "fin": b, "extrait": e["texte"][a:b],
                       "empreinte_enonce": e["empreinte_texte"], "statut": "VALIDE", "auteur": "LP",
                       "decision_reference": "LP FICTIF de recette"})
        r = liste_paragraphes_fragments(c, fs)
        self.assertEqual([p["statement_id"] for p in r["paragraphes"]], [1])
        self.assertEqual(r["fragments_valides"], 3)
        fs[0]["extrait"] = "Reformulation interdite"
        with self.assertRaisesRegex(Refus, "littéral"):
            liste_paragraphes_fragments(c, fs)

    def test_aucun_fragment_valide_aucune_conclusion_positive(self):
        r = liste_paragraphes_fragments(capturer(self.source, self.concordance), [])
        self.assertEqual(r["paragraphes"], [])
        self.assertEqual(r["fragments_valides"], 0)
