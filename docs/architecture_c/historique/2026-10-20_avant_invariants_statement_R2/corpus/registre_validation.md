# Registre courant de validation des use cases C

**Actualisation de revue du 20 octobre 2026 — C0A-UML-R1; contrats C-UML-2026-10-20-R1.**

Autorité des transitions : [protocole](PROTOCOLE_VALIDATION_UML.md). Inventaire et dépendances : [plan](PLAN_MODELISATION_UML.md). Ce registre ne confond pas approbation architecturale de principe et approbation d’un dossier UML.

**Constat R2 : dossiers 13/14/15 à quatre vues produits; 13 validé B documentaire, 14/15 en revue. Aucune validation globale de C, approbation utilisateur ou autorisation de développement n’est enregistrée.**

| Use case | Statut | Version du dossier / vues | Réserves propres | Validation B | Approbation utilisateur | Prêt / mandat de lot |
|---|---|---|---|---|---|---|
| UC-C-01A | `A_SPECIFIER` | À constituer; A0 à revoir; S/E/C absents | R06 | AUCUNE | AUCUNE | NON; L1-A non autorisé par ce dossier |
| UC-C-01B | `A_SPECIFIER` | À constituer; A0 à revoir; S/E/C absents | R06 | AUCUNE | AUCUNE | NON; L5/L6 non autorisé par ce dossier |
| UC-C-02 | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; L1-B non autorisé par ce dossier |
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
| UC-C-12 | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; C0-B/L6 non autorisé par ce dossier |
| UC-C-13 | `VALIDE_ARCHITECTURE` | [C0A-UML-R1; A/S/E/C présentes](use_cases/UC-C-13/specification.md); [empreintes](use_cases/UC-C-13/manifest_sha256.json) | Limites C0-A explicites; aucun arbitrage bloquant pour ce seul dossier | [Attestation B du 20 octobre](use_cases/UC-C-13/validation.md), T/F/A documentaire | AUCUNE; à soumettre | NON; mandat de validation/correction sur 515666e absent; lot non atterri |
| UC-C-14 | `EN_REVUE` | [C0A-UML-R1; A/S/E/C présentes](use_cases/UC-C-14/specification.md) | Clôturer la revue détaillée des suppressions et cascades | [T effectué; F/A à clôturer](use_cases/UC-C-14/validation.md) | AUCUNE | NON; C0-A non atterri |
| UC-C-15 | `EN_REVUE` | [C0A-UML-R1; A/S/E/C présentes](use_cases/UC-C-15/specification.md) | C0A-REV-01; contrat de résultats partiels proposé; patch AC03/06 non conforme | [T effectué; F/A à clôturer](use_cases/UC-C-15/validation.md) | AUCUNE | NON; correction et tests sur 515666e à mandater |
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

Lors d’une transition, ajouter la référence exacte de version/empreintes, date, décision et réserves, avec le chemin du dossier. Une suspension utilisateur reste une décision explicite consignée; ne jamais en déduire un statut prêt.


Les compléments COV-B/C/E affectent la spécification future de 03/04/05P/08
et les parcours intégrés; ils sont proposés dans la matrice et ne leur
accordent aucun statut validé. L’ancien registre exact est conservé dans
l’historique avant revue R2.
