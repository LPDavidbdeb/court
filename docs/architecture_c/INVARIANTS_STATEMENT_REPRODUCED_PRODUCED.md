# Statement — provenance, propriété et réutilisation

**ST-2026-10-20-R1 — décision fonctionnelle reçue et analyse documentaire.**
**Suivi du 20 octobre 2026 :** le seul profil UC13::C0A_ISOLER R2-ST décrit
ci-dessous a depuis été [approuvé explicitement](use_cases/UC-C-13/approbation.json)
au manifeste de cd584c3; les mécanismes permanents L1-A restent proposés.
La copie contractuelle antérieure à l’approbation est conservée à l’identique.

Source conservée : [mandat utilisateur](references/MANDAT_INVARIANTS_STATEMENT_2026-10-20.md).
Socle lu : `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`; patch C0-A inchangé.
Ce document précise les contrats actuels. Il ne certifie ni les données réelles,
ni le respect de ces règles par le code, et n’autorise aucun développement.

## 1. Invariants fonctionnels décidés par l’utilisateur

| ID | Règle cible | Conséquence |
|---|---|---|
| ST01 | Les occurrences et contenus REPRODUCED sont immuables. | Ni édition du texte, ni renommage/repointage/déplacement/suppression d’une occurrence reproduite. Les opérations d’import initial et leur clôture nécessitent un protocole distinct; ce n’est pas une édition d’une source déjà constituée. |
| ST02 | Seuls les Statement provenant d’un document REPRODUCED peuvent être réutilisés par une autre occurrence, notamment PRODUCED. | L’admissibilité repose sur la provenance attestée, pas seulement la présence actuelle dans un document de ce type. |
| ST03 | Une édition de texte dans une occurrence PRODUCED réutilisant une origine REPRODUCED crée un Statement privé. | L’original et les autres occurrences demeurent inchangés; capter les états utiles et recontrôler les décisions courantes. |
| ST04 | Un Statement créé pour PRODUCED appartient à une seule occurrence et ne peut être réutilisé par une autre. | Copier le texte vers une nouvelle occurrence crée un nouvel objet, même si le texte est identique. Le retrait de son propriétaire ne rend pas l’ancien objet réutilisable. |
| ST05 | Toute édition autorisée préserve les autres occurrences et états historiques protégés. | Un Document PRODUCED devenu référent ou gelé reste protégé. Sa protection ne le transforme pas en origine REPRODUCED réutilisable. |

Ces cinq règles sont **DÉCIDÉES UTILISATEUR** par le mandat. Les mécanismes,
le profil transitoire ci-dessous et la version du dossier UML restent proposés
à approbation. Ni `is_user_created`, ni un titre, un hash égal, un référent ou
`derived_from` ne constituent une preuve de provenance réutilisable.

## 2. Ce que le modèle sait réellement établir

| Question | Observation disponible | Limite de la preuve |
|---|---|---|
| Usage dans REPRODUCED | `LibraryNode(content_type, object_id)` → `Document.source_type`; `statement_protege()` vérifie cet usage | Prouve un usage actuel, pas le document où l’objet a été créé. Une association ajoutée plus tard ne prouve pas cette origine. |
| Un seul usage PRODUCED | Décompte des occurrences portant le couple typé Statement/PK | Prouve la cardinalité observée à cet instant; ni propriété durable, ni absence d’ancien propriétaire ou de nouvel attachement concurrent. |
| Partage actuel | Au moins deux LibraryNode pour le même couple typé, dans un ou plusieurs Documents | Ne classe pas ce partage comme autorisé; il faut connaître la provenance. |
| Protection historique | REPRODUCED, ReferentHistorique; usages/captures/archives E01; futurs états figés | Ne constitue pas une origine de création. Un référent PRODUCED reste PRODUCED. |
| Provenance et propriété privées | Aucun champ d’origine ni de propriétaire dans Statement; GFK sans unicité conditionnelle | Impossible d’attester universellement ST02/ST04 avec les seuls modèles présents. |

`Statement.is_user_created` décrit un mode de saisie, pas la provenance au
sens de ST02. Le sélecteur actuel `search_evidence_ajax` filtre pourtant les
Statement sur `is_user_created=False` et les affiche « Reproduced Text » :
c’est une convention insuffisante pour la nouvelle règle. À l’inverse, un
texte saisi à la main peut reproduire un document; aucune déduction inverse
n’est davantage fiable.

Deux historiques de création différents peuvent produire exactement les
mêmes associations actuelles. Les relations présentes ne permettent donc
pas de reconstruire arbitrairement cet historique, même si une seule
association REPRODUCED subsiste aujourd’hui. Une provenance non établie doit
rester **À ÉTABLIR**, sans réaffectation automatique d’anciens Statement.

## 3. Chemins d’écriture et garanties observées

| Chemin au socle `515666e` | Constat en lecture de code | Lot responsable de la cible |
|---|---|---|
| `views/produced_views.py`, création/ajout | Crée de nouveaux Statement pour la racine et les nouveaux textes; aucun propriétaire persistant | L1-A pour les constructeurs/attributions; UC02 pour le parcours |
| `views/library_node_ajax.py:111`, `add_library_node_ajax` | Accepte un ContentType et un object_id soumis; vérifie l’existence avec le gestionnaire par défaut. Pour Statement, aucune vérification de provenance REPRODUCED ou de propriété privée avant création de l’occurrence | L1-A pour fermer ce rattachement et les entrées équivalentes; fichier hors des huit fichiers du patch C0-A, à autoriser séparément avant toute écriture |
| Même module, `search_evidence_ajax` | `is_user_created=False` employé comme filtre d’un texte dit reproduit | L1-A / UC02 : filtre d’admissibilité; la vérification serveur reste nécessaire, même avec un sélecteur filtré |
| `concordance.detacher_pour_edition`, code principal | Détache si partagé/protégé; sinon modifie l’objet en place | C0-A pour la sécurité locale d’édition; modèle d’origine durable en L1-A |
| Même service dans le patch | Préserve les captures et détache les partages constatés; peut toujours modifier en place un objet considéré privé | Pas conforme à une garantie de propriété durable; profil conservateur proposé au §5 |
| `protection.garde_modification_statement`, code principal / patch | Refuse le texte actuellement porté par REPRODUCED ou référent; le patch ajoute le refus du partage constaté à la sauvegarde | Gardes utiles mais insuffisantes pour prouver la provenance ou fermer les rattachements. L1-A pour l’interdiction ST04; L5 pour les gardes globales de gel |
| `protection.garde_modification_noeud` | Code principal : protège les champs du référent, pas tous les REPRODUCED; création d’un nouveau nœud retourne avant cette garde. Le patch renforce ancien/nouveau Document référent mais n’ajoute pas le contrôle ST04 | Fermeture des mutations de sources et des rattachements : L1-A; limites signalées, pas réputées réalisées par C0-A |
| `DocumentUpdateView` / `DocumentForm` | Le formulaire expose `source_type`; pas de garde de provenance durable observée sur son changement | L1-A : interdire la requalification d’un Document servant à blanchir une provenance; aucune conversion silencieuse du dépôt historique |
| `LibraryNode` ORM, bulk, SQL | GFK sans FK vers Statement, sans contrainte d’exclusivité privée; un signal ne couvre pas toutes ces écritures | L1-A doit protéger sa règle d’attribution et ses voies autorisées; pas de promesse universelle reportée implicitement à un simple formulaire. L5 complète le gel global |
| `ajax_views.update_statement_flags` | `QuerySet.update()` sur is_true/is_falsifiable, hors gardes de texte; métadonnées partagées susceptibles d’être modifiées | Définir en L1-A si ces appréciations sont du contenu immuable ou doivent être portées par l’occurrence/examen. Pas de modification de ce chemin dans C0-A |
| `concordance.relier` | Crée une filiation entre occurrences existantes; ne crée pas leur partage de Statement | Ne pas confondre lien éditorial et autorisation de réutiliser un objet |
| Imports et démonstration E01 | L’import de la demande crée un Document PRODUCED et des objets neufs; les fixtures du patch créent explicitement deux PRODUCED partageant un Statement | Conservation historique; audit/qualification à préparer avant application globale, aucune conversion des types ou réparation automatique |

La recherche a porté sur les écritures/rattachements LibraryNode et les
créations/modifications Statement dans les sources Python du dépôt, puis les
routes, formulaires et gardes nommés ci-dessus. Les noms « source » dans un
service ou une fixture ne constituent pas `DocumentSource.REPRODUCED`.

### Situations historiques à conserver et auditer

Le test du patch `test_http_edition_detache_deux_documents_produced` est une
preuve de robustesse face à une association héritée incompatible avec ST04,
**pas un parcours positif désormais autorisé pour créer ce partage**.
`test_http_cible_detache_le_texte_du_referent` utilise également un référent
PRODUCED : protection historique et origine reproduite doivent rester distinctes.
Ces tests et le patch ne sont pas modifiés.

Les anciennes conceptions de reprise entre analyses autorisaient le même
Statement à texte égal. Elles sont remplacées pour les nouveaux parcours
PRODUCED→PRODUCED par une copie de texte et un nouvel objet. Les 38 scénarios
NR/CF3 sont conservés; leurs partages de source sont soit des origines
REPRODUCED attestées, soit des contre-épreuves de données héritées à qualifier.
Ne pas réécrire leur histoire ou les résultats P6 pour les rendre conformes.

Aucune base réelle n’est interrogée dans cette revue. On ne peut donc ni
affirmer l’absence de lignes incompatibles, ni donner leur nombre. L’audit
futur devra lister, par couple typé, occurrences/Documents, captures, référents
et preuves d’import; cardinalité seule → candidats à examen, jamais origine
inventée. La décision de traitement des anciennes associations appartient à
l’utilisateur, sans déliaison, suppression ou conversion automatique.

## 4. Concurrence : conclusion précise

**Dans un système respectant ST04 sur toutes ses écritures**, un Statement
privé ne peut devenir partagé par un parcours autorisé. Aucun mécanisme
général de verrouillage des arbres n’est nécessaire pour ce scénario interdit.

**Dans le code actuel, même avec le patch**, le scénario demeure possible :

1. T1 lit un Statement S porté par la seule occurrence N1 PRODUCED.
2. T1 termine ses contrôles de partage, y compris le comptage du signal de
   sauvegarde ajouté par le patch : un seul usage à cet instant.
3. T2 rattache S à une nouvelle occurrence N2 via `add_library_node_ajax`;
   cette création n’a pas de garde ST04, et sa GFK ne verrouille pas S.
4. T1 écrit le texte de S et valide. N1 et N2 voient le texte modifié.

Si T2 termine avant le contrôle final du patch, ce contrôle peut refuser T1;
cela ne couvre pas la fenêtre après ce contrôle. `transaction.atomic` garantit
l’annulation d’une opération refusée, pas l’impossibilité de cet entrelacement.
Cette construction découle des chemins lus; ce n’est pas un test PostgreSQL
de concurrence exécuté.

**Recommandation minimale :** ne pas ajouter de verrous généraux à C0-A.
Éviter son écriture en place tant que la propriété et la fermeture des
rattachements ne sont pas établies (§5), puis imposer la règle d’attribution
dans L1-A (§6). Un éventuel contrôle atomique local de l’attribution initiale
en L1-A porte sur cette attribution, pas sur un gestionnaire général de partage.
Les éditions concurrentes de la même occurrence et les conflits de gel sont
des risques distincts; la nouvelle règle ne les élimine pas.

## 5. Profil C0-A proposé : `UC-C-13::C0A_ISOLER`

Ce profil **à approuver** ne crée pas de schéma, de registre de provenance ou
de nouvel objet de domaine. Pour une occurrence PRODUCED éditable :

- Texte identique : conserver le Statement; traiter `item` séparément.
- Texte réellement différent : capter l’ancien texte, créer un Statement neuf
  pour cette occurrence, la repointer et capter le résultat; **ne jamais
  mettre à jour en place le texte de l’ancien Statement dans ce profil**.
- Occurrence sans contenu : créer son premier Statement; type incompatible
  ou occurrence protégée : refus atomique.
- Une association ambiguë ou illégale déjà présente reste diagnostiquée comme
  telle; cette édition demandée ne vaut ni certification de sa provenance ni
  réparation globale. Aucune autre occurrence n’est modifiée.

La copie est un choix conservateur transitoire, pas une obligation métier de
dupliquer un contenu privé à chaque édition une fois L1-A réalisé. Elle évite
le décompte de partage comme décision de sécurité, la fenêtre T1/T2 sur l’ancien
texte, et une dépendance circulaire C0-A→L1-A→C0-A. Un rattachement interdit
ultérieur reste possible dans le code non corrigé; **C0-A ne réalise donc pas
à lui seul ST04 sur toute l’application**. Il garantit la non-altération des
autres contenus par sa propre opération d’édition.

La modification directe reste admissible dans le contrat complet uniquement
si provenance privée, propriétaire de l’occurrence, mutabilité et interdiction
effective des rattachements sont établis. Ce chemin est **désactivé dans le
profil C0-A soumis**; son activation relève de L1-A et de la revalidation d’UC13.

Le patch actuel ne suit pas encore ce profil : il conserve une branche de
modification privée en place. Sa modification reste interdite dans ce mandat.
Une future correction resterait proposée dans `document_manager/concordance.py`
et les tests C0-A associés, après autorisation écrite; aucun ajout de contrôle
sur `library_node_ajax.py` n’est absorbé silencieusement dans le périmètre.

Alternative : fermer tous les rattachements avant d’autoriser l’écriture
privée en place. Elle est recevable, mais exige un mandat couvrant ces entrées
et une preuve de provenance; le patch de huit fichiers ne l’établit pas.
Le seul comptage sous transaction, ou un verrou pris uniquement par l’éditeur,
est rejeté comme preuve : le chemin de rattachement doit participer au contrat.

## 6. Solution persistante minimale proposée — L1-A

Deux métadonnées sur **Statement existant**, noms proposés et non schéma approuvé :

1. `document_origine_id` : FK vers le Document réellement à l’origine, attribuée
   par une voie contrôlée, immuable et protégée contre la suppression utile.
   NULL historique signifie **non établi**, jamais REPRODUCED par défaut.
2. `occurrence_proprietaire_pk` : identité persistante de l’occurrence à laquelle
   un Statement privé est attribué. Une identité historique conservée, pas un
   FK SET_NULL qui libérerait l’objet après retrait du propriétaire. Elle peut
   rester un ancien identifiant qualifié par son document d’origine, comme les
   identifiants d’archive existants. Allocation et vérification doivent être
   atomiques et contrôlées; les PK historiques ne doivent pas être recyclées.

Pour une origine REPRODUCED attestée : pas de propriétaire privé exclusif;
réutilisations PRODUCED permises, source et provenance immuables. Pour une
origine PRODUCED : tout rattachement à une autre identité d’occurrence est
refusé, même dans le même Document ou après suppression de l’ancien nœud.
Le type du Document d’origine ne peut être modifié pour blanchir cette règle.

Il faut contrôler création/rattachement/repointage, admin et opérations bulk/
SQL autorisées avec les droits/gardes appropriés, pas seulement un formulaire.
La finalisation d’une première attribution doit interdire deux propriétaires
concurrents et une attribution non terminée; le détail SQL se conçoit et se
teste sur base jetable dans L1-A. Pas d’entité nouvelle ni de migration créée ici.

Pourquoi deux informations : le document d’origine seul ne mémorise pas le
propriétaire autorisé après retrait; l’unicité globale d’un Statement sur les
occurrences interdirait les réutilisations REPRODUCED légitimes. Un booléen
`partageable`, `is_user_created` ou un compteur d’usages ne prouve pas l’origine.
Une table de provenance distincte n’est pas nécessaire à ce stade.

Ces métadonnées ne sont jamais remplies rétroactivement à partir de l’usage
présent seul. Les nouveaux objets sont attribués dans leur opération de
création; l’historique inconnu exige des preuves d’import/examen séparées.
Le contrat de conservation des propriétaires et des suppressions sera revu
avec UC14; aucun effacement de capture ou refus historique n’est levé ici.

## 7. `item` : question distincte

`item` appartient à **LibraryNode**, pas à Statement. Le patch sépare sa
sauvegarde de celle du texte; un changement d’item seul n’exige pas de nouveau
Statement. Sur REPRODUCED ou référent, l’édition reste refusée.

Mais `item` n’est **pas toujours un simple libellé** : dans `numerotation.py`,
`genre_du_noeud()` classe notamment un item `C-…` en conclusion et un item vide
en mention; la numérotation/rendu peut donc changer. Les instantanés de référent
et NoeudArchive capturent aussi cette propriété.

Les lecteurs de fraîcheur C0-A comparent Statement/empreinte/Document et
portée d’appui; ils ne comparent pas `item`. Un simple renommage sans effet
sur le contexte examiné ne périme pas automatiquement une décision de texte.
Si `item` change le rôle ou la portée interprétée, C0-A **ne garantit pas** le
réexamen de cette décision. L1-A/C0-B doivent prendre le contexte pertinent
dans le manifeste d’examen et ses contrôles, sans invalider aveuglément toute
modification d’affichage. Le profil et la frontière libellé/rôle sont à
spécifier dans UC02/05E/12; ST04 ne résout pas ce point.

## 8. Impacts et conditions de décision

| Use case / lot | Conséquence |
|---|---|
| 02 / L1-A puis L1-B | Ne plus proposer un Statement privé comme objet réutilisable; copier le texte crée un nouvel objet. Un déplacement de la même occurrence n’est pas un partage; ses protections/contexte restent contrôlés. Le sélecteur doit éviter l’étiquette de provenance déduite du seul drapeau de saisie. |
| 07 / L1-B/L2 | Reprise depuis PRODUCED, même gelé et texte identique : nouvel objet Statement et nouvelles occurrences. Filiation via Correspondance; aucune confirmation automatique par hash ou identité partagée. Depuis REPRODUCED : partage seulement avec provenance attestée. |
| 14 / C0-A, puis L1-A/C0-B | Préserver sources/anciens objets utiles et archives. Ne pas traiter la suppression du propriétaire comme une libération du droit de réutilisation. Pas de réparation automatique des anciens partages. |
| 15 / C0-A/C0-B | Les appuis historiques restent consultables par couple et type vérifiés, même si l’association ancienne demande qualification. Leur lecture ne donne aucun droit de créer un nouveau partage. **C0A-REV-01 reste ouverte et distincte.** |
| L1-A | Attribuer provenance/propriété fiables et fermer les rattachements autorisés; reprise historique contrôlée, pas de backfill fictif. |
| C0-B | Manifeste/examen de contexte et transition historique, notamment item sémantique; ne pas fabriquer des examens anciens. |
| L5 | Compléter les protections de gel des versions, relations et fichiers; ne pas lui attribuer rétroactivement les garanties de C0-A. |

**À approuver maintenant :** le dossier exact UC13 C0A-UML-R2-ST pour le seul
profil `C0A_ISOLER`, son absence d’écriture en place et ses limites affichées.
La décision utilisateur ST01–ST05 est acquise; cette proposition d’exécution
limitée ne l’est pas. Le contrat complet de propriété ne devient pas livré.

**Avant toute activation du chemin direct :** décider et valider la solution
persistante L1-A, l’allocation du propriétaire, les droits et toutes les entrées
de rattachement; traiter les inconnus historiques selon une décision explicite.
Avant approbation complète des examens de contexte : fermer le cas d’item
sémantique dans leurs dossiers. Aucun DEC-R01–R08 n’est clos par ce document.

Aucun code, patch, migration, base, branche ou travail de A n’est modifié.


## 9. Vérifications et conservation

Les [contrôles documentaires détaillés](lots/C0-A/CONTROLES_INVARIANTS_STATEMENT_R2.json)
confirment : six critères UC13 littéralement inchangés, 91 critères V2 et
38 scénarios NR/CF3 conservés, 44 tickets/22 UC/10 lots, six vues révisées
compilées et inspectées. Les huit vues locales 14/15 sont inchangées.
Les [manifestes UC13](use_cases/UC-C-13/manifest_sha256.json) identifient la
version soumise; l’[archive précédente](historique/2026-10-20_avant_invariants_statement_R2/README.md)
conserve 72 fichiers avec empreintes. Les 12 scénarios ST sont **NON EXECUTES**.
Aucun essai Django/PostgreSQL ou sur base réelle n’est présenté comme exécuté.

Les 670 fichiers de référence hors documentation et le patch ont conservé
leurs octets. Pendant ce travail, un commit externe `94f3bc4` a ajouté les
artefacts de préparation de A et modifié son plan documentaire; les changements
entre `515666e` et ce HEAD sont limités à `docs/`. Le socle applicatif lu
reste donc `515666e`. Aucun commit, push ou changement de branche n’a été fait
par B; les ressources de A n’ont pas été modifiées par cette intervention.
