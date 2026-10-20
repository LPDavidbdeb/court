# Modèle global cible — G-C0A-R1

**20 octobre 2026 — TRANS-02, périmètre initial C0-A seulement.** Le socle
observé proposé est `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`; le patch non
appliqué reste celui construit sur P6. Les deux vues sont une cible de
comportements sur un schéma inchangé, pas un relevé de toute l’application ni
le modèle complet de L1–L6. Auteur : B. Approbation utilisateur : aucune.

- [ERD consolidé C0-A](erd_consolide.svg) · [source](erd_consolide.puml)
- [Classes et composants consolidés](classes_consolidees.svg) · [source](classes_consolidees.puml)

Les 12 entités métier représentées sont déjà présentes dans le code. Les
associations M2M existantes sont logiques; ContentType est le référentiel
technique représenté, les autres tables techniques et champs étrangers au
périmètre sont omis. Aucun nouveau champ/table n’est proposé
pour C0-A. La GFK LibraryNode et les anciens IDs de NoeudArchive ne sont pas des
FK vers Statement. Les `on_delete` réels restent visibles, même quand le patch
ajoute un refus applicatif pour éviter leur cascade.

`MODIF_PATCH` désigne un comportement du patch, non le code principal livré.
`PROPOSE_CORRECTION` désigne le retour partiel qualifié de UC-C-15, absent du
patch actuel. LectureAppuis est un résultat en mémoire, pas un modèle Django.
ExamenEditorial, Correspondance.nature et les gardes globales de gel ne sont
pas introduits ici. Les relevés observés P6 restent conservés à leur place.

Les vues locales de [13](../use_cases/UC-C-13/specification.md),
[14](../use_cases/UC-C-14/specification.md) et
[15](../use_cases/UC-C-15/specification.md) sélectionnent les données et
responsabilités propres à chaque cas; elles ne se réduisent pas à une inclusion
du modèle global entier.

Contrôles : PlantUML 1.2026.8, compilation/rendus SVG réussis, PNG de contrôle
conservés avec fond blanc, inspection visuelle. Les clés, nullabilités et
`on_delete` ont été confrontés aux modèles lus au SHA proposé. Les validations
des dossiers portent les empreintes des sources/rendus et du style inclus.
La validation globale porte seulement ce périmètre initial; aucun R01–R08
n’est fermé et aucune conformité applicative sur `515666e` n’est attestée.

Régénération documentaire depuis la racine :

```sh
.venv/bin/python -B docs/architecture_c/outils/generer_uml_c0a.py
plantuml -charset UTF-8 -tsvg 'docs/architecture_c/modele_global/*.puml' 'docs/architecture_c/use_cases/UC-C-13/*.puml' 'docs/architecture_c/use_cases/UC-C-14/*.puml' 'docs/architecture_c/use_cases/UC-C-15/*.puml'
```

Après régénération, rendre chaque SVG avec
`rsvg-convert --background-color=white -o <nom>.png <nom>.svg`, inspecter les
images et actualiser les preuves/empreintes avant toute nouvelle validation.
