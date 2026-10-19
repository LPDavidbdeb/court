"""
L'oracle de P6 (verifier_ab.py), éprouvé seul sur des mesures fabriquées.

    python -m unittest discover -s scripts/regime_citations -p 'test_*.py'

Chaque cas négatif altère une seule chose — une surface, un service, une empreinte inscrite, la liste des
surfaces, une différence HTML non autorisée, une erreur nouvelle, le périmètre — et l'oracle doit la
refuser (code 1). Les cas positifs : mesures identiques, différences HTML autorisées seulement.
"""
import copy
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import projection as P  # noqa: E402
import verifier_ab as V  # noqa: E402

ADMIN = "/admin/argument_manager/tramenarrative/7/change/"
COURRIEL = "/emails/email/12/"
AFFIDAVIT = "/arguments/7/affidavit/"


def mesure(surfaces, services, secondaire, liste=None, meta=None, empreintes=None):
    m = {"surfaces": surfaces, "services": services, "secondaire": secondaire,
         "liste_des_surfaces": liste or P.empreinte(sorted(surfaces)),
         "meta": meta or {"base": "court_quote_regime_clone", "arbre": "/arbre/mesure", "surfaces": len(surfaces)}}
    e = {"surfaces": P.empreinte(surfaces), "services": P.empreinte(services), "secondaire": P.empreinte(secondaire)}
    e["canonique"] = P.empreinte([e["surfaces"], e["services"]])
    m["empreintes"] = empreintes or e
    return m


def base():
    surfaces = {
        COURRIEL: {"statut": 200, "ens_instanciees": ["email_quote:3"], "seq_marqueurs": ["email_quote:3"]},
        AFFIDAVIT: {"statut": 200, "seq_marqueurs": ["evidence:Quote:1", "evidence:Quote:6"]},
        ADMIN: {"statut": 200, "ens_instanciees": ["email_quote:3"]},
        "/emails/quote/9/": {"statut": 500},
    }
    services = {"cause:1:pieces": {"n": 2, "seq_pieces_produites": [{"label": "P-1"}, {"label": "P-1-1"}]}}
    secondaire = {COURRIEL: {"html": "h1"}, AFFIDAVIT: {"html": "h2"}, ADMIN: {"html": "h3"}, "/emails/quote/9/": {}}
    return surfaces, services, secondaire


def ecrire(chemin, texte):
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write(texte)


def verdict(a, b):
    with tempfile.TemporaryDirectory() as d:
        pa, pb = os.path.join(d, "a.json"), os.path.join(d, "b.json")
        ecrire(pa, json.dumps(a)); ecrire(pb, json.dumps(b))
        with redirect_stdout(StringIO()) as sortie:
            code = V.main(["ab", pa, pb])
    return code, sortie.getvalue()


class Positifs(unittest.TestCase):

    def test_identiques(self):
        a = mesure(*base())
        self.assertEqual(verdict(a, copy.deepcopy(a))[0], 0)

    def test_html_admin_trames_autorise(self):
        s, sv, sec = base()
        a = mesure(s, sv, sec)
        sec_b = copy.deepcopy(sec); sec_b[ADMIN] = {"html": "autre"}
        code, sortie = verdict(a, mesure(s, sv, sec_b))
        self.assertEqual(code, 0)
        self.assertIn("différences autorisées (1)", sortie)

    def test_erreur_preexistante_admise(self):
        a = mesure(*base())   # /emails/quote/9/ est en 500 dans A comme dans B
        self.assertEqual(verdict(a, copy.deepcopy(a))[0], 0)


class Negatifs(unittest.TestCase):

    def test_surface_modifiee(self):
        s, sv, sec = base()
        s_b = copy.deepcopy(s); s_b[AFFIDAVIT]["seq_marqueurs"] = ["evidence:Quote:6", "evidence:Quote:1"]
        self.assertEqual(verdict(mesure(s, sv, sec), mesure(s_b, sv, sec))[0], 1)

    def test_service_modifie(self):
        s, sv, sec = base()
        sv_b = copy.deepcopy(sv); sv_b["cause:1:pieces"]["seq_pieces_produites"][1]["label"] = "P-1-2"
        self.assertEqual(verdict(mesure(s, sv, sec), mesure(s, sv_b, sec))[0], 1)

    def test_empreinte_inscrite_alteree(self):
        a = mesure(*base())
        b = copy.deepcopy(a); b["empreintes"]["surfaces"] = "0" * 64
        code, sortie = verdict(a, b)
        self.assertEqual(code, 1)
        self.assertIn("intégrité de B", sortie)

    def test_empreinte_canonique_alteree_des_deux_cotes(self):
        a = mesure(*base())
        a["empreintes"]["canonique"] = "f" * 64
        b = copy.deepcopy(a)
        self.assertEqual(verdict(a, b)[0], 1)

    def test_liste_des_surfaces_differente(self):
        a = mesure(*base())
        b = copy.deepcopy(a); b["liste_des_surfaces"] = P.empreinte(["autre liste"])
        self.assertEqual(verdict(a, b)[0], 1)

    def test_surface_absente_de_b(self):
        s, sv, sec = base()
        s_b = copy.deepcopy(s); del s_b[COURRIEL]
        sec_b = copy.deepcopy(sec); del sec_b[COURRIEL]
        a = mesure(s, sv, sec)
        b = mesure(s_b, sv, sec_b, liste=a["liste_des_surfaces"])   # même liste déclarée, URL manquante
        self.assertEqual(verdict(a, b)[0], 1)

    def test_html_non_autorise(self):
        s, sv, sec = base()
        sec_b = copy.deepcopy(sec); sec_b[COURRIEL] = {"html": "autre"}
        code, sortie = verdict(mesure(s, sv, sec), mesure(s, sv, sec_b))
        self.assertEqual(code, 1)
        self.assertIn(COURRIEL, sortie)

    def test_admin_trame_modifiee_hors_html(self):
        # la catégorie autorisée ne vaut que pour le HTML secondaire, jamais pour la projection canonique
        s, sv, sec = base()
        s_b = copy.deepcopy(s); s_b[ADMIN]["ens_instanciees"] = ["email_quote:3", "email_quote:880001"]
        self.assertEqual(verdict(mesure(s, sv, sec), mesure(s_b, sv, sec))[0], 1)

    def test_erreur_nouvelle(self):
        s, sv, sec = base()
        s_b = copy.deepcopy(s); s_b[COURRIEL] = {"statut": 500}
        code, sortie = verdict(mesure(s, sv, sec), mesure(s_b, sv, sec))
        self.assertEqual(code, 1)
        self.assertIn("erreurs : aucune surface en erreur dans B", sortie)

    def test_arbre_different(self):
        s, sv, sec = base()
        b = mesure(s, sv, sec, meta={"base": "court_quote_regime_clone", "arbre": "/autre/arbre", "surfaces": 4})
        self.assertEqual(verdict(mesure(s, sv, sec), b)[0], 1)

    def test_entree_illisible(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.json"); ecrire(p, "pas du JSON")
            with redirect_stdout(StringIO()):
                self.assertEqual(V.main(["ab", p, p]), 2)


class T11(unittest.TestCase):

    CONFORME = {
        "tables_identiques": 87, "tables_divergentes": [], "tables_nouvelles": [],
        "colonnes_nouvelles": {"email_manager_quote": ["regime"], "pdf_manager_quote": ["regime"]},
        "email_manager_quote : PK et updated_at identiques": True, "email_manager_quote : par régime": {"HERITE": 268},
        "pdf_manager_quote : PK et updated_at identiques": True, "pdf_manager_quote : par régime": {"HERITE": 126},
        "migrations_ajoutees": [["email_manager", "0009_quote_regime"], ["pdf_manager", "0009_quote_regime"]],
    }

    def code(self, rapport, prefixe=""):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t11.txt"); ecrire(p, prefixe + json.dumps(rapport))
            with redirect_stdout(StringIO()):
                return V.main(["t11", p])

    def test_conforme(self):
        self.assertEqual(self.code(self.CONFORME, prefixe="sortie de script\n"), 0)

    def test_conforme_suivi_d_un_avertissement(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t11.txt"); ecrire(p, json.dumps(self.CONFORME) + "\nUserWarning: …\n")
            with redirect_stdout(StringIO()):
                self.assertEqual(V.main(["t11", p]), 0)

    def test_table_divergente(self):
        self.assertEqual(self.code(dict(self.CONFORME, tables_divergentes=["email_manager_email"])), 1)

    def test_colonne_en_trop(self):
        r = copy.deepcopy(self.CONFORME); r["colonnes_nouvelles"]["email_manager_email"] = ["x"]
        self.assertEqual(self.code(r), 1)

    def test_citation_phrase(self):
        self.assertEqual(self.code(dict(self.CONFORME, **{"pdf_manager_quote : par régime": {"HERITE": 125, "PHRASE": 1}})), 1)

    def test_migration_manquante(self):
        self.assertEqual(self.code(dict(self.CONFORME, migrations_ajoutees=[["email_manager", "0009_quote_regime"]])), 1)

    def test_pk_modifiees(self):
        self.assertEqual(self.code(dict(self.CONFORME, **{"email_manager_quote : PK et updated_at identiques": False})), 1)


if __name__ == "__main__":
    unittest.main()
