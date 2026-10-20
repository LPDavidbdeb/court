# Modèle global cible — G-C0A-R2-ST

**20 octobre 2026 — TRANS-02, périmètre initial C0-A seulement, révisé ST-R1.**
Socle lu : `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`; patch P6 inchangé.
Ces deux vues décrivent des comportements cibles sur un schéma inchangé,
pas toute l’application ou L1–L6. Auteur : B. Approbation utilisateur : aucune.
La [version G-C0A-R1](../historique/2026-10-20_avant_invariants_statement_R2/corpus/modele_global/README.md)
est conservée avec ses sources/rendus.

- [ERD consolidé C0-A](erd_consolide.svg) · [source](erd_consolide.puml)
- [Classes et composants consolidés](classes_consolidees.svg) · [source](classes_consolidees.puml)

Les 12 entités métier et ContentType existent dans le code. Les M2M sont
des associations logiques; les tables techniques et champs hors périmètre
sont omis. Aucun champ ou table nouveau en C0-A. GFK LibraryNode et anciens
IDs de NoeudArchive ne sont pas des FK vers Statement. Les `on_delete` réels
restent visibles, même lorsqu’un refus applicatif du patch protège la cascade.

Le [contrat ST-R1](../INVARIANTS_STATEMENT_REPRODUCED_PRODUCED.md) exige une
origine REPRODUCED attestée pour réutiliser un objet. Les Statement PRODUCED
sont privés. L’ERD signale l’absence actuelle de provenance/propriété; les
métadonnées durables proposées relèvent de L1-A et ne sont pas des champs
C0-A. Les associations actuelles ou is_user_created ne prouvent pas l’origine.

`MODIF_PATCH` désigne le comportement du patch, pas du code principal livré.
`CIBLE_R2_ST` désigne le module dont l’édition proposée crée toujours un objet
neuf sur texte différent, dans **UC13::C0A_ISOLER**; sa branche privée actuelle
en place n’est pas réputée corrigée. `PROPOSE_CORRECTION` désigne le résultat
partiel qualifié UC15, absent du patch (C0A-REV-01). LectureAppuis est en mémoire,
pas un modèle Django. ExamenEditorial, nature et gel global ne sont pas ajoutés.

Les vues locales [13](../use_cases/UC-C-13/specification.md),
[14](../use_cases/UC-C-14/specification.md) et
[15](../use_cases/UC-C-15/specification.md) sélectionnent leurs données et
responsabilités. UC13 R2-ST dispose d’une attestation B pour le seul sous-cas
C0A_ISOLER; 14/15 restent EN_REVUE, vues locales R1 inchangées. L1-A devra
faire respecter ST04 à tous les rattachements; C0-A ne le réalise pas seul.

Contrôles actuels : les quatre vues 13 et les deux globales ont été recompilées
avec PlantUML 1.2026.8, code 0, rendues SVG/PNG sur fond blanc et inspectées.
Clés/nullabilités/cascades restent celles des modèles lus au SHA nommé.
Les huit vues locales 14/15 gardent leurs contrôles T historiques. Les
manifestes et validations distinguent ces versions. Aucun R01–R08 fermé,
aucune conformité applicative sur 515666e attestée.

Régénération des **sources courantes déjà révisées**, depuis la racine :

```sh
plantuml -charset UTF-8 -tsvg docs/architecture_c/modele_global/*.puml docs/architecture_c/use_cases/UC-C-13/*.puml
```

Puis rendre les SVG avec `rsvg-convert --background-color=white -o <nom>.png
<nom>.svg`, inspecter et actualiser les empreintes avant revalidation.
L’ancien générateur `outils/generer_uml_c0a.py` construit R1; une garde le fait
refuser la génération lorsque UC13 porte R2-ST, afin de ne pas écraser la
révision. Les `.puml` courants font autorité; aucun générateur R1 à relancer.
