# UC-C-15, résultat partiel qualifié C15-D1 — Validation documentaire B

**C0A-UML-R2-DIAG — 20 octobre 2026 — VALIDE_ARCHITECTURE.** Auteur/revue : B.
Code lu : 515666e; modèle global proposé : G-C0A-R3-CIT.
[Spécification](specification.md), [traçabilité](tracabilite.md), [empreintes](manifest_sha256.json).
Les quatre vues sont des cibles documentaires, pas du code implanté.
L’[approbation UC13](../../use_cases/UC-C-13/approbation.json) ne s’étend pas à ce dossier.

## 1. Contrôle technique T

PlantUML 1.2026.8 / 149874a, Graphviz 12.2.1. Dix-neuf sources concernées
(UC14/15, deux sous-cas citations dont un état, deux modèles globaux), compilation
finale SVG code **0**. Les premières erreurs d’échappement ont été corrigées;
les cinq vues ajustées en revue ont été recompilées avec succès.
PNG sur fond blanc avec rsvg-convert, code 0. B a ouvert les dix-neuf PNG,
puis réinspecté les cinq rendus corrigés : lisibles, accents conservés, pas de
troncature ou de collision gênant la lecture. Les grands ERD/classes restent
consultables en SVG avec zoom; le global de classes a été rééquilibré.
Aucune des douze sources/images approuvées UC13 n’a été régénérée ou modifiée.

| Vue | Résultat T / visuel | SHA-256 source |
|---|---|---|
| [activity](activity.svg) | compilation finale 0; PNG ouvert par B | `ba4b7e489423a0f7001d4e0b713c3e47a72a213fcd0210255539f3ee6ad46459` |
| [sequence](sequence.svg) | compilation finale 0; PNG ouvert par B | `ccfa4b38bedee9b5d78a63c33d0d7b6eb57f1744d125a4b22e4dab1064f42ff6` |
| [erd](erd.svg) | compilation finale 0; PNG ouvert par B | `299697646fe490c835270d1404b56bc28cec9ce11f17e14ca7d2cd0eaa71fd60` |
| [class](class.svg) | compilation finale 0; PNG ouvert par B | `0410a51a987c54088d8cd3dbe154f05347807eb7abc429a27697febf84430756` |

Inclusions locales seulement; style commun inchangé. Commandes et empreintes
sont reprises dans [la preuve commune](../../lots/C0-A/VALIDATION_UML_C0A.json).
Les états UC12 constituent un complément, pas un remplacement d’une vue.

## 2. Contrôle fonctionnel F

Chaque AC est rattaché aux éléments ACT / SEQ / ERD / CLS et aux scénarios
nommés. Les résultats attendus, refus et états devant rester inchangés sont
explicités dans la traçabilité. Les scénarios applicatifs, PostgreSQL, HTTP,
interface et concurrence sont tous **NON EXECUTES** dans ce mandat.
Aucun succès P6 ou de A n’est transféré à la correction proposée.

## 3. Contrôle architectural A1–A8

| Contrôle | Conclusion et limite |
|---|---|
| A1 | La boucle distingue structure, Statement vérifié et anomalie locale; l’erreur globale et la panne technique ont des sorties explicites. |
| A2 | Concordance contrôle couple/types et accumule; export conserve les deux listes puis les transmet aux contrôles EX. Chaque résultat a une responsabilité nommée. |
| A3 | Toutes les données lues sont dans l’ERD existant; LectureAppuis, DiagnosticAppui et erreur de contexte sont non persistants. |
| A4 | Aucune PK générique ou archive non typée n’est convertie en Statement. Chaque appui conserve ses identités de groupe/extrémité/origine. |
| A5 | La lecture VERSION SOURCE ne crée ni confirmation, ni sélection courante, ni nouvelle filiation. Le vide ne décide pas d’absence d’appui. |
| A6 | Aucune écriture; les exceptions techniques se propagent. Après collecte, une incomplétude empêche le strict; un succès local ne satisfait pas les autres EX. |
| A7 | EX01–EX07 restent cumulatifs, EX04 reçoit les défauts de résolution; pas de EX08, de nature anticipée ou de certification de citation inventée. |
| A8 | UC14 conserve les contenus et archives disponibles; UC12 qualifie l’examen séparément. La certification de A n’est pas une confirmation éditoriale E01. |

B valide le contrat de correction proposé, et non le patch. La boucle ne perd
aucun résultat valide en raison d’une autre origine invalide; les diagnostics
restent visibles et empêchent le strict si la résolution est incomplète.
C15-D1 reste à approuver fonctionnellement. **C0A-REV-01 reste ouverte dans
le code**, sans test exécuté de correction. Aucune réserve interne bloquante
à ce contrat documentaire n’est identifiée.

## 4. Attestation et décision attendue

**VALIDE_ARCHITECTURE — B, 20 octobre 2026 — UC-C-15, résultat partiel qualifié C15-D1, C0A-UML-R2-DIAG**, fichiers du manifeste.
Cette attestation ne certifie aucune implantation, migration, capacité de
journal/adaptateur, fermeture SQL/bulk, gel global ou conformité du patch.
**Approbation utilisateur : AUCUNE. PRET_DEVELOPPEMENT : NON.**
Les réserves fonctionnelles sont celles de la spécification et de l’analyse
ciblée; aucune approbation implicite n’est déduite d’un diagramme compilé.

## 5. Journal / conformité future

La version R1 de UC14/15 et G-R2 est conservée au commit cd584c3; le dossier
UC13 approuvé dispose aussi d’une copie exacte et de son manifeste d’origine.
Cette révision C0A-UML-R2-DIAG est soumise à un examen graphique réel. Tout autre
choix fonctionnel impose mise à jour des vues et nouvelle validation.
Un futur mandat A devra citer les versions approuvées, le socle et les fichiers
permis, la copie indépendante, PostgreSQL jetable et les tests à exécuter.
Aucun mandat d’implantation ni autorisation de fusion applicative n’est émis.
Conformité après implantation : NON EVALUEE; code et patch restent inchangés.
