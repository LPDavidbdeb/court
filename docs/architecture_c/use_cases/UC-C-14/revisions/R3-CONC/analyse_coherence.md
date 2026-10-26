# UC14 R3-CONC — Défaut, mécanisme et cohérence des quatre vues

**23 octobre 2026 — conception préalable, pas un rapport d'implantation.**
Le [mandat utilisateur](mandat_source.md) exige une revue UML avant tout
code. La [revue B01](../../../../lots/C0-A/REVUE_INDEPENDANTE_B01.md) demeure
l'autorité sur les résultats exécutés et le blocage du candidat `f35ec85`.

## 1. Fenêtre identifiée précisément

Le candidat reconstruit part de `515666e`, reçoit le patch de reprise puis
le delta B01 de `f35ec85`. `supprimer_occurrence` archive et repointe dans un
`atomic` de service, imbriqué dans l'`atomic` de `ajax_delete_node`.
La garde finale de `protection.py` compare l'instance collectée et relève
son identité pendant `pre_delete`. Le collecteur Django émet ces signaux,
puis exécute `delete_batch(pk_list)`. Le SQL retire des PK; il ne conditionne
pas le retrait au texte ou à la clé générique contrôlés par le signal.

Dans cette séparation, T2 valide une édition réelle `ajax_edit_node`, ou un
`LibraryNode.save()` repointant vers une citation. T1 retire ensuite la même
PK avec un état différent de l'archive. Le contrôle des identités et le
contrôle final du chemin ne détectent pas ce changement d'état. Les deux
échecs tardifs de B01 restent acquis; une nouvelle lecture seule déplacerait
la fenêtre sans l'éliminer. Ni `atomic` seul ni un signal `pre_delete` ne
réservent la ligne contre cette édition.

## 2. Protection locale recommandée

### T1 : plan, acquisition, revalidation et retrait

1. Dans la transaction de suppression, lire un **plan attendu** B0/E0 :
   ensemble exact des PK du bloc, identité/document, path/depth, item,
   paragraph_number, paire ContentType/object_id; pour un Statement réel,
   identité et texte/empreinte attendus. Ajouter les parents dont l'API
   Treebeard modifiera `numchild`, y compris le parent extérieur au bloc.
   Ces valeurs en mémoire ne sont ni un examen inventé ni une nouvelle table.
2. Acquérir et **évaluer** les verrous `SELECT ... FOR UPDATE` de toutes
   ces LibraryNode dans l'ordre croissant des PK, sur la même connexion et
   dans le même `atomic`. Aucun `skip_locked`, aucune exclusion silencieuse.
3. Recharger sous protection; vérifier l'existence, l'identité des parents,
   la composition exacte du bloc B1=B0 et l'état documentaire E1=E0. Si le
   plan diffère, refuser et annuler l'opération. Ne pas étendre tardivement
   le plan en prenant de nouveaux verrous dans un autre ordre. Une lecture
   initiale répartie sur plusieurs requêtes ne dispense pas de ce contrôle.
4. Verrouiller ensuite les Statement utilisés, par PK croissante, et relire
   leurs textes. Tout changement depuis le plan est un refus. Refaire les
   gardes de mutabilité, référents, décisions/cascades et archivabilité sous
   protection. Les structures sans contenu restent distinctes des textes
   vides; les citations restent refusées par C14-D2.
5. Archiver les instances **rechargées et protégées**, repointer les
   extrémités, puis employer l'API Treebeard du bas vers le haut. Conserver
   les gardes finales et les contrôles d'identités B01, sans les traiter
   comme substituts aux protections. Conserver tous les contenus/captures.
6. Garder les verrous pendant `pre_delete`, le SQL effectif et jusqu'au
   **commit de la transaction HTTP externe**. Relâcher le savepoint de
   service ne clôt pas cette période. Une erreur tardive annule les
   archives, associations, retraits et compteurs de cette opération avant
   son interception HTTP.

Treebeard 4.8.0, `MP_NodeQuerySet.delete`, recharge les parents et appelle
`parent.save()` pour décrémenter leurs compteurs, puis délègue au collecteur
Django. Les parents font donc partie du périmètre d'écriture local à
protéger. `numchild` est un compteur structurel qui évolue légitimement
pendant les retraits : ne pas assimiler sa nouvelle valeur à une modification
du contenu probatoire depuis E0. Vérifier sa cohérence structurelle séparément.

La documentation PostgreSQL explique l'attente des écritures concurrentes,
la durée des verrous et leur libération lors d'un rollback au savepoint.
Ces propriétés motivent le protocole; elles ne prouvent pas que son futur
code les respectera. [Verrous PostgreSQL 18](https://www.postgresql.org/docs/18/explicit-locking.html).
Sous READ COMMITTED, un `SELECT FOR UPDATE` qui attend peut retrouver une
ligne mise à jour, ou aucune ligne si elle a été supprimée : la relecture
et le test d'existence après attente sont nécessaires.
[Isolation PostgreSQL 18](https://www.postgresql.org/docs/18/transaction-iso.html).

### T2 : participation des voies d'écriture et absence de résurrection

`ajax_edit_node` doit acquérir la protection de la cible et la recharger
**avant** le détachement, les captures et les changements d'association ou
d'intitulé. Les règles UC13 R2-ST restent celles approuvées : copie neuve
si texte distinct, aucun détachement inutile si texte égal, rollback complet
en cas de refus. Une cible absente à l'entrée conserve le 404. Si elle était
présente mais disparaît pendant l'attente, le refus de domaine est traduit
en 403; pas de réponse de succès ni de contenu neuf partiellement conservé.

La voie ORM doit aussi être couverte. Une méthode `LibraryNode.save()`
adaptée localement distinguera l'instance existante chargée (`_state.adding`
faux) de la création neuve Treebeard. Pour une instance existante : même
alias de base et `atomic`, protection/relecture de la ligne, refus si absente,
puis sauvegarde **UPDATE seulement**. Même sans `update_fields`, aucun
fallback de l'UPDATE vers un INSERT n'est permis. Un `force_insert` sur
cette ancienne instance doit être refusé. Les parents Treebeard déjà
protégés par T1 peuvent être sauvegardés dans la même transaction.

Une instance neuve conserve le chemin d'insertion Treebeard. La fermeture
de `bulk_create`, du SQL brut, de `save_base` direct, d'une falsification
manuelle de `_state` ou d'une reconstruction volontaire d'objet neuf avec
ancien PK n'est pas promise ici. Ce sont des limites différentes d'un
`save()` ordinaire sur l'instance réellement chargée avant suppression.

Cette adaptation est indispensable : Django peut tenter une insertion si
la sauvegarde normale d'une instance à PK ne met aucune ligne à jour.
[Sauvegarde des modèles Django 5.2](https://docs.djangoproject.com/en/5.2/ref/models/instances/).
Les requêtes de verrouillage sont paresseuses : les construire ne suffit
pas; leur évaluation doit se faire dans la transaction de l'opération.
[select_for_update Django 5.2](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#select-for-update).

## 3. Deux issues sûres et annulations

| Ordonnancement | Résultat requis |
|---|---|
| T2 valide après la lecture E0, avant la protection T1 | T1 relit l'état changé et refuse. Le commit T2 demeure. Aucune archive ni suppression partielle T1 ne subsiste. |
| T1 protège, puis T2 veut écrire | T2 attend sans exiger un succès impossible pendant le verrou. T1 archive l'état protégé et valide son retrait. T2 relit la ligne absente et refuse; aucune réinsertion. |
| T1 protège puis échoue après écritures | Rollback T1 de toutes ses écritures; les verrous pris après le savepoint sont libérés par son rollback. T2 peut reprendre sur les lignes restaurées, refaire ses contrôles et valider si admissible. Les verrous antérieurs au savepoint suivent la transaction externe. |
| T2 a déjà validé une opération distincte sur une autre occurrence | Cette transaction indépendante est préservée quel que soit le résultat T1. Des écritures encore non validées dans une même transaction T2 ne sont pas des effets indépendants. |

La continuité vient du verrou de la ligne existante détenu entre sa
validation et le commit : un UPDATE concurrent ne peut plus être validé
dans l'intervalle `pre_delete`–`DELETE`. La barrière T2 et l'UPDATE sans
réinsertion ferment le second risque, après le retrait validé de T1.
Cela doit être observé sur deux connexions PostgreSQL lors de l'implantation.

## 4. Plusieurs occurrences, portée et limites

Les ensembles connus suivent l'ordre commun **LibraryNode par PK puis
Statement par PK**, avant mutation. Les parents de compteurs sont inclus.
Une opération portant sur plusieurs occurrences refuse en entier si une
cible manque; aucun préfixe de lot n'est conservé. Les essais devront aussi
exercer des suppressions sœurs avec parent commun et des textes partagés.

Ce protocole ne promet pas l'absence universelle de deadlock : un écrivain
extérieur acquérant les ressources en ordre inverse peut encore en créer.
La victime PostgreSQL doit annuler intégralement sa transaction, avec erreur
technique, sans succès partiel ni retry caché. Les tests bornent les attentes
et identifient les PID, verrous et événements; un timeout de test n'est pas
une preuve de sécurité.

La protection de lignes n'est pas un verrou de plage sur tout l'arbre.
Un nouveau membre observé lors des contrôles provoque un refus; aucune
garantie contre toutes les insertions possibles n'est déduite de ces verrous.
**L'orphelin tardif reste distinct et non corrigé** : ajout UC02 sur un parent
périmé après le retrait, déjà documenté dans la revue antérieure. Ni
`ajax_add_node`, ni verrou général de Cause/Document, ni nouveau schéma ne
sont proposés ici. Les limites L1-A/C0-B/L5 restent inchangées.

## 5. Impact cohérent sur les vues

| Vue | Révision et conclusion |
|---|---|
| [Séquence principale](sequence.svg) | Acquisition effective, E0/E1, Statement, archive, SQL et commit externe; T2 avant/après protection, refus et absence d'INSERT. Deux compléments couvrent rollback et plusieurs occurrences. |
| [Activité](activity.svg) | Contrôle exact du plan sous protection, types et textes, rollback total et finalisation avant réponse. [Complément T2](activity_t2.svg) pour UC13/save périmé. |
| [Classes](class.svg) | produced_views = frontières HTTP; concordance = orchestration; protection = plan, acquisition, validation, archives/gardes; LibraryNode.save = existence et UPDATE seul; Treebeard = retrait/compteurs; atomic/PostgreSQL = durée. PlanRetrait/EtatControle sont en mémoire. |
| [ERD](erd.svg) | **Aucun changement de schéma nécessaire à cette solution.** Mêmes tables/champs/relations que R2-HIST. La nouvelle copie ne change que le chemin relatif d'inclusion du style; les anciens ERD source/rendus et leurs manifestes restent intacts. Les verrous ne sont pas des relations persistantes. |

UC13 est techniquement affecté par la barrière avant mutation, sans changer
AC01–AC08 R2-ST. Les quatre vues partagées ici et l'activité T2 rendent cet
impact explicite; l'ancienne approbation UC13 ne valide pas automatiquement
ce mécanisme nouveau. UC15 consomme les mêmes archives/diagnostics : aucune
responsabilité nouvelle; sa non-régression devra être exécutée. Aucun modèle
transversal ni décision de cotation n'est réouvert.

## 6. Périmètre exact de la future autorisation proposée

Après revue et approbation explicite, reconstruire un banc **indépendant de
A** au socle `515666e` avec les deux patches livrés à `f35ec85`, puis produire
un delta correctif. Cette référence de reconstitution ne modifie pas la
cible P6 validée ni le pilote A. PostgreSQL jetable, socket privé, refus des
réglages réels et de `.env`; aucune écriture sur la base réelle.

Fichiers applicatifs proposés, tous déjà dans le périmètre historique C0-A :

| Fichier | Nécessité précise |
|---|---|
| `document_manager/concordance.py` | Plan/revalidation, protections et orchestration du retrait; frontière atomique avant interception HTTP. |
| `document_manager/protection.py` | Helpers de protection et gardes locales; état attendu, archivage exact et contrôles finaux existants. |
| `document_manager/models.py` | Sauvegarde d'une LibraryNode existante : protection/existence et UPDATE seul; aucune déclaration de champ ou Meta modifiée. |
| `document_manager/views/produced_views.py` | Barrière UC13 avant ses écritures, traitement du refus de cible disparue, transactions HTTP conservées. |
| `document_manager/test_e01_numerotation.py` | Contre-épreuves tardives, variantes multiligne, non-résurrection et atomicité. |

La correction ne peut donc pas se limiter aux trois fichiers du delta B01 :
les modifications proposées de `models.py` et de la voie HTTP sont justifiées
par les deux écrivains et par le risque de résurrection demandé explicitement.
Tout autre fichier doit être signalé et justifié **avant** son changement.
Les rapports, patches et preuves restent sous `lots/C0-A/`, sans remplacer
les livraisons antérieures.

Interdits : schéma/migration, purge de contenu, réécriture des contrats
approuvés, voie d'ajout, arbre global, L1-A/C0-B/L5, modification du pilote ou
des contrôles A, commit/push/fusion/déploiement et ressources réelles.
Après correction seulement : résultats complets, delta et nouvelle revue B.
L'intégration restera une autorisation distincte.
