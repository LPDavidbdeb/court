from legal.verification_appuis.commun import Refus
from legal.verification_appuis.constat import capturer
from legal.verification_appuis.decisions import courantes
from legal.verification_appuis.liasses import preparer_liasse, verifier_rattachement
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.tests.test_va04 import observation


class VA10(CasVA):
    def setUp(self):
        super().setUp()
        for c in self.source["cotes"]:
            c.update(cote=f"P-43.{c['id']}", cote_racine="P-43", sous_rang=c["id"])
        self.source["liens"] = [{"id": i, "statement_id": 1, "entree_id": i, "cote_citee": "P-43", "via_liasse": True} for i in (1, 2, 3)]
        self.constat = capturer(self.source, self.concordance)
        self.base_obs = observation()
        self.base_obs["empreinte_enonce"] = self.constat["enonces"][0]["empreinte_texte"]
        self.membres = [{"lien_id": i, "entree_id": i, "supports": [{"chemin": f"fixture-{i}.eml", "sha256": str(i) * 64}]} for i in (1, 2, 3)]

    def test_une_observation_couvre_trois_liens(self):
        o = preparer_liasse(self.constat, [1, 2, 3], list(reversed(self.membres)), self.base_obs)
        self.assertEqual(o["liens"], [1, 2, 3])
        self.assertEqual(len(courantes([o])), 3)
        verifier_rattachement(o, self.constat)

    def test_sous_cote_nommee_refusee(self):
        self.constat["liens"][1]["via_liasse"] = False
        with self.assertRaisesRegex(Refus, "sous-cote"):
            preparer_liasse(self.constat, [1, 2, 3], self.membres, self.base_obs)

    def test_manifeste_incomplet_ne_couvre_pas_le_membre_absent(self):
        o = preparer_liasse(self.constat, [1, 2, 3], self.membres[:2], self.base_obs)
        self.assertEqual(o["liens"], [1, 2])
        self.assertEqual(o["liens_non_examines"], [3])
        self.assertNotIn(3, courantes([o]))
