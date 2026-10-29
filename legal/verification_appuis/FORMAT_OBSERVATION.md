# va-observation/1 — fichier d'attente JSONL

Une ligne UTF-8 = un objet JSON complet, terminé par un saut de ligne. Les
identifiants et versions sont stables ; une correction ajoute une ligne.

Champs communs : `schema`, `id`, `liens` (identifiants AppuiDepotJuillet),
`avancement`, `auteur` (identité réelle, CODEX pour cet agent), `date` ISO 8601
avec fuseau, `empreinte_enonce` SHA-256, `remplace` (ID précédent ou null).

Un NON_EXAMINE ne porte aucun résultat. Les autres états portent `resultat`
(RELATION_REPEREE, AUCUNE_RELATION_REPEREE, INDETERMINE), `raison`, `supports`
(liste de chemins, SHA-256 et qualifications). La liste peut être vide pour
INDETERMINE si les supports sont manquants.

- RELATION_REPEREE exige `element_observe` et `localisation`.
- AUCUNE_RELATION_REPEREE exige `perimetre_lu`.
- INDETERMINE exige `obstacle`.
- VALIDE et REJETE exigent `auteur=LP` et `decision_reference` : la référence
  à sa décision réelle. L'agent ne prend jamais ces décisions.

Les champs `portee`, `reste_sans_piece`, `ecarts`, `membres`, `nature` et
`fragments` sont réservés aux stories suivantes. Le contrat n'attribue aucune
vérité objective au contenu rapporté. Les fragments ne créent aucun appui.

Le validateur vérifie la forme et la provenance déclarée ; il ne peut pas
authentifier à lui seul l'identité d'une personne. La voie de décision VA07
exige une décision LP fournie explicitement, jamais générée par l'agent.

## VA08 — portée documentaire

Une relation repérée exige `portee` : ETABLIT_L_ENONCE, EN_ETABLIT_UNE_PARTIE
ou ECLAIRE_SEULEMENT. Une portée partielle exige `reste_sans_piece`. Cette
portée compare le paragraphe à la pièce, sans jugement de vérité objective.
