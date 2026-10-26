# UC-C-13 — Validation documentaire

**C0A-UML-R1 — 20 octobre 2026.** Conception et revue documentaire : B.
Référence observée proposée : `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`.
Modèle global : G-C0A-R1. Les [empreintes complètes](manifest_sha256.json)
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
| [activity](activity.svg) | OK, compilation 0 et inspection B | `f408867d762c5dbca76ec6b3c60745838ba391a7614c6ac014e0912891bdccc1` | `2a18075d4737862998e40f4c64a98fb0d76cf7d2f6dc5cb1ea953319142452a5` |
| [sequence](sequence.svg) | OK, compilation 0 et inspection B | `67b7c7e1547c3f6ddc34e0294b09d506e49f1c45d9e0a4ce655edc53b6319ccb` | `4e97fda8d2e1993defc26363ad2a20fbe3c033a2fa8ca14a60120dfe62005a8e` |
| [erd](erd.svg) | OK, compilation 0 et inspection B | `f6b7766a962d2de5009f864db8e2bda67556eb62f959320b8573dfb0a3193e6d` | `099cfe542fdec84ad394eb7d680fda4fbaa15507641988bdf4cb0477969eff2d` |
| [class](class.svg) | OK, compilation 0 et inspection B | `c809381fc595e7c6aed7dda43976a4e6c56b44553f03ecabee6bc030a83ab51f` | `b06b469791a4bd7f6ec59b05c2fa3518cc4251b80a915635daebd1ebe795ed9a` |

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
| A1 | Nominal, texte identique, privé/partagé, structure vide et refus ont des branches activité/séquence; rollback explicite. |
| A2 | Vue → concordance.detacher_pour_edition → protection / ORM / VersionTexte; fraîcheur portée par Correspondance et ConfirmationAppui. |
| A3 | Toutes les données nécessaires figurent dans l’ERD local ou dans G-C0A-R1; source_type, ContentType et GFK explicités; aucun modèle proposé fictivement existant. |
| A4 | Capture avant modification et association de l’occurrence réelle; schéma et cascades existants conservés; limites du set de captures explicites. |
| A5 | Texte dans Statement, position dans LibraryNode, décisions E01 conservées; aucun appui ou journal concurrent créé. |
| A6 | Transaction HTTP et service imbriqué; annulation des nouveaux objets au refus; pas de fichier ou finalisation de gel dans ce use case. |
| A7 | Référents protégés, pas de recotation ni altération de juillet, type Statement contrôlé; aucun assouplissement HERITE/PHRASE. |
| A8 | Contrat de capture partagé avec 14; lecture des appuis 15 indépendante. C0A-REV-01 bloque le lot, sans modifier le contrat d’édition 13. |

Revue F B : AC01–AC08 et leurs contre-épreuves sont représentés. La conservation garantie porte sur les captures disponibles, sans reconstruire un examen manquant. La sérialisation universelle, les gardes SQL/bulk, le manifeste des occurrences et le gel global sont explicitement hors périmètre. Aucune contradiction bloquante restante dans ce périmètre documentaire.

## 4. Attestation B et décision utilisateur

**VALIDE_ARCHITECTURE — attestation B du 20 octobre 2026**, limitée à la conception UC-C-13 C0A-UML-R1 et aux fichiers du manifeste. Revue T/F/A et traçabilité complètes dans ce périmètre. Aucun arbitrage R01–R08 nécessaire à ce comportement. Cette attestation ne valide pas dynamiquement le patch sur le socle proposé et ne valide pas l’ensemble du lot C0-A.

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
| 2026-10-20 | Création C0A-UML-R1; compilation et revue documentaire B | Validation B limitée à 13, dossier soumis à approbation; aucune décision utilisateur |
