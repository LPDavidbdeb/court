# Registre courant de validation des use cases C

**Actualisation du 20 octobre 2026 — UC13 C0A-UML-R2-ST; UC14 R2-HIST, UC15 R2-DIAG; sous-cas citations CIT-UML-R1; global proposé R3-CIT.**

Autorité des transitions : [protocole](PROTOCOLE_VALIDATION_UML.md). Inventaire et dépendances : [plan](PLAN_MODELISATION_UML.md). Ce registre ne confond pas approbation architecturale de principe et approbation d’un dossier UML.

**État courant : UC13::C0A_ISOLER R2-ST APPROUVE_UTILISATEUR au manifeste de cd584c3. UC14 R2-HIST et UC15 R2-DIAG sont validés B pour les contrats proposés et soumis à une revue graphique; aucune approbation utilisateur de ces dossiers. Les sous-cas citations UC02/12 restent EN_REVUE. Aucun statut PRET_DEVELOPPEMENT ni mandat de code.**

| Use case | Statut | Version du dossier / vues | Réserves propres | Validation B | Approbation utilisateur | Prêt / mandat de lot |
|---|---|---|---|---|---|---|
| UC-C-01A | `A_SPECIFIER` | À constituer; A0 à revoir; S/E/C absents | R06 | AUCUNE | AUCUNE | NON; L1-A non autorisé par ce dossier |
| UC-C-01B | `A_SPECIFIER` | À constituer; A0 à revoir; S/E/C absents | R06 | AUCUNE | AUCUNE | NON; L5/L6 non autorisé par ce dossier |
| UC-C-02 | `EN_REVUE` **pour RENOMMER_CITATION seulement** | [CIT-UML-R1; quatre vues](use_cases/UC-C-02/RENOMMER_CITATION/specification.md); UC02 complet reste à modéliser | CIT-D1/D2 : action distincte, frontière intitulé/contexte et extension éventuelle de fichiers | [T/F/A de revue, arbitrages ouverts](use_cases/UC-C-02/RENOMMER_CITATION/validation.md) | AUCUNE | NON; aucune extension C0-A automatique, lot naturel L1-B |
| UC-C-03 | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; L2 non autorisé par ce dossier |
| UC-C-04 | `A_SPECIFIER` | À constituer; A0 à revoir; S/E/C absents | R05 | AUCUNE | AUCUNE | NON; L2/L3-A non autorisé par ce dossier |
| UC-C-05E | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; L1-A non autorisé par ce dossier |
| UC-C-05P | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; L2 non autorisé par ce dossier |
| UC-C-06 | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; L1-B; contrôles de gel L5 non autorisé par ce dossier |
| UC-C-07 | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; L2; intégration L6 non autorisé par ce dossier |
| UC-C-08 | `A_SPECIFIER` | À constituer; A0 à revoir; S/E/C absents | R04; D07/CF4 selon source | AUCUNE | AUCUNE | NON; L3-B/L4 non autorisé par ce dossier |
| UC-C-09 | `A_SPECIFIER` | À constituer; A0 à revoir; S/E/C absents | R02/R03/R04 | AUCUNE | AUCUNE | NON; L3-A non autorisé par ce dossier |
| UC-C-10 | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; L3/L4 non autorisé par ce dossier |
| UC-C-11 | `A_SPECIFIER` | À constituer; A0 à revoir; S/E/C absents | R08 | AUCUNE | AUCUNE | NON; L5 non autorisé par ce dossier |
| UC-C-12 | `EN_REVUE` **pour DIAGNOSTIQUER_EXAMEN seulement** | [CIT-UML-R1; quatre vues + états](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/specification.md); UC12 complet reste à modéliser | CIT-D3/D4 : diagnostic et nouvel examen avec journal/type admissible, sans reconfirmation fictive | [T/F/A de revue, préalables futurs](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/validation.md) | AUCUNE | NON; journal L1-A/C0-B et adaptateur selon type, aucune écriture C0-A autorisée |
| UC-C-13 | `APPROUVE_UTILISATEUR` **pour C0A_ISOLER seulement** | [C0A-UML-R2-ST; quatre vues du sous-cas](use_cases/UC-C-13/specification.md); [empreintes](use_cases/UC-C-13/manifest_sha256.json) | Copie neuve sur texte différent approuvée pour ce profil; patch non conforme à ce profil (C0A-ST-01). Propriété durable / fermeture globale des rattachements L1-A exclues de cette attestation | [Nouvelle attestation B T/F/A](use_cases/UC-C-13/validation.md); R1 conservée, non transférée | [20 octobre 2026, décision expresse](use_cases/UC-C-13/approbation.json); PR #30, cd584c3, manifeste original conservé | NON; dépendances/mandat de correction absents; lot non atterri; aucun autre sous-cas approuvé |
| UC-C-14 | `VALIDE_ARCHITECTURE` **option conservatrice C14-D1/D2** | [C0A-UML-R2-HIST; quatre vues](use_cases/UC-C-14/specification.md) | À approuver : conserver tous les contenus, refuser les archives insuffisantes; C0A-14-01 reste un écart du patch | [Attestation B T/F/A](use_cases/UC-C-14/validation.md) | AUCUNE; examen graphique demandé | NON; dépendances/mandat/tests du lot non satisfaits |
| UC-C-15 | `VALIDE_ARCHITECTURE` **contrat proposé C15-D1** | [C0A-UML-R2-DIAG; quatre vues](use_cases/UC-C-15/specification.md) | Appuis valides + diagnostics; erreur globale distincte et strict bloqué si incomplet. C0A-REV-01 ouverte dans le patch | [Attestation B T/F/A](use_cases/UC-C-15/validation.md) | AUCUNE; examen graphique demandé | NON; correction et tests isolés à mandater |
| UC-C-16 | `A_SPECIFIER` | À constituer; A/S/E/C absents | R01/R02/R03/R04/R05 | AUCUNE | AUCUNE | NON; L3-A; composants L4 non autorisé par ce dossier |
| UC-C-17 | `A_SPECIFIER` | À constituer; A/S/E/C absents | R01/R02 | AUCUNE | AUCUNE | NON; L6; contrats L3-A non autorisé par ce dossier |
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
