import json
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest


def exemple():
    enonces = [
        {"id": 1, "occurrence_id": 101, "ordre": 1, "numero_md": "43", "texte": "Alpha a écrit une lettre le 1er juin. P-1 et P-2."},
        {"id": 2, "occurrence_id": 102, "ordre": 2, "numero_md": "44", "texte": "Bêta a répondu le lendemain. P-1 et P-3."},
        {"id": 3, "occurrence_id": 103, "ordre": 3, "numero_md": "45", "texte": "Gamma rapporte une déclaration."},
    ]
    cotes = [{"id": i, "cote": f"P-{i}", "cote_racine": f"P-{i}", "rang": i,
              "sous_rang": None, "source_modele": "fixture.document", "source_id": i}
             for i in (1, 2, 3)]
    liens = [{"id": i, "statement_id": s, "entree_id": e, "cote_citee": f"P-{e}", "via_liasse": False}
             for i, (s, e) in enumerate(((1, 1), (1, 2), (2, 1), (2, 3)), 1)]
    concordance = {"lignes": [{"numero_md": str(43 + i), "numero_imprime": str(41 + i), "incipit": e["texte"][:25]}
                              for i, e in enumerate(enonces)]}
    return {"enonces": enonces, "liens": liens, "cotes": cotes}, concordance


def ecrire_fixture(chemin, source):
    with closing(sqlite3.connect(chemin)) as connexion, connexion:
        for nom in ("enonces", "liens", "cotes"):
            connexion.execute(f"CREATE TABLE {nom} (id INTEGER PRIMARY KEY, contenu TEXT NOT NULL)")
            connexion.executemany(f"INSERT INTO {nom} VALUES (?, ?)",
                                  [(e["id"], json.dumps(e, ensure_ascii=False)) for e in source[nom]])


class CasVA(unittest.TestCase):
    def setUp(self):
        self.temporaire = tempfile.TemporaryDirectory(prefix="court-va-fixture-")
        self.addCleanup(self.temporaire.cleanup)
        self.repertoire = Path(self.temporaire.name)
        self.source, self.concordance = exemple()
        self.base = self.repertoire / "synthetique.sqlite3"
        ecrire_fixture(self.base, self.source)
