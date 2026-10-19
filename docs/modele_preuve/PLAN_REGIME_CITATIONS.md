# Le régime des citations — plan en deux étapes

Proposition de LP du 2026-10-17. Fait suite à `CONCEPTION_PREUVE.md` § 17. **L'étape 1 a été exécutée
sur un clone le 17 octobre (§ 9) ; la base réelle n'est pas touchée.** **Version 5** du plan, révisée après quatre passes d'une revue externe le même jour
(§ 6), avec les décisions de LP arrêtées (§ 8). Verdict de la quatrième passe : « Étape 1 : feu
vert sans réserve. Étape 2 : feu vert après l'ajout de l'empreinte du `quote_text` certifié. »
Cette empreinte est intégrée (§ 4).

> **LP** : « comme première étape, je suggère de modifier le modèle sans ajouter de nouvelle
> quote, identifier celles existantes, appliquer le filtre partout pour que les résultats de
> l'app demeurent inchangés. Les view, form, template. Ce qui implique définir une série
> d'objectifs et de tests. Une fois réussie, comme deuxième étape, nous testerons en ajoutant une
> première citation dans le nouveau régime et testerons qu'elle reste indétectée par le système
> tel qu'il est. »

---

## 1. Deux invariants, à ne pas confondre

| | Énoncé | Ce qui le prouve |
|---|---|---|
| **A — non-régression** | Sans citation du nouveau régime, introduire le champ de régime ne change aucun comportement de l'ancien système. | l'empreinte canonique, avant et après (T1.8), sur un clone de la base réelle |
| **B — isolation** | En présence d'une citation du nouveau régime, aucun consommateur de l'ancien système ne peut l'observer. | à l'étape 1, une citation fictive dans la base de test (T1.2 à T1.7) ; à l'étape 2, une citation réelle (T2.2) |

**Un test qui ne peut pas échouer ne prouve rien.** Sans citation du nouveau régime, l'invariant A
est vrai que le filtre soit posé ou non. L'invariant B se prouve donc par des tests écrits
**avant** le filtre : on les voit échouer, puis réussir.

---

## 2. L'architecture du filtre

**Trois gestionnaires, sur les deux modèles de citation** :
- `objects` : **gestionnaire par défaut, filtré sur l'ancien régime**. C'est la frontière de
  comportement de l'ancien système ;
- `all_objects` : **gestionnaire de base, sans restriction**. C'est la vérité complète de la table ;
- `phrase_objects` : le nouveau régime seulement, pour le nouveau pont.

Le `Meta` déclare explicitement `default_manager_name = "objects"` et `base_manager_name = "all_objects"`.
Le gestionnaire de base de Django est déjà non filtré par défaut. Le déclarer documente
l'intention et rend `dumpdata --all` prévisible. Les noms sont à harmoniser avec le code voisin au
moment d'écrire.

**Ce que le gestionnaire par défaut couvre, et ce qu'il ne couvre pas** (vérifié dans les sources
de Django 5.2.4, installé) :

| Chemin | Gestionnaire utilisé | Filtré ? |
|---|---|---|
| `Quote.objects…` dans les vues, services, commandes | défaut | oui |
| relations inverses (`email.quotes`) et M2M (`trame.citations_courriel`), donc les gabarits et `prefetch_related` | classe du gestionnaire **par défaut** | oui |
| listes de choix des formulaires (`ModelChoiceField`, `ModelMultipleChoiceField`) | défaut | oui |
| accès direct par clé étrangère (d'un autre modèle vers une citation) | **base** | non |
| clés génériques (`LibraryNode`, `ProducedExhibit` : `content_object`) | **base** | non |
| **écriture** d'un lien M2M par `set()` / `add()` avec des PK brutes | **aucun** : la PK va droit dans la table de liaison | non — gardé par `invisible_pks` (§ 9) |
| **écriture** d'une clé générique résolue par `get_object_for_this_type` | **base** | non — résolue par le gestionnaire par défaut (§ 9) |
| `dumpdata` / `dumpdata --all` | défaut / base | oui / non |
| administration | **décision : `all_objects`**, avec une colonne et un filtre `regime` | non, voulu |

**L'administration voit tout.** L'ancien système fonctionnel ne voit que l'ancien régime ;
l'administration technique voit les deux, pour qu'un objet du nouveau régime reste diagnosticable.
Aujourd'hui, aucune administration n'est déclarée pour les citations (`email_manager/admin.py` et
`pdf_manager/admin.py` ne les enregistrent pas). L'étape 1 en crée une, sur `all_objects`. Le widget de
citations de l'administration des trames (`argument_manager/admin.py`) appartient à l'ancien
système : il reste sur le gestionnaire par défaut.

Le gestionnaire filtré **réduit fortement** le nombre d'endroits à modifier. Il **ne prouve pas** à
lui seul que tous les chemins respectent le filtre. Les tests T1.3 à T1.7 restent indispensables.

---

## 3. Étape 1 — modifier le modèle, sans nouvelle citation

**Portée** : le champ de régime, les gestionnaires et la visibilité administrative nécessaire à
leur diagnostic. Aucune modification des données ni des fonctionnalités métier de citation.

### Objectifs

| # | Objectif |
|---|---|
| O1.1 | Un champ `regime` (énumération `TextChoices`), sur `email_manager.Quote` et `pdf_manager.Quote`. Valeur par défaut : **l'ancien régime**. La migration y classe les 394 citations existantes (268 + 126). Aucune autre colonne n'est touchée. |
| O1.2 | `objects` ne rend que l'ancien régime ; `all_objects` rend tout ; `phrase_objects` ne rend que le nouveau. |
| O1.3 | Tous les chemins de création existants produisent l'ancien régime. |
| O1.4 | **Invariant A** : l'empreinte canonique de l'ancien système est identique avant et après. |
| O1.5 | **Invariant B** : une citation du nouveau régime, créée dans la base de test, n'est observable par aucun consommateur de l'ancien système. |
| O1.6 | Une administration des citations sur `all_objects`, avec une colonne et un filtre `regime`. |

### L'oracle : l'identité de la citation, jamais son texte

Une citation est un extrait de son document source. Sur la fiche d'un courriel, le texte de la
citation apparaît **parce que le corps du courriel est affiché**, que la citation soit visible ou
non. Chercher le texte est donc un oracle trompeur. À l'étape 2, il ne pourrait même pas réussir,
puisque la phrase choisie a déjà une ancienne citation équivalente.

On teste l'**identité** :
- l'ensemble des **PK de citations présentes dans le contexte de rendu** (`response.context` du
  client de test, parcouru récursivement : instances, listes, `QuerySet`). C'est l'oracle
  principal, sans analyse du HTML ;
- en second lieu, l'absence de la PK nouvelle dans les liens et les attributs HTML de citation ;
- le **nombre** de citations rendues par surface, inchangé ;
- l'absence de la PK nouvelle dans les résultats des services et les structures sérialisées.

### L'empreinte canonique (invariant A)

Ce n'est pas un hachage des pages : les jetons CSRF, l'ordre non garanti, les horodatages et les
espaces le feraient varier sans rapport avec les citations. C'est une **projection** du
comportement de l'ancien système, par surface :

```json
{ "url": "/email/100/", "status": 200, "quote_ids": [17, 24, 31], "trame_ids": [4, 9] }
```

Les projections sont normalisées (listes triées, JSON aux clés triées), puis hachées. Les services
(inscription et reconstruction des pièces, archives) sont projetés de la même façon : identifiants
et résultats métier normalisés. La liste des surfaces est fixée avant la première mesure et ne
change plus.

### Tests

| # | Test | Invariant |
|---|---|---|
| T1.1 | Sur le clone : nombre de citations par régime (394 / 0), ensemble des PK identique, `updated_at` identiques avant et après la migration | A |
| T1.2 | `objects` exclut le nouveau régime ; `all_objects` l'inclut ; `phrase_objects` ne rend que lui | B |
| T1.3 | Relations inverses et M2M (`email.quotes`, `pdf_document.quotes`, `trame.citations_courriel`, `trame.citations_pdf`), `prefetch_related` : PK nouvelle absente | B |
| T1.4 | Formulaires : PK nouvelle absente des listes de choix ; **un POST qui soumet la PK nouvelle est rejeté** (l'ancien système ne peut pas la rattacher à une trame) | B |
| T1.5 | Vues, par le client de test (superutilisateur) : PK nouvelle absente du contexte de rendu de chaque surface ; la fiche d'une citation nouvelle rend 404 | B |
| T1.6 | Services (`exhibit_service`, `archive_service`, `backfill_embeddings`, `ai_services/utils`) : PK nouvelle absente des résultats | B |
| T1.7 | Chemins de création (`argument_manager/views.py` lignes 648 et 724, formulaire de citation de courriel, vues de `pdf_manager`) → régime ancien | B |
| T1.8 | Empreinte canonique : identique avant et après la migration, sur le clone | A |
| T1.9 | La suite de tests existante (`manage.py test`) passe avant et après | A |
| T1.10 | L'administration des citations montre la citation nouvelle de la base de test, et le filtre `regime` la sépare des anciennes | O1.6 |

---

## 4. Étape 2 — une première citation dans le nouveau régime

### Les bornes, définies une fois pour toutes

- **Le texte de référence** : le texte canonique de la source. Pour un courriel, `body_plain_text`.
  Pour un PDF, `transcription` (le champ `ai_analysis` sans son en-tête). On ne réutilise **pas**
  les coordonnées repliées de `position_in_source` (`core.text_matching`), qui ne valent que pour
  ordonner.
- **`start` inclusif, `end` exclusif**, en indices Python dans ce texte.
- **`source_text_sha256`** : l'empreinte du texte de référence au moment de la création. Si la
  source change (réimportation, nouvelle transcription), la citation est détectée comme
  « à revérifier » au lieu de désigner silencieusement autre chose.
- **Invariants** :
  - `0 <= start < end <= len(source_text)` ;
  - pour un courriel et un PDF natif, `source_text[start:end] == quote_text`.
- **Ce que la base peut garantir, et ce qu'elle ne peut pas** : une contrainte de vérification
  porte `0 <= start < end` et l'obligation des bornes pour le nouveau régime. Elle ne peut pas
  lire la longueur d'un texte situé dans une autre table. La borne `end <= len(source_text)` et
  l'égalité des textes se vérifient donc dans l'application, en trois couches :
  1. **le point d'entrée applicatif normal**, `create_phrase_quote(source, start, end, …)`. Il lit
     le texte de référence, calcule `quote_text`, `source_text_sha256` et `anchored_text_sha256`,
     appelle `full_clean()`, puis sauvegarde. Django n'appelle pas `full_clean()` de lui-même lors
     d'un `save()` ou d'un `objects.create()` : sans ce point d'entrée, un script pourrait écrire
     `end = 500000` sur un courriel de 200 caractères. Ce n'est pas le seul chemin technique :
     d'où les deux couches suivantes ;
  2. **une garde dans `save()`** pour le régime `PHRASE` : elle refuse une citation qui viole les
     invariants, même créée hors du point d'entrée (`Quote.all_objects.create(…)`) ;
  3. **un audit** (commande de gestion) : `QuerySet.update()` et `bulk_create()` contournent
     `save()`. L'audit relit toutes les citations `PHRASE` et signale celles qui violent un
     invariant. Il **détecte et sert à réparer** ; il n'est pas ce qui protège (point suivant).
- **L'ancrage valide et la certification effective.** La certification est recalculée à chaque
  lecture, à partir de l'état réel de la source et des bornes :

  ```text
  valid_anchor = 0 <= start < end <= len(source_text)
                 AND sha256(source_text) == source_text_sha256
                 AND sha256(source_text[start:end]) == anchored_text_sha256
                 AND sha256(quote_text) == certified_text_sha256
                 AND (corrected_on_scan OR source_text[start:end] == quote_text)

  effective_certification = certified AND valid_anchor
  ```

  **Trois empreintes, trois objets distincts** :

  | Empreinte | Ce qu'elle garantit |
  |---|---|
  | `source_text_sha256` | le texte de référence est toujours le même |
  | `anchored_text_sha256` | les bornes désignent toujours la même tranche |
  | `certified_text_sha256` | le verbatim certifié par l'humain est toujours le même |

  Pour une citation ordinaire, les deux dernières portent sur le même texte. Pour un scan corrigé,
  elles diffèrent volontairement : `hash("savotr")` pour la tranche, `hash("savoir")` pour la
  lecture certifiée. **Toute mutation non autorisée d'une composante qui a participé à la
  certification la rend immédiatement ineffective.**

  **`certified_text_sha256` se fixe au moment de la certification**, non de la création. Pour un
  courriel, l'original est la base : `create_phrase_quote` certifie dans le même geste. Pour un
  PDF scanné, la certification est un acte distinct, fait après la lecture du scan
  (`certify_phrase_quote`) : elle pose `certified`, `corrected_on_scan` et
  `certified_text_sha256`. Tant que ce dernier est vide, la certification n'est pas effective.

  **Le périmètre de la protection.** Ces empreintes protègent contre une mutation accidentelle
  ou non autorisée (un `update()` mal ciblé, une restauration partielle, une réimportation).
  Elles ne sont pas une signature : quelqu'un qui a un accès en écriture à la base peut
  recalculer une empreinte. Une protection contre un acte délibéré demanderait un journal de
  certification en ajout seul, ou une signature à clé. La question se posera avec le gel des
  versions, pas à cette étape.

  **Conséquence** : même si quelqu'un contourne `save()` et corrompt les bornes d'une citation
  `PHRASE` par `update()`, elle cesse **immédiatement** d'être certifiée, donc utilisable. L'audit
  ne sert ensuite qu'à la trouver et à la réparer. Une source modifiée produit le même effet : la
  citation retombe « à revérifier ». Le nouveau pont, quand il existera, ne rendra que des
  éléments dont la certification est effective : c'est la garde « un élément non certifié ne se
  rend pas dans un acte » (`CONCEPTION_PREUVE.md` § 7.5).

  **`anchored_text_sha256`** (ajouté à la version 4) est l'empreinte de la tranche
  `source_text[start:end]` au moment de la création. Elle couvre la corruption des **bornes**
  d'un scan corrigé. Elle laissait un trou, relevé par la quatrième passe de la revue : un
  `update()` du **`quote_text`** d'un scan corrigé passait inaperçu, puisque `corrected_on_scan`
  dispense de l'égalité avec la tranche. `certified_text_sha256` ferme ce trou.
- **Le cas des PDF scannés.** Pour pdf-3, pdf-7 et pdf-8, le texte certifié (lu sur le scan) peut
  corriger la transcription OCR (« savotr »). L'égalité stricte ne tient plus : les bornes et
  l'empreinte désignent la transcription, `quote_text` porte la lecture certifiée. Un indicateur
  (`corrected_on_scan`) déclare l'écart. L'invariant devient alors : la phrase de la transcription
  entre `start` et `end` est celle que la lecture certifiée corrige.

### Objectifs

| # | Objectif |
|---|---|
| O2.1 | Les champs du nouveau régime : `start`, `end`, `source_text_sha256`, `anchored_text_sha256`, `certified_text_sha256`, `certified`, `corrected_on_scan`, `derived_from`. |
| O2.2 | Les contraintes en base : bornes obligatoires et `0 <= start < end` pour le nouveau régime ; **unicité conditionnelle** (source, `start`, `end`) pour le nouveau régime (PostgreSQL). |
| O2.3 | `derived_from` → l'ancienne citation, en **`on_delete=PROTECT`**. Supprimer une ancienne citation dont une nouvelle procède est refusé. L'antécédence a une valeur historique. Le décommissionnement de l'ancien pont devra traiter ces liens explicitement. |
| O2.4 | Une première citation réelle, créée **par `create_phrase_quote`** (le point d'entrée applicatif normal), à partir d'une phrase entière vérifiée sur l'original. |
| O2.6 | `effective_certification = certified AND valid_anchor`, recalculée à la lecture. Une source modifiée ou des bornes corrompues la rendent fausse immédiatement. |
| O2.5 | **Invariant B sur la base réelle** : elle reste inobservable par l'ancien système, et `phrase_objects` la rend. |

### Tests

| # | Test | Invariant / objectif |
|---|---|---|
| T2.1 | Seconde citation sur la même phrase → `IntegrityError` ; citation nouvelle sans bornes ou avec `start >= end` → `IntegrityError` ; `end > len(source_text)` → refusé par `create_phrase_quote` **et** par la garde de `save()` (`Quote.all_objects.create(regime=PHRASE, end=len+1, …)` échoue) | O2.2, O2.4 |
| T2.2 | Empreinte canonique après l'insertion : **identique** à celle de l'étape 1 | B |
| T2.3 | `phrase_objects` la rend ; `source_text[start:end] == quote_text` ; l'empreinte du texte source concorde | O2.4 |
| T2.4 | Supprimer l'ancienne citation dont elle procède → refusé (`PROTECT`) | O2.3 |
| T2.5 | Aucune clé générique de l'ancien pont ne la désigne ; elle figure dans la sauvegarde `pg_dump` | B |
| T2.6 | Dans la base de test, modifier le texte de la source → `effective_certification` devient faux, et l'audit signale la citation | O2.6 |
| T2.7 | Dans la base de test, corrompre les bornes d'une citation `PHRASE` par `update()` (`end` hors du texte, puis une tranche décalée) → `effective_certification` devient faux **immédiatement**, et l'audit la signale | O2.6, O2.2 |
| T2.8a | Citation `corrected_on_scan` : modifier les bornes par `update()` → `anchored_text_sha256` ne concorde plus → `effective_certification` faux | O2.6 |
| T2.8b | Citation `corrected_on_scan` : modifier `quote_text` par `update()` → `certified_text_sha256` ne concorde plus → `effective_certification` faux | O2.6 |
| T2.9 | Une citation `certified` dont `certified_text_sha256` est vide → `effective_certification` faux | O2.6 |
| *T-pont* | ***Reporté à la construction du nouveau pont*** : une citation dont la certification n'est pas effective est refusée par le rendu du pont | — |

**La première citation** : l'email 100, « je t'ai deja dit que les mardi et mercredi elise
dansait ». La base est l'original, donc la vérification est mécanique. Une ancienne citation
équivalente existe déjà, ce qui éprouve `derived_from`, la coexistence des deux régimes sur la même
phrase et l'oracle par identité.

---

## 5. Exécution : sur un clone d'abord

Les outils PostgreSQL 18 sont installés (`/Library/PostgreSQL/18/bin` : `pg_dump`, `pg_restore`,
`createdb`). La sauvegarde quotidienne existe (`~/Backups/court/court_project_pg.dump`, refaite
chaque nuit à 1 h).

1. **Créer un clone** de `court_project_pg` en y restaurant la sauvegarde du jour. Cela éprouve du
   même coup la restauration de la sauvegarde.
2. **Sur le clone** : empreinte « avant » → écrire les tests B et les voir échouer → migration et
   gestionnaires → tous les tests passent → empreinte « après » identique (A).
3. **Sur la base réelle**, seulement ensuite : sauvegarde → même séquence → mêmes résultats.
4. **Étape 2** : sur le clone, puis sur la base réelle, dans le même ordre.

---

## 6. La revue externe du 2026-10-17 et ce qui en est retenu

| Point de la revue | Retenu ? | Nuance |
|---|---|---|
| Déclarer le gestionnaire de base non filtré à côté du gestionnaire par défaut filtré ; ne pas prétendre que le filtre « couvre tout » | oui | vérifié dans Django 5.2.4 : relations inverses et M2M filtrées ; clés étrangères directes et clés génériques non filtrées (§ 2) |
| Tester l'identité de la citation, pas son texte | **oui — correction d'une erreur du plan v1** | oracle principal : les PK du contexte de rendu, plutôt que l'analyse du HTML |
| Une empreinte sémantique et canonique, pas un hachage des pages | oui | — |
| Attacher `start`/`end` à une version du texte source ; `0 <= start < end <= len` | oui | la base ne peut pas vérifier la longueur d'un texte d'une autre table : `clean()`, test et audit. Les PDF scannés exigent `corrected_on_scan` |
| Politique de suppression de `derived_from` : `PROTECT` | oui | la revue supposait un ménage des anciennes citations, abandonné le 17 octobre ; `PROTECT` reste juste, à cause des suppressions par l'interface et du décommissionnement |
| Une énumération plutôt qu'un booléen | oui | valeurs en français, comme les énumérations voisines (`EtatAppui`) : par exemple `HERITE` / `PHRASE` |
| Exécuter d'abord sur un clone, avec un test de restauration | oui | faisable : PostgreSQL 18 et la sauvegarde quotidienne sont en place |
| Ajouté ici | — | un POST qui soumet une PK du nouveau régime à un formulaire de l'ancien système est rejeté (T1.4) |
| **Seconde passe.** `clean()` n'est pas appelé par `save()` ni `create()` | oui | un point d'entrée applicatif normal (`create_phrase_quote`) + une garde dans `save()` + un audit, puisque `update()` et `bulk_create()` contournent `save()` |
| **Seconde passe.** L'effet d'une empreinte de source périmée | oui | `effective_certification` ; pas de rendu jusqu'à revérification |
| **Seconde passe.** La visibilité dans l'administration | oui | administration des citations créée sur `all_objects`, avec colonne et filtre `regime` ; aucune n'existait |
| **Troisième passe.** L'audit est détectif, pas préventif : `effective_certification = certified AND valid_anchor` | oui | ajouté ici : `anchored_text_sha256`, pour que la vérification couvre aussi les PDF scannés (T2.8) |
| **Troisième passe.** « seul point d'entrée » → « point d'entrée applicatif normal » | oui | — |
| **Troisième passe.** Le refus du rendu par le pont (T2.6) dépend d'une architecture qui n'existe pas encore | oui | T2.6 limité à la certification et à l'audit ; le refus du rendu passe au test du pont (*T-pont*) |
| **Troisième passe.** La portée de l'étape 1 doit inclure l'administration | oui | phrase de portée corrigée (§ 3) |
| **Quatrième passe.** `corrected_on_scan` dispense de l'égalité : un `update()` de `quote_text` passait inaperçu | **oui — trou réel dans l'ajout de la version 4** | `certified_text_sha256`, fixé à la certification ; T2.8a, T2.8b, T2.9 |
| **Quatrième passe.** « Version 3 » et « Version 4 » en tête | oui | corrigé |
| Ajouté ici | — | le périmètre de la protection : accidentelle, non délibérée (pas une signature) ; `certify_phrase_quote` distinct de la création pour les PDF scannés |

---

## 7. L'inventaire des surfaces (relevé du 2026-10-17)

**Python** (hors migrations, tests et `docs/purge_quotes/`) :
- `ai_services/utils.py`
- `argument_manager/` : `admin.py`, `models.py`, `views.py`, `templatetags/evidence_tags.py`,
  `management/commands/fusionner_trames.py`
- `case_manager/` : `archive_service.py`, `exhibit_service.py`, `models.py`, `signals.py`, `views.py`
- `core/` : `text_matching.py`, `views.py`
- `document_manager/` : `management/commands/backfill_embeddings.py`,
  `templatetags/document_extras.py`, `views/library_node_ajax.py`, `views/new_views.py`,
  `views/produced_views.py`
- `email_manager/` : `forms.py`, `forms/quote/form.py`, `models.py`, `urls.py`,
  `views/__init__.py`, `views/email.py`, `views/quote.py`, `views/thread.py`
- `pdf_manager/` : `forms.py`, `models.py`, `urls.py`, `views.py`
- `protagonist_manager/views/model_views.py`
- `legal/create_court_reference_docx.py`

**Gabarits** (une quarantaine) : `argument_manager/templates/…` (sélection de citations, banc de
preuve, trame, affidavit, argument de parjure) ; `case_manager/templates/…` (contestation) ;
`core/templates/…` (pages publiques, récits) ; `document_manager/templates/…` (types de contenu
des citations, nœuds des documents produits, récits) ; `email_manager/templates/…` (fiche du
courriel, liste et édition des citations).

---

## 8. Décisions arrêtées (LP, 2026-10-17)

- **Les valeurs de l'énumération : `HERITE` / `PHRASE`.**
- **Les identifiants en anglais**, comme les champs existants de `Quote` (`quote_text`,
  `page_number`, `created_at`). Gestionnaires : `objects` (par défaut, filtré sur `HERITE`),
  `all_objects` (base, sans restriction), `phrase_objects`. Champs de l'étape 2 : `start`, `end`,
  `source_text_sha256`, `anchored_text_sha256`, `certified_text_sha256`, `certified`, `corrected_on_scan`, `derived_from`.
  Fonctions : `create_phrase_quote`, `certify_phrase_quote`. Propriétés : `valid_anchor`, `effective_certification`.
  Le champ s'appelle `regime`, et l'énumération `QuoteRegime`.

---

## 9. Exécution de l'étape 1 sur un clone (2026-10-17) — première passe

> **Remplacée par le § 10** pour les mesures et le verdict : outil d'empreinte versionné, ordre de
> l'affidavit rendu déterministe, états A et B mesurés depuis le même arbre. Ce paragraphe reste
> comme trace de la première passe.

**Où.** Base `court_quote_regime_clone`, restaurée depuis la sauvegarde de la nuit (01 h 01) :
88 tables, contenu identique à la base réelle (empreinte md5 par table), 268 + 126 citations. La
restauration de la sauvegarde est donc éprouvée. Le code est dans un arbre de travail séparé
(`../court-quote-regime`, branche `feat/quote-regime-step1`, rien de commité) : un modèle qui
déclare `regime` devant une base non migrée fait tomber toutes les pages de citations (constaté
sur le clone), l'arbre principal et la base réelle n'ont donc pas été touchés. Un second arbre,
détaché au commit d'origine (`../court-quote-regime-avant`), a servi à mesurer le « avant ».

**Ce qui a été modifié** (6 fichiers, 4 nouveaux) :
- `core/quote_regime.py` : `QuoteRegime`, `HeriteQuoteManager`, `PhraseQuoteManager`, `invisible_pks` ;
- `email_manager/models.py`, `pdf_manager/models.py` : champ `regime`, trois gestionnaires,
  `default_manager_name` / `base_manager_name` ; migrations `0009_quote_regime` (une par application) ;
- `email_manager/admin.py`, `pdf_manager/admin.py` : administration des citations sur `all_objects`,
  colonne et filtre `regime`, `regime` en lecture seule ;
- `argument_manager/views.py`, `document_manager/views/library_node_ajax.py` : les gardes de
  T1.4 (ci-dessous) ;
- `core/test_regime_citations.py` : 31 tests (T1.2 à T1.7, T1.10).

**Constat : le gestionnaire filtré ne suffit pas à T1.4.** Cinq chemins de l'ancien système
rattachaient une citation PHRASE à partir d'une PK soumise :
- `TrameNarrativeUpdateView.form_valid` (`selected_email_quotes`, `selected_pdf_quotes`) et les deux
  vues AJAX `ajax_update_narrative_email_quotes` / `…_pdf_quotes` : `set()` de M2M avec des PK
  brutes, qui écrit dans la table de liaison sans lire les lignes ;
- `add_library_node_ajax` : `get_object_for_this_type`, qui passe par le gestionnaire de base.

Les quatre premiers vérifient désormais les PK par `invisible_pks` (refus : 400, ou formulaire
invalide, rien d'écrit) ; le cinquième résout par le gestionnaire par défaut. Pour une soumission
valide de l'ancien régime, le comportement est inchangé.

**Les tests d'isolation, vus échouer puis réussir :**

| Phase | Code | Résultat (31 tests) |
|---|---|---|
| 0 | aucun | erreur à l'import (`core.quote_regime` absent) |
| 1 | champ seul, sans gestionnaires | 52 échecs d'assertion, 9 erreurs (gestionnaires absents) |
| 2 | gestionnaires, administration, gardes | **31 réussis** |
| contre-épreuve | version finale des tests, `objects` neutralisé | 49 échecs, 0 erreur |

Dans la contre-épreuve, réussissent seulement ce qui ne dépend pas du filtre : la déclaration des
gestionnaires, T1.7 (le défaut du champ suffit) et T1.10. Sur les 33 surfaces de T1.5, 25
voient la citation PHRASE quand le filtre est retiré ; les 8 autres n'affichent aucune liste de
citations et ne font que garder la non-régression.

**Suite complète** : 145 tests avant, **176 après** (145 + 31), tous réussis.

**T1.1** (instantané avant / après la migration, sur les mêmes colonnes) : 87 tables identiques,
aucune divergente ; seule colonne nouvelle, `regime`, sur les deux tables de citations ;
268 + 126 citations en `HERITE`, 0 en `PHRASE` ; PK et `updated_at` identiques.

**T1.8 — l'empreinte canonique.** 5 588 surfaces (toutes les fiches de courriel, de fil, de
citation, de PDF, de trame, de cause, de contestation, de document, de protagoniste, d'événement,
les listes, les points AJAX, les formulaires, l'administration des trames) et les services
(registre et pièces produites des 5 causes, archive globale, sélection du rattrapage des
plongements, méthodes de preuve des 65 trames, tables de citations et de liaison). Mesure dans une
transaction annulée, réseau sortant bloqué, `PYTHONHASHSEED=0`.
- Avant, deux mesures identiques : canonique `300bdb48…`, secondaire (HTML normalisé) `96fba8d4…`.
  Le déterminisme a demandé trois normalisations, fixées avant la mesure « après » : les PK des
  redirections vers un objet créé pendant la requête (séquence qui avance malgré l'annulation),
  les jetons CSRF, l'anti-cache `?v=<time.time()>` du visionneur PDF.
- Après : **les 5 588 surfaces sont identiques**. Services : un seul écart, la clé `regime`
  (= `HERITE` partout) ajoutée à la projection des tables de citations ; sans elle, l'empreinte des
  services est identique.
- Secondaire (HTML) : 68 pages divergent.
  - 65 fiches d'administration des trames : la barre latérale liste désormais les citations, et le
    sélecteur porte les boutons d'ajout ; effet attendu de O1.6.
  - 2 exports docx (`/cases/1/export/`, `/cases/2/export/`) : identiques une fois normalisé le nom
    de l'arbre de travail, que l'export écrit dans le message d'erreur des photos absentes.
  - **1 écart réel : `/arguments/62/affidavit/`.** Même ensemble de citations, mêmes pièces, mais
    l'ordre des citations PDF d'une même page change, donc leur sous-numérotation (P-2-k). Le
    générateur trie par `(pdf_document_id, page_number)` sans départage ; l'ordre des égalités
    était celui du plan d'exécution de PostgreSQL, que le filtre a changé. L'ancien ordre ne suit
    aucune règle (ni la PK, ni l'ordre d'insertion des liens) : il n'est pas reproductible.
    **Résolu au § 10** : ordre total explicite (document, page, position dans la source, PK).

**Défauts préexistants relevés, non corrigés** (24 réponses 500, identiques avant et après) :
16 fiches de citation de courriel dont le fil n'a pas de protagoniste (`NoReverseMatch`) ; la
trame 30 et 4 vues cinématiques de documents (tri de dates de types mélangés) ; l'export docx de
la cause 5 (caractère de contrôle) ; l'aperçu police de la contestation 3.

**Reste ouvert, hors étape 1** : les administrations à `object_id` brut (nœuds de bibliothèque,
pièces produites) peuvent désigner n'importe quelle ligne, citation PHRASE comprise ; c'est
l'administration technique, voulue sans filtre. `fusionner_trames` ne déplace que les citations
visibles : un lien vers une citation PHRASE serait perdu à la fusion, mais l'ancien système ne
peut plus en créer.

**Non fait** : la base réelle ; l'étape 2 (voir § 10).

---

## 10. Clôture de l'étape 1 sur le clone (2026-10-17)

Consigne de clôture (revue externe, transmise par LP) : rendre déterministe l'ordre de
l'affidavit, rendre l'empreinte sensible aux ordres sémantiques, versionner l'instrument, et
comparer un **état A** (code historique + correctif d'ordre) à un **état B** (le même + le régime),
pour que la comparaison ne mesure que l'effet du régime.

### 10.1 L'ordre de l'affidavit — correction d'un défaut préexistant

`argument_manager/views.py`, `affidavit_generator_view` : sous chaque pièce PDF, les citations
passent par `order_by_position` (`core.text_matching`), qui trie sur `Quote.position_in_source` :

1. le document (la requête groupe par `pdf_document_id`) ;
2. la page (`page_number`) ;
3. la position dans la transcription (`PDFDocument.transcription`, repérage replié de
   `core.text_matching`, sur `position_anchor` quand il est rempli). Une citation introuvable dans
   le texte suit les citations situées de sa page, dans l'ordre de création (`created_at`) ;
4. la PK, dernier départage.

C'est l'abstraction qu'emploient déjà les pièces produites (`exhibit_service`). Il ne s'agit pas
d'un effet du régime : la requête ne triait que sur (document, page), et l'ordre des citations d'une
même page — donc leur sous-cote P-n-k — revenait au plan d'exécution de PostgreSQL. Les citations de
courriel (triées par courriel puis PK) n'avaient pas ce défaut et ne sont pas touchées.

Effet mesuré du seul correctif (code historique → état A) : **23 affidavits** changent l'ordre de
leurs citations PDF sous une même pièce (mêmes éléments), et rien d'autre — aucune autre surface,
aucun service. Ce sont les pages qui dépendaient du même ordre indéterminé.

### 10.2 L'instrument, versionné : `scripts/regime_citations/`

`projection.py` (règles, sans Django), `surfaces.py` (inventaire), `empreinte.py` (mesure),
`comparer.py` (diff champ par champ), `instantane_t11.py`, `test_projection.py`, réglages du clone,
README (procédure, table des champs, normalisations). Les sorties restent hors du dépôt (elles
portent le texte des citations ; dépôt public).

Chaque champ est **ensemble** (présence : PK instanciées, PK du contexte, registres, sélections,
tables) ou **séquence** (ordre observable : marqueurs de citation dans l'ordre du document, ordre
du contexte, JSON, texte, texte des docx, pièces produites, chronologies). Rien n'est trié par
défaut. Normalisations : les trois du § 9, inchangées (CSRF, anti-cache, PK d'un objet temporaire
— désormais remplacée seulement si l'objet n'existe plus après l'annulation).

### 10.3 Résultats (outil première version — historiques)

> Les empreintes et le verdict de ce paragraphe sont **historiques** : ils ont été obtenus avec la
> première version de l'instrument. L'oracle final et le verdict sont au § 10.4.


| Test | Résultat |
|---|---|
| T-C1 rendus répétés de l'affidavit 62 | 5 rendus identiques, en A et en B ; empreinte des sous-cotes `d4f87363…` dans les deux états |
| T-C2 même page, positions différentes | réussi ; **échoue sans le correctif** |
| T-C3 dernier départage | réussi (même position → PK ; introuvables de même création → PK) ; la variante « introuvables » **échoue sans le correctif** |
| T-C4 séquence permutée → divergence | réussi (outil) ; appliqué au HTML réel de l'affidavit 62 capturé au § 9 : l'ancienne projection ne voyait rien, la nouvelle voit la permutation |
| T-C5 ensemble permuté → stable | réussi (outil) |
| T-C6 A → B | voir ci-dessous : **un écart dans l'instrument** |
| T-C7 tests du régime | **33/33** (31 + le test d'édition de trame scindé en trois : courriel, PDF, témoin) |
| T-C8 filtre neutralisé | 22 tests sur 33 échouent (50 échecs avec les sous-tests), 0 erreur ; les 11 autres ne dépendent pas du filtre (déclaration des gestionnaires, création, administration, témoin) |
| T-C9 cinq POST forgés | 5/5 refusés, témoins HERITE acceptés |
| T-C10 suite complète | **183/183** (145 + 5 d'ordre + 33 du régime) ; outil : 12/12 |
| T-C11 erreurs 500 | 24 en M0, en A et en B : la même liste ; aucune nouvelle |
| T1.1 | 87 tables identiques ; `regime` seule colonne nouvelle ; 268 + 126 `HERITE`, 0 `PHRASE` ; PK et `updated_at` identiques |

Empreintes (canonique / secondaire) : code historique `ffd6df9c…` / `7e14ab06…` ; état A, deux
mesures identiques `186b7f86…` / `53ed0f35…` ; état B `6f12f94d…` / `a5ec9499…`. Services : A = B
(`a8f22026…`).

**A → B, ce qui diffère :**
- HTML secondaire : les **65 fiches d'administration des trames** (barre latérale et boutons
  d'ajout des citations) — voulu, O1.6 ;
- canonique : **4 fiches de protagoniste** (`/protagonists/2/`, `7/`, `10/`, `17/`), champ
  `seq_contexte` seulement : mêmes citations, autre ordre. Leur HTML, leurs marqueurs, leurs
  ensembles sont identiques. Cause : `ProtagonistDetailView` met dans le contexte
  `email_quotes = EmailQuote.objects.filter(…).order_by('-email__date_sent')`, que le gabarit
  **n'utilise jamais** (ni lui, ni `base.html` et ses inclusions). Le queryset n'est évalué que par
  l'instrument ; les citations d'un même courriel y sont à égalité de date, et l'ordre de ces
  égalités suit le plan d'exécution, que le filtre change. L'ordre n'est ni affiché ni utilisé.

**Verdict d'alors : non validée à la lettre** — le critère 4 (« toutes les surfaces métier identiques selon
la nouvelle projection ») n'est pas atteint : l'instrument classe comme séquence l'ordre d'un
queryset que le rendu n'évalue pas. Arrêt ici, conformément à la consigne.

**Proposition d'alors** (retenue par LP, § 10.4) : préciser la règle de `seq_contexte` — un queryset que le
rendu n'a pas évalué n'a pas d'ordre observable ; il compte dans `ens_contexte`, pas dans
`seq_contexte` — puis remesurer A et B avec l'instrument précisé (restauration du clone, A, B :
environ 40 minutes). Le défaut d'égalité de `email_quotes` lui-même reste hors de portée (variable
morte ; ne pas corriger sans décision).

**État des lieux d'alors** : arbre en état B, clone migré (voir § 10.4 pour l'état final).

### 10.4 L'oracle final et le verdict (2026-10-17, décision de LP)

**La décision.** Ne pas modifier `ProtagonistDetailView` : `email_quotes` est placé dans le contexte
mais n'est consommé ni par le gabarit ni par ses inclusions ; son ordre n'a aucun effet observable.
Préciser à la place une **règle générale** de l'instrument, non propre aux protagonistes :

- **séquence sémantique** — l'ordre influence le rendu, une numérotation, une cote, une structure
  sérialisée ou un résultat métier : conservé et comparé rang par rang (l'affidavit en est une : son
  ordre fait les sous-cotes) ;
- **collection non ordonnée** — seule la composition compte : canonicalisée ;
- **collection non consommée** par la surface — présente dans le contexte, mais ni la vue ni le
  gabarit ne l'a évaluée (un `QuerySet` au cache vide après le rendu) : présence et contenu
  contrôlés, ordre non.

**La trace de l'écart.** L'oracle première version évaluait lui-même `email_quotes` et a signalé
quatre divergences A → B (`/protagonists/2/`, `7/`, `10/`, `17/`), dues à l'ordre SQL non déterminé des
citations d'un même courriel (égalité sur `-email__date_sent`). L'analyse a établi que la variable
n'est jamais consommée par le rendu ; la règle a été précisée **avant** la mesure finale
(`scripts/regime_citations/empreinte.py`, `projection.py`, README, « Historique de la règle »). Aucune
normalisation n'a été ajoutée ; les trois normalisations restent celles du § 9.

**La procédure.** Outil figé (sommes de contrôle relevées avant la première mesure finale et
vérifiées avant la mesure B). État B sauvegardé (`etat_B.tgz`, 11 fichiers, sommes SHA-256), copié
dans `~/Backups/court/regime_etape1/` (privé, hors dépôt) et vérifié. Arbre remis en état A
(historique + correctif d'ordre), clone restauré depuis la sauvegarde de la nuit, non migré : 150
tests réussis ; deux mesures A. Puis état B restauré depuis l'archive, 11 fichiers vérifiés ; 183
tests réussis (dont 33 du régime et 5 d'ordre) et 12 de l'outil ; instantané T1.1 ; migration du
clone seul ; T1.1 ; mesure B. Même arbre, même outil, même base restaurée : seul le régime change
entre A et B.

**Résultats.**

| Contrôle | Résultat |
|---|---|
| Déterminisme de A | deux mesures identiques : canonique `64def7f9…`, services `a8f22026…`, secondaire `53ed0f35…` |
| T1.1 | 87 tables identiques ; `regime` seule colonne nouvelle ; 268 + 126 `HERITE`, 0 `PHRASE` ; PK et `updated_at` identiques |
| **Surfaces A → B** (5 588) | **identiques** — canonique `c06158a5…` des deux côtés |
| **Services A → B** | **identiques** — `a8f22026…` |
| Canonique A → B | **identique** — `64def7f9…` |
| HTML secondaire A → B | 65 pages diffèrent, toutes `/admin/argument_manager/tramenarrative/<pk>/change/` : O1.6 (la barre latérale liste les citations, le sélecteur porte les boutons d'ajout) |
| Affidavits | ordre identique A → B (projection identique) ; T-C1 : 5 rendus identiques en A et en B, empreinte des sous-cotes `d4f87363…` dans les deux états |
| Erreurs 500 | 24 en A, 24 en B, même liste ; aucune nouvelle |
| Tests | 183/183 (B), 150/150 (A), outil 12/12 ; T-C8 et T-C9 inchangés (code B identique octet pour octet à celui du § 10.3) |

**Différences admises restantes** : l'administration (O1.6) ; hors projection, déclarés au README —
la colonne `regime` (contrôlée par T1.1), les métadonnées des docx, le HTML des pages 5xx.

**Empreintes.** Oracle final : A = B = `64def7f9f78e…` (canonique). Les empreintes antérieures
(`300bdb48…` au § 9 ; `ffd6df9c…`, `186b7f86…`, `6f12f94d…` au § 10.3) restent **historiques** et ne
constituent plus l'oracle final.

**Verdict : étape 1 validée sur le clone.**

**État des lieux.** L'état B est conservé dans trois commits locaux de `feat/quote-regime-step1`,
non poussés, l'arbre restant identique octet pour octet à l'état validé : `5fa62ed` (ordre des
affidavits, M0 → A), `b45808c` (régime, A → B), `11214d1` (instrument). Intégration décidée par LP :
une branche d'intégration (epic + merge explicite de feat), éprouvée sur un clone restauré ;
`epic/E01` n'avance qu'à la bascule, par avance rapide, dans la même opération que la migration de
la base réelle — le serveur de l'arbre principal tourne contre la base réelle, et un code qui déclare
`regime` devant une base non migrée fait tomber les pages de citations. Base réelle non touchée ;
étape 2 non lancée.


---

## 11. Préparation de la bascule sur la base réelle (2026-10-18)

Plan exécutable : `docs/modele_preuve/BASCULE_REGIME_ETAPE1.md` (version 2, après revue indépendante),
outillé par `scripts/regime_citations/bascule.sh` et éprouvé par `essai_bascule.sh` sur des bases
jetables : 52 contrôles réussis, 0 raté, depuis un environnement vide (chemin nominal, migration
partielle, verrou, connexion résiduelle, R1, R2, R3 interrompu et repris, avance rapide interrompue,
incident après réouverture).

**La référence validée reste `4b53e83`.** La pointe de `integration/quote-regime-step1` ne lui ajoute
que des fichiers de `docs/` et de `scripts/regime_citations/` ; le pilote refuse toute cible qui
modifierait autre chose. L'avance rapide de `epic/E01` vers cette pointe reste possible tant que
`epic/E01` est à `14f7533`.

**Prochaine étape soumise à autorisation** : la répétition générale P6, sur une copie fraîche de la
base réelle (§ 12 du plan de bascule). Base réelle, arbre principal et serveur non touchés ; étape 2 non
lancée.

**2026-10-19 — P6 rendue bloquante.**
- Elle se lance en une commande, `scripts/regime_citations/p6.sh lancer` : huit étapes, arrêt à la
  première défaillance, verdict `P6 RÉUSSIE` ou `P6 ÉCHEC — étape …`.
- La comparaison A/B passe par un oracle à code de sortie, `verifier_ab.py`, avec une liste explicite
  des différences admises.
- Chaque exécution ne touche qu'à ses propres ressources temporaires ; P6 n'utilise plus
  `court_quote_regime_clone`.

Détail et essais : § 12 du plan de bascule.
