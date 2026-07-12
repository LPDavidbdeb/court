# Audit canonique des références de preuve

Ce dossier est généré par la commande Django suivante :

```bash
./.venv/bin/python manage.py audit_legal_evidence
```

La commande inspecte en lecture seule les fichiers Markdown, CSV et XLSX de
`legal/organisation_preuve`, conserve chaque forme de référence observée, la
normalise lorsque possible vers un tuple `(model, pk)`, puis vérifie l'objet
Django et la disponibilité de sa source matérielle.

Elle n'attribue aucune cote procédurale, ne modifie aucun objet Django et ne
modifie aucun fichier de preuve original.

## Rapports

- `inventaire_canonique.csv` : union dédupliquée par tuple Django;
- `occurrences_references.csv` : toutes les occurrences avec leur provenance;
- `exceptions_references.csv` : objets absents, originaux incomplets et références non résolues;
- `references_non_resolues.csv` : anciennes cotes, plages et agrégats non ramenés à un tuple unique;
- `alias_references.csv` : formes différentes convergeant vers un même tuple;
- `audit_preuve.json` : représentation complète exploitable par script;
- `resume_audit.json` : principaux contrôles et taux de couverture;
- `audit_preuve.xlsx` : classeur de consultation des mêmes résultats.

## Contrôle de reproductibilité

```bash
./.venv/bin/python manage.py audit_legal_evidence --check
```

Le contrôle réussit uniquement si une nouvelle exécution produit exactement
les mêmes rapports JSON et CSV.
