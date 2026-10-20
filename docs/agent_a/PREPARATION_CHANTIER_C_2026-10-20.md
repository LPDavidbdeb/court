# Préparation technique du chantier C — Agent A

**20 octobre 2026. Socle : `515666eb8c6e7fdcdd265f9187c9c37b769b0fed` (`epic/E01-numerotation-concordance`).**

Ce rapport répond à deux mandats :
- **le mandat préparatoire** : contrat du fournisseur, compatibilité de C0-A, préparation des
  vérifications ;
- **le mandat complémentaire** : reproductibilité du banc et référence exécutée du socle.

**Mandat clos par LP le 20 octobre.** La référence est acceptée : 205 tests applicatifs et 33 tests
d'outillage réussis, isolation vérifiée, aucun changement de schéma, aucun patch C0-A appliqué. Elle a
été reproduite dans un banc neuf construit selon C.2 (C.8).

Les suites de C0-A passent par la gouvernance UML :
- dossiers UC-C-13/14/15 de l'Agent B ;
- anomalie `C0A-REV-01` ;
- approbation de LP ;
- puis mandat d'implantation délimité.

**Ce qui n'a pas été fait :**
- le patch C0-A n'a été ni appliqué ni fusionné ;
- le code applicatif, la base réelle, le serveur et les fichiers de l'Agent B n'ont pas été modifiés ;
- rien n'a été poussé ;
- aucune mesure n'a été faite sur des données réelles.

**Ce qui a été exécuté :** des tests, uniquement dans un banc jetable et isolé (partie C).

Légende des constats :
- **[code]** : lu dans le code au SHA ci-dessus ;
- **[git]** : vérifié par Git ;
- **[exécuté]** : obtenu dans le banc de la partie C ;
- **[rapporté]** : affirmé par un document, non revérifié ici ;
- **[non éprouvé]** : déduit de la lecture, sans exécution.

---

## A. Contrat technique du fournisseur HERITE / PHRASE

Ce qui suit décrit l'existant au SHA ci-dessus. Ce n'est pas une proposition d'architecture.

### A.1 Modèles et interfaces disponibles [code]

| Élément | Emplacement | Rôle |
|---|---|---|
| `QuoteRegime` (`HERITE`, `PHRASE`) | `core/quote_regime.py` | champ `regime` des deux modèles, défaut `HERITE`, indexé |
| `email_manager.Quote` | `email_manager/models.py` | citation de courriel ; FK `email` (`CASCADE`) |
| `pdf_manager.Quote` | `pdf_manager/models.py` | citation de PDF ; FK `pdf_document` (`CASCADE`), `page_number` obligatoire |
| `PhraseAnchor` (mixin) | `core/quote_regime.py` | ancrage, garde, propriétés de certification ; hérité par les deux modèles |
| `create_phrase_quote(source, start, end, *, derived_from=None, page_number=None, certify=None)` | idem | point d'entrée de création |
| `certify_phrase_quote(quote, *, certified_text=None)` | idem | acte de certification distinct (scan) |
| `sha256_text(text)` | idem | SHA-256 hexadécimal du texte UTF-8 (`None` donne `""`) |
| `invisible_pks(model, pks)` | idem | les PK soumises que le gestionnaire par défaut ne rend pas |
| `manage.py create_phrase_quote` | `core/management/commands/` | options `--email` ou `--pdf`, `--start`, `--end`, `--derived-from`, `--page`, `--dry-run` |
| `manage.py audit_phrase_quotes` | idem | relit toutes les PHRASE ; lève `CommandError` en cas de défaut |
| Migrations `0010_quote_phrase` | `email_manager/`, `pdf_manager/` | 8 colonnes et 2 contraintes par table |

**Champs PHRASE**, identiques sur les deux modèles :
- `start`, `end` : `PositiveIntegerField`, nuls admis ;
- `source_text_sha256`, `anchored_text_sha256`, `certified_text_sha256` : `CharField(64)`, `db_default=""` ;
- `certified`, `corrected_on_scan` : `db_default=False` ;
- `derived_from` : FK vers `self`, `PROTECT`, `related_name="derived_phrases"`.

**Attributs propres à chaque modèle :**
- `source_field` : `"email"` ou `"pdf_document"` ;
- `reference_text`, pour un courriel : `email.body_plain_text or ""`. Il n'y a **pas** de repli sur le
  sujet, contrairement à `source_text` ;
- `reference_text`, pour un PDF : `pdf_document.transcription`, soit `ai_analysis` sans son premier
  commentaire `<!-- … -->`.

**Contraintes en base :**
- `*_quote_phrase_bornes` : `regime=HERITE`, ou bien bornes non nulles et `0 <= start < end` ;
- `*_quote_phrase_unique` : (source, `start`, `end`) est unique quand `regime=PHRASE`.

### A.2 Les trois gestionnaires [code]

| Gestionnaire | Classe | Rend | Usage prévu |
|---|---|---|---|
| `objects` | `HeriteQuoteManager`, gestionnaire **par défaut** (`Meta.default_manager_name`) | `HERITE` seulement | l'ancien système ; aussi les relations inverses (`email.quotes`, `derived_phrases`), les M2M, `prefetch_related` et les formulaires |
| `all_objects` | `models.Manager`, gestionnaire **de base** (`Meta.base_manager_name`) | tout | les FK directes, les clés génériques, les cascades et l'administration |
| `phrase_objects` | `PhraseQuoteManager` | `PHRASE` seulement | le nouveau pont |

**Les citations dérivées se lisent par `Quote.phrase_objects.filter(derived_from=ancienne)`.**
La relation inverse `ancienne.derived_phrases` passe par le gestionnaire filtré sur `HERITE` : elle est
donc **toujours vide**. Le test `T23Ancrage.test_l_ancien_systeme_ne_la_voit_pas` vérifie les deux.

### A.3 Création d'une citation PHRASE [code]

`create_phrase_quote` procède ainsi :
1. **Choix du modèle selon la source :**
   - `Email` donne une `EmailQuote`, certifiée par défaut (`certify=True`) ;
   - `PDFDocument` donne une `PDFQuote`, non certifiée par défaut (`certify=False`) ;
   - tout autre type lève `TypeError`.
2. **Page d'un PDF.** Elle vient de la dernière marque `PAGE_MARKER` qui précède `start`. À défaut, elle
   vient du `page_number` fourni. Sinon, `ValidationError`.
3. **Bornes.** Il faut des entiers, avec `0 <= start < end <= len(reference_text)`.
4. **Champs posés :**
   - `regime=PHRASE` ;
   - `quote_text = reference_text[start:end]` ;
   - `source_text_sha256`, `anchored_text_sha256`, `derived_from` ;
   - si la citation est certifiée : `certified=True` et `certified_text_sha256`.
5. **Enregistrement.** `full_clean()` puis `save()`, dans `transaction.atomic()`.

La fonction ne segmente pas le texte : les bornes sont choisies par l'humain (décision de LP, plan
§ 12.4).

`certify_phrase_quote` :
- exige une citation `PHRASE` sans `anchor_problems()` ;
- prend comme texte certifié la tranche, ou `certified_text` s'il est fourni (non vide) ;
- pose `corrected_on_scan = (texte != tranche)` ;
- appelle `full_clean()` puis `save()`.

### A.4 Les trois empreintes, la certification enregistrée et la certification effective [code]

| Empreinte | Fixée à | Atteste que |
|---|---|---|
| `source_text_sha256` | la création | le texte de référence n'a pas changé |
| `anchored_text_sha256` | la création | les bornes désignent toujours la même tranche |
| `certified_text_sha256` | la certification | le verbatim certifié n'a pas changé |

- **Certification enregistrée** : le booléen `certified` stocké en base.
- **Certification effective** : `effective_certification = certified AND valid_anchor`. Elle est
  **recalculée à chaque lecture**.
- **`valid_anchor`** vaut `regime == PHRASE AND not anchor_problems() AND not certification_problems()`.

⚠ **`valid_anchor` contrôle aussi la certification.** Prenons un PDF créé sans être certifié :
- `valid_anchor` vaut `False` ;
- pourtant, l'audit le déclare « ancrage valide, en attente de certification », parce qu'il appelle
  `anchor_problems()` séparément.

Pour tester l'ancrage seul, il faut donc vérifier `anchor_problems() == []`, et non `valid_anchor`.

⚠ **`derivation_problems()` n'entre pas dans `effective_certification`.** Ce contrôle n'intervient que
dans la garde de `save()` et dans `audit_problems()`.

### A.5 Conditions d'invalidation [code et tests]

Chacune de ces causes fait tomber la certification effective :

| Cause | Problème signalé | Test |
|---|---|---|
| texte de référence modifié, hors de la tranche | `source_text_sha256` | T2.6 |
| texte de référence modifié, dans la tranche | `source_text_sha256`, `anchored_text_sha256` et l'égalité avec la tranche | T2.6 |
| `end` hors du texte | bornes hors du texte | T2.7 |
| bornes décalées | `anchored_text_sha256` | T2.7, T2.8a |
| `quote_text` modifié | `certified_text_sha256` (plus l'égalité, pour une citation ordinaire) | T2.8b, T2.8c |
| `certified` vrai sans `certified_text_sha256` | empreinte absente | T2.9 |
| bornes nulles | « bornes absentes » | aucun |
| `regime` différent de `PHRASE` | `valid_anchor` faux | aucun |

Les tests sont dans `core/test_regime_citations_etape2.py`. Ses 22 tests passent au socle [exécuté, C.4].

### A.6 Détection, prévention et conservation : trois garanties distinctes [code]

Les trois mots ne se confondent pas :
- **détecter** : constater après coup qu'une mutation a eu lieu ;
- **prévenir** : empêcher l'écriture ;
- **conserver** : garder l'état antérieur consultable.

| | Citation **PHRASE** | Citation **HERITE** |
|---|---|---|
| **Prévention** | contraintes en base (bornes, `start < end`, unicité) ; garde de `save()` (ancrage et antécédent) ; `create_phrase_quote` et `full_clean()` ; champs PHRASE en lecture seule dans l'administration | **seule** la suppression d'une citation dont une PHRASE procède est empêchée (`PROTECT` de `derived_from`, test T2.4) |
| **Non prévenu** | `update()`, `bulk_create()`, SQL ; modification du texte source (`Email.body_plain_text`, `PDFDocument.ai_analysis`) ; suppression de la PHRASE elle-même (aucune garde ; `CASCADE` depuis la source). [non éprouvé] modification du `quote_text` d'un scan corrigé en administration | toute modification : `quote_text` reste éditable (`champs_editables`, formulaires) ; suppression d'une citation sans dérivée |
| **Détection** | `effective_certification`, recalculée à chaque lecture (A.5) ; `manage.py audit_phrase_quotes` | **aucune détection à l'exécution** : pas d'empreinte. Les outils du régime (`verifier_t22.py`, oracle P6) comparent des instantanés ponctuels ; ce sont des contrôles d'exploitation |
| **Conservation de l'état historique** | aucune : ni journal, ni historique de certification. Les empreintes gardent la trace de l'état certifié, pas son contenu : après une modification de la source, la tranche d'origine ne se reconstitue pas depuis la citation | aucune dans le code. L'état au déploiement de l'étape 2 est conservé dans la sauvegarde `avant_0010.dump`, et les 394 lignes y ont été **constatées** identiques [rapporté, plan § 12.6]. `derived_from` conserve l'identité et l'existence de l'antécédent, pas son contenu |

Les empreintes ne sont pas une signature : quiconque a un accès en écriture peut les recalculer
(plan § 4). Aucune protection supplémentaire n'est proposée ici ; elle relèverait d'un contrat approuvé
par l'Agent B.

### A.7 Restrictions des consommateurs de l'ancien système

- **Chemins de lecture [code].** Par `objects`, les relations inverses, les M2M ou les formulaires, une
  PHRASE est invisible.
- **Écritures M2M par PK brutes [code].** Les chemins de l'ancien système les contrôlent par
  `invisible_pks` (plan § 9).
- **Clés génériques (`LibraryNode`, `ProducedExhibit`).**
  - Aucune ne désigne une PHRASE [code et test T2.5].
  - Mais `content_object` se résout par le gestionnaire **de base** [rapporté, plan § 2]. Il **verrait**
    donc une PHRASE si une clé pointait vers elle.
  - L'isolation repose ici sur l'absence de telles clés, pas sur un filtre.
- **Pages propres de la citation** : elles répondent 404, 404 et 405, comme pour une PK inexistante
  (T2.2) [rapporté].

### A.8 Lectures disponibles pour un futur consommateur [code]

**Par le gestionnaire :** `Quote.phrase_objects` (filtrable comme tout QuerySet) et `Quote.all_objects`.

**Par instance :**
- `reference_text`, `quote_text`, `start` et `end` ;
- les trois empreintes, `certified`, `corrected_on_scan`, `derived_from` ;
- `effective_certification` et `valid_anchor` ;
- `anchor_problems()`, `certification_problems()`, `derivation_problems()`, `audit_problems()`.

**En lot :** `manage.py audit_phrase_quotes`.

### A.9 Limites actuelles : ce qui exigerait un développement

- **Pas de service de lecture dédié au pont.** Il n'existe ni interface du type « citations certifiées
  d'une source », ni sérialisation, ni vue. Un consommateur interroge directement les modèles.
- **T-pont n'est pas réalisé.** Aucun rendu ne refuse aujourd'hui une PHRASE dont la certification n'est
  pas effective. La garde « un élément non certifié ne se rend pas » reste à la charge du futur
  consommateur.
- **Pas d'historique.** Il n'y a ni réancrage après modification de la source, ni historique de
  certification, ni journal en ajout seul, ni signature, ni versionnement des citations.
- **Prévention partielle** (voir A.6).
- **Pas d'interface commune formelle.** Il y a deux modèles distincts, et le mixin n'est pas un
  protocole déclaré. Aucune clé générique ni table de liaison ne relie une PHRASE à d'autres objets.
- **Deux sources seulement** : le corps d'un `Email` et la transcription d'un `PDFDocument`.
- **Pas d'outil de segmentation de phrase.**
- **Contenu réel [rapporté, plan § 12.6]** : une seule citation PHRASE, `email_manager.Quote` n° 303,
  sur le courriel 100, bornes `[0, 62)`, dérivée de la n° 40, certification effective.

### A.10 Décision d'usage (LP, 20 octobre)

- **Les citations `PHRASE` se créent progressivement**, au fur et à mesure des besoins de rédaction et
  de preuve : une proposition, une utilisation probatoire ou un acte en préparation.
- **Les 394 citations `HERITE` ne seront pas converties systématiquement.**
- Chaque création conserve les garanties d'ancrage, de certification et d'antécédence (A.3 à A.6). Le
  point d'entrée existant, `create_phrase_quote`, y suffit.
- **Aucun développement supplémentaire ni traitement en masse n'est demandé.**

---

## B. Diagnostic de compatibilité de C0-A

### B.1 Le patch et le socle [git]

**Le patch** est `docs/architecture_c/lots/C0-A/C0A_DIFF_COMPLET.patch` : 42 106 octets, SHA-256
`d10781a1…27a27`. `git apply --stat` donne **8 fichiers, 495 insertions et 78 suppressions**, comme le
rapport C0-A.

**Les 8 fichiers n'ont pas changé depuis P6.** Pour chacun, l'empreinte de pré-image inscrite dans le
patch est identique au blob de `212a7fe`, au blob de `515666e` et au fichier de l'arbre principal.
L'application textuelle devrait donc passer sans conflit, mais elle **n'a pas été exécutée**.

**Les changements intervenus depuis P6 ne recoupent pas le patch.**
- `212a7fe..515666e` compte 5 commits.
- Ils modifient 14 fichiers, aucun des 8 du patch.
- `mysite/`, `manage.py`, `requirements.txt` et `requirements-dev.txt` sont inchangés.

**Les deux modules de tests ne reçoivent que des ajouts :**
- `case_manager/test_e01_cotes_concordance.py` : +109, −0 ;
- `document_manager/test_e01_numerotation.py` : +217, −0.

**Les modifications locales de l'Agent B ne recoupent pas le patch.**

### B.2 Interactions avec le régime des citations [code]

1. **Aucune voie de C0-A ne supprime ni ne modifie une citation.**
   - `supprimer_occurrence` supprime des `LibraryNode`, puis seulement des `Statement` orphelins.
   - Depuis C0-A, les candidats sont filtrés sur le ContentType `Statement`, alors qu'à P6 ils prenaient
     tous les `object_id`.
   - Aucun modèle ne déclare de `GenericRelation` : rien ne cascade d'un nœud vers une citation.
   - Le `PROTECT` de `derived_from` n'est pas sollicité.
2. **Lecture de l'arbre.** `_get_and_process_tree`, que le patch ne modifie pas, lit les citations par
   `Model.objects`, donc en `HERITE` seulement.
3. **Archives.** `archiver_noeud` n'inscrit plus `statement_pk` pour un nœud qui ne porte pas un
   `Statement`.
4. **Outils du régime.** `surfaces.py` exclut les vues qui ne répondent qu'en POST. Les routes modifiées
   par C0-A échappent donc à T2.2 et à `verifier_ab.py`, qui ne sont pas un oracle de non-régression
   pour C0-A.
5. **Deux changements de comportement**, décrits en B.3 et B.4. Ils sont soumis à la validation
   fonctionnelle de l'Agent B.

### B.3 Changement A : l'édition d'un nœud portant une citation

**Point d'entrée.** `POST /documents/ajax/produced/edit-node/<node_pk>/`, soit
`document_manager.views.produced_views.ajax_edit_node`, décorée `@transaction.atomic`. Elle reçoit
`NodeForm` : `item` obligatoire, `text` facultatif.

**À P6 et au socle actuel [code].** Avec un formulaire valide :
1. le titre (`item`) est enregistré ;
2. le contenu suit l'une de deux branches :
   - si le contenu a un attribut `text`, le texte est réécrit en place ;
   - sinon, un nouveau `Statement(text=…, is_user_created=True)` remplace la clé générique du nœud.

Une `Quote` n'a pas d'attribut `text` (elle porte `quote_text`) : elle prend donc toujours la seconde
branche. **La citation disparaît du nœud**, même pour un simple changement de titre et même avec un texte
vide. La ligne de citation elle-même reste intacte.

Exception : dans le référent historique, la garde `pre_save` E01 de `LibraryNode` refusait déjà.

**Avec C0-A [code, lignes du patch sur `ajax_edit_node`].** Pour un POST au formulaire valide :

| Ordre | Condition | Effet |
|---|---|---|
| 1 | document du nœud `REPRODUCED` (`est_reproduit`) ou référent historique (`est_referent`) | `ModificationRefusee`, **403**, quel que soit le contenu |
| 2 | contenu = `Statement` | `concordance.detacher_pour_edition(noeud, text)` |
| 3 | nœud vide (`content_type_id` et `object_id` tous deux nuls) | nouveau `Statement` |
| 4 | **tout autre cas** | `ModificationRefusee("Cette occurrence ne porte pas un Statement rédactionnel.")`, **403** |
| — | le titre n'est enregistré qu'après l'étape du contenu | un refus laisse aussi le titre intact (transaction annulée) |

Les cas inchangés : nœud inexistant (404), `GET` (rend `item` et `text`, ce dernier vide pour une
citation), formulaire invalide (400).

**Portée du refus.** Le cas 4 vise **tous les nœuds portant une citation** :
- citations de courriel ou de PDF, quel que soit leur régime (`HERITE` ou `PHRASE`) ;
- dans **tout** document ;
- pour **toute** demande valide, y compris un simple changement de titre.

Il vise aussi les nœuds portant un `Event`, une `TrameNarrative` ou un `PhotoDocument`, une clé
générique incomplète, ou une clé dont la cible n'existe plus.

**Exposition dans l'interface [code, non éprouvé dans un navigateur].**
- L'éditeur n'offre pas l'édition en place d'une citation affichée : les gabarits
  `content_types/*_quote_edit.html` n'ont pas la classe `.editable-item`.
- La route n'est donc atteinte, pour un nœud-citation, que de deux façons :
  - par un POST direct ;
  - par un nœud dont le contenu ne se résout pas dans `_get_and_process_tree` (citation absente,
    filtrée ou supprimée). Ce nœud s'affiche alors « Click to add content… » et devient éditable.
- La réponse 403 est celle de Django pour `PermissionDenied` : une page HTML, sans JSON, puisque
  `mysite/urls.py` ne déclare pas de `handler403`.
- Le client (`produced/_js.html`, `saveAndDestroyEditor`) appelle `response.json()` : l'échec ne finit
  qu'en `console.error`, sans alerte. **L'utilisateur ne verrait pas le refus.** Cela concerne le
  comportement de l'interface, pas la règle elle-même.

**Tests existants.**
- **Aucun test au socle ne passe par la route d'édition.**
- Les 5 tests HTTP d'édition de C0-A (`C0AEditionEtConservation`) couvrent :
  - le détachement d'un `Statement` partagé (200) ;
  - le refus du référent (403) ;
  - le refus d'un document REPRODUCED, y compris le simple renommage (403) ;
  - l'annulation après un refus simulé (403).
- **Aucun ne couvre le cas 4** (contenu qui n'est pas un `Statement`, notamment une citation).
- Le test `test_un_identifiant_generique_ne_declenche_pas_la_purge_dun_statement` porte un `Event`, mais
  sur la suppression. Le refus d'édition d'un nœud-citation n'est donc **pas éprouvé**.

### B.4 Changement B : les concordances « à réexaminer »

**État courant [code, inchangé par C0-A].** `Correspondance.etat_courant()` rend `A_REEXAMINER` quand
deux conditions sont réunies : l'état enregistré est `CONFIRME`, et `versions_courantes_examinees()` est
faux. Sinon, il rend l'état enregistré.
- L'état enregistré n'est jamais réécrit.
- `A_ETABLIR` reste `A_ETABLIR`.

**`versions_courantes_examinees()` à P6 [code].** La méthode vérifie seulement que chaque `VersionTexte`
captée est encore courante : son empreinte doit égaler le SHA-256 du texte actuel de son `Statement`.
Elle ne lit pas les extrémités.

**`versions_courantes_examinees()` avec C0-A [code, patch sur `document_manager/models.py`].** Pour chaque
côté (SOURCE, CIBLE), pour chaque extrémité :

| Situation de l'extrémité | Résultat |
|---|---|
| `noeud` nul (occurrence supprimée, extrémité archivée) | **faux** |
| nœud appartenant à un autre document que celui déclaré pour ce côté | **faux** |
| nœud vide (`content_type` et `object_id` nuls) | ignoré |
| contenu qui n'est pas un `Statement` : **citation**, `Event`, cible disparue… | **faux** |
| `Statement` | le couple (PK, SHA-256 de son texte actuel) est ajouté à l'ensemble actuel |

La méthode est ensuite fausse dans deux cas :
- l'ensemble actuel diffère de l'ensemble des captures (`versions_*_examinees`) ;
- aucune extrémité ne porte de texte (`contient_texte`).

**La règle pour une citation.** Une concordance `CONFIRME` dont **au moins une extrémité porte une
citation** est calculée `A_REEXAMINER` dès que C0-A est en place.
- Le contenu, le régime et la certification de la citation n'y changent rien.
- **Reconfirmer ne la rétablit pas** [non éprouvé]. `confirmer_traitement`, que C0-A ne modifie pas, ne
  capte que les `Statement` et passe les citations sous silence. L'extrémité-citation refait donc
  échouer le contrôle. La concordance reste à réexaminer tant que l'extrémité porte une citation.
- À P6, la même concordance restait `CONFIRME` : le côté citation n'était ni capté ni contrôlé.

**Règle voisine pour les appuis [code].** Avec C0-A, `ConfirmationAppui.etat_courant()` (case_manager)
rend `A_REEXAMINER` dès que le nœud ne porte pas un `Statement` (citation comprise), si l'état enregistré
est `CONFIRME` ou `SANS_APPUI`.

**Où ces règles se manifestent [code].**
- Ni vue ni URL ne crée, ne confirme ou n'affiche ces états.
- `relier()` accepte des nœuds de tout type. Il n'est appelé, comme `confirmer_traitement()`, que par
  `manage.py demonstration_e01` et par les tests.
- `ConfirmationAppui` n'est créée que par `demonstration_e01` et par les tests.
- L'état courant est lu par l'export `manage.py exporter_concordance` (`export_concordance.py`) et par
  la démonstration.

Le nombre de concordances réelles concernées n'est pas mesuré : cette mesure est reportée à la revue de
C0-A (mandat complémentaire, § 5).

**Ce que cette règle n'est pas : l'invalidation des empreintes PHRASE.**

| | Concordance « à réexaminer » (E01 / C0-A) | Certification PHRASE ineffective (fournisseur) |
|---|---|---|
| Objet | `Correspondance`, `ConfirmationAppui` (document_manager, case_manager) | `email_manager.Quote`, `pdf_manager.Quote` au régime `PHRASE` |
| Ce qui est comparé | l'identité des `Statement` et `VersionTexte.empreinte` (SHA-256 de `Statement.text`), captées à la confirmation | `source_text_sha256`, `anchored_text_sha256`, `certified_text_sha256` |
| Rôle d'une citation | son **type** seul : une extrémité qui n'est pas un `Statement` | la mutation de **sa** source, de ses bornes ou de son texte certifié |
| Lit le contenu de la citation | non | oui |
| État enregistré modifié | non, calcul à la lecture | non, calcul à la lecture |
| Retour à l'état valide | aucun par reconfirmation tant que l'extrémité porte une citation [non éprouvé] | aucun réancrage ; il faut une nouvelle citation |

Aucune des deux règles ne lit l'autre :
- une PHRASE effectivement certifiée laisserait une concordance à réexaminer, si un nœud la portait
  (aucun ne la porte) ;
- l'invalidation d'une PHRASE n'atteint aucune concordance.

### B.5 Schéma et migrations

- **[git]** Le socle porte `email_manager.0010_quote_phrase` et `pdf_manager.0010_quote_phrase`. Le patch
  ne contient aucune migration.
- **[exécuté]** Au socle seul, `makemigrations --check --dry-run` donne `No changes detected`, et
  `check` ne signale aucun problème.
- Il reste à rejouer ce contrôle **avec** le patch, lors de la revue de C0-A.

### B.6 Risques d'intégration et vérifications nécessaires

| # | Risque | Vérification |
|---|---|---|
| R1 | Les 209 tests du rapport C0-A n'incluaient pas 38 tests de la suite P6 : `case_manager.test_evidence_audit` (8), `test_piece_file_audit` (13), `test_procedural_registry` (4), `cause_manager.tests` (12), `email_manager.tests` (1). Ce chiffre est confirmé par exécution : 183 à P6 moins 145 (C.4) | exécuter avec C0-A la suite **complète**, soit 205 + 31 attendus |
| R2 | `core.test_regime_citations_etape2` (22 tests) n'existait pas à P6 | l'inclure, comme le fait la suite complète |
| R3 | `keepdb=True` réutilise une base de test d'une exécution à l'autre | supprimer `test_court_c0a` avant chaque exécution (procédure de C.2) |
| R4 | Le cas 4 de B.3 n'est couvert par aucun test | décision de l'Agent B dans la revue de C0-A |
| R5 | Les changements B.3 et B.4 n'ont pas été mesurés sur les données réelles | mesure reportée à la revue de C0-A |
| R6 | Intégration dans l'arbre principal, qui porte des fichiers de l'Agent B non suivis | n'indexer que les 8 fichiers ; vérifier que l'état Git de l'Agent B est identique avant et après |
| R7 | Retour arrière | sans changement de schéma, un `git revert` ou `git reset --keep` du commit suffit [non éprouvé] ; aucune donnée n'est migrée |

---

## C. Banc reproductible et référence exécutée du socle

### C.1 Scripts conservés

`docs/agent_a/banc_c0a/` contient trois fichiers :
- `c0a_settings.py` et `run_tests.py` : copies à l'octet près des scripts de l'Agent B, SHA-256 vérifiés ;
- `README.md` : contrôle de contenu, fonction, dépendances, paramètres et statut.

Le contrôle de contenu n'a trouvé que des valeurs synthétiques. La seule mention de la base réelle est la
contre-épreuve volontaire de `run_tests.py`, ligne 50.

**Statut :** fonctionnement **démontré sur `515666e` sans le patch**, avec les scripts non modifiés, pour
ces usages :
- le contrôle de schéma ;
- la suite applicative par étiquettes de paquets ;
- l'outillage.

Ils ne sont pas validés au-delà.

### C.2 Recréer l'environnement jetable

Ce sont les commandes effectivement exécutées le 20 octobre, de 15 h 05 à 15 h 12. Le banc de ce jour
est `/private/tmp/court-agent-a-ref-20261020-qmcM78`.

```sh
D=/Users/Louis-Philippe/Documents/GitHub/court
B=$(mktemp -d /private/tmp/court-agent-a-ref-AAAAMMJJ-XXXXXX)
mkdir -p $B/harness $B/logs $B/socket $B/tmp $B/static $B/media && chmod 700 $B/socket
cp -p $D/docs/agent_a/banc_c0a/c0a_settings.py $D/docs/agent_a/banc_c0a/run_tests.py $B/harness/

# Copie Git indépendante : objets copiés, ni worktree, ni alternates, ni remote
git init -q $B/repo
git -C $B/repo fetch -q --no-tags $D 515666eb8c6e7fdcdd265f9187c9c37b769b0fed 212a7feee81aef46a5b43d36e8eeafe0f8870064
git -C $B/repo checkout -q --detach 515666eb8c6e7fdcdd265f9187c9c37b769b0fed

# Python indépendant : interpréteur copié, paquets recopiés du .venv du projet
~/.pyenv/versions/3.11.9/bin/python3.11 -m venv --copies --without-pip $B/venv
cp -R $D/.venv/lib/python3.11/site-packages/. $B/venv/lib/python3.11/site-packages/
diff <($D/.venv/bin/python -m pip freeze) <($B/venv/bin/python -m pip freeze)   # aucune différence

# Cluster PostgreSQL 18 jetable : socket privé, sans TCP
PGB=/Library/PostgreSQL/18/bin
$PGB/initdb -D $B/pgdata -U c0a_owner -A trust -E UTF8 --locale=C
$PGB/pg_ctl -D $B/pgdata -l $B/logs/postgresql.log \
  -o "-k $B/socket -p 55439 -h '' -c max_connections=20 -c shared_buffers=32MB -c fsync=off" -w start
q() { $PGB/psql -X -v ON_ERROR_STOP=1 -h $B/socket -p 55439 -U c0a_owner "$@"; }
q -d postgres -c "CREATE ROLE c0a_runner LOGIN CREATEDB NOSUPERUSER;"
q -d template1 -c "CREATE EXTENSION vector;"
$PGB/createdb -h $B/socket -p 55439 -U c0a_owner -O c0a_runner court_c0a
q -d postgres -c "ALTER SYSTEM SET log_connections = 'on';" -c "SELECT pg_reload_conf();"

# Exécutions, dans l'ordre réel (cd $B). Numéros de C.4 entre crochets.
P="DAL Utils ai_services argument_manager case_manager cause_manager core document_manager email_manager events googlechat_manager helpers pdf_manager photos protagonist_manager video_manager"
$B/venv/bin/python $B/harness/run_tests.py ref-schema-515666e C0A_SCHEMA_CHECK          # [1]
$B/venv/bin/python $B/harness/run_tests.py ref-app-515666e .                             # [2] à ne pas reprendre
$PGB/dropdb -h $B/socket -p 55439 -U c0a_owner --if-exists test_court_c0a
$B/venv/bin/python $B/harness/run_tests.py ref-app-515666e-etiquettes $P                 # [3] référence
$B/venv/bin/python $B/harness/run_tests.py ref-outillage-515666e scripts.regime_citations.test_projection scripts.regime_citations.test_verifier_ab   # [4]

# Décompte de P6 et de l'étape 2 (212a7fe est rapatrié par le fetch ; 826c4f7 est un ancêtre de 515666e)
$PGB/dropdb -h $B/socket -p 55439 -U c0a_owner --if-exists test_court_c0a
git -C $B/repo checkout -q --detach 212a7feee81aef46a5b43d36e8eeafe0f8870064
$B/venv/bin/python $B/harness/run_tests.py p6-app-212a7fe-etiquettes $P                  # [5]
$PGB/dropdb -h $B/socket -p 55439 -U c0a_owner --if-exists test_court_c0a
git -C $B/repo checkout -q --detach 826c4f7b1f27dd9e7d9b7b7dd31e54a3bc5d2fb2
$B/venv/bin/python $B/harness/run_tests.py etape2-app-826c4f7-etiquettes $P              # [6]
$PGB/dropdb -h $B/socket -p 55439 -U c0a_owner --if-exists test_court_c0a
git -C $B/repo checkout -q --detach 515666eb8c6e7fdcdd265f9187c9c37b769b0fed

# Arrêt
$PGB/pg_ctl -D $B/pgdata -m fast -w stop
```

**Choix à connaître :**
- **`--locale=C`** : le cluster du banc C0-A a ses paramètres `lc_*` à `C`. La collation de la base réelle
  n'a pas été lue.
- **`-A trust`** : l'authentification sans mot de passe est limitée au socket local, dont le répertoire
  est en mode 700, sans écoute TCP.
- **Les étiquettes de paquets** reproduisent la découverte de `manage.py test` depuis `.`, à un paquet
  près : `mysite`, qui ne contient aucun test (voir C.4, exécution n° 2).

### C.3 Vérification effective de l'isolation

**Avant toute exécution [code].**
- `c0a_settings.py` vise le socket privé et n'importe aucun réglage réel.
- Seul `psycopg2` est installé : l'enveloppe de `run_tests.py` couvre donc toutes les connexions de
  Django.
- Le crochet d'audit refuse les fichiers `.env*`.

Ce point compte : **la copie contient un fichier `.env*` versionné.** Aucune erreur d'ouverture n'est
apparue pendant les exécutions.

**Pendant les exécutions [exécuté].**
- **Contre-épreuve.** Chaque journal porte la ligne
  `ISOLATION: external PostgreSQL probe rejected before libpq; no .env; no TCP.` : la connexion à la base
  réelle a été refusée avant `libpq`.
- **Aucune écoute réseau.** `lsof -i` sur le postmaster du banc ne rend aucune ligne.
- **Connexions reçues par le cluster privé.** `log_connections` a été activé après la création du rôle.
  Depuis, le journal du cluster compte 193 connexions, toutes `host=[local]` :

  | Rôle | Base | Connexions | Origine |
  |---|---|---:|---|
  | `c0a_owner` | `postgres` | 5 | administration par `psql`, `dropdb` |
  | `c0a_owner` | `test_court_c0a` | 1 | administration par `psql` |
  | `c0a_runner` | `court_c0a` | 1 | contrôle de schéma |
  | `c0a_runner` | `postgres` | 4 | création des bases de test |
  | `c0a_runner` | `test_court_c0a` | 182 | tests |

- **Fin d'exécution.** Le cluster est arrêté (`postmaster.pid` absent) et la copie est revenue à
  `515666e`, propre.

### C.4 Résultats

| # | Exécution | Code | Découverts | Exécutés | Résultat | Journal |
|---|---|---|---:|---:|---|---|
| 1 | contrôle de schéma, `515666e` | 0 | — | — | `No changes detected` ; `System check identified no issues (0 silenced).` | `ref-schema-515666e.log` |
| 2 | suite applicative, étiquette `.`, `515666e` | 1 | 206 | 206 | 205 OK + **1 erreur d'import**, `mysite.settings` refusé par le crochet d'audit | `ref-app-515666e.log` |
| 3 | **suite applicative, étiquettes de paquets, `515666e`, base de test neuve** | 0 | **205** | **205** | **OK** (9,963 s) | `ref-app-515666e-etiquettes.log` |
| 4 | **outillage, `515666e`** | 0 | **33** | **33** | **OK** : `test_projection` 12, `test_verifier_ab` 21 | `ref-outillage-515666e.log` |
| 5 | suite applicative, P6 `212a7fe`, base de test neuve | 0 | 183 | 183 | OK | `p6-app-212a7fe-etiquettes.log` |
| 6 | suite applicative, `826c4f7` (étape 2, premier commit), base de test neuve | 0 | 203 | 203 | OK | `etape2-app-826c4f7-etiquettes.log` |

**Sur les exécutions 2 et 3.** L'exécution n° 2 n'est pas un échec du code. La découverte depuis `.`
importe le paquet `mysite.settings`, que le lanceur interdit. Les 205 tests y passent aussi.

L'exécution n° 3 en est la forme correcte. Sa base de test a été reconstruite : 120 migrations appliquées
pendant l'exécution, `0010` comprises.

**Répartition de la référence (exécution n° 3) :**

| Module | Tests |
|---|---:|
| `document_manager.test_e01_numerotation` | 51 |
| `case_manager.test_e01_cotes_concordance` | 56 |
| `case_manager.test_evidence_audit` | 8 |
| `case_manager.test_piece_file_audit` | 13 |
| `case_manager.test_procedural_registry` | 4 |
| `cause_manager.tests` | 12 |
| `core.test_regime_citations` | 33 |
| `core.test_regime_citations_etape2` | 22 |
| `argument_manager.test_affidavit_ordre` | 5 |
| `email_manager.tests` | 1 |
| **Total** | **205** |

Les estimations du mandat se vérifient : **205 tests applicatifs et 33 d'outillage, tous réussis.**
Aucun test n'a été modifié.

**Ce qui est conservé dans `docs/agent_a/reference_515666e/` :**
- les journaux des 6 exécutions ;
- `initdb.log` ;
- `pip_freeze.txt` ;
- `connexions_cluster.log` ;
- `SHA256SUMS`.

**Le journal complet du cluster n'est pas versionné.** `postgresql.log` reproduit les instructions SQL
des tests conçus pour échouer. Elles portent un texte cité du dossier, la phrase du courriel 100, qui sert
de jeu de test dans `core/test_regime_citations_etape2.py`.

À sa place, `connexions_cluster.log` n'en garde que trois sortes de lignes :
- le démarrage, dont une seule écoute, sur le socket Unix ;
- les 193 connexions, toutes `host=[local]` ;
- l'arrêt.

C'est la preuve d'isolation. Le journal complet reste dans le banc, hors dépôt (C.6).

### C.5 L'écart du décompte P6 (« 203 »)

**Établi par exécution :** **P6 compte 183 tests** (exécution n° 5). C'est le chiffre du plan § 10.3, et
la somme des 145 tests du rapport C0-A et des 38 de R1.

**Le « 203 » est celui de l'étape 2 avant `b695e46`.** Au premier commit de l'étape 2, `826c4f7`, le
module `core.test_regime_citations_etape2` comptait 20 tests. La suite donne alors 183 + 20 = 203
(exécution n° 6). Le commit `b695e46` a ajouté 2 tests : 22, d'où 205.

**Le journal d'origine le confirme.** `~/Backups/court/regime_etape2/suite_complete_etape2.log`, du
20 octobre à 9 h 20, a été produit dans l'arbre `court-quote-regime-etape2` et porte
`Found 203 test(s)`, `Ran 203 tests`, `OK`.

**Où le chiffre est mal rattaché.** Le plan § 12.1 rattache ce « 203 » à la vérification fonctionnelle de
l'étape 1, au code `212a7fe`. Le même plan, au § 12.3 de la version `1924df2`, l'avait correctement
décrit : « 203 tests sur 203, dont … étape 2 : 20 ».

Le § 12.1 du plan est corrigé, sur autorisation de LP du 20 octobre. Il porte désormais « 183 tests sur
183 » au code `212a7fe`, avec la trace de l'erreur et sa cause.

### C.6 Obstacles à une future revue indépendante

1. **Les bancs vivent sous `/private/tmp`**, ceux de C0-A comme ceux de ce jour : ils sont exposés à
   la purge.
   - Les scripts, la procédure et les journaux de tests sont désormais dans le dépôt.
   - Le venv (1,8 Go) et le cluster sont reconstructibles par C.2, et C.8 le démontre. Ils ne sont pas
     versionnés.
   - Il reste deux bancs locaux de 2,1 Go chacun, cluster arrêté :

     | Banc | Rôle | Contenu propre |
     |---|---|---|
     | `/private/tmp/court-agent-a-ref-20261020-qmcM78` | exécutions n° 1 à 6 | journal complet du cluster |
     | `/private/tmp/court-agent-a-ref-20261020-k0tja2` | reproduction de C.8 | — |

   - Il restait 9,9 Go libres après la reproduction. Le premier banc peut être supprimé : ses journaux de
     tests et l'extrait des connexions sont versionnés.
2. **Les noms du banc sont figés dans les scripts** : `c0a_runner`, `court_c0a`, port `55439`, racine
   `<racine>/repo`. Pour tester un autre arbre, il faut un banc distinct. Deux bancs peuvent coexister,
   puisque chaque socket a son propre répertoire.
3. **Le venv dépend du `.venv` du projet** à la date de la copie. Son `pip freeze` est conservé et sert
   de référence.
4. **La collation `C` du cluster** n'est pas comparée à celle de la base réelle. Un test sensible à
   l'ordre alphabétique pourrait diverger entre le banc et une base en `fr_CA`. Aucun écart n'est apparu.
5. **Aucun test ne couvre le cas 4 de B.3**, et la règle B.4 n'est éprouvée par aucun test portant une
   citation. Leurs conséquences ne sont établies que par lecture.
6. **Coordination.** Depuis le premier rapport, l'Agent B a ajouté sous `docs/architecture_c/outils/`
   des outils de vérification de C0-A, dont `verifier_patch_c0a_sans_base.py`. Je ne les ai ni lus ni
   exécutés. Il faudra les rapprocher de ce banc avant la revue, pour éviter deux procédures
   concurrentes.
7. **Signalement de sécurité** sur un fichier de configuration versionné. Il est hors du périmètre de
   C0-A. L'évaluation a été transmise directement à LP, sans être inscrite dans ce dépôt public.

### C.7 Séquence prévue pour la revue de C0-A (non exécutée)

1. Construire un banc neuf (C.2) au SHA autorisé.
2. Rejouer la référence : 205 + 33.
3. Appliquer le patch dans la copie : `git apply --check`, puis `git apply`.
4. Rejouer `C0A_SCHEMA_CHECK`.
5. Rejouer les suites sur une base de test neuve. Attendus calculés, non mesurés :
   - **236** tests applicatifs (205 + 31) ;
   - **33** tests d'outillage ;
   - E01 : 72 et 66.
6. Contrôler `git diff --check` et la liste exhaustive des 8 fichiers.

**Ce qui doit rester identique :** les 107 tests E01 existants, les 55 tests du fournisseur (33 + 22) et
`scripts/regime_citations/`.

### C.8 Reproduction indépendante de la référence (20 octobre, après 15 h 30)

**La méthode.** Un banc neuf, `/private/tmp/court-agent-a-ref-20261020-k0tja2`, a été construit en
suivant **littéralement** les commandes de C.2 :
- avec les scripts versionnés de `docs/agent_a/banc_c0a/` ;
- sans réutiliser aucune ressource du premier banc.

Seules les exécutions n° 1, 3 et 4 ont été rejouées.

**Vérifications d'isolation :**
- la copie Git est à `515666e`, sans remote ni alternates ;
- `pip freeze` est identique à celui du `.venv` du projet ;
- le postmaster n'a aucune écoute réseau ;
- la contre-épreuve du lanceur est présente dans les trois journaux ;
- le cluster privé a reçu 51 connexions, **aucune** non locale ;
- le cluster est arrêté à la fin.

| Exécution | Code | Résultat |
|---|---|---|
| [1] contrôle de schéma | 0 | `No changes detected` ; `System check identified no issues (0 silenced).` |
| [3] suite applicative, base de test neuve | 0 | `Found 205` ; `Ran 205 tests` ; `OK` |
| [4] outillage | 0 | `Found 33` ; `Ran 33 tests` ; `OK` |

**Les listes de tests sont identiques à la référence**, identifiant par identifiant : 205 et 33.

**La référence de `515666e` est reproductible à partir du seul dépôt**, pourvu qu'on dispose du `.venv`
du projet, de PostgreSQL 18 et de `pgvector`.
