# Registre d’exécution — arrêt au pilote VA16

État courant du mandat dicté par LP. Les SHA ci-dessous sont les commits
réels contrôlés dans Git ; chaque commit de story est limité aux deux racines
modifiables autorisées. Les rapports portent les listes exactes de fichiers
issues de Git, les sorties brutes des tests et les lectures réelles.

| Story | Verdict courant | Commit de livraison | Tests synthétiques | Rapport |
|---|---|---|---|---|
| VA01 | **PASS** | `feba45e45cbea9ad4ed6867664c32254f7ff10f9` | 5 OK | [VA01.reel.md](VA01.reel.md) |
| VA02 | **PASS** | `472a22d7a81cf3e01f76fd4832932bbed59eb07b` | 4 OK | [VA02.md](VA02.md) |
| VA03 | **PASS** | `ae00981d2228fcb2ba21b84930f503e9b5d0eab2` | 1 OK | [VA03.md](VA03.md) |
| VA04 | **PASS** | `8cbeec74c9f285fa54ed6af1ee79650c6e0e9620` | 3 OK | [VA04.md](VA04.md) |
| VA05 | **BLOQUÉ — 8 liens sans fichier matérialisé** | `57d35692caf056a5283cd1c1f5ff3f0ccb44efc5` | 2 OK | [VA05.md](VA05.md) |
| VA06 | **PASS** | `647adbecaaf4de4db3845afb0fb146b1dd04f35c` | 2 OK | [VA06.md](VA06.md) |
| VA07 | **PASS** | `29a8f9e0e46fd925e8750e7273f75f8b792e0ea5` | 2 OK | [VA07.md](VA07.md) |
| VA08 | **PASS** | `f3eee6bfce3319ac92cbacaa30c869088921cdbd` | 3 OK | [VA08.md](VA08.md) |
| VA09 | **PASS** | `1198be7775535c1e48be35705fab5cfe376258cb` | 3 OK | [VA09.md](VA09.md) |
| VA10 | **PASS** | `04df3717a5944c3ca64eefff65d89d5fe2d5d519` | 3 OK | [VA10.md](VA10.md) |
| VA11 | **PASS** | `38981c1cc971c863e7edcfca20dc9a7374bc7a4d` | 1 OK | [VA11.md](VA11.md) |
| VA12 | **PASS** | `7a15ff07d7fe5d3babfc6fa8fe3252b8170f0498` | 1 OK | [VA12.md](VA12.md) |
| VA13 | **PASS** | `b3b29b869aeac3c7a1e6f439e8b90a7eda366c93` | 2 OK | [VA13.md](VA13.md) |
| VA15 | **PASS** | `98b23112e856679d53410c5547d27accb9dd36b6` | 2 OK | [VA15.md](VA15.md) |
| VA16 | **BLOQUÉ — recette LP attendue** | `ecbe88ba5a5bcefdee4c8b9a30009ae08ff67542` | 2 OK | [VA16.md](VA16.md) |

## Résultat et point d’arrêt

- Recette technique cumulée : **36 tests réussis**, [sortie brute](RECETTE_PHASE0.tests.txt).
- VA01 réel : **287 énoncés, 515 liens, 268 cotes**, deux captures identiques
  octet pour octet ; 198 numéros imprimés propres appariés, aucun numéro inventé.
- VA05 : **515 fiches, 628 fichiers source hachés**. Les huit liens 240–247,
  vers P-58 à P-64, restent sans fichier matérialisé au manifeste. Ils sont
  explicitement bloqués et ne font pas partie du pilote.
- Pilote : **7 propositions CODEX**, liens 468–474, **0 VALIDE, 0 REJETE**.
  Le §236 sans référence est présenté séparément. [Dossier à valider](../../../legal/verification_appuis/pilote/A_VALIDER_PAR_LP.md).
- Couverture globale après pilote : 508 NON_EXAMINE, 7 PROPOSE, 0 VALIDE,
  0 REJETE, 0 A_REVOIR. Le pilote a 7 PROPOSE et un taux de validation LP de 0 %.
- VA14 exclue ; VA17 non exécutée ; aucune autre série et aucune phase 1.
- Le JSON d’accords a été reproduit tel que dicté. Les lectures PostgreSQL ont
  utilisé uniquement le socket Unix local et des transactions READ ONLY.
  Aucun fichier source ni aucune donnée métier en base n’a été modifié par
  cet agent. Les tests SQL d’altération concernent uniquement les fixtures.

## Publication

Aucun push n’a été exécuté par cet agent dans ce mandat. L’interdiction réseau
et la demande de push après PASS sont contradictoires ; une question a été
soumise à LP, sans réponse reçue à la clôture. L’état distant n’a pas été
interrogé. Aucun accès Gmail ni autre accès réseau n’a été effectué.

Le superpush préalable, antérieur au présent mandat, avait livré les commits
20d2513, ed973f0 et 80913a0. Les rapports initiaux VA01 et la revue externe
restent conservés comme états historiques ; le présent tableau porte les
verdicts courants. Le suivi documentaire inscrit les SHA après création des
commits, sans prétendre qu’un commit peut contenir son propre identifiant.

## Périmètre de fichiers

Les changements de l’autre activité, dont ceux de `legal/instance/` et la
revue externe hors `execution/`, ne sont pas intégrés aux commits de livraison
ci-dessus. Les commits ont été vérifiés par liste de chemins ; aucune
modification applicative, migration, écriture dans l’archive gelée ou création
de cote de pièce n’appartient à ces livraisons.
