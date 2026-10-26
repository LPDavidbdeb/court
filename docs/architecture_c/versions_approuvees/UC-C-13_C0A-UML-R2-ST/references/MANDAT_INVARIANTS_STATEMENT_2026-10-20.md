# Mandat à l'Agent B — Clarification des invariants de réutilisation des Statement et révision d'UC-C-13

## 1. Décision fonctionnelle

Je souhaite préciser une règle fondamentale de l'application, qui doit désormais guider la conception et la validation d'UC-C-13.

**Seuls les `Statement` provenant de documents de type `REPRODUCED` peuvent être réutilisés par d'autres occurrences.**

Les documents `REPRODUCED` sont des reproductions de documents figés dans le temps. Leur contenu n'est pas éditable.

Les documents `PRODUCED`, en revanche, sont destinés à la rédaction et peuvent être modifiés sous réserve des protections historiques applicables.

J'établis donc les invariants fonctionnels suivants :

1. Les occurrences et les contenus des documents `REPRODUCED` sont immuables.
2. Les `Statement` provenant de documents `REPRODUCED` peuvent être réutilisés dans les documents `PRODUCED`.
3. La modification du texte d'une occurrence `PRODUCED` qui réutilise un tel `Statement` ne modifie jamais le `Statement` d'origine. Elle entraîne la création d'un nouveau `Statement` propre à l'occurrence modifiée.
4. Les `Statement` créés pour les documents `PRODUCED` ne peuvent pas être réutilisés par d'autres occurrences.
5. Une modification autorisée dans un document `PRODUCED` ne doit jamais altérer les contenus d'autres occurrences ni les états historiques protégés.

Ces règles définissent le comportement cible. Elles ne constituent pas une affirmation selon laquelle le code existant les garantit déjà.

## 2. Conséquences pour UC-C-13

La formulation actuelle du use case est :

« Modifier une occurrence partageant un Statement ».

Elle décrit un risque technique, mais ne rend pas suffisamment explicite la distinction fonctionnelle entre `REPRODUCED` et `PRODUCED`.

Je te demande de réexaminer le contrat d'UC-C-13 à partir de cette distinction.

En particulier :

- AC01 doit garantir l'interdiction de modifier le contenu des documents `REPRODUCED` et des occurrences historiques protégées.
- AC02 doit décrire la création d'un `Statement` privé lorsqu'une occurrence éditable réutilise un `Statement` d'origine immuable.
- AC03 doit préciser les conditions permettant la modification directe d'un `Statement` propre à une occurrence `PRODUCED`.
- AC04 doit maintenir la distinction entre modification du texte et modification de `item`, sans produire de détachement inutile.
- AC05 et AC06 doivent préserver la détection des changements d'identité ou de contenu et la conservation des décisions antérieures.
- AC07 doit conserver l'atomicité des opérations.
- AC08 doit maintenir la séparation entre `Statement` et citations `HERITE / PHRASE`.

Ne modifie pas mécaniquement les huit critères. Conserve ceux qui sont déjà conformes et corrige uniquement les formulations ou garanties affectées par cette décision.

## 3. Vérification du modèle existant

Avant de conclure, examine comment l'application distingue actuellement :

- Un `Statement` provenant d'un document `REPRODUCED`.
- Un `Statement` privé d'une occurrence `PRODUCED`.
- Un `Statement` partagé entre plusieurs occurrences.
- Une occurrence historiquement protégée.
- Un `Statement` qui aurait été réutilisé contrairement à la nouvelle règle.

La provenance d'un `Statement` ne doit pas être déduite arbitrairement de sa seule utilisation actuelle si plusieurs associations sont possibles.

Vérifie si les modèles et relations existants permettent d'établir cette distinction de manière fiable.

Si une contrainte supplémentaire est nécessaire, présente la solution minimale et indique le lot responsable. Ne crée pas automatiquement une nouvelle entité ou une migration.

Vérifie également si des parcours historiques ou des associations déjà présentes pourraient contredire la règle. Toute situation existante incompatible doit être signalée, sans modification ou suppression automatique.

## 4. Réévaluation du risque de concurrence

Une réserve a été soulevée concernant le cas où un `Statement` considéré comme privé deviendrait partagé pendant une modification.

La nouvelle règle interdit précisément cette réutilisation des `Statement` privés.

Je te demande donc de réévaluer ce risque.

Détermine :

1. Si le scénario est effectivement impossible dans les parcours autorisés.
2. Si cette impossibilité est garantie par le code existant ou seulement prévue par le contrat fonctionnel.
3. Si certains chemins de création, copie, rattachement ou modification permettent de contourner cette règle.
4. Si une protection minimale est nécessaire dans C0-A ou relève d'un lot ultérieur.

Ne conserve pas une exigence complexe de verrouillage uniquement pour prévenir un comportement désormais interdit, sauf si tu démontres qu'un risque concret subsiste.

Inversement, ne déclare pas le risque éliminé si la règle n'est pas effectivement respectée par tous les chemins d'écriture pertinents.

## 5. Vérification des conséquences sur les autres use cases

Cette décision doit être confrontée aux autres contrats qui créent, réutilisent, copient ou suppriment des occurrences, notamment :

- UC-C-02 — Structure rédactionnelle.
- UC-C-07 — Reprise de sous-arbres.
- UC-C-14 — Suppression d'occurrences.
- UC-C-15 — Consultation des appuis d'origine.

Indique les conséquences éventuelles sans élargir inutilement le périmètre de C0-A.

En particulier, la réutilisation du contenu d'un `Statement` et le partage de son identité sont deux opérations différentes : recopier un texte n'implique pas nécessairement réutiliser son objet source.

## 6. Révision des diagrammes UML

Réexamine les quatre diagrammes d'UC-C-13 :

- Activity Diagram.
- Sequence Diagram.
- ERD.
- Class Diagram.

Assure-toi qu'ils expriment correctement la distinction entre les deux types de documents, la protection des sources reproduites et la propriété des contenus éditables.

Les diagrammes doivent montrer les responsabilités et les contrôles effectivement nécessaires.

Si une modification s'impose, révise les sources PlantUML concernées, régénère les rendus et valide leur cohérence.

Mets également à jour les critères d'acceptation, les scénarios de test et la traçabilité concernés.

Ne produis pas de nouveaux diagrammes sans nécessité.

## 7. Une question à conserver distincte : `item`

La modification de `item` ne doit pas être confondue avec celle du texte d'un `Statement`.

Vérifie si `item` constitue seulement une propriété éditoriale de l'occurrence ou si sa modification peut rendre une décision historique périmée.

Précise les garanties de C0-A et celles qui relèvent de L1-A/C0-B.

Cette question ne doit pas être déclarée résolue par la seule règle de réutilisation des `Statement`.

## 8. Restrictions

Le présent mandat est exclusivement architectural et documentaire.

- Ne modifie pas le code applicatif.
- N'applique aucune migration.
- Ne modifie pas la base réelle.
- Ne modifie pas le patch C0-A.
- Ne commence pas l'implantation d'UC-C-13.
- Ne présume pas de mon approbation fonctionnelle.

L'anomalie distincte `C0A-REV-01`, concernant la disparition des appuis valides en présence d'un référent invalide, demeure ouverte et doit rester traitée dans le dossier UC-C-15.

## 9. Livrables attendus

Je souhaite recevoir :

1. Une formulation consolidée des invariants `REPRODUCED / PRODUCED`.
2. La version révisée d'UC-C-13 et de ses critères, si des corrections sont nécessaires.
3. Les quatre diagrammes UML mis en cohérence.
4. Une analyse du respect effectif des nouvelles règles par le modèle et les opérations existantes.
5. Une conclusion précise sur le risque de concurrence.
6. La liste des impacts éventuels sur les autres use cases et lots.
7. Les décisions ou garanties qui demeurent ouvertes avant approbation.

## 10. Résultat recherché

**Je souhaite qu'UC-C-13 exprime la véritable règle métier : les documents `REPRODUCED` constituent des contenus historiques immuables et réutilisables; les documents `PRODUCED` permettent une rédaction modifiable dont les `Statement` privés ne sont pas partagés.**

La protection contre la modification involontaire d'autres occurrences doit découler de cette règle plutôt que d'un mécanisme général de gestion du partage plus complexe que nécessaire.

Après révision, soumets-moi la version exacte du dossier UC-C-13 pour approbation.

Aucune approbation ni autorisation de développement n'est accordée par le présent mandat.