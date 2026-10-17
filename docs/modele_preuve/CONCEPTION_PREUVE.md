# Modèle Preuve — conception

Ouvert le 2026-10-15. **En discussion : rien n'est construit.** Ce document est lié au plan de
fusion des citations (`docs/purge_quotes/PLAN_FUSION_CITATIONS.md`), qu'il modifie (§6).

**Complément du 16 octobre 2026 — socle des causes.** La structure commune
`Cause`, ses états, les liens entre causes et le rattachement d'origine des
documents et courriels sont implémentés séparément du pont de preuve décrit
ici. Voir [ARCHITECTURE_CAUSES.md](ARCHITECTURE_CAUSES.md), qui précise aussi
la cible `Cause → Acte → VersionActe → Transmission`. Le pont de preuve et le
gel d'une version complète restent à construire; « rien n'est construit »
ci-dessus concerne ce pont.

## 0. État d'avancement (16 octobre 2026)

*Section remplacée à chaque point d'étape. Rien n'est construit : tout ce qui suit est sur papier.*

### Ce qui est décidé

**Le cadre.** Deux rives (la preuve ; la thèse) et un pont. Le nouveau pont ne dépend que des
rives ; il se construit en parallèle, et l'ancien pont se décommissionne ensuite (§ 1).

**La chaîne.** Paragraphe → démonstration → preuve (arbre) → élément → document (§§ 2, 8) :
- des nœuds d'affirmation (énoncé, nature, degré, règle), des feuilles (rôle relatif au parent)
  et des renvois entre preuves, sans cycle ;
- une démonstration est une liste de poignées vers des nœuds, à tout niveau, avec ses cibles ;
- le témoignage est un appui sans document ;
- une preuve non rattachée est l'état de triage.

**Le bordereau** (§ 3). La culée du pont : calculé par l'usage, un seul, versionné. Le gel se fait
au dépôt : demande, preuve et bordereau partagent un numéro de version. La correspondance se fait
par modèle + PK. Juillet en est la première version, lue une fois dans `BordereauDepotJuillet`.

**Le rendu.** Aucune cote ni aucun verbatim en dur : tout est rendu depuis la chaîne. La phrase
est entière, sans troncature (§§ 7.5, 12.6).

**Les unités.**
- L'élément est l'unité minimale suffisante, et une citation est une phrase.
- Les actes adverses se citent au paragraphe.
- Le document d'une citation de courriel est le courriel.
- Une liasse devient une preuve.

**Les versions.** Ce qu'utilise une version gelée ne se modifie plus : on le copie, et la copie
garde son origine (copie du chemin). Un élément non certifié sur l'original ne se rend pas.

**Le verdict** (§ 15). L'architecture modélise les trois axes éprouvés (danse, garderie,
activités), avec trois ajouts : une **période** sur les affirmations, le **fondement du degré**
(document seul ou avec témoignage) et un **nœud compté** (unité de compte et critère écrit).

### Ce qui reste à trancher

| Question | Où |
|---|---|
| Le document d'un message de clavardage (la séquence ?) et d'une photographie (l'événement ?) | § 15.2 |
| Les cardinalités recommandées : un paragraphe a au plus une démonstration ; une démonstration sert un bloc | § 5 |
| Ce qu'on reprend de l'ancien pont : les 12 faits en triage ? | § 5 |
| La formulation des faits de la garderie et des activités | §§ 12.2, 13.2 |
| Le plancher des sorties inclut-il l'escalade ? | § 14.2 |
| Les précisions de la règle de la phrase : énumérations, « : », retours à la ligne | `PLAN_FUSION_CITATIONS.md` § 3.3 |
| Le sort des 80 nœuds-citations des docs 5 et 6 | en suspens |
| La forme du document intermédiaire | reportée par LP |
| La complétude de la preuve (courriels non utilisés, photos de Cape Cod 2012) | reportée par LP |

### Ce qui manque avant de construire

1. **Le schéma sur papier.** Les concepts sont arrêtés, les tables ne le sont pas : preuve et
   nœuds (`MP_Node`), élément (clé générique), démonstration et poignées, lien paragraphe →
   démonstration (portée, état, version, mode d'affichage), versions et entrées du bordereau.
2. **L'entretien de la rive, préalable au bordereau.** *Révisé le 2026-10-17* : le ménage des
   citations est abandonné au profit de **deux régimes** (§ 17). Restent à faire :
   - le champ de régime, avec ses contraintes ;
   - le chemin de création des citations du nouveau régime : règle de la phrase, position,
     certification ;
   - la certification des énoncés des actes adverses ;
   - le marquage des doublons de documents (email 48 / 347), avec le report des notes de fils.
3. **Une première construction d'épreuve** : l'arbre de la danse (§ 11), rattaché à un vrai
   paragraphe de la version 2. Elle éprouverait ce que les axes n'ont pas éprouvé : la
   démonstration réelle, le bordereau calculé et le gel (§ 15.3).

### Les diagrammes

`docs/modele_preuve/diagrammes/` (PlantUML) : rives et ponts, schéma proposé, arbre de la danse,
versions et gel, rendu et bordereau. Voir le `README.md` du dossier.

### Ce que l'exercice a produit au passage, du côté de la thèse

- La théorie des cours de danse de LP est portée dans l'axe (`01_cours_danse_mere.md`).
  L'automne 2013 est déterminé (lundi).
- Des pièces présentes au corpus, mais non mobilisées par la référence de leur thème, ont été
  relevées pour la garderie (§ 12.5) et les activités (§ 13.5).
- Les notes personnelles de LP se trouvent dans `EmailThread.note` (§ 12.6).

---

## La proposition de LP (mot pour mot)

> Le ménage dans les quotes est necessaire, mais je crois qu'il manque un model pour médier
> les différent elements de preuves et les paragraphes de la requete est c'est un modele
> preuve. Le modele preuve est un nested set, qui permet d'assembler plusieurs éléments
> (quotes-email, quote-pdf, evente, statement, etc) le model nested set permet d'ordoner les
> pieces hierarchiquement et entre "sibblings" un abre par preuve et les preuves que l'on
> définit comme un ensemble d'élément ordonnée peuvent êtres réuitlisé dans différente
> démonstration. Je viens de dégager 3 concepts important je crois, les éléments de preueves
> qui contitue une preuve et qui ensemble constitue des démonstrations. la démonstration est
> relié au paragraphe et c'est a travers la chaine pragraphe -> demonstration -> preuve ->
> elements de preuves que les documents (pdf, email, event, documents, chat sequence) que le
> lien s'établit

> Oui je crois que ma proposition remplace tout ce que nous avons envisagé par le passé pour
> lié les paragraphes avec la preuve. Voici comment je percoit la situation. Nous avons 2 bloc
> fondamentaux, les documents de preuve et les pargraphes qui construise le grief. Ces
> paragraphes sont dans le model document_manager et c'est leurs place. le reste des app du
> projet servent a lier les 2 et je crois que la structure proposé est suffisante en elle
> meme. Elle rend donc le reste redondant est inutile. Je souhaite développer l'approche en
> parallele, en supposant que les documents de preuves soient une rive et que la these soit
> l'autre rive, séparée par un cour d'eau, l'infrastructure existante est un pont, avant de
> le décomissioner, nous allons construire le nouveaux et mous nous occuperons du
> décomissionement par la suite, ce qui fait que la nouvelle construction doit etre
> completement indépendante de la premiere et ne dépendre que des deux rives.

> laisse moi précisé d'avantage mon analogie de la rive, et critique la. La rive, celle des
> element de preuve. le tablier du pont repose sur le bordereau des pieces, le bordereau des
> pieces est l'élément qui uniformise la provenance des élément de preuve, lorsqu'une quote /
> statement (email / PDF / document) ou un event ou un chat sequece est utilisé, le document
> entier se voit inclure dans l'ensemble ordoné chonologique qu'est le bordereau des pieces et
> se voit attribué une quote et la quote / statement se voit attribuer une sous cote.
> L'utilisation d'une nouvelle quote ajoute la sous-quote au bordereau des preuve. de cette
> facons le bordereau se construit au fure et a mesure que la demonstration des paragraphes
> se construit et les documents, cistation et cote sont accessible de la requete et les cote
> sont calculée "on the fly" ce qui évite une renumérotation a chaque ajout d'un document ou
> d'une quote. l'odre des email devrait etre déterminer par le timestamp et l'ordre des quote
> par le nombre que caractére ou d'espace qui sépare son début de celui du text.

> 'aucune cote ne soit jamais tapée en dur dans un paragraphe, le paragraphe peut la
> déterminée dynamiquement par interogeant le model du bordereau. un document "produced" doit
> avoir un status "Draft" ou "Dépsé", un document déposé est figé, Le moodification d'un
> document déposé demeure possible, mais en travaillant sur une copie. Donc oui tu as raison,
> il doit y avoir un gel de verison au moment ou le status d'un document passe de Draft à
> déposé. Pour les liasses, évalue si je me trompe, mais elle sont "traduite" en
> démonstration. une liasse c'est un arbre, un ensemble d'élément de preuve. Pour le concept
> de document au niveau des courriels, donne moi ton avis. Le bloc de preuve est la citation
> (quote) et le parent de la quote est le courriel, en utilsant le courriel comme unité de
> document, le bordereau contiendra seulement les courriels qui nous servent, la quantité
> d'information est limité a ce qui nous est utile. Cela prive de context, limiet le risque,
> on fournnit a la demande. Pour E. L'ordre chronologique demande une règle de date par type.
> Oui, la regle est déja implantée dans la construction du bordereau, ce qui lui manque est
> l'endroit dans le text. un seul bordereau, mais versionable. Nous avons ce besoins, nous
> avons déposé un bordereau et nous ajoutons et retrirons des elements de preuves. une
> corespondance doit etre maintenue entre l'ancienne cote et la nouvelle. donc a chaque
> nouvelle version, une coresponsance doit existé de maniere qu'a travers 3 révision,
> l'historique de la cote d'un document qui apparait dans les 3 doit etre retracassable. Un
> document maintient sa PK dans le bordereau ce qui rend le travail trivial, c'est seulement
> son ordre chronologique qui change

> est il permis de référé la démonstration, qui elle refère aux preuves? c'est dire se servir
> de la hierarchie et utilisé le parent comme poigné pour manipuler l'ensemble? Le constat de
> juillet n'est il pas le document 9? La forme du statut d'un acte est sans importance, comme
> dans le cas d'une serie de version d'un meme logiciel, la demande, sa preuve, le bordereau
> doivent partagé un numéro de version une fois déposé / envoyé et être gelé dans le temps.
> [...] Quand tu réfères a preuve tu réfère a un aubre?

> pour le point 1) le bordereau présentera les piece de maniere chronologique, il ne sera pas
> possible d'abbrévier la présentation de la cote par "P-47 a P-52", n'est il pas permis de
> présenté un document intermédiare qui fait le pont entre la demande et le détail des
> preuves? ce document présenterait les découpages du bodereau chrnonologique en
> démonstration, sont role est d'isolé les elements du borderau pertinent a la démonstration,
> de masquer les éléments qui se rapportent a autre chose. Pour le point 2) je suis d'acccord
> avec ton constat, mais tu utilises des notions que nous avons développées dans le cadre
> d'une nouvelle architechture et tu les appliques à l'ancienne. Je ne suis pas certain du
> role de l'application case_manager dans le dernier dépot. J'ai en tete l'image suivante des
> modele impliqués, la demande est traduite dans le document_manager et un model spécial fut
> créé pour gerer la corespondance de l'ancien bordereau de preuve au nouveau.

---

## 1. Deux rives, un pont

| | Ce que c'est | Où cela vit |
|---|---|---|
| **Rive de la preuve** | les documents de preuve et leurs fragments | `email_manager` (courriels, citations), `pdf_manager` (PDF, citations), `events`, `photos`, `googlechat_manager` (messages, séquences), `video_manager`. Plus les **actes adverses reproduits** (`document_manager`, documents `REPRODUCED`), dont les énoncés sont des éléments de preuve |
| **Rive de la thèse** | les paragraphes qui construisent le grief | `document_manager` : les actes `PRODUCED` (dépôt de juillet, version 2…), leurs nœuds et leurs énoncés |
| **L'ancien pont** | tout ce qui relie les deux rives aujourd'hui | `argument_manager` (`TrameNarrative`, `Axe`, `Fait`, `AppuiFait`, `RattachementAxe`, `PerjuryArgument`) et `case_manager` (registres de pièces, appuis, confirmations, ancrages…) |
| **Le nouveau pont** | la chaîne paragraphe → démonstration → preuve → élément de preuve, et le **bordereau calculé** sur lequel repose son tablier (§3) | une application nouvelle, construite en parallèle |

**Une rive se définit par le rôle, pas par l'application.** `document_manager` porte les deux
rives à la fois : un acte `PRODUCED` est la thèse, un acte `REPRODUCED` est de la preuve. Le
pont peut donc relier un nœud de `document_manager` à un énoncé de `document_manager`.

### La règle de construction

> **Le nouveau pont ne dépend que des deux rives. Les rives ne dépendent d'aucun pont.**

Concrètement :
- la nouvelle application importe depuis les rives, jamais depuis `argument_manager` ni
  `case_manager` ;
- aucune rive n'importe la nouvelle application. Les liens vont du pont vers les rives (clés
  génériques). On remonte d'une rive vers le pont par une requête faite **dans** le pont ;
- c'est cette dépendance à sens unique qui rendra le décommissionnement possible sans toucher
  aux rives. Elle permettra aussi, un jour, de remplacer le pont à son tour.

### L'ancien pont est ancré dans les rives

La règle n'est pas respectée aujourd'hui : **plusieurs applications des rives importent l'ancien
pont.** Relevé du 2026-10-15, hors tests :

| Rive | Fichier | Ce qu'il importe de l'ancien pont |
|---|---|---|
| preuve | `email_manager/forms/quote/form.py` | `TrameNarrative` — le **formulaire de création de citation** |
| preuve | `email_manager/views/email.py`, `thread.py`, `quote.py` | `TrameNarrative`, `EvidenceDeleteMixin` |
| preuve | `pdf_manager/views.py` | `TrameNarrative`, `EvidenceDeleteMixin` |
| preuve | `events/management/commands/inventaire_events.py` | `BordereauDepotJuillet` |
| thèse | `document_manager/views/library_node_ajax.py`, `produced_views.py`, `new_views.py` | `TrameNarrative`, `PerjuryContestation`, `ExhibitRegistry` |
| thèse | `document_manager/referent.py`, `concordance.py`, `export_concordance.py`, `views/schema_views.py`, commandes `demonstration_e01` et `exporter_concordance` | `AppuiDepotJuillet`, `ConfirmationAppui`, `citations`, `cotes_concordance`, `appui_depot_service` |
| thèse | `document_manager/migrations/0003_…` | une dépendance de migration vers l'ancien pont |
| — | `core/views.py`, `protagonist_manager/views/model_views.py` | `TrameNarrative`, `LegalCase`, `ProducedExhibit`, services de rebuild |

À cela s'ajoutent, dans la rive de la thèse elle-même, les **80 nœuds de `LibraryNode` des
docs 5 et 6** qui pointent directement vers des citations. C'est un tronçon de l'ancien pont
logé dans une rive.

**Effet sur la construction :** aucun. Le nouveau pont n'a pas besoin de ces ancrages.
**Effet sur le décommissionnement :** c'est la liste des ancrages à couper. Le plus sensible est
le formulaire de création de citation : il lie aujourd'hui la création d'une citation à une
trame.

---

## 2. Les trois concepts

| Concept | Ce que c'est | Forme |
|---|---|---|
| **Élément de preuve** | un fragment d'une source : citation de courriel, citation de PDF, événement, énoncé d'un acte adverse, séquence de clavardage… | une feuille, sur la rive de la preuve ; sa source reste atteignable |
| **Preuve** | un ensemble ordonné d'éléments | un arbre par preuve, hiérarchie et ordre entre frères ; **réutilisable** |
| **Démonstration** | un ensemble de preuves | reliée au paragraphe, sur la rive de la thèse |

```
RIVE DE LA THÈSE                           LE PONT                              RIVE DE LA PREUVE
paragraphe ──► démonstration ──► preuve (arbre) ──► élément de preuve ──► document
(nœud d'un acte                                       (citation, événement,   (courriel, PDF, événement,
 PRODUCED)                                             énoncé, séquence)       acte reproduit, séquence)
```

Le paragraphe n'atteint jamais un document directement : il passe toujours par une
démonstration.

**Provenance et utilisation dans une cause (LP, 16 octobre 2026).** Un paragraphe
d'un acte adverse peut faire partie d'un arbre de preuve associé à la nouvelle
cause. Le nœud de preuve référence ce paragraphe dans son document d'origine;
ce document conserve sa cause d'origine. L'arbre est utilisé dans la nouvelle
cause par la démonstration et la version d'acte auxquelles il est associé.
Voir [ARCHITECTURE_CAUSES.md, §3.1](ARCHITECTURE_CAUSES.md#31-un-paragraphe-dune-autre-cause-dans-larbre-de-preuve).

**Technique.** `django-treebeard` 4.8 est déjà installé et fournit le nested set (`NS_Node`) et
le chemin matérialisé (`MP_Node`), avec la même API. Les deux donnent la hiérarchie et l'ordre
entre frères. `LibraryNode` utilise `MP_Node`. À cette échelle, le choix est sans enjeu.

---

## 3. Le bordereau, culée du pont

### 3.1 La proposition (LP, 2026-10-15)

- Le tablier du pont repose sur le **bordereau des pièces**, qui **uniformise la provenance** des
  éléments de preuve.
- Dès qu'un élément est utilisé (citation, énoncé, événement, séquence de clavardage), son
  **document entier** entre au bordereau et reçoit une **cote**. La citation ou l'énoncé reçoit
  une **sous-cote**.
- Le bordereau se construit **au fur et à mesure** des démonstrations. Les cotes sont
  **calculées à la volée**. Les documents sont ordonnés par leur horodatage, les citations par
  leur position dans le texte de leur source.

### 3.2 Décisions arrêtées (LP, 2026-10-15)

| Décision | Contenu |
|---|---|
| **Aucune cote en dur** | Le paragraphe obtient sa cote en interrogeant le bordereau. |
| **Statut de l'acte** | Un acte `PRODUCED` est soit en **brouillon**, soit **déposé**. Un acte déposé est figé. Pour le modifier, on travaille sur une copie. La forme du statut importe peu. |
| **Version partagée** | Comme les versions successives d'un logiciel : une fois déposés ou envoyés, **la demande, sa preuve et le bordereau partagent un même numéro de version** et sont gelés ensemble. |
| **Un seul bordereau, versionné** | Une correspondance relie chaque version à la précédente. La cote d'un document se retrace à travers toutes les révisions. Le document garde son identité (modèle + PK) ; seul son rang change. |
| **Liasses** | Une liasse se traduit en un arbre d'éléments de preuve dans le pont. |
| **Unité de document d'une citation de courriel** | Le courriel. Le bordereau ne contient que les courriels qui servent ; le reste se fournit sur demande. |
| **Ordre** | La règle de date par type existe déjà. Il manque la position de la citation dans le texte de sa source. |
| **La culée appartient au pont** | Le bordereau se calcule depuis les démonstrations. La rive ne fournit que les dates et les positions. |
| **Aucun verbatim en dur** (2026-10-15) | Le passage cité dans un paragraphe est **rendu depuis l'élément**, comme la cote. |
| **L'unité minimale suffisante** (2026-10-15) | Si une citation ou un groupe de citations (un arbre de preuve) suffit, c'est elle qu'on utilise, rendue depuis l'élément. Le document entier n'est l'élément que si rien de plus petit ne suffit. LP estime que 90 % des cas se règlent par une phrase ou un ensemble de phrases. |
| **Les actes adverses se citent au paragraphe** (2026-10-15) | Pour P-19, P-40 et P-42, l'unité est l'énoncé (`Statement`), pas la phrase. |

### 3.3 Ce qui est juste, et ce qui existe déjà

- **Uniformiser, construire par l'usage, calculer.** Le bordereau contient exactement ce que
  les paragraphes invoquent : ni pièce orpheline ni cote fantôme.
- **L'identité par modèle + PK rend la correspondance triviale**, puisqu'elle devient une
  jointure. Le bordereau gelé de juillet désigne déjà ses 268 pièces par modèle + PK
  (`legal/depots/2026-07-24_initial/`, transcrit dans `BordereauDepotJuillet`). Il peut devenir
  la première version du bordereau versionné (§4).
- **Le statut et le gel existent déjà sur la rive de la thèse.**
  - `ReferentHistorique` : « Ce document est un acte déposé : son contenu ne se modifie plus ».
    Les gardes le consultent avant d'écrire.
  - `InstantaneReferent` / `InstantaneNoeud` : les instantanés.
  - Le doc 10 « version 2 » est déjà la copie de travail du doc 9 déposé.

  « Déposé » équivaut donc à « porte un `ReferentHistorique` ». Rien n'est à inventer de ce
  côté, et la forme du statut importe peu (LP). Ce qui manque, c'est le **numéro de version
  partagé** avec le bordereau et la preuve.
- **La règle de date est sur la rive.** `get_exhibit_date()` est défini sur chaque modèle de
  pièce (courriel, fil, PDF, acte, événement, photo, document photo).
- **Le courriel comme unité de document : je suis d'accord.**
  - C'est le parent naturel de la citation.
  - C'est l'unité d'auteur, d'expéditeur et de date. Un fil mêle plusieurs auteurs et plusieurs
    dates, et sa place dans la chronologie est mal définie.
  - Il réduit ce qui est communiqué à ce qui sert.
  - Pour 40 fils, la base ne contient que les répliques de LP : le courriel y est de toute façon
    la seule unité disponible.

  Une réserve, au point 5 du §3.4.

### 3.4 Points de vigilance

**1. Le gel porte sur une version entière, et il descend toute la chaîne.** La version partagée
(§3.2) se comprend comme en logiciel. Le brouillon est la **branche de travail**. Le dépôt ou
l'envoi pose une **étiquette** qui fige ensemble trois choses :
- l'acte, sur la rive de la thèse ;
- ses démonstrations et ses preuves, dans le pont ;
- le bordereau calculé à ce moment, dans le pont lui aussi.

Un acte déposé se rend donc avec les cotes de **sa** version, pas avec le calcul courant. Sa
requête au bordereau n'est pas « quelle est la cote de ce document ? », mais « quelle était sa
cote dans ma version ? ».

**Règle proposée : une démonstration ou une preuve qu'utilise une version gelée ne se modifie
plus. La modifier, c'est en faire une copie.** Par « preuve », on entend l'**arbre entier** :
ses nœuds, leur ordre et les éléments vers lesquels ils pointent. Le geler, c'est geler ces
trois choses. Une copie mémorise l'objet **dont elle est issue**, comme
`ConfirmationAppui.issu_de` : l'histoire d'une preuve se retrace à travers les versions, comme
celle d'une cote. Les éléments eux-mêmes (les citations) ne se copient pas. Ils sont sur la
rive, et c'est le journal de redirection qui les protège (point 2).

Copier un acte (doc 9 → doc 10) ne copie rien d'autre. Les paragraphes de la copie pointent
vers les mêmes démonstrations, qui sont gelées. C'est la première modification qui fait la
copie, et seulement de ce qu'elle touche.

**2. La PK d'un document est stable ; celle d'une citation ne l'est pas.**
- Courriels et PDF gardent leur PK (le courriel a même une clé naturelle, `message_id`).
- Les citations sont supprimées et recréées, et bientôt fusionnées. `CARTE_RELATIONS.md` le
  constatait déjà : « Les PK de quotes ne sont pas, et n'ont jamais été, des identifiants
  stables ».

Supposons qu'une version gelée donne la sous-cote P-12.2 à pq-83, et que la fusion remplace
ensuite pq-83 par pq-75. La correspondance perd sa trace. Il faut donc deux choses :
- **un journal de redirection** tenu par la fusion (pq-83 → pq-75), que la correspondance
  consulte ;
- **ne plus supprimer une citation utilisée par une version gelée**, mais la rediriger.

Enfin, « PK » veut toujours dire **modèle + PK** : le courriel 12 n'est pas le PDF 12.

**3. Deux cas de correspondance ne sont pas 1 → 1.** Quand l'unité de document change, la PK
cesse d'être partagée.
- **Les 4 fils entiers de juillet** (P-4, P-14, P-24, P-27). Dans le nouveau bordereau, seuls
  les courriels utilisés de chaque fil y figurent. Une cote de juillet correspond donc à N
  cotes nouvelles.
- **Les 30 liasses.** Leurs 192 documents ont chacun leur PK, et leur correspondance est
  triviale. Mais la cote racine « P-43 » était citée **en bloc** par 198 des 515 appuis de
  juillet. Elle correspond à N cotes nouvelles.

La concordance doit donc admettre le cas 1 → N.

**4. Les liasses : juste sur le fond, avec une nuance et deux conséquences.**
- **La nuance.** Par la définition même de LP, « un arbre, un ensemble d'éléments de preuve »,
  une liasse est une **preuve**. Une démonstration, elle, réunit des preuves. La liasse se
  traduit donc en preuve, qu'une ou plusieurs démonstrations utilisent.
- **Le bordereau s'allonge.** Les 268 pièces de juillet tenaient sous 106 cotes. Chacune en
  aura une, soit environ 2,5 fois plus de cotes.
- **Le rendu dans le paragraphe.** 20 des 30 liasses de juillet sont dispersées dans la
  chronologie (E01, T25). Une telle preuve, rendue en cotes chronologiques individuelles,
  donnera une liste discontinue (« P-43, P-47, P-52… ») là où juillet écrivait « P-43 ».

**La démonstration comme poignée (question de LP).** Dans le modèle, oui : le paragraphe tient
la démonstration, et manipuler le parent, c'est manipuler l'ensemble. Ajouter un document à la
preuve met à jour tous les paragraphes qui la citent. Dans le **texte déposé**, la poignée doit
toutefois se résoudre en quelque chose que le lecteur peut retrouver. Le tribunal et la partie
adverse n'ont que le bordereau : ils ne connaissent pas les démonstrations. Deux voies :
- **la poignée reste dans le modèle, le texte en montre le développement.** C'est la liste des
  cotes, avec les suites compressées : « P-43, P-47 et P-52 », « P-43 à P-47 ». Rien ne
  contraint la réutilisation ;
- **la preuve devient elle-même une entrée du bordereau** : une liasse avec sa cote et ses
  sous-cotes, citable d'un mot (« P-43 »), comme en juillet. Mais un document ne peut porter
  qu'une cote. Une preuve réutilisée qui partage un document avec une autre preuve-liasse
  donnerait deux cotes au même document. Cette voie impose donc qu'un document n'appartienne
  qu'à une seule preuve-liasse.

Dans un bordereau chronologique, les documents d'une démonstration sont rarement contigus. La
compression « P-43 à P-47 » sera donc l'exception. LP propose une troisième voie.

**Le document intermédiaire (proposition de LP, 2026-10-15).** C'est un document placé entre la
demande et le détail des preuves. Il présente le bordereau chronologique **découpé en
démonstrations**. Pour chacune, il isole les pièces qui la concernent et masque celles qui
servent à autre chose. C'est la poignée, rendue visible au lecteur.

**Ce que dit le Code (texte local, C.p.c. à jour au 24 octobre 2025) :**
- **Art. 247** : les pièces au soutien d'un acte de procédure « sont indiquées » **« dans
  celui-ci ou dans un avis qui y est joint »**. Le Code ne prévoit pas d'autre véhicule.
- **Art. 99** : l'acte expose ses énoncés « avec clarté, précision et concision, dans un ordre
  logique ». Il doit aussi indiquer « tout ce qui, s'il n'était pas énoncé, pourrait surprendre
  une autre partie ».
- Le texte du Code ne contient ni « tableau » ni « cahier ». Rien n'y interdit un tel document,
  mais rien ne lui donne de statut propre.

**Lecture qui en découle :**
- **Sa place sûre est à l'intérieur de l'acte**, en annexe faisant partie de la demande
  (« Annexe A — Pièces par démonstration »), ou dans l'avis de pièces joint. C'est là que
  l'art. 247 veut que les pièces soient indiquées. Le paragraphe peut alors renvoyer à la
  démonstration (« tel qu'il appert des pièces de la démonstration 3, annexe A »), et l'annexe
  en donne les cotes. Notifié comme document autonome, son statut serait incertain : ce n'est
  ni un acte de procédure, ni une pièce.
- **Ce n'est jamais une pièce.** Il est construit par la partie : le coter comme pièce ferait
  appuyer une allégation sur un document de son propre auteur.
- **Ses intitulés restent neutres.** En annexe de l'acte, ils se lisent comme des énoncés de
  l'acte. La règle de l'exposé des faits vaut pour eux : « zéro qualificatif »
  (`legal/poursuite_expose_des_faits.md`). Les qualifications (fausseté, mauvaise foi…)
  relèvent des moyens.
- **Il se génère depuis le pont** (démonstration → preuves → documents → cotes) et **se gèle
  avec la version**. Il partage le numéro de version de la demande et du bordereau.
- **Une limite de lecture.** Le renvoi à l'annexe ajoute une étape au lecteur. Quand une
  démonstration ne compte que deux ou trois pièces, mieux vaut les nommer directement dans le
  paragraphe.

**Décision reportée (LP, 2026-10-15).** La forme du document intermédiaire se décidera une fois
la demande, les citations, le bordereau, les preuves et les démonstrations complétés, au vu du
portrait qu'ils tracent. L'analyse ci-dessus servira alors de point de départ. Le modèle n'en
dépend pas : la poignée existe de toute façon, puisque le paragraphe tient la démonstration.

**5. Le courriel comme unité : oui, à une condition.** « Fournir le contexte sur demande » ne
suffit pas quand le message auquel le courriel répond **change le sens** de la citation. Ce
message doit alors être produit aussi, comme pièce à part entière. C'est le critère que le
dossier oppose lui-même à la partie adverse : un énoncé vrai dont on omet le contexte
déterminant donne une appréciation fausse. Un bordereau qui omettrait un contexte déterminant
s'exposerait au même reproche. Souvent, le corps du courriel cite déjà le message précédent
(lignes « > »), ce qui couvre une partie des cas.

**6. La règle de date : sur la rive, sauf deux morceaux restés dans l'ancien pont.**
- La date d'une séquence de clavardage (`start_date`, ou à défaut le premier message) est
  calculée dans `case_manager/cotation_service.horodatage`, et non sur le modèle.
- Le marqueur « atemporelle » est un champ de `BordereauDepotJuillet`. Le seuil « à dater »
  (`PLANCHER`, an 2000) est dans `cotation_service`.

Pour respecter la règle d'indépendance, ces deux morceaux doivent passer sur la rive : un
`get_exhibit_date()` sur `ChatSequence`, et un marqueur « atemporel » sur les modèles de
pièces. S'y ajoute un défaut dangereux : `Document.document_original_date` vaut
`default=timezone.now`. Un acte créé sans date reçoit la date du jour, sans que rien ne le
signale.

**7. La position dans le texte : à ajouter sur la rive.** Elle se stocke sur la citation et se
recalcule quand le texte change. Elle suppose la citation localisable, et 48 ne le sont pas
aujourd'hui : le ménage des citations est un préalable (§6).

---

## 4. Ce que le nouveau pont remplace

**Tout l'ancien pont** (décision de LP, 2026-10-15). La décision vaut pour la fonction de
liaison, et le remplacement se fera **après** la mise en service du nouveau pont :

| Ancien | Ce qu'il faisait | Où sa fonction passe |
|---|---|---|
| `TrameNarrative` | sac non ordonné d'énoncés visés et de preuves | démonstration + preuves |
| `Axe` → `Fait` → `AppuiFait` | liste ordonnée de pièces entières, avec un rôle, par paragraphe | démonstration + preuves |
| `ConfirmationAppui` | paragraphe → pièce, avec portée et état | le lien paragraphe → démonstration |
| `RattachementAxe` | triage : « cette pièce concerne cet axe » | à discuter (§5) |
| `ExhibitRegistry`, `ProducedExhibit`, `cotation_service`, `AncrageCitation` | numérotation des pièces, rendu des cotes dans le texte | **le bordereau versionné** (§3) |

### Le dépôt de juillet, dans les termes de l'ancienne architecture

*Corrigé le 2026-10-15. La version précédente de cette section appliquait à l'ancienne
architecture des notions de la nouvelle (« version 1 », « pont »). Voici ce que le code et
l'archive établissent.*

**Ce qui a été déposé.** Une **copie papier** de la demande et du bordereau, remise au comptoir
du greffe de Longueuil le 24 juillet 2026 à 15 h 19 (dossier 505-17-016235-261). Aucun fichier
n'a été transmis. Le référent officiel est le papier.

**Ce qui le conserve, dans l'ordre où cela a été fait :**

| Date | Quoi | Où | Rôle |
|---|---|---|---|
| 24 juillet | sources d'impression gelées : la demande (md, docx, pdf), le bordereau (md, docx), `cotes.lock.json`, `SHA256SUMS`, `preuve_de_depot.pdf` | `legal/depots/2026-07-24_initial/` (commit `1f0af56`) | **la référence**. Le travail postérieur vit dans `legal/amendements/` |
| avant le dépôt | PDF des pièces et cahier de pièces, générés depuis le bordereau markdown | commandes `sync_pieces`, `sync_pieces_pdf` et `build_cahier_pieces` de `case_manager` | **outillage** : `case_manager` a produit les livrables, il ne portait pas la cotation |
| 12 août | `BordereauDepotJuillet` : la cote de juillet de chaque pièce (modèle + pk), liasses développées | `case_manager`, importé du bordereau **gelé** | **le modèle spécial dont LP se souvient** : il sert à traduire l'ancienne cotation vers la nouvelle (`traduire_cotes`) |
| 19 août | `AppuiDepotJuillet` : quel paragraphe invoque quelle cote, extrait du texte (« tel qu'il appert de la pièce P-49.2 ») | `case_manager` (`persister_appuis_depot`) | relevé de ce que le texte plaidait. Il ne lit aucun `Fait`, `Axe` ni `AppuiFait` |
| — | la demande transcrite | `document_manager`, **doc 9**, figé par `ReferentHistorique`, qui pointe le fichier gelé et son empreinte | la demande dans la base |
| 14 octobre (E01) | concordance des paragraphes doc 9 ↔ doc 10 (`Correspondance`), cote du pont, `ConfirmationAppui`, `AncrageCitation` | `document_manager` et `case_manager` | travail de la version modifiée |

**L'image de LP est juste.** La demande est traduite dans `document_manager` (doc 9).
`BordereauDepotJuillet` est le modèle spécial créé pour la correspondance de l'ancien bordereau
vers le nouveau. `ExhibitRegistry` et `TrameNarrative` n'ont pas produit le bordereau de juillet.

**Pour la nouvelle architecture.** Ce qui a été déposé existe déjà comme un ensemble gelé : la
demande et le bordereau ensemble, avec empreintes et verrou des cotes. La « version partagée »
du §3.2 est donc déjà pratiquée, sous forme de fichiers. **Le doc 9 est gelé et reste où il
est** : rien ne se copie de la demande.

**Ce que ce choix remplace.** Le verrou du 27 juillet posait quatre règles :
1. une cote conserve toujours la même source ;
2. une cote retirée n'est jamais réaffectée ;
3. toute nouvelle pièce reçoit P-107 ou la suivante ;
4. un changement de description n'altère pas l'identité.

Le bordereau versionné et chronologique **remplace les règles 2 et 3 pour les versions à
venir** : d'une version à l'autre, une cote peut désigner une autre pièce, et une pièce ajoutée
prend son rang chronologique. La règle 1 ne vaut plus qu'**à l'intérieur d'une version**. La
règle 4 reste entière. La correspondance par modèle + PK est ce qui rend ce changement sûr.

**Ce qui découle de l'exigence de LP.** LP exige une correspondance entre l'ancienne cote et la
nouvelle, retraçable sur plusieurs révisions (§3.2). Le bordereau versionné du nouveau pont doit
donc **commencer par la cotation de juillet** : pour chaque pièce, son modèle + PK et sa cote de
juillet. Sans elle, la correspondance juillet → version 2 n'a pas de point de départ dans le
pont.

**Elle est déjà en base (rappel de LP, 2026-10-15) : on la lit dans `BordereauDepotJuillet`.**
Contenu relevé ce jour :

| | Lignes | Ce que c'est |
|---|---|---|
| colonne `cote` renseignée | 268 (106 cotes racines) | **la cotation de juillet**, importée de la copie gelée |
| colonne `cote` vide | 66 (62 courriels, 2 PDF, 1 événement, 1 document photo) | pièces versées **après** le dépôt. Elles n'ont aucune cote dans la table : la leur se calcule (`traduire_cotes`) |
| colonne `cote_pont` | 268, **toutes identiques** à la cote de juillet ; 0 ligne de précision | la cotation de travail d'E01, jamais divergée |

**Contrôle contre le verrou** (`cotes.lock.json`, 106 cotes) : les 106 cotes racines
concordent. Seules quatre désignent un objet différent : P-1, P-8, P-15 et P-101. Le verrou y
nomme une photo, la table le document photo qui la contient. Ce sont les quatre équivalences de
contenant établies et vérifiées par E01.

**Règle d'import.**
- Un script **ponctuel**, placé hors de la nouvelle application, lit la colonne `cote` (268
  lignes) et crée la version de juillet du bordereau versionné.
- La nouvelle application n'importe jamais `case_manager`. Une lecture faite une fois ne crée
  pas de dépendance durable : l'indépendance est préservée.
- On ne reprend ni `cote_pont` (cotation de travail de l'ancien pont), ni les 66 pièces versées
  après le dépôt. Celles-ci entrent au bordereau de la version 2 si une démonstration les
  utilise, comme toute pièce.

Les paragraphes du doc 9 n'ont pas besoin de démonstrations dans le nouveau pont : ils citent
leurs cotes dans leur texte, et ils sont gelés.

Au décommissionnement, ni l'archive gelée ni le doc 9 ne sont concernés. Les tables de
`case_manager` qui les transcrivent ne sont plus que des copies.

---

## 5. Questions ouvertes

**Sur le bordereau :**

1. **La forme du document intermédiaire** (§3.4, point 4) : **reportée** (LP, 2026-10-15).
   Elle se décidera une fois la demande, les citations, le bordereau, les preuves et les
   démonstrations complétés, au vu du portrait qu'ils tracent.

**Sur la chaîne** (recommandations du 2026-10-15, à trancher par LP) :

2. **Où vivent l'objet, le rôle, la portée et l'état.**
   - **Chaque preuve énonce son objet** : ce qu'elle établit, en termes factuels, sans
     qualificatif (« Le demandeur a offert la garde partagée en avril 2015 »). C'est ce qui
     permet de la retrouver et de la réutiliser. Sans objet, une preuve redevient un sac,
     comme `TrameNarrative`. C'est l'équivalent de `Fait.enonce` dans l'ancien pont.
   - **Le rôle** (attestation, cadre, inférence, vérification, illustration) est porté par
     **l'élément dans la preuve**, relativement à l'objet de celle-ci. C'est ce que faisait
     `AppuiFait.role` relativement au fait. Il suit la preuve quand elle est réutilisée. Le
     nouveau pont redéfinit ces valeurs chez lui.
   - **La portée, l'état de confirmation et la version examinée** sont portés par le **lien
     paragraphe → démonstration**. La même démonstration peut établir des choses différentes
     pour deux paragraphes.
3. **Réutiliser, puis modifier.** ✅ **Retenu par LP le 2026-10-15**, étendu par la copie du
   chemin (§8.2, point 2). Proposition (§3.4, point 1) : une démonstration ou une
   preuve (l'arbre entier) qu'utilise une version gelée ne se modifie plus. La modifier, c'est
   en faire une copie, qui mémorise l'objet dont elle est issue. Tant qu'aucune version gelée
   ne l'utilise, elle se modifie librement, et les liens qui l'avaient confirmée retombent
   « à réexaminer ».
4. **Le triage : pas de modèle à part.** Une preuve qui n'est encore rattachée à aucune
   démonstration **est** l'état de triage : elle a un objet et des éléments, mais ne sert
   encore aucun paragraphe. Elle n'entre pas au bordereau, qui se construit par l'usage.
5. **Les cardinalités.**
   - **Un paragraphe a au plus une démonstration. Une démonstration peut servir plusieurs
     paragraphes**, par exemple un bloc comme les §§ 14-18. Le lien porte la portée propre à
     chaque paragraphe. Si un paragraphe a besoin de deux lignes de preuve, sa démonstration
     contient deux preuves. Le rendu reste simple : un paragraphe, une démonstration, ses
     cotes.
   - **Une démonstration est une liste ordonnée de preuves.** L'arbre vit dans la preuve.
   - ⚠️ *Retiré après l'épreuve des axes (§8.2, points 2 et 3) : une démonstration tient des
     poignées vers des nœuds à tout niveau, et une preuve peut renvoyer à une autre.*
   - ~~**Une preuve ne contient pas d'autre preuve, du moins au départ.**~~ La réutilisation se
     fait au niveau de la démonstration, qui assemble des preuves. Permettre l'imbrication
     ajouterait des copies et des gels en cascade : copier une sous-preuve forcerait à copier
     chaque preuve gelée qui la contient. On l'ajoutera si un cas réel le demande.
6. **Le contenu de l'ancien pont : partir vide, sauf les faits.**
   - Les **12 faits** (2 axes : la danse, le soccer d'Alexia à l'été 2013), tous rattachés à
     des paragraphes du doc 9, deviennent par un import ponctuel **12 preuves en triage**.
     L'objet de chacune reprend l'énoncé du fait, et ses éléments reprennent les 34 appuis avec
     leur rôle. Leurs `raison` (9) se conservent en note. Les appuis qui désignent un courriel ou
     un PDF entier seront ensuite ramenés à leurs phrases (unité minimale suffisante).
   - **`TrameNarrative`** (65) : non reprise, jugée sans valeur en août.
   - **`ConfirmationAppui`** (1) : refaite à la main.
   - Les **appuis de juillet** (515) servent de matière à la version 2 (§7).

**Acquis :**
- les décisions du §3.2 ;
- le paragraphe est une **occurrence**, c'est-à-dire un `LibraryNode` et non un `Statement` :
  un même énoncé repris dans deux actes peut n'y être pas appuyé pareil (décision d'E01).

---

## 6. Effets sur le ménage des citations

- **Le ménage est de l'entretien de rive, et un préalable au bordereau.** Les citations sont sur
  la rive de la preuve. Leur ménage ne dépend d'aucun pont, et il sert les deux : la fusion
  repointe toute référence, dans l'ancien pont comme dans le nouveau. Le scanner de clés
  génériques de la fusion doit donc connaître le nouveau modèle, puisqu'il refuse les modèles
  inconnus.
- **La fusion tient un journal de redirection** (citation absorbée → citation qui survit). Sans
  ce journal, la correspondance des sous-cotes entre versions du bordereau se perd (§3.4,
  point 2).
- **La position de la citation dans sa source devient une donnée de la rive.** On la stocke et
  on la recalcule quand le texte change (§3.4, point 7).
- **L'objection au passage de 1 à N tombe pour le nouveau pont.** Scinder une citation en N
  phrases revient à remplacer une feuille par N feuilles sœurs dans l'arbre d'une preuve. La
  règle stricte de LP, « une citation est une phrase », redevient praticable
  (`PLAN_FUSION_CITATIONS.md` §3.2). En contrepartie, chaque phrase recevrait sa sous-cote.
- **La composition trouve sa place.** En août, elle relevait de la couche `.md`. Elle appartient
  désormais à la preuve. Les citations restent atomiques.
- **La sous-cote d'un passage se calcule depuis le bordereau** au lieu d'être stockée
  (`PLAN_FUSION_CITATIONS.md` §4.4, suspendu).

---

## 7. La traduction de juillet

### 7.1 La proposition (LP, mot pour mot)

> confirme ou infirme ceci : une étape du projet serait de traduire le bordereau de juillet
> dans le nouveau model de bordereau, cette traduction consisterait a déterminer les pieces et
> les quote utilisé dans la demande juillet, le verbatime est utilisé dans la demande même, il
> n'est cependant pas garantit que le verbatime sois exact, nous avons établit qu'a l'avennir
> une quote est une phrase. la traduction consiste alors a utilisé la phrase non tronqué et si
> un verbatime est composé de plsieurs phrase dans la demande, il faudra scinder le verbatime
> en ses phrase individuel et reconstruire le raisonement en utiisant le model de preuve.

**Décision enregistrée : une citation est une phrase, au sens strict** (LP, 2026-10-15). Cela
tranche la question que le modèle Preuve avait rouverte (`PLAN_FUSION_CITATIONS.md` §3.2). Les
précisions de la règle (énumérations, « : », retours à la ligne, §3.3 du plan de fusion)
restent à arrêter avant toute application mécanique.

### 7.2 Mesures sur le doc 9

| | |
|---|---|
| paragraphes appuyés par au moins une pièce (`AppuiDepotJuillet`) | 148 (515 liens) |
| — dont avec un passage cité entre « » | **46** |
| — dont **sans** passage cité | **102**, qui portent **394 des 515 liens** |
| passages entre « » dans tout le doc 9 | 66 (65 dans la source gelée) |
| — dont de plusieurs phrases | **0** |
| — plus long passage de 4 mots ou plus | 144 caractères |

Les 394 liens sans verbatim se répartissent ainsi : courriels 114, PDF 109, événements 90,
actes 56, documents photo 12, fils 8, clavardage 5.

### 7.3 Verdict

**Confirmé :**
- **L'inventaire est une étape nécessaire** : pour chaque paragraphe de juillet, les pièces et
  les passages qu'il invoque.
- **Le verbatim de juillet n'est pas fiable.** L'audit du 8 octobre a relevé une trentaine de
  citations inexactes. Leurs corrections sont dans
  `legal/amendements/01_avant_notification/demande_amendee.md`. Chaque passage se reprend donc
  **sur l'original** : la base pour les courriels et le clavardage, le scan pour P-19, P-40 et
  P-42. Jamais sur le texte de la demande ni sur la fiche.
- **L'élément est la phrase entière de la source.**
- **Un passage de plusieurs phrases devient plusieurs éléments**, assemblés dans l'arbre d'une
  preuve. C'est exactement ce que le modèle permet.

**À corriger :**

1. **Le bordereau de juillet ne se traduit pas : il s'importe tel quel.** Il reste au niveau des
   pièces, avec les cotes et les liasses de juillet (§4). Ce que LP décrit est la traduction des
   **appuis** de juillet (paragraphe → pièce → passage) en chaînes du nouveau pont. Or ces
   chaînes appartiennent à la **version 2** : le doc 10 et l'atelier `legal/redaction_v2/`.
   Elles n'appartiennent pas à la version de juillet. Écrire des phrases et des sous-cotes dans
   la version de juillet fabriquerait un juillet qui n'a jamais été déposé : il n'avait aucune
   sous-cote de passage, et ses citations inexactes sont un fait de l'acte déposé.
2. **Le cas de la scission ne se présente pas dans juillet.** Aucun des 66 passages ne compte
   plusieurs phrases. Le cas réel est **l'inverse** : ce sont presque tous des **fragments** de
   phrase. La traduction **étend** donc chaque fragment à sa phrase, et le paragraphe de la
   version 2 **affiche la phrase entière** (§7.5).
3. **L'essentiel du travail n'est pas dans le verbatim.** 102 des 148 paragraphes appuyés ne
   citent rien. Ils portent 394 liens. Pour les événements et les photos, le document est
   lui-même l'élément. Pour les courriels, les PDF et les actes (279 liens), il faut **lire
   pour trouver la phrase qui appuie le paragraphe**, ou admettre le document entier comme
   élément (§5, question 7). C'est le cœur de l'étape.
4. **Les actes adverses se citent au paragraphe.** P-19, P-40 et P-42 (docs 1 à 3) sont cités
   par numéro (« § 14 de la Requête »). Leur unité naturelle est l'énoncé (`Statement`), pas la
   phrase. La règle de la phrase vaut pour les courriels, les PDF et le clavardage. L'étendre
   aux actes demanderait un élément de niveau phrase sur les énoncés, qui n'existe pas.
   **Recommandation : le paragraphe reste l'unité pour les actes.**
5. **Le raisonnement à reconstruire est celui de la version 2.** L'atelier a réécrit des blocs
   entiers (20 à 24). L'inventaire de juillet fournit la matière, pas le plan.

### 7.4 Une proposition qui découle de « aucune cote en dur »

Les citations inexactes de juillet viennent toutes du même geste : le verbatim a été **tapé**
dans le paragraphe. Si le passage cité dans le paragraphe est **rendu depuis l'élément**, comme
la cote (avec `[…]` quand le paragraphe n'en cite qu'une partie), il ne peut plus diverger de
l'original. **Retenu par LP le 2026-10-15** (§7.5).

### 7.5 Décisions de LP (2026-10-15) et ce qu'elles entraînent

| Question | Décision |
|---|---|
| Le verbatim dans le paragraphe | **Rendu depuis l'élément**, comme la cote |
| Un courriel ou un PDF cité sans passage | **L'unité minimale suffisante** : une phrase ou un arbre de phrases dans environ 90 % des cas ; le document entier seulement si rien de plus petit ne suffit |
| Les actes adverses | **Le paragraphe** (`Statement`) reste l'unité |

**Conséquence n° 1 : l'exactitude se vérifie une fois, sur l'élément.** Puisque le paragraphe
reproduit l'élément, une erreur dans l'élément passe telle quelle dans l'acte. Le texte de
l'élément doit donc être **certifié sur l'original avant tout usage**. *Tableau corrigé le
2026-10-15 après vérification.*

| Source | Texte de l'élément | État relevé | Ce qui reste à faire |
|---|---|---|---|
| courriel, clavardage | `body_plain_text`, `ChatMessage.text_content` | la base est l'original | rien : vérification mécanique |
| PDF natif | `ai_analysis`, « extraction directe de la couche texte, fiabilité : exacte » | **37 PDF** dont la couche texte est le texte d'origine | rien |
| PDF scanné avec couche OCR du numériseur | `ai_analysis`, même en-tête « exacte » | **3 PDF : pdf-3, pdf-7, pdf-8** (16 citations). « Exacte » y signifie « fidèle à la couche OCR », pas à la page : la couche de pdf-3, produite par un numériseur Canon, porte « savotr » | lire sur l'image les phrases utilisées |
| PDF lu visuellement | `ai_analysis`, « lecture directe du document, fiabilité : relue, réserves signalées » | **7 PDF** (5 cités) | relire les réserves signalées |
| PDF sans transcription | `ai_analysis` vide | 48 PDF, dont **4 portent des citations** | transcrire ces 4 |
| **articles académiques** (type « Scholarly Article ») | — | 8 PDF, sans transcription, **aucune citation** | **rien : hors preuve, jamais réécrits** (consigne de LP) |
| acte adverse (P-19, P-40, P-42) | texte de l'énoncé (docs 1 à 3) | voir ci-dessous | comparer chaque énoncé utilisé au scan |

**Les actes adverses.** L'audit du 8 octobre a confronté aux scans les **94 occurrences
citées** par la demande déposée (`journal_modifications.md`). Il n'a pas comparé un à un les
énoncés de la base. Au passage, il a relevé quatre écarts dans la **fiche P-42**
(`legal/piece_document-3.md`, la déclaration assermentée de la demanderesse du 21 octobre 2019,
doc 3) : § 6 c), § 8, § 16 et § 18. Contrôle de ce jour : **les énoncés du doc 3 partagent deux
de ces écarts** :
- § 6 c) : « refuse » en base, « refusent » à l'original ;
- § 8 : « de 1341,87 » en base, « de1341,87 » à l'original.

Ils sont conformes au § 16 et au § 18. Les énoncés de la base ne sont donc pas certifiés.

La garde qui en découle (retenue par LP) : **un élément non certifié ne se rend pas dans un
acte**. Il apparaît signalé, comme une cote non résolue bloquait l'export strict en E01.

**Conséquence n° 2 : pas de coupe, ni dans la base ni au rendu.** *Corrigé le 2026-10-15.* La
version précédente de ce paragraphe faisait porter au lien paragraphe → élément une portion de
phrase, rendue avec `[…]`. C'était contraire à la décision : **l'unité est la phrase complète,
sans troncature**. Le paragraphe affiche donc toujours la phrase entière. Le lien ne porte
aucune portion, et ni `[…]` ni `[x]` n'ont lieu d'être. Ces conventions restent celles des
citations **tapées** de l'ancien régime (`demande_amendee.md`).

**Conséquence n° 3 : la version de juillet garde son texte tapé.** Le doc 9 est gelé. Ses
citations, exactes ou non, sont ce qui a été déposé, et le rendu depuis l'élément ne s'applique
qu'aux versions à venir.

**Un exemple de document entier comme élément** (LP n'en voyait pas) : quand le fait à établir
est **l'existence, la date ou l'envoi** du document, et non ce qu'il dit. Par exemple : « Le
demandeur a écrit à la défenderesse le 22 juin 2020 ». C'est l'en-tête et l'horodatage qui
prouvent, pas une phrase du corps. C'est aussi le cas naturel des événements et des photos.


---

## 8. Mise à l'épreuve : la danse, la garderie, la fréquence de la présence

Demande de LP (2026-10-15) : examiner ce qui constitue l'axe de la danse, puis celui de la
garderie, en noter les mêmes observations, puis voir comment ces axes servent à démontrer la
fréquence de la présence du père, et comment le modèle les accueille.

Sources lues : `legal/axe_agenda_danse_elise.md`, `legal/axe_garderie_coordination.md`,
`legal/implication_parentale_recurrence/` (00, 02, 05, 09), et en base `Axe` 2 (danse,
8 faits, 21 appuis) et `Axe` 1 (soccer 2013).

### 8.1 Ce qui constitue chaque axe

| Composante | Danse | Garderie |
|---|---|---|
| **Une structure** qui engendre la quantité | calendrier de l'école : deux sessions, environ 30 semaines, créneau hebdomadaire fixe (doc. photo 4) ; inscription de 1999 à 2016 (PDF 59, biographie) | la garderie elle-même : dépôt et retour chaque jour de fréquentation. **Aucun document ne l'établit** : elle vient de la nature de la structure et du témoignage |
| **Une règle d'inférence**, écrite | « une visite de Johanne conditionnée à l'absence d'Élise pour la danse, un jour X d'une session, attribue X au calendrier » | aucune règle formelle ; « la quantité vient de la nature quotidienne de la structure » |
| **Des conclusions intermédiaires** | une par session : « H-P 2011 : mardi et mercredi » (courriels 114 et 116, événements 46 et 52), « automne 2011 : au moins un soir, jour non déterminé »… | par mécanisme : coordination en temps réel (courriel 54), dépôt planifié (369), trajets matinaux (événements 213 et 214), retour de Nicolas (29), relais de Johanne (371) |
| **Des points de contrôle** répartis dans le temps | 2010 à 2014 : événements 46, 52, 274, 278 ; courriel 347 | 2011 à 2015, « distribution chronologique de la preuve » |
| **Une attribution** | l'échange du 16 septembre 2016 (courriels 7, 304, 305, 306) ; aveu de l'« aide familiale pour mes soirs de danse » | le même courriel 7 ; **le témoignage de LP** pour le mode général |
| **Une calibration** à chaque étage | « directement déterminé », « fortement soutenu », « plus probable que non », « jour non déterminé » | « directement établi », « établi avec authentification de LP », « non démontré et non nécessaire » |
| **Des réserves** expresses | le calendrier ne date pas les années de cohabitation ; pas « chaque soir sans exception » | pas « chaque matin et chaque après-midi » |
| **Une dépendance à un autre axe** | — | « Point d'appui : l'organisation déjà démontrée par les cours de danse » (courriel 347) |
| **Les allégations visées** | doc 1, énoncés 8, 9, 10, 11, 19, 20, 21 | doc 1, énoncés 9, 19, 20 |
| **Des faits atomiques** (art. 99) | 28 paragraphes d'un fait et d'une pièce chacun | — |

La **fréquence de la présence** (`05_synthese_evenements_cycliques.md`) assemble les axes
(danse, garderie, activités, soccer 2013) en trois couches : la quantité (les structures),
l'attribution (2016 et le témoignage) et la corroboration (les points de contrôle). La synthèse
multidimensionnelle (`09`) assemble à son tour sept thèmes, dont cette synthèse.

**La hiérarchie réelle compte donc cinq étages** : élément → conclusion intermédiaire → axe →
synthèse des événements cycliques → synthèse multidimensionnelle. Le même élément sert
plusieurs axes (courriels 7 et 347), et un axe sert plusieurs synthèses.

### 8.2 Ce que ces observations imposent au modèle

**1. Les nœuds internes d'une preuve sont des affirmations, pas des dossiers.** « H-P 2011 :
mardi et mercredi » n'est pas un regroupement : c'est une proposition, établie à un certain
degré, par une règle, à partir de ses feuilles. Un nœud interne porte donc :
- un **énoncé** ;
- une **nature** : proposition, structurel, inférence, conséquence, réserve. Ce sont les
  valeurs de l'ancien `NatureFait`, redéfinies dans le pont ;
- un **degré** : établi, fortement soutenu, plus probable que non, non déterminé, à
  authentifier ;
- au besoin, la **règle** qui le tire de ses enfants.

L'« objet » de la preuve (§5, question 2) n'est que l'énoncé de sa racine.

**2. Une preuve doit pouvoir s'appuyer sur une autre.** La garderie s'appuie sur la conclusion
de la danse. La synthèse des événements cycliques assemble des axes, et la synthèse
multidimensionnelle l'assemble à son tour. **La recommandation « pas de preuve dans une
preuve » (§5, question 5) est démentie par les données et retirée.** Un nœud peut **renvoyer**
à un autre nœud, de la même preuve ou d'une autre, sans le copier. Il faut interdire les
cycles.

Le gel reste praticable par **copie du chemin**. Modifier, pour un brouillon, une sous-preuve
gelée en fait une copie. Ses ancêtres gelés sont copiés à leur tour, jusqu'au premier ancêtre
non gelé, qui est simplement repointé. Les versions gelées gardent l'original intact.

**3. Une démonstration tient des poignées, à n'importe quel niveau d'un arbre.** Le
paragraphe atomique « Le 9 février 2011, le demandeur s'est occupé de la routine du soir
d'Alexia » (fait 10 de la danse) s'appuie sur **une feuille** de l'arbre de la danse. Le
paragraphe de clôture « Lus ensemble, ces éléments documentent un engagement récurrent »
s'appuie sur **la racine**. C'est la poignée que LP décrivait : un nœud parent qui manipule
l'ensemble. La démonstration devient une liste ordonnée de poignées vers des nœuds, et non
plus une liste de preuves entières (§5, question 5).

**4. Le témoignage est un appui sans document.** Le mode général de la garderie « s'établit
par le témoignage ». Le modèle doit accepter un nœud d'affirmation dont l'appui est déclaré
« témoignage », sans feuille ni cote. Ce nœud n'entre pas au bordereau. Il reste visible
comme tel, pour qu'on ne le prenne pas pour une affirmation documentée.

**5. Les allégations visées appartiennent à la démonstration.** Les deux axes répondent à des
énoncés précis du doc 1. Dans la chaîne paragraphe → démonstration → preuve, rien ne les
porte encore. La démonstration doit porter ses **cibles** : des énoncés d'actes adverses, sur
la rive de la preuve.

**6. Le rôle se lit par rapport au nœud parent, pas dans l'absolu.** Le courriel 347 est une
attestation sous « la mère dansait le mardi en 2012 », mais un point d'appui sous la
garderie. Le rôle se place donc sur le nœud-feuille, relativement à son parent, et non sur
l'élément.

**7. La distribution dans le temps se calcule.** « Des points de contrôle répartis de 2011 à
2015 » est une propriété des dates des feuilles d'un sous-arbre. Une vue la produit ; aucune
structure n'est à ajouter.

### 8.3 Esquisse qui en résulte

```
Démonstration « présence récurrente du père »    cibles : doc 1, énoncés 9, 19, 20…
 ├─ poignée → [danse] racine
 ├─ poignée → [garderie] racine
 └─ poignée → [attribution 2016] racine

Preuve [danse]
 └─ AFFIRMATION « Pendant la cohabitation, Élise dansait au moins un soir par semaine,
    environ 30 semaines par an » — inférence, établi
     ├─ AFFIRMATION « L'école fonctionne par sessions à créneau fixe » — structurel
     │    ├─ élément : doc. photo 4 (calendrier)              rôle : cadre
     │    └─ élément : PDF 59, phrase « … jusqu'en 2016 »      rôle : attestation
     ├─ AFFIRMATION « H-P 2011 : mardi et mercredi » — directement déterminé
     │    ├─ élément : courriel 114, phrase « Ce soir elle danse de 7 à 10 »
     │    ├─ élément : courriel 116 …
     │    └─ élément : événement 46, événement 52
     ├─ AFFIRMATION « Automne 2011 : au moins un soir, jour non déterminé » — plus probable que non
     │    └─ renvoi → l'affirmation structurelle ci-dessus
     └─ RÉSERVE « Le calendrier ne date pas les années de cohabitation »

Preuve [garderie]
 └─ AFFIRMATION « Les parents se coordonnaient pour les dépôts et retours » — établi
     ├─ renvoi → [danse] « organisation déjà démontrée » (courriel 347)
     ├─ AFFIRMATION « mode général matin/soir » — appui : TÉMOIGNAGE
     ├─ élément : courriel 54, phrase « vas tu la chercher ou j'y vais? »   rôle : attestation
     └─ élément : événements 213, 214                                     degré : à authentifier

Paragraphe « Le 9 février 2011… »  → démonstration → poignée → la feuille « événement 46 »
```

### 8.4 Ce que cela tranche dans le §5

| Question du §5 | Avant l'épreuve | Après |
|---|---|---|
| 2. Où vivent l'objet, le rôle, la portée, l'état | objet sur la preuve ; rôle sur l'élément | **pas de table supplémentaire**. Énoncé, nature, degré et règle sur **chaque nœud d'affirmation**. Rôle sur le **nœud-feuille**, relativement à son parent. Ordre et cibles sur la **démonstration**. Portée, état et version sur le **lien paragraphe → démonstration** |
| 3. Réutiliser, puis modifier | proposition | **retenu par LP** (2026-10-15) ; étendu par la copie du chemin (§8.2, point 2) |
| 4. Le triage | une preuve non rattachée est l'état de triage | **confirmé par les données** : les fichiers `axe_*` sont exactement cela, des preuves construites avant de savoir quel paragraphe elles serviront |
| 5. Les cardinalités | liste de preuves entières ; pas d'imbrication | **démonstration = liste ordonnée de poignées vers des nœuds, à tout niveau ; renvois entre preuves permis, sans cycle** |

---

## 9. Application : le troisième mouvement de la démonstration 1

### 9.1 Le contexte (LP, 2026-10-15)

Les fichiers `axe_*` démontrent la présence récurrente du père. Ils sont **une dimension du
contre-argument à la thèse principale de la requête du 19 novembre 2015** (P-19, doc 1). C'est
la démonstration 1 du plan de l'exposé des faits (`legal/redaction_v2/32_plan_expose_des_faits.md`
§5.1) :
- les ¶1-3 reproduisent les neuf paragraphes jurés, puis nomment le **socle** sur lequel ils
  reposent : l'implication minimale, la difficulté à assumer le rôle de père et
  l'indisponibilité (`Statement` 9, 11 et 19) ;
- la contradiction se fait **en mouvement** : (1) le désaveu implicite par l'acte, avec le
  courriel du 11 juin 2013 ; (2) les offres d'accès d'août 2015 ; (3) le **raisonnement sur
  l'implication, le rôle et la disponibilité parentale**. C'est dans ce troisième mouvement que
  les axes sont mobilisés.

Le texte que LP a collé est sa version du 29 septembre (¶41-56). L'atelier l'a revue
(`24_demonstration_sincerite_et_presentation.md` §4). La version en vigueur est la partie IV
de `25_presentation_argument_complet.md` (¶41-49), qui remplace les ¶41-56 et cite déjà des
pièces « notamment ». Son fondement : le **témoignage sur l'habitude** (art. 2843-2844 C.c.Q.)
et les **présomptions de fait** graves, précises et concordantes (art. 2846 et 2849), les pièces
servant de points de contrôle.

### 9.2 La chaîne

```
Démonstration 1 « contradiction de la thèse principale de P-19 »
  cibles : Statement 9 (§6), 11 (§7), 19 (§15) — le socle ; 20 (§16), 21 (§17)
  ├─ poignée → AFFIRMATION « Les neuf paragraphes reposent sur un même socle »
  │              éléments : Statement 7, 8, 9, 10, 11, 18, 19, 20, 21, 22 (unité : le paragraphe)
  ├─ poignée → [mouvement 1] le courriel du 11 juin 2013 (bloc 20)
  ├─ poignée → [mouvement 2] les offres d'accès d'août 2015 (bloc 21)
  └─ poignée → [mouvement 3] AFFIRMATION « La vie commune exclut la caractérisation jurée »
                 nature : inférence — règle : présomptions de fait (art. 2846, 2849)
       ├─ ¶41 AFFIRMATION résidence au domicile, 64 mois sauf environ 4 mois en 2011 — appui : TÉMOIGNAGE
       ├─ ¶42-43 AFFIRMATION structures récurrentes — structurel
       │    ├─ renvoi → [danse] « l'école fonctionne par sessions à soir fixe »
       │    ├─ renvoi → [activités] structure (séquence de clavardage 12, non cotée)
       │    └─ garderie : aucun document — appui : TÉMOIGNAGE et nature de la structure
       ├─ ¶44 AFFIRMATION répartition habituelle — appui : TÉMOIGNAGE (art. 2843-2844)
       │    ├─ a) garderie  → renvoi [garderie] racine
       │    ├─ b) danse     → renvoi [danse] racine
       │    ├─ c) activités → renvoi [activités], [soccer 2013]
       │    └─ d) maladie   → renvoi [journées de maladie] (16 adaptations, liasse S-4)
       ├─ ¶45-47 AFFIRMATION confirmation de 2016
       │    ├─ courriel 7  — rôle : cadre (ce qui lui est opposé ; pas une preuve de son contenu)
       │    ├─ courriel 306, la phrase « je n'ai pas dit… 50% du temps » — rôle : attestation du seuil
       │    └─ courriel du 11 janvier 2016 (P-20) — rôle : vérification (même seuil, avant l'audition)
       ├─ RÉSERVE « ni l'égalité, ni chaque occasion : l'exclusion de la version jurée suffit » (24 §1 d)
       └─ ¶48 points de contrôle → poignées vers les feuilles des axes, rendues « notamment »

¶49 (conclusion) → la racine du mouvement 3
```

### 9.3 Ce que l'application confirme

- **Le témoignage comme appui sans document** (§8.2, point 4) : ¶41 et ¶44 reposent sur lui,
  exactement comme le fondement juridique retenu par l'atelier.
- **Les présomptions de fait sont des nœuds d'inférence** : une structure connue, des
  occurrences réparties et une règle (art. 2846 et 2849) donnent le fait inconnu.
- **Le rôle dépend du contexte** : le courriel 7 est, dans la confirmation, un **cadre**. C'est
  la déclaration du demandeur lui-même. Il n'atteste pas son contenu, et le silence de la
  défenderesse ne vaut pas aveu (art. 2851). Le courriel 306, lui, atteste un énoncé positif
  (« pas 50 % »).
- **Une démonstration sert un bloc de paragraphes**, et chaque paragraphe tient une poignée
  à son niveau.

### 9.4 Ce que l'application ajoute

**« Notamment » : la poignée doit pouvoir sélectionner ce qu'elle montre.** Le ¶48 renvoie aux
axes par une **sélection** de pièces représentatives, alors que les axes en contiennent des
dizaines. Le bordereau, construit par l'usage, reçoit toutes les feuilles des sous-arbres
désignés. Le paragraphe n'en affiche que quelques-unes. Le lien paragraphe → démonstration
doit donc pouvoir porter un **mode d'affichage** : exhaustif, ou « notamment » avec la liste
des feuilles montrées. La question rejoint le document intermédiaire (reporté) et les liasses
de volume S-1 à S-5.

**Les calibrations existent déjà : le modèle doit les porter, pas les redécouvrir.** *Corrigé
le 2026-10-15.* La version précédente de ce paragraphe signalait trois « écarts » au ¶42 et au
¶44 b) : « seul », « plus de trente semaines », « d'une à trois fois ». Elle s'appuyait sur
l'ancien inventaire `legal/axe_agenda_danse_elise.md`. **Les trois sont déjà rapprochés** dans le
document de référence du thème, `legal/implication_parentale_recurrence/01_cours_danse_mere.md` :
- « seul » : « normalement seul… sous réserve d'exceptions » ; les visites de Johanne sont des
  exceptions à la prise en charge **en solitaire**, non à la responsabilité (§§ 129, 135-139) ;
- la durée : « environ trente semaines » (portée retenue de P-90) ;
- « une à trois » : « cohérente avec cette structure, sans être transformée en décompte exact »
  (conclusion du thème).

Ce sont exactement des **degrés** et des **réserves** de nœuds (§8.2, point 1). Le document de
référence les formule déjà sous ces deux formes : « Portée retenue / non recherchée »,
« Précisions et limites admises ». L'import d'un thème dans le pont doit donc partir du
document de référence du thème, jamais de l'ancien inventaire `axe_*`.

---

## 10. La thèse de la danse — collecte

Demandée par LP le 2026-10-15. Elle sert de matière à l'arbre [danse] du nouveau pont. Ce qui
suit **renvoie** aux sources et ne les recopie pas : le verbatim vit dans les fiches `piece_*`.

### 10.1 Les sources, et laquelle fait foi

| Source | Ce que c'est | Statut |
|---|---|---|
| `legal/implication_parentale_recurrence/01_cours_danse_mere.md` | **le document de référence du thème** : proposition, méthode de détermination du jour, tableau par session, fonction des visites de Johanne, session de l'hiver 2010 et § 6, corroboration de 2016, conclusion, limites admises, état de la preuve | **fait foi** ; « démonstration factuelle principale close » |
| `legal/engagements_danse_elise.md` (27 juil.) | inventaire des engagements d'Élise de 1999 à 2018, **sans** la présence de LP | antérieur à la référence |
| `legal/axe_agenda_danse_elise.md` | ancien inventaire : 25 pièces, règle d'inférence, faits sur le modèle art. 99, estimation par couches | antérieur ; ses calibrations sont dépassées par la référence |
| `legal/annexes/annexe_B_danse_routine_soir.md` (12 juil.) | annexe de preuve agrégée | antérieure |
| Base : `Axe` 2 (8 faits, 21 appuis) | les faits voulus, comparés au plaidé : `raison` = PLAIDE_PARTIELLEMENT ou ENFOUI | outil de l'ancien pont |
| **Acte déposé** (doc 9) | §§ 27-31 (`Statement` 542-546), § 83 (offre du 2 sept. 2015), §§ 128 et 131 (2016) | gelé |
| **Atelier** `legal/redaction_v2/` | 10 (¶ 22-B à 22-E ; ¶ 95-C à 95-F), 11 (rang 1 ; § 15 contre § 17), 12 (¶ 104 à 104-D), 14 (A0.3, A4.3, A4.8, A4.10, B3.1, C3.4), 17 (tapisserie ; génératrice composite), 03 (variable supprimée), 24 et 25 (¶ 42, ¶ 44 b), revues 26 à 28, 30 (3 sept. 2015) | en cours |
| Mémoire | « prédicat à variable supprimée » (§ 17) ; « test de sincérité » | règles |

### 10.2 La proposition et sa calibration (référence, 01)

- **Proposition.** Pendant la cohabitation, les cours de danse de la mère étaient un engagement
  cyclique qui l'amenait à s'absenter. Pendant ces absences, le père assumait normalement la
  responsabilité et les soins des enfants. La présence occasionnelle de la grand-mère était une
  aide ou une visite.
- **Fréquence.** Au minimum hebdomadaire pendant les sessions. Plusieurs soirs là où deux
  créneaux sont identifiés (mardi et mercredi à l'automne 2010 et à l'hiver-printemps 2011).
  « Une à trois fois » : cohérent avec la structure, sans décompte exact.
- **Structure.** Deux sessions, **environ trente semaines**, créneau fixe à l'intérieur de la
  session (P-90). Le calendrier de 2025-2026 illustre la nature cyclique ; il ne date pas les
  années historiques.
- **« Seul ».** Normalement seul, sous réserve d'exceptions. Les visites de Johanne sont des
  exceptions à la prise en charge **en solitaire**, non à la responsabilité du père.
- **Méthode.** Sept étapes, de l'en-tête local du courriel au classement par session. Jamais de
  transport automatique d'un jour d'une session à la suivante. Trois degrés : directement
  établi, fortement soutenu, non déterminé.
- **Limites admises.** Pas de présence sans exception de la mère ; aucun nombre exact de cours ;
  l'aide de la grand-mère est compatible avec la responsabilité du père ; la danse n'est pas
  critiquée ; le calendrier récent ne date rien ; un jour historique n'est affirmé que
  lorsqu'une pièce l'identifie.

### 10.3 Les pièces

| Cote de juillet | PK | Ce qu'elle porte (référence, 01) |
|---|---|---|
| P-83 | pdf-59 | biographie : continuité de 1999 à 2016 (C1) |
| P-90 | photodoc-4 | calendrier 2025-2026 : sessions, créneau fixe |
| P-48.1 à P-48.3 | emails 81, 80, 100 | décembre 2010 : visite conditionnée à l'absence, mardis et mercredis |
| P-49.1 à P-49.3 | events 46, 52, 78 | février 2011, deux routines du soir ; juin 2011, trois chorégraphies |
| P-72 (liasse) | emails 67, 114, 66, 116, 115 | mars 2011 : « Ce soir elle danse de 7 à 10 », bain, visite reportée |
| P-50.1, P-50.2 | emails 347, 474 | mardi 6 mars 2012 ; mercredi 8 mai 2013 (fortement soutenu) |
| P-51.1, P-51.2 | events 274, 278 | lundis 27 janvier et 3 mars 2014, avec les deux enfants |
| P-17 | pdf-6 | 2 sept. 2015 : horaire de garde « en considération de ses cours de danse » |
| P-22 (fil 6) | emails 7, 304, 305, 306 | 16 sept. 2016 : « mes soirs de danse », « une à trois fois », « pas 50 % » |
| — (sans cote de juillet) | event 19 | 13 juin 2010 : spectacle d'Élise, première année d'Alexia |
| — (P-__) | photodoc-15 | adresse de l'école |

### 10.4 Ce que la thèse sert : une preuve, de nombreuses poignées

| Cible | Usage | Où |
|---|---|---|
| § 15, « rarement disponible » | **la danse mène** : la structure seule détermine l'attribution | 11 (rang 1) ; 12 ¶ 104-D |
| § 17, « aidait lorsque la demanderesse n'était pas disponible » | fournit la **variable supprimée** : son indisponibilité, plus de trente semaines par an. Mais l'axe se relit comme une confirmation du § 17 : **contre le § 17, la garderie mène** | 03 ; 12 ¶ 104 à 104-D ; 11 ; 28 |
| § 6, « minimalement… depuis la naissance d'Alexia » | **la session de l'hiver 2010**, première année d'Alexia : une conduite volontaire difficilement conciliable avec la croyance énoncée (test de sincérité, calibré : pas l'insincérité de 2015) | 01, §§ 141-173 |
| § 7, « difficulté à assumer son rôle de père » | Élise lui confiait la routine du soir d'une enfant en bas âge, puis de deux | 01, conclusion ; 27 (plancher d'un soir hebdomadaire) |
| §§ 6 et 16, « c'est la demanderesse qui s'occupait des enfants » | **qui gardait les enfants les soirs de danse ?** La requête n'identifie personne : c'est un constat d'absence d'allégation, non un mensonge | 10 ¶ 95-D à 95-F ; 26 |
| Démonstration 1, mouvement 3 | la structure et la répartition | 25 ¶ 42, ¶ 44 b ; doc 9 §§ 27-31 |
| La confirmation de 2016 | elle nomme elle-même « mes soirs de danse », et l'aide familiale est postérieure à la séparation | 03 ; doc 9 §§ 128, 131 |
| Août-septembre 2015 | une garde partagée aménagée autour de ses cours, refusée comme « prématurée » | doc 9 § 83 ; 30 |
| Génératrice composite | danse, rupture avec la famille paternelle et désir de la grand-mère : d'où les visites des soirs de danse | 17 ; 01, §§ 93-139 |

**C'est le cas réel de réutilisation que le modèle doit porter** : un seul arbre, au moins neuf
poignées, posées à des niveaux différents. Les §§ 15 et 7 visent la racine. Le § 17 vise le
nœud de structure. Le § 6 vise le nœud « hiver 2010 ». La question des soirs de danse vise la
proposition de responsabilité. La confirmation de 2016 vise son propre nœud.

### 10.5 Positions dépassées à ne pas importer

Les anciens inventaires portent des positions que la référence a remplacées. L'import dans le
pont part donc de la référence (01) seule :
- `engagements_danse_elise.md` § 5 : « aveu par acquiescement sur la fréquence (silence dans
  l'email-306) ». La référence dit « sans contester séparément ». L'atelier rappelle que le
  silence ne vaut pas aveu (art. 2851, au 24).
- `engagements_danse_elise.md` § 5 : « entre 1 et 3 cours par semaine selon les témoignages
  directs (email-7) ». La référence en fait une affirmation rétrospective cohérente, sans
  décompte.
- `axe_agenda_danse_elise.md` : l'estimation par couches (« 400 à 600 occasions »). La référence
  écrit : « aucun nombre exact de cours suivis n'est avancé ».
- Base, `Axe` 2 : l'email-7 y est un appui de rôle ATTESTATION. Dans la référence, c'est
  l'affirmation rétrospective de LP, qui corrobore sans attester.

### 10.6 Déterminer les jours de danse (questions de LP, 2026-10-15)

**Les bases** (méthode de la référence, 01), de la plus forte à la plus faible :
1. **Une communication contemporaine** qui nomme le jour ou dit « ce soir », datée par l'en-tête
   local et non par l'UTC de la base : emails 100, 114, 116, 347. Le jour est **directement
   établi**.
2. **Une visite de Johanne expressément reliée à la danse**, un jour X : emails 81 et 80, et
   l'email 474 dans le fil « Re: Demain ». Le jour est **fortement soutenu** (fondement
   ci-dessous).
3. **Un événement photographié**, dont l'explication rattache la soirée à la danse : events 46,
   52, 274 et 278. L'horodatage des photos fixe la date ; le lien avec la danse vient de
   l'explication enregistrée par LP, que son témoignage doit authentifier. Les récitals d'Alexia
   (events 220, 224, 302) ne disent rien du jour de la mère.
4. **La structure** (P-90 : aucun cours à l'unité, créneau fixe dans la session) étend un jour
   établi à toute la session. C'est une présomption de fait (art. 2846 et 2849). Jamais d'une
   session à l'autre (règle 7).
5. **La continuité** (P-83, de 1999 à 2016 ; confirmée par P-17 en 2015 et par l'email 305 en
   2016) donne **au moins un soir par session, jour non déterminé**.
6. **Le témoignage** sur l'habitude : celui de LP (art. 2843-2844), éventuellement celui de
   Johanne.

**Pourquoi les visites de Johanne renseignent le calendrier.** Ce n'est pas une coïncidence,
c'est une **contrainte** :
- **la prémisse** : après novembre 2010, Élise a rompu avec la mère de LP (email 82, du
  1er décembre 2010 : « je veux juste m'assurer que je vais garder mon lien avec Alexia »).
  Johanne ne pouvait voir Alexia au domicile qu'**en l'absence d'Élise**. Une visite est donc un
  **marqueur d'absence** ;
- **la contrainte, dans les mots de Johanne** : email 81 (« lorsque Élise sera à la danse »,
  « si Élise n'est pas là demain soir ») ; email 67 (la voiture d'Élise était là, « donc j'ai
  pensé que je ne devais pas arrêter ») ;
- **LP relaie l'information sur les absences** : email 100 (« je t'ai deja dit que les mardi et
  mercredi Élise dansait ») ;
- **la chaîne** : une visite expressément reliée à la danse un jour X, donc Élise dansait ce
  jour-là ; avec le créneau fixe de la session, X revient chaque semaine de la session.

**Pourquoi le lien exprès avec la danse est indispensable.** Une visite prouve une absence, pas
sa cause. Élise s'absentait aussi pour son travail, pour l'enseignement de la danse orientale à
compter de 2010, pour les cours d'Urban Element (sans horaire fixe) et, à compter de 2013, pour
les événements d'Aziza. D'où la règle de la référence : « une visite familiale sans ce lien
explicite ne suffit pas ». L'email 115, qui ne fait que reporter une visite au lendemain, ne
fixe pas à lui seul le mercredi.

**Statut de la prémisse.** Le début de la rupture est établi par l'email 82, contemporain et
écrit par Johanne. Sa **permanence** (« jamais de réconciliation pendant la période ») figure à
compléter dans l'état de la preuve de la référence : elle repose sur le témoignage et sur les
emails 82 et suivants. Deux remarques :
- pour les visites **expressément** reliées à la danse, le texte de la visite suffit à fixer le
  jour, sans la prémisse ;
- la question de Johanne le 7 mai 2013, « Est ce que Élise va danser? » (email 474), suppose que
  la contrainte joue encore en 2013. Elle corrobore donc la permanence de la rupture.

**Vérifié dans la base le 2026-10-15** : aucune source non exploitée ne fixe le jour d'une
session indéterminée.
- Courriels de 2009 à 2015 mentionnant la danse : tous déjà exploités. Le seul autre résultat,
  l'**email 48**, est **le même message que l'email 347** (6 mars 2012, à la même seconde),
  importé deux fois (fils 38 et 78). C'est un doublon de **document** sur la rive : le bordereau
  versionné étant indexé par modèle + PK, il donnerait deux cotes au même message.
- Clavardage : la base ne le couvre que de septembre 2014 à février 2015. Le message 127 du
  23 octobre 2014 (« je paie le mien ») confirme l'inscription d'Élise à l'automne 2014, sans le
  jour. Il figure déjà dans `axe_activites_enfants.md`, mais la référence de la danse ne le
  mobilise pas pour cette session.
- Hors base, ce qui pourrait fixer les sessions indéterminées : les registres d'inscription de
  l'école de 2009 à 2015, déjà envisagés dans l'ancien inventaire.

---

## 11. L'arbre du fait : les soins du soir pendant les cours de danse

### 11.1 Le fait (LP, 2026-10-15, mot pour mot)

> le pere assurait les soins des enfants le soir quand Élise s'absentait pour suivre ses cours
> de dance. Au minimum une fois par semaine, j'usqu a 3 fois par semaine, environs 30 semaine
> par année.

C'est le **fait 7 de l'`Axe` 2** en base, marqué **ENFOUI** : la demande de juillet ne l'a
jamais posé comme énoncé autonome, il n'y figure que dans la phrase de clôture du § 31. La
version 2 le pose. Tout ce qui précède (§10) sert ce fait.

### 11.2 L'arbre

Légende : *rôle* de l'élément par rapport à son nœud parent ; [degré] de chaque affirmation.
Unité : la phrase pour un courriel ou un PDF, l'événement entier pour une photographie, le
document entier pour le calendrier (une structure).

```
FAIT — « Pendant la cohabitation, le père assurait les soins des enfants le soir lorsque la mère
        s'absentait pour ses cours de danse : au minimum une fois par semaine, jusqu'à trois fois,
        environ trente semaines par année. »                    [établi — présomption + témoignage]
│
├─ A. « La mère s'absentait le soir, de façon récurrente, pour ses cours de danse »     [établi]
│   ├─ A1. Continuité de l'engagement, de 1999 à 2016                                     [établi]
│   │    ├─ P-83 (pdf-59), C1 « Elle continue ensuite ses cours … jusqu'en 2016 »    attestation
│   │    ├─ P-17 (pdf-6), 2 sept. 2015 : horaire de garde « en considération de ses cours de danse »
│   │    │                                                                           vérification
│   │    ├─ email 305 (C11), 16 sept. 2016 : « mes soirs de danse » — au présent, au pluriel :
│   │    │    une catégorie permanente de sa semaine, qu'elle nomme elle-même       vérification
│   │    └─ chat 127, 23 oct. 2014 : « je paie le mien » — inscription à l'automne 2014
│   │                                                                                vérification
│   ├─ A2. Structure : sessions, créneau hebdomadaire fixe, environ trente semaines   [structurel]
│   │    ├─ P-90 (photodoc-4), calendrier                                            cadre
│   │    └─ RÉSERVE : le calendrier de 2025-2026 ne date pas les années historiques
│   ├─ A3. Jours déterminés, session par session                           [degré par session]
│   │    ├─ hiver 2010 : au moins une chorégraphie, jour non déterminé ← event 19 (13 juin 2010)
│   │    ├─ automne 2010 : mardi et mercredi [direct] ← emails 81, 80, 100 (P-48.1 à 48.3)
│   │    ├─ hiver-printemps 2011 : mardi 19 h-22 h et mercredi [direct]
│   │    │     ← emails 114, 116 (P-72) ; events 46, 52 (P-49.1, 49.2) ; event 78 (P-49.3)
│   │    ├─ hiver-printemps 2012 : mardi [direct] ← email 347 (P-50.1) — doublon : email 48
│   │    ├─ hiver-printemps 2013 : mercredi [fortement soutenu] ← email 474 (P-50.2), fil « Demain »
│   │    ├─ hiver-printemps 2014 : lundi [direct] ← events 274, 278 (P-51.1, 51.2)
│   │    └─ autres sessions : au moins un soir, jour non déterminé ← renvoi A1 + A2
│   └─ A4. Règle des visites : une visite expressément reliée à la danse marque un soir de danse
│        ├─ prémisse : rupture d'Élise avec la famille paternelle ← email 82 (1er déc. 2010)
│        │    └─ permanence [à compléter] ← TÉMOIGNAGE ; email 474 (2013) corrobore
│        ├─ visite conditionnée à l'absence ← email 81 ; email 67 (« la voiture d'Élise était là »)
│        └─ RÉSERVE : une visite prouve une absence, pas sa cause — lien exprès avec la danse requis
│
├─ B. « Pendant ces absences, le père assurait les soins du soir »         [établi — normalement]
│   ├─ B1. Routines documentées
│   │    ├─ Alexia seule : events 46, 52 (février 2011 : repas, bain, pyjama)        attestation
│   │    └─ Alexia et Nicolas : events 274, 278 (lundis de 2014)                     attestation
│   ├─ B2. Adaptation de son horaire ← email 347 « je dois etre a la maison de bonne heure ce soir
│   │       parceque tu danses »                                                     attestation
│   ├─ B3. Il coordonnait la présence de la famille paternelle pendant qu'il avait la charge
│   │       ← emails 81, 80, 100, 66, 116, 115, 474                                  attestation
│   │    └─ RÉSERVE : les visites de Johanne sont des exceptions à la garde en solitaire, non à la
│   │       responsabilité
│   ├─ B4. Le mode normal ← TÉMOIGNAGE (art. 2843-2844) ; les photographies sont à authentifier
│   ├─ B5. Deux configurations : Alexia seule jusqu'en février 2013, puis les deux enfants
│   └─ B6. La fonction devait être remplie, et le dossier ne nomme aucun autre candidat que le père
│        │                                     [inférence par élimination — 03 §3 ; doc 9 § 131]
│        ├─ email 305 (C11) : « j'ai une aide familiale pour leur cours de natation et pour mes
│        │    soirs de danse » — après la séparation, la fonction exige un arrangement
│        │    permanent ; « on n'embauche pas le remplaçant de quelqu'un qui ne faisait rien »
│        │                                                                           attestation
│        ├─ email 305 (C11) : « une de mes soeurs les prend quand toi tu ne le fais pas » — elle
│        │    place ses sœurs à l'accès du dimanche, non aux soirs de danse ; cela écarte
│        │    l'hypothèse « chez tes sœurs » de l'email 7                             vérification
│        ├─ email 304 : « j'ai des aides ou des gardiennes » — un réseau postérieur à la séparation
│        │                                                                           cadre
│        ├─ P-19 § 17 (Statement 21) : « Le défendeur aidait lorsque la demanderesse n'était pas
│        │    disponible » — l'acte adverse nomme lui-même le père                   attestation
│        ├─ CONSTAT : la requête n'identifie personne d'autre pour ces soirs (10 ¶ 95-D, 95-E) —
│        │    une absence d'allégation, jamais une preuve par l'absence
│        └─ RÉSERVE : ces messages décrivent 2016, non la cohabitation ; l'aide n'est identifiée
│             ni dans son identité, ni dans son statut, ni dans sa rémunération. Ce qu'ils
│             établissent est étroit et suffit : la fonction existe, elle est permanente, et
│             quelqu'un doit la remplir
│
├─ C. « Fréquence : au minimum une fois, jusqu'à trois fois par semaine, environ trente semaines »
│   ├─ C1. Plancher d'un soir par semaine pendant les sessions [établi — présomption]
│   │       ← renvoi A1 + A2 + A3 ; email 305 : une catégorie permanente, qu'elle ne pourra pas
│   │         présenter ensuite comme occasionnelle
│   ├─ C2. Deux soirs documentés : automne 2010, hiver-printemps 2011 [direct] ← renvoi A3
│   ├─ C3. Jusqu'à trois soirs [cohérent avec la structure, sans décompte]
│   │    ├─ TÉMOIGNAGE
│   │    ├─ email 7, 16 sept. 2016 : « … de une a trois fois semaine »   cadre (sa propre affirmation)
│   │    └─ email 306 : elle ne conteste pas séparément la fréquence — non un aveu (art. 2851)
│   └─ C4. Environ trente semaines par année ← renvoi A2
│
├─ D. Confronté en 2016, la défenderesse ne conteste pas la participation
│   ├─ email 7 : l'énumération des catégories, dont les soirs de danse            cadre
│   └─ email 306 : « … tu ne t'en occupais pas 50% du temps »   attestation (d'un seuil, non d'une absence)
│
└─ RÉSERVES (limites admises, référence 01)
     pas sans exception ; aucun nombre exact de cours ; l'aide de la grand-mère est compatible
     avec la responsabilité ; la danse n'est pas critiquée ; un jour n'est affirmé que si une
     pièce l'identifie
```

### 11.3 Ce que l'arbre produit

- **Le bordereau**, par l'usage. Les pièces qui entrent : P-83, P-90, P-48, P-49, P-72, P-50,
  P-51, P-17 et P-22. S'y ajoutent l'event 19, l'email 82 et le chat 127, dont la cote reste à
  vérifier ou à attribuer. Le doublon email 48 / email 347 doit être réglé avant, sinon le même
  message recevrait deux cotes.
- **Les appuis sans document** : A4 (permanence de la rupture), B4 (le mode normal) et C3 (jusqu'à
  trois). Ils restent visibles comme tels et n'entrent pas au bordereau.
- **Un même élément, trois rôles.** L'email 305 apparaît en A1 (la catégorie existe), en B6 (la
  fonction se remplace) et en C1 (elle est permanente). C'est le cas prévu au §8.2, point 6 : le
  rôle se lit par rapport au nœud parent. *Ajouté le 2026-10-15 : la première version de l'arbre
  ne mobilisait l'admission de l'aide familiale qu'en A1, comme simple vérification.*
- **Les poignées des paragraphes.** Le paragraphe qui énonce le fait tient la racine. Un
  paragraphe sur la structure tient A2. Un paragraphe sur une session tient la feuille de cette
  session. Les autres démonstrations du §10.4 tiennent leurs propres nœuds du même arbre : A pour
  le § 17, la session de l'hiver 2010 pour le § 6, B pour le § 7.
- **La calibration est portée par les nœuds**, non par la prose : « normalement » sur B, « sans
  décompte » sur C3, « environ » sur C4, « à compléter » sur la permanence de la rupture. Un
  paragraphe qui affirmerait plus que son nœud se repère.

---

## 12. Le même exercice pour la garderie

Demandé par LP le 2026-10-16. Même méthode qu'aux §§ 10 et 11 : partir de la référence du thème,
mobiliser tout ce qui sert le fait, ne pas rouvrir ce qui est calibré.

### 12.1 Les sources, et laquelle fait foi

| Source | Ce que c'est | Statut |
|---|---|---|
| `legal/implication_parentale_recurrence/02_garderie.md` | **la référence développée** : proposition, point d'appui sur la danse, sept occurrences, distribution chronologique, mécanisme à trois niveaux, force de l'argument (directement établi / avec authentification / non démontré) | **fait foi** ; « substantiellement documenté, encore ouvert pour le témoignage sur le mode général » |
| `legal/implication_parentale_recurrence/02_routine_garderie.md` | version antérieure du même thème (deux fichiers portent le n° 02) : mode de fonctionnement, **analyse de l'échange de 2016** (email 7, C5 ; email 306, C3), précisions et limites admises | **complète la référence** sur 2016 et les limites, que la référence ne reprend pas ; son tableau « à compléter » est dépassé par la référence |
| `legal/axe_garderie_coordination.md` | ancien inventaire, qui renvoie lui-même à la référence | antérieur |
| **Acte déposé** (doc 9) | § 22 (énumération des responsabilités), § 25 (`Statement` 539, P-44 : le mode de répartition), § 26 (`Statement` 540, P-45.1, P-45.2, P-46, P-47 : les occurrences) | gelé |
| **Atelier** | 10 ¶ 22-B (deux trajets par jour ouvrable) et ¶ 95-C ; 11 §1-bis (contre le § 17, la garderie mène) ; 14 (la trame quotidienne contre le § 15) ; 17 (l'interdépendance des horaires) ; 25 ¶ 42, ¶ 44 a), ¶ 48 | en cours |
| Pièce de clavardage P-62 (`piece_chatsequence-3.md`) | 3 nov. 2014 – 13 févr. 2015 : coordination parentale et médicale | mobilisée au thème de la **maladie** (04), pas à la garderie |

### 12.2 Le fait

LP a formulé lui-même le fait de la danse. Pour la garderie, la formulation qui suit est **reprise
de la référence et du ¶ 50 de LP (29 sept.), à confirmer** :

> Pendant les périodes où les deux parents travaillaient à temps plein, le père effectuait des
> dépôts et des retours de garderie selon une répartition établie avec la mère en fonction de leurs
> horaires, et assurait les soins de l'enfant jusqu'au retour de l'autre parent.

### 12.3 L'arbre

```
FAIT (à confirmer) — dépôts et retours de garderie selon une répartition fondée sur les horaires ;
                     soins jusqu'au retour de l'autre parent
                                            [établi — témoignage + présomption + occurrences]
│
├─ A. La structure : la garderie fixe deux transitions par jour de fréquentation      [structurel]
│   ├─ la nature de l'institution : témoignage et connaissance d'office
│   ├─ email 7 (C5), 16 sept. 2016 : « tu allais chercher et porter les enfants a la garderie tout
│   │    les soirs et tout les matins » — sur un ton ironique, LP pose la structure (deux trajets,
│   │    chaque jour) devant Élise, qui ne la conteste pas                                  cadre
│   │    (corrigé le 2026-10-16 : la version précédente disait « aucun document ne l'établit »)
│   ├─ la période : le 7 mars 2011, Alexia n'a pas de place en garderie (email 68, « elle n a pas
│   │    de place en garderie ») ; le 24 novembre 2011, la coordination des retours a commencé
│   │    (email 54) ; les occurrences vont jusqu'en février 2015 ; Nicolas est en garderie en 2014.
│   │    La garderie commence donc entre mars et novembre 2011                              cadre
│   │    (corrigé le 2026-10-16 : l'email 120 de mai 2011 parle de l'entrée future à la
│   │    maternelle ; il ne date pas le début de la garderie)
│   └─ l'interdépendance (atelier 17) : l'heure de cueillette dépend de l'heure de fin de travail,
│        qui dépend du soir de cours de l'autre parent, fixé pour la session — elle force la
│        répartition                                                                     inférence
│        └─ renvoi → [danse] : email 347, le « pont » (il avance son horaire pour prendre Alexia)
│
├─ B. La répartition : un mode général matin/soir selon les horaires          [à établir — TÉMOIGNAGE]
│   ├─ TÉMOIGNAGE : l'objectif de réduire le temps de garde, le principe d'alternance, les plages
│   │    habituelles, les soins assurés par le parent revenu le premier
│   └─ RÉSERVE : pas d'alternance mathématique ; le parent du matin ou du soir pouvait changer
│
├─ C. Les applications contemporaines, réparties de 2011 à 2015              [points de contrôle]
│   ├─ C1 24 nov. 2011 — email 54 (P-44) : « vas tu la chercher ou j'y vais? » — lieu non nommé
│   │                                                                                 attestation
│   ├─ C2 18 et 19 oct. 2012 — events 213, 214 (P-45.1, 45.2) : deux matins à pied vers la
│   │    maternelle [à authentifier : LP photographe, destination] ; RÉSERVE : les photos de 9 h 32
│   │    de l'event 214 sont étrangères à la sortie                                     attestation
│   ├─ C3 7 mars 2013 — email 369 (P-46) : « apres etre aller porter Alexia » — destination non
│   │    nommée                                                                         attestation
│   ├─ C4 17 sept. 2014 — email 29 : « quand je suis aller le chercher à la garderie » (Nicolas)
│   │    — garderie nommée ;                                                            attestation
│   │    email 148, le même jour : « juste avant d'aller les chercher »                 vérification
│   │    (cotes d'amendement ; sans cote de juillet)
│   ├─ C5 3 déc. 2014 — P-62 (clavardage 463 à 476) : **une urgence médicale** de Nicolas (RV à
│   │    13 h 30) impose de le sortir de la garderie avant la sieste. Élise : « il faut aller
│   │    chercher nicolas » ; LP s'organise (sa mère le conduit) ; Élise : « j'ai averti que […] tu
│   │    t'en venais », « avant 12h30 car ils commencent le processus dodo »  [lieu non nommé]
│   │    illustration — LP est une personne que la mère et la garderie attendent pour aller
│   │    chercher l'enfant
│   │    RÉSERVE : un trajet d'exception, à midi, causé par la maladie ; ce n'est pas une
│   │    application de la répartition ordinaire matin/soir. L'élément appartient d'abord au
│   │    thème de la maladie (04 ; P-62, C3)
│   ├─ C6 16 févr. 2015 — email 371 (P-47) : Johanne, « Tu n'as pas besoin d'aller à la garderie » ;
│   │    réponse de LP, email 372 : « Ok non »                                          attestation
│   └─ C7 la mère aussi fait des retours — clavardage 409 (4 nov. 2014) ; clavardage 504
│        (16 déc. 2014 : Nicolas, malade, est sous antibiotiques et à la maison avec LP ; elle va
│        chercher Alexia) — c'est la répartition elle-même, non une contradiction ; le 16 décembre
│        relève aussi de la maladie                                                       illustration
│
├─ D. Les soins après le retour, jusqu'à l'arrivée de l'autre parent                [TÉMOIGNAGE]
│   ├─ clavardage 504 (16 déc. 2014) : « as tu prévu qqc pour souper? » — « oui » — un jour de
│   │    maladie, non un jour ordinaire                                                  illustration
│   └─ renvoi → [danse] B : la routine du soir
│
├─ E. 2016 : confronté, la défenderesse ne conteste pas les trajets
│   ├─ email 7 (C5) : le même passage qu'en A — ici, sa fonction est la négation du portrait
│   │    d'une mère qui faisait tous les trajets (02_routine)                           cadre
│   └─ email 306 (C3) : « pas 50 % » — elle ne répond pas spécifiquement aux trajets ; ce n'est
│        pas un aveu (art. 2851)                                       attestation (d'un seuil)
│
└─ RÉSERVES (référence, § 9, et 02_routine, limites admises)
     pas d'alternance parfaite ; pas d'heures exactes ; ni l'absence de toute exception ou de tout
     relais, ni 50 % ; le recours à Johanne est un relais, non la preuve d'une absence de
     responsabilité ; les communications corroborent des occurrences, elles ne sont pas un registre
```

### 12.4 Ce que la garderie sert

| Cible | Usage | Où |
|---|---|---|
| § 17, « aidait lorsque la demanderesse n'était pas disponible » | **la garderie mène** : à huit heures un mardi ordinaire, personne n'est « indisponible ». Elle atteint le § 17 sans passer par la variable | 11 §1-bis ; 03 |
| § 15, « rarement disponible » | la trame quotidienne, sur l'année entière, et l'interdépendance des horaires | 14 ; 17 |
| §§ 6 et 16 | elle n'assumait pas seule les deux trajets quotidiens | 10 ¶ 95-C |
| Démonstration 1, mouvement 3 | la structure (¶ 42), la répartition (¶ 44 a), les points de contrôle (¶ 48 : P-44, P-46, P-47) | 25 |
| Synthèse des événements cycliques | la quantité vient de la nature quotidienne de la structure | 05 |
| Ce que la danse n'apporte pas | une responsabilité **quotidienne**, indépendante de toute activité personnelle de la mère | 02, § 10 |

### 12.5 Ce que l'exercice a trouvé

Ce sont des pièces **présentes au corpus, mais non mobilisées par la référence de la garderie**.
Ce n'est pas de la preuve nouvelle :
- **le 3 décembre 2014** (P-62, C3). C'est d'abord une **urgence médicale** : le thème de la
  maladie l'utilise à ce titre. Le trajet de garderie en découle. LP va chercher Nicolas à midi,
  avant la sieste, pour le conduire au rendez-vous ; Élise en avertit la garderie. *Corrigé le
  2026-10-16* : la version précédente en faisait « l'équivalent de l'aide familiale » et la
  répartition dans les mots d'Élise. Elle surévaluait l'élément. C'est un trajet d'exception
  causé par la maladie. Il montre seulement que LP était une personne que la mère et la garderie
  attendaient pour aller chercher l'enfant. Il ne montre pas la répartition ordinaire ;
- **l'email 148** (17 sept. 2014), « avant d'aller les chercher ». Il corrobore l'email 29 le même
  jour, au pluriel. Il est utilisé ailleurs, au thème de la résidence de 2014 ;
- **les emails 68 et 120** (2011) : ils bornent le début de la structure. Ils sont utilisés au
  thème des absences du travail ;
- **l'email 372**, « Ok non » : la réponse de LP à Johanne. Il n'est utilisé nulle part. Sa
  portée est mince et ambiguë ; on peut le joindre à l'email 371 sans rien lui faire dire de
  plus ;
- **les clavardages 409 et 504** : la mère fait elle aussi des retours. C'est la répartition
  elle-même. Le dire est plus sûr que de laisser la partie adverse le présenter comme une
  contradiction.

**Pour le modèle**, la même leçon qu'avec la danse. Un élément appartient à la rive, et
plusieurs thèmes le tiennent par des poignées : le 3 décembre 2014 sert la maladie **et** la
garderie, avec deux rôles différents. Aujourd'hui, chaque thème garde sa propre liste dans son
fichier. Le pont rendra visible qu'un même élément sert plusieurs thèmes, ce que les fichiers
séparés cachent.

### 12.6 Les notes personnelles de LP (champ `note`) — lecture du 2026-10-16

**Où elles sont.** Les notes portent sur les **fils** (`EmailThread.note`), non sur les
courriels : 137 fils annotés sur 160, aucun courriel annoté.

**Les notes qui touchent la garderie :**

| Fil | Ce que dit la note | Courriels | Dans la preuve de la garderie ? |
|---|---|---|---|
| 42 | coordination « qui va chercher Alexia à la garderie » | 54 | **oui** (C1, P-44) |
| 91 | « la responsabilité récurrente d'aller porter et chercher les enfants à la garderie » | 369, 370 | **oui** (C3, P-46) |
| 23 | « le défendeur allait chercher Nicolas à la garderie » | 29, 146 à 149 | **oui** (C4) |
| 92 | « l'implication du père dans le transport des enfants à la garderie » | 371, 372 | **oui** (C6, P-47) |
| **38** | « les parties se coordonnaient pour aller porter et chercher Alexia à la garderie pour permettre à la demanderesse de s'absenter pour suivre ses cours de danse » | **48** | **non**, voir ci-dessous |
| **152, 153, 71, 72, 73, 74** | « Alexia n'avait pas de place en garderie » après le congé de maternité ; les grands-mères assuraient les soins pendant que les parents travaillaient (maternelle 4 jours, paternelle 1 jour) | 601 ; 602, 603 ; 86, 97 ; 87, 93 à 96 ; 88 ; 89 (septembre à novembre 2010) | **non**, voir ci-dessous |

**Le fil 38 : la note est attachée au doublon.** L'email 48 est le même message que l'email 347
(fil 78, P-50.1). La note est sur le fil 38. Le fil 78, celui de la pièce, n'en a aucune : ton
observation n'était donc pas visible depuis P-50.1. Sur le fond, le courriel dit : « je t'ai
offert […] de m'occuper d'alexia pour que tu puisse partir du travail plus tard pour que tu
puisse egalement partir de la maison plus tard ». La référence l'a volontairement calibré comme
un **pont** : le mot « garderie » n'y figure pas. Ta note apporte le contexte de garderie, que ton
témoignage devra porter. Conséquence pour le ménage de la rive : **fusionner deux courriels en
double doit reporter les notes de leurs fils**.

**Les fils de 2010 : le chapitre d'avant la garderie.** Ils sont utilisés ailleurs
(`piece_emails_petite_enfance_2010.md`, `document_de_faits.md`, atelier 15 et 16), mais pas dans
la référence de la garderie. Ils montrent la même fonction (organiser les soins pendant que les
deux parents travaillent), remplie autrement : LP coordonne les grands-mères, et il garde lui-même
Alexia un jour de semaine. Email 601 (Johanne, 23 août 2010) : « tu dois également rester à la
maison une journée de la semaine ». Email 603 (LP, 8 nov. 2010) : « elise reste à la maison et
je moi je prends le mercredi ». **Ils ne portent pas sur la
garderie** (vérifié le 2026-10-16). Aucun des douze courriels ne mentionne la garderie : ils
organisent une garde **à domicile** par les grands-mères (« garder le vendredi », « chez vous à
7H30 ») et le jour de semaine de LP. « Pas de place en garderie » vient de la note, non des
courriels. Leur portée est le § 6 (« depuis la naissance d'Alexia ») : ils relèvent d'un arbre
« petite enfance 2010 », distinct de la garderie. Même la borne de début de la garderie se prend
ailleurs, dans l'email 68 (mars 2011).

**Hors garderie, une note de danse à signaler : le fil 131.** Ta note : « une journée de danse
de la demanderesse durant la session d'automne 2013 ». Le dimanche 1er décembre 2013, LP à
Johanne : « Viens tu demain? » ; elle : « oui - je serai là » (emails 498 et 499). Le lendemain
est le lundi 2 décembre. Or l'automne 2013 est une session au **jour non déterminé** dans la
référence (01), qui ne cite pas ce fil. Le seul autre usage est l'atelier, au fichier 16.
Calibrage : le texte ne mentionne ni la danse ni l'absence d'Élise (le fil s'intitule « Linge »).
Par la règle de la référence elle-même, il ne fixe pas le jour sans ton témoignage. Le lundi
concorde avec le créneau de l'hiver-printemps 2014, mais un jour ne se transporte pas d'une
session à l'autre.

### 12.7 La soirée du 2 décembre 2013 (question de LP, 2026-10-16)

**Ce que la base contient** (courriels du 24 nov. au 9 déc. 2013, événements, photographies) :

| Moment | Pièce | Contenu |
|---|---|---|
| dim. 1er déc., 18 h 01 | email 498 (fil 131, « Linge ») | LP à Johanne : « Salut. Viens tu demain? Elise a fait un sac de linge qu elle veut vendre 50 $ sur kijiji. Tu pourrais voir sibca t interesse avant qu elle l affiche » |
| dim. 1er déc., 20 h 31 | email 499 | Johanne : « oui - je serai là - est ce que tu es libre dimanche prochain pour un souper » |
| dim. 1er déc., 19 h 37 à 19 h 58 | event 271, 7 photos | « LP est chez lui avec Alexia et Nicolas » — la veille, le soir |
| lun. 2 déc., 11 h 40 à 12 h 26 | emails 500 à 504 | cadeau de Noël, réparation de la voiture ; **rien sur la visite du soir** |
| lun. 2 déc. | — | aucun événement, aucune photographie |

De septembre 2013 à juin 2014, **aucun autre courriel** entre LP et Johanne n'organise une visite.
Seul le fil 25 (janvier 2014) parle d'un virus dans la maison.

**Ce que le texte établit.** Johanne prévoyait d'être à la maison le lundi 2 décembre 2013.

**Ce qu'il n'établit pas.** Ni l'heure (« demain », sans « soir »), ni l'absence d'Élise, ni la
danse, ni que la visite a eu lieu.

**Les indices, à leur juste poids :**
- « Viens tu demain? » ressemble davantage à la vérification d'une visite habituelle qu'à une
  invitation (« peux-tu venir »). C'est une lecture du texte, non une preuve ;
- le lundi est le créneau directement établi pour l'hiver-printemps 2014 (events 274 et 278), et
  Johanne figure sur les deux lundis photographiés. Mais un jour ne se transporte pas d'une
  session à l'autre (règle 7 de la référence) ;
- Johanne doit voir le sac de linge d'Élise « avant qu'elle l'affiche ». Avec la rupture, cela se
  lit plus naturellement comme une visite en l'absence d'Élise. C'est compatible avec une soirée
  de danse, sans l'établir.

**Conclusion.** Par la règle de la référence (une visite n'identifie un jour de danse que si elle
est expressément reliée à la danse), le fil 131 **ne fixe pas** à lui seul le jour de l'automne
2013. Le témoignage de LP peut le faire : l'heure de la visite, l'absence d'Élise, la raison de
cette absence. Il porterait alors le lundi de l'automne 2013 au degré « soutenu par le
témoignage ».

### 12.8 La règle de LP : quand Johanne se rend chez Alexia, Élise danse (2026-10-16)

> **LP, mot pour mot** : « la rêg;e universelle, quand johanne se dirige a la maison d'Alexia,
> Elise dance. »

**Ce que la règle change.** La référence (01) exige que la visite soit **expressément** reliée à
la danse : c'est le standard documentaire, sans témoignage. La règle de LP est une **règle de
témoignage** (art. 2843 : des faits dont il a eu personnellement connaissance). Elle fait de toute
visite de Johanne à la maison un soir de danse. Les deux degrés coexistent dans l'arbre, au
nœud A4 :
- **par le document seul** : seule une visite expressément reliée à la danse fixe le jour ;
- **avec le témoignage de LP** : toute visite documentée de Johanne à la maison fixe le jour.

**Ce qu'elle débloque.** Les visites documentées après la rupture :

| Visite | Jour | Session | Degré par le document seul | Degré avec la règle |
|---|---|---|---|---|
| 8 déc. 2010 (emails 81, 80) | mercredi | automne 2010 | direct | direct |
| 15-16 mars 2011 (emails 66, 116, 115) | mardi, mercredi | hiver-printemps 2011 | direct | direct |
| 8 mai 2013 (email 474) | mercredi | hiver-printemps 2013 | fortement soutenu | **établi par témoignage** |
| **2 déc. 2013 (emails 498, 499)** | **lundi** | **automne 2013** | **non déterminé** | **établi par témoignage** |
| 27 janv., 3 mars 2014 (events 274, 278) | lundi | hiver-printemps 2014 | direct | direct |

L'automne 2013 passe de « jour non déterminé » à **lundi**. Les autres sessions indéterminées
(automne 2011, 2012 et 2014, hiver-printemps 2015) restent sans visite datée dans la base. La
série des visites demeure « à compléter » dans la référence.

**La règle était déjà écrite par LP**, dans sa note sur le fil 66 (le 7 décembre 2010) :

> « L'intersection de ces 2 faits, le refus de la demanderesse d'entretenir une relation avec la
> famille paternelle d'Alexia et sa participation hebdomadaire a des cours de dance permet de
> déterminer des absences de la demanderesse durant la cohabitation des parties. Par exemple, si
> la grand mère paternelle d'Alexia discute d'une visite ou fait une visite un soir de semaine à
> la résidence familiale d'Alexia, c'est que la demanderesse suit un cours de dance, ce jour de la
> semaine et pour la durée de la session. »

La même note fixe la période : « durant les 5 prochaines années, jusqu'en février 2015 », à
compter du 7 décembre 2010. Les gardes de 2010 sont antérieures.

**LP maintient la formulation universelle** (2026-10-16, réitérée mot pour mot). *Corrigé le
2026-10-16* : la version précédente de ce paragraphe proposait de l'adoucir (« n'entrait que
pendant… ») et présentait l'email 67 comme un contre-exemple de la lecture littérale. Les deux
sont retirés. Le 7 mars 2011, Johanne écrit qu'elle passait **devant** la maison. Elle ne s'y
dirigeait pas, n'y est pas entrée et n'avait annoncé aucune visite. L'épisode n'entre donc pas
dans la règle.

---

## 13. Le même exercice pour les activités des enfants

Demandé par LP le 2026-10-16. Même méthode : partir de la référence, lire les notes de LP sur les
fils, vérifier dans la base, ne pas rouvrir ce qui est calibré.

### 13.1 Les sources

| Source | Ce que c'est | Statut |
|---|---|---|
| `legal/implication_parentale_recurrence/03_activites_enfants.md` | **la référence** : proposition (accompagnateur / second enfant), ChatSequence 12, inférence cumulative, analyse de l'échange de 2016, natation (fil 75, event 62, email 8, email 305), renvoi au soccer | **fait foi** ; « axe ouvert — fonctionnement général établi, corroboration à compléter » |
| `legal/implication_parentale_recurrence/03a_soccer_alexia_ete_2013.md` | sous-thème : le soccer de l'été 2013 et la prise en charge de Nicolas | **fait foi** pour le soccer ; « deux éléments demeurent testimoniaux » |
| `06_sorties_activites_librement_organisees.md` | les sorties organisées librement par le père. Son plancher **exclut l'escalade** | thème voisin |
| **Acte déposé** (doc 9) | § 32 (activités structurées, P-52), § 33 (AcroGym, soccer, escalade : P-53, P-54, P-55), §§ 45-47 (été 2013 : P-54, P-55, P-76, P-106), § 131 (aide familiale pour la natation) | gelé |
| **Atelier** | 10 ¶ 22-F ; 12 ¶ 104-E, 104-F ; 14 A4.11 ; 11 (ChatSequence 12) ; 25 ¶ 42, ¶ 44 c), ¶ 48 (P-52) | en cours |
| **Notes de LP** sur les fils | fil 75 (natation 2010), 26 et 159 (soccer), **83** (natation de Nicolas), **132** (YMCA), **1** (escalade) | voir § 13.5 |

### 13.2 Le fait

Repris de la référence et du ¶ 52 de LP (29 sept.), **à confirmer** :

> Lorsqu'un enfant devait être accompagné à une activité, le père l'accompagnait, ou assurait les
> soins de l'enfant qui restait à la maison.

### 13.3 L'arbre

```
FAIT (à confirmer) — accompagnement à l'activité, ou soins du second enfant
                                            [établi — témoignage + présomption + occurrences]
│
├─ A. Les activités existent, en sessions, à horaire fixe                          [structurel]
│   ├─ A1 ChatSequence 12 (23 oct. 2014) : natation, gymnastique, danse, cheerleading, ski,
│   │      plusieurs sessions par année ; Nicolas en gymnastique à deux ans          attestation
│   ├─ A2 natation
│   │    ├─ fil 75 (mai 2010) : « c est dimanche a 9hre » — LP donne l'horaire     attestation
│   │    ├─ email 8 (C3) : Élise reproche à LP d'avoir été « tanné » après un cours de
│   │    │    dix semaines                                                       attestation
│   │    ├─ email 305 (C11), 2016 : aide familiale « pour leur cours de natation » vérification
│   │    └─ email 355 (fil 83), 27 août 2013 : LP paie l'inscription de Nicolas, six mois,
│   │         aux cours de natation de Saint-Lambert                             attestation  [nouveau au thème]
│   ├─ A3 gymnastique : events 136 et 150 (P-53), AcroGym d'Alexia, dimanches 11 déc. 2011 et
│   │      29 janv. 2012, même session                                          attestation  [nouveau au thème]
│   ├─ A4 danse d'Alexia : ChatSequence 12 ; clavardage 127 (« il y a les deux cours ») ;
│   │      récitals : events 220 (16 déc. 2012), 224 (9 févr. 2013), 302 (14 déc. 2014)
│   │                                                                            attestation  [nouveau au thème]
│   └─ A5 soccer, été 2013 → renvoi [soccer 2013] (03a)
│
├─ B. La règle de division : un parent accompagne, l'autre prend le second enfant
│   ├─ B1 TÉMOIGNAGE : la règle familiale habituelle
│   ├─ B2 email 7 (C3) : « Quand les enfants avaient des cours, tu les prenaient les 2 et moi je
│   │      restait a la maison et me saoulais pendant ce temps la » — la négation du scénario
│   │                                                                            cadre
│   ├─ B3 email 306 : « pas 50 % » — ne nie pas la présence ; pas un aveu (art. 2851)
│   └─ B4 inférence cumulative (03) : plusieurs cours récurrents + deux enfants + négation du
│          scénario = présence récurrente avec l'un ou l'autre                 inférence
│
├─ C. Le père accompagnateur — occurrences
│   ├─ C1 natation : event 62 (P-52), 7 mai 2011, LP dans l'eau avec Alexia, 17 photos ;
│   │      fil 132 (janv. 2011) : LP est membre du YMCA de la rue Stanley   attestation ; vérification [fil 132 nouveau au thème]
│   ├─ C2 AcroGym : events 136, 150 (P-53) — LP photographie Alexia au cours   attestation  [nouveau au thème]
│   ├─ C3 récitals de danse d'Alexia : events 220, 224, 302 — LP présent aux fins de session
│   │                                                                            attestation  [nouveau au thème]
│   │      RÉSERVE : ces récitals ne disent rien du jour de danse de la **mère** (01) ; ici ils
│   │      servent l'activité d'**Alexia** — même élément, autre rôle
│   └─ C4 soccer : events 239, 263 (P-54) → renvoi [soccer 2013]
│
├─ D. Le père avec le second enfant
│   ├─ D1 soccer 2013 : il prend Nicolas pendant que la mère anime les ateliers
│   │      → renvoi [soccer 2013] : thread 26 (P-76) « Y a pas dw soccer demain » + TÉMOIGNAGE
│   └─ D2 autres occurrences : à compléter (03, état de la preuve)
│
├─ E. Organisation et décision
│   ├─ ChatSequence 12 : connaissance des sessions, discussion de l'âge de Nicolas  attestation
│   ├─ email 355 : il paie une inscription                                       attestation
│   └─ fil 75 : il est la source de l'horaire                                   attestation
│
└─ RÉSERVES (référence, limites admises)
     la simultanéité de deux activités n'est pas requise ; l'existence d'une activité ne suffit
     pas sans le témoignage ou les pièces sur la division ; aucune prétention que le père
     accompagnait chaque activité, ni que la mère n'en accompagnait pas ; les coûts ou les
     inscriptions montrent l'organisation, non la présence ; l'aide familiale ultérieure ne
     remplace pas la preuve du fonctionnement antérieur
```

### 13.4 Ce que les activités servent

| Cible | Usage | Où |
|---|---|---|
| § 16, « C'est la demanderesse qui s'occupait des enfants, **qui allait aux activités**, etc. » | **la cible directe** : le père accompagnait, ou gardait le second enfant | 03 ; doc 9 §§ 32-33 |
| § 15, « rarement disponible » | une présence aux structures hebdomadaires et saisonnières | 05 ; 14 |
| L'été 2013, « parti tout l'été » | le soccer (03a), l'inscription de Nicolas à la natation (email 355), l'escalade (P-55) | doc 9 §§ 45-47 ; note du fil 83 |
| Démonstration 1, mouvement 3 | les structures (¶ 42), la division (¶ 44 c), les points de contrôle (¶ 48 : P-52) | 25 |

### 13.5 Ce que l'exercice a trouvé

Ces pièces sont **présentes au corpus**, et la plupart dans l'acte déposé. La **référence** 03 ne
les mobilise pas :
- **l'email 355** (fil 83, 27 août 2013) : LP paie l'inscription de Nicolas, six mois, aux cours de
  natation. La référence classe les activités de Nicolas comme un « projet contemporain établi ;
  réalisation à confirmer ». Cet email en documente une, déjà en 2013, et sert aussi l'été 2013.
  Il a une fiche et des cotes d'amendement ;
- **les events 136 et 150** (AcroGym, P-53, cités au § 33 de l'acte déposé) : deux dimanches de la
  même session, LP au cours. Ils remplissent la ligne « Père accompagnant un enfant à une
  activité », marquée « à compléter » dans la référence ;
- **les events 220, 224 et 302** (récitals de danse d'Alexia, 2012 à 2014) : LP présent à chaque
  fin de session. Ils ne sont pas dans la référence, et la référence de la danse interdit, avec
  raison, de les utiliser pour le jour de danse de la mère. Ils servent ici l'activité d'Alexia ;
- **le fil 132** (janvier 2011) : LP est membre du YMCA de la rue Stanley. Il corrobore
  l'explication de l'event 62.

**Une question de classement : l'escalade.** P-55 (onze séances, de juin 2013 à mars 2014), plus
l'event 327 (février 2015, avec Nicolas) et la note du fil 1. L'acte déposé la range parmi les
« activités structurées et récurrentes » (§ 32). La référence 03 ne la mentionne pas. La
référence 06 l'exclut expressément de son plancher. Le critère posé par 03 (inscription et
horaire fixe, ou sortie organisée librement par le père) la placerait plutôt en 06. **Elle
n'appartient aujourd'hui à aucun arbre** : son classement revient à LP.

**Tranché par LP (2026-10-16)** : « l'escalade est une activité non structurée et sans fréquence
définie, elle est du même type que les sorties au parc ». Elle relève donc de l'arbre des
**sorties librement organisées** (06), non des activités. Le § 32 de l'acte déposé, qui la range
parmi les « activités structurées et récurrentes », est gelé. La version 2 la classe parmi les
sorties.

---

## 14. Les événements (`Event.explanation`) — lecture du 2026-10-16

Demandée par LP : faire pour les événements ce qui a été fait pour les notes des fils. Les
événements n'ont pas de champ `note`. Les observations de LP y sont dans **`explanation`**, rédigée
événement par événement.

**Méthode** (`docs/modele_preuve/scan_evenements.py`, lecture seule). Les 313 événements de la
cohabitation (6 oct. 2009 – 23 févr. 2015) sont classés par thème selon leur explication. Pour
chacun, on vérifie s'il est cité par son numéro dans la référence de son thème
(`implication_parentale_recurrence/`), s'il porte une cote de juillet (`BordereauDepotJuillet`) et
s'il est cité ailleurs dans `legal/`. **« Non cité » ne veut pas dire « inconnu »** : un fait peut
être documenté par une autre pièce (le voyage de Cape Cod de 2012 l'est par des courriels).

| | Événements |
|---|---:|
| cités dans une référence de thème | 85 |
| portant une cote de juillet | 107 |
| cités ailleurs dans le corpus seulement | 147 |
| cités nulle part par leur numéro | 28 |

### 14.1 Par thème

| Thème | Référence | Constat |
|---|---|---|
| Danse de la mère | 01 | les 6 événements sont dans la référence |
| Garderie | 02 | les events 213 et 214 sont dans la référence |
| Activités | 03, 03a | 62, 239 et 263 y sont. **136 et 150** (AcroGym, P-53) et **220, 224, 302** (récitals d'Alexia) n'y sont pas (voir § 13.5) |
| Sorties | 06 | la référence retient un plancher de 20 dates sur trois catégories (parcs, chalet, Estrie) et exclut l'escalade, le vélo, les festivals, le zoo, les glissades et les voyages, **sans justification écrite** (§ 14.3) |
| Présence au domicile | 08 | l'assiette est définie par un critère (117 événements, 100 journées), et non par une liste. Les événements « chez lui avec » y sont couverts |

### 14.2 Ce que la lecture apporte

**L'escalade entre aux sorties** (décision de LP, § 13.5). La référence 06 l'excluait de son
plancher, sans raison écrite (§ 14.3). Avec la décision de LP (« du même type que les sorties au
parc »), les events 316 à 327 ajoutent jusqu'à **11 dates distinctes** (du 27 juin 2013 au
16 mars 2014, et le 7 février 2015 avec Nicolas), sous réserve de chevauchement avec les dates
déjà retenues.

**Deux sorties au parc Alexandra hors du plancher**, dans une catégorie pourtant retenue par 06 :
- event 208 (1er sept. 2012) : LP revient à pied du parc avec Alexia ;
- event 88 (24 juill. 2011, P-68) : au parc avec Alexia et Élise.

L'event 25 (11 nov. 2010, P-56.1) est antérieur à la période du plancher. Ces trois événements
sont à confronter au critère de 06, qui n'est pas écrit.

**Les 28 événements cités nulle part**, classés :

| Groupe | Événements | Portée possible |
|---|---|---|
| Les premières semaines d'Alexia | 3 (7 oct. 2009, « au moment de sa naissance »), 4, 6, 7, 10 | présence de LP dès la naissance, contre « depuis la naissance d'Alexia » (§§ 5-6). Une photographie établit une présence, non des soins : la portée est mince |
| La naissance de Nicolas | 221 (1er févr. 2013, 22 h 50) | présence de LP le jour de la naissance |
| Le projet de séparation de 2012 | 206 (appartement loué pour juillet 2012, à sous-louer) ; 205 (inondation du sous-sol) | chronologie de 2012 (fil 79). Les faits sont connus du corpus par d'autres pièces |
| Le voyage à Cape Cod de juillet 2012, sans Alexia | 191 à 197 | **pièces potentiellement défavorables**. Le voyage est connu (`piece_emails_cape_cod_2012.md`), mais ses photographies n'y sont pas rattachées. À lire avant que la partie adverse ne le fasse |
| Une sortie et une journée au domicile | 93 (parc de Boucherville, 6 août 2011) ; 112 (25 sept. 2011) | candidats pour 06 et 08 |
| Sans portée apparente | 26, 29, 130, 131, 153, 163, 177, 193, 209, 212, 272, 292 (dont cinq sans explication) | — |

### 14.3 La justification du plancher de 06 (question de LP, 2026-10-16)

*Corrigé le 2026-10-16.* Les §§ 14.1 et 14.2 disaient d'abord que la référence retenait
« volontairement » son plancher et que ses exclusions étaient « des choix, pas des oublis ».
C'était une surinterprétation. La référence 06 écrit :
- « Axe d'implication ponctuelle **en cours de consolidation**. Le présent inventaire retient
  seulement trois catégories nommées — parcs, chalet et Estrie — et applique un décompte
  conservateur par date » ;
- « Le sous-corpus **actuellement retenu** documente 20 dates » ; « Sélection limitée aux trois
  catégories » ;
- « Ce plancher exclut notamment l'escalade, le vélo, les festivals, le zoo, les glissades d'eau,
  les voyages, le voilier et plusieurs événements familiaux. Il ne prétend donc pas mesurer la
  totalité des activités père-enfants. »

**Aucune raison n'est donnée** pour le choix de ces trois catégories, ni dans le fichier (créé
avant le dépôt, modifié le 19 août 2026), ni dans le journal de l'atelier. Les seules exclusions
motivées sont celles de la catégorie « Piscine » : la natation est une activité structurée
(thème 3), et la baignade relève d'un rassemblement familial (thème 7). Le plancher est un
**inventaire de travail**, non un choix raisonné.

**Hypothèse, non vérifiée.** Plusieurs sorties exclues se font avec Élise (zoo de Granby, event
106 ; festival de Longueuil, 107 ; glissades de Bromont, 246 ; festival de jazz, 244). Elles
montrent moins l'initiative du père seul. Cette raison ne vaut pas pour l'escalade (LP seul avec
Alexia) ni pour le vélo (event 234, LP avec Alexia et un ami). **Rien ne justifie de les écarter.**
Avec la décision de LP, l'escalade entre au plancher au même titre que les parcs.


---

## 15. Verdict : l'architecture modélise-t-elle les axes ?

Question de LP (2026-10-16). La complétude de la preuve est reportée. Trois axes ont été analysés :
la danse (§§ 10-11), la garderie (§ 12) et les activités (§ 13). On confronte ici **chaque trait
structurel observé** aux constructions du modèle : paragraphe → démonstration → preuve (arbre) →
élément, le bordereau calculé et les versions gelées.

### 15.1 Trait par trait

Légende : ✔ porté tel quel · ✔⁺ porté grâce aux précisions du § 8.2 · ➕ demande un ajout ·
❓ règle à fixer.

| # | Trait observé | Axes | Construction du modèle | |
|---|---|---|---|---|
| 1 | Un fait racine, décomposé en affirmations sur plusieurs niveaux (A, B, C, D…) | les trois | nœuds d'affirmation imbriqués | ✔⁺ |
| 2 | Des feuilles de granularités différentes : phrase de courriel ou de PDF, événement entier, document entier (calendrier P-90), énoncé d'un acte adverse (§ 17 de P-19), message de clavardage | les trois | élément = clé générique vers la rive | ✔ — voir 15.2, point 3 |
| 3 | Le même élément sous plusieurs nœuds avec des rôles différents (email 305 en A1, B6 et C1 ; email 7 cadre en A et en E ; le 3 déc. 2014 en maladie et en garderie) | les trois | rôle porté par le nœud-feuille, relatif à son parent | ✔⁺ |
| 4 | Des degrés par affirmation : direct, fortement soutenu, plus probable que non, non déterminé, à authentifier | les trois | degré sur le nœud d'affirmation | ✔⁺ |
| 5 | **Deux degrés pour la même affirmation** : par le document seul, et avec le témoignage (la règle des visites de LP fait passer l'automne 2013 de « non déterminé » à « lundi ») | danse | — | ➕ |
| 6 | Des réserves et limites admises, au niveau d'un nœud ou de la racine | les trois | nœud de nature RÉSERVE | ✔⁺ |
| 7 | Le témoignage comme appui sans document (mode général, permanence de la rupture, « jusqu'à trois ») | les trois | appui TÉMOIGNAGE, hors bordereau | ✔⁺ |
| 8 | Des règles d'inférence : règle des visites, présomptions de fait (art. 2846, 2849), inférence cumulative, « on n'embauche pas le remplaçant » | les trois | champ règle du nœud ; une règle partagée devient un nœud vers lequel on renvoie | ✔⁺ |
| 9 | Structure × occurrences : la quantité vient de la structure (calendrier, nature de la garderie, sessions d'activités) | les trois | nœud structurel + inférence | ✔⁺ |
| 10 | **Des affirmations datées par une période** : chaque session de danse, la portée de la règle des visites (du 7 déc. 2010 à février 2015), la période de la garderie (de 2011 à 2015), « pour la durée de la session », et la règle des sessions (un jour ne vaut pour une autre session que si celle-ci a son propre appui) | danse, garderie | — | ➕ |
| 11 | La distribution chronologique des occurrences | garderie, danse | vue calculée sur les dates des feuilles (§ 8.2, point 7) | ✔ — avec 10 pour les sessions dont aucune pièce ne fixe le jour |
| 12 | Des renvois entre axes : garderie → danse (email 347), activités → soccer (03a), danse → rupture avec la famille paternelle | les trois | renvoi vers un nœud d'une autre preuve, sans cycle | ✔⁺ |
| 13 | Un sous-thème traité comme un arbre à part (soccer 2013) | activités | preuve distincte, atteinte par renvoi | ✔⁺ |
| 14 | Plusieurs cibles par axe, atteintes par des nœuds différents (§§ 6, 7, 15, 16, 17 ; l'été 2013) | les trois | démonstration avec cibles ; poignées à tout niveau | ✔⁺ |
| 15 | Hiérarchie à cinq étages : élément → conclusion intermédiaire → axe → synthèse des événements cycliques → synthèse multidimensionnelle | les trois | affirmations imbriquées + renvois entre preuves | ✔⁺ |
| 16 | Le silence ne vaut pas aveu (art. 2851) : « pas 50 % » atteste un seuil, non une absence | les trois | rôle (« cadre », « attestation d'un seuil ») + degré | ✔ |
| 17 | Des interdits d'usage : les récitals d'Alexia ne disent rien du jour de danse de la mère | danse, activités | réserve sous le nœud concerné | ✔ |
| 18 | Des lacunes de travail : « à compléter », « à authentifier » | les trois | degré ou état du nœud | ✔ |
| 19 | Le verbatim rendu depuis l'élément, la phrase entière, sans troncature | les trois | rendu depuis l'élément (décision de LP) | ✔ |
| 20 | « Notamment » : un paragraphe montre une sélection des feuilles d'un sous-arbre | les trois | mode d'affichage sur le lien paragraphe → démonstration (§ 9.4) | ✔ |
| 21 | **Un plancher compté** (20 dates de sorties, 100 journées au domicile), sur un critère de sélection et une unité de compte (la journée, sans double compte) | activités, sorties | — | ➕ |
| 22 | Un message de clavardage comme élément (clavardage 127, 463 à 476, 504) | les trois | élément vers `ChatMessage` ; mais quel est son **document** au bordereau ? | ❓ |
| 23 | Une photographie précise comme élément (Johanne sur une photo du 3 mars 2014), plutôt que l'événement entier | danse | élément vers `Photo` ; document = l'événement | ❓ |
| 24 | Un doublon sur la rive, et une note attachée au doublon (email 48 / 347) | danse, garderie | entretien de la rive : fusion, journal de redirection, report des notes | ✔ |
| 25 | Les axes évoluent, et les versions gelées doivent les conserver tels qu'ils étaient | les trois | gel par copie du chemin (§ 8.2, point 2) | ✔⁺ |

### 15.2 Ce que l'architecture doit recevoir

Rien de ce qui a été observé n'oblige à remettre en cause la chaîne. Il faut trois ajouts et deux
règles :

1. **➕ Une période sur les nœuds d'affirmation** (début et fin, facultatifs). Elle porte les sessions
   de danse, y compris celles dont aucune pièce ne fixe le **jour** (« au moins un soir, jour non
   déterminé »). *Corrigé le 2026-10-16* : la version précédente les disait « sans feuille ». Or
   chaque session de la cohabitation est appuyée par P-83 (la biographie ne mentionne ni pause ni
   arrêt jusqu'en 2016), par P-90 et par le témoignage du père. Seul le jour peut manquer. La
   période porte aussi la portée d'une règle (la règle des visites vaut du 7 décembre 2010 à
   février 2015) et la **règle des sessions, précisée par LP** : un jour établi pour une session
   ne vaut pour une autre que si **celle-ci a son propre appui**. Avec des périodes, la règle
   devient vérifiable par le modèle.
2. **➕ Le fondement du degré.** Chaque degré dit sur quoi il repose : le **document seul**, ou le
   **document avec le témoignage**. Une même affirmation peut porter les deux (« non déterminé »
   par le document, « lundi » avec le témoignage). C'est ce qui permet de distinguer ce que la
   preuve écrite établit seule de ce qui dépend du témoin. Le contre-interrogatoire porte
   exactement sur cette différence.
3. **➕ Un nœud d'agrégation compté** : une **unité de compte** (la journée, la date distincte, la
   session) et un **critère de sélection écrit**. Le décompte devient une vue calculée sur les
   feuilles. L'absence de critère écrit pour le plancher de 06 (§ 14.3) montre que ce critère doit
   être une donnée, non une phrase perdue dans la prose.
4. **❓ Le document d'un message de clavardage** (pour le bordereau) : la séquence qui le contient
   (`ChatSequence`, comme P-62), ou le fil ? La même question que « le courriel ou le fil » pour
   les courriels. Le précédent (le courriel, non le fil) suggère : **la séquence**, à condition
   qu'elle existe pour chaque message utilisé.
5. **❓ Le document d'une photographie** : l'événement qui la contient. La cote va à l'événement ;
   la photographie précise est l'élément, quand l'unité minimale suffisante le demande.

### 15.3 Ce que les axes n'ont pas mis à l'épreuve

- **La démonstration** n'a été exercée que dans sa forme simple : une liste de poignées et des
  cibles. Le portrait du § 10.4 (neuf usages de la danse, chacun vers un nœud différent) montre
  qu'elle est nécessaire, mais la portée par paragraphe, l'état de confirmation et la version
  examinée n'ont été éprouvés sur aucun paragraphe réel de la version 2.
- **Le bordereau calculé** n'a pas été calculé : les arbres ont été dessinés, non construits.
- **Le gel et la copie du chemin** n'ont pas été éprouvés sur une modification réelle.

### 15.4 Verdict

**Oui. L'architecture modélise la structure des trois axes**, sous réserve des ajouts 1 à 3 et des
règles 4 et 5. Les traits les plus exigeants — un même élément sous plusieurs rôles, la
hiérarchie à cinq étages, les renvois entre axes, le témoignage comme appui, la poignée à tout
niveau — sont portés par les précisions déjà retenues au § 8.2. Les trois ajouts concernent le
**temps** (période), la **source de la certitude** (document ou témoignage) et le **compte**
(plancher). Aucun n'oblige à revoir les trois niveaux paragraphe → démonstration → preuve →
élément.

L'épreuve suivante naturelle : construire un arbre réel, par exemple celui de la danse (§ 11), sur
un paragraphe réel de la version 2. On éprouverait alors le § 15.3 : la démonstration, le
bordereau calculé et le gel.

---

## 16. La théorie des cours de danse de LP, dans le modèle

Le texte intégral est consigné au journal de l'atelier (`legal/redaction_v2/99_journal.md`,
entrée 39) et, à la demande de LP, **dans l'axe de la danse lui-même**
(`legal/implication_parentale_recurrence/01_cours_danse_mere.md`, section « La théorie des cours de
danse »). On le fait correspondre ici aux nœuds de l'arbre du § 11.

### 16.1 Les affirmations de la théorie, nœud par nœud

| Affirmation de la théorie | Nœud | Appuis |
|---|---|---|
| « Durant toute la période de cohabitation » | A1, continuité | P-83 : 1999-2016, sans pause ni arrêt |
| « de une à 3 fois par semaine » | C | C1 (plancher), C2 (deux soirs, 2010-2011), C3 (jusqu'à trois : témoignage ; email 7) |
| « deux sessions par année, plus de 30 semaines » | A2 | P-90 |
| « C'est le défendeur qui assurait les soins des enfants (routine du soir, bain-dodo) » | B | B1 (events 46, 52, 274, 278), B2 (email 347), B4 (témoignage) |
| « Il prenait en charge Alexia lorsqu'elle était un nourrisson » | B5, première configuration ; session de l'hiver 2010 | event 19 (spectacle de juin 2010 : une chorégraphie, donc un cours pendant la session ; Alexia a de 3 à 8 mois) ; témoignage |
| « Il prenait en charge Nicolas et Alexia lorsque Nicolas était un nourrisson et qu'Alexia avait 3 ans » | B5, seconde configuration ; sessions de 2013 et 2014 | **hiver-printemps 2013** (email 474 : Nicolas a 3 mois) et **automne 2013** (fil 131 : Nicolas a 10 mois), déterminés par la règle des visites ; **hiver-printemps 2014** (events 274, 278) ; témoignage |
| « incompatible avec un père peu impliqué… » | racine → poignées de la démonstration 1 | renvois vers les autres axes (activités structurées et non structurées, garderie, maladie) |

### 16.2 La chaîne des visites, telle que LP la formule

La théorie pose cinq contraintes, puis les cumule :
1. une visite de Johanne implique une absence d'Élise. Toujours, depuis la rupture (email 82 ;
   emails 81, 80) ;
2. **l'absence de visite n'implique pas la présence d'Élise**. Les visites sont sporadiques ;
3. un cours de danse implique l'absence d'Élise. Les exceptions sont rares : « la danse est une
   passion pour Élise » ;
4. un cours revient le même jour, toute la session ;
5. la participation à un cours mène au spectacle de fin d'année.

Conclusion : une visite un mercredi de la session d'hiver, donc un cours le mercredi pendant toute
la session, auquel Élise « participe très probablement ». Donc LP assure les soins pendant cette
période.

**Dans le modèle :**
- les contraintes 1 à 5 sont des nœuds de règle sous A4 et A2. La contrainte 2 est la réserve qui
  empêche de lire une absence de visite comme une présence ;
- le degré de la conclusion est celui que la théorie lui donne elle-même : « très probablement ».
  Il repose sur le **document** (la visite, la rupture, la structure) **et sur le témoignage** :
  c'est LP qui sait que les absences des soirs de visite étaient la danse (sa règle, § 12.8). La
  contrainte 1 établit l'absence ; c'est le cumul avec 3, 4 et le témoignage qui en fait un soir
  de danse. Le modèle rend ce partage visible, grâce au fondement du degré (§ 15.2, point 2) ;
- la contrainte 5 donne aux spectacles (events 19 et 78) leur fonction : ils attestent un cours
  **pendant la session** du spectacle, sans en donner le jour ;
- « Les courriels de Johanne ne servent que d'appuis à la théorie » : ils sont des **feuilles
  sous A3**. Ils déterminent des jours ; ils ne portent pas la proposition, que portent A1, A2 et
  B. C'est exactement la place que l'arbre leur donne.

**Ce que la théorie confirme pour l'architecture** : chacune de ses affirmations trouve son nœud.
Sa logique (une implication, sa réciproque refusée, une règle avec des exceptions rares, une
conclusion probable) se représente avec les nœuds de règle, les réserves et les degrés. Le seul
ajout qu'elle sollicite est celui déjà relevé : le **fondement du degré**, document ou
témoignage.


---

## 17. Le régime des citations : ancien et nouveau (proposition de LP, 2026-10-17)

> **LP** : « je ne souhaite pas procéder au ménage des quotes tel que nous l'avions anticipé. […]
> Nous allons plutôt établir l'ancien et le nouveau régime. Les quotes actuelles appartiennent à
> l'ancien régime, nous allons en créer un attribut régime (ancien/nouveau, True or False — peu
> importe) et nous l'utiliserons pour filtrer. »

### 17.1 Faisabilité : immédiate

- Un champ sur `email_manager.Quote` et `pdf_manager.Quote`, une migration. Les 394 citations
  actuelles (268 + 126) prennent la valeur « ancien ».
- Le nouveau pont ne prend comme éléments que les citations du nouveau régime. L'ancien pont
  (`TrameNarrative`, nœuds des docs 5 et 6, `ProducedExhibit`) continue de pointer vers les
  anciennes, **sans qu'on touche à une seule référence**.
- Le champ est une propriété de la rive (la façon dont la citation a été faite). Le pont le lit,
  ce qui respecte la règle de dépendance.

### 17.2 Efficacité : elle retire l'essentiel du ménage

| Travail prévu par `PLAN_FUSION_CITATIONS.md` | Avec les deux régimes |
|---|---|
| Étendre 138 fragments, scinder 69 citations, réancrer 48 | **supprimé** : les anciennes restent telles quelles |
| Fusionner 42 groupes de doublons, repointer ~1 100 références (527 M2M, 80 nœuds, 585 `ProducedExhibit`) | **supprimé** : aucune référence n'est déplacée, l'ancien pont n'est pas exposé |
| Journal de redirection pour les citations | **supprimé pour les anciennes**. Les nouvelles ne se dédoublonnent pas : elles naissent uniques (§ 17.3, point 2) |
| La règle de la phrase, la position, la certification | **conservées, pour le nouveau régime seulement** |
| Le sort des 80 nœuds des docs 5 et 6 | **sans objet pour le pont** : ils restent dans l'ancien régime |

Le seul travail qui demeure est la création des citations nouvelles. Il fallait le faire de toute
façon : la règle de la phrase imposait déjà de reprendre chaque passage sur l'original. Les
anciennes citations ne sont pas perdues : elles servent de **liste de candidats**. Les
190 passages choisis à la main en août restent consultables.

### 17.3 Quatre conditions pour que le filtre tienne

1. **La valeur par défaut est « ancien ».** Le code crée aujourd'hui des citations à trois
   endroits, tous dans l'ancien pont ou ses écrans : `argument_manager/views.py` (lignes 648
   et 724) et le formulaire de citation de courriel. Si le défaut était « nouveau », ces chemins
   produiraient des citations du nouveau régime sans la règle de la phrase. **Le nouveau régime
   se mérite : seul le chemin de création du nouveau pont le donne.**
2. **Des contraintes en base pour le nouveau régime.**
   - Une contrainte de vérification : une citation du nouveau régime a ses bornes (début et fin
     dans la source).
   - Une **contrainte d'unicité conditionnelle** (PostgreSQL) sur (source, début, fin), limitée
     au nouveau régime : la même phrase ne peut exister deux fois.

   La garde à la création devient une règle de la base, et non une vérification de l'écran.
3. **Un lien de provenance, facultatif** : `issue_de`, de la citation nouvelle vers l'ancienne
   dont elle procède. Il garde la trace du travail de sélection, et dit quelles anciennes
   citations ont déjà été reprises.
4. **Les écrans de la rive affichent le régime** (fiche du courriel, fiche du PDF, liste des
   citations), et filtrent par défaut sur le nouveau. Sinon, une ancienne et une nouvelle
   citation de la même phrase se côtoient sans qu'on les distingue.

### 17.4 Ce que le régime ne règle pas

- **Les doublons de documents** (email 48 / email 347). Le bordereau est indexé par modèle + PK :
  un même message sous deux PK recevrait deux cotes. Même philosophie, appliquée au document :
  **marquer plutôt que supprimer**, par un champ `doublon_de` sur `Email` vers la pièce
  canonique, que le pont et le bordereau ignorent. Les notes du fil en double (fil 38) sont à
  reporter sur le fil canonique (78).
- **La certification des énoncés des actes adverses** : les `Statement` du doc 3 s'écartent du
  scan aux § 6 c) et § 8. C'est un autre modèle, et une autre question.
- **Les séquences de clavardage**, si une `ChatSequence` devait servir d'élément. Elle aussi est
  une sélection, comme une citation. La question se règle avec celle du document d'un message
  (§ 15.2, point 4). Si l'élément est le message (`ChatMessage`), aucun régime n'est nécessaire.

### 17.5 Le nom du champ

Un booléen suffit, et LP le laisse ouvert. Une **valeur nommée** (`regime` : `ANCIEN` |
`NOUVEAU`) se lit mieux dans les filtres et laisse place à un troisième état. L'adjectif
« nouveau », lui, vieillira. Un nom qui dit la règle plutôt que la date, par exemple
`regime = PHRASE` contre `HERITE`, resterait juste dans deux ans.

### 17.6 Verdict

**Faisable immédiatement, et plus efficace que le ménage prévu.** Le régime remplace la fusion,
le repointage et la normalisation des 394 citations par un filtre. Il isole l'ancien pont au lieu
de le modifier, ce qui est exactement la stratégie du pont parallèle. Les quatre conditions du
§ 17.3 sont ce qui rend le filtre fiable. Sans elles, en particulier sans le défaut « ancien »
et sans la contrainte d'unicité, le nouveau régime se contaminerait.

### 17.7 Le plan en deux étapes (LP, 2026-10-17)

Étape 1 : modifier le modèle sans nouvelle citation, filtrer partout, et vérifier que
l'application affiche exactement la même chose. Étape 2 : créer une première citation du nouveau
régime et vérifier qu'elle reste indétectée. Objectifs, tests et inventaire des surfaces :
`docs/modele_preuve/PLAN_REGIME_CITATIONS.md`.

