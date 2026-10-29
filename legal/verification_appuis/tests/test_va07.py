from legal.verification_appuis.commun import Refus
from legal.verification_appuis.decisions import corriger, courantes, decider
from legal.verification_appuis.journal import proposer
from legal.verification_appuis.observations import lire_observations
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.tests.test_va04 import observation


def decision(oid, vid, action="VALIDER"):
    return {"auteur": "LP", "reference": "Décision LP FICTIVE, fixture de recette", "action": action,
            "observation_id": oid, "version_id": vid, "date": "2026-10-29T21:00:00+00:00"}


class VA07(CasVA):
    def test_proposer_valider_corriger_et_nouvelle_validation(self):
        p = self.repertoire / "attente.jsonl"
        proposer(p, observation())
        decider(p, decision("fixture-v1", "fixture-v2"))
        avant = p.read_bytes()
        corriger(p, "fixture-v3", "2026-10-29T22:00:00+00:00", {"remplace": "fixture-v2", "raison": "Correction inventée."})
        h = lire_observations(p)
        self.assertEqual(len(h), 3)
        self.assertEqual([o["remplace"] for o in h], [None, "fixture-v1", "fixture-v2"])
        self.assertTrue(p.read_bytes().startswith(avant))
        self.assertEqual(courantes(h)[1]["validee"]["id"], "fixture-v2")
        decider(p, decision("fixture-v3", "fixture-v4"))
        self.assertEqual(courantes(lire_observations(p))[1]["validee"]["id"], "fixture-v4")

    def test_rejet_lp_et_usurpation_refusee(self):
        p = self.repertoire / "attente.jsonl"
        proposer(p, observation())
        d = decision("fixture-v1", "fixture-v2")
        d["auteur"] = "CODEX"
        with self.assertRaisesRegex(Refus, "LP"):
            decider(p, d)
        decider(p, decision("fixture-v1", "fixture-v2", "REJETER"))
        etat = courantes(lire_observations(p))[1]
        self.assertIsNone(etat["validee"])
        self.assertEqual(etat["derniere"]["avancement"], "REJETE")
