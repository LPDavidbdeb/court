# Attestation de l'approbation utilisateur — UC14 R3-CONC

**Date : 23 octobre 2026 — statut : APPROUVE_UTILISATEUR.**
Cette attestation enregistre la décision explicite de l'utilisateur dans le
[mandat source](../../../references/MANDAT_APPROBATION_UC14_R3_CONC_2026-10-23.md).
Elle constitue une preuve pour le [registre officiel](../../../registre_validation.md),
qui reste l'autorité des statuts courants. Elle n'est pas une attestation de
conformité du code.

## Version exacte approuvée

| Élément | Référence |
|---|---|
| Identifiant | UC14 R3-CONC / UC14-R3-CONC-2026-10-23 |
| Branche documentaire | `docs/uc14-r3-conc-20261023` |
| Commit approuvé | [`b0adf1136c55c38a830d3a1cd1a4332741bf297d`](https://github.com/LPDavidbdeb/court/commit/b0adf1136c55c38a830d3a1cd1a4332741bf297d) |
| Dossier approuvé | [R3-CONC au commit exact](https://github.com/LPDavidbdeb/court/tree/b0adf1136c55c38a830d3a1cd1a4332741bf297d/docs/architecture_c/use_cases/UC-C-14/revisions/R3-CONC) |
| Revue préalable | [validation.md](../../../use_cases/UC-C-14/revisions/R3-CONC/validation.md), [revue_B.md](../../../use_cases/UC-C-14/revisions/R3-CONC/revue_B.md) : VALIDE_ARCHITECTURE |
| SHA-256 du manifeste de conception | `258ca9a719c0b172461f75dc5f27bb98b74335b532340c00654b5165f7e87b0d` |
| SHA-256 du manifeste de livraison | `b1ecaf1ebb55cc84b989153c1b6536836cdfbf3184c7d0e59cb2498fc27818ba` |

## Autorisation limitée et fichiers concernés

L'approbation autorise une **correction applicative isolée conforme à R3-CONC**,
dans les cinq fichiers ci-dessous, conformément au §6 de l'[analyse approuvée](../../../use_cases/UC-C-14/revisions/R3-CONC/analyse_coherence.md).

| Fichier autorisé pour cette correction | Portée exacte |
|---|---|
| `document_manager/concordance.py` | Plan/revalidation, protections et orchestration du retrait; frontière atomique avant interception HTTP. |
| `document_manager/protection.py` | Helpers et gardes locaux; état attendu, archive fidèle et contrôles finaux existants. |
| `document_manager/models.py` | Méthode de sauvegarde des LibraryNode existantes : existence protégée et UPDATE seul; aucun champ ni Meta modifié. |
| `document_manager/views/produced_views.py` | Barrière UC13 avant écriture, refus d'une cible disparue, transactions HTTP conservées. |
| `document_manager/test_e01_numerotation.py` | Contre-épreuves tardives, plusieurs occurrences, absence de résurrection et atomicité. |

La correction vise la continuité état contrôlé–archive–DELETE–commit et les
deux issues sûres T1/T2. Les critères UC14 AC01–AC07, C14-D1/D2 et UC13 R2-ST
restent opposables. Aucun élargissement aux autres fichiers historiques de
C0-A n'est déduit de l'ancienne liste de huit fichiers.

Reconstitution prévue : socle `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`,
patch de reprise puis delta B01 livrés à `f35ec8586866f4359d44f52a0bc5cc57c0804217`,
puis futur delta R3. Conserver les copies et ressources indépendantes de A,
les données synthétiques et la configuration de banc sans accès à la base
réelle. La référence P6 et les contrôles/pilotes de A ne sont pas déplacés.
Un besoin hors de ces cinq fichiers ou une divergence de contrat doit être
signalé avant sa réalisation, sans extension silencieuse.

**Le présent mandat est exécuté uniquement sous son volet documentaire.**
Il ne demande pas de commencer l'implantation ni de lancer des essais
applicatifs dans cette intervention. L'autorisation corrective est enregistrée
pour l'étape isolée; aucune nouvelle confirmation de cette même portée ne
sera nécessaire du seul fait du présent enregistrement.

## Interdictions et réserves persistantes

L'approbation n'autorise ni intégration, ni fusion, ni migration, ni déploiement,
ni intervention réelle. Aucun changement de schéma, de politique de cotation,
de pilote, de contrôle A, de serveur ou de sauvegarde; aucune purge, refonte
générale d'arbre ou livraison L1-A/C0-B/L5. Les commits/push applicatifs ne
sont pas inclus dans la portée du §6 approuvé. Le présent travail ne réalise
aucune opération Git de publication supplémentaire.

L'orphelin tardif reste distinct : **ni corrigé ni testé dans ce mandat**.
La voie d'ajout UC02 reste exclue. Une base de test future doit être jetable
et indépendante; le présent mandat n'autorise aucune exécution de migration.

## État probatoire au moment de l'approbation

| Nature | État enregistré |
|---|---|
| Conception | APPROUVE_UTILISATEUR au commit nommé |
| Futur candidat R3 soumis à la revue | Aucun candidat identifié dans les livraisons consultées |
| Vérification applicative R3-CONC | **En attente**; aucune garantie opérationnelle R3 démontrée |
| Tests T01–T24 R3 | NON EXECUTES |
| Candidat B01 antérieur `f35ec85` | NON CONFORME selon la revue indépendante B01; deux défauts tardifs restent bloquants |
| Intégration de C0-A | **Blocage maintenu**; pas d'autorisation d'intégrer |

Les anciens succès 270/33 portent sur le candidat B01, avec deux échecs
tardifs documentés; ils ne sont pas des résultats R3. La nouvelle
[grille de revue](GRILLE_REVUE_CONFORMITE.md) prépare l'examen indépendant
d'un futur candidat et de ses résultats réels.

Les sources, rendus, manifestes, spécifications et attestations R3 publiés
restent figés. Leurs anciennes mentions « approbation AUCUNE » décrivent
l'état avant la présente décision. Aucun de ces fichiers n'est réécrit pour
changer son statut; le registre courant et cette attestation portent la
nouvelle décision. Aucune révision de conception supplémentaire n'est créée.
