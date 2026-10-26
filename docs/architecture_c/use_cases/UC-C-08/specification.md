# UC-C-08 — Composer et référencer une citation fidèle

**Complément C-COT-2026-10-21-R1 — L3-B/L4 — US-C-08, V2 US-06.**
Acteur : rédacteur. Déclencheur : composition/insertion d’une citation dans
une occurrence rédactionnelle d’une VersionActe de travail.

La [décision PO](../../references/DECISION_PO_COTATION_DOCUMENT_CITATIONS_2026-10-21.md)
est acquise; [modèle transversal](../../MODELE_TRANSVERSAL_COTATION.md).
Ce complément renseigne la cotation du dossier encore `A_SPECIFIER`.
Les quatre vues locales, leur revue et leur approbation restent à produire.
Les exigences de fidélité, ancrage et certification de la story restent applicables.

| Critère complémentaire | Résultat attendu |
|---|---|
| COT08-AC01 | La citation garde son identité qualifiée et son document source vérifié; aucun rattachement n’est déduit d’une PK homonyme |
| COT08-AC02 | La référence est résolue dans le bordereau de la version utilisatrice : cote principale du document et sous-cote de la citation, jamais cote principale autonome de Quote |
| COT08-AC03 | Le même extrait peut être utilisé plusieurs fois avec la même sous-cotation de version; conserver les utilisations distinctes sans créer une cote par insertion |
| COT08-AC04 | L’ordre des segments, omissions/emphases et insertions reste explicite. Il ne remplace pas le profil d’ordonnancement des citations du bordereau |
| COT08-AC05 | Une composition mobilisant plusieurs documents conserve les références de chaque document/citation; elle ne leur invente pas un parent unique ni une cote principale de citation composite |
| COT08-AC06 | Recotation du brouillon : résoudre à nouveau les libellés depuis le même ResultatVersion. Relecture gelée : conserver les références historiques et les états cités |

Parcours : sélectionner les sources et citations → vérifier provenance et
capacités PHRASE/D07 → composer et ancrer selon D10 → résoudre chaque renvoi
dans le bordereau de la version. Source ambiguë, référence absente ou mauvais
document/version : diagnostic et refus du strict concerné; aucune correction
implicite de l’identité ou du texte source.

Dépendances : UC02/04 pour occurrence/utilisations, contrats UC09/16 pour
résolution, fournisseur A pour PHRASE, D07 selon source. R04 ne porte plus que
sur notation/ordonnancement technique. Scénarios COT:T01/T04/T07 et critères
de fidélité existants : **NON EXECUTES**. Aucun code ou lot autorisé ici.

## Compatibilité avec le versionnement transversal

[Contrat C-TRANS](../../MODELE_TRANSVERSAL_C.md) : les entrées probatoires
proviennent d’UP pointant une révision exacte; les sélections sont développées
dans cette révision (TRV04-AC01). ResultatVersion, bordereau et rendu partagent
ces mêmes entrées. Un état figé conserve révisions, états sources, parents et
associations, sans lecture de l’arbre courant (TRV11-AC01).
Cette précision ne modifie aucun critère COT et ne clôt pas R04 technique.
