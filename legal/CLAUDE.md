# Dossier `legal/` — conventions

Deux types de fichiers, à ne pas confondre :

- **Fichier pièce** (`piece_*.md`) — rattaché à une source de la base, contient le verbatim + métadonnées. C'est la matière première.
- **Fichier thèse** (`these_*.md`, `allegation_*.md`) — un argument qui s'appuie sur le contenu des pièces, sans recopier le verbatim (il y renvoie). C'est la construction.

## Fichiers d'allégation — deux natures, NE SONT PAS des doublons

Une même allégation de la Requête peut avoir **deux** fichiers de natures différentes. Ce ne sont **pas** des doublons :

- **Fichier d'analyse** (`allegation_stmt*…`) — décomposition de l'allégation en sous-allégations, « Faits disponibles », « Lecture » / calibration. C'est le travail analytique.
- **Fichier de réponse / plaidoirie** (p. ex. `allegation_62_…`) — des **paragraphes de réponse numérotés** (62.1, 62.2, …) destinés à être versés dans la contestation, accompagnés d'une **table de correspondance Faits ↔ Documents (DB)** avec statut de collecte (✅/⚠️/❌). C'est l'outil de rédaction du plaidé et de suivi des pièces.

Exemple : pour l'art. 7 (séparation 2011), `allegation_stmt62_separation_2011.md` est l'**analyse** et `allegation_62_separation_2011.md` est la **réponse rédigée**. Les deux portent sur la même allégation mais remplissent des fonctions distinctes.

> **Numéros des noms de fichiers — non fiables comme identifiant.** Les chiffres après `allegation_`/`stmt` suivent des schémas hétérogènes (tantôt le n° de §, tantôt l'id DB du Statement, tantôt le n° du paragraphe de réponse « 62.x »). Pour savoir quel paragraphe un fichier traite, se fier à l'**en-tête** du fichier (« Doc 1, art. N » + verbatim) et au mapping § ↔ DB stmt de [piece_document-1.md](piece_document-1.md), jamais au seul numéro du nom de fichier.

## Nommage des pièces

`piece_<model>-<id>.md` — le modèle préfixe l'id pour distinguer `email #15` de `pdf #15`.
- Emails : un fichier par courriel, `piece_thread-<tid>_email-<eid>.md` (le `tid` regroupe les courriels d'un même thread : `ls piece_thread-6_*`).
- Autres : `piece_pdf-<id>.md`, `piece_photodoc-<id>.md`, `piece_photo-<id>.md`.

## Procédure à chaque référence à une pièce

1. Déterminer `piece_<model>-<id>.md`.
2. Fichier absent → le créer (référence + verbatim + contexte).
3. Fichier présent, citation absente → l'ajouter (verbatim + métadonnées + contexte).
4. Fichier présent, citation déjà là → ajouter seulement le nouveau contexte, sans dupliquer.

Ne jamais re-requêter la base pour une source déjà extraite. Le verbatim vit une seule fois dans le `piece_` ; les thèses y renvoient (lien + n° de citation Cn).

## Liste de faits (exposé des faits — art. 99 CPC)

Forme d'une entrée : **« N. ‹ancrage temporel› — ‹une seule proposition factuelle, descriptive, sans qualificatif› (source : ‹pièce(s)›). »** Types implicites (pas d'étiquette).

Règles :
1. **Un fait = une proposition.** Pas de « et » qui cache deux faits.
2. **Aucun énoncé ne dépasse sa source.** La force d'une source s'évalue **par proposition** (une pièce peut être forte pour un énoncé, muette pour un autre — éviter la **dérive de source**). Ne pas non plus **sous-utiliser** une source forte.
3. **Zéro qualificatif / conclusion** dans la liste (« dévoué », « rarement », « impliqué » : interdits ; ça va dans l'argument).
4. **Une source peut être** : un fait **documentaire**, un fait **structurel**, ou leur **combinaison déductive** — chaque brique étant elle-même ancrée.
   - **Outil documentaire + structurel → récurrence :** (période documentée) + (structure connue de l'institution : cours = hebdomadaire/session ; garderie = quotidienne ; école = quotidienne/année scolaire) → établit la **récurrence** avec un **plancher conservateur** (« au minimum un… »), **sans** collecte instance par instance. Le fait structurel doit être ancré (pièce, p. ex. calendrier d'inscription, ou connaissance d'office).
5. **Source plus faible que l'énoncé** → soit **rétrograder** l'énoncé au niveau prouvé (par défaut), soit le marquer **`[à sourcer]`** (cible non plaidable tant que la pièce n'est pas obtenue).
6. **Ordre chronologique.** Périmètre : faits **en champ** (exclure les énoncés ⚪ non falsifiables / hors champ).
7. **Allégation discrète vs structurelle/périodique.**
   - Une allégation **discrète** (un événement daté) se réfute par une **pièce précise**, concise.
   - Une allégation **structurelle/périodique** (« depuis la naissance », « tout l'été 2013 », « en 2011-2012 ») met en cause la **texture d'une période** → se réfute par le **volume distribué** : **(a)** un **paragraphe de densité** (nombre d'occurrences + bornes temporelles + répartition sur toute la période) ; **(b)** un **tableau chronologique** des instances (date + pièce) ; **(c)** **pièces exhaustives**. *Le volume est porteur — ne pas l'agréger en « vague ».*
   - La **proportionnalité (art. 18) est relative à l'ampleur de l'allégation** : une accusation large justifie une preuve large (la largeur de la réfutation doit égaler celle de l'accusation).
   - Calibrer l'énoncé de densité : il réfute la **fausse caractérisation** (« minimale / rarement disponible / parti »), il n'**overclaim pas** l'égalité (≈40-46 % concédé).
