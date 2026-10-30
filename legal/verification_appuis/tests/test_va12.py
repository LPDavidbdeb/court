from legal.verification_appuis.constat import capturer
from legal.verification_appuis.rapports import image_depot, markdown_image
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.tests.test_va04 import observation


class VA12(CasVA):
    def test_trois_liens_un_valide_deux_restes_et_parite_json_markdown(self):
        self.source["liens"] = [{"id": i, "statement_id": 1, "entree_id": i, "cote_citee": f"P-{i}", "via_liasse": False} for i in (1, 2, 3)]
        validee = observation()
        validee.update(id="fixture-validee", avancement="VALIDE", auteur="LP", decision_reference="LP FICTIF de recette")
        proposee = observation()
        proposee.update(id="fixture-proposee", liens=[2])
        image = image_depot(capturer(self.source, self.concordance), [validee, proposee])
        p = image["paragraphes"][0]
        self.assertEqual(p["numero_imprime"], "41")
        self.assertEqual(p["texte"], self.source["enonces"][0]["texte"])
        self.assertEqual(len(p["observations_validees"]), 1)
        self.assertEqual(len(p["restes"]), 2)
        self.assertEqual(len(p["propositions_en_attente"]), 1)
        md = markdown_image(image)
        self.assertIn("Observation validée fixture-validee", md)
        self.assertNotIn("Observation validée fixture-proposee", md)
        self.assertIn("lien 2 — PROPOSE", md)
        self.assertIn("lien 3 — NON_EXAMINE", md)
        self.assertIn(p["texte"], md)
