# R3-CONC — Contre-épreuves à exécuter après autorisation

**23 octobre 2026 — tous les essais T01–T24 ci-dessous : NON EXECUTES.**
Ce document est un plan d'acceptation, pas un journal de tests applicatifs.
La [revue B01](../../../../lots/C0-A/REVUE_INDEPENDANTE_B01.md#5-tests-effectivement-exécutés-par-b)
reste le seul résultat référencé : 270 tests applicatifs et 33 d'outillage
réussis sur l'ancien candidat, mais **deux échecs tardifs bloquants**.
Ces succès ne prouvent aucune garantie de R3-CONC.

## Banc et synchronisation nécessaires

Reconstitution indépendante au socle `515666e`, patches de reprise et B01 de
`f35ec85`, puis delta R3 autorisé. PostgreSQL jetable, données synthétiques,
deux connexions/PID distincts, réglages refusant toute base réelle. Utiliser
des tests transactionnels réellement committables, sans transaction de
fixture qui masquerait les attentes. Aucun essai SQLite ne prouve ces courses.

Piloter les entrelacements par événements/barrières observables : E0 lu,
protection effective, passage du signal, DELETE sur le point de partir,
attente réelle de T2, commit/rollback. Relever les PID et les verrous
PostgreSQL. Les pauses dans `execute_wrapper` conservent la requête et ses
paramètres; les gardes ne sont pas remplacées. Attentes bornées pour le banc,
nettoyage dans `finally`, aucune réussite artificielle exigée pendant un verrou.

Deux campagnes sont nécessaires pour les nouveaux tests discriminants :
ancienne production `f35ec85` inchangée, puis candidat corrigé. Le même test
doit échouer par **violation de l'assertion de conformité** sur l'ancienne
version; un timeout de harnais, une fixture cassée ou un import absent ne
constitue pas une reproduction du défaut. Les contrôles historiques restent
consultables; ne pas réécrire leurs anciens résultats.

## Scénarios affectés

| Test | Entrelacement / contrôle | Acceptation |
|---|---|---|
| T01 | B01 initial : remplacement d'un descendant par un nouveau Statement avec compensation d'effectif | Refus T1, aucune archive T1, état et archive T2 conservés, identités exactes. |
| T02 | Même scénario avec citation nouvelle | Même résultat; aucune archive citation de T1. |
| T03 | Cas A : HTTP UC13 valide après E0 mais avant protection effective de T1 | Nouveau Statement et captures T2 conservés; refus T1 et extrémités restaurées. |
| T04 | Cas A : `save()` repointe vers une citation dans le même intervalle | Refus T1, rattachement citation T2 conservé, aucune archive mensongère. |
| T05 | Cas B tardif B : HTTP démarrée entre garde `pre_delete` et DELETE | Observer l'attente; laisser T1 committer; HTTP T2 refusée, aucune recréation ni effets partiels T2. L'ancienne version accepte l'édition puis la perd. |
| T06 | Cas B tardif B : instance chargée puis `save()` ordinaire repointant vers citation | Même attente puis refus de domaine; aucune ligne recréée. L'ancienne version supprime la citation sous une archive Statement. |
| T07 | Ancienne instance sauvegardée sans `update_fields` après le commit de suppression | Refus, absence de la PK confirmée, ni INSERT implicite ni changement d'archives. |
| T08 | Même ancienne instance avec `update_fields`; tentative `force_insert` sur instance chargée | Refus propre dans les deux variantes; aucun ancien PK réinséré. |
| T09 | T1 annule après protection; T2 HTTP attendait | T2 reprend sur l'occurrence restaurée, refait ses contrôles et peut valider; aucune archive/repointage T1 subsistant. |
| T10 | Même rollback T1; T2 ORM citation attendait | Repointage possible après restauration et contrôles propres; aucune archive citation T1. |
| T11 | Pannes après archive, après repointage, après premier retrait (trois points) | Rollback complet des archives, extrémités, nœuds et compteurs; 403 pour refus, 500 pour panne. |
| T12 | RELEASE du savepoint de service avant fin de la transaction HTTP | T2 reste bloquée jusqu'au commit externe, puis refuse la cible supprimée; aucun succès HTTP anticipé. |
| T13 | Plusieurs descendants : l'un modifié par T2 avant protection T1 | Refus de tout le bloc; aucun autre descendant archivé/supprimé par T1; commit indépendant T2 conservé. |
| T14 | Deux suppressions sur des branches sœurs avec parent compteur commun | Ordre de protections compatible, pas de compteur perdu/négatif; attente puis relecture/refus si le plan a changé. |
| T15 | Deux opérations à ensembles chevauchants présentés dans des ordres inverses | Le mécanisme prend les PK dans le même ordre; fin bornée, aucun préfixe d'opération conservé en cas de cible manquante. Aucun nouvel endpoint batch n'est requis. |
| T16 | T2 valide sur une occurrence extérieure au bloc puis T1 refuse/échoue | Ce commit indépendant subsiste avec son texte, ses captures et son association. |
| T17 | T2 comporte deux écritures dans la même transaction non validée et une cible disparaît | Toute cette opération T2 est annulée; ne pas qualifier la première écriture non committée d'indépendante. |
| T18 | Écrivain étranger en ordre inverse provoquant réellement un deadlock PostgreSQL | Victime identifiée SQLSTATE 40P01, rollback intégral; autre transaction conforme, aucun retry caché ni succès partiel. |
| T19 | Modification directe du texte d'un Statement partagé, avant/après sa protection | Avant : texte divergent détecté et refus T1. Après : UPDATE attend; l'archive validée correspond exactement au texte effectivement retiré. Pas de purge ni réécriture UC13 des autres usages. |
| T20 | Descendant nouveau/déplacé visible lors de la relecture B1 | Ensemble exact différent : refus entier. Ne pas assimiler ce test à une protection contre l'orphelin tardif après commit. |
| T21 | Archive d'un Statement vide, structure vide, chemins/item/numéro, extrémités multiples | Chaque archive correspond champ par champ à l'état protégé supprimé; textes vides distingués; anciennes décisions/captures consultables; `statements_supprimes=[]`. |
| T22 | REPRODUCED/référent historique, ConfirmationAppui, AncrageCitation, GFK incohérente, citation et objet manquant | Refus atomiques inchangés, aucune archive partielle; gardes directes ORM existantes toujours actives. |
| T23 | UC13 partage de Statement, texte égal/distinct, item, rollback et création Treebeard neuve | COW neuf sur changement, autres usages intacts, texte égal sans capture inutile, insertion neuve ordinaire conservée, aucune régression des compteurs. |
| T24 | Suites complètes UC13/14/15, citations P6 et E01; outillage; Django check et migrations à sec | Aucun échec; aucun changement de schéma. Rapporter nombre réellement découvert, durée, journal et SHA, sans supposer que l'effectif futur restera 270/33. |

T05/T06 et T07 doivent être démontrés discriminants contre `f35ec85`.
T01/T02 servent de non-régression du B01 initial, déjà corrigé; ils ne sont
pas attendus en échec contre cette livraison. T03/T04 assurent l'ordre A;
leur passage seul ne valide pas l'ordre B. Les tests peuvent regrouper
plusieurs variantes, mais le rapport doit conserver ces identifiants et
indiquer le nombre réel d'essais exécutés, sans compter un plan comme un test.

## Fidélité, atomicité et clôture

Pour chaque retrait accepté, conserver un relevé d'état pris **après** la
protection et avant les archives, puis comparer document, ancien ID,
path/depth, item, numéro, identité Statement, texte et empreinte aux archives.
Vérifier séparément les associations aux archives, décisions historiques et
captures toujours lisibles. Après refus, comparer toutes les tables affectées
à leur état attendu en tenant compte des seuls commits indépendants T2.

Conserver diff complet et delta, versions des dépendances, isolation des
connexions, logs et empreintes. Les contre-épreuves tardives doivent réussir
sur le candidat, puis être revues indépendamment par B. Le succès des suites
historiques seul ne lève pas B01. L'orphelin tardif reste une réserve distincte,
sans correction ni prétendue preuve de fermeture dans ce lot.
