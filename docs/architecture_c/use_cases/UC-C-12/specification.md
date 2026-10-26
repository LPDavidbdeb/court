# UC-C-12 — Produire la concordance des paragraphes historiques

**Complément C-TRANS-2026-10-21-R1 — C0-B puis L6.** US-C-12; CF3-D1/D2; mandat D.
Acteur : l’utilisateur humain unique (rédacteur, relecteur ou lecteur selon
l’opération). [Contrat transversal](../../MODELE_TRANSVERSAL_C.md).

Ce complément précise les invariants du dossier existant à spécifier/modéliser;
il ne constitue pas un quadruplet UML ni une attestation de validation.
[Statut faisant autorité](../../registre_validation.md). Les exigences
antérieures du plan et de la story restent applicables.

| Critère transversal | Résultat attendu |
|---|---|
| TRV12-AC01 | La concordance compare explicitement les paragraphes du référent déposé le 24 juillet 2026 à ceux de la demande modifiée, à partir des identités, filières N:M, textes et numéros attestés. Une absence de capture ou un lien ambigu reste diagnostiqué; aucune filiation ou décision passée fabriquée. |

**Parcours et refus :** Identifier les deux référents → lire les états conservés, cartes N:M et archives → distinguer décision historique, validité actuelle et admissibilité stricte → présenter/exporter les correspondances et lacunes. L’acte de juillet est papier, les fichiers archivés sont la source d’impression. Aucun ancien examen ni VersionActe d’époque n’est déduit de données actuelles.

**Dépendances et limites :** UC05E/13/14/15 pour lecture qualifiée et archives; pas de dépendance obligatoire à Preuve/L2 pour la concordance des paragraphes. UC17 fournit séparément la concordance documentaire; les fondements exacts instrumentés se retrouvent via UC11/17. Le sous-cas DIAGNOSTIQUER_EXAMEN reste EN_REVUE et inchangé; ce complément ne lui transfère aucune validation.

Scénarios TRV:T10/T12 : **NON EXECUTES**. Séquences, ERD et classes locaux restent à produire et à rapprocher des responsabilités du modèle transversal. Aucun développement autorisé.
