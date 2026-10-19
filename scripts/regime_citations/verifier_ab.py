"""
L'oracle de la répétition générale P6 : verdict et code de sortie, là où comparer.py décrit.

    python verifier_ab.py ab A.json B.json     # deux mesures d'empreinte.py : A (historique + ordre), B (A + régime)
    python verifier_ab.py t11 rapport.json     # sortie de « instantane_t11.py … comparer »

Code 0 : tout est conforme. Code 1 : un invariant est violé. Code 2 : entrée illisible.
comparer.py reste l'outil de diagnostic ; il n'est pas modifié.

INVARIANTS « ab »

  1. Périmètre : même liste de surfaces (empreinte de la liste et ensemble des URL), même base mesurée,
     même arbre (l'export docx écrit le chemin de l'arbre dans son texte). Une différence de périmètre
     est un échec, jamais un succès par défaut.
  2. Intégrité : chaque empreinte inscrite dans une mesure est recalculée sur son contenu ; une
     empreinte qui ne correspond pas à ce qu'elle résume est un échec.
  3. Surfaces : projection canonique identique, surface par surface.
  4. Services : identiques, clé par clé.
  5. Empreintes canoniques égales.
  6. HTML secondaire : toute différence porte sur une URL d'une catégorie de DIFFERENCES_AUTORISEES.
  7. Erreurs : aucune surface en erreur dans B (statut ≥ 400, ou exception de mesure) qui ne l'était
     pas dans A.

Les différences autorisées sont énumérées ci-dessous, par catégorie et motif ; aucune n'est déduite d'un
nombre de divergences. Les surfaces et les services n'en admettent aucune.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import projection as P  # noqa: E402

# Seule différence admise entre A et B : le HTML (secondaire) des fiches d'administration des trames,
# dont la barre latérale et le sélecteur de citations listent désormais l'administration des
# citations (objectif O1.6 du plan du régime, § 3).
DIFFERENCES_AUTORISEES = {
    "secondaire": [
        (re.compile(r"^/admin/argument_manager/tramenarrative/\d+/change/$"),
         "O1.6 — administration des citations visible depuis la fiche d'administration d'une trame"),
    ],
    "surfaces": [],
    "services": [],
}

# Ce que la migration du régime a le droit de changer dans les tables (T1.1).
T11_COLONNES_NOUVELLES = {"email_manager_quote": ["regime"], "pdf_manager_quote": ["regime"]}
T11_MIGRATIONS = sorted([["email_manager", "0009_quote_regime"], ["pdf_manager", "0009_quote_regime"]])


class Verdict:

    def __init__(self):
        self.violations = []

    def verifier(self, condition, message, details=()):
        print(("OK      " if condition else "ÉCHEC   ") + message)
        if not condition:
            self.violations.append(message)
            for d in list(details)[:20]:
                print(f"          {d}")
        return condition

    def info(self, message):
        print("        " + message)


def _charger(chemin):
    with open(chemin, encoding="utf-8") as fh:
        texte = fh.read()
    debut = texte.find("{")   # une sortie de script peut précéder ou suivre le JSON
    if debut < 0:
        raise ValueError(f"aucun JSON dans {chemin}")
    return json.JSONDecoder().raw_decode(texte[debut:])[0]


def _autorisee(categorie, url):
    for motif, raison in DIFFERENCES_AUTORISEES[categorie]:
        if motif.match(url):
            return raison
    return None


def _en_erreur(projection):
    return "erreur" in projection or projection.get("statut", 0) >= 400


def _integrite(v, nom, m):
    e = m.get("empreintes", {})
    attendu = {
        "surfaces": P.empreinte(m["surfaces"]),
        "services": P.empreinte(m["services"]),
        "secondaire": P.empreinte(m["secondaire"]),
    }
    attendu["canonique"] = P.empreinte([attendu["surfaces"], attendu["services"]])
    faux = [k for k, val in attendu.items() if e.get(k) != val]
    v.verifier(not faux, f"intégrité de {nom} : empreintes inscrites = empreintes recalculées",
               [f"{k} inscrite {str(e.get(k))[:12]}…, recalculée {attendu[k][:12]}…" for k in faux])
    return attendu


def verifier_ab(chemin_a, chemin_b):
    v = Verdict()
    a, b = _charger(chemin_a), _charger(chemin_b)
    for nom, m in (("A", a), ("B", b)):
        manque = [k for k in ("surfaces", "services", "secondaire", "empreintes", "liste_des_surfaces", "meta") if k not in m]
        if manque:
            v.verifier(False, f"structure de {nom} : champs absents {manque}")
            return v

    # 1. Périmètre
    v.verifier(a["liste_des_surfaces"] == b["liste_des_surfaces"], "périmètre : même liste de surfaces (empreinte de la liste)",
               [f"A {a['liste_des_surfaces'][:12]}…, B {b['liste_des_surfaces'][:12]}…"])
    ua, ub = set(a["surfaces"]), set(b["surfaces"])
    v.verifier(ua == ub, f"périmètre : mêmes URL mesurées ({len(ua)} / {len(ub)})",
               [f"seulement dans A : {u}" for u in sorted(ua - ub)] + [f"seulement dans B : {u}" for u in sorted(ub - ua)])
    v.verifier(set(a["secondaire"]) == ua and set(b["secondaire"]) == ub, "périmètre : HTML secondaire mesuré sur les mêmes URL")
    v.verifier(set(a["services"]) == set(b["services"]), "périmètre : mêmes services mesurés",
               sorted(set(a["services"]) ^ set(b["services"])))
    for cle in ("base", "arbre"):
        v.verifier(a["meta"].get(cle) == b["meta"].get(cle), f"périmètre : même {cle} ({a['meta'].get(cle)})",
                   [f"A {a['meta'].get(cle)}, B {b['meta'].get(cle)}"])

    # 2. Intégrité
    ea = _integrite(v, "A", a)
    eb = _integrite(v, "B", b)

    # 3. Surfaces
    communes = sorted(ua & ub)
    diff_surfaces = [u for u in communes if a["surfaces"][u] != b["surfaces"][u]]
    v.verifier(not diff_surfaces, f"surfaces : {len(communes)} projections canoniques identiques",
               [f"{u} : {P.ecart(a['surfaces'][u], b['surfaces'][u])}" for u in diff_surfaces])

    # 4. Services
    diff_services = sorted(k for k in set(a["services"]) & set(b["services"]) if a["services"][k] != b["services"][k])
    v.verifier(not diff_services, f"services : {len(a['services'])} identiques", diff_services)

    # 5. Empreintes canoniques (recalculées, donc indépendantes de ce qui est inscrit)
    v.verifier(ea["canonique"] == eb["canonique"], f"empreinte canonique : A = B ({ea['canonique'][:12]}…)",
               [f"A {ea['canonique'][:12]}…, B {eb['canonique'][:12]}…"])

    # 6. HTML secondaire
    diff_html = [u for u in communes if a["secondaire"].get(u) != b["secondaire"].get(u)]
    non_autorisees = [u for u in diff_html if not _autorisee("secondaire", u)]
    v.verifier(not non_autorisees, "HTML secondaire : toutes les différences sont autorisées", non_autorisees)
    par_raison = {}
    for u in diff_html:
        r = _autorisee("secondaire", u)
        if r:
            par_raison.setdefault(r, []).append(u)
    for raison, urls in par_raison.items():
        v.info(f"différences autorisées ({len(urls)}) — {raison}")

    # 7. Erreurs nouvelles
    nouvelles = [u for u in communes if _en_erreur(b["surfaces"][u]) and not _en_erreur(a["surfaces"][u])]
    v.verifier(not nouvelles, "erreurs : aucune surface en erreur dans B qui ne l'était pas dans A",
               [f"{u} : {b['surfaces'][u].get('statut', b['surfaces'][u].get('erreur'))}" for u in nouvelles])
    statuts = {}
    for u in communes:
        if _en_erreur(a["surfaces"][u]):
            s_ = str(a["surfaces"][u].get("statut", "exception"))
            statuts[s_] = statuts.get(s_, 0) + 1
    v.info("surfaces à statut ≥ 400 dans A comme dans B (préexistantes) : "
           + ", ".join(f"{n} en {s_}" for s_, n in sorted(statuts.items())))
    return v


def verifier_t11(chemin):
    v = Verdict()
    r = _charger(chemin)
    v.verifier(r.get("tables_divergentes") == [], "T1.1 : aucune table divergente sur ses colonnes d'origine",
               r.get("tables_divergentes") or [])
    v.verifier(r.get("tables_nouvelles") == [], "T1.1 : aucune table nouvelle", r.get("tables_nouvelles") or [])
    v.verifier(r.get("tables_identiques", 0) > 0, f"T1.1 : {r.get('tables_identiques')} tables identiques")
    v.verifier(r.get("colonnes_nouvelles") == T11_COLONNES_NOUVELLES,
               "T1.1 : seule la colonne regime est nouvelle, sur les deux tables de citations",
               [json.dumps(r.get("colonnes_nouvelles"), ensure_ascii=False)])
    for t in ("email_manager_quote", "pdf_manager_quote"):
        v.verifier(r.get(f"{t} : PK et updated_at identiques") is True, f"T1.1 : {t}, PK et updated_at identiques")
        regimes = r.get(f"{t} : par régime") or {}
        v.verifier(list(regimes) == ["HERITE"] and regimes["HERITE"] > 0,
                   f"T1.1 : {t}, toutes les citations HERITE ({regimes})")
    v.verifier(sorted(r.get("migrations_ajoutees") or []) == T11_MIGRATIONS,
               "T1.1 : exactement les deux migrations 0009 ajoutées", [json.dumps(r.get("migrations_ajoutees"))])
    return v


def main(argv):
    if len(argv) < 2 or argv[0] not in ("ab", "t11") or (argv[0] == "ab" and len(argv) != 3):
        print(__doc__.split("\n\n")[1])
        return 2
    try:
        v = verifier_ab(argv[1], argv[2]) if argv[0] == "ab" else verifier_t11(argv[1])
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"ÉCHEC   entrée illisible : {type(e).__name__}: {e}")
        return 2
    if v.violations:
        print(f"ORACLE : ÉCHEC ({len(v.violations)} invariant(s) violé(s))")
        return 1
    print("ORACLE : CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
