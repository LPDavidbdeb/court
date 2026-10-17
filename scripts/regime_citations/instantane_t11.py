"""
T1.1 — la migration du régime ne touche aucune donnée existante.

    ... instantane_t11.py --base court_quote_regime_clone instantane avant.json   (avant la migration)
    ... instantane_t11.py --base court_quote_regime_clone comparer  avant.json   (après)

Avant : pour chaque table, ses colonnes et l'empreinte de son contenu ; pour
les citations, PK et `updated_at`. Après : les mêmes empreintes, sur les MÊMES
colonnes ; les colonnes nouvelles ; les citations par régime.

Même environnement que empreinte.py (réglages, PYTHONPATH).
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.getcwd())

TABLES_CITATIONS = ("email_manager_quote", "pdf_manager_quote")


def tables(cur):
    cur.execute("select table_name from information_schema.tables "
                "where table_schema='public' and table_type='BASE TABLE' order by 1")
    return [r[0] for r in cur.fetchall()]


def colonnes(cur, table):
    cur.execute("select column_name from information_schema.columns "
                "where table_schema='public' and table_name=%s order by ordinal_position", (table,))
    return [r[0] for r in cur.fetchall()]


def empreinte(cur, table, cols):
    sel = ", ".join(f'x."{c}"' for c in cols)
    cur.execute(f"select count(*), md5(coalesce(string_agg(row({sel})::text, '|' "
                f"order by row({sel})::text), '')) from public.\"{table}\" x")
    n, h = cur.fetchone()
    return {"n": n, "md5": h}


def citations(cur, table):
    cur.execute(f'select id, updated_at::text from public."{table}" order by id')
    return [list(r) for r in cur.fetchall()]


def migrations(cur):
    cur.execute("select app, name from django_migrations where app in ('email_manager','pdf_manager') "
                "order by app, name")
    return [list(r) for r in cur.fetchall()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("mode", choices=["instantane", "comparer"])
    ap.add_argument("fichier")
    args = ap.parse_args()
    import django
    django.setup()
    from django.db import connection
    if connection.settings_dict["NAME"] != args.base or args.base == "court_project_pg":
        sys.exit("base refusée")
    with connection.cursor() as cur:
        if args.mode == "instantane":
            snap = {"tables": {t: {"colonnes": colonnes(cur, t), **empreinte(cur, t, colonnes(cur, t))}
                               for t in tables(cur)},
                    "citations": {t: citations(cur, t) for t in TABLES_CITATIONS},
                    "migrations": migrations(cur)}
            json.dump(snap, open(args.fichier, "w"), indent=1)
            print({t: snap["tables"][t]["n"] for t in TABLES_CITATIONS})
            return
        snap = json.load(open(args.fichier))
        rapport = {"tables_identiques": 0, "tables_divergentes": [], "colonnes_nouvelles": {},
                   "tables_nouvelles": sorted(set(tables(cur)) - set(snap["tables"]))}
        for t, avant in snap["tables"].items():
            if t == "django_migrations":
                continue
            apres = empreinte(cur, t, avant["colonnes"])
            if (apres["n"], apres["md5"]) == (avant["n"], avant["md5"]):
                rapport["tables_identiques"] += 1
            else:
                rapport["tables_divergentes"].append(t)
            nouvelles = [c for c in colonnes(cur, t) if c not in avant["colonnes"]]
            if nouvelles:
                rapport["colonnes_nouvelles"][t] = nouvelles
        for t in TABLES_CITATIONS:
            rapport[f"{t} : PK et updated_at identiques"] = citations(cur, t) == snap["citations"][t]
            if "regime" in colonnes(cur, t):
                cur.execute(f'select regime, count(*) from public."{t}" group by regime order by regime')
                rapport[f"{t} : par régime"] = dict(cur.fetchall())
        rapport["migrations_ajoutees"] = [m for m in migrations(cur) if m not in snap["migrations"]]
        print(json.dumps(rapport, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
