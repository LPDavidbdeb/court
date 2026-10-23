# UC14 R3-CONC — Conception approuvée et préparation de la vérification

**23 octobre 2026 — branche documentaire `docs/uc14-r3-conc-20261023`.**
Publication des artefacts exacts présentés dans la session. Base documentaire :
`976982394cc1c8046eec4e5ed5ab3e866bcdbb5b`, publication des modèles transversaux.
La branche est destinée à l'examen, sans fusion dans `main` ni changement
applicatif. Aucun patch de correction n'est appliqué par cette publication.

**Conception R3-CONC : APPROUVE_UTILISATEUR le 23 octobre 2026 au commit
`b0adf1136c55c38a830d3a1cd1a4332741bf297d`, après la revue indépendante
VALIDE_ARCHITECTURE.** L'autorisation corrective reste limitée aux cinq
fichiers du §6 approuvé. La vérification applicative est en attente; aucun
candidat R3 ni résultat R3 n'est présenté. Le candidat `f35ec85` demeure
NON CONFORME et l'intégration C0-A reste bloquée.

La publication de l'approbation et de la grille utilise **la même branche**.
Les fichiers du dossier R3 approuvé restent intacts. Les mentions « approbation
AUCUNE » de ses documents désignent leur état historique avant la décision;
le registre courant porte l'approbation nouvelle.

## Diagrammes à examiner

Les PNG s'affichent directement sur GitHub. Les SVG permettent l'examen en
grand format; les sources PlantUML sont conservées pour reproduction.

| Vue | Aperçu PNG | SVG | Source PlantUML |
|---|---|---|---|
| Séquence T1/T2 : deux issues conformes, verrou et commit externe | [PNG](use_cases/UC-C-14/revisions/R3-CONC/sequence.png) | [SVG](use_cases/UC-C-14/revisions/R3-CONC/sequence.svg) | [PUML](use_cases/UC-C-14/revisions/R3-CONC/sequence.puml) |
| Activité de suppression UC14 | [PNG](use_cases/UC-C-14/revisions/R3-CONC/activity.png) | [SVG](use_cases/UC-C-14/revisions/R3-CONC/activity.svg) | [PUML](use_cases/UC-C-14/revisions/R3-CONC/activity.puml) |
| Classes et responsabilités transactionnelles | [PNG](use_cases/UC-C-14/revisions/R3-CONC/class.png) | [SVG](use_cases/UC-C-14/revisions/R3-CONC/class.svg) | [PUML](use_cases/UC-C-14/revisions/R3-CONC/class.puml) |
| ERD R2-HIST conservé, aucun changement métier | [PNG](use_cases/UC-C-14/revisions/R3-CONC/erd.png) | [SVG](use_cases/UC-C-14/revisions/R3-CONC/erd.svg) | [PUML](use_cases/UC-C-14/revisions/R3-CONC/erd.puml) |
| Complément : annulation T1 et reprise T2 | [PNG](use_cases/UC-C-14/revisions/R3-CONC/sequence_rollback.png) | [SVG](use_cases/UC-C-14/revisions/R3-CONC/sequence_rollback.svg) | [PUML](use_cases/UC-C-14/revisions/R3-CONC/sequence_rollback.puml) |
| Complément : plusieurs occurrences et effets indépendants | [PNG](use_cases/UC-C-14/revisions/R3-CONC/sequence_multiple.png) | [SVG](use_cases/UC-C-14/revisions/R3-CONC/sequence_multiple.svg) | [PUML](use_cases/UC-C-14/revisions/R3-CONC/sequence_multiple.puml) |
| Complément : édition UC13 / sauvegarde ORM T2 | [PNG](use_cases/UC-C-14/revisions/R3-CONC/activity_t2.png) | [SVG](use_cases/UC-C-14/revisions/R3-CONC/activity_t2.svg) | [PUML](use_cases/UC-C-14/revisions/R3-CONC/activity_t2.puml) |

<details>
<summary>Afficher la séquence principale T1/T2</summary>

![Séquence UC14 R3-CONC](use_cases/UC-C-14/revisions/R3-CONC/sequence.png)

</details>

<details>
<summary>Afficher l'activité de suppression</summary>

![Activité UC14 R3-CONC](use_cases/UC-C-14/revisions/R3-CONC/activity.png)

</details>

<details>
<summary>Afficher les responsabilités de classes et services</summary>

![Classes UC14 R3-CONC](use_cases/UC-C-14/revisions/R3-CONC/class.png)

</details>

<details>
<summary>Afficher l'ERD conservé</summary>

![ERD UC14 R2-HIST conservé](use_cases/UC-C-14/revisions/R3-CONC/erd.png)

</details>

## Pièces de validation et références

| Pièce | Lien |
|---|---|
| Approbation utilisateur et portée corrective exacte | [Attestation](lots/C0-A/verification_R3_CONC/APPROBATION_UTILISATEUR.md), [mandat source](references/MANDAT_APPROBATION_UC14_R3_CONC_2026-10-23.md) |
| Vérification du futur candidat : sept vues, 17 contrôles et T01–T24 | [Grille de conformité](lots/C0-A/verification_R3_CONC/GRILLE_REVUE_CONFORMITE.md) |
| Intégrité des références R2/R3 et état de préparation | [Preuves d'intégrité](lots/C0-A/verification_R3_CONC/INTEGRITE_CONCEPTIONS_APPROUVEES.json), [rapport](lots/C0-A/verification_R3_CONC/RAPPORT_PREPARATION_VERIFICATION.md) |
| Dossier R3-CONC complet | [README](use_cases/UC-C-14/revisions/R3-CONC/README.md) |
| Défaut, mécanisme, cohérence et périmètre des cinq fichiers proposé | [Analyse](use_cases/UC-C-14/revisions/R3-CONC/analyse_coherence.md) |
| AC01–AC07 conservés et garanties techniques proposées | [Spécification](use_cases/UC-C-14/revisions/R3-CONC/specification.md) |
| Revue indépendante de conception et limites de son verdict | [Validation](use_cases/UC-C-14/revisions/R3-CONC/validation.md), [attestation B](use_cases/UC-C-14/revisions/R3-CONC/revue_B.md) |
| Essais T01–T24 prévus, NON EXECUTES | [Plan d'essais](use_cases/UC-C-14/revisions/R3-CONC/plan_tests.md), [traçabilité](use_cases/UC-C-14/revisions/R3-CONC/tracabilite.md) |
| Sources et rendus exacts soumis à la revue | [Manifeste de conception](use_cases/UC-C-14/revisions/R3-CONC/manifest_conception.json) |
| Livraison complète et contrôles réellement exécutés | [Manifeste de livraison](use_cases/UC-C-14/revisions/R3-CONC/manifest_livraison.json), [contrôles documentaires](use_cases/UC-C-14/revisions/R3-CONC/controles_documentaires.json) |
| Constat du défaut ayant motivé la révision | [Revue B01](lots/C0-A/REVUE_INDEPENDANTE_B01.md), [preuves historiques](lots/C0-A/preuves_revue_B01/README.md) |
| Références approuvées préservées | [UC13 R2-ST](versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md), [UC14 R2-HIST](versions_approuvees/UC-C-14_C0A-UML-R2-HIST/README.md), [UC15 R2-DIAG](versions_approuvees/UC-C-15_C0A-UML-R2-DIAG/README.md) |
| Statuts par version | [Registre unique](registre_validation.md) |

SHA-256 du manifeste de conception examiné :
`258ca9a719c0b172461f75dc5f27bb98b74335b532340c00654b5165f7e87b0d`.
SHA-256 du manifeste de livraison :
`b1ecaf1ebb55cc84b989153c1b6536836cdfbf3184c7d0e59cb2498fc27818ba`.

Les fichiers R3-CONC sont publiés sans réécriture. Seul le chemin d'inclusion
du style dans la copie de l'ERD diffère de R2-HIST, comme documenté lors de la
revue. Les anciennes vues, leurs archives approuvées et leurs manifestes
restent intacts. Les preuves B01 et les patches conservés sont documentaires;
ils ne sont ni appliqués ni réexécutés ici. L'orphelin tardif reste distinct.

## Suite attendue

L'approbation de la conception et l'autorisation corrective isolée sont
enregistrées; aucun nouveau feu vert pour cette même portée n'est demandé.
La preuve opérationnelle attend un candidat identifié, les essais réels
et sa nouvelle revue indépendante. Les rapports de préparation et leurs
preuves consignent l'étape documentaire antérieure à cette publication.
Aucune autorisation d'intégration, fusion, migration ou déploiement ne découle
de la mise à disposition sur GitHub. L'orphelin tardif n'est ni corrigé ni
testé ici; la voie d'ajout UC02 reste exclue.
