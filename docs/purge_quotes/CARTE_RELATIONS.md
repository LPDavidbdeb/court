# Carte des relations — Quotes et leurs dépendances

État de la base relevé les 2026-08-09 / 08-10 (`court_project_pg`, PostgreSQL, localhost).
Tous les chiffres ci-dessous sont mesurés, pas estimés.

> **Cadrage retenu** (précisions de LP, 2026-08-10) :
> - les documents `PRODUCED` sont des tests, **sans valeur** ; seuls les `REPRODUCED` comptent ;
> - on ne touche **pas** aux modèles de base, uniquement à leurs produits dérivés — les *quotes* en premier lieu ;
> - les `TrameNarrative` en place sont **sans valeur** (travail préliminaire, immature, largement dupliqué) ;
> - le travail d'analyse vit dans `legal/**/*.md`, pas en base.
>
> Ce cadrage supprime deux des trois difficultés identifiées au premier passage. Ce qui
> reste est détaillé au §5.

### Fichiers de ce dossier

| Fichier | Rôle | Écrit en base ? |
|---|---|---|
| `CARTE_RELATIONS.md` | ce document : la carte + la marche à suivre | — |
| `audit_quotes.py` | état complet des quotes et de leurs dépendances, avant **et** après | non |
| `export_citations_hors_corpus.py` | **le seul export qui compte** : les passages absents de `legal/**/*.md` | non |
| `citations_hors_corpus.md` | l'inventaire produit (190 passages, 93 Ko) | — |
| `export_quote_links.py` / `quote_links_export.json` | export du câblage trame↔citation — **devenu inutile** (voir §5) | non |
| `relink_quotes.py` | recâblage après recréation — **hors plan** depuis le cadrage | avec `--apply` |

---

## 1. Vue d'ensemble

```
   COUCHE 0 — SOURCES (intouchées)
   ┌──────────────────────┐   ┌──────────────────┐   ┌───────────────┐   ┌──────────────┐   ┌──────────────┐
   │ EmailThread    (157) │   │ PDFDocument (96) │   │ Document  (8) │   │ Event  (319) │   │ PhotoDoc (19)│
   │  └ Email       (629) │   │                  │   │ Statement(218)│   │              │   │ ChatSeq  (12)│
   └──────────┬───────────┘   └────────┬─────────┘   └───────┬───────┘   └──────┬───────┘   └──────┬───────┘
              │ FK CASCADE             │ FK CASCADE          │                  │                  │
   COUCHE 1 — FRAGMENTS (à purger)     │                     │                  │                  │
   ┌──────────▼───────────┐   ┌────────▼─────────┐           │                  │                  │
   │ email_manager.Quote  │   │ pdf_manager.Quote│           │                  │                  │
   │        (211)  ct=21  │   │    (103)  ct=29  │           │                  │                  │
   └──────────┬───────────┘   └────────┬─────────┘           │                  │                  │
              │ M2M 250                │ M2M 169             │ M2M 20+117       │ M2M 405          │ M2M 18+15
   COUCHE 2 — ARGUMENTAIRE (sans valeur, jetable)             │                  │                  │
   ┌──────────▼─────────────────────────▼─────────────────────▼──────────────────▼──────────────────▼───────┐
   │ argument_manager.TrameNarrative (69)   ← le collecteur de preuves (7 M2M)                              │
   └──────────────────────────────────┬─────────────────────────────────────────────────────────────────────┘
                                      │ M2M supporting_narratives
   COUCHE 3 — DOSSIER
   ┌──────────────────────────────────▼─────────────────────────────────────────────────────────────────────┐
   │ LegalCase (5) ─┬─ PerjuryContestation (13) ─┬─ AISuggestion (29)                                        │
   │                ├─ ExhibitRegistry (619)   GenericFK → PARENTS SEULEMENT (0 quote)   ← attribue les P-n  │
   │                └─ ProducedExhibit (1898)  GenericFK → parents ET quotes (438)       ← table dérivée     │
   └────────────────────────────────────────────────────────────────────────────────────────────────────────┘

   HORS COUCHE — liens génériques non contraints
   ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
   │ document_manager.LibraryNode (488)  GenericFK → 78 EmailQuote + 2 PDFQuote                              │
   │        ↳ 100 % dans doc 5 « Test » et doc 6 « Affidavit », tous deux PRODUCED → jetables                │
   │ ai_services.GeminiResponse (0)      table vide, non-sujet                                               │
   └────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> **La base bouge pendant le travail.** Entre le relevé du 08-09 et celui du 08-10 :
> `TrameNarrative` 73 → **69**, `citations_courriel` 258 → **250**, `citations_pdf` 171 → **169**.
> Cohérent avec un dédoublonnage de trames en cours. Relancer `audit_quotes.py` juste avant
> de purger plutôt que de se fier aux chiffres de ce document.

---

## 2. Tables et clés primaires

| Modèle | Table | PK | Clé naturelle | Lignes |
|---|---|---|---|---|
| `email_manager.EmailThread` | `email_manager_emailthread` | `id` serial | **`thread_id` (unique)** | 157 |
| `email_manager.Email` | `email_manager_email` | `id` serial | **`message_id` (unique)** | 629 |
| `email_manager.Quote` | `email_manager_quote` | `id` serial | **aucune** | 211 |
| `pdf_manager.PDFDocument` | `pdf_manager_pdfdocument` | `id` serial | aucune (titre non unique) | 96 |
| `pdf_manager.Quote` | `pdf_manager_quote` | `id` serial | **aucune** | 103 |
| `document_manager.Document` | `document_manager_document` | `id` serial | — | 8 |
| `document_manager.Statement` | `document_manager_statement` | `id` serial | — | 218 |
| `document_manager.LibraryNode` | `document_manager_librarynode` | `id` serial (+ `path` treebeard) | `path` | 488 |
| `events.Event` | `SupportingEvidence_supportingevidence` | `id` serial | — | 319 |
| `argument_manager.TrameNarrative` | `argument_manager_tramenarrative` | `id` serial | — | 69 |
| `case_manager.ExhibitRegistry` | `case_manager_exhibitregistry` | `id` serial | `(case, content_type, object_id)` unique | 619 |
| `case_manager.ProducedExhibit` | `case_manager_producedexhibit` | `id` serial | — (table dérivée) | 1898 |

### Séquences

```
email_manager_quote_id_seq   last_value = 217   (min id=1, max id=217, 211 lignes → 6 trous)
pdf_manager_quote_id_seq     last_value = 104   (min id=1, max id=104, 103 lignes → 1 trou)
```

Des trous existent déjà : des quotes ont été supprimées par le passé. Les PK de quotes ne
sont pas, et n'ont jamais été, des identifiants stables.

---

## 3. Les quatre porteurs de référence vers une Quote

| # | Porteur | Mécanisme | Contrainte SQL | Au `DELETE` d'une Quote | Lignes | Statut |
|---|---|---|---|---|---|---|
| 1 | `..._citations_courriel` | M2M, vraie FK | `ON DELETE NO ACTION` | **nettoyé** par l'ORM | 250 | jetable |
| 2 | `..._citations_pdf` | M2M, vraie FK | `ON DELETE NO ACTION` | **nettoyé** par l'ORM | 169 | jetable |
| 3 | `case_manager_producedexhibit` | GenericFK | aucune | orphelin muet | 438 | table dérivée, régénérée |
| 4 | `document_manager_librarynode` | GenericFK | aucune | orphelin muet | 80 | **jetable** (voir ci-dessous) |

Aucun `GenericRelation` n'est déclaré dans le projet : le collector Django ne touchera
jamais #3 ni #4. Il faut donc s'en occuper explicitement — mais, dans les deux cas, en les
supprimant, pas en les préservant.

### LibraryNode : le piège est levé

Répartition mesurée des 80 nœuds pointant vers une quote :

| Document | `source_type` | Nœuds EmailQuote | Nœuds PDFQuote |
|---|---|---|---|
| doc **5** — « Test » | PRODUCED | 35 | 2 |
| doc **6** — « Affidavit » | PRODUCED | 43 | 0 |
| **tout document REPRODUCED** | REPRODUCED | **0** | **0** |

Les quatre documents qui portent la valeur probante — doc 1 (Requête 2015), doc 2
(Dénonciation), doc 3 (Déclaration assermentée), doc 4 (courriel « plainte pour violence
conjugale ») — sont tous `REPRODUCED` et ne contiennent **aucun** nœud-quote : uniquement
des `Statement`. La purge ne les effleure pas.

Vérifié également : **les 80 nœuds sont tous des feuilles** (`get_children_count() == 0`).
Les supprimer n'emporte donc aucun sous-arbre treebeard. `LibraryNode.objects.filter(...).delete()`
est sûr.

Conséquence : la phase « mettre `object_id` à NULL puis repointer » du premier plan tombe.
On supprime, point.

### Supprimer une trame ne supprime aucune citation — vérifié

Question posée le 2026-08-10 : faut-il corriger la cascade `TrameNarrative → Quote` ?
**Non, il n'y a rien à corriger** : le comportement souhaité est déjà celui en place.
Cinq vérifications convergentes.

**1. Par construction.** `citations_courriel` et `citations_pdf` sont de simples
`ManyToManyField` ([argument_manager/models.py:54](../../argument_manager/models.py:54)).
Un M2M ne cascade jamais vers sa cible : seule la ligne de la table de liaison porte les FK.

**2. Contraintes SQL.** Sur les deux tables de liaison, les deux colonnes sont en
`ON DELETE NO ACTION` (Django émule la cascade côté ORM). Aucune FK ne part de
`TrameNarrative` vers `Quote`.

**3. Plan de suppression calculé par Django** (`Collector`) pour la trame pk=2, qui cite
12 citations de courriel dont 5 partagées avec d'autres trames :

```
argument_manager.TrameNarrative                              1 objet
[fast_delete] TrameNarrative_targeted_statements             1 ligne
[fast_delete] TrameNarrative_evenements                     38 lignes
[fast_delete] TrameNarrative_citations_courriel             12 lignes
[fast_delete] PerjuryContestation_supporting_narratives      1 ligne
→ email_manager.Quote / pdf_manager.Quote : ABSENTS du plan
```

**4. Suppression réelle, puis `ROLLBACK`.** `EmailQuote` 211 → **211**, `PDFQuote` 103 →
**103**. Les 12 citations restent présentes, y compris les 5 partagées (eq-15 aussi citée
par la trame 8, eq-8 par 11 et 66, eq-7 par 11, eq-3 par 15, eq-2 par 3). État restauré à
l'identique après annulation.

**5. Le code ne supprime jamais de citation.** Aucun récepteur `pre_delete`/`post_delete`
dans le projet, aucune surcharge de `delete()`, `TrameNarrativeDeleteView` est un
`DeleteView` nu. La seule suppression de citation est `QuoteDeleteView`, action explicite
de l'utilisateur sur une citation précise.

**Confirmation sur données réelles** : entre le relevé du 08-09 et celui du 08-10, 4 trames
ont été supprimées (73 → 69) et le nombre de citations n'a pas bougé — **211 et 103 dans les
deux relevés**. Effet observé, conforme : les citations libérées deviennent orphelines
(54 courriel + 15 pdf sans aucune trame), elles ne disparaissent pas.

**Sens inverse** également vérifié : supprimer une citation retire sa ligne de liaison et ne
touche pas la trame.

**La seule cascade réelle vers les citations** part des modèles de base :
`Quote.email` et `Quote.pdf_document` sont en `on_delete=CASCADE`. Supprimer un `Email` ou un
`PDFDocument` détruit ses citations — mais ces modèles sont hors périmètre.

### ProducedExhibit et ExhibitRegistry : inchangés

`ProducedExhibit` est explicitement une table dérivée (« *wiped and recreated on demand* »,
[case_manager/models.py:89](../../case_manager/models.py:89)), reconstruite par
`rebuild_produced_exhibits(case_id)` ([exhibit_service.py:130](../../case_manager/exhibit_service.py:130)).

`refresh_case_exhibits()` remonte systématiquement de la citation vers son parent
([exhibit_service.py:43](../../case_manager/exhibit_service.py:43)) :

```python
for email_quote in narrative.citations_courriel.all():
    if email_quote.email:
        all_evidence_objects.add(email_quote.email)     # ← l'Email, pas la Quote
```

Résultat mesuré : **0 ligne de `ExhibitRegistry` ne pointe vers une Quote**. La numérotation
P-n est structurellement immunisée.

---

## 4. Le dépôt gelé n'est pas concerné

- `legal/bordereau_pieces.md` référence ses sources par `piece_<modèle>-<pk>` avec
  `modèle ∈ {photo, pdf, email, thread, events, document, chatsequence}` — **jamais `quote`**.
- `pieces_pdf/manifest.json` et `cahier_pieces/manifest_cahier.json` : 105 pièces réparties
  en `source_type ∈ {email 38, pdf 29, event 15, chatsequence 7, photodoc 5, photo 4,
  thread 4, document 3}` — **aucun `quote`**.
- Les **68 sous-cotes `P-n.x`** du bordereau (P-5.1→P-5.6, P-43.1→P-43.19, P-107.x, P-108.x,
  P-112.x…) sont toutes des **liasses de courriels ou d'événements**, jamais des citations.
  `manifest_cahier.json` ne contient **aucune** clé `P-n.x`.
- `grep` de tout `legal/` : **zéro** référence à une PK de quote.
- `case_manager/exhibit_renderers/` : un renderer par type de source, **aucun pour quote**.

Une purge des quotes ne déplace aucune cote et n'invalide ni le bordereau, ni le cahier de
pièces, ni les PDF déjà produits.

**Corollaire sur l'ordre des sous-cotes.** Les sous-pièces `P-n-1`, `P-n-2` de
`ProducedExhibit` sont triées par `Quote.created_at`
([exhibit_service.py:366](../../case_manager/exhibit_service.py:366)), qui est un
`auto_now_add` : l'ordre de recréation fixera la numérotation. Comme aucune de ces
sous-cotes ne figure au dépôt, cela n'affecte que le rapport Word régénéré. **Non-sujet.**

---

## 5. Ce qui se perd réellement

Trois choses étaient candidates. Le cadrage en élimine deux.

### ❌ Le câblage trame↔citation — sans valeur

419 liens (250 + 169) portés par 69 trames. Le cadrage les déclare sans valeur, et la
mesure le confirme : sur les 14 groupes de citations dupliquées, **le câblage diffère d'une
jumelle à l'autre**, ce qui est la signature d'un travail repris sans mémoire du passage
précédent :

| Parent | Jumelles (date de saisie) | Trames rattachées |
|---|---|---|
| email 91 | eq-1 (2025-10-01) / eq-137 (2026-01-20) | `[11, 66]` / `[]` |
| email 90 | eq-38 (2025-10-07) / eq-136 (2026-01-20) | `[11, 66]` / `[]` |
| email 21 | eq-31 (2025-10-07) / eq-194 (2026-06-03) | `[3]` / `[50, 67]` |
| email 349 | eq-50 (2025-10-12) / eq-63 (2025-10-17) | `[26]` / `[8, 19, 34, 48, 52]` |
| email 299 | eq-101 (2025-12-03) / eq-105 (2025-12-06) | `[55]` / `[]` |
| email 61 | eq-152 (2026-01-21) / eq-186 (2026-06-03) | `[5]` / `[67]` |
| email 11 | eq-145 (2026-01-21) / eq-198 (2026-06-03) | `[]` / `[68]` |
| email 266 | eq-146 (2026-01-21) / eq-199 (2026-06-03) | `[]` / `[68]` |
| **pdf 1** | pq-3 (10-08) / pq-24 (11-20) / pq-51 (12-06) | `[]` / `[35]` / `[50, 55, 70]` |
| pdf 1 | pq-8 (10-08) / pq-53 (12-06) | `[70]` / `[55]` |
| pdf 1 | pq-22 (10-21) / pq-59 (12-09) | `[]` / `[56, 62]` |
| pdf 6 | pq-14 (2025-10-15) / pq-67 (2025-12-09) | `[]` / `[56]` |
| pdf 8 | pq-70 / pq-72 (même jour) | `[62]` / `[48, 55]` |
| pdf 13 | pq-75 (12-16) / pq-83 (2026-01-08) | `[62]` / `[62]` |

Le même passage porte un câblage différent selon la session de saisie. Il n'y a donc rien à
préserver — la purge **résout** ces doublons au lieu de les propager.

`export_quote_links.py` et `relink_quotes.py` deviennent hors plan. Ils restent dans le
dossier si le cadrage devait changer.

### ❌ Les nœuds LibraryNode — sans valeur

80 nœuds, 100 % dans `PRODUCED`, tous feuilles. Voir §3.

### ✅ Le choix du passage — **c'est la seule perte réelle**

Une citation n'est pas de la donnée dérivée : c'est une **sélection**. Confrontation
mesurée du texte des 314 citations au corpus `legal/**/*.md` (490 fichiers, 6,26 M
caractères, comparaison insensible à la casse, aux apostrophes, guillemets et espaces) :

| Corpus | Total | Déjà présent dans le .md | **Uniquement en base** | Trop court pour trancher |
|---|---|---|---|---|
| courriels | 211 | 90 | **112** | 9 |
| PDF | 103 | 25 | **78** | 0 |
| **total** | **314** | **115** | **190** | **9** |

**190 passages sélectionnés à la main n'existent que dans la base.** Ventilation par
disponibilité d'une fiche `piece_*.md` de la source :

| | absent du .md | la source A une fiche | la source N'A PAS de fiche |
|---|---|---|---|
| courriels | 112 | 41 | **71** |
| PDF | 78 | 61 | **17** |

- **41 courriels + 61 PDF** ont une fiche, mais le passage n'y a jamais été reporté — la
  section « Citations extraites » des fiches est vide (`*À constituer lors du rattachement…*`).
  Le report est mécanique.
- **71 courriels + 17 PDF** n'ont aucune fiche : la source elle-même est hors corpus `.md`.

Asymétrie importante : pour un courriel, la fiche `piece_*.md` contient le **verbatim
intégral** du corps, donc le texte reste atteignable même sans la citation. Pour un **PDF,
rien de tel** — ni le texte, ni surtout le **`page_number`**. Les 78 citations PDF sont donc
la partie la plus exposée : perdre `(page, passage)` sur un document de plusieurs dizaines
de pages, c'est perdre du travail de repérage réel.

→ **Phase 1 du plan** : `export_citations_hors_corpus.py` fige ces 190 passages en markdown.

### Les 40 citations non ré-extractibles : ce que c'est exactement

40 des 211 citations de courriels n'ont pas leur `quote_text` comme sous-chaîne exacte de
`email.body_plain_text`. Diagnostic ligne à ligne :

| Cause | Nombre | PK |
|---|---|---|
| différence de normalisation seule (apostrophes, espaces) | 2 | 195, 200 |
| corps du courriel vide en base | 1 | 173 |
| **élision éditoriale `[...]` / `(...)`** | 11 | 68, 69, 94, 97, 98, 99, 107, 109, 122, 124, 125 |
| bloc cité `>` (réponse imbriquée) | 1 | 5 |
| **recollage / ponctuation ajoutée** | 25 | 9, 21, 22, 32, 54, 86, 90, 92, 93, 127, 169, 170, 178, 180, 182, 183, 184, 185, 187, 189, 191, 192, 193, 196, 208 |

Ce ne sont pas des artefacts d'extraction, ce sont des **citations composées** :

- `eq-97` = `[...] je ne te considérais pas comme mon coloc [...]` — deux élisions autour
  d'un fragment de 5 mots ;
- `eq-21` = `…with her, thanks, lp` alors que le corps porte `…with her thanks lp` —
  ponctuation rétablie à la main ;
- `eq-32` = 145 caractères communs avec le corps, puis divergence — deux passages non
  contigus recollés ;
- `eq-9` = texte tiré d'un bloc *forwarded* absent du corps stocké ;
- `eq-5` = inclut l'en-tête de citation `> bonne fête lp!!`.

À l'échelle des deux corpus, **11/211 citations de courriel et 16/103 citations de PDF
portent une élision explicite** — 27 citations éditées au total.

Conséquence opérationnelle : une ré-extraction qui copie des spans contigus du corps
reproduira 171/211 citations de courriel à l'identique, et **ne reproduira pas ces 40**.
Elles sont dans `citations_hors_corpus.md` quand elles sont hors du .md, et leur texte
composé est à reprendre tel quel.

---

## 6. Marche à suivre (révisée)

```
Backup → export des 190 passages → suppression des 80 nœuds → delete ORM des quotes
       → recréation → backfill_embeddings → rebuild exhibits → audit
```

Cinq étapes au lieu de neuf : plus d'export de câblage, plus de mise à NULL, plus de
recâblage, plus de contrainte sur les séquences.

### Phase 0 — Sauvegarde

```bash
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -Fc -f backup_avant_purge_quotes.dump
```

### Phase 1 — Figer ce qui a de la valeur

```bash
.venv/bin/python docs/purge_quotes/audit_quotes.py > docs/purge_quotes/audit_avant.txt
.venv/bin/python docs/purge_quotes/export_citations_hors_corpus.py
```

Produit `citations_hors_corpus.md` : les 190 passages qui n'existent qu'en base, avec pour
chacun sa source (`message_id` / `thread_id` pour un courriel, `page_number` pour un PDF) et
l'indication de l'existence d'une fiche. **Commiter avant de purger.**

### Phase 2 — Supprimer les nœuds-quotes des documents PRODUCED

```bash
.venv/bin/python manage.py shell
```
```python
from django.contrib.contenttypes.models import ContentType
from document_manager.models import LibraryNode
from email_manager.models import Quote as EQ
from pdf_manager.models import Quote as PQ

cts = [ContentType.objects.get_for_model(EQ).id, ContentType.objects.get_for_model(PQ).id]
qs = LibraryNode.objects.filter(content_type_id__in=cts)
assert qs.filter(document__source_type='REPRODUCED').count() == 0, "STOP : un noeud-quote est dans un REPRODUCED"
assert all(n.get_children_count() == 0 for n in qs), "STOP : un noeud-quote a des enfants"
print(qs.delete())          # attendu : 80
```

Les deux `assert` sont le garde-fou : ils échouent si la structure a changé depuis ce
relevé. Ne pas les retirer.

### Phase 3 — Purger

Par l'ORM, pas en SQL : les FK M2M sont en `ON DELETE NO ACTION`, un `TRUNCATE` échouerait
et un `TRUNCATE … CASCADE` viderait les tables M2M sans trace.

```python
from email_manager.models import Quote as EQ
from pdf_manager.models import Quote as PQ

print(EQ.objects.all().delete())   # quote 211 + through ~250
print(PQ.objects.all().delete())   # quote 103 + through ~169
```

**Les séquences n'ont plus d'importance.** Le premier plan interdisait `RESTART IDENTITY`
parce que des `LibraryNode` de valeur auraient pu être redirigés vers une PK recyclée.
Ces nœuds étant supprimés en phase 2 et `ProducedExhibit` étant reconstruite, plus aucune
référence ne survit à la purge : remettre les séquences à zéro est désormais **sans risque**.
Le faire reste toutefois inutile — autant garder la continuité des identifiants.

### Phase 4 — Recréer, puis reconstruire

Recrée les quotes par ton procédé habituel. Puis :

```bash
.venv/bin/python manage.py backfill_embeddings
```
```python
from case_manager.models import LegalCase
from case_manager.services import refresh_case_exhibits, rebuild_produced_exhibits

for c in LegalCase.objects.all():
    refresh_case_exhibits(c.id)
    rebuild_produced_exhibits(c.id)
```

### Phase 5 — Vérifier

```bash
.venv/bin/python docs/purge_quotes/audit_quotes.py > docs/purge_quotes/audit_apres.txt
diff docs/purge_quotes/audit_avant.txt docs/purge_quotes/audit_apres.txt
```

Critères d'acceptation :

- `dangling` = **0** partout ;
- nœuds-quotes dans `LibraryNode` = **0** ;
- nœuds-quotes dans un document `REPRODUCED` = **0** (l'était déjà, doit le rester) ;
- `ExhibitRegistry` = **619 lignes, inchangé** — si ce nombre bouge, quelque chose est allé
  de travers ;
- `Document` : 8 lignes, `Statement` : 218, `Email` : 629, `PDFDocument` : 96 — **inchangés**,
  c'est la garantie qu'aucun modèle de base n'a été touché.

Ne **pas** relancer `sync_pieces`, `sync_pieces_pdf` ni `build_cahier_pieces` : ils ne lisent
aucune quote, et les relancer remettrait en jeu des cotes gelées.
