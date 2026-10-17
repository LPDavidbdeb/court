"""
Compare deux mesures d'empreinte et dit où elles divergent, champ par champ.

    python scripts/regime_citations/comparer.py a.json b.json

Une séquence dont seuls les rangs changent est signalée comme telle
(« mêmes éléments, ordre différent dès le rang … »).
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import projection as P  # noqa: E402


def gabarit(url):
    return "/".join("#" if x.isdigit() else x for x in url.split("?")[0].split("/"))


def main(chemin_a, chemin_b):
    a, b = json.load(open(chemin_a)), json.load(open(chemin_b))
    print(f"A : {chemin_a}\n    {a['meta']}\nB : {chemin_b}\n    {b['meta']}\n")
    if a["liste_des_surfaces"] != b["liste_des_surfaces"]:
        print("⚠ les listes de surfaces diffèrent : comparaison sans objet")
    for cle in ("canonique", "surfaces", "services", "secondaire"):
        egal = a["empreintes"][cle] == b["empreintes"][cle]
        print(f"{cle:10} {'identique' if egal else 'DIFFÉRENT'}  {a['empreintes'][cle][:12]} / {b['empreintes'][cle][:12]}")

    surf = [u for u in a["surfaces"] if a["surfaces"][u] != b["surfaces"].get(u)]
    print(f"\nSurfaces divergentes : {len(surf)}")
    for u in surf:
        print(f"  {u}")
        for champ, quoi in P.ecart(a["surfaces"][u], b["surfaces"][u]).items():
            print(f"      {champ} : {quoi}")

    serv = [k for k in sorted(set(a["services"]) | set(b["services"]))
            if a["services"].get(k) != b["services"].get(k)]
    print(f"\nServices divergents : {len(serv)}")
    for k in serv:
        print(f"  {k}")
        for champ, quoi in P.ecart(a["services"].get(k), b["services"].get(k)).items():
            print(f"      {champ} : {quoi}")

    sec = [u for u in a["secondaire"] if a["secondaire"][u] != b["secondaire"].get(u)]
    print(f"\nHTML normalisé (secondaire) divergent : {len(sec)}")
    for g, n in collections.Counter(gabarit(u) for u in sec).most_common():
        print(f"  {n:4}  {g}")

    for nom, m in (("A", a), ("B", b)):
        err = sorted(u for u, p in m["surfaces"].items() if p.get("statut", 0) >= 500 or "erreur" in p)
        print(f"\nErreurs (5xx) dans {nom} : {len(err)}")
        if nom == "B":
            err_a = {u for u, p in a["surfaces"].items() if p.get("statut", 0) >= 500 or "erreur" in p}
            print(f"  nouvelles : {sorted(set(err) - err_a)}")
            print(f"  disparues : {sorted(err_a - set(err))}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
