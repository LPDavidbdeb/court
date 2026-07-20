# Intégration finale des cotes — 12 juillet 2026

## Portée

- Demande intégrée : `legal/requete_secton_faits_lp.md`
- Copie de sauvegarde antérieure à l’intégration finale : `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md`
- Bordereau complété : `legal/bordereau_pieces.md`
- Classeur synchronisé : `legal/organisation_preuve/registre_procedural/registre_procedural_integre.xlsx`

## Résultat vérifié

- 87 cotes proposées et 87 cotes résolues;
- 239 composantes rattachées;
- 23 liasses;
- 134 sous-cotes ordonnées;
- 0 composante Django manquante;
- 0 conflit où un même tuple `(modèle, PK)` serait attribué à plusieurs cotes;
- 0 cote partielle ou non résolue;
- 0 marqueur `P-[…]` restant dans la demande;
- 182 mentions de pièces dans la demande, toutes rattachées à une cote existante;
- aucune sous-cote citée hors de la plage définie au bordereau.

## Décisions de structure

- Les liasses regroupent un seul type de modèle à la fois.
- L’ordre des identifiants inscrit au bordereau détermine l’ordre des sous-cotes `.1`, `.2`, etc.
- Le tableau historique des événements demeure un outil de repérage; les paragraphes de la demande renvoient aux événements sources cotés.
- Les relevés d’assurance P-84 et P-85 remplacent la référence à une documentation de régime non disponible; le paragraphe 279 a été reformulé selon ce que ces relevés permettent effectivement de constater.
- Les séquences de clavardage P-58 à P-64 existent dans la base, mais devront être rendues en fichiers lors de l’export matériel des pièces.
- P-87 correspond uniquement au courriel non privilégié `Email:487` par lequel Johanne Bazinet transmet au demandeur, le 15 mai 2015, le fichier `Courriel du 11 juin 2013.docx`; la retransmission à l’avocat (`Email:475`) demeure en réserve et n’est pas une composante produite de P-87.
- L’identité du document joint aux deux courriels est vérifiée par sa taille (14 721 octets) et son empreinte SHA-256 (`d84bfac0bb4209be86535528c5d633d662dafb1285496abf762eefb380f2202a`). L’analyse complète et ses limites sont consignées dans `legal/organisation_preuve/chaine_transmission_p2_2013_2015.md`.

## Contrôles exécutés

- reconstruction du registre procédural;
- contrôle reproductible `build_procedural_registry --check`;
- contrôle des cotes et sous-cotes citées dans la demande;
- contrôle `git diff --check`;
- 12 tests ciblés du registre procédural et de l’audit de preuve : réussis;
- inspection du contenu et vérification visuelle des onze onglets du classeur intégré;
- balayage du classeur : aucune erreur de formule détectée.
