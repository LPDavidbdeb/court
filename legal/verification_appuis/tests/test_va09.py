from legal.verification_appuis.commun import Refus
from legal.verification_appuis.observations import valider_observation
from legal.verification_appuis.rapports import rapport_ecarts
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.tests.test_va04 import observation


class VA09(CasVA):
    def test_date_et_citation_toutes_deux_rapportees(self):
        o = observation()
        o["ecarts"] = [{"type": "CITATION", "description": "Mots différents dans la fixture."},
                       {"type": "DATE", "description": "Dates différentes dans la fixture."}]
        valider_observation(o)
        self.assertEqual({e["type"] for e in rapport_ecarts([o])}, {"DATE", "CITATION"})

    def test_type_inconnu_ou_description_absente_refuse(self):
        for ecart in ({"type": "AUTRE", "description": "Test"}, {"type": "DATE"}):
            o = observation()
            o["ecarts"] = [ecart]
            with self.assertRaisesRegex(Refus, "ecart"):
                valider_observation(o)

    def test_compatible_avec_chaque_resultat(self):
        for resultat in ("RELATION_REPEREE", "AUCUNE_RELATION_REPEREE", "INDETERMINE"):
            o = observation()
            o.update(resultat=resultat, perimetre_lu="Fixture entière", obstacle="Fixture illisible",
                     ecarts=[{"type": "IDENTITE_PIECE", "description": "Identité à vérifier dans la fixture."}])
            valider_observation(o)
