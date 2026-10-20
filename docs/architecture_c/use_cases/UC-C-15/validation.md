# UC-C-15 — Validation documentaire

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
| [activity](activity.svg) | OK, compilation 0 et inspection B | `5409e23bddb93596ed7e82b4906e28b31da021d9ab5b834adf28625217fb4b9e` | `822a84192b0ec55bddfa47bcedb6d1fac7bc60d21671731ebc84cfc4117d1a6b` |
| [sequence](sequence.svg) | OK, compilation 0 et inspection B | `1ec7810f18b103d4f2731b9d9d5bb4670d21e98cef9c48fffdd846b1288e2d94` | `103e007b666cf5cae30e9b4d9e3e6b6407878cf3fcb77a0f793f4531df62900e` |
| [erd](erd.svg) | OK, compilation 0 et inspection B | `23a86628bdc514cdc43306ba6ad7657833672ed5e2b8f033a06efe07ce4047ce` | `42c4f852b3d7cc691b7917090dcbb7d71ea841ee6a632e77714d0a4a0a92c647` |
| [class](class.svg) | OK, compilation 0 et inspection B | `11cf54d4d9975bb43753c9fe6d028d98cef5b38d36f71419b22eb117bb5bec06` | `c19b3483c810b4e91c41a24cb5984437b28bee3301c8f19c3da344251a373b72` |

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
| A1/A2 | Lecture par couple et traitement local d’anomalies représentés; interface LectureAppuis proposée et identifiée comme non persistante. |
| A3/A4 | Données E01 seulement; archive sans type non résolue par supposition; pas de nature anticipée. |
| A5/A6 | Appui historique distinct du courant; aucune écriture, aucun export réputé strict sur la seule lecture partielle. |
| A7/A8 | Patch actuel non conforme AC03/AC06; contrat d’erreur globale / anomalie locale et ses consommateurs à revoir puis approuver avant correction A. |

AC01–AC06 et cas mixtes explicités. C0A-REV-01 est confirmé par la fonction du patch exécutée en mémoire avec doubles; l’export est inspecté statiquement. L’API de retour et les diagnostics doivent être approuvés avant correction. Aucun test ORM/HTTP/SQL de la correction, puisqu’elle n’est pas implantée.

## 4. Attestation B et décision utilisateur

**EN_REVUE.** Contrôle T effectué; contrat de correction proposé, revue F/A à clôturer et approbation à obtenir. Le patch existant ne satisfait pas AC03/AC06; aucune conformité applicative attestée.

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

Lire un appui historique conservé ne donne aucun droit de réutiliser son
Statement dans une nouvelle occurrence. Les anciens liens incompatibles
restent consultables sans certification de provenance actuelle. **C0A-REV-01
reste ouverte**, sans correction du patch et sans nouveaux essais ORM/HTTP/SQL.
Statut : EN_REVUE.
