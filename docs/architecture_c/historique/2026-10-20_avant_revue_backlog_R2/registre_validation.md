# Registre courant de validation des use cases C

**Initialisation du 20 octobre 2026 — C-UML-2026-10-20-R1.**

Autorité des transitions : [protocole](PROTOCOLE_VALIDATION_UML.md). Inventaire et dépendances : [plan](PLAN_MODELISATION_UML.md). Ce registre ne confond pas approbation architecturale de principe et approbation d’un dossier UML.

**Constat : aucun dossier cible à quatre vues n’est encore complet. Aucune validation B globale ni approbation utilisateur de dossier n’est enregistrée.**

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
| UC-C-13 | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; C0-A non autorisé par ce dossier |
| UC-C-14 | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; C0-A non autorisé par ce dossier |
| UC-C-15 | `A_MODELISER` | À constituer; A0 à revoir; S/E/C absents | — | AUCUNE | AUCUNE | NON; C0-A non autorisé par ce dossier |
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

Lors d’une transition, ajouter la référence exacte de version/empreintes, date, décision et réserves, avec le chemin du dossier. Une suspension utilisateur reste une décision explicite consignée; ne jamais en déduire un statut prêt.
