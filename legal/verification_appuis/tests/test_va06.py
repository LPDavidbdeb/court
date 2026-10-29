from legal.verification_appuis.commun import Refus, empreinte
from legal.verification_appuis.journal import proposer
from legal.verification_appuis.observations import lire_observations
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.tests.test_va04 import observation


class VA06(CasVA):
    def test_ajout_conserve_octets_precedents_et_nouvelle_ligne_conforme(self):
        p = self.repertoire / "attente.jsonl"
        o = observation()
        proposer(p, o)
        avant = p.read_bytes()
        nouveau = observation()
        nouveau.update(id="fixture-v2", remplace=o["id"], raison="Précision inventée.")
        proposer(p, nouveau)
        self.assertEqual(empreinte(avant), empreinte(p.read_bytes()[:len(avant)]))
        self.assertEqual(len(lire_observations(p)), 2)
        self.assertEqual(lire_observations(p)[-1]["auteur"], "CODEX")

    def test_refuse_identite_fausse_validation_et_version_perimee(self):
        p = self.repertoire / "attente.jsonl"
        proposer(p, observation())
        avant = p.read_bytes()
        for champs in ({"id": "f2", "auteur": "CLAUDE"}, {"id": "f2", "avancement": "VALIDE", "auteur": "LP"}, {"id": "f2"}):
            o = observation()
            o.update(champs)
            with self.assertRaises(Refus):
                proposer(p, o)
            self.assertEqual(p.read_bytes(), avant)
