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
| `export_citations_hors_corpus.py` | les passages absents de `legal/**/*.md` | non |
| `citations_hors_corpus.md` | l'inventaire produit (190 passages, 93 Ko) | — |
| `analyse_chevauchements.py` | **blocs simples vs compositions**, et usage réel dans le `.md` | non |
| `analyse_chevauchements.md` | le rapport produit — à lire avant de décider quoi reconstruire | — |
| `socle_citations.py` / `.md` | les citations reprises **mot pour mot** dans le `.md` (115) | non |
| `socle_similarite.py` / `.md` | les citations reprises **par similarité** (214) — mesure de référence | non |
| `idees_sans_citation.py` / `.md` | **idées non étayées** du `.md` auxquelles une citation existante répond | non |
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

**Nuance mesurée après coup** : ces citations recomposées à la main n'ont, pour l'essentiel,
jamais servi. Sur les 27 que l'analyse d'intervalles ne parvient pas à localiser,
**25 (93 %) ne sont reprises dans aucun fichier `.md`** (voir `analyse_chevauchements.md`
§1bis). Le travail éditorial qu'elles représentent est réel, mais il n'a pas irrigué
l'analyse. À pondérer en conséquence.

### Blocs simples et compositions : le vice de méthode

Les citations se chevauchent. Le même passage existe comme bloc atomique **et** comme
prémisse à l'intérieur d'une composition — ce qui le fait compter deux fois et retire à
l'exercice sa rigueur. Mesuré en localisant chaque citation par ses **offsets** dans la
source (une citation élidée `A [...] B` donne deux segments), puis en traitant le
recouvrement comme un problème d'intervalles :

| Classe | Courriels | PDF |
|---|---|---|
| COMPOSITION (contient au moins un autre bloc) | 15 | **24** |
| bloc simple, repris dans une composition | 16 | **25** |
| chevauchement partiel | 2 | — |
| doublon exact | 14 | 4 |
| bloc simple isolé | 134 | 50 |
| non localisable (recomposé à la main) | 31 | — |

Épicentre : **pdf-1**, le courriel du « plan » de Me Ayoub (P-2), 39 citations. `pq-2`
(« si j'étais ton avocate le plan serait le suivant : », 49 car.) est reprise à l'intérieur
de **six** compositions — pq-17, 22, 25, 26, 55, 59 — dont pq-25 (793 car.) et pq-26
(890 car.), qui avalent quasiment tout le document.

**Le corpus `.md` a déjà tranché.** Les blocs atomiques qu'une composition a avalés sont les
plus repris dans l'analyse ; les compositions, beaucoup moins. Autrement dit : **la couche
`.md` travaille déjà par blocs simples, c'est la base qui est restée en arrière.** La purge
est le moment de faire converger les deux.

> ⚠️ **Correction du 2026-08-10.** Un premier comptage par égalité stricte de chaîne
> concluait que 75 % des compositions et 90 % des blocs isolés n'étaient « jamais cités ».
> **Ce chiffre était un artefact de mesure** : la comparaison exacte échouait sur la
> ponctuation (`l'éducation, la santé` en base vs `l'éducation la santé` dans le `.md`) et
> sur les élisions introduites par l'analyse elle-même. Repris par similarité de
> 4-grammes (`socle_similarite.py`), **214 citations sur 305 mesurables — 70 % — sont
> démontrablement reprises** dans le corpus. Voir §5bis.

Règle à retenir pour la reconstruction : **une citation = un segment contigu,
non décomposable**. La composition appartient à la couche `.md`, qui juxtapose des
références de blocs — jamais à la base, qui dupliquerait la prémisse.

### 5bis. Ce que l'usage mesure — et ce qu'il ne mesure pas

Appariement par similarité de 4-grammes de mots, sur les 305 citations d'au moins 6 mots
(`socle_similarite.py`) :

| Palier | Taux de reprise | Citations |
|---|---|---|
| reprise quasi intégrale | ≥ 0,85 | **186** |
| largement reprise | ≥ 0,60 | 28 |
| noyau repris, reste absent | ≥ 0,35 | 15 |
| écho faible | ≥ 0,15 | 17 |
| aucune trace | < 0,15 | 59 |

**Socle élargi : 214 citations** (contre 115 par égalité stricte). Les 99 citations
récupérées ne « manquaient » que pour des raisons de rendu typographique.

⚠️ **Ce que ce classement ne dit pas.** Une citation sans trace dans le `.md` n'est pas une
citation *inutile*. L'usage constaté est un indice **positif** — il établit qu'un passage a
servi ; il n'établit rien sur les autres. On ne peut pas exclure qu'un argument gagnerait à
être davantage étayé par des passages encore inexploités : conclure de l'absence d'usage à
l'absence de valeur, ce serait tirer une absence d'une absence.

Les 76 citations sous 0,35 sont donc à lire comme un **gisement non exploité**, pas comme un
rebut. Indice qui va dans ce sens : **51 d'entre elles sont rattachées à au moins une trame**
— quelqu'un les a jugées pertinentes au moment de les saisir. Elles se concentrent d'ailleurs
sur des sources marginales dans l'analyse actuelle (pdf-54 à pdf-68, relevés d'assurance et
pièces périphériques), ce qui décrit un angle peu creusé plutôt qu'un déchet.

Conséquence sur la reconstruction : le socle élargi donne l'**ordre de priorité**, pas un
critère d'exclusion. Rien ne justifie de jeter les 76 — seulement de les traiter en second.

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
.venv/bin/python docs/purge_quotes/analyse_chevauchements.py
```

- `citations_hors_corpus.md` : les 190 passages qui n'existent qu'en base, avec pour chacun
  sa source (`message_id` / `thread_id` pour un courriel, `page_number` pour un PDF) et
  l'indication de l'existence d'une fiche.
- `analyse_chevauchements.md` : blocs simples vs compositions, et usage réel dans le `.md`.
  **C'est ce rapport qui dit quoi reconstruire** — sans lui, la reconstruction réimporte le
  vice de méthode.

**Commiter les deux avant de purger.**

### Phase 1bis — Arrêter la cible

Avant de supprimer quoi que ce soit, fixer la liste des blocs à reconstruire. Point de
départ suggéré, tiré des mesures :

1. **Socle élargi** : les **214** citations dont le corpus `.md` reprend le texte à un taux
   ≥ 0,60 (`socle_similarite.md` §1 et §3). Ce sont celles dont l'usage est établi.
2. **Décomposer** les compositions qui figurent dans ce socle en leurs prémisses atomiques —
   l'analyse `.md` les cite déjà séparément dans la plupart des cas.
3. **Fusionner** les doublons exacts : un bloc par passage distinct.
4. **Trancher à l'œil** les 15 citations au palier « noyau repris » (0,35–0,60) : soit
   l'analyse n'a gardé qu'une partie du passage, et **c'est cette partie le bloc atomique**,
   soit la correspondance est fortuite. Le rapport met en regard le texte en base et
   l'extrait du `.md`.
5. **Reporter en second rang** — et non écarter — les 76 citations sous 0,35. Leur absence
   du `.md` ne prouve pas leur inutilité (§5bis) ; 51 d'entre elles portent déjà une trame.

Cette liste est une décision d'analyse, pas une opération technique : elle se prend avant la
phase 2, et elle conditionne tout ce qui suit.

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

Recrée les quotes par ton procédé habituel.

**4.1 — Vider les colonnes `embedding` (obligatoire).**

Le modèle d'embedding a été changé le 2026-08-11 à
[ai_services/services.py:311](../../ai_services/services.py:311) :
`all-mpnet-base-v2` (anglophone) → `paraphrase-multilingual-mpnet-base-v2`.

Les deux produisent des vecteurs de **768 dimensions**. `VectorField(dimensions=768)` les
accepte donc indifféremment, **sans lever d'erreur**. Une base contenant les deux
renverrait des distances cosinus dénuées de sens, silencieusement. D'où l'invariant :

> `embedding` contient soit `NULL`, soit un vecteur du modèle courant. Jamais un mélange.

`NULL` est un état sûr — explicite, et `backfill_embeddings` le repère et le remplit. On vide
donc **tout**, en une transaction, avant de remplir quoi que ce soit :

```python
from django.db import transaction
from document_manager.models import Statement, Document
from email_manager.models import Email, Quote as EmailQuote
from pdf_manager.models import PDFDocument, Quote as PDFQuote
from events.models import Event
from photos.models import PhotoDocument

with transaction.atomic():
    for m in (Email, Event, PDFDocument, PhotoDocument, Document,
              EmailQuote, PDFQuote, Statement):
        print(m._meta.label, m.objects.exclude(embedding=None).update(embedding=None))
```

Ces deux appels — `queryset.update()` ici, `bulk_update(rows, ["embedding"])` dans
[backfill_embeddings.py:142](../../document_manager/management/commands/backfill_embeddings.py:142)
— **contournent `save()`**. Aucun champ `auto_now` n'est touché : les `updated_at` de
`Quote`, `Statement` et `Document` restent intacts. Aucun index n'existe sur ces colonnes,
donc pas de reconstruction ni de verrou long. **Seule la colonne `embedding` est écrite.**

**4.2 — Remplir.**

```bash
.venv/bin/python manage.py backfill_embeddings
```

`--only-missing` est vrai par défaut : la commande est reprenable si elle s'interrompt —
précisément parce que 4.1 a tout remis à `NULL`.

Comptes attendus après remplissage (lignes qui ont un texte source ; les autres restent
`NULL` légitimement) :

| Modèle | Attendu | | Modèle | Attendu |
|---|---|---|---|---|
| `Email` | 628 | | `Document` | 8 |
| `Event` | 318 | | `Statement` | 217 |
| `PDFDocument` | 31 | | `Quote` (courriel) | = nb recréées |
| `PhotoDocument` | 13 | | `Quote` (PDF) | = nb recréées |

**4.3 — Test qui attrape une bascule ratée.**

```python
from ai_services.services import generate_embedding
import numpy as np
a = np.array(generate_embedding("la mere a demande la garde exclusive des enfants"))
b = np.array(generate_embedding("le chat dort sur le canape"))
print(float(a @ b))     # attendu ≈ 0,08
```

Si ce nombre ressort vers **0,40**, c'est l'ancien modèle qui a tourné : la configuration
n'a pas été prise en compte. C'est le seul contrôle qui distingue une bascule réussie d'une
bascule qui en a l'air.

**4.4 — Reconstruire les tables dérivées.**

```python
from case_manager.models import LegalCase
from case_manager.services import refresh_case_exhibits, rebuild_produced_exhibits

for c in LegalCase.objects.all():
    refresh_case_exhibits(c.id)
    rebuild_produced_exhibits(c.id)
```

> **Enjeu réel de la bascule : faible.** Le seul consommateur des embeddings est
> `global_semantic_search` ([core/services.py:15](../../core/services.py:15)), appelé par
> une route `/semantic-search/` vers laquelle **aucune template ne pointe** — page
> orpheline, atteignable seulement en tapant l'URL. Rien d'autre dans le projet ne lit une
> colonne `embedding` : ni les pièces, ni le bordereau, ni le cahier, ni les cotes. Le pire
> scénario d'un échec est donc nul en pratique. La bascule se fait ici parce que le
> `backfill` a lieu de toute façon, pas parce qu'elle presse.

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
