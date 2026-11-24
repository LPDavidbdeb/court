# Consigne de conversion n° 2 — l'annexe du paragraphe 7 (le rôle de père) et le rendu des annexes

*Rédigée le 23 novembre 2026. Destinataire : un agent qui n'a pas participé aux travaux précédents. Travail mécanique : changer la forme, jamais le fond. Deux volets : (A) convertir l'annexe ; (B) permettre à l'assembleur de la rendre dans le document Word.*

## Contexte à lire d'abord

Branche : `fiches/email-16-portee-retrait` du dépôt `LPDavidbdeb/court`. Lisez, dans cet ordre :

1. `AGENTS.md` (racine) et `legal/CLAUDE.md` ;
2. `legal/amendements/01_avant_notification/blocs/METHODE.md` (§§ 4 à 6 et 10) et `blocs/conventions.md` ;
3. le bloc qui traite la première phrase du même paragraphe : `blocs/par07_duree_2011.md` ;
4. la source à convertir : `analyses_experimentales/annexe_par7_role_de_pere.md` (version 2 du 19 novembre 2026) ;
5. les outils : `outils/assembler.py`, `outils/rendre_docx.js`, `outils/verif_citations.py`.

**Ce qu'est une annexe.** Une pièce de démonstration jointe à la demande, à laquelle un paragraphe de la demande renvoie (« tel qu'il appert de l'annexe 1 »). Elle n'a pas de paragraphes numérotés : des sections, des listes et des tableaux. Elle a sa propre numérotation (annexe 1, annexe 2…), distincte de celle des paragraphes.

## Volet A — Convertir l'annexe

Créez `blocs/annexes/ann07_role_de_pere.md`. La source reste intacte.

1. **Le fond ne change pas.** Le texte de chaque section, de chaque ligne de tableau et de chaque citation est repris mot pour mot. Si vous remarquez une erreur ou une contradiction, ne la corrigez pas : signalez-la dans votre compte rendu.
2. **En-tête YAML :**
   ```yaml
   ---
   annexe: ann07_role_de_pere
   titre: "Le rôle de père, de la naissance d'Alexia à la fin de la thérapie de couple"
   requete: [7]
   rattachee_a: "par07_role_de_pere (bloc à rédiger)"
   statut: à valider
   registre: [P142, P166, P201, P213, P214, P215, P237, P238, P239]
   source: "analyses_experimentales/annexe_par7_role_de_pere.md (version 2, 19 novembre 2026)"
   ---
   ```
3. **Titre et introduction.** `# ` suivi du titre. Sous le titre, un seul paragraphe d'introduction : le contenu de la ligne « **Objet.** » de la source, sans le mot « Objet ». Les lignes « Proposition, version 2 », « Ce qui change par rapport à la version 1 », « Version 1 », « Sources » et « Conventions » passent dans les notes (règle 7).
4. **Sections.** Les sections 1 à 7 de la source deviennent des titres `## ` (sans leur numéro : « ## Le fait soutenu »), les sous-sections `### `. Ajoutez à la fin de chaque titre `##` une étiquette `{#ann07-mot-cle}` unique. Les listes à puces restent des listes `- ` ; les tableaux restent des tableaux Markdown, colonnes inchangées.
5. **Désignation des pièces.** Écrivez chaque fiche avec le chemin `legal/…` entre accents graves (`piece_pdf-58.md` devient `` `legal/piece_pdf-58.md` ``). Deux fiches existent depuis le 23 novembre pour des courriels que la source cite par l'extraction :
   - « Email 382 (extraction ; P-70) » → `` `legal/piece_thread-95_email-382.md` `` ;
   - « Email 383, extraction ; cote P-70 » → `` `legal/piece_thread-95_email-383.md` ``.
   Les Events sans fiche, les PhotoDocuments et les autres cotes restent tels quels ; énumérez-les dans votre compte rendu.
6. **Renvois.** Les mentions « bloc B », « registre Pxxx », « annexe A-1 » à « A-7 » restent en texte. Ne créez aucun renvoi `{§…}`.
7. **Notes.** Le texte se termine par `<!-- fin-du-texte -->`, suivi de `## Notes de rédaction`. Y placer, dans cet ordre : les lignes d'en-tête déplacées (règle 3), puis le contenu de la section « Notes (à retirer) » de la source, mot pour mot.

## Volet B — Le rendu des annexes par l'assembleur

Objectif : `python3 outils/assembler.py` produit, après les blocs, les annexes listées dans `blocs/annexes/ordre_annexes.txt`, dans le même document Markdown et Word.

1. **Ordre.** Créez `blocs/annexes/ordre_annexes.txt` contenant `ann07_role_de_pere.md`. L'assembleur lit ce fichier s'il existe ; absent ou vide, la sortie est celle d'aujourd'hui.
2. **Numérotation.** Chaque annexe reçoit son numéro d'ordre (1, 2…). Son titre est rendu « Annexe N — ‹titre› », sur une nouvelle page.
3. **Renvoi aux annexes depuis les blocs.** Ajoutez la syntaxe `{annexe:ann07_role_de_pere}`, rendue « l'annexe N ». Un identifiant inconnu est une `ERREUR`. Aucun bloc n'utilise encore cette syntaxe : testez-la sur une copie, sans modifier les blocs.
4. **Étiquettes d'annexe.** Les `{#ann07-…}` sont retirées du rendu et entrent dans le contrôle des doublons, comme celles des blocs.
5. **Markdown à rendre dans Word** (`outils/rendre_docx.js`) :
   - titres `##` et `###` des annexes (styles de titre définis, comme ceux des blocs) ;
   - listes à puces : configuration de numérotation `LevelFormat.BULLET`, jamais de « • » littéral ;
   - tableaux : largeur totale égale à la largeur utile de la page (format Lettre), `columnWidths` sur la table et `width` sur chaque cellule, en `WidthType.DXA` ; première ligne en gras, ombrage `ShadingType.CLEAR` ; police Times New Roman 11 dans les tableaux ;
   - accents graves (chemins de fiches) : texte simple, sans les accents graves ;
   - les notes de rédaction des annexes ne sont pas rendues (comme celles des blocs).
6. **Option** `--sans-annexes` pour assembler les blocs seuls.
7. **Non-régression.** Le rendu des blocs ne change pas. Avant toute modification, conservez `build/demande_assemblee.md` ; après, la partie qui précède la première annexe doit être identique octet pour octet (`cmp` ou `diff`).
8. Documentez la syntaxe et le fichier d'ordre dans `METHODE.md`, § 6 (assemblage) et § 8 (résumé des conventions). Mettez à jour la ligne « § 7, rôle de père » du tableau du § 9 : « converti, en attente de validation ».

## Ce qui est interdit

- Modifier le fond de l'annexe, retirer un passage, même s'il vous paraît contredire `par07_duree_2011.md` (signalez-le).
- Rédiger le paragraphe de la demande qui renverra à l'annexe : il sera rédigé à part.
- Modifier les blocs existants, le registre, les fiches `legal/piece_*.md`, ou écrire dans `legal/depots/`.
- Attribuer ou modifier une cote.

## Contrôles à exécuter

```
cd legal/amendements/01_avant_notification
python3 outils/verif_citations.py blocs/annexes/ann07_role_de_pere.md
python3 outils/assembler.py
python3 outils/assembler.py --sans-annexes      # doit redonner la sortie d'avant
soffice --headless --convert-to pdf build/demande_assemblee.docx --outdir build/   # si LibreOffice est disponible
```

Attendus : aucune `ERREUR` ; les quatre `ALERTE` connues de `par14_17_motif.md` et la citation `NO` connue de `par28_29_mediation.md`, rien d'autre ; 7 blocs, 116 paragraphes, 116 étiquettes, plus les étiquettes de l'annexe ; toute citation `NO` de l'annexe expliquée (citation de l'extraction, fiche absente). Si vous pouvez rendre le PDF, regardez au moins une page de chaque tableau.

## Rendu

- Nouvelle branche `conv/annexe-par07`, créée à partir de `fiches/email-16-portee-retrait`. Un commit pour le volet A, un pour le volet B, un pour `METHODE.md` et le journal (`journal_modifications.md`, entrée en tête, sur le modèle des précédentes). Poussez la branche.
- Si vous n'avez pas de clone complet, dites-le et précisez quels contrôles ont porté sur une copie partielle.
- **Compte rendu**, en français, un seul message :
  1. volet A : nombre de sections, de tableaux, de lignes de tableau et d'étiquettes ; chaque changement de forme autre que ceux des règles 3 à 5 ; les Events, PhotoDocuments et cotes laissés tels quels ;
  2. contradictions remarquées entre l'annexe et `par07_duree_2011.md` (dates, durée, faits au témoignage), sans les corriger ;
  3. volet B : fichiers modifiés, résultat de la non-régression, rendu des tableaux ;
  4. résultat des contrôles (citations, assembleur) ;
  5. ce que vous n'avez pas pu faire, et pourquoi.
