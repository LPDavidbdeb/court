# UC-C-02::RENOMMER_CITATION seulement — Validation documentaire B

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
| [activity](activity.svg) | compilation finale 0; PNG ouvert par B | `def04f85eb6083899227f0fd0a76d6797e84be9c014a516b546db418770bf0a3` |
| [sequence](sequence.svg) | compilation finale 0; PNG ouvert par B | `7a1cfd0c7e363ccfe5f0443545dd5b4a35cd4625636a51693f8ad7127036ef88` |
| [erd](erd.svg) | compilation finale 0; PNG ouvert par B | `9884d9650e2d0db32a9d55c239b7891c5851535c7535edc747e611f8f091e95c` |
| [class](class.svg) | compilation finale 0; PNG ouvert par B | `05d88b95d82a9fb95a5665d6d9d454c56cd28cff9a7c6c304cd3157ff10da59d` |

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
| A1 | Nominal item seul, no-op, protections, type/régime, contexte et rollback sont représentés; erreur de sauvegarde tardive explicite. |
| A2 | Une action distincte UC02 et ServiceRenommage portent l’écriture de item; le résolveur de citation est en lecture seule. |
| A3 | LibraryNode.item existe; Quote et champs de régime restent existants. Genre/index sont calculés, pas des colonnes nouvelles. |
| A4 | GFK, source, texte, ancrage et certification inchangés. Contexte dépendant ou indéterminable est refusé; aucune ancienneté d’examen reconstruite. |
| A5 | UC13 garde son contrat d’édition de Statement approuvé; le libellé rédactionnel n’est pas un service d’édition probatoire. |
| A6 | Recontrôle dans opération locale atomique; état attendu et refus explicites. Aucun verrou général ou gel universel déclaré réalisé. |
| A7 | Gestionnaires HERITE/PHRASE distincts, pas de fallback par PK ou derived_from et aucune activation des rendus/contrôles de A. |
| A8 | Arbitrage CIT-D1/D2 ouvert sur l’autorisation limitée et le contexte. Route/formulaire/interface hors des huit fichiers nécessiteraient un mandat supplémentaire. |

Attestation B de revue : quatre vues T et traçabilité présentes; la conception
conservatrice est explicitée. Le choix d’autoriser ce renommage limité et sa
frontière de contexte doivent encore être tranchés (CIT-D1/D2); aucune attestation
VALIDE_ARCHITECTURE de tout UC02, approbation utilisateur ou extension C0-A.
Le dossier ne promet pas de reconnaître automatiquement la sémantique d’un item.

## 4. Attestation et décision attendue

**EN_REVUE — B, 20 octobre 2026 — UC-C-02::RENOMMER_CITATION seulement, CIT-UML-R1**, fichiers du manifeste.
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
