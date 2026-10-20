"""
T2.2 — l'ancien système avant et après l'étape 2 (plan du régime des citations, § 4 et § 12).

    python verifier_t22.py E1.json E3.json <pk de la citation PHRASE>

(Les messages nomment les deux mesures par leur nom de fichier : E1 et E3, ou E1 et E4 après la correction
des bornes du 20 octobre.)

E1 : empreinte.py, code de l'étape 1, sans citation PHRASE. E3 : même clone, même arbre de mesure, code de
l'étape 2 (migration 0010) et une citation PHRASE. Lecture seule : compare deux fichiers de mesure.

L'outil d'empreinte projette les tables de citations et énumère les pages des citations par le gestionnaire
de base : E3 y voit forcément les colonnes de la migration 0010 et la citation PHRASE. Ce sont les seuls
écarts admis. Tout le reste (surfaces communes, services de l'ancien système, comptes visibles) doit être
identique, et les pages propres de la citation PHRASE doivent se comporter comme celles d'une citation
inexistante (404, ou 405 avant toute recherche).

Services : la mesure en compte 143. Deux d'entre eux, `table_email_quote` et `table_pdf_quote`, sont les
projections brutes des tables par le gestionnaire de base (la vérité de la table, toutes les lignes, sans la
colonne `regime`) : après la migration 0010, ils diffèrent par construction. Ils sont contrôlés à part, ligne
à ligne. Les 141 autres sont les services de l'ancien système ; ils doivent être identiques. Les comptes par
le gestionnaire par défaut (`visibles_*`) en font partie. Entre deux mesures du même code sans citation
PHRASE (contrôle de l'étape 1 : E1 contre la mesure B de P6), les 143 sont comparés tels quels.

Code 0 : conforme. Code 1 : écart à examiner.
"""
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import projection as P  # noqa: E402

NOUVELLES_COLONNES = {"start", "end", "source_text_sha256", "anchored_text_sha256", "certified_text_sha256",
                      "certified", "corrected_on_scan", "derived_from_id"}
TABLES = ("table_email_quote", "table_pdf_quote")
PK_PHRASE = int(sys.argv[3]) if len(sys.argv) > 3 else 303

e1, e3 = (json.load(open(f)) for f in sys.argv[1:3])
N1, N3 = (os.path.splitext(os.path.basename(f))[0] for f in sys.argv[1:3])
ok = True


def verdict(cond, msg):
    global ok
    print(("OK      " if cond else "ÉCHEC   ") + msg)
    ok = ok and cond


# Périmètre : l'inventaire énumère les citations par le gestionnaire de base ; E3 y ajoute les trois
# pages de la citation PHRASE elle-même, que l'ancien système doit refuser.
u1, u3 = set(e1["surfaces"]), set(e3["surfaces"])
propres = {f"/emails/quote/{PK_PHRASE}/", f"/emails/quote/{PK_PHRASE}/update/", f"/emails/quote/{PK_PHRASE}/delete/"}
verdict(u1 <= u3 and u3 - u1 == propres, f"surfaces : {N1} {len(u1)}, {N3} {len(u3)} ; en plus dans {N3} : {sorted(u3 - u1)}")
verdict(e1["meta"].get("arbre") == e3["meta"].get("arbre"), f"même arbre de mesure ({e3['meta'].get('arbre')})")
for u in sorted(u3 - u1):
    p = e3["surfaces"][u]
    statut = p.get("statut")
    # Rien d'instancié ni dans le contexte. Sur une page 404, la page technique de Django (DEBUG) reprend
    # l'URL demandée (titre, « Request URL ») : c'est la seule marque admise, la même que pour une PK inexistante.
    rien = not p.get("ens_instanciees") and not p.get("ens_contexte") and not p.get("seq_contexte") \
        and not p.get("nb_instanciations")
    echo_seul = set(p.get("seq_marqueurs", [])) <= {f"email_quote:{PK_PHRASE}"} and len(p.get("seq_marqueurs", [])) <= 2
    verdict(statut in (404, 405) and rien and (statut == 405 and not p.get("seq_marqueurs") or statut == 404 and echo_seul),
            f"{u} → {statut} ; rien d'instancié ni dans le contexte ; marques : {p.get('seq_marqueurs')} "
            f"({'URL demandée, reprise par la page 404' if p.get('seq_marqueurs') else 'aucune'})")
    if statut == 405:
        autres = [v.get("statut") for k, v in e3["surfaces"].items() if re.fullmatch(r"/emails/quote/\d+/delete/", k) and k != u]
        verdict(set(autres) == {405}, f"          (405 comme les {len(autres)} autres pages de suppression : refus avant toute recherche)")

# Surfaces
diff = [u for u in u1 if e1["surfaces"][u] != e3["surfaces"][u]]
familles = Counter(re.sub(r"\d+", "<n>", u) for u in diff)
verdict(not diff, f"surfaces communes : {len(u1) - len(diff)} identiques, {len(diff)} différentes {dict(familles)}")
for u in diff[:5]:
    for k, v in P.ecart(e1["surfaces"][u], e3["surfaces"][u]).items():
        print(f"          {u} · {k} : {str(v)[:220]}")

# La PK nouvelle n'apparaît dans aucune surface ni aucun service hors des tables brutes
marque = f"email_quote:{PK_PHRASE}"
dans_surfaces = [u for u, p in e3["surfaces"].items() if marque in json.dumps(p) and u not in propres]
verdict(not dans_surfaces, f"« {marque} » absente de toutes les autres surfaces ({len(e3['surfaces']) - len(propres)})")
services_hors_tables = {k: v for k, v in e3["services"].items() if k not in TABLES}
dans_services = [k for k, v in services_hors_tables.items() if marque in json.dumps(v)]
verdict(not dans_services, f"« {marque} » absente de tous les services de l'ancien système ({len(services_hors_tables)})")

# Services
cles = set(e1["services"]) | set(e3["services"])
sd = sorted(k for k in cles if e1["services"].get(k) != e3["services"].get(k))
autres = [k for k in sd if k not in TABLES]
anciens = cles - set(TABLES)
verdict(set(TABLES) <= cles and not autres,
        f"services : {len(cles)} = {len(anciens)} de l'ancien système, {len(anciens) - len(autres)} identiques, "
        f"+ {len(TABLES)} projections brutes des tables, contrôlées ci-dessous ; écarts hors tables brutes : {autres}")
for cle in ("visibles_email_quote", "visibles_pdf_quote"):
    verdict(e1["services"].get(cle) == e3["services"].get(cle),
            f"{cle} (gestionnaire par défaut) : {e1['services'].get(cle)} → {e3['services'].get(cle)}")

# Les deux projections brutes (gestionnaire de base) : seuls écarts permis
for cle in TABLES:
    a, b = e1["services"][cle], e3["services"][cle]
    ra = {r["pk"]: r for r in a}
    rb = {r["pk"]: r for r in b}
    colonnes_ajoutees = set().union(*(set(r) for r in b)) - set().union(*(set(r) for r in a))
    verdict(colonnes_ajoutees <= NOUVELLES_COLONNES,
            f"{cle} : colonnes ajoutées = {sorted(colonnes_ajoutees)} (toutes de la migration 0010)")
    lignes_en_plus = sorted(set(rb) - set(ra))
    lignes_en_moins = sorted(set(ra) - set(rb))
    attendu_plus = [PK_PHRASE] if cle == "table_email_quote" else []
    verdict(lignes_en_plus == attendu_plus and not lignes_en_moins,
            f"{cle} : lignes en plus {lignes_en_plus}, en moins {lignes_en_moins} (attendu : {attendu_plus}, [])")
    modifiees = [pk for pk in ra if pk in rb and {k: v for k, v in rb[pk].items() if k not in NOUVELLES_COLONNES} != ra[pk]]
    verdict(not modifiees, f"{cle} : les {len(ra)} lignes existantes, sur leurs colonnes d'origine, inchangées "
            f"({len(modifiees)} modifiée(s))")
    valeurs_neuves = Counter(json.dumps({k: rb[pk].get(k) for k in sorted(NOUVELLES_COLONNES)}, sort_keys=True)
                             for pk in ra)
    print(f"        {cle} : valeurs des colonnes nouvelles sur les lignes de l'ancien régime : {dict(valeurs_neuves)}")
    if cle == "table_email_quote" and PK_PHRASE in rb:
        r = rb[PK_PHRASE]
        print(f"        ligne {PK_PHRASE} : regime absent de la projection ; start={r.get('start')} end={r.get('end')} "
              f"derived_from_id={r.get('derived_from_id')} certified={r.get('certified')}")

# HTML secondaire
hd = [u for u in u1 if e1["secondaire"][u] != e3["secondaire"].get(u)]
print(f"        HTML secondaire : {len(hd)} page(s) différente(s) {dict(Counter(re.sub(r'[0-9]+', '<n>', u) for u in hd))}")

# Empreinte de l'ancien système : surfaces communes et services hors des projections brutes
def ancien_systeme(m):
    return P.empreinte([P.empreinte({u: m["surfaces"][u] for u in sorted(u1)}),
                        P.empreinte({k: v for k, v in m["services"].items() if k not in TABLES})])


a1, a3 = ancien_systeme(e1), ancien_systeme(e3)
print(f"        empreinte canonique brute (outil) : {N1} {e1['empreintes']['canonique'][:16]}… | "
      f"{N3} {e3['empreintes']['canonique'][:16]}… (diffère par construction)")
verdict(a1 == a3, f"empreinte de l'ancien système : {N1} {a1[:16]}… | {N3} {a3[:16]}…")

print("T2.2 : " + ("CONFORME — l'ancien système est inchangé ; seules les projections brutes des tables diffèrent, "
                   "de la façon attendue" if ok else "ÉCARTS À EXAMINER"))
sys.exit(0 if ok else 1)
