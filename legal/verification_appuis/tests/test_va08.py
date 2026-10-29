from legal.verification_appuis.commun import Refus
from legal.verification_appuis.observations import valider_observation
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.tests.test_va04 import observation


class VA08(CasVA):
    def test_portee_absente_refusee(self):
        o = observation()
        o.pop("portee")
        with self.assertRaisesRegex(Refus, "portee"):
            valider_observation(o)

    def test_partie_sans_reste_refusee_puis_acceptee(self):
        o = observation()
        o["portee"] = "EN_ETABLIT_UNE_PARTIE"
        with self.assertRaisesRegex(Refus, "reste_sans_piece"):
            valider_observation(o)
        o["reste_sans_piece"] = "Le motif allégué ne figure pas dans cette fixture."
        valider_observation(o)

    def test_etablit_sans_reste_accepte_et_valeur_inconnue_refusee(self):
        valider_observation(observation())
        o = observation()
        o["portee"] = "VRAI_DANS_LA_REALITE"
        with self.assertRaisesRegex(Refus, "portee"):
            valider_observation(o)
