# Registre courant de validation des use cases C

**Actualisation du 23 octobre 2026 — UC14 R3-CONC APPROUVE_UTILISATEUR au commit b0adf1136c55c38a830d3a1cd1a4332741bf297d; correction isolée limitée à cinq fichiers; vérification applicative en attente. Approbations R2 conservées.**

Autorité des transitions : [protocole](PROTOCOLE_VALIDATION_UML.md). Inventaire et dépendances : [plan](PLAN_MODELISATION_UML.md). Ce registre ne confond pas approbation architecturale de principe et approbation d’un dossier UML.

**État courant : UC14 R3-CONC est APPROUVE_UTILISATEUR par décision expresse du 23 octobre 2026 au commit documentaire b0adf1136c55c38a830d3a1cd1a4332741bf297d. Seule la correction isolée des cinq fichiers du §6 de l'analyse est autorisée; le présent mandat reste documentaire. Aucun candidat ni résultat applicatif R3 n'est identifié : vérification applicative en attente, T01–T24 NON EXECUTES. Le candidat C0-A f35ec85 reste NON CONFORME selon la [revue B01](lots/C0-A/REVUE_INDEPENDANTE_B01.md); le blocage d'intégration C0-A demeure. Ni intégration, fusion, migration ou déploiement autorisé. Aucun statut PRET_DEVELOPPEMENT global ni conformité applicative n'est attribué. UC13 R2-ST, UC14 R2-HIST et UC15 R2-DIAG sont conservés avec leurs approbations et empreintes; UC02/12 citations restent EN_REVUE.**

| Use case | Statut | Version du dossier / vues | Réserves propres | Validation B | Approbation utilisateur | Prêt / mandat de lot |
|---|---|---|---|---|---|---|
| UC-C-01A | `A_SPECIFIER` | [Complément C-TRANS](use_cases/UC-C-01A/specification.md); A0 actualisée à contextualiser; S/E/C locaux absents | R06 | AUCUNE | AUCUNE | NON; L1-A non autorisé par ce dossier |
| UC-C-01B | `A_SPECIFIER` | [Complément C-TRANS](use_cases/UC-C-01B/specification.md); A0 actualisée à contextualiser; S/E/C locaux absents | R06 | AUCUNE | AUCUNE | NON; L5/L6 non autorisé par ce dossier |
| UC-C-02 | `EN_REVUE` **pour RENOMMER_CITATION seulement** | [CIT-UML-R1; quatre vues](use_cases/UC-C-02/RENOMMER_CITATION/specification.md); UC02 complet reste à modéliser | CIT-D1/D2 : action distincte, frontière intitulé/contexte et extension éventuelle de fichiers | [T/F/A de revue, arbitrages ouverts](use_cases/UC-C-02/RENOMMER_CITATION/validation.md) | AUCUNE | NON; aucune extension C0-A automatique, lot naturel L1-B |
| UC-C-03 | `A_MODELISER` | [Complément C-TRANS](use_cases/UC-C-03/specification.md); A0 actualisée à contextualiser; S/E/C locaux absents | — | AUCUNE | AUCUNE | NON; L2 non autorisé par ce dossier |
| UC-C-04 | `A_SPECIFIER` | [Complément C-TRANS](use_cases/UC-C-04/specification.md); A0 actualisée à contextualiser; S/E/C locaux absents | R05 | AUCUNE | AUCUNE | NON; L2/L3-A non autorisé par ce dossier |
| UC-C-05E | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; L1-A non autorisé par ce dossier |
| UC-C-05P | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; L2 non autorisé par ce dossier |
| UC-C-06 | `A_MODELISER` | [Complément C-TRANS](use_cases/UC-C-06/specification.md); A0 actualisée à contextualiser; S/E/C locaux absents | — | AUCUNE | AUCUNE | NON; L1-B; contrôles de gel L5 non autorisé par ce dossier |
| UC-C-07 | `A_MODELISER` | [Complément C-TRANS](use_cases/UC-C-07/specification.md); A0 actualisée à contextualiser; S/E/C locaux absents | — | AUCUNE | AUCUNE | NON; L2; intégration L6 non autorisé par ce dossier |
| UC-C-08 | `A_SPECIFIER` | [Complément C-COT](use_cases/UC-C-08/specification.md); A0 actualisée, S/E/C locaux absents | Cote du document/sous-cote décidée; R04 technique; D07/CF4 selon source | AUCUNE | AUCUNE | NON; L3-B/L4 non autorisé par ce dossier |
| UC-C-09 | `A_SPECIFIER` | [Complément C-COT](use_cases/UC-C-09/specification.md); A0 actualisée, S/E/C locaux absents | R02/R03; R04 notation/ordre seulement; sans citation déjà déterminé | AUCUNE | AUCUNE | NON; L3-A non autorisé par ce dossier |
| UC-C-10 | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; L3/L4 non autorisé par ce dossier |
| UC-C-11 | `A_SPECIFIER` | [Complément C-TRANS](use_cases/UC-C-11/specification.md); A0 actualisée à contextualiser; S/E/C locaux absents | R08 | AUCUNE | AUCUNE | NON; L5 non autorisé par ce dossier |
| UC-C-12 | `EN_REVUE` **pour DIAGNOSTIQUER_EXAMEN seulement** | [CIT-UML-R1; quatre vues + états](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/specification.md); UC12 complet reste à modéliser | CIT-D3/D4 : diagnostic et nouvel examen avec journal/type admissible, sans reconfirmation fictive | [T/F/A de revue, préalables futurs](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/validation.md) | AUCUNE | NON; journal L1-A/C0-B et adaptateur selon type, aucune écriture C0-A autorisée |
| UC-C-13 | `APPROUVE_UTILISATEUR` **pour C0A_ISOLER seulement** | [C0A-UML-R2-ST; quatre vues du sous-cas](use_cases/UC-C-13/specification.md); [empreintes](use_cases/UC-C-13/manifest_sha256.json) | Copie neuve sur texte différent approuvée pour ce profil; patch non conforme à ce profil (C0A-ST-01). Propriété durable / fermeture globale des rattachements L1-A exclues de cette attestation | [Nouvelle attestation B T/F/A](use_cases/UC-C-13/validation.md); R1 conservée, non transférée | [20 octobre 2026, décision expresse](use_cases/UC-C-13/approbation.json); PR #30, cd584c3, manifeste original conservé | NON; mandat de reprise proposé, à approuver; lot non atterri; aucun autre sous-cas UC13 approuvé |
| UC-C-14 | `APPROUVE_UTILISATEUR` **R3-CONC; C14-D1/D2 conservés** | [R3-CONC, sept vues](use_cases/UC-C-14/revisions/R3-CONC/README.md) au commit b0adf11; [R2-HIST conservée](use_cases/UC-C-14/specification.md) | Défaut tardif B01 à corriger et démontrer; orphelin tardif séparé | [Revue B T/F/A R3](use_cases/UC-C-14/revisions/R3-CONC/validation.md), sans verdict applicatif | [23 octobre 2026, attestation et portée](lots/C0-A/verification_R3_CONC/APPROBATION_UTILISATEUR.md), b0adf1136c55c38a830d3a1cd1a4332741bf297d; approbation R2 du 20 octobre conservée | Correction isolée dans cinq fichiers seulement; vérification applicative en attente; intégration C0-A bloquée |
| UC-C-15 | `APPROUVE_UTILISATEUR` **C15-D1** | [C0A-UML-R2-DIAG; quatre vues](use_cases/UC-C-15/specification.md) | Appuis valides + diagnostics; erreur globale distincte et strict bloqué si incomplet. C0A-REV-01 ouverte dans le patch | [Attestation B T/F/A](use_cases/UC-C-15/validation.md) | [20 octobre 2026, décision expresse](use_cases/UC-C-15/approbation.json); PR #31, 30724df, manifeste original préservé | NON; mandat de reprise à approuver, correction/tests à réaliser |
| UC-C-16 | `A_SPECIFIER` | [Complément C-COT](use_cases/UC-C-16/specification.md); A/S/E/C locaux absents | Cote du document/sous-cote décidée; R01/R02 compositions, R03/R05; R04 technique | AUCUNE | AUCUNE | NON; L3-A; composants L4 non autorisé par ce dossier |
| UC-C-17 | `A_SPECIFIER` | [Complément C-COT](use_cases/UC-C-17/specification.md); A/S/E/C locaux absents | Concordance documents/citations par identités décidée; R01/R02 pour compositions | AUCUNE | AUCUNE | NON; L6; contrats L3-A non autorisé par ce dossier |
| UC-C-18A | `A_MODELISER` | À constituer; A/S/E/C absents | — | AUCUNE | AUCUNE | NON; L3/L4 non autorisé par ce dossier |
| UC-C-18B | `A_SPECIFIER` | À constituer; A/S/E/C absents | R07 pour promesse de régénération | AUCUNE | AUCUNE | NON; L5/L6 non autorisé par ce dossier |
| UC-C-19 | `A_MODELISER` | À constituer; A/S/E/C absents | — | AUCUNE | AUCUNE | NON; L6 non autorisé par ce dossier |

## Décisions de principe déjà acquises, sans approbation implicite des dossiers

- D05 CHRONO_VERSION : décidée explicitement dans le [mandat source §2](references/MANDAT_CONSOLIDATION_UML_2026-10-20.md).
- Quadruplet UML + validation B + approbation utilisateur : exigés par les §§4–8 du même mandat.
- Contrats C et autorisation C0-A antérieurs : conservés avec leurs conditions. Le patch C0-A a été testé isolément; il n’est pas atterri. Cette ligne ne le requalifie pas en développement nouvellement autorisé.

## Journal de changements du registre

| Date | Action | Référence | Effet |
|---|---|---|---|
| 2026-10-20 | Initialisation de 22 dossiers, sans attestation de vues cibles | Mandat et plan C-UML-2026-10-20-R1 | Statuts A_SPECIFIER ou A_MODELISER uniquement; tests applicatifs NON EXECUTES dans cette intervention |
| 2026-10-20 | Revue de couverture et préparation C0-A | [Mandat conservé](references/MANDAT_REVUE_COUVERTURE_C0A_2026-10-20.md), [rapport](RAPPORT_REVUE_COUVERTURE_ET_C0A.md) | 13 → VALIDE_ARCHITECTURE documentaire; 14/15 → EN_REVUE; approbation utilisateur AUCUNE; pas d’implantation |
| 2026-10-20 | Révision de la réutilisation des Statement | [Mandat ST](references/MANDAT_INVARIANTS_STATEMENT_2026-10-20.md), [analyse](INVARIANTS_STATEMENT_REPRODUCED_PRODUCED.md), [validation 13 R2-ST](use_cases/UC-C-13/validation.md) | Ancienne attestation 13 R1 historique; nouvelle attestation limitée à C0A_ISOLER. Six critères inchangés, AC02/03 corrigés. 14/15 restent EN_REVUE, C0A-REV-01 ouverte; aucun code modifié |

Lors d’une transition, ajouter la référence exacte de version/empreintes, date, décision et réserves, avec le chemin du dossier. Une suspension utilisateur reste une décision explicite consignée; ne jamais en déduire un statut prêt.


Les compléments COV-B/C/E affectent la spécification future de 03/04/05P/08
et les parcours intégrés; ils sont proposés dans la matrice et ne leur
accordent aucun statut validé. L’ancien registre exact est conservé dans
l’historique avant revue R2.


| Date | Action de suivi | Référence | Effet limité |
|---|---|---|---|
| 2026-10-20 | Approbation expresse de UC13 R2-ST | [Mandat](references/MANDAT_APPROBATION_UC13_VALIDATION_C0A_2026-10-20.md), [décision](use_cases/UC-C-13/approbation.json) | UC13::C0A_ISOLER → APPROUVE_UTILISATEUR au commit cd584c3; jamais PRET_DEVELOPPEMENT par automatisme. 14/15 non approuvés. |


| Date | Revue graphique préparée | Référence | Effet |
|---|---|---|---|
| 2026-10-20 | UC14/15 révisés; citations attribuées à UC02/12 | [Livraison graphique](REVUE_GRAPHIQUE_C0A_UC14_UC15.md), [analyse](ANALYSE_CIBLEE_CITATIONS_C0A.md) | UC14/15 → VALIDE_ARCHITECTURE pour les seules options proposées; UC02/12 sous-cas → EN_REVUE. UC13 approuvé inchangé; aucune approbation nouvelle, code ou fusion. |

## Approbations UC14/15 et préparation du mandat C0-A

Le [mandat utilisateur du 20 octobre 2026](references/MANDAT_APPROBATION_UC14_UC15_PREPARATION_C0A_2026-10-20.md) approuve exclusivement
UC14 C0A-UML-R2-HIST et UC15 C0A-UML-R2-DIAG au commit `30724df7ec5cbd1aba8ef25d59b5c3a162d20dab`,
PR #31. [Décision UC14](use_cases/UC-C-14/approbation.json) et
[décision UC15](use_cases/UC-C-15/approbation.json) fixent les périmètres et
les empreintes originales. Les mentions « à approuver » du journal ci-dessus
sont historiques. Les copies approuvées sont conservées sans modification.

UC13 reste approuvé dans sa version antérieure; UC02/12 citations restent
EN_REVUE. Aucun transfert d’approbation à L1-A ou au global G-R3 entier.
La finalisation et la fusion **documentaires** de la PR #31 sont autorisées;
l’implantation et l’atterrissage applicatif de C0-A ne le sont pas.
Le [mandat technique unique](lots/C0-A/MANDAT.md) est soumis à approbation.
C0A-ST-01, C0A-14-01 et C0A-REV-01 restent à corriger et à tester.
Aucun arbitrage citations ni mécanisme L1-A ne bloque ce périmètre isolé.

## Complément PO de cotation — 21 octobre 2026

Principe cote principale du document / sous-cotes des citations **décidé** par
le [Product Owner](references/DECISION_PO_COTATION_DOCUMENT_CITATIONS_2026-10-21.md).
Spécifications UC08/09/16/17 et [ERD transversal](MODELE_TRANSVERSAL_COTATION.md)
complétés. Les quatre dossiers restent A_SPECIFIER, sans approbation implicite
de leurs futures vues ni statut prêt. R04 est limité aux modalités techniques;
le document retenu sans citation est déjà couvert. Aucun développement autorisé.

## Cohérence transversale — C-TRANS-R1

21 octobre 2026 : [mandat](references/MANDAT_COHERENCE_TRANSVERSALE_2026-10-21.md),
[modèles et revue](MODELE_TRANSVERSAL_C.md), couverture §13, backlog §15.
Les statuts des **22 dossiers restent inchangés**. Compléments de specs
01A/01B/03/04/06/07/11/12/19 ajoutés, 08/09/16/17 enrichis; sept activités A0
actualisées. Les quatre vues locales et leur revue restent à produire pour
ces périmètres complets. Les compléments parent12/19 ne constituent pas un
nouveau sous-cas validé; UC12::DIAGNOSTIQUER_EXAMEN reste EN_REVUE.

Trois vues communes C-TRANS-R1 sont proposées, compilées et contrôlées;
aucune validation B complète, approbation utilisateur ou autorisation de lot
n’est inscrite. UC13/14/15 et leurs dépendances graphiques/manifeste restent
exactement inchangés. Les modèles communs ne leur transfèrent aucune garantie
L1-A/C0-B/L5. Le suivi d’implantation et la correction B01 de C0-A restent
hors de cette revue documentaire.

## UC14 R3-CONC — conception préalable à la correction de concurrence (historique avant approbation)

23 octobre 2026 : [mandat complémentaire](use_cases/UC-C-14/revisions/R3-CONC/mandat_source.md),
[dossier de sept vues](use_cases/UC-C-14/revisions/R3-CONC/README.md),
[attestation indépendante B T/F/A](use_cases/UC-C-14/revisions/R3-CONC/validation.md).
Version UC14-R3-CONC-2026-10-23; manifeste de conception SHA-256
`258ca9a719c0b172461f75dc5f27bb98b74335b532340c00654b5165f7e87b0d`.

**VALIDE_ARCHITECTURE pour la conception seulement. Approbation utilisateur :
AUCUNE; implantation non autorisée par cette attestation.** L'impact technique
sur ajax_edit_node / UC13 est représenté dans les vues partagées et l'activité
T2, sans modification des AC UC13 ni UC14. Les anciennes sources/rendus,
manifestes et approbations R2 restent intacts. Les lignes UC13/14/15 du
tableau ci-dessus décrivent ces approbations historiques précises.

Le plan T01–T24 est NON EXECUTE. Le candidat `f35ec85` reste NON CONFORME;
les deux contre-épreuves tardives B01 ne sont pas résolues par une conception.
La correction isolée proposée porte sur cinq fichiers déjà dans le périmètre
C0-A, sous [conditions explicites](use_cases/UC-C-14/revisions/R3-CONC/analyse_coherence.md#6-périmètre-exact-de-la-future-autorisation-proposée).
Elle attend la décision utilisateur exigée par le mandat courant.
L'orphelin tardif demeure une réserve séparée; aucun lot suivant n'est ouvert.

## Approbation UC14 R3-CONC — 23 octobre 2026

Décision utilisateur : **APPROUVE_UTILISATEUR**, identifiant **UC14 R3-CONC**,
branche `docs/uc14-r3-conc-20261023`, commit documentaire approuvé
[`b0adf1136c55c38a830d3a1cd1a4332741bf297d`](https://github.com/LPDavidbdeb/court/commit/b0adf1136c55c38a830d3a1cd1a4332741bf297d).
[Mandat source](references/MANDAT_APPROBATION_UC14_R3_CONC_2026-10-23.md),
[attestation de décision et limites](lots/C0-A/verification_R3_CONC/APPROBATION_UTILISATEUR.md).
Le verdict B préalable reste VALIDE_ARCHITECTURE; aucune de ses mentions
historiques n'est réécrite dans le dossier approuvé.

L'autorisation corrective porte exclusivement sur les opérations du §6 de
l'analyse R3-CONC dans les cinq fichiers suivants :

- `document_manager/concordance.py` : plan/revalidation et orchestration du retrait protégé et atomique;
- `document_manager/protection.py` : protections/gardes locales, état attendu et archive fidèle;
- `document_manager/models.py` : sauvegarde des LibraryNode existantes protégée, sans INSERT de remplacement, sans changement de champ ou Meta;
- `document_manager/views/produced_views.py` : barrière UC13 avant mutation, refus et transactions HTTP;
- `document_manager/test_e01_numerotation.py` : contre-épreuves tardives, plusieurs occurrences, non-résurrection et atomicité.

Reconstitution isolée prévue au socle `515666e`, avec reprise et delta B01
de `f35ec85` puis futur delta R3 identifié. Ressources indépendantes de A,
données synthétiques et base jetable suivant les autorisations applicables.
Aucune extension implicite aux autres fichiers de l'ancien périmètre C0-A.
Un besoin hors de cette portée doit être signalé avant exécution.

**Vérification applicative en attente.** Aucun candidat R3 corrigé n'est
identifié dans les livraisons consultées; aucun résultat R3 n'est acquis;
T01–T24 restent NON EXECUTES. Le présent mandat prépare uniquement la
[grille de revue indépendante](lots/C0-A/verification_R3_CONC/GRILLE_REVUE_CONFORMITE.md)
et l'[intégrité des références](lots/C0-A/verification_R3_CONC/INTEGRITE_CONCEPTIONS_APPROUVEES.json).
Il ne commence pas la correction et ne demande pas une nouvelle approbation
pour la portée isolée déjà autorisée.

**Intégration C0-A toujours bloquée.** La revue B01 NON CONFORME et ses deux
contre-épreuves tardives demeurent opposables. Les anciens succès 270/33 ne
valent pas résultats R3. Ni intégration, fusion, migration, déploiement,
ressource réelle ni publication applicative autorisés. La voie d'ajout UC02,
l'orphelin tardif (ni corrigé ni testé ici) et les lots L1-A/C0-B/L5 restent
hors périmètre. Les versions UML R2 et R3 approuvées, leurs manifestes et
historiques sont intacts. Seul le présent registre évolue pour consigner la
décision; les empreintes du registre publiées avec R3 désignent son état
historique au commit approuvé.

| Date | Décision | Version exacte | Effet |
|---|---|---|---|
| 2026-10-23 | Approbation utilisateur expresse | UC14 R3-CONC, b0adf1136c55c38a830d3a1cd1a4332741bf297d | APPROUVE_UTILISATEUR; correction isolée de cinq fichiers autorisée; aucune correction exécutée dans ce mandat; vérification applicative en attente et intégration C0-A bloquée |
