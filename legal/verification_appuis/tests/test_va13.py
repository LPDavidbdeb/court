import copy
from legal.verification_appuis.commun import empreinte, octets_json
from legal.verification_appuis.constat import capturer
from legal.verification_appuis.derives import detecter_derives
from legal.verification_appuis.rapports import couverture, image_depot
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.tests.test_va04 import observation


class VA13(CasVA):
    def test_nouvelle_proposition_sur_cote_corrigee_et_ancien_objet_perime(self):
        c, h = self.preparation()
        c["cotes"][0].update(source_modele="fixture.document", source_id=330)
        h[0]["supports"][0]["identite"] = {"modele":"fixture.Document", "pk":330}
        actuel = copy.deepcopy(c)
        actuel["cotes"][0]["source_id"] = 4
        # Même sans l'ancien constat, l'ancienne proposition reste périmée.
        self.assertEqual(detecter_derives(actuel, h)["observations_a_revoir"], ["fixture-1"])
        nouvelle = copy.deepcopy(h[0])
        nouvelle.update(id="fixture-refaite", empreintes_cotes={"1":empreinte(octets_json(actuel["cotes"][0]))})
        nouvelle["supports"][0]["identite"]["pk"] = 4
        # L'ancien état de cote ne doit pas périmer la version refaite sur le nouvel état.
        self.assertEqual(detecter_derives(c, [h[0], nouvelle], actuel)["observations_a_revoir"], ["fixture-1"])
        suivant = copy.deepcopy(actuel)
        suivant["cotes"][0]["source_ref"] = "modification ultérieure"
        self.assertEqual(detecter_derives(actuel, [nouvelle], suivant)["observations_a_revoir"], ["fixture-refaite"])

    def preparation(self):
        c = capturer(self.source, self.concordance)
        h = []
        for i in (1, 2):
            p = self.repertoire / f"source-{i}.eml"
            p.write_bytes(f"Fixture {i}".encode())
            o = observation()
            o.update(id=f"fixture-{i}", liens=[i], avancement="VALIDE", auteur="LP", decision_reference="LP FICTIF de recette",
                     empreinte_enonce=c["enonces"][0]["empreinte_texte"], supports=[{"chemin": str(p), "sha256": empreinte(p.read_bytes())}])
            h.append(o)
        return c, h

    def test_support_change_a_revoir_autre_valide_et_histoire_intacte(self):
        c, h = self.preparation()
        avant = octets_json(h)
        (self.repertoire / "source-1.eml").write_bytes(b"Fixture modifiee")
        d = detecter_derives(c, h)
        self.assertEqual(d["observations_a_revoir"], ["fixture-1"])
        r = couverture(c, h, d["observations_a_revoir"])
        self.assertEqual([e["avancement"] for e in r["liens"][:2]], ["A_REVOIR", "VALIDE"])
        self.assertEqual(octets_json(h), avant)
        image = image_depot(c, h, d["observations_a_revoir"])
        self.assertEqual([o["id"] for o in image["paragraphes"][0]["observations_validees"]], ["fixture-2"])

    def test_texte_et_lien_changes_detectes(self):
        c, h = self.preparation()
        actuel = copy.deepcopy(c)
        actuel["enonces"][0]["texte"] += " changement"
        self.assertEqual(len(detecter_derives(c, h, actuel)["observations_a_revoir"]), 2)
        actuel = copy.deepcopy(c)
        actuel["liens"] = [l for l in actuel["liens"] if l["id"] != 1]
        self.assertEqual(detecter_derives(c, h, actuel)["observations_a_revoir"], ["fixture-1"])
