import copy
from legal.verification_appuis.commun import Refus
from legal.verification_appuis.observations import valider_observation
from legal.verification_appuis.tests.aide import CasVA


def observation():
    return {"schema": "va-observation/1", "id": "fixture-v1", "liens": [1], "avancement": "PROPOSE",
            "auteur": "CODEX", "date": "2026-10-29T20:00:00+00:00", "empreinte_enonce": "a" * 64,
            "resultat": "RELATION_REPEREE", "element_observe": "Déclaration inventée.",
            "localisation": "fixture, ligne 1", "raison": "Même déclaration rapportée.",
            "supports": [{"chemin": "fixture.eml", "sha256": "b" * 64}], "remplace": None,
            "portee": "ETABLIT_L_ENONCE"}


class VA04(CasVA):
    def test_ligne_conforme(self):
        self.assertEqual(valider_observation(observation())["auteur"], "CODEX")

    def test_tous_les_refus_prescrits_et_rejet_reserve_a_lp(self):
        cas = [({"avancement": "NON_EXAMINE"}, "NON_EXAMINE"),
               ({"element_observe": "", "localisation": ""}, "élément observé"),
               ({"resultat": "AUCUNE_RELATION_REPEREE"}, "périmètre"),
               ({"resultat": "INDETERMINE"}, "obstacle"),
               ({"avancement": "VALIDE"}, "auteur LP"),
               ({"avancement": "REJETE"}, "auteur LP")]
        for changement, motif in cas:
            with self.subTest(changement=changement), self.assertRaisesRegex(Refus, motif):
                o = observation()
                o.update(changement)
                valider_observation(o)

    def test_non_examine_sans_resultat_et_decision_lp_fictive(self):
        o = observation()
        o.update(avancement="NON_EXAMINE", resultat=None)
        valider_observation(o)
        o.update(avancement="VALIDE", resultat="RELATION_REPEREE", auteur="LP", decision_reference="Décision LP fictive de recette")
        valider_observation(o)
