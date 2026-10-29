from legal.verification_appuis.constat import capturer
from legal.verification_appuis.observations import valider_observation
from legal.verification_appuis.rapports import couverture
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.tests.test_va04 import observation


class VA11(CasVA):
    def test_dix_liens_partition_et_absence_de_resultat_non_examine(self):
        self.source["cotes"] = [{"id": i, "cote": f"P-{i}", "cote_racine": f"P-{i}", "rang": i} for i in range(1, 11)]
        self.source["liens"] = [{"id": i, "statement_id": 1, "entree_id": i, "cote_citee": f"P-{i}", "via_liasse": False} for i in range(1, 11)]
        historique = []
        for i, avancement in enumerate(("PROPOSE", "VALIDE", "REJETE", "A_REVOIR", "VALIDE", "PROPOSE", "VALIDE", "REJETE"), 2):
            o = observation()
            o.update(id=f"fixture-{i}", liens=[i], avancement=avancement)
            if avancement in {"VALIDE", "REJETE"}:
                o.update(auteur="LP", decision_reference="Décision LP FICTIVE")
            if i == 2:
                o["ecarts"] = [{"type": "DATE", "description": "Écart fictif."}, {"type": "CITATION", "description": "Citation fictive."}]
            valider_observation(o)
            historique.append(o)
        r = couverture(capturer(self.source, self.concordance), historique)
        self.assertEqual(r["denominateur"], 10)
        self.assertEqual(sum(r["comptes"].values()), 10)
        self.assertEqual(r["comptes"]["NON_EXAMINE"], 2)
        self.assertTrue(all(e["resultat"] is None for e in r["liens"] if e["avancement"] == "NON_EXAMINE"))
        self.assertEqual({e["type"] for e in r["ecarts"]}, {"DATE", "CITATION"})
        self.assertEqual(len(r["sans_reference"]), 2)
