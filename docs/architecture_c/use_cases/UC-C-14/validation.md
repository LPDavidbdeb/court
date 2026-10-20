# UC-C-14, option conservatrice C14-D1/C14-D2 — Validation documentaire B

**Suivi du 20 octobre 2026 : APPROUVE_UTILISATEUR**, version C0A-UML-R2-HIST,
commit `30724df7ec5cbd1aba8ef25d59b5c3a162d20dab` / PR #31. [Décision et portée](approbation.json).
L’attestation B ci-dessous est conservée comme contrôle précédant la décision;
ses mentions de décision attendue décrivent cette étape passée.
[Validation originale exacte](../../versions_approuvees/UC-C-14_C0A-UML-R2-HIST/use_cases/UC-C-14/validation.md).
Les quatre vues et critères ne sont pas modifiés; aucun essai applicatif nouveau.
**PRET_DEVELOPPEMENT : NON; [mandat proposé](../../lots/C0-A/MANDAT.md) à approuver.**

**C0A-UML-R2-HIST — 20 octobre 2026 — VALIDE_ARCHITECTURE.** Auteur/revue : B.
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
| [activity](activity.svg) | compilation finale 0; PNG ouvert par B | `0c9961078c28e93aff5c08b09fe91117c73bdb1f0592eb099406818e3c2fd77c` |
| [sequence](sequence.svg) | compilation finale 0; PNG ouvert par B | `48d19465addc59a10a115b11b7c60c20482be8c775bce902266fb69042b0c518` |
| [erd](erd.svg) | compilation finale 0; PNG ouvert par B | `be8e3c1d4dd8ed48fc7215ca94b652e52f52eadb599ebf3852099e5ce41dc394` |
| [class](class.svg) | compilation finale 0; PNG ouvert par B | `17d942770ce02231c0e69098f48b1832cc0994c6cba9e3ab9d03fb764d8e9c0a` |

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
| A1 | Requête, bloc entier, refus de mutabilité/type, archivage, repointage, retrait et annulation concordent entre activité et séquence. |
| A2 | Vue → service atomique → protection/ORM; archive et extrémités ont leurs modèles, aucun collecteur de contenu implicite. |
| A3 | Les colonnes de NoeudArchive, les captures et les relations sont existantes; absence de type historique explicitée. Aucun schéma ajouté. |
| A4 | C14-D2 refuse ce que l’archive ne sait pas conserver; C14-D1 supprime les seules occurrences. CASCADE de décision/ancrage refusée; toutes les captures sont conservées. |
| A5 | La filiation et l’examen antérieur ne deviennent pas des appuis courants. Aucun droit de partage privé n’est déduit d’un retrait. |
| A6 | Transaction de service imbriquée; échec après capture/repointage/retrait annule l’ensemble avant le catch HTTP. Concurrence globale non prétendue couverte. |
| A7 | ST01–ST05, cotes historiques et HERITE/PHRASE préservés; les contenus non Statement sont refusés, pas transformés ni détruits. |
| A8 | UC15 lit les archives comme historiques non typées; UC13 R2 reste inchangé. Journal, provenance/propriété et archives typées restent L1-A/C0-B; gel L5. |

B valide la cohérence de **l’option explicitement dessinée** : pas de purge et
refus des contenus non archivables. Aucun obstacle interne à ce contrat
n’est identifié. C14-D1 et C14-D2 sont des recommandations fonctionnelles à
approuver avec les quatre vues; elles ne sont pas considérées déjà décidées.
Si l’utilisateur retient une autre politique de purge ou d’archive, ce verdict
ne lui est pas transféré. C0A-14-01 demeure l’écart du patch à traiter sous mandat.

## 4. Attestation et décision attendue

**VALIDE_ARCHITECTURE — B, 20 octobre 2026 — UC-C-14, option conservatrice C14-D1/C14-D2, C0A-UML-R2-HIST**, fichiers du manifeste.
Cette attestation ne certifie aucune implantation, migration, capacité de
journal/adaptateur, fermeture SQL/bulk, gel global ou conformité du patch.
**Approbation utilisateur : AUCUNE. PRET_DEVELOPPEMENT : NON.**
Les réserves fonctionnelles sont celles de la spécification et de l’analyse
ciblée; aucune approbation implicite n’est déduite d’un diagramme compilé.

## 5. Journal / conformité future

La version R1 de UC14/15 et G-R2 est conservée au commit cd584c3; le dossier
UC13 approuvé dispose aussi d’une copie exacte et de son manifeste d’origine.
Cette révision C0A-UML-R2-HIST est soumise à un examen graphique réel. Tout autre
choix fonctionnel impose mise à jour des vues et nouvelle validation.
Un futur mandat A devra citer les versions approuvées, le socle et les fichiers
permis, la copie indépendante, PostgreSQL jetable et les tests à exécuter.
Aucun mandat d’implantation ni autorisation de fusion applicative n’est émis.
Conformité après implantation : NON EVALUEE; code et patch restent inchangés.
