# UC14 R3-CONC — Revue indépendante préalable

**23 octobre 2026 — VALIDE_ARCHITECTURE; approbation utilisateur : AUCUNE.**
La revue indépendante technique, fonctionnelle et architecturale est
terminée. L'[attestation B](revue_B.md) est retranscrite de la réponse d'un
agent distinct de l'auteur, `/root/revue_uc14_r3`, intervenu strictement en
lecture seule sur demande explicite de revue indépendante de l'utilisateur.
Aucun résultat applicatif R3-CONC n'est annoncé. Le candidat `f35ec85`
demeure NON CONFORME; aucun passage à PRET_DEVELOPPEMENT.

## Dossier soumis

[Spécification](specification.md), [sept vues et sources](README.md),
[analyse de cohérence](analyse_coherence.md), [plan d'essais](plan_tests.md),
[traçabilité](tracabilite.md), [manifest de conception](manifest_conception.json).
La revue porte sur ce mécanisme limité et ses impacts UC13/14, sans rouvrir
les modèles transversaux ni modifier les contrats R2 approuvés.

| Axe | Questions examinées indépendamment | Verdict B |
|---|---|---|
| Technique | Durée des verrous dans la conception, savepoints, relecture après attente, parents Treebeard, texte Statement, ordre multiligne, UPDATE sans INSERT | VALIDE_ARCHITECTURE |
| Fonctionnel | Deux issues sûres, archive exacte, refus lisibles, rollback T1/T2 et commits indépendants, UC13 préservé | VALIDE_ARCHITECTURE |
| Architectural | Quatre vues cohérentes, schéma inchangé, scope local C0-A, limites orphelin/bulk/gel, approbations antérieures intactes | VALIDE_ARCHITECTURE |

## Version exacte et contrôles réalisés

SHA-256 du manifeste de conception examiné :
`258ca9a719c0b172461f75dc5f27bb98b74335b532340c00654b5165f7e87b0d`.
Ses 27 fichiers et la dépendance de style ont été vérifiés indépendamment.
Le statut `CONCEPTION_SOUMISE_A_REVUE` dans ce manifeste figé décrit sa
soumission; le résultat courant de la revue est consigné sur cette page.

Les sept sources compilent avec PlantUML 1.2026.8; sept SVG et sept PNG
conservés et inspectés. Les commandes, empreintes par vue et comparaisons
sont dans les [contrôles documentaires](controles_documentaires.json).
AC01–AC07 sont identiques; l'ERD ne diffère que par l'inclusion relative du
style. Les trois manifestes approuvés UC13/14/15 et leurs dépendances sont
intacts. Les fichiers suivis contrôlés et 206 documents protégés n'ont pas
changé. Aucun cluster ni test applicatif n'a été lancé.

## Points obligatoires de la future revue de code

B n'identifie aucun obstacle documentaire supplémentaire. La future revue
doit néanmoins vérifier les instances réellement rechargées et leurs caches
de relations/GFK, l'alias et la connexion communs, l'ordre effectif des
protections avec parents, les variantes de sauvegarde ORM sans INSERT et
la création neuve Treebeard. Les observations PostgreSQL doivent prouver les
deux ordres sûrs, les attentes, les annulations et la fidélité des archives.
Ces points ne sont pas des garanties déjà implantées.

Une validation de conception n'est pas la clôture du blocage B01. Celle-ci
exigera la correction autorisée, les contre-épreuves réelles et une nouvelle
revue indépendante du candidat. La présente livraison ne fusionne, ne
déploie et ne modifie aucun code.

## Historique de cette révision

| Date | Étape | Effet |
|---|---|---|
| 2026-10-23 | Soumission R3-CONC, sept sources/rendus, manifeste 27 fichiers | EN_REVUE; anciennes approbations R2 conservées |
| 2026-10-23 | Attestation indépendante B T/F/A reçue | VALIDE_ARCHITECTURE pour cette conception uniquement; aucun code ni approbation utilisateur |
