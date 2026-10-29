from legal.verification_appuis.constat import capturer
from legal.verification_appuis.travail import liste_travail
from legal.verification_appuis.tests.aide import CasVA


class VA03(CasVA):
    def test_quatre_groupes_comptes_et_numero_imprime(self):
        s = self.source
        # Ordre du texte inverse de la priorité : reste, préjudice, actes, prescription.
        s["enonces"] += [{"id": 4, "ordre": 4, "texte": "Delta décrit le préjudice."},
                         {"id": 5, "ordre": 5, "texte": "Epsilon examine un acte."},
                         {"id": 6, "ordre": 6, "texte": "Zêta expose la prescription."}]
        for i, numero in ((4, "200"), (5, "75"), (6, "234")):
            self.concordance["lignes"].append({"incipit": s["enonces"][i-1]["texte"], "numero_imprime": numero})
        s["cotes"][2]["cote_racine"] = "P-19"
        s["liens"] += [{"id": 5, "statement_id": 4, "entree_id": 1, "cote_citee": "P-1", "via_liasse": False},
                        {"id": 6, "statement_id": 5, "entree_id": 3, "cote_citee": "P-19", "via_liasse": False},
                        {"id": 7, "statement_id": 6, "entree_id": 1, "cote_citee": "P-1", "via_liasse": False}]
        t = liste_travail(capturer(s, self.concordance))
        self.assertEqual([l["priorite"] for l in t["liens"]], sorted(l["priorite"] for l in t["liens"]))
        self.assertEqual(t["liens"][0]["numero_imprime"], "234")
        self.assertEqual(t["totaux"]["lignes"], len(s["liens"]) + 1)
        self.assertEqual(t["sans_reference"][0]["statement_id"], 3)
        self.assertTrue(any(l["numero_imprime"] == "41" for l in t["liens"]))
