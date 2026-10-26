# UC-C-09 — Bordereau et cotation des documents par version

**Complément C-COT-2026-10-21-R1 — L3-A — US-C-09, V2 US-05/09.**
Acteur : rédacteur. Déclencheur : calcul ou consultation du bordereau d’une
VersionActe identifiée et de son ResultatVersion.

La [décision PO](../../references/DECISION_PO_COTATION_DOCUMENT_CITATIONS_2026-10-21.md)
fixe définitivement le document coté et les citations sous-cotées.
[Modèle transversal et cas sans citation](../../MODELE_TRANSVERSAL_COTATION.md).
Ce complément laisse le dossier `A_SPECIFIER` : quatre vues et validation du
dossier complet manquantes, aucun développement autorisé.

| Critère complémentaire | Résultat attendu |
|---|---|
| COT09-AC01 | Le périmètre réunit les documents effectivement retenus pour la production par les utilisations de la version; une citation sélectionnée conserve son document parent dans ce périmètre |
| COT09-AC02 | Calculer une cote principale par `(VersionActe, DocumentSource)` selon CHRONO_VERSION/D06; répétitions de citations ou d’usages ne multiplient pas la cote du document |
| COT09-AC03 | Chaque citation retenue reçoit une sous-cote sous la cote de son document dans cette même version; aucune Quote n’est une entrée principale autonome |
| COT09-AC04 | Document entier retenu sans citation : une cote principale et zéro sous-cote; ne créer aucun extrait fictif |
| COT09-AC05 | Bordereau, références dans le texte, fichiers et cahier consomment les mêmes associations du ResultatVersion; un filtre d’affichage ne recalcule pas la référence |
| COT09-AC06 | Insertion/retrait recalcule le brouillon; le gel conserve les documents, citations, cotes, sous-cotes, profil et usages exacts. Une autre version peut recoter sans modifier l’histoire |

Parcours : résoudre sélections et parents → établir les documents retenus
et les états/compositions → classer les documents selon D06 → attribuer cotes
puis sous-cotes selon le profil → publier le résultat commun. Dates requises
non établies, parent incohérent ou règle technique de sous-cotation manquante :
diagnostic et refus du résultat strict concerné, sans date ou ordre inventé.

R03 conserve son périmètre sur dates de composites; R04 concerne seulement
notation et ordre technique des sous-cotes. Les documents sans citation et
le principe cote/sous-cote ne sont plus des arbitrages. Dépendances UC04/16,
interfaces UC08/10/11/17; scénarios COT:T01/T02/T04/T05/T06/T07 et scénarios
CHRONO_VERSION existants : **NON EXECUTES** dans ce complément.

## Compatibilité avec le versionnement transversal

[Contrat C-TRANS](../../MODELE_TRANSVERSAL_C.md) : les entrées probatoires
proviennent d’UP pointant une révision exacte; les sélections sont développées
dans cette révision (TRV04-AC01). ResultatVersion, bordereau et rendu partagent
ces mêmes entrées. Un état figé conserve révisions, états sources, parents et
associations, sans lecture de l’arbre courant (TRV11-AC01).
Cette précision ne modifie aucun critère COT et ne clôt pas R04 technique.
