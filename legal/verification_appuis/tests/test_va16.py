from legal.verification_appuis.commun import Refus
from legal.verification_appuis.constat import capturer
from legal.verification_appuis.pilote import verifier_perimetre_pilote
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.tests.test_va04 import observation


class VA16(CasVA):
    def preparation(self):
        for ligne, numero in zip(self.concordance["lignes"], ("234", "235", "236")):
            ligne["numero_imprime"] = numero
        c = capturer(self.source, self.concordance)
        enonces = {e["id"]: e for e in c["enonces"]}
        propositions = []
        for lien in c["liens"]:
            o = observation()
            o.update(id=f"fixture-pilote-{lien['id']}", liens=[lien["id"]],
                     empreinte_enonce=enonces[lien["statement_id"]]["empreinte_texte"])
            propositions.append(o)
        return c, propositions

    def test_pilote_complet_et_uniquement_propose(self):
        c, ps = self.preparation()
        self.assertEqual(verifier_perimetre_pilote(c, ps), [1, 2, 3, 4])

    def test_incomplet_hors_perimetre_et_decision_lp_refuses(self):
        c, ps = self.preparation()
        with self.assertRaisesRegex(Refus, "Périmètre"):
            verifier_perimetre_pilote(c, ps[:-1])
        ps[0]["auteur"] = "LP"
        ps[0]["avancement"] = "VALIDE"
        with self.assertRaisesRegex(Refus, "propositions CODEX"):
            verifier_perimetre_pilote(c, ps)
