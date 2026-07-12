# Registre procédural proposé

Ce dossier est produit par :

```bash
./.venv/bin/python manage.py build_procedural_registry
```

Le registre relie les cotes provisoires de `legal/bordereau_pieces.md` aux
tuples canoniques de l’audit, inventorie les anciennes cotes, développe les
petites plages numériques à titre de propositions et recense tous les
placeholders `P-[…]` de `legal/requete_secton_faits_lp.md`.

Il s’agit d’un registre **proposé**. La commande ne modifie ni la demande, ni le
bordereau, ni la base Django. Les correspondances marquées ambiguës, hors
bordereau ou nécessitant le contexte doivent être décidées avant le gel des
cotes.

## Rapports

- `registre_procedural_propose.csv` : une ligne par cote provisoire;
- `composantes_cotes.csv` : tuples composant chaque cote ou liasse;
- `conflits_cotes.csv` : même tuple affecté à plusieurs cotes proposées;
- `aliases_historiques.csv` : correspondances explicites des anciennes cotes;
- `plages_collectives.csv` : développement proposé des petites séries;
- `placeholders_demande.csv` : chaque référence `P-[…]` avec son contexte;
- `registre_procedural.json` : rapport complet exploitable par script;
- `registre_procedural_propose.xlsx` : classeur de coordination.

## Contrôle

```bash
./.venv/bin/python manage.py build_procedural_registry --check
```
