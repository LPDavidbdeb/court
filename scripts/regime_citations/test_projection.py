"""
Les règles de la projection, éprouvées seules (sans Django ni base).

    python -m unittest discover -s scripts/regime_citations -p 'test_*.py'

T-C4 : une permutation d'une séquence sémantique change l'empreinte.
T-C5 : une permutation d'un ensemble ne la change pas.
Et l'écart du type « affidavit 62 » — mêmes citations, autre ordre sous une même
pièce — est vu par les marqueurs, ce que la projection en ensembles ne voyait pas.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import projection as P  # noqa: E402


def bouton(pk, type_="Quote"):
    """Le balisage de `remove_evidence_button` (argument_manager/templatetags/evidence_tags.py)."""
    return (f'<a href="#" class="badge bg-danger rounded-pill text-decoration-none remove-evidence-btn"\n'
            f'           role="button"\n'
            f'           data-evidence-id="{pk}"\n'
            f'           data-evidence-type="{type_}">')


def page_affidavit(ordre):
    items = "".join(f'<li id="evidence-item-{pk}">P-2-{i} {bouton(pk)}</li>' for i, pk in enumerate(ordre, 1))
    return f"<h3>Pièce P-2</h3><ul>{items}</ul>"


class TC4SequenceSensibleALOrdre(unittest.TestCase):

    def test_permutation_d_une_sequence(self):
        self.assertNotEqual(P.empreinte({"seq": P.sequence([12, 14, 18])}),
                            P.empreinte({"seq": P.sequence([14, 12, 18])}))

    def test_marqueurs_dans_l_ordre_du_document(self):
        self.assertEqual(P.marqueurs(page_affidavit([24, 50, 108])),
                         ["evidence:Quote:24", "evidence:Quote:50", "evidence:Quote:108"])

    def test_l_ecart_de_l_affidavit_est_detecte(self):
        avant, apres = page_affidavit([24, 50, 108, 127]), page_affidavit([127, 108, 24, 50])
        # l'ancienne projection — ensembles de PK — ne voyait rien
        self.assertEqual(P.ensemble(P.marqueurs(avant)), P.ensemble(P.marqueurs(apres)))
        # la nouvelle voit la permutation, et dit laquelle
        self.assertNotEqual(P.empreinte(P.marqueurs(avant)), P.empreinte(P.marqueurs(apres)))
        self.assertIn("ordre différent dès le rang 0",
                      P.ecart({"seq_marqueurs": P.marqueurs(avant)},
                              {"seq_marqueurs": P.marqueurs(apres)})["seq_marqueurs"])

    def test_autres_marqueurs(self):
        texte = ('<a href="/pdfs/quote/7/">x</a> <a href="/emails/quote/3/">y</a> '
                 '<blockquote data-quote-id=\\"9\\" data-source=\\"pdf\\">')
        self.assertEqual(P.marqueurs(texte), ["pdf_quote:7", "email_quote:3", "data_quote:pdf:9"])


class TC5EnsembleInsensibleALOrdre(unittest.TestCase):

    def test_permutation_d_un_ensemble(self):
        self.assertEqual(P.empreinte({"ens": P.ensemble([3, 1, 2])}),
                         P.empreinte({"ens": P.ensemble([2, 3, 1])}))

    def test_doublons_d_un_ensemble(self):
        self.assertEqual(P.ensemble(["b", "a", "b"]), ["a", "b"])

    def test_ensemble_de_lignes(self):
        lignes = [{"pk": 2, "x": "b"}, {"pk": 1, "x": "a"}]
        self.assertEqual(P.empreinte(P.ensemble(lignes)), P.empreinte(P.ensemble(list(reversed(lignes)))))

    def test_cles_d_objet_sans_ordre(self):
        self.assertEqual(P.canon({"a": 1, "b": 2}), P.canon({"b": 2, "a": 1}))


class Normalisations(unittest.TestCase):

    def test_csrf_et_anti_cache(self):
        jeton = "A" * 32 + "b" * 32
        self.assertEqual(P.normaliser_texte(f'<input value="{jeton}"> <x src="/m/a.pdf?v=1792248599">'),
                         '<input value="<csrf>"> <x src="/m/a.pdf?v=#">')

    def test_redirection_vers_un_objet_temporaire(self):
        url = "/arguments/perjury-argument/74/update/"
        self.assertEqual(P.normaliser_location(url, lambda label, pk: False),
                         "/arguments/perjury-argument/<temporaire>/update/")

    def test_redirection_vers_un_objet_existant_gardee(self):
        url = "/arguments/perjury-argument/10/update/"
        self.assertEqual(P.normaliser_location(url, lambda label, pk: True), url)

    def test_autre_redirection_gardee(self):
        self.assertEqual(P.normaliser_location("/pdfs/pdf/12/", lambda label, pk: False), "/pdfs/pdf/12/")


if __name__ == "__main__":
    unittest.main()
