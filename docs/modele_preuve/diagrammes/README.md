# Diagrammes du modèle de preuve

Sources PlantUML (`.puml`) et rendus (`.svg`, `.png`). Ils illustrent
`../CONCEPTION_PREUVE.md`, qui fait foi pour la série historique 01–05. Un `❓` marque un point encore ouvert, un `➕` un ajout
issu du verdict (§ 15.2).

**Consolidation et gouvernance C-UML-2026-10-20-R1 :**
[avenant, couverture V2, plan et protocole obligatoires](../../architecture_c/README.md).
D05 `CHRONO_VERSION` est désormais décidée. Les activités ci-dessous et celles
de C restent des bases antérieures à réexaminer; chaque use case exige aussi sa
séquence, son ERD cible et ses classes, avec validation puis approbation explicite.

**Diagrammes de classes actuelles — 20 octobre 2026 :** voir
[la vue globale, les treize vues détaillées et les sources PlantUML](classes_etat_actuel/README.md).
Cette série montre les attributs, méthodes, propriétés et héritages :
54 modèles et 35 classes ou énumérations de support, extraits du code P6.

**État actuel du système — 20 octobre 2026 :** voir
[l’Entity-Relationship Diagram et ses vues détaillées](erd_etat_actuel/README.md).
Cette série est extraite des modèles Django présents dans le dépôt :
54 modèles du projet, 12 modèles techniques et 21 jointures automatiques.
Elle décrit le schéma déclaré par le code, sans consultation de la base réelle,
et reste distincte des propositions et user stories de l’architecture C.

**User stories de l’architecture C — 20 octobre 2026 :** voir
[la nouvelle série et son index](user_stories_architecture_c/README.md).
Elle contient une vue d’ensemble et quinze parcours PlantUML, avec rendus SVG/PNG.
Elle distingue les contrats approuvés, les détails résiduels de D05, les conditions D07/CF4 et C0-A testé
isolément, encore soumis à revue. Les diagrammes 01–05 ci-dessous conservent
la proposition antérieure du 16 octobre; leur chaîne Démonstration/Poignée
ne décrit pas l’architecture C retenue.

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
