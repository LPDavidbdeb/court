# Diagrammes du modèle de preuve

Sources PlantUML (`.puml`) et rendus (`.svg`, `.png`). Ils illustrent
`../CONCEPTION_PREUVE.md`, qui fait foi. Un `❓` marque un point encore ouvert, un `➕` un ajout
issu du verdict (§ 15.2).

| Fichier | Contenu | Sections |
|---|---|---|
| `01_rives_et_ponts` | les deux rives, l'ancien pont, le nouveau, et le sens des dépendances | § 1 |
| `02_schema_nouveau_pont` | le schéma proposé : preuve, nœud, démonstration, poignée, lien paragraphe, version, entrée du bordereau | §§ 2, 3, 5, 8, 15 |
| `03_arbre_danse` | l'arbre du fait de la danse, avec la théorie de LP | §§ 11, 16 |
| `04_versions_et_gel` | du brouillon au dépôt : le gel, la copie du chemin, la correspondance | §§ 3.2, 3.4, 8.2 |
| `05_rendu_et_bordereau` | du paragraphe au verbatim et aux cotes | §§ 3, 7.5, 9.4 |

**Régénérer** (PlantUML 1.2026.8, installé dans `/usr/local/bin/plantuml`) :

    cd docs/modele_preuve/diagrammes
    plantuml -charset UTF-8 -tsvg *.puml
    plantuml -charset UTF-8 -tpng *.puml

Piège de syntaxe : dans un diagramme d'activité, un `;` termine l'activité. N'en mettre aucun
à l'intérieur d'un texte d'activité.
