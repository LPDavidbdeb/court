import copy
from legal.verification_appuis.commun import Refus
from legal.verification_appuis.constat import capturer
from legal.verification_appuis.pilote import verifier_perimetre_pilote
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.tests.test_va04 import observation


class VA16(CasVA):
    def test_recette_dictee_six_sur_sept_et_histoire_conservee(self):
        from legal.verification_appuis.recette_pilote import appliquer_recette
        from legal.verification_appuis.journal import proposer
        from legal.verification_appuis.observations import lire_observations
        from legal.verification_appuis.rapports import couverture
        c = capturer(self.source, self.concordance)
        c["liens"] = [{"id":i,"statement_id":1,"entree_id":1,"cote_citee":"P-1","via_liasse":False} for i in range(468,475)]
        journal = self.repertoire / "recette_fictive.jsonl"
        for i in range(468,475):
            o = observation()
            o.update(id=f"VA16-L{i}-v1",liens=[i],empreinte_enonce=c["enonces"][0]["empreinte_texte"])
            o["ecarts"] = [{"type":"DATE","description":"DATE FICTIVE initiale"}] if i==469 else []
            proposer(journal,o,c)
        avant=journal.read_bytes()
        nouvelle=copy.deepcopy(lire_observations(journal)[4])
        nouvelle.update(id="VA16-L472-v2",remplace="VA16-L472-v1")
        appliquer_recette(journal,c,nouvelle,"2026-10-29T20:00:00-04:00",reference="LP FICTIF — test synthétique",texte_date="Dictée FICTIVE de correction")
        h=lire_observations(journal)
        self.assertTrue(journal.read_bytes().startswith(avant))
        self.assertEqual(len(h),15)
        r=couverture(c,h)
        self.assertEqual(r["comptes"]["VALIDE"],6)
        self.assertEqual(r["comptes"]["PROPOSE"],1)
        self.assertEqual(next(x for x in r["liens"] if x["lien_id"]==472)["avancement"],"PROPOSE")
        self.assertEqual(h[1]["ecarts"][0]["description"],"DATE FICTIVE initiale")

    def test_correction_date_ne_change_que_la_description_dictee(self):
        from legal.verification_appuis.recette_pilote import ecarts_date_corriges
        o=observation()
        o["ecarts"]=[{"type":"DATE","description":"avant"},{"type":"SENS","description":"conservé"}]
        avant=copy.deepcopy(o)
        ecarts=ecarts_date_corriges(o,"dictée exacte")
        self.assertEqual(o,avant)
        self.assertEqual(ecarts,[{"type":"DATE","description":"dictée exacte"},{"type":"SENS","description":"conservé"}])

    def test_grille_v11_exige_degre_sans_invalider_historique(self):
        from legal.verification_appuis.observations import valider_observation
        o=observation();o["ecarts"]=[{"type":"SENS","description":"Écart FICTIF"}]
        valider_observation(o)
        o["grille_version"]="1.1"
        with self.assertRaisesRegex(Refus,"degré"):
            valider_observation(o)
        o["ecarts"][0]["degre"]="CONTREDIT"
        valider_observation(o)

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
