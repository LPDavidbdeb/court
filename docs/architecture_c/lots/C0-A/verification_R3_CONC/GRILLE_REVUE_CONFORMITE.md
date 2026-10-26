# UC14 R3-CONC — Grille de revue d'un futur candidat correctif

**23 octobre 2026 — vérification applicative en attente.**
Candidat R3 soumis : **aucun identifié**. Code examiné pour une conformité
R3 : aucun. Essais applicatifs exécutés dans ce mandat : **aucun**.
Cette grille décline les contrats approuvés; elle ne les complète pas par
de nouvelles garanties ni par une approbation anticipée du code.

## Références opposables et lecture des états

Référence documentaire immuable :
[`b0adf1136c55c38a830d3a1cd1a4332741bf297d`](https://github.com/LPDavidbdeb/court/tree/b0adf1136c55c38a830d3a1cd1a4332741bf297d/docs/architecture_c/use_cases/UC-C-14/revisions/R3-CONC).
Sources : [spécification AC01–AC07/G01–G10](../../../use_cases/UC-C-14/revisions/R3-CONC/specification.md),
[analyse §§1–6](../../../use_cases/UC-C-14/revisions/R3-CONC/analyse_coherence.md),
[plan T01–T24](../../../use_cases/UC-C-14/revisions/R3-CONC/plan_tests.md),
[traçabilité](../../../use_cases/UC-C-14/revisions/R3-CONC/tracabilite.md),
[réserves de la revue de conception](../../../use_cases/UC-C-14/revisions/R3-CONC/revue_B.md),
[B01 §§4–7](../REVUE_INDEPENDANTE_B01.md) et [approbation limitée](APPROBATION_UTILISATEUR.md).

| Niveau | Sens | État actuel |
|---|---|---|
| Exigence définie | Comportement attendu dans la conception approuvée | AC/G et T01–T24 définis, conception APPROUVE_UTILISATEUR |
| Garantie examinée dans le code | Chemins réellement présents dans un candidat identifié, avec localisation et limites | NON VERIFIE |
| Garantie démontrée par essais | Assertion passée sur ce candidat, journal et environnement identifiés | AUCUNE pour R3-CONC |
| Garantie non vérifiée | Candidat absent, essai absent ou preuve insuffisante | Tous les contrôles applicatifs ci-dessous |

Lors de la revue, renseigner séparément pour chaque contrôle : localisation
du code, test réellement exécuté, résultat observé, journal/empreinte et
écart éventuel. Une case « exigence définie » n'est jamais un résultat OK.
Valeurs de résultat : **NON VERIFIE**, **DEMONTRÉ DANS LE PÉRIMÈTRE**,
**ECART CONSTATE**, **NON CONCLUANT**. Un succès est borné aux variantes
exercées; pas de garantie universelle déduite de quelques essais.

## 1. Admission du candidat et reproduction indépendante

Avant toute conclusion, relever : identité du livrable (commit ou patches
avec SHA-256), socle, ordre d'application, diff complet et delta R3, empreintes
des fichiers obtenus, auteur et relecteur indépendant. Socle attendu :
`515666eb8c6e7fdcdd265f9187c9c37b769b0fed`, reprise puis delta B01 de
`f35ec8586866f4359d44f52a0bc5cc57c0804217`, puis correction R3 identifiée.
Un autre socle ou une extension doit être explicitement autorisé.

Reconstituer hors des ressources de A, vérifier le périmètre des cinq fichiers
et l'absence de champs, Meta, migrations ou dépendances nouveaux. Les scripts
de banc restent des moyens d'exécution séparés du delta applicatif. Une
base jetable préparée conformément aux autorisations applicables est requise;
aucun `.env` réel, dump réel ou accès réel. Le présent mandat documentaire
n'autorise ni lancement du banc ni exécution de migration.

L'ancien témoin de la campagne discriminante est **le candidat B01 `f35ec85`
reconstitué avec ses deux patches**, pas le seul code de l'arbre Git au SHA
`f35ec85` (qui livre les patches documentaires). Comparer les empreintes de
reconstruction aux preuves B01. Le précédent candidat antérieur à B01 sert
uniquement aux résultats historiques conservés, pas de substitut au témoin
pour la fenêtre tardive R3.

## 2. Fidélité aux sept vues

| Vue approuvée | Vérification dans le candidat | État actuel |
|---|---|---|
| [sequence.puml](../../../use_cases/UC-C-14/revisions/R3-CONC/sequence.puml) | SEQ14-PLAN/LOCK/COMPARE/ARCH/REL/DELETE/COMMIT et ATTENTE/NOINSERT : ordre réel, connexion, durée, réponses et cas A/B | NON VERIFIE |
| [activity.puml](../../../use_cases/UC-C-14/revisions/R3-CONC/activity.puml) | ACT14-REQ/GARDE/TYPE/REFUS/ROLLBACK/SUCCES : chemins nominal, refus avant archive et échec tardif | NON VERIFIE |
| [class.puml](../../../use_cases/UC-C-14/revisions/R3-CONC/class.puml) | Responsabilités de produced_views, concordance, protection, LibraryNode.save, Treebeard et atomic; pas de service ou table implicite. Les noms de nouveaux helpers restent proposés, sans imposer une copie littérale des noms. | NON VERIFIE |
| [erd.puml](../../../use_cases/UC-C-14/revisions/R3-CONC/erd.puml) | Même schéma, relations et types vérifiés; NoeudArchive/Extremite/Statement/VersionTexte inchangés; aucun mécanisme en mémoire transformé en table | NON VERIFIE |
| [sequence_rollback.puml](../../../use_cases/UC-C-14/revisions/R3-CONC/sequence_rollback.puml) | RB-WRITE/ROLLBACK/REPRISE : annulation T1, libération des verrous concernés et reprise T2 sur état restauré | NON VERIFIE |
| [sequence_multiple.puml](../../../use_cases/UC-C-14/revisions/R3-CONC/sequence_multiple.puml) | MULTI-PLAN/LOCK/REFUS/RB/INDEP : ensembles connus, ordre commun, pas de préfixe conservé, commits indépendants | NON VERIFIE |
| [activity_t2.puml](../../../use_cases/UC-C-14/revisions/R3-CONC/activity_t2.puml) | T2-LOCK/NOINSERT avant COW/captures; branches HTTP/ORM, sauvegarde existante et création neuve distinguées | NON VERIFIE |

Une divergence significative revient en revue avant extension. Ne pas modifier
les diagrammes approuvés pour les aligner après coup sur le code livré.

## 3. Contrôles de conformité et preuves exigées

Tous les contrôles ci-dessous sont **définis mais NON VERIFIES** à ce stade.
La colonne « preuves à fournir » indique une condition future, pas une preuve
déjà disponible.

| ID | Référence / objet | Vérifications du code et preuves à fournir | Essais liés |
|---|---|---|---|
| V01 | §6 analyse; autorisation | Diff limité aux cinq fichiers nommés dans l'attestation; pas de code UC02, pilote A, schéma/migration ou verrouillage général. Empreintes du socle et des patches contrôlées. | T24, contrôle du diff |
| V02 | G01/G02; état exact | Plan B0 et E0 complets avant mutation; égalité d'ensembles, pas d'effectifs. Document, path/depth, item, numéro, paire générique et identité/texte Statement réellement relus. Un nouveau membre, une absence ou une divergence font refuser tout le bloc. | T01/02/03/04/13/20 |
| V03 | G02/G04; acquisition réelle | Requêtes FOR UPDATE effectivement évaluées dans atomic, sans skip_locked; ordre PK des LibraryNode, puis Statement. Même connexion/alias pour verrou, archive, repointage, retrait et transaction externe. SQL/PID/locks observables, pas une simple présence de select_for_update dans le source. | T05/06/12/14/15/19 |
| V04 | G04; durée jusqu'au commit | Verrous conservés durant pre_delete, DELETE SQL et commit HTTP externe. Après RELEASE SAVEPOINT, T2 reste réellement en attente. Aucun succès émis au client avant finalisation; aucun UPDATE T2 validé dans la fenêtre tardive. | T05/06/12 |
| V05 | AC01/02, G02/G09; gardes | Gardes de mutabilité, référents, décisions/cascades, contenu réel et GFK refaites sur les instances protégées; caches GFK/relations/descendants anciens écartés. Pas de fausse lecture de PK Statement homonyme. | T04/06/20/22 |
| V06 | AC03/G03; archive fidèle | Relevé d'état APRÈS acquisition/relecture et AVANT archive comparé champ par champ à l'archive et à l'identité effectivement supprimée : Document, ancien ID, position, item, numéro, Statement vérifié, texte/empreinte disponibles et motif. Structure sans contenu distinguée du Statement vide. | T05/06/19/21 |
| V07 | G03; texte partagé | Statement utilisés stabilisés/revalidés après les nœuds; une modification avant protection est détectée, après protection elle attend. L'archive conserve le texte de l'état retiré; pas de purge ni réécriture des autres usages par UC13. | T19/21/23 |
| V08 | G05; cas A | T2 HTTP ou ORM citation committée après E0 mais avant protection T1 : état changé constaté, refus T1, aucun effet partiel T1; commit et captures/association T2 conservés. | T03/04/13 |
| V09 | G06/G10; HTTP T2 | Barrière et rechargement AVANT captures, nouveau Statement, association et item. Après attente et disparition : 403 lisible sans succès ni effets partiels. 404 initial et 400 de formulaire restent distincts; édition UC13 conserve ses règles. | T05/09/12/23 |
| V10 | G06; instance ORM périmée | Ligne existante requise sous protection; UPDATE seul sans repli INSERT. Tester save sans update_fields, avec update_fields et force_insert sur ancienne instance. Création neuve Treebeard encore possible. | T06/07/08/10/23 |
| V11 | AC06/G07; atomicité T1 | Refus/panne après archive, repointage ou premier retrait : rollback de toutes les archives, extrémités, suppressions et compteurs T1 avant interception HTTP. 403 métier / 500 technique; pas de succès partiel. | T09/10/11/18 |
| V12 | G06/G07/G08; atomicité T2 | Après commit de suppression T1 : T2 annulée sans recréation ni contenu/capture parasite. Après rollback T1 : T2 peut reprendre et valider après ses contrôles. Une transaction distincte committée survit; des actions non committées d'une même T2 sont annulées ensemble. | T05/06/09/10/16/17 |
| V13 | G02/G08; parents Treebeard | Parents de compteurs compris, même hors bloc; API de retrait conservée, parent.save compatible avec la garde existante. numchild évolue légitimement, ne sert pas de faux conflit probatoire; compteurs cohérents après commit/refus et suppressions sœurs. | T11/14/15/23 |
| V14 | G08; plusieurs occurrences | Ensemble connu verrouillé en ordre commun avant mutation; cible manquante/refus = opération entière annulée. Plan changé refusé plutôt qu'étendu tardivement. Deadlock étranger réel : SQLSTATE 40P01, victime et rollback identifiés, pas de retry caché ni promesse d'absence universelle de deadlock. | T13/14/15/16/17/18 |
| V15 | AC04/05/07/G09; histoire | Repointage de toutes les extrémités; retrait des seules identités autorisées du bas vers le haut; gardes ORM existantes conservées. Tous Statement/VersionTexte et anciennes décisions/captures disponibles conservés/consultables; statements_supprimes vide. Citation non archivable refusée. | T01/02/11/21/22 |
| V16 | B01 §4; pouvoir discriminant | Mêmes assertions essentielles et fixtures synthétiques sur témoin f35 et nouveau candidat; T05/T06/T07 échouent par violation de conformité sur témoin et passent sur correctif. SQL/paramètres originaux et gardes conservés; un timeout, import absent ou harnais cassé n'est pas une reproduction. | T05/06/07 |
| V17 | AC/G, UC13/14/15; non-régression | Exécuter les variantes ciblées puis la suite complète du socle, E01/citations P6 et outillage. Compter les tests réellement découverts/exécutés, journaliser échecs/exclusions; ne pas prendre 270/33 comme effectif imposé ni supprimer un oracle pour obtenir le vert. | T01–T24 |

## 4. Registre des essais à compléter pour le candidat

Les ID restent dans l'espace local **UC14-R3-CONC:T01–T24**. Les variantes
du plan approuvé restent exigées; le tableau n'en remplace pas les détails.
Toutes les cellules « nouveau candidat » sont NON EXECUTEES.

| Test | Objet du plan approuvé | Fonction du témoin f35 dans cette campagne | Nouveau candidat |
|---|---|---|---|
| T01 | Compensation d'effectif avec remplacement Statement | Non-régression du B01 initial déjà corrigé | NON EXECUTE |
| T02 | Compensation avec remplacement citation | Même rôle, pas un échec exigé contre f35 | NON EXECUTE |
| T03 | Cas A HTTP avant protection | Contrôle d'ordre A | NON EXECUTE |
| T04 | Cas A ORM citation avant protection | Contrôle d'ordre A | NON EXECUTE |
| T05 | HTTP tardif après garde, avant DELETE | **Échec de conformité discriminant requis** | NON EXECUTE |
| T06 | ORM citation tardif après garde, avant DELETE | **Échec de conformité discriminant requis** | NON EXECUTE |
| T07 | Save périmé sans update_fields après suppression | **Échec de conformité discriminant requis** | NON EXECUTE |
| T08 | update_fields et force_insert sur instance périmée | Contre-épreuves de sauvegarde | NON EXECUTE |
| T09 | Rollback T1 puis reprise HTTP | Atomicité / ordre de reprise | NON EXECUTE |
| T10 | Rollback T1 puis reprise ORM citation | Même contrôle, autre voie d'écriture | NON EXECUTE |
| T11 | Pannes après archive, repointage, premier retrait | Trois points d'injection conservés | NON EXECUTE |
| T12 | Verrous après RELEASE, avant commit externe | Durée réelle, observation distincte | NON EXECUTE |
| T13 | Un descendant changé dans un bloc multiple | Refus entier, conservation T2 | NON EXECUTE |
| T14 | Branches sœurs, parent commun | Compteurs et ordre des protections | NON EXECUTE |
| T15 | Ensembles chevauchants présentés en ordre inverse | Plusieurs cibles, fin bornée | NON EXECUTE |
| T16 | Commit indépendant hors bloc | Conservation du commit indépendant | NON EXECUTE |
| T17 | Deux écritures non committées d'une même T2 | Annulation de l'opération entière | NON EXECUTE |
| T18 | Deadlock étranger réellement provoqué | Traitement de la victime 40P01 | NON EXECUTE |
| T19 | Statement partagé modifié avant/après protection | État exact et attente légitime | NON EXECUTE |
| T20 | Nouveau membre/déplacement visible à B1 | Refus de plan différent; pas fermeture UC02 | NON EXECUTE |
| T21 | Archives vides/structures/positions/extrémités | Fidélité et histoire conservée | NON EXECUTE |
| T22 | Protections, cascades, GFK et types refusés | Refus atomiques et gardes inchangés | NON EXECUTE |
| T23 | COW UC13 et création Treebeard neuve | Compatibilité fonctionnelle | NON EXECUTE |
| T24 | Suites complètes et schéma à sec | Résultats réels, effectifs non présumés | NON EXECUTE |

Pour chaque essai exécuté ultérieurement, ajouter : commande, variante,
empreintes code/test, PostgreSQL et dépendances, PID T1/T2, événements/SQL
observés, assertions, durée/code de sortie, journal et empreinte. Le témoin
et le candidat utilisent les mêmes exigences de conformité; seule la
production change. Un aménagement indispensable du harnais doit être décrit
et ne doit pas changer l'oracle pour le correctif.

Pour les cas B, démarrer T2 dans la fenêtre tardive sans demander son commit
tant que T1 la verrouille. Établir l'attente réelle (PID, verrous et événements),
laisser T1 terminer, puis observer le refus T2. Les bornes d'attente servent
à détecter un test bloqué, jamais à valider la correction. Après rollback T1,
observer séparément la reprise possible de T2. Ne pas neutraliser les gardes
pour forcer un entrelacement.

## 5. Règle de verdict et dossier de preuve

Le relecteur indépendant doit confronter code, vues, assertions et journaux,
et reconstituer/rejouer les essais discriminants sur son banc dans la mesure
nécessaire à son verdict. Le dossier doit contenir un état post-opération
permettant de vérifier archives, extrémités, occurrences, textes/captures et
compteurs, y compris après les refus. Une suite générale verte ne remplace
aucun échec tardif B ni la comparaison des archives.

Un contrôle absent ou non concluant reste non vérifié; un écart prouvé est
signalé avec son impact. Ne prononcer une conformité bornée R3 qu'après
examen d'un candidat identifié et des résultats réels satisfaisant les
contrats. Ne jamais transformer le verdict de conception en verdict du code.
Même un futur verdict favorable ne vaut pas autorisation d'intégration,
de fusion, de migration ou de déploiement.

Le rapport futur distinguera : référence candidate et delta; contrôles de
code effectués; tests réellement exécutés; résultats ancien/nouveau;
garanties démontrées et leurs limites; écarts et points non vérifiés;
réponse explicite sur la levée du défaut résiduel B01 et la conformité C0-A.
L'orphelin tardif sera une réserve séparée, **ni corrigée ni testée par ce
mandat**; aucune voie UC02 ni garantie globale L1-A/C0-B/L5 n'est ajoutée.
