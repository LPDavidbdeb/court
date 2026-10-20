# UC-C-12::DIAGNOSTIQUER_EXAMEN seulement — Validation documentaire B

**CIT-UML-R1 — 20 octobre 2026 — EN_REVUE.** Auteur/revue : B.
Code lu : 515666e; modèle global proposé : G-C0A-R3-CIT.
[Spécification](specification.md), [traçabilité](tracabilite.md), [empreintes](manifest_sha256.json).
Les quatre vues sont des cibles documentaires, pas du code implanté.
L’[approbation UC13](../../../use_cases/UC-C-13/approbation.json) ne s’étend pas à ce dossier.

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
| [activity](activity.svg) | compilation finale 0; PNG ouvert par B | `032f7d26dd8774cebdfb726af41494d330bc894612345ef0142b0a0d6155be95` |
| [sequence](sequence.svg) | compilation finale 0; PNG ouvert par B | `a79f31506b986b2c2cbac7baf7829201b346cfc7cd236c58f14b7a3772da4326` |
| [erd](erd.svg) | compilation finale 0; PNG ouvert par B | `6b136b721976245c738edef4ea7b06433d65da80d41dbdb4828526b77516c629` |
| [class](class.svg) | compilation finale 0; PNG ouvert par B | `4cdbce4ff2c9ba0bf4b8efa845e5764469ab36e09e7945013c3a4de9feb4f770` |

Inclusions locales seulement; style commun inchangé. Commandes et empreintes
sont reprises dans [la preuve commune](../../../lots/C0-A/VALIDATION_UML_C0A.json).
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
| A1 | Les branches décision absente, capture manquante, type hors contrat, source invalide, divergence et contrôle limité sont visibles; états complémentaires cohérents. |
| A2 | QualificationExamen explique l’état sans écrire; UC05E est responsable du futur ajout, jamais du diagnostic C0-A. |
| A3 | Correspondance, VersionTexte et types Quote existants; journal jaune PROPOSE L1-A, clairement absent du schéma C0-A. |
| A4 | Une Quote n’est pas capturée comme Statement. Un ancien examen manquant n’est pas inventé. Une nouvelle décision future n’écrase pas l’ancienne. |
| A5 | Admissibilité fournisseur, fraîcheur éditoriale et confirmation d’appui restent distinctes; aucune certification automatique HERITE/PHRASE. |
| A6 | Le présent sous-cas est en lecture seule. Les écritures/rollback de nouvel examen sont dessinés seulement sous garde de capacités futures disponibles et autorisées. |
| A7 | Lecture de l’occurrence réelle et captures disponibles; les limites de composition et de contexte sont exposées. Gel global et manifeste typé ne sont pas réputés livrés. |
| A8 | CIT-D3/D4 ouverts; journal UC05E/L1-A, adoption C0-B et adaptateur de régime requis selon le type. Pas de dépendance circulaire pour le diagnostic seul. |

Attestation B de revue : les quatre vues, états et limites permettent un examen
graphique de CIT-D3/D4. Leur approbation, le contrat de diagnostic et les préalables
réels du nouvel examen restent à arrêter. Aucune attestation de reconfirmation
opérationnelle ou de validation complète de UC12 n’est accordée. La fonction
actuelle qui remplace les champs/M2M n’est pas assimilée au journal futur.

## 4. Attestation et décision attendue

**EN_REVUE — B, 20 octobre 2026 — UC-C-12::DIAGNOSTIQUER_EXAMEN seulement, CIT-UML-R1**, fichiers du manifeste.
Cette attestation ne certifie aucune implantation, migration, capacité de
journal/adaptateur, fermeture SQL/bulk, gel global ou conformité du patch.
**Approbation utilisateur : AUCUNE. PRET_DEVELOPPEMENT : NON.**
Les réserves fonctionnelles sont celles de la spécification et de l’analyse
ciblée; aucune approbation implicite n’est déduite d’un diagramme compilé.

## 5. Journal / conformité future

La version R1 de UC14/15 et G-R2 est conservée au commit cd584c3; le dossier
UC13 approuvé dispose aussi d’une copie exacte et de son manifeste d’origine.
Cette révision CIT-UML-R1 est soumise à un examen graphique réel. Tout autre
choix fonctionnel impose mise à jour des vues et nouvelle validation.
Un futur mandat A devra citer les versions approuvées, le socle et les fichiers
permis, la copie indépendante, PostgreSQL jetable et les tests à exécuter.
Aucun mandat d’implantation ni autorisation de fusion applicative n’est émis.
Conformité après implantation : NON EVALUEE; code et patch restent inchangés.
