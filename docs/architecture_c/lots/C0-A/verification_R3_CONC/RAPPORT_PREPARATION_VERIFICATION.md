# UC14 R3-CONC — Approbation enregistrée et revue future préparée

**23 octobre 2026 — vérification applicative en attente.**
L'approbation explicite de la conception au commit
`b0adf1136c55c38a830d3a1cd1a4332741bf297d` est enregistrée au statut
**APPROUVE_UTILISATEUR**. La correction isolée est délimitée; aucune
implantation n'est réalisée par ce mandat documentaire.

## Livrables

| Livrable demandé | Pièce produite |
|---|---|
| Registre officiel actualisé | [registre_validation.md](../../../registre_validation.md), ligne UC-C-14 et section d'approbation R3 |
| Attestation de l'approbation et de sa portée | [APPROBATION_UTILISATEUR.md](APPROBATION_UTILISATEUR.md), liée au [mandat source](../../../references/MANDAT_APPROBATION_UC14_R3_CONC_2026-10-23.md) |
| Grille des futures implantations | [GRILLE_REVUE_CONFORMITE.md](GRILLE_REVUE_CONFORMITE.md) : sept vues, 17 contrôles, T01–T24, preuve ancien/nouveau et règle de verdict |
| Vérification d'intégrité | [INTEGRITE_CONCEPTIONS_APPROUVEES.json](INTEGRITE_CONCEPTIONS_APPROUVEES.json), détails des empreintes et références Git |
| Rapport bref | Présent document |

## Éléments approuvés et autorisation exacte

Conception R3-CONC approuvée après revue B VALIDE_ARCHITECTURE. Les critères
UC14 AC01–AC07/C14-D1/D2 et le contrat UC13 R2-ST sont conservés. Seuls
`concordance.py`, `protection.py`, `models.py`, `views/produced_views.py` et
`test_e01_numerotation.py`, sous `document_manager/`, sont autorisés pour la
correction isolée décrite au §6 de l'analyse approuvée. L'[attestation](APPROBATION_UTILISATEUR.md)
détaille chaque opération et ses limites. Cette portée n'exige pas d'être
réapprouvée du seul fait de son enregistrement.

## Contrôles documentaires effectivement réalisés

- **165 fichiers de conception** comparés octet par octet, via SHA-256, aux
  blobs Git du commit documentaire approuvé : aucun écart. Ce périmètre inclut
  les 32 fichiers R3, les versions locales R2 et les archives approuvées.
- Manifeste R3 de conception : **27 entrées + style** vérifiées; manifeste
  de livraison : **31 entrées** vérifiées. Sept sources PlantUML, sept SVG
  et sept PNG intacts, sans régénération ni réécriture de contenu.
- Manifestes originaux R2 vérifiés aux commits `cd584c3` et `30724df`, puis
  **24/26/26 entrées archivées** UC13/14/15 contrôlées. Manifestes actifs :
  **26/29/29 entrées**, sans écart; anciennes décisions et historiques intacts.
- Les sept critères AC UC14 sont identiques dans R2 et R3. Les 12 sources
  contractuelles de la grille, dont B01, correspondent au commit publié.
- **671 fichiers suivis hors docs/legal** inchangés depuis le relevé initial
  de cette intervention. HEAD et branche de travail inchangés; aucun commit,
  push, merge, lancement du banc ou accès à une base.

Le registre évolue volontairement pour consigner l'approbation. Son empreinte
dans le manifeste R3 publié désigne **son état historique au commit b0adf11**,
vérifié dans Git, et non son futur état courant. Cette évolution n'altère
aucun fichier du dossier approuvé; aucune nouvelle révision UML n'est requise.

## Éléments non exécutés et blocages maintenus

Aucun candidat R3 corrigé n'est identifié dans les livraisons consultées
(`lots/C0-A/`, rapports A et préparation d'intégration du 21 octobre).
Cette préparation concerne le candidat B01 antérieur, pas R3-CONC. Aucune
recherche intrusive dans les bancs de A ni aucun examen d'un nouveau code.

**Aucun test applicatif R3 exécuté, aucune garantie opérationnelle R3
démontrée.** T01–T24 restent NON EXECUTES. Les anciens résultats 270/33 et
les deux échecs tardifs de B01 gardent leur portée historique. La grille
exige code et résultats réels, échecs discriminants sur le témoin f35
reconstitué et succès sur le correctif, sans succès fondé sur des timeouts.
Elle impose une comparaison des archives et des états réellement supprimés.

**C0-A demeure bloqué à l'intégration.** Ni intégration, fusion, migration,
déploiement, ressource réelle ou publication applicative autorisés. Aucun
lot suivant, refonte générale ou accès à la base réelle. L'orphelin tardif
reste une réserve distincte : **ni corrigé ni testé ici**; UC02 est exclu.
La prochaine revue attend un candidat R3 identifié et ses résultats réels;
le présent rapport ne prononce aucune conformité applicative.
