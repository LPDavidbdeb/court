# UC-C-14 — Validation documentaire

**C0A-UML-R1 — 20 octobre 2026.** Conception et revue documentaire : B.
Référence observée proposée : `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`.
Vues locales : C0A-UML-R1 inchangées. Modèle global de contexte : G-C0A-R2-ST.
Le contrôle T ci-dessous est celui de R1; l’actualisation ST est précisée en fin de dossier. Les [empreintes complètes](manifest_sha256.json)
identifient spécification, traçabilité, sources, rendus et inclusions.

## 1. Contrôle technique T

PlantUML 1.2026.8 / 149874a; GraphViz 12.2.1. Compilation/rendu final :
code **0**, quatre sources locales et deux modèles globaux, sans inclusion distante.

```sh
plantuml -charset UTF-8 -tsvg 'docs/architecture_c/modele_global/*.puml' 'docs/architecture_c/use_cases/UC-C-13/*.puml' 'docs/architecture_c/use_cases/UC-C-14/*.puml' 'docs/architecture_c/use_cases/UC-C-15/*.puml'
```

Depuis la racine du dépôt. Pour chaque SVG :
`rsvg-convert --background-color=white -o <nom>.png <nom>.svg`, code 0.
Sources et rendus contrôlés visuellement par B : textes lisibles, accents
conservés, pas de troncature; erreurs/refus visibles. L’ERD reste une vue
logique partielle et n’est pas un relevé complet de la base. Les PNG sont conservés.

| Vue | Résultat T / contrôle visuel | SHA-256 source | SHA-256 SVG |
|---|---|---|---|
| [activity](activity.svg) | OK, compilation 0 et inspection B | `67bb8fa78d2001e6af6bc004fc83c7c45345935cad236f3223c7236dbfec8e28` | `f2c002a904e54d4a05438cc1172fac85bf2096bc760ee49dfd7ef9b352f1689c` |
| [sequence](sequence.svg) | OK, compilation 0 et inspection B | `ca23a53eb847fbe48ea0355767949c47589f4809ab5da94b6dcf612a794b40f4` | `2f080db217c8ba25bcb5e7c2fd229f13bedeaacf995c3d2c7fb85cc103d411e9` |
| [erd](erd.svg) | OK, compilation 0 et inspection B | `910a555744763fcd0416daba78fcbe64894b6843f7d3e391e6f9809db6e538c8` | `31a38e5a75911859857153d1235381d24d9accbd4ad464f2c28ad5ad6f51240e` |
| [class](class.svg) | OK, compilation 0 et inspection B | `36d279c1f83e787ae625094f05e2a6989a8dedc109a9c968ac5400faa06d7f87` | `32b835886757c636b82175a9991df1377ce6e56b299c5745878d0f268146248e` |

Style local inclus : `../../modele_global/style.iuml`, empreinte dans le manifeste.
Preuves communes : [validation UML C0-A](../../lots/C0-A/VALIDATION_UML_C0A.json).

## 2. Contrôle fonctionnel F

[Traçabilité](tracabilite.md) : critères reliés aux éléments précis des quatre vues.
**Tests applicatifs sur le nouveau socle : NON EXECUTES.** Les méthodes du patch
et ses 209 résultats historiques P6 ne sont pas de nouvelles preuves sur `515666e`.
La contre-épreuve de lecture en mémoire est distincte des essais Django/HTTP/SQL.

## 3. Contrôle architectural A1–A8

| Contrôle | Revue et limite |
|---|---|
| A1/A2 | Précontrôle, archives, repointage et purge représentés avec leurs responsables; revue détaillée F/A à clôturer après priorité 13. |
| A3/A4 | Schéma réel, RefHistorique et appuis nécessaires au refus/purge représentés; refus avant capture et rollback de service explicités. |
| A5/A6 | Archive ne devient pas un nouveau journal; transaction de service distincte du catch HTTP; aucun stockage externe. |
| A7/A8 | Garanties complètes NR12/CF3-25 différées; lecture depuis une archive non typée renvoie au contrat 15 et au défaut C0A-REV-01. |

Critères AC01–AC06 et scénarios fournis. La revue détaillée du bloc, des cascades et des variantes de données reste à clôturer par B; les exécutions sur le nouveau socle devront être mandatées à A.

## 4. Attestation B et décision utilisateur

**EN_REVUE.** Contrôle T effectué et traçabilité proposée; l’attestation F/A complète reste à clôturer. Aucune VALIDE_ARCHITECTURE ni approbation utilisateur accordée à ce dossier.

**Décision utilisateur : AUCUNE APPROBATION DU DOSSIER.**
Version proposée : C0A-UML-R1; périmètre exact et empreintes : manifeste lié.
Aucune transition APPROUVE_UTILISATEUR ou PRET_DEVELOPPEMENT.

## 5. Préparation du développement et conformité ultérieure

Mandat A : **ABSENT** pour la nouvelle correction/validation sur `515666e`.
Copie Git indépendante, configuration synthétique sans écriture réelle et
PostgreSQL jetable exigés dans le futur mandat. Les fichiers autorisés et
le circuit Git devront être décidés. Aucune migration, implantation, application
du patch ou intégration exécutée par ce dossier.

Conformité après implantation : **NON EVALUEE**. B comparera diff, routes,
services, schéma inchangé et résultats aux quatre vues; tout écart contractuel
impose révision/revalidation. La clôture du lot reste soumise aux six conditions.

## 6. Journal documentaire

| Date | Version / action | Effet |
|---|---|---|
| 2026-10-20 | Création C0A-UML-R1; compilation et revue documentaire B | Dossier préparé; revue F/A ouverte; aucune décision utilisateur |


## 7. Analyse d’impact ST-R1, sans validation supplémentaire

Le [contrat Statement](../../INVARIANTS_STATEMENT_REPRODUCED_PRODUCED.md)
ne modifie pas les quatre vues locales de ce dossier : leurs octets et rendus
R1 sont conservés. Les deux vues globales sont révisées G-C0A-R2-ST et leurs
empreintes actualisées dans le manifeste. Ce changement de contexte ne
clôture pas la revue F/A, et ne transfère aucune attestation de UC13.

Une suppression autorisée doit conserver les traces utiles; elle ne rend pas
réutilisable le Statement privé de l’ancien propriétaire. Cette propriété
durable n’existe pas encore dans le schéma : L1-A doit la porter, et UC14
sera revalidé pour ce mécanisme. Les partages privés hérités restent des
contre-épreuves à préserver, sans réparation automatique. Statut : EN_REVUE.
