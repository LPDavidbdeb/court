import json
import sqlite3
import subprocess
import sys
from contextlib import closing

from legal.verification_appuis.commun import octets_json
from legal.verification_appuis.constat import capturer, enregistrer_constat
from legal.verification_appuis.tests.aide import CasVA


class VA02(CasVA):
    def setUp(self):
        super().setUp()
        enregistrer_constat(capturer(self.source, self.concordance), self.repertoire / "constat")
        self.table = self.repertoire / "concordance.json"
        self.table.write_bytes(octets_json(self.concordance))

    def lancer(self):
        return subprocess.run([sys.executable, "-B", "-m", "legal.verification_appuis.outil", "verifier_ancrage",
                               "--fixture", str(self.base), "--concordance", str(self.table),
                               "--constat", str(self.repertoire / "constat/constat.json")], capture_output=True, text=True)

    def test_concordance_code_zero(self):
        execution = self.lancer()
        self.assertEqual(execution.returncode, 0, execution.stderr)

    def test_mot_modifie_code_non_nul_enonce_nomme(self):
        ligne = self.source["enonces"][0].copy()
        ligne["texte"] = ligne["texte"].replace("lettre", "missive")
        with closing(sqlite3.connect(self.base)) as c, c:
            c.execute("UPDATE enonces SET contenu=? WHERE id=1", [json.dumps(ligne)])
        execution = self.lancer()
        self.assertNotEqual(execution.returncode, 0)
        self.assertIn("enonces 1", execution.stderr)

    def test_lien_supprime_code_non_nul_lien_nomme(self):
        with closing(sqlite3.connect(self.base)) as c, c:
            c.execute("DELETE FROM liens WHERE id=2")
        execution = self.lancer()
        self.assertNotEqual(execution.returncode, 0)
        self.assertIn("liens 2", execution.stderr)

    def test_cote_modifiee_et_capture_corrompue_refusees(self):
        ligne = self.source["cotes"][0].copy()
        ligne["source_id"] = 99
        with closing(sqlite3.connect(self.base)) as c, c:
            c.execute("UPDATE cotes SET contenu=? WHERE id=1", [json.dumps(ligne)])
        self.assertIn("cotes 1", self.lancer().stderr)
        p = self.repertoire / "constat/constat.json"
        p.write_bytes(p.read_bytes() + b" ")
        self.assertIn("Empreinte", self.lancer().stderr)
