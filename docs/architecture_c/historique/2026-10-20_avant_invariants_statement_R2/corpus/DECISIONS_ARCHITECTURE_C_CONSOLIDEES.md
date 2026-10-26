# Décisions consolidées de l’architecture C

**Registre actif — Agent B. Version initiale du 19 octobre 2026; révision C-UML-2026-10-20-R1.**

Les approbations viennent des mandats utilisateur, jamais de la présence d’une décision dans un rapport. Le mandat « Approbation architecturale et autorisation limitée du lot C0-A » a retenu les orientations D/CF avec leurs conditions; le [mandat du 20 octobre](references/MANDAT_CONSOLIDATION_UML_2026-10-20.md) décide désormais **D05 CHRONO_VERSION** et impose quatre vues UML validées puis approuvées par use case avant implantation.

Changements de cette révision : statuts d’approbation explicités, principe D05 tranché, limites résiduelles R01–R08 identifiées, gouvernance par use case articulée aux lots, évolution locale PHRASE signalée. Contrats complémentaires : [avenant](AVENANT_ARCHITECTURE_C.md). Porte obligatoire : [protocole UML](PROTOCOLE_VALIDATION_UML.md). La [copie exacte antérieure](historique/2026-10-20_avant_consolidation/README.md) préserve l’historique sans devenir une autorité concurrente. Aucun code, schéma ou lot suivant n’est autorisé ici.

Ce document réunit le contrat recommandé, les arbitrages restants et les lots à mandater. Il précise deux points du dernier addendum : la conservation immuable des examens et la transition E01. Il ne reprend pas l’analyse générale des besoins.

## 1. Références, périmètre et décisions à prendre

| Référence | État utilisé pour la consolidation |
|---|---|
| E01 / dépôt courant | `14f7533650d2a28832698b2222ced1df1cd89bb1`; arbre propre au début du mandat. Lecture seule. |
| Cible P6 gouvernante | **`212a7feee81aef46a5b43d36e8eeafe0f8870064`**, donnée par le demandeur et vérifiée dans la référence locale d’intégration. Ce SHA reste intangible dans ce mandat. |
| Premier addendum, D01–D12 | `docs/agent-b-pont-probatoire-20261019`, commit `06fe44c1a7e8582792f9d1fcfcba8155046168ee`, chemin `docs/modele_preuve/ADDENDUM_AGENT_B_NOTE_02_PONT_PROBATOIRE.md`. Lecture par Git, sans changement de branche. |
| Validation fonctionnelle, CF1–CF4 | [VALIDATION_FONCTIONNELLE_ARCHITECTURE_C.md](./VALIDATION_FONCTIONNELLE_ARCHITECTURE_C.md). |
| Audit CF3 / 38 scénarios | [CF3_COMPATIBILITE_CONCORDANCES_E01.md](./CF3_COMPATIBILITE_CONCORDANCES_E01.md). Document conservé tel quel. |
| Continuité | `AGENTS.md`, `PROJECT_CONTEXT.md`, `legal/METHODOLOGIE_POST_DEPOT.md` lus. Archive de juillet intouchable, acte déposé sur papier. Archives non modifiées; politique future CHRONO_VERSION décidée par le mandat actuel, sans réécriture de juillet. |
| Agent A | Plans `PLAN_REGIME_CITATIONS.md`, `BASCULE_REGIME_ETAPE1.md`, README et code du régime lus à la cible P6. L’état de l’essai de récupération et de la bascule réelle n’est pas vérifié sur le serveur. L’information gouvernante est celle du demandeur : ils sont encore préparés par A. |

**Modification recommandée au dernier addendum :** remplacer le champ JSON historique mutable de `Correspondance` par une table enfant `ExamenEditorial`, une ligne immuable par décision. `Correspondance` et ses extrémités demeurent l’unique filiation. Il s’agit d’un support de conservation des examens, pas de la solution 3 créant une seconde filiation. Aucun champ `examens_editoriaux` n’a été implémenté; cette précision ne suppose donc aucune conversion d’un schéma déjà installé.

Les statuts du registre distinguent **approuvée comme orientation** (décision utilisateur, pas réalisation), **conditionnelle** (activation sous préalable nommé), **recommandée pour approbation** (choix non encore décidé) et **arbitrage encore nécessaire**. Le principe D05 est approuvé; ses détails R ne le sont pas automatiquement. Les statuts de dossiers UML sont distincts et figurent au [registre de validation](registre_validation.md). Aucune condition technique n’est présentée comme satisfaite par la seule approbation du contrat.

Les tests sont nommés sans collision : `E01:Txx` = exigences/tests historiques; `C:T01–T22` et `C:N01–N14` = premier addendum; `VF01–VF14` = validation des deux arbres; `NR01–NR12` et `CF3-01–CF3-26` = 38 scénarios du dernier addendum; `IMxx`/`TRxx` = précisions nouvelles de ce document. **Aucun de ces tests n’est exécuté dans ce mandat.**

## 2. Garantie A — Immutabilité des examens

### 2.1 Choix minimal recommandé

Un JSON n’est pas immuable par sa nature. `save()`, des signaux ou un contrôle d’interface ne couvrent pas toutes les écritures : Django confirme notamment que `update()` ne passe pas par `save()` ou ses signaux. [Documentation Django](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#update).

| Option | Garantie nécessaire | Conclusion |
|---|---|---|
| JSON append-only dans Correspondance | Trigger comparant OLD/NEW : ancien tableau préservé comme préfixe exact, ajout validé seulement en fin, contrôle de tous les autres champs, verrou de concurrence, suppression du parent interdite et gestion des valeurs héritées. | Faisable, mais chaque ajout réécrit un même agrégat mutable et mêle évolution de la filiation et conservation des décisions. Aucun avantage décisif pour le besoin présent. |
| **ExamenEditorial enfant immuable** | Une nouvelle ligne par examen; UPDATE/DELETE interdits sans comparaison de préfixes; ajout sérialisé et validé; parent protégé. | **Recommandée.** Même besoin de protections en base, mais règle d’immutabilité plus simple, identité d’examen stable et références historiques directes. |
| JSON avec hashes et audit seulement | Détecte éventuellement une altération après coup; un écrivain peut remplacer texte et hash. | Rejetée : ne garantit pas la conservation demandée. |

Modèle de conservation minimal proposé dans `document_manager` :

| Donnée | Contrat |
|---|---|
| `correspondance` | FK vers Correspondance, suppression protégée dans l’ORM et en SQL. Aucune suppression du parent ne doit emporter les examens. |
| `ordinal` | Rang d’ajout par correspondance; unique `(correspondance, ordinal)`. Ce n’est pas un numéro procédural. |
| `origine` | `EXAMEN_EXPLICITE` ou `RELEVE_HERITE`. Le second ne possède pas la valeur d’un nouvel examen des occurrences. |
| `manifeste` | JSON de format versionné contenant décision/motif, auteur du nouvel examen ou collecteur du relevé identifié, ancien auteur seulement s’il est attesté, date d’enregistrement et date ancienne déclarée si connue, nature et couple, carte des extrémités, versions de texte, textes exacts/empreintes examinés, et informations de provenance disponibles. |
| `empreinte` | SHA-256 canonique du manifeste hors son propre digest. Clés d’objet triées, ordre sémantique des listes conservé, format de dates explicite. |
| `enregistre_le` | Date d’enregistrement effective, posée par la base. Une date historique éventuellement rapportée est un champ distinct; elle ne remplace pas cette date. |

Le manifeste complet conserve l’histoire même si une occurrence est ensuite archivée. Les identifiants y restent qualifiés par modèle, Document et version. Une référence seule ou un hash sans le texte ne suffisent pas. Les captures `VersionTexte` encore utilisées restent également protégées; leur conservation n’est pas confiée aux seules M2M héritées.

Les champs actuels de Correspondance et ses M2M peuvent subsister comme projections de compatibilité. Après un premier examen explicite au nouveau format, le lecteur décisionnel fait autorité depuis cet examen; une divergence de projection est une anomalie, pas une seconde décision concurrente. Les extrémités restent la carte active de filiation; les manifestes en conservent les états examinés. Aucune seconde table de liens SOURCE/CIBLE n’est créée.

### 2.2 Écritures directes, bulk et suppressions

Contrat à réaliser et tester dans une base isolée avant son activation :

1. **Interdire UPDATE et DELETE d’un ExamenEditorial en base**, même en brouillon, y compris ses métadonnées et son manifeste. Corriger une erreur signifie ajouter une nouvelle décision expliquant celle qu’elle remplace; l’ancienne reste lisible. Un trigger de refus s’applique aussi aux chemins ORM/bulk/SQL; une garde Django améliore le message mais ne constitue pas la garantie.
2. **Traiter TRUNCATE séparément**, par retrait du privilège applicatif et garde au niveau instruction. Les triggers de ligne UPDATE/DELETE ne couvrent pas TRUNCATE. Les cascades ou suppressions de parents ne doivent pouvoir ni effacer les examens ni les rendre inaccessibles. Les FK SQL et les gardes portent aussi sur Correspondance et les conteneurs utiles. PostgreSQL distingue précisément ces événements et exécute les triggers dans la transaction concernée. [Comportement des triggers](https://www.postgresql.org/docs/18/trigger-definition.html).
3. **Ne pas donner INSERT libre au rôle applicatif sur les examens.** L’entrée de confirmation appelle une fonction d’ajout contrôlée en base, qui valide la concordance entre le manifeste proposé et les occurrences/textes réellement examinés, alloue le rang et écrit l’examen. Les INSERT/bulk_create directs échouent. Un RELEVE_HERITE utilise une voie distincte, incapable de produire une origine EXAMEN_EXPLICITE ou une certification rétroactive.
4. **Limiter les privilèges de cette fonction** : propriétaire technique distinct du rôle d’exécution, périmètre et chemins SQL fixes, exécution réservée, absence de droit applicatif de désactiver les gardes ou de modifier les tables/fonctions. La fonction n’accorde pas le droit général de modifier l’histoire. Les privilèges sont cumulatifs, donc les héritages de rôles doivent être inclus dans les tests. [Privilèges PostgreSQL](https://www.postgresql.org/docs/current/sql-grant.html). Si `SECURITY DEFINER` est utilisé, fixer un `search_path` sûr, qualifier les objets et restreindre EXECUTE dès la création. [Contrat des fonctions](https://www.postgresql.org/docs/18/sql-createfunction.html#SQL-CREATEFUNCTION-SECURITY).
5. **Ne pas confondre immutabilité et véracité de l’examen.** La base vérifie identités, cohérence des textes et provenance déclarée; elle ne prouve pas qu’un humain a correctement apprécié la reformulation ou la pertinence d’une pièce. L’action explicite et son auteur sont enregistrés par le service. Un administrateur propriétaire/superutilisateur capable de modifier le schéma sort du périmètre de résistance du rôle applicatif. Les sauvegardes et livrables conservés restent nécessaires; aucune inviolabilité absolue n’est annoncée.

Cette proposition ne demande aucune modification actuelle des rôles ou du serveur. La capacité de séparation des rôles est une condition à vérifier sur un environnement d’essai, puis dans un mandat de déploiement séparé. Le JSON avec comparaison de préfixes aurait besoin de protections équivalentes; il ne contourne pas ce préalable.

### 2.3 Concurrence : aucune décision perdue, aucun examen d’un état mélangé

L’ajout reçoit l’ordinal précédent attendu et les empreintes/révisions du précontrôle. L’ordre de verrouillage est commun aux écritures concernées : conteneurs Document/version dans un ordre déterministe, puis Correspondance, occurrences et textes concernés. L’entrée en base relit les données après acquisition des verrous, vérifie le gel propriétaire et les valeurs attendues, construit/valide le manifeste et ajoute l’examen. La mise à jour des projections de compatibilité appartient à la même transaction.

Deux confirmations fondées sur le même état attendu ne se remplacent pas : la première peut réussir; la seconde reçoit un conflit de révision/ordinal et doit être revue. Une contrainte d’unicité seule ne remplace pas ce protocole. Toute écriture concurrente pouvant changer les extrémités ou les textes doit participer au verrou du conteneur, y compris les chemins SQL permis; des gardes en base imposent cette participation. Un simple verrou de Correspondance ne stabiliserait pas le texte d’un Statement modifié ailleurs. Les mécanismes précis de verrouillage doivent être éprouvés dans les deux ordres d’arrivée; un conflit ou interblocage produit un échec transactionnel, jamais une réussite partielle. [Verrous PostgreSQL](https://www.postgresql.org/docs/current/explicit-locking.html).

### 2.4 Immutabilité d’une décision et gel d’une version : deux garanties

| Situation | Décisions conservées | Objets rédactionnels |
|---|---|---|
| Brouillon avec un examen | Examen ancien déjà immuable. Une nouvelle décision peut être ajoutée après revue. | Texte/structure/liens éditables par les services; un changement pertinent rend l’ancien examen inapplicable au courant, sans l’altérer. |
| Destination gelée | Aucun nouvel examen ne peut être ajouté à une relation appartenant au contenu gelé; les examens et leur interprétation historique sont conservés. | Aucun ajout, changement, transfert de parent/version ou suppression dans l’agrégat gelé. Une nouvelle version porte les changements. |
| Source gelée reprise dans un nouveau brouillon | Nouvelle Correspondance et nouvel examen appartenant à la destination, autorisés si les références sont valides. | La source gelée n’est pas modifiée. Sa liste de réutilisations ultérieures est une projection extérieure; elle ne réécrit pas son contenu figé. |

Les gardes d’examen s’appliquent dès leur livraison L1-A. Les protections globales de tous les objets C relèvent de L5 et sont exigées avant tout gel réel. On ne reporte pas l’immutabilité d’un examen déjà utilisé à un futur lot de gel.

## 3. Garantie B — Transition des confirmations E01

### 3.1 Trois dimensions indépendantes

**Décision historique** : ce qui est effectivement conservé (état, date, motif, captures et références disponibles). **Validité actuelle** : ce qui peut être démontré aujourd’hui pour les occurrences/textes réellement portés. **Admissibilité stricte** : satisfaction des critères du nouvel export, dont la provenance de l’examen, plus EX01–EX07. Ces trois réponses peuvent être différentes.

| Situation | Conservation historique | Validité actuelle | Nouvel export strict renforcé | Action |
|---|---|---|---|---|
| Ancienne confirmation sans manifeste, captures présentes et compatibles avec les textes actuels | Conservée telle quelle; relevé daté du jour possible, avec provenance héritée. | Compatibilité textuelle constatée, mais identité complète des extrémités au moment de l’ancien examen **non attestée**. Ce n’est pas une confirmation nouvelle. | Ne suffit pas à satisfaire EX02 au nouveau contrat. Diagnostic « examen hérité sans manifeste ». | Nouvel examen explicite sur la rédaction modifiable si une sortie stricte est demandée. |
| Ancienne confirmation avec capture absente, rôle incohérent, mauvais Statement, texte changé ou occurrence substituée | Décision ancienne conservée avec ses limites; aucune capture manquante inventée. | `A_REEXAMINER` ou anomalie de rattachement; état enregistré ancien inchangé. | Refus. | Revoir la bonne relation et les textes actuels; ajouter une nouvelle décision, pas remplacer l’ancienne. |
| Ancienne occurrence supprimée/archivée | Conserver décision, archive typée et textes disponibles. Type historique inconnu reste inconnu. | Histoire consultable; ne couvre pas automatiquement les occurrences actives. | Pas de couverture actuelle induite; décisions actuelles requises pour le périmètre restant. | Qualifier retrait/ajout/transformation explicitement; ne pas déduire RETRAIT de la suppression physique. |
| Ancien rendu ou contenu effectivement gelé | Fichier/contenu, valeur historique et traces conservés sans régénération. | Sa lecture historique s’appuie sur l’état conservé, pas sur le brouillon actuel. | On peut le relire ou le remettre à l’identique; ce n’est pas un nouvel export strict attestant un examen qui n’existait pas. | Produire une nouvelle version et un nouvel examen pour un nouveau contenu soumis au contrat renforcé. |
| Nouvel examen explicite au format renforcé | Nouvelle ligne, date actuelle, manifeste complet; le relevé hérité reste intact. | Évaluée par correspondance exacte des occurrences, textes, nature, couple et transformation. | Peut satisfaire EX02 si courant; les autres EX restent obligatoires. | Reconfirmation distincte des appuis; aucune union implicite des deux validations. |
| Renumérotation/cote d’affichage seule | Décisions et captures inchangées. | N’invalide pas un examen complet autrement courant. N’améliore pas la provenance d’un examen hérité. | Pas de dispense d’EX02 ou EX04. | Pas de revue de texte pour ce seul affichage; ne pas en tirer une validation rétroactive. |

Le nom `A_REEXAMINER` est un résultat de lecture actuel lorsque le contrôle échoue; le diagnostic de provenance manquante peut s’ajouter sans réécrire l’ancien `etat=CONFIRME`. Une compatibilité textuelle partielle n’est pas renommée arbitrairement « confirmé ». Le contrôle doit vérifier le Statement **porté par l’occurrence**, pas seulement `VersionTexte.est_courante` sur un ancien Statement détaché.

### 3.2 Transition opérationnelle, sans histoire fabriquée

1. Produire un diagnostic sur une copie isolée : identités, champs conservés, captures accessibles, archives, anomalies et provenance disponible. Le relevé décrit sa date de collecte; il ne prétend pas décrire la carte des extrémités à une date ancienne.
2. Ajouter les nouveaux schémas avec états hérités explicites; ne pas remplir des manifestes « anciens » à partir des nœuds actuels. La valeur E01 de nature conserve un profil hérité, pas une preuve du dépôt réel.
3. Avant le premier remplacement d’une projection ancienne, enregistrer un `RELEVE_HERITE` contenant seulement les faits effectivement disponibles. Inconnus et absences restent visibles. Il ne possède aucun ordinal de décision humaine antérieure supposée; son ordinal est celui de son enregistrement dans le nouveau journal.
4. Tout nouvel examen demandé porte sur l’état actuel relu sous verrou, avec date actuelle et action explicite. Le manifeste distingue cette décision du relevé précédent. Aucun état CONFIRME, auteur inconnu ou ancien ensemble de nœuds n’est imputé par migration.
5. Activer le lecteur/strict renforcé par un déploiement explicite, avec diagnostic préalable et liste des réexamens nécessaires. Pas de mode de forçage « admettre les anciens CONFIRME ». L’export diagnostique reste disponible.
6. Les contenus gelés restent immuables : une lacune historique est signalée; elle n’est pas réparée dans leur ancienne version. Les traces anciennes déjà perdues ne sont pas récupérées par reconstruction du présent.

Cette transition exige une approbation explicite car certains nouveaux exports auparavant acceptés par le contrôle incomplet devront demander un réexamen. Ce changement est une restriction documentée de certification actuelle, pas une modification de la décision historique. Il ne bloque pas les sous-lots indépendants ou la bascule de l’Agent A.

## 4. Registre consolidé des décisions

Chaque fiche énonce l’exigence, la recommandation, les rejets, les effets et les tests. Les suites de tests s’entendent toujours comme à exécuter dans les lots indiqués plus loin.
### D01 — Architecture C et cardinalité

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Plusieurs appuis, complets ou partiels, d’une proposition ou d’un groupe.
- **Solution recommandée :** C : 0..N UtilisationPreuve par cible, une Preuve par utilisation et 1..N sélections par usage valide.
- **Alternatives rejetées :** A avec Demonstration 0..1 et B avec supports arborescents obligatoires : responsabilités et synchronisations supplémentaires sans opération nécessaire.
- **Modèles et services :** Créer Preuve/NoeudPreuve, UP/SelectionPreuve; aucune conclusion ou proposition concurrente dans la preuve.
- **Acceptation :** C:T06–T08/T12/T21; VF11/VF13; CF3-08/12/24.

### D02 — Appuis collectifs et supports projetés

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Appui propre à un groupe et navigation de l’éditeur.
- **Solution recommandée :** Cibles STATEMENT ou REGROUPEMENT; SUPPORT projeté, identifié par UP.pk.
- **Alternatives rejetées :** Héritage automatique des enfants; SUPPORT physique obligatoire créant des contraintes Treebeard sans besoin démontré.
- **Modèles et services :** Aucune seconde table d’appuis. Un support physique éventuel exige une nouvelle décision, lien unique et parent=cible; il est hors premier développement.
- **Acceptation :** C:T08/T15/T20; VF03; CF3-07/12.

### D03 — Structure récursive et numérotation

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Rédaction à profondeurs variables, numéros propres aux occurrences.
- **Solution recommandée :** Nature structurelle, rôle éditorial et présentation indépendants; compteur principal commun aux profondeurs du nouveau profil.
- **Alternatives rejetées :** Sémantique déduite de depth/item/titre, numérotation d’un bloc isolé ou d’un Statement partagé.
- **Modèles et services :** Étendre Document/LibraryNode avec défaut LEGACY; résolveur commun, AUTO/STORED préservés; index complet avant filtrage.
- **Acceptation :** C:T01–T05/T22; E01:T05–T10/T17; NR02; CF3-21.

### D04 — Unité de fragment d’un acte

**Statut : unité de l’occurrence complète retenue par l’utilisateur; détails de sous-cotation conditionnels à R04.**

- **Exigence :** Citer et réutiliser un paragraphe source complet sans créer de pièces par phrase.
- **Solution recommandée :** Occurrence LibraryNode complète comme fragment; sous-cote par ordre source parmi les fragments sélectionnés; numéro imprimé conservé comme repère distinct.
- **Alternatives rejetées :** Sous-cote égale automatiquement au numéro source; plage/composition comme identité de fragment, instable avec les recouvrements.
- **Modèles et services :** Adaptateur d’acte et fragment_key par occurrence; plusieurs usages/compositions réutilisent la même identité. Le principe D05 est décidé; l’affectation et la notation des sous-cotes actives attendent la décision résiduelle R04.
- **Acceptation :** C:T09/T11/T12; C:N09; CF3-24.

### D05 — Politique des cotes futures

**Statut : APPROUVÉE UTILISATEUR — principe CHRONO_VERSION, mandat du 20 octobre 2026 §2.**

- **Exigence :** Coter les pièces effectivement retenues dans chaque nouvelle version sans réécrire juillet.
- **Solution décidée :** Recalcul chronologique du brouillon; associations `(version, pièce, composition, cote)` immuables après gel. La cote est locale à sa version. Une nouvelle version peut attribuer une autre cote à la même pièce.
- **Alternatives écartées pour les nouvelles versions :** permanence globale des libellés et double cotation active imposée. Aucune réaffectation historique n’est autorisée.
- **Modèles et services :** ResultatVersion unique; références actives contextualisées; conservation des compositions, paramètres et artefacts; concordance documentaire depuis les états figés. Les responsabilités ne prescrivent pas des tables supplémentaires sans ERD justifié.
- **Conditions restantes :** R01–R04 pour identité/composition, dates et sous-cotes, R05 pour le périmètre produit; détails dans l’[avenant §§2–4 et 7](AVENANT_ARCHITECTURE_C.md). L’approbation du principe ne tranche pas ces choix et n’autorise pas le code.
- **Acceptation :** C:T16; C:N09/N10; E01:T24–T28; NR08; CF3-24; EPIC-V2:T01–T14 selon le parcours, C-UML:N02/N04–N10/N15/N16. Scénarios à tracer, pas déclarés exécutés ici.

### D06 — Dates, précision et ambiguïtés

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Bordereau déterministe fondé sur les pièces effectivement sélectionnées.
- **Solution recommandée :** Dates métier vérifiées et précision explicite; heure normalisée si fiable; jour seul sans heure inventée; atemporelle explicitement qualifiée; A_DATER bloque le strict.
- **Alternatives rejetées :** saved_at/uploaded_at/created_at comme repli silencieux; date sentinelle prise pour une pièce ancienne; ordre SQL comme départage.
- **Modèles et services :** Contrat des adaptateurs et ResultatVersion avec diagnostics; identité qualifiée pour départager les égalités.
- **Acceptation :** C:N02/N07/N10; E01:T25/T26; NR08; CF3-24.

### D07 — Fidélité des actes reproduits

**Statut : conditionnelle.**

- **Exigence :** Rendre le passage exact d’un acte dont le texte et les numéros font preuve.
- **Solution recommandée :** Vérification par occurrence et original/scan, trace de certification propre à l’acte.
- **Alternatives rejetées :** Assimilation d’un paragraphe d’acte à Quote PHRASE; transcription de travail réputée conforme par défaut.
- **Modèles et services :** CertificationPassageActe append-only; contrôle des textes, numéros, structure et original. Activation stricte conditionnée à la vérification réelle des sources.
- **Acceptation :** C:T09/T14; C:N01/N14; contrôles de sources L3/L6.

### D08 — Gel complet et cohérent

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Conserver exactement la version produite ou communiquée, et isoler les versions suivantes.
- **Solution recommandée :** Un ContenuVersionFige canonique, livrables sous URI immuables, gardes en base et stockage contrôlé, finalisation transactionnelle après recontrôle.
- **Alternatives rejetées :** Instantané/hash seul réputé interdire les écritures; recalcul des cotes ou citations vivantes pour relire une version ancienne.
- **Modèles et services :** Verrous Document/VersionActe/Preuve et relations; captures des textes, examens, liens, usages, fragments et rendus; insertion d’un événement de transmission séparée du gel.
- **Acceptation :** C:T16/T20; C:N06/N08/N11–N14; VF08; NR01/12; CF3-16–19/25; IM05/07.

### D09 — Forme des unités

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Explorer des rédactions différentes sans imposer un plan narratif.
- **Solution recommandée :** Observation/Réfutation comme convention de profil facultative.
- **Alternatives rejetées :** Schéma universel obligatoire ou rôle éditorial décidé par un intitulé libre.
- **Modèles et services :** Bibliothèque neutre de rôles et présentations; propositions sans UP permises; pas de champ de vérité automatique.
- **Acceptation :** C:T01/T02/T05; VF12; CF3-13.

### D10 — Chevauchements et transformations de texte

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Restituer exactement les citations et les insertions sans assemblage ambigu.
- **Solution recommandée :** Refus strict initial des PHRASE chevauchantes ambiguës/discordantes et des remplacements rédactionnels recouvrants; ordre explicite des insertions au même point.
- **Alternatives rejetées :** Fusion/troncature automatique de phrases; maintien d’offsets après réécriture; remplacement global de nombres/cotes.
- **Modèles et services :** Validation des compositions et InsertionRendu ancrées sur VersionTexte; texte source échappé, emphases structurées, omissions explicites.
- **Acceptation :** C:T09–T11/T18; C:N03–N05; VF04; CF3-10/11.

### D11 — Appui simple uniforme

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Une citation seule doit utiliser le même contrat de sélection et de gel.
- **Solution recommandée :** Preuve atomique produite au besoin par le service, puis UP et sélection, même pour une source unique.
- **Alternatives rejetées :** Raccourci GFK direct depuis le paragraphe créant une seconde autorité d’appui.
- **Modèles et services :** Service d’appui simple dans proof_manager; réutilisation de la source, pas duplication d’Email/PDF/Quote.
- **Acceptation :** C:T06/T07/T21; VF13; CF3-08/24.

### D12 — Frontières des modules et périmètre

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Conserver une rive rédactionnelle neutre et une rive probatoire indépendante des anciens raisonnements.
- **Solution recommandée :** document_manager pour occurrences/textes/filiation; act_manager neutre pour Acte/VersionActe et conservation; proof_manager pour organisation/sélections/rendu probatoire.
- **Alternatives rejetées :** Import de proof_manager dans document_manager; conversion automatique de TrameNarrative/ConfirmationAppui; DAG d’inférence ou renvois récursifs entre preuves.
- **Modèles et services :** Réutiliser Cause; distinguer origine d’une source et cause d’usage. Aucune nouvelle version de source créée par la version d’un acte; copie entière de preuve si nécessaire.
- **Acceptation :** Tests de dépendances des modules L1/L2; C:T17; VF05; CF3-12/26.

### CF1 — Analyse interne versionnée

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Analyse danse/garderie avec propres usages, rédaction et gel volontaire.
- **Solution recommandée :** Nature ANALYSE_INTERNE dans le même Acte/VersionActe; un Document PRODUCED propre par version; gel sans dépôt ni transmission.
- **Alternatives rejetées :** Document sans contexte recevant une UP à version inventée; architecture parallèle pour analyses; transmission fictive pour satisfaire E01.
- **Modèles et services :** Étendre les catégories du conteneur neutre, sans nouvelle famille documentaire; contexte de cause explicitement identifié selon le périmètre retenu.
- **Acceptation :** VF01/VF08; CF3-01/02/16/23.

### CF2 — Liens rédactionnels déclarés

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Navigation et suivi des prémisses expressément invoquées.
- **Solution recommandée :** LienRedactionnel entre occurrences : RENVOI ou DEPENDANCE_DECLAREE; textes examinés par occurrence; dépendance externe stricte vers version gelée ou prémisse reprise.
- **Alternatives rejetées :** Déduire une dépendance de sources communes; utiliser Correspondance pour une inférence; union transitive des appuis.
- **Modèles et services :** FK d’occurrences, contrôle de fraîcheur, projection de renvoi; interdire cycles de dépendances déclarées, y compris liens à revoir, sous sérialisation commune; renvois réciproques permis.
- **Acceptation :** VF05–VF11; CF3-12/14–18/21; tests de concurrence VF10.

### CF3 — Reprise partielle

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Reprendre des passages entre analyses/demande, sans modifier l’original ni perdre le contexte.
- **Solution recommandée :** reprendre_sous_arbre avec plan explicite et copie atomique : occurrences nouvelles, usages choisis, réserves/prémisses/liens/insertions traités explicitement.
- **Alternatives rejetées :** Déplacement des nœuds source; copie de tout le dossier d’appuis; absence de sélection interprétée comme RETRAIT E01.
- **Modèles et services :** Réutiliser Correspondance qualifiée; carte N:M par couple; détachement avant réécriture; point d’orchestration probatoire en L2.
- **Acceptation :** VF02/03/04/05/08; CF3-01–26; NR03/07/11/12.

### CF4 — Photos avec contenant Event

**Statut : conditionnelle.**

- **Exigence :** Invoquer seulement des photos pertinentes d’un événement composé.
- **Solution recommandée :** Feuille Photo avec Event explicitement désigné; valider l’appartenance; Event comme pièce, photos comme fragments utilisés.
- **Alternatives rejetées :** Nettoyer/modifier l’Event source; sélectionner Event entier puis filtrer ses photos en silence; prendre le premier contenant M2M.
- **Modèles et services :** Expliciter l’adaptateur Photo→Event avec les champs de contenant déjà proposés; ordre du contenant et dates vérifiés, pas de nouveau modèle de copie.
- **Acceptation :** VF14; C:N07; CF3-08/24/26.

### CF3-D1 — Une filiation qualifiée

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Distinguer juillet→version, révision d’un acte et reprise interdocumentaire après relecture.
- **Solution recommandée :** Solution 2, nature E01 / REVISION_ACTE / REPRISE_DOCUMENTAIRE; lectures filtrées par nature et couple.
- **Alternatives rejetées :** Qualification implicite par titre/source_type; nouvelle filiation concurrente sans invariant incompatible démontré.
- **Modèles et services :** Ajouter nature à Correspondance; conserver SOURCE/CIBLE et groupes; appuis_dorigine reste un lecteur historique scoped; rapport CF3 distinct.
- **Acceptation :** NR04/07/08/09/10; CF3-01/02/05/06/26.

### CF3-D2 — Examens immuables et transition

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Conserver la décision et les occurrences examinées, résister aux écritures directes et éviter la rétrovalidation.
- **Solution recommandée :** ExamenEditorial immuable, fonction d’ajout sérialisée, manifestes complets, RELEVE_HERITE séparé et nouvel examen daté du jour.
- **Alternatives rejetées :** JSON mutable ou hashes seuls; backfill d’un ancien examen depuis le présent; sets de textes pris pour une carte d’occurrences.
- **Modèles et services :** Précision nouvelle par rapport au dernier addendum : une table enfant d’examens remplace le champ JSON historique; projections héritées sans autorité concurrente; garanties §§2–3.
- **Acceptation :** NR03/06/10/12; CF3-03/20/22; IM01–IM08; TR01–TR06.

### CF3-D3 — Plan et contexte de reprise

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Empêcher l’omission silencieuse des limites, prémisses ou appuis de groupes.
- **Solution recommandée :** Sous-arbre et réserves inclus par défaut; omissions motivées; candidats d’ancêtres hors bloc décidés avant application; groupes exacts par couple.
- **Alternatives rejetées :** Détection sémantique prétendument exhaustive; union automatique des usages; groupe cartésien représentant des filières indépendantes.
- **Modèles et services :** DTO/plan de service avec empreintes de précontrôle; aucune table d’opération multi-document nécessaire; attributions destination explicites.
- **Acceptation :** VF02/03/05; CF3-05–09/12–15/22/23.

### CF3-D4 — Édition et archives fiables

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Détacher sans altérer la source et conserver les textes et décisions après suppression.
- **Solution recommandée :** Raccorder les vues aux services; capturer avant réécriture; NoeudArchive.type_contenu qualifié, inconnu historique explicite; protéger histoire et conteneurs utiles.
- **Alternatives rejetées :** Écriture directe dans un Statement partagé; purge CASCADE des examens; object_id considéré comme Statement.pk sans type.
- **Modèles et services :** Garder la suppression physique PRODUCED lorsque l’histoire reste lisible; refuser bloc protégé en totalité; gardes ORM et en base au niveau nécessaire.
- **Acceptation :** NR01/03/05/11/12; CF3-03/19/23/25/26; IM03/07.

### CF3-D5 — Propriété du gel de filiation

**Statut : approuvée comme orientation par le mandat utilisateur antérieur; implantation soumise aux dossiers UML et lots autorisés.**

- **Exigence :** Reprendre une analyse gelée sans modifier son histoire, geler la destination indépendamment.
- **Solution recommandée :** Relation/examens entrants conservés avec la destination; nouvelle relation vers source gelée possible; lecture historique depuis le contenu figé.
- **Alternatives rejetées :** Interdiction de toute réutilisation d’une source gelée; dénouage ultérieur d’une relation déjà incluse dans un gel.
- **Modèles et services :** Gardes sur ancien et nouveau propriétaire, création d’examens comprise; nouvelle version nécessaire pour actualiser un contenu gelé.
- **Acceptation :** VF08; CF3-16–19/25; IM05/07.

### CF3-D6 — Lots, intégration et acceptation

**Statut : découpage accepté comme plan par l’utilisateur; aucun lot suivant automatiquement autorisé, quatre vues UML approuvées par use case désormais préalables.**

- **Exigence :** Développer C sans perturber la récupération/bascule de A ni confondre primitives et solution complète.
- **Solution recommandée :** Lots et paliers §§7–9; 38 scénarios conservés; travail isolé depuis P6, intégration différée et validation propre à C.
- **Alternatives rejetées :** Insérer des commits/migrations C dans la cible P6; déclarer CF3 complet avec L1 seul; réutiliser le retour arrière A comme plan global de C.
- **Modèles et services :** Activation conditionnée aux sorties des lots, capacités PHRASE disponibles et validation d’intégration; aucun déploiement implicite.
- **Acceptation :** 38 scénarios en §8; C:T19; invariants A/B de l’Agent A; IM/TR et récupération C.

## 5. D05 décidée et portée des détails restant à arbitrer

Le [mandat utilisateur §2](references/MANDAT_CONSOLIDATION_UML_2026-10-20.md) tranche **CHRONO_VERSION** pour chaque nouvelle version d’acte. La permanence globale n’est plus une alternative ouverte pour ces nouveaux bordereaux. Les associations historiques de juillet restent intactes et leur verrou n’est pas modifié.

Le choix est une exception explicite à la portée des anciens textes méthodologiques. La règle P-107 demeure celle du registre historique; elle ne devient pas le compteur global des nouveaux bordereaux. Une référence active et un fichier produit sont qualifiés par leur version. Les cotes littérales historiques ne sont pas réécrites.

Il reste à spécifier ou décider les détails R01–R08 de l’[avenant](AVENANT_ARCHITECTURE_C.md), sans rouvrir le principe : identité/composition, déduplication, dates des composites et précision, sous-cotes, usages analytiques/produits, parcours de brouillon, promesse de régénération et stockage/récupération. Ces réserves bloquent les chemins concernés, pas la conception ni les corrections E01 indépendantes.

L’historique des options examinées le 19 octobre est conservé dans la copie antérieure. L’existence de tests E01, les anciens diagrammes et une validation isolée ne valent toujours ni approbation des dossiers UML actuels ni autorisation de lot.

## 6. Contrat commun des modèles, services et invariants

### 6.1 Une autorité par responsabilité

| Responsabilité | Autorité recommandée | Limite |
|---|---|---|
| Proposition, conclusion, prémisse, réserve | Statement dans son occurrence LibraryNode rédactionnelle | Preuve ne contient pas une copie concurrente des conclusions. `is_true`/`is_falsifiable` ne valent pas examen. |
| Identité du document et de sa version | Acte/VersionActe neutres; Document propre à chaque version | Pas de fausse version source ou de transmission fictive pour une analyse. |
| Organisation des éléments | Preuve/NoeudPreuve, arbre simple | Pas de renvoi entre preuves ni moteur d’inférence. Seuls les groupes portent des enfants. |
| Rattachement documentaire | UtilisationPreuve/SelectionPreuve | Un usage n’est pas une déclaration de vérité. Ni parenté, ni filiation, ni dépendance ne crée ses sélections. |
| Filiation active | Correspondance qualifiée et ses extrémités | Un couple de Documents par groupe; nouvelles occurrences pour une reprise. |
| Décisions éditoriales conservées | ExamenEditorial immuable | Ne crée ni confirmation probatoire, ni décision passée manquante. |
| Dépendance/renvoi déclaré | LienRedactionnel | Contrôle de texte et de cible, sans calcul de validité logique. |
| Citation et emplacement | CompositionCitation/segments; InsertionRendu | Adaptateur pour le verbatim, sélection pour l’appui, VersionTexte pour l’emplacement : fonctions distinctes. |
| Pièces, fragments, numéros et cotes du résultat | Un ResultatVersion central, profil explicite | Aucune cotation indépendante par thème, format ou exportateur; D05 CHRONO_VERSION décidée, détails résiduels à approuver pour le chemin concerné. |
| Histoire gelée et fichiers | Un ContenuVersionFige; LivrableVersion immuables | Pas de reconstruction depuis les relations vivantes pour lire l’histoire. |
| Origine des pièces et certification PHRASE | Fournisseurs documentaires / contrat de l’Agent A | C ne certifie pas une PHRASE à leur place et ne modifie pas leurs gestionnaires hérités. |

Les modèles détaillés du premier addendum sont conservés dans ce périmètre : CertificationPassageActe pour les actes, composants de bordereau dans le contenu canonique, LivrableVersion et événements de transmission séparés. Les exceptions historiques de pièces (CONTIENT/EQUIVALENCE_VALIDEE) restent distinctes de la filiation rédactionnelle Correspondance : elles relient des unités documentaires, pas des propositions. Cause existante réutilisée; pas de nouvelle table de causes. La concordance de pièces ne modifie pas AppuiDepotJuillet ni les sources pour faire correspondre deux libellés.

### 6.2 Invariants d’acceptation transversaux

| ID | Invariant |
|---|---|
| INV01 — Provenance | Source par modèle qualifié + PK, original et empreintes utiles; contenant explicite si plusieurs possibles. Ni texte semblable ni date égale ne déduplique deux sources. |
| INV02 — Sélection | Développer uniquement les racines/branches/feuilles sélectionnées par les usages de la version. Source entière et fragment n’inscrivent pas deux fois la même unité résolue; conserver tous les chemins d’usage. Pour les assemblages autonomes, ne pas fusionner toutes les pièces sur leur seule source commune : identité/composition selon l’avenant §3, R01/R02. |
| INV03 — Contexte | Usage d’ancêtre hors bloc, réserve et prémisse extérieure ont un devenir explicite dans le plan. Aucune prétention à détecter automatiquement toute réserve implicite d’une prose. |
| INV04 — Citation | Verbatim issu du fournisseur, certification effectivement valable au moment du nouveau rendu, littéraux historiques intacts; pas de remplacement global de cotes dans Statement.text. |
| INV05 — Ancrage rédactionnel | Insertion sur la bonne occurrence, le Statement actuellement porté et sa VersionTexte, indices Python [start,end); changement du texte/rattachement impose réancrage. |
| INV06 — Numérotation | Résolution sur le Document entier puis filtrage; PK d’occurrence comme identité. LEGACY et STORED inchangés par défaut; numéro imprimé jamais déduit d’un numéro de travail. |
| INV07 — Cotation | Identité documentaire séparée du libellé; politique et version de bordereau explicites, dates métier/précisions vérifiées. D05 non contourné. |
| INV08 — Reprise | Nouvelles occurrences et usages destination; sources préservées; partage de Statement seulement sous détachement fiable sur toutes les voies; texte capturé avant modification. |
| INV09 — Filiation | Nature et couple persistants; groupes N:M exacts. Une transformation collective ne devient pas la preuve de toutes les filières d’un lot disparate. |
| INV10 — Examen | Manifestes par occurrence, deux côtés, qualification et textes. Décision immuable; modification pertinente invalide son application au courant. Numéro/cote d’affichage seuls ne changent pas l’examen. |
| INV11 — Archive | Une extrémité vivante XOR archive cohérente; type conservé pour les nouvelles archives. Absence/type historique inconnu diagnostiqués; aucune perte par CASCADE ou purge de captures utiles. |
| INV12 — Gel | Vérifier l’ancien et le nouveau périmètre propriétaire pour tout ajout/changement/suppression, y compris bulk et changement de parent/version. Préuve entière verrouillée si engagée dans un gel; nouvelle copie pour la modifier dans un autre périmètre. |
| INV13 — Conservation | Contenu et fichiers réellement utilisés capturés avec textes, numéros, cotes, examens, liens, sélections, certifications, algorithmes et ressources. Fichier absent ou état concurrent changé : pas de gel achevé. |
| INV14 — Isolation A | HERITE reste invisible au flux PHRASE strict et PHRASE aux consommateurs hérités selon le contrat A. Une GFK ou des PK brutes n’autorisent aucun contournement. Aucun changement de régime implicite. |

Pour le premier profil de tri proposé par D06, fixer le fuseau de comparaison dans le profil : instants fiables normalisés, date de précision JOUR classée avant les instants connus de cette journée, sans lui attribuer une heure probatoire. Départage ensuite par modèle qualifié et PK; atemporelles explicitement qualifiées après les pièces datées. Une date plus vague qu’un jour ou un fuseau nécessaire non déterminé reste bloquant pour le strict du premier profil. Le résultat conserve toujours la précision et la provenance de la date.

Le service de reprise orchestre les primitives neutres et les choix probatoires dans une transaction; document_manager n’importe pas proof_manager. Les compositions/insertions choisies qui ne sont pas encore disponibles dans un lot ne sont pas silencieusement omises : le plan complet reste refusé ou explicitement limité au périmètre livré. Une sélection de racine dans une preuve partagée ne peut pas changer en place ce que d’autres versions sélectionnent; copier l’arbre entier et repointer uniquement les usages choisis.

Le gel prépare les livrables, acquiert les verrous et recontrôle les entrées, stabilise les représentations lues, vérifie le stockage immuable, puis crée le contenu unique et pose les verrous en transaction. Une panne peut laisser un candidat orphelin, jamais une version gelée pointant vers un fichier absent. La finalisation répétée retrouve le même contenu ou refuse une divergence; elle ne remplace pas un gel. Corriger une transcription dérivée ne versionne pas l’Email/PDF d’origine et ne réécrit pas un rendu ancien; le nouveau rendu strict recontrôle le fournisseur.

## 7. Plan opérationnel et dépendances

### 7.1 Lots à mandater

Aucun lot n’est lancé ici. « Avant A réel » indique une indépendance technique possible sur **un checkout et une base jetable distincts**, sans intervention sur les ressources de A. Cela n’autorise ni déploiement anticipé ni contournement du processus : C0-A n’est pas atterri, le lot suivant n’est pas ouvert. La conception peut avancer; l’implantation demande les quatre vues approuvées des use cases concernés et un mandat de lot. Le détail de cette nouvelle porte figure dans le protocole.

| Lot | Livraison et limites | Préalables / dépendances | Acceptation et tests | Avant A réel? |
|---|---|---|---|---|
| **C0-A — Corrections E01 sans schéma** | Détachement par les vues; capture avant édition; suppression par service; fraîcheur par occurrence/Statement; appuis historiques restreints au couple et type vérifié; protection des captures encore nécessaires. Aucun nouveau champ ou journal. | Mandat limité; checkout indépendant au SHA P6; configuration de test synthétique sans accès réel. | Contre-exemples de NR03/07/11, absence de perte de captures; anciennes suites E01 et régime sans changement d’attentes arbitraire. Ne certifie pas encore l’historique complet des examens. | **Oui**, premier lot proposé. |
| **L1-A — Contexte et conservation neutres** | Acte/VersionActe et analyse interne; Correspondance.nature, ExamenEditorial, archive typée; API d’examen, fonction d’ajout et gardes locales d’immutabilité; protection des captures. | D12/CF1/CF3-D1/D2/D4 approuvés; C0-A; droits/gardes éprouvés sur PostgreSQL de test. Nouvelles migrations uniquement sur la branche future dédiée. | NR10, CF3-20, IM01–IM08; nouveaux champs avec défauts historiques explicites; aucun manifeste ancien inventé. Refus des mutations du journal via SQL/ORM et des ajouts périmés. | **Oui**. Ne touche pas aux migrations 0009 de A. |
| **C0-B — Adoption E01 du contrat renforcé** | Lecteurs filtrés nature/couple; confirmation via examens immuables; projections héritées; archives dans les restitutions; diagnostic de transition et EX02 renforcé. | L1-A; CF3-D2/transition approuvés. Les nouvelles colonnes ne sont pas requises par le code de production avant une migration future autorisée. | NR04–NR10/NR12, TR01–TR06; EX01–EX07 conservés, diagnostics disponibles; ancien rendu inchangé; réexamens exigés clairement listés. | **Oui**, sur copie de test seulement. |
| **L1-B — Structure, liens et reprise rédactionnelle** | Profil récursif, index commun, rôle/présentation; LienRedactionnel; copie neutre de texte/occurrences et carte N:M, réserves/prémisses/liens explicités. Pas d’UP. | D03/D09/CF2/CF3-D3 approuvés; C0-A; APIs L1-A pour filiation/examens. | C:T01–T05/T22, VF06/07/09/10, NR02, CF3-03/04/05/13/14/15/21. Non-régression LEGACY/STORED et des sorties historiques. | **Oui**. |
| **L2 — Organisation et utilisations de preuves** | Preuve/NoeudPreuve; UP/SelectionPreuve; appuis de groupe, preuve atomique, copie entière et repointage; orchestration CF3 complète hors rendus encore indisponibles. | D01/D02/D11; CF1; L1-A/B. Sortie exige C0-B et cohérence des frontières de modules. | C:T06–T08/T12/T17/T20/T21; VF02/03/05/11–14; CF3-01/02/06–09/12/22/23. Application atomique, usages et sélections exacts, aucun import automatique d’appuis. | **Oui**, avec types de test / sources non PHRASE. |
| **L3-A — Adaptateurs et résultat documentaire** | Identités, contenants, fragments, datation, certification des actes; Photo→Event; ResultatVersion unique; correspondance de pièces, tri déterministe. Affectation officielle des cotes séparée. | L2; D04/D06/D07/CF4 pour les capacités activées. Contrats de sources et originaux vérifiés pour le strict réel. | C:N01/N02/N07/N09/N10/N14, VF14; CF3-08/24/26. Exactement les pièces des usages, fragment unique avec tous ses chemins; source absente/ambiguë refusée. | **Oui** hors certification PHRASE réelle et sans cotation officielle non arbitrée. |
| **L3-B — Fournisseur PHRASE** | Adaptateur du fournisseur de l’étape 2; contrôles de régime, bornes, trois empreintes, certification effective; navigation contextuelle nouvelle. Ne crée ni ne migre les citations de A. | Contrat A étape 2 disponible et versionné sur environnement isolé; D07 ne remplace pas ce contrat. L3-A; validation commune d’interface. | C:T14/T19, C:N03/N04/N14; CF3-26; témoins HERITE refusés, PHRASE de test altérée immédiatement refusée, ancien système toujours isolé. | Contrats/doubles **oui**; connexion réelle au fournisseur seulement quand sa capacité existe, sans attendre nécessairement des PHRASE réelles en production. |
| **L4 — Compositions, insertions et rendus** | Segments composites, omissions, emphases, répétitions, offsets/reprises, affichages éditeur/clean/PDF cohérents. | L1/L2, D10; résultat L3-A. Sous-lot rendu avec doubles/non-PHRASE autonome; activation PHRASE dépend L3-B; cotes procédurales dépendent D05. | C:T09–T15/T18/T22; C:N04/N05; VF04; CF3-10/11/24. Même résultat dans toutes les sorties, littéraux intacts, texte changé → réancrage. | **Oui** pour le moteur et les types disponibles. |
| **L5 — Gel et protections globales** | Contenu canonique, fichiers immuables, verrous complets, propriétés du gel des relations/examens, clones et références externes; tests SQL/bulk et panne/concurrence. | D08/CF3-D5; L1–L4 pour le périmètre gelé; stockage et stabilisation des fournisseurs; politique de cotes approuvée pour le profil officiel. | C:T16/T20, C:N06/N08/N11–N14; VF08; CF3-16–19/25; IM05/07. Aucun premier gel réel avant réussite des gardes et du protocole. | **Oui** pour développement/tests; pas de gel réel ni intervention chez A. |
| **L6 — Intégration et validation complète** | Intégration future des développements sur le socle livré par A; concordances historique rédactionnelle et documentaire; reprise contrôlée et démonstration de bout en bout; récupération C. | A clôture et récupérabilité confirmées; nouvelle référence d’intégration explicitement autorisée; L1–L5, D05 et sources réelles contrôlées pour le résultat officiel. | Revalidation des **38** scénarios, suites E01/A, C:T01–T22/C:N01–N14, VF01–VF14 et IM/TR; différences autorisées identifiées; historique/fichiers inchangés. Aucun nouvel usage réel par simple succès sur fixtures. | Préparation/doubles oui; intégration/déploiement réels **différés** et à mandater séparément. |

Dépendance principale : **C0-A → L1-A → C0-B**, avec **L1-B → L2 → L3-A/L4 → L5 → L6**. L1-B utilise le socle L1-A; sa préparation de structure peut avancer séparément de l’adoption E01 C0-B. L2 peut préparer ses arbres/sélections sur les APIs neutres, mais ne déclare pas CF3 accepté avant les sorties L1/C0-B. L3-B est une dépendance de la capacité PHRASE, pas de tous les autres adaptateurs ou du moteur de rendu. D05 est décidée; ses détails résiduels et les dossiers UML bloquent seulement les chemins concernés. Les règles d’atterrissage des lots et d’approbation des dossiers s’ajoutent à ces dépendances techniques.

### 7.2 Sous-lots réellement indépendants de la bascule

Peuvent avancer avec des contrats/données synthétiques : C0-A, journal neutre et archives, contexte d’analyse CF1, profil récursif et index, liens CF2, copie de texte, arbres de preuve, sélection/portée, résolution d’identités, composition de passages d’actes et moteur de rendu, stockage/gel simulé. Les tests peuvent contenir des doubles PHRASE conformes au contrat; ils ne sont pas une preuve de certification d’une vraie citation.

Attendent une capacité distincte : lecture d’une PHRASE effectivement certifiée par l’étape 2, contrôles d’intégration de ses mutations, vérification des originaux réels pour un rendu probatoire et intégration sur le socle de production livré. **La bascule de l’étape 1 ne fournit pas les bornes/certifications de l’étape 2.** Aucun sous-lot C ne doit les ajouter opportunément aux migrations de l’étape 1.

## 8. Tests conservés et affectation aux lots

### 8.1 Les 38 scénarios du dernier addendum

Les quatre colonnes de contrôle ci-dessous sont reprises **sans modification** du dernier addendum. Seules l’affectation aux lots et la mention de revalidation sont ajoutées. Les manifestes qu’elles demandent sont désormais conservés dans ExamenEditorial selon §2. La perte éventuelle d’un schéma lors d’un retour de migration mentionnée dans NR10 n’autorise pas à effacer un journal réel : ce test reste limité à une base jetable; après usage réel, une récupération conserve les examens et exige un plan séparé.

**Statut de chacune des 38 lignes : NON EXÉCUTÉ dans ce mandat.** « Lot principal » désigne la livraison responsable du contrôle; les variantes exigeant le gel global ou un fournisseur indisponible ne sont acceptées qu’aux lots de revalidation indiqués. Les précontrôles partiels en C0-A ne suffisent pas à accepter les lignes complètes qui attendent le nouveau schéma.

| ID | Référence/scénario conservé | Contrôle positif conservé | Contre-épreuve conservée | Lot principal | Revalidation |
|---|---|---|---|---|---|
| NR01 | C02/C09; T02 dans `document_manager/test_e01_numerotation.py:477` | Référent PRODUCED ou REPRODUCED protégé; création d’un lien E01 possible avant T01, sans inventer le numéro imprimé. | Écriture/suppression source par instance/lot/cascade refusée, transaction intacte. CF3 ne contourne pas ces gardes. | C0-A | L5, L6 |
| NR02 | C04/C06/C07; T05–T10, T16–T18 | Deux occurrences d’un même Statement gardent leurs numéros propres; renumérotation d’affichage conserve les examens applicables. | Aucun numéro copié d’un autre Document; index par Statement ambigu ne choisit pas une occurrence. | L1-B | L6 |
| NR03 | C07/C09; T18, T16 (`:601`, `:778`) | Confirmer puis réécrire une cible non partagée et une cible partagée : nouveau contrôle à réexaminer, ancienne capture lisible. | Cas partagé X→Y refusé comme encore confirmé, même si X/V1 reste courant sur la source. Variante : modification du côté SOURCE dans une rédaction B/C mutable. | C0-A | C0-B, L2, L6 |
| NR04 | C07; T19/T20 (`:656`, `:668`) | 1:N et N:1 conservent tous les antécédents/cibles et leur ordre. | Mauvais Document, doublon, rôle invalide, extrémité vide ou incohérente : refus sans groupe partiel. | C0-B | L1-B, L6 |
| NR05 | C08/C09; T21/T22 (`:678`, `:701`) | AJOUT/RETRAIT motivés restent des décisions; occurrence PRODUCED liée archivée, origine intacte. | Absence de lien ne devient pas décision; suppression physique ne retire pas automatiquement les antécédents. Groupe archivé consultable, décisions courantes explicites pour les occurrences actives. | C0-B | L5, L6 |
| NR06 | C09/C11; T18/T23 | Reconfirmer uniquement l’appui ne résout pas EX02; reconfirmer uniquement le traitement ne résout pas EX05. | Copier état, date ou appréciations d’une autre relation ne confirme pas le nouveau texte. | C0-B | L6 |
| NR07 | C10/C11; T23 dans `case_manager/test_e01_cotes_concordance.py:608` | Depuis le bon groupe E01, appuis de tous les antécédents consultables comme historiques; aucun appui retenu créé. | Ajouter un antécédent CF3 d’un autre Document partageant un Statement historique : les lignes de l’export E01 du couple initial restent identiques sur ce point. | C0-A | C0-B, L2, L6 |
| NR08 | C13–C17; T24–T28 | Export E01 conserve codes EX01–EX07, colonnes, cohérence source/cote, citations littérales et reproductibilité d’un même état. | Un échec indépendant de chaque EX continue de bloquer le strict; CF3 ne contourne ni lock ni contrôle de référent. | C0-B | L3/L4, L6 |
| NR09 | C16/C17; T27/T29 (`case_manager/test_e01_cotes_concordance.py:650`, `:810`) | Parcours diagnostique → décisions séparées → strict; suppression historique correctement restituée. | Un groupe de reprise ne couvre pas une occurrence E01 manquante et ne rend pas strict un état probatoire incomplet. | C0-B | L6 |
| NR10 | T11 et nouvelle migration | Valeur de profil héritée conservée, textes/PK/extrémités/M2M inchangés; nouvelles confirmations ajoutent leur manifeste; archives héritées non qualifiées signalées. | Pas de classification par titre, de type d’archive deviné ou de manifeste historique fabriqué. Ancien examen sans manifeste diagnostiqué; retour de migration sur base jetable documente la perte des seules métadonnées nouvelles. | L1-A | C0-B, L6 |
| NR11 | C09; routes `produced_views.py:230/254` | Requête HTTP d’édition d’une cible partagée détache et préserve la source; suppression autorisée archive. | Requête vers un référent/gel refusée; le chemin ne réalise pas d’écriture partagée. Vérifier les messages et l’absence d’effets partiels. | C0-A | L5, L6 |
| NR12 | C08/C09; archives et VersionTexte | Confirmer V1, réécrire et reconfirmer V2, archiver la cible : les deux décisions, leurs textes et le type du contenu au retrait restent consultables. | Purge Statement/VersionTexte, Document cible ou archive utile : refus si elle détruit l’histoire. Un Statement sans usage ni histoire utile reste supprimable. | C0-B | L5, L6 |
| CF3-01 | VF02, analyse danse → demande | Nouveaux LibraryNode et groupes REPRISE_DOCUMENTAIRE; source intacte; numérotation destination; nouveaux usages choisis vers mêmes éléments. | Aucun déplacement des nœuds source, aucune requalification comme juillet, aucune copie de PK/path source. | L2 | L5/L6 |
| CF3-02 | Analyse A → analyse B | Contextes internes distincts; copie partielle et filiation consultables sans dépôt/transmission. | Impossible d’exiger un ReferentHistorique fictif ou EX04 juillet pour valider cette seule reprise. | L2 | L6 |
| CF3-03 | VF02, édition après partage | Confirmer la relation nouvelle, modifier la cible puis la source en brouillon; détachement approprié et réexamen des relations concernées. | Modifier l’un changeant silencieusement l’autre, ou confirmation restant courante sur l’ancien Statement détaché. | L1-B | L2/L6 |
| CF3-04 | Reprise conservée/reformulée | Texte conservé traçable même avec un Statement destination distinct; reformulation possède ses captures. | Statement partagé ou même hash considéré comme confirmation automatique de pertinence ou filiation. | L1-B | L2/L6 |
| CF3-05 | Reprise partielle N:M | Deux sources et trois cibles d’un même couple forment un groupe collectif déclaré; toutes les identités et textes examinés sont conservés. | Réduire la fusion à un seul antécédent ou inventer des filières pour un lot dont les liens sont indépendants. | L1-B | L2/L6 |
| CF3-06 | Liens parcimonieux; plusieurs Documents | `s1→t1` et `s2→t2` restent deux groupes. Deux analyses vers une demande donnent des groupes par couple dans une application atomique. | Mettre une occurrence du second Document dans le premier côté SOURCE; prétendre représenter un groupe unique à trois Documents. | L2 | L6 |
| CF3-07 | VF03, ancêtre hors bloc | Usage de groupe proposé, puis explicitement omis ou rattaché avec portée à une nouvelle cible. | Héritage silencieux, cible destination absente, annulation laissant texte ou usages partiellement copiés. | L2 | L6 |
| CF3-08 | Appuis sélectionnés | Source avec cinq usages; plan en retient deux et quelques feuilles. Destination contient exactement ces UP/sélections, nouvelles identités et même preuve. | Union de tous les usages source, sélection automatique de racine, seconde autorité par Correspondance. | L2 | L3/L6 |
| CF3-09 | Nouvelle portée après reformulation/scission | Les candidats sont revus par cible; le plan accepté déclare les portées destination. | Hériter d’une ConfirmationAppui/absence confirmée, ou utiliser la confirmation éditoriale comme validation probatoire. | L2 | L6 |
| CF3-10 | VF04, reprise à l’identique | Nouvelle insertion remappée au bon Statement/version, composition et usages destination; rendu correct dans cet état. | Réutiliser simplement les offsets/source et conclure qu’ils sont valides car dans les bornes. | L4 | L5/L6 |
| CF3-11 | VF04, reformulation | Réancrage explicite après changement de texte; ancien rendu source intact. | Cote identique au même offset mais texte examiné différent : aucun faux succès de validation. | L4 | L5/L6 |
| CF3-12 | VF05, séparation des opérations | Copier le texte seul; créer séparément des usages; déclarer séparément un LienRedactionnel. | Une seule opération créant automatiquement les deux autres. Les options explicites d’un plan restent des décisions séparées. | L2 | L6 |
| CF3-13 | Réserves et contexte | S3 et ses sous-items de réserve sont repris par défaut; une omission volontaire est identifiée et motivée. | Copie du seul parent présentée comme sous-arbre complet; aucune tentative de détection sémantique automatique prétendument exhaustive. | L1-B | L2/L6 |
| CF3-14 | Prémisses/liens internes | Liens choisis remappés vers les nouvelles occurrences; textes réexaminés si reformulation. | Lien restant sur un ancien numéro ou déclaré courant par simple recapture automatique de la nouvelle prose. | L1-B | L2/L6 |
| CF3-15 | Prémisse hors bloc | Reprise de prémisse ou maintien d’une cible externe explicitement choisie. | Référence manquante, décision non résolue ou cible imaginée à partir d’un paragraphe de même numéro : application refusée. | L1-B | L5/L6 |
| CF3-16 | VF08, analyse V1 gelée → demande D1 | Dépendance vers l’occurrence V1, puis gel D1; analyse V2 modifiée sans effet sur renvoi, textes, examens, usages et rendus V1/D1. | Alias « dernière version » actualisant le renvoi historique; création de V2 modifiant les objets de V1. | L5 | L6 |
| CF3-17 | VF08, dépendance externe mutable | Brouillon possible avec suivi; gel strict après gel de la cible ou reprise explicite des prémisses. | Gel strict tant que cette dépendance reste sur une analyse externe mutable. Simple RENVOI reste une capture qualifiée selon CF2, sans import d’appuis. | L5 | L6 |
| CF3-18 | Gel propriétaire de la filiation | Nouvelle demande pouvant référencer une source déjà gelée; sa nouvelle relation appartient à la destination. | Geler la source interdisant toute reprise future; ou reprendre en modifiant une relation déjà incluse dans un contenu gelé. | L5 | L6 |
| CF3-19 | Archive d’une occurrence liée | Archive lisible avec ancien PK, Document, dernier texte, examen antérieur et motif; relation historique distinguée de la couverture courante. | Extrémité `None` non traitée, perte V1 par CASCADE, source réputée retirée par la seule suppression cible. | C0-B | L5/L6 |
| CF3-20 | Changement de composition après confirmation | Ajouter/substituer une occurrence portant le même Statement, changer rôle/couple/qualification : examen à refaire ou mutation refusée. | Ensembles de versions identiques permettant de conserver l’examen d’autres occurrences. | L1-A | L1-B/L6 |
| CF3-21 | Numérotation et sous-ensemble | Numéros issus des Documents complets; renvoi actif suit le PK après déplacement; rendu gelé garde ses repères. | Numérotation du bloc isolé utilisée comme numérotation globale, numéro source forcé dans la demande. | L1-B | L4/L5/L6 |
| CF3-22 | Plan périmé / concurrence | Vérification au précontrôle puis sous transaction de source, destination et relations; conflit explicite. | Édition entre rapport et application acceptée sans recontrôle; source gelée pendant la transaction puis modifiée; copie partielle après échec d’usage. | L2 | L5/L6 |
| CF3-23 | Sources/destination invalides | Analyse PRODUCED avec contexte valide, destination modifiable, éléments sélectionnés cohérents. | Destination gelée, REPRODUCED ou référent; contexte absent; source hors Document; sélection d’une autre preuve; usage visant une autre version : refus atomique. | L2 | L5/L6 |
| CF3-24 | Rendu et cotes | Résultat destination utilise seulement les sources sélectionnées, une identité documentaire par pièce selon C, cotes qualifiées par version. | Importer tout le bordereau source ou modifier les cotes/associations de juillet pour faire réussir la copie. | L3-A | L4/L5/L6 |
| CF3-25 | Gel / voies de mutation | Gardes exercées sur textes, occurrences, relations, M2M, usages, archives et fichiers conservés. | `update`, bulk, suppression/cascade ou écriture autorisée en brouillon contournant le gel. La seule présence de hashes n’est pas un succès. | L5 | L6 |
| CF3-26 | Type générique et régime de citation | Seuls les contenus rédactionnels admis sont repris; citations techniques restent sous les adaptateurs/règles de régime existants. | object_id d’un objet non Statement pris pour un Statement de même PK; ancien régime liant silencieusement une citation du nouveau régime. | L3-B | L6; noyau typé dès C0-A/L1 |

### 8.2 Contrôles nouveaux des deux garanties demandées

Ces contrôles complètent les 38 scénarios; ils ne les renumérotent pas et ne s’y substituent pas. Statut : **NON EXÉCUTÉ** pour chaque ligne.

| ID | Contrôle positif / attaque négative | Résultat exigé | Lot |
|---|---|---|---|
| IM01 | Créer un examen par l’entrée autorisée, puis tenter UPDATE de manifeste/date/origine via save, update, bulk_update et SQL direct sous rôle d’exécution. | Ajout valide conservé; toute mutation refusée; anciens octets/empreintes identiques. Tester aussi une écriture ne visant pas le seul champ manifeste. | L1-A; revalidation L6. |
| IM02 | Tentatives INSERT direct, bulk_create, upsert modifiant une ligne et ajout par la fonction avec manifeste incohérent. | Écriture directe refusée par droits/gardes; pas de ligne incomplète ni de validation des mauvaises occurrences; l’API seule peut ajouter un examen cohérent. | L1-A; L6. |
| IM03 | DELETE d’examen ou Correspondance parent, cascade du Document; TRUNCATE simple et CASCADE sous droits d’essai représentatifs. | Refus sans perte, y compris par ORM/SQL. Archives/captures nécessaires restent lisibles. | L1-A/C0-B; L5/L6. |
| IM04 | Deux transactions confirment le même ordinal/révision attendu; édition de texte et substitution d’extrémité concurrentes. | Au plus une confirmation du même état attendu réussit; l’autre reçoit un conflit. L’examen correspond à un état cohérent relu, jamais à un mélange; tester les deux ordres d’arrivée. | L1-A; L2/L5/L6. |
| IM05 | Examen d’un brouillon puis gel de destination; tentative d’ajouter une décision après gel; nouvelle reprise depuis source déjà gelée. | Ancienne décision immuable dès le brouillon; ajout dans la destination gelée refusé; nouvelle relation d’une autre destination permise sans modifier la source. | L1-A pour journal; L5/L6 pour gel. |
| IM06 | Reconfirmer une reformulation, tenter d’écraser/reclasser une ancienne entrée et falsifier seulement les projections héritées. | Nouvelle décision ajoutée; ancienne intacte. Aucune projection falsifiée ne produit un état confirmé valide; anomalie détectée/refusée. | C0-B; L6. |
| IM07 | Supprimer un Statement/VersionTexte/une archive référencés par un examen; modifier la version ou le parent avant l’attaque. | Conservation des textes et identités examinés; gardes sur ancien et nouveau périmètre; aucune perte par détour relationnel. | C0-B/L5; L6. |
| IM08 | Échec après insertion de l’examen avant mise à jour des projections; contrôle sous le vrai rôle d’essai, héritages de privilèges compris. | Transaction entièrement annulée; pas de projection orpheline ou de décision perdue. Le rôle ne peut désactiver les gardes, modifier la fonction ou obtenir les droits du propriétaire. | L1-A/C0-B; L6. |
| TR01 | Ancien CONFIRME, textes actuellement compatibles, mais aucun manifeste. | Décision historique conservée; provenance manquante signalée; nouveau strict refusé pour EX02 sans nouvel examen. | C0-B. |
| TR02 | Ancien CONFIRME puis détachement, texte changé, captures absentes ou mauvaise appartenance. | Réexamen/anomalie courant; données historiques inchangées; aucun ancien manifeste reconstruit. | C0-A pour détachement; C0-B pour transition. |
| TR03 | Créer un RELEVE_HERITE puis un nouvel examen explicite. | Date d’enregistrement actuelle distincte de l’ancienne date déclarée; seules les informations disponibles sont relevées; examen nouveau daté du jour et distinct. | L1-A/C0-B. |
| TR04 | Réouvrir un ancien contenu/livrable gelé et demander ensuite un nouveau rendu modifié. | Ancien artefact identique; le nouveau demande une nouvelle version et les examens requis. Pas de modification du gel pour satisfaire la transition. | L5/L6. |
| TR05 | Changer seulement numéro/cote d’affichage. | Examen complet demeure applicable; examen hérité reste de provenance insuffisante. Aucun numéro égal ne remplit un manque de manifeste. | C0-B/L1-B/L3/L4. |
| TR06 | Nouveau manifeste courant, mais citation/appui/numéro/référent en défaut; puis résolution séparée de chaque condition. | EX02 ne remplace pas EX01/03/04/05/06/07; strict refuse chaque manque puis accepte seulement l’ensemble valide. | C0-B; L3/L4/L6. |

Les tests de garanties SQL utilisent le rôle d’exécution effectivement restreint, pas seulement un propriétaire de base qui réussirait à contourner ses propres gardes. La création et le nettoyage des bases jetables peuvent relever d’un rôle de préparation distinct; aucune exception de purge du journal n’est ouverte au rôle applicatif pour faciliter les tests. La preuve attendue porte sur les chemins que le futur service utilisera.

### 8.3 Conservation des autres suites

| Suite | Responsabilité et lots |
|---|---|
| E01:T01–T29 | Conserver les tests existants et leurs attentes métier; C0-A/C0-B puis L6. Les contrôles du référent réel T01/T03/T24 ne sont pas exécutés pendant les travaux sur fixtures. |
| C:T01–T22 | T01–T05/T22 : L1; T06–T08/T12/T17/T20/T21 : L2; T09–T15/T18 : L3/L4; T16/T20 : L5; T19 : L3-B et contrat A; totalité revalidée en L6. |
| C:N01–N14 | Sources/dates/contenants/tri : L3; chevauchements/texte : L4; N03 fournisseur PHRASE : L3-B; gel/stockage/concurrence : L5; historique N09 : L6; revalidation finale commune. |
| VF01–VF14 | CF1 en L1; copie/usages en L2; liens en L1-B; insertion en L4; référence externe/gel en L5; Photo→Event en L3-A; tous en L6. |
| Invariants A/B et tests du régime | Invariance des surfaces héritées selon le contrat A et isolation par identité des PHRASE. Instruments/oracles de A inchangés; éventuels contrôles C complémentaires dans son propre espace. Un double d’adaptateur n’est pas une réussite d’intégration fournisseur. |

U1/U2 restent une démonstration rédactionnelle de référence (65 occurrences principales) avec les textes manquants explicitement signalés; aucune lacune n’est comblée par une citation inventée. Danse/garderie/synthèse restent les scénarios de reprise et de séparation des autorités. Ils servent à valider les contrats, pas à réviser le fond du dossier dans ce mandat.

## 9. Coordination et intégration sans perturbation de l’Agent A

### 9.1 État du fournisseur et frontière d’intégration

**Actualisation du 20 octobre :** une branche locale étape 2 existe à `b695e4683ed68bbc82e50cd68f712b3d5c5206d5`, avec PhraseAnchor et deux migrations 0010. Voir le [rapport de références](RAPPORT_CONSOLIDATION_ET_VALIDATION.md). Les descriptions « à la cible P6 » ci-dessous restent exactes pour ce socle observé; elles ne nient pas ce travail non intégré. Aucun état du serveur n’est certifié ici.

À la cible P6, `core/quote_regime.py` définit HERITE/PHRASE, `objects` filtré HERITE, `phrase_objects` et `all_objects` non filtré. Les GFK peuvent consulter le gestionnaire de base et les M2M à PK brutes ne passent pas par un filtre de lecture : C doit donc valider explicitement régime, type et capacité dans ses propres entrées.

Les deux `0009` portent l’étape 1. La cible ne fournit pas encore par ces seules migrations les bornes/certifications de l’étape 2. Les états et résultats documentés dans les plans sont des preuves antérieures; ce document n’annonce ni nouvelle P6 exécutée, ni récupération réussie, ni bascule réelle effectuée.

Le contrat PHRASE cible retenu pour les tests d’adaptateur :

- Courriel : corps canonique `body_plain_text`, sans repli opportuniste vers le sujet; PDF : transcription canonique et repères de page selon le fournisseur.
- Bornes Python `start` inclusif / `end` exclusif, dans le texte source; pas les coordonnées repliées `position_in_source` destinées à l’ordre.
- Certification effective : indicateur certifié **et** ancrage/texte-source/bornes/texte certifié encore compatibles, avec les trois empreintes du contrat A. Un scan corrigé conserve la différence explicite entre OCR ancré et lecture certifiée.
- Champs ou capacité indisponibles : diagnostic/refus du flux concerné. HERITE n’est pas transformé en PHRASE; une citation non certifiée ne passe pas dans un nouveau rendu probatoire strict.
- Au gel, conserver le texte effectivement rendu et les traces de certification. Après gel, relire le contenu/fichier conservé; un changement du fournisseur déclenche un diagnostic pour les nouveaux rendus sans modifier l’histoire.

Ces exigences ne demandent aucune modification immédiate du travail A. La stabilisation des représentations pendant la capture et les protections locales nécessaires au gel devront être coordonnées à l’intégration L5/L6, sans supposer que les seuls hashes du fournisseur réalisent le gel global C.

### 9.2 Règles Git et migrations futures

1. Pendant la récupération puis la bascule A : ne modifier ni E01, ni la branche d’intégration, ni leur cible P6, ni pilote/scripts/oracles, ni migrations existantes. Le plan A vérifie notamment qu’après sa référence applicative validée seuls certains fichiers docs/scripts ont changé et qu’exactement deux `0009` sont prévues. Ajouter les tables C à cette cible invaliderait cette prémisse.
2. Si un lot C est autorisé : créer une copie/clone **indépendant**, sans `.git` partagé avec l’espace de A, et partir du SHA P6 immuable. Sa propre branche peut contenir les changements C autorisés. Aucun worktree/migration/commit n’est créé dans ce mandat documentaire.
3. Tests C sur base jetable explicitement distincte, paramètres de test sans chargement de l’environnement réel, stockage temporaire et services externes simulés. Ne pas réutiliser les noms/ressources de P6, de son essai de récupération ou de sa référence de sauvegarde.
4. Nouvelles migrations C seulement dans les lots approuvés, après les migrations applicables de leur branche; aucun renommage/réécriture/squash des migrations de A. La résolution éventuelle de têtes de migrations concurrentes sera faite dans une intégration future approuvée et testée, jamais dans la cible figée.
5. Après clôture A : identifier le socle effectivement livré et son état de migrations. Préparer une branche d’intégration C distincte, réexaminer les conflits et rejouer les contrôles sur une restauration/copie dédiée. Toute nouvelle cible nécessite sa propre validation; P6 n’est pas un label transmissible automatiquement à un descendant contenant C.
6. Le passage d’une validation isolée à la base réelle reste un mandat distinct. Aucun succès de tests dans un lot n’autorise à lancer `migrate`, importer l’historique, créer une PHRASE réelle ou publier un rendu de C sur le serveur.

### 9.3 Retour arrière : préserver celui de A, puis éprouver celui de C

Le plan A impose le retour de base R2/R3 avant le retour de code R1. Pendant sa fenêtre immobilisée, le périmètre est celui de l’étape 1; après réouverture, ses règles distinguent conservation des écritures et restauration avec perte soumise à décision. **C ne change aucune de ces conditions pendant cette fenêtre.** Les scripts de A ne sont pas exécutés ni modifiés ici.

Avant un déploiement C ultérieur, capturer un nouvel état de référence **après A**, valider la récupération avec les nouvelles tables/FK/gardes/fichiers et tester la paire code/schéma correspondante. Un ancien journal append-only ne doit pas être détruit par une marche arrière de migration sur une base ayant reçu des décisions réelles : conserver schéma/journal ou restaurer un état conforme avec conservation des écritures selon un plan explicitement approuvé. Le test de retour de schéma NR10 reste un test sur base jetable, pas une procédure de purge de données réelles.

L’ordre futurement acceptable est : récupérer C vers un état post-A validé, puis réévaluer séparément un éventuel retour de A si nécessaire. Après de vraies PHRASE ou des objets C persistés, les anciennes hypothèses de récupération de l’étape 1 ne suffisent plus à garantir la conservation du sens des données. Toute restauration susceptible de perdre des écritures exige une décision explicite et une capture préalable; aucun retour global automatique n’est proposé.

## 10. Situation actuelle, réserves et prochain passage

### 10.1 Orientations déjà approuvées

D01–D03, D06, D08–D12, CF1–CF3 et CF3-D1–D5 sont retenues par le mandat utilisateur antérieur, avec leurs garanties. D04 est retenue quant à l’unité complète; D05 est maintenant décidée pour le principe CHRONO_VERSION. CF3-D6 est accepté comme plan, pas comme autorisation globale d’exécution.

### 10.2 Conditions et arbitrages encore ouverts

D07 et CF4 restent conditionnelles à la vérification des sources. R01–R08 figurent dans l’avenant; les détails ne sont pas tranchés par le code. La disponibilité locale du fournisseur A étape 2 ne prouve pas son déploiement et ne remplace pas ses contrôles.

### 10.3 Obstacles à une nouvelle implantation

Les dossiers à quatre vues sont incomplets; aucun n’est approuvé par l’utilisateur au nouveau protocole. C0-A n’est pas atterri. Les réserves sur les composites, la cotation détaillée, les brouillons et le stockage bloquent leurs chemins respectifs. Les protections du journal et du gel restent à éprouver dans les lots futurs, sans validation rétroactive des décisions héritées.

### 10.4 Premier travail et lot suivant

Premier dossier à finaliser : **UC-C-13**, puis UC-C-14/15 pour la revue de C0-A. Leur approbation et un mandat distinct d’atterrissage sont nécessaires avant de déclarer le lot fait. Le premier nouveau lot candidat reste **L1-A**, seulement après les préalables, les dossiers correspondants et l’autorisation de lot. Le présent mandat reste documentaire.

### 10.5 Périmètre historique du premier mandat C0-A

**Mandat initial approuvé puis exécuté isolément le 19 octobre; non atterri.** Les points ci-dessous conservent le périmètre initial et ne constituent pas une nouvelle autorisation. Rapport et diff sont dans `lots/C0-A/`. La revue/intégration et les dossiers UML UC-C-13/14/15 restent à mandater selon le processus actuel.

**Périmètre conservé du mandat initial :**

1. Préparer une copie de travail indépendante au SHA **`212a7feee81aef46a5b43d36e8eeafe0f8870064`**, avec sa propre branche de développement et une base de test jetable distincte. Ne toucher ni au dépôt principal ni aux ressources de A. Aucun chargement de `.env` réel, appel serveur ou service externe réel.
2. Modifier uniquement les services E01 communs, leurs méthodes de contrôle et leurs appels existants : `document_manager/concordance.py`, `export_concordance.py`, `protection.py`, les méthodes Python concernées de `document_manager/models.py`, `document_manager/views/produced_views.py` et, si nécessaire pour le même défaut de fraîcheur, les méthodes de `ConfirmationAppui` dans `case_manager/models.py`. Aucun ajout/modification de définition de champ, de migration, d’application installée ou de politique de cotes.
3. Réaliser les corrections précisément bornées : détachement/capture avant édition par les routes actives; suppression par le service d’archivage existant avec refus atomique; vérification du texte examiné contre le Statement porté par l’occurrence; transmission du couple de Documents jusqu’au lecteur des appuis historiques, type vérifié et archives inconnues traitées sans deviner; refus de purge des captures encore nécessaires aux examens existants. Le filtrage par nature et l’historique complet attendent L1-A/C0-B.
4. Ajouter les contre-épreuves dans les tests E01 et tests HTTP pertinents, en visant les variantes C0-A de NR03/NR07/NR11 et la conservation de texte. Exécuter les suites E01 et de régime disponibles sur données synthétiques isolées, avec le code et les migrations déjà existants de la cible; ne modifier aucun oracle/pilote ou critère de A pour les faire passer. Toute régression inattendue doit être expliquée et corrigée, pas normalisée.
5. Livrer le diff, le rapport d’exécution et les limites restantes pour revue. **Aucun commit, push, fusion, modification de cible E01/P6, nouvelle migration, application à la base réelle, lancement de récupération/bascule ou déploiement n’entre dans cette première autorisation proposée.** Ces actions resteraient à mandater séparément. Cette session n’exécute aucune des opérations proposées.
