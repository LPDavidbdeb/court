from legal.verification_appuis.commun import Refus, empreinte
from legal.verification_appuis.constat import capturer
from legal.verification_appuis.fiches import construire_fiches
from legal.verification_appuis.tests.aide import CasVA


class VA05(CasVA):
    def test_manifeste_ancien_objet_email_refuse(self):
        m = self.manifeste()
        self.source["cotes"][0].update(source_modele="email_manager.email", source_id=4)
        m["cotes"][0]["fichiers"][0].update(modele="email_manager.Email", pk=330)
        with self.assertRaisesRegex(Refus, "identité du manifeste"):
            construire_fiches(capturer(self.source, self.concordance), m)
        m["cotes"][0]["fichiers"][0]["pk"] = 4
        self.assertFalse(construire_fiches(capturer(self.source, self.concordance), m)["liens_avec_obstacle"])

    def test_racine_transcriptions_limitee_aux_sept_pdf_dictes(self):
        from legal.verification_appuis.commun import RACINE
        from legal.verification_appuis.fiches import support_autorise
        self.assertEqual(support_autorise(RACINE / "pieces_pdf/P-58.pdf"), (RACINE / "pieces_pdf/P-58.pdf").resolve())
        with self.assertRaisesRegex(Refus, "hors des racines"):
            support_autorise(RACINE / "pieces_pdf/P-57.pdf")

    def manifeste(self):
        m = {"cotes": []}
        for cote in self.source["cotes"]:
            photo = cote["id"] == 2
            p = self.repertoire / (f"photo{cote['id']}.jpg" if photo else f"courriel{cote['id']}.eml")
            p.write_bytes(b"Photo inventee" if photo else b"Subject: Fixture\n\nDeclaration inventee.")
            m["cotes"].append({"cote": cote["cote"], "fichiers": [{"chemin": str(p), "sha256_source": empreinte(p.read_bytes()),
                               "qualification": "dérivé en base" if photo else "fichier conservé en base", "champ": "file"}]})
        return m

    def test_courriel_photo_empreintes_et_qualification(self):
        m = self.manifeste()
        r = construire_fiches(capturer(self.source, self.concordance), m)
        self.assertEqual(len(r["fiches"]), 4)
        for f in r["fiches"]:
            for s in f["supports"]:
                from pathlib import Path
                self.assertEqual(s["sha256"], empreinte(Path(s["chemin"]).read_bytes()))
        self.assertEqual(r["fiches"][1]["supports"][0]["qualification"], "dérivé en base")
        self.assertEqual(r["fiches"][0]["enonce"]["texte"], self.source["enonces"][0]["texte"])

    def test_support_change_refuse_et_scan_exige(self):
        m = self.manifeste()
        m["cotes"][0]["fichiers"][0]["sha256_source"] = "0" * 64
        with self.assertRaisesRegex(Refus, "divergent"):
            construire_fiches(capturer(self.source, self.concordance), m)
        m = self.manifeste()
        self.source["cotes"][0]["cote_racine"] = "P-19"
        with self.assertRaisesRegex(Refus, "scan"):
            construire_fiches(capturer(self.source, self.concordance), m)
