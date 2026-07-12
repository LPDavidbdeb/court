# Dossier `expose/` — assemblage de l'exposé des faits déposable

Objectif : assembler les **sections d'exposé** (une par § ou groupe de § contesté, tirées de `faits/` + `pont/` + `analyse/`) en un **exposé des faits unique, numéroté et coté**, conforme au C.p.c. (art. 99 : clair/précis/succinct ; art. 145 et 247 : pièces indiquées et communiquées).

## Structure

| Élément | Rôle |
|---|---|
| `sections/NN_<label>.md` | chaque section soumise, rangée **verbatim** (références de source conservées) |
| `_sources_verifiees/` | **documents originaux vérifiés** (copiés de la base) ; + fichiers constitutifs des faits agrégés ; + index de liasses générés |
| `registre_pieces.md` | **registre maître** : `(model, PK)` ↔ cote P- + métadonnées de vérification + bordereau. *Source unique de vérité.* |
| `expose_faits.md` | exposé **assemblé et rendu** (numérotation continue + cotes). **Généré** — ne pas éditer à la main. |

## Processus en deux phases

**Phase A — Collecte & vérification (boucle PAR SOURCE, à chaque section reçue) :**
- **A1** — Repérer la référence dans `faits_*`/`pont` (mode **RETRACE** : apparier par date + contenu).
- **A2** — Confirmer `(model, PK)` en base ; résoudre le **chemin du fichier original** (ou marquer « agrégé — sans natif »).
- **A3** — **Empreinte (hash)** du fichier → tester le doublon au registre (même hash = même pièce → lier, **ne pas recoter**).
- **A4** — Copier l'original dans `_sources_verifiees/` **si nouveau et natif**.
- **A5** — **Recevabilité** : statut (libre / privilège de règlement / secret pro / avocat-client) — *verrou avant cotation*.
- **A6** — **Mode de preuve** : comment la pièce sera prouvée (aveu / affidavit / témoin / connaissance d'office).
- **A7** — **Index inverse** : relier la source à tous les faits/axes qui l'utilisent.
- → inscrire la ligne au registre, **sans cote** (provisoire).

**Phase B — Consolidation & rendu (GLOBAL, sur signal de gel) :**
- **B1** — **Autonome vs liasse** (par nature homogène) ; définir les sous-cotes.
- **B2** — **Stabiliser l'ordre narratif** de l'exposé (colonne vertébrale éditoriale).
- **B3** — **Attribuer les cotes P-** dans l'ordre de première invocation (voir règle de gel).
- **B4** — Générer les **fichiers de dépôt** (noms définitifs `P-12_...`) : natifs copiés + liasses/tableaux compilés.
- **B5** — Générer **bordereau + index de liasses + renvois aux paragraphes** (après numérotation).

## Règles fixées

- **Cotation** : Méthode A — sous-cotes. Source isolée → `P-N` ; séquence répétitive de même nature → liasse `P-N` avec `P-N.1, P-N.2…`. Pagination (Méthode B) reportée à la compilation physique.
- **Cote canonique** : une source = **une seule cote**, partout (2015 / 2019 / 2023) — dédup par **hash** + `(model, PK)`.
- **Règle de gel des cotes** : les cotes restent **provisoires** jusqu'à un **signal de gel** (par volet ou pour tout le dossier). Après gel, toute source nouvelle **s'ajoute en fin** (`P-N+1`) — pas de renumérotation. Avant gel, l'ordre peut bouger.
- **Numérotation des paragraphes** : **continue sur tout le dossier**.
- **Un paragraphe = une proposition factuelle homogène** (médical / garderie / routines / activités…) ; pas de méga-paragraphe.
- **Liasse** : même nature + même proposition + séquence répétitive + chronologique. Sinon **cotes distinctes** (courriels-pro ≠ photos ≠ Events ≠ échanges des parties ≠ biographie ≠ PDF formels).
- **Nature de la source** : *natif* (`PDFDocument`/`Email`/`PhotoDocument` → original copié) **vs** *agrégé/structurel* (comptes d'`Event`, densité → la pièce est un **tableau + liasse générés** ; fichiers constitutifs dans `_sources_verifiees/`).
- **Reconstitution du nombre** : total au paragraphe → 2-3 exemples avec sous-références → **index complet en tête de liasse**. *L'index localise ; il n'est pas la preuve.*
- **Recevabilité** : une source privilégiée n'est **pas** cotée en silence ; son statut est tranché **avant B3**, car il change la trame et la séquence des cotes.

## Convention de référence — mode RETRACE

Les sections soumises **ne portent pas** de tags de source. Chaque proposition est retracée à sa source `(model, PK)` via `faits/`/`pont/` (appariement date + contenu). Une proposition **sans source retrouvable** (fait nouveau) est marquée **`❌ à sourcer`**, jamais cotée d'office.

## Séquencement opérationnel (décidé)

- **Maintenant** : rédaction depuis les `piece_*.md` uniquement (verbatim + métadonnées + chemins qu'ils portent). On mène la Phase A **intellectuelle** (retrace, registre, cotes provisoires) **sans toucher aux originaux**.
- **Reporté à la Phase B (compilation du dépôt)** : la **collecte physique** — résoudre les chemins, calculer les hash, copier dans `_sources_verifiees/`. Le **mécanisme d'accès** (requête base + `media/` par l'assistant, ou fichiers fournis par le client) sera **décidé au moment de compiler**.
- Conséquence : les colonnes `Hash` et `Fichier vérifié` du registre restent **vides jusqu'à la Phase B** ; la dédup provisoire s'appuie d'ici là sur `(model, PK)`.
