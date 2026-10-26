# Publication pour examen — modèles transversaux C

**21 octobre 2026 — branche `docs/architecture-c-transversale-20261021`.**
Publication documentaire demandée par l’utilisateur pour examen des fichiers
exacts avant approbation du Product Owner. Base Git : `origin/main`,
`cb56fa62f3d8aa8a6455a3a06783d734d23ed986`. Aucune fusion vers main.

Cette publication ne vaut ni approbation de l’architecture, ni autorisation
de développement. Les modèles, critères et scénarios conservent leurs statuts;
les TRV/COT sont planifiés et NON EXECUTES. Aucun patch applicatif n’est
appliqué. Les archives de C0-A déjà approuvées et leurs manifestes sont conservés.

## Documents à examiner

| Élément | Document faisant autorité |
|---|---|
| Trois modèles, invariants, écarts et limites de cohérence | [MODELE_TRANSVERSAL_C](MODELE_TRANSVERSAL_C.md) |
| État VersionActe | [PlantUML](modele_global/etat_version_acte.puml), [SVG](modele_global/etat_version_acte.svg), [PNG](modele_global/etat_version_acte.png) |
| État RevisionPreuve | [PlantUML](modele_global/etat_revision_preuve.puml), [SVG](modele_global/etat_revision_preuve.svg), [PNG](modele_global/etat_revision_preuve.png) |
| ERD transversal avec cotation | [PlantUML](modele_global/erd_transversal_c.puml), [SVG](modele_global/erd_transversal_c.svg), [PNG](modele_global/erd_transversal_c.png) |
| Matrice synthétique transversale | [Matrice de couverture §13](MATRICE_COUVERTURE_V2_C.md#13-cohérence-transversale--actes-révisions-de-preuve-et-histoire) |
| Cotation documentaire déjà décidée | [Modèle spécialisé](MODELE_TRANSVERSAL_COTATION.md), [décision PO](references/DECISION_PO_COTATION_DOCUMENT_CITATIONS_2026-10-21.md) |
| User stories et activités actualisées | [Index des stories](../modele_preuve/diagrammes/user_stories_architecture_c/README.md) |
| Spécifications et vues locales manquantes | [Plan UML §11](PLAN_MODELISATION_UML.md#11-cohérence-transversale-c-trans--21-octobre-2026), [registre existant](registre_validation.md) |
| Lots et dépendances conception / implantation | [Backlog §15](BACKLOG_ARCHITECTURE_C.md#15-fondations-transversales--r8-trans) |
| Autorités D/CF et compléments | [Décisions consolidées](DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md), [avenant](AVENANT_ARCHITECTURE_C.md) |
| Contrôles et empreintes des vues livrées | [Relevé documentaire](modele_global/controles_transversal_c_2026-10-21.json), [SHA-256](modele_global/manifest_transversal_c_2026-10-21.json) |
| États antérieurs exacts | [Avant cotation](historique/2026-10-21_avant_cotation_document_citations/README.md), [avant cohérence transversale](historique/2026-10-21_avant_coherence_transversale/README.md) |

## Questions encore soumises au Product Owner

Les questions restent portées par l’[avenant §7](AVENANT_ARCHITECTURE_C.md#7-dépendances-et-arbitrages-résiduels)
et les tickets DEC-R du backlog existant. Ce tableau est un index pour examen,
non un nouveau registre de décisions.

| Réserve | Arbitrage fonctionnel restant / recommandation déjà formulée |
|---|---|
| R01 | Continuité de l’identité logique d’une composition modifiée : maintien seulement par décision explicite, ou nouvelle identité avec filiation |
| R02 | Compositions simultanées d’une même identité et déduplication : recommandation d’une composition active, sans fusion automatique d’identités distinctes |
| R03 | Date de classement des composites et traitement des dates trop vagues; conserver la précision et la provenance, sans inventer une date probatoire |
| R05 | Choix explicite et conservé entre usage analytique et production, avec exceptions diagnostiquées |
| R06 | Parcours de rédaction et règle des brouillons actifs / variantes personnelles; la pluralité des versions et le mono-utilisateur sont déjà acquis |
| R07 | Niveau supplémentaire éventuel de régénération; la restitution des octets conservés est déjà obligatoire |

**Modalités techniques à proposer puis soumettre dans les dossiers :** R04
notation/ordonnancement des sous-cotes; R08 stockage immuable, droits,
finalisation et récupération. Aucun de ces choix n’est approuvé ici.
Le principe cote principale du document / sous-cotes de ses citations et
le document retenu sans citation (une cote, zéro sous-cote) sont **décidés**.
D07/CF4 attendent les vérifications des sources, distinctes d’un arbitrage
sur ce principe. Les contraintes physiques de RevisionPreuve et la clôture
exacte du gel restent à justifier dans les vues locales.

## C0-A et priorité suivante

Les versions approuvées de [UC13](versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md),
[UC14](versions_approuvees/UC-C-14_C0A-UML-R2-HIST/README.md) et
[UC15](versions_approuvees/UC-C-15_C0A-UML-R2-DIAG/README.md) restent inchangées.
Les documents et preuves de la revue antérieure de reprise sont conservés
comme historique; leur verdict porte sur le patch antérieur à B01.

Après cette publication, la priorité demandée est la revue indépendante
ciblée du delta B01 livré par A au commit
`f35ec8586866f4359d44f52a0bc5cc57c0804217`. Cette publication n’en annonce
aucun verdict et ne fusionne ni ce commit ni le code de C0-A. La branche
ne transporte aucune modification applicative des branches de A.

## Dépendances documentaires incluses

Les stories, ERD/classes observés P6 et sources de conception qu’indexent les
autorités C étaient encore absents de main. Ils sont inclus pour rendre
la consultation des renvois possible, sans transporter leur code applicatif.
Les liens de code du dictionnaire de classes sont fixés à P6; leur
[copie originale](historique/2026-10-21_publication/README.md) est conservée.
Aucune autre modification des trois sources C-TRANS et de leurs rendus.
