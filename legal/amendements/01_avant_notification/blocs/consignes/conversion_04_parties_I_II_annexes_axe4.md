# Consigne de conversion n° 4 — les parties I et II du document de travail et les annexes A-1 à A-7

*Rédigée le 23 novembre 2026. Destinataire : un agent qui n'a pas participé aux travaux précédents. Travail mécanique : découper l'ancien travail en blocs et en annexes selon le nouveau processus, sans changer le fond. Modèles : les conversions n° 1 (sections en blocs) et n° 2 et 3 (annexes), toutes validées.*

## Objectif

Obtenir un seul document Word pour toute la section consacrée à la requête du 19 novembre 2015 : partie I, partie II (quatre axes), partie III (déjà en blocs), puis toutes les annexes, numérotés d'un bout à l'autre par Word, avec des renvois calculés. La partie IV n'est pas convertie : elle sera réécrite à part.

## Contexte à lire d'abord

Branche : `fiches/email-16-portee-retrait` du dépôt `LPDavidbdeb/court`. Lisez, dans cet ordre :

1. `AGENTS.md` (racine) et `legal/CLAUDE.md` ;
2. `legal/amendements/01_avant_notification/blocs/METHODE.md` (en entier) et `blocs/conventions.md` ;
3. les consignes `blocs/consignes/conversion_01_sections.md`, `conversion_02_annexe_par07.md` et `conversion_03_annexe_par09.md` ;
4. un bloc converti (`blocs/par18_entente.md`) et une annexe convertie (`blocs/annexes/ann07_role_de_pere.md`) ;
5. la source : `sections/contestation_requete_2015_document_travail_2026-11-19.md`, lignes 1 à 351 (titre, note d'en-tête, partie I, partie II) et lignes 352 à 355 (titre et § 112 de la partie III) ;
6. les annexes sources : `annexes_axe4/A-1_soirs_de_danse.md` à `annexes_axe4/A-7_vie_quotidienne.md` ;
7. les outils : `outils/assembler.py`, `outils/rendre_docx.js`, `outils/verif_citations.py`.

## Règles communes

1. **Le fond ne change pas.** Chaque phrase, chaque citation et chaque ligne de tableau est reprise mot pour mot. Si vous remarquez une erreur ou une contradiction, ne la corrigez pas : signalez-la.
2. **Ne découpez pas les paragraphes.** La règle « un fait par paragraphe » (`conventions.md`) s'appliquera plus tard, lors de la révision d'ensemble (objections O9 et O21). Un paragraphe numéroté de la source devient un paragraphe numéroté du bloc.
3. **Les numéros disparaissent.** Le `**N.**` de tête de chaque paragraphe devient `1. ` (Word numérote). Chaque paragraphe reçoit une étiquette `{#préfixe-mot-cle}` unique, en fin de paragraphe.
4. **Les renvois internes deviennent calculés.** Un renvoi à un paragraphe du document de travail (« § 44 », « §§ 49 à 53 ») devient `{§étiquette}` ou `{§début..fin}`. Un renvoi à un paragraphe **de la requête** reste en texte ; s'il est écrit « § 6 », précisez-le en « paragraphe 6 de la requête » seulement si la source le dit sans ambiguïté, sinon laissez-le et listez-le. Un renvoi à un paragraphe de la partie IV (non convertie) reste en texte et est listé.
5. **Les citations en retrait** (lignes `> `) rattachées à un paragraphe deviennent des sous-items `   a) `, `   b) `… de ce paragraphe, dans l'ordre, mot pour mot.
6. **Désignations des pièces.** Chemin `legal/…` entre accents graves ; les liens relatifs Markdown (`[...](../../../piece_x.md)`) deviennent `` `legal/piece_x.md` ``. Rien d'autre ne change dans les désignations. Ne créez aucune fiche ; n'ajoutez ni ne modifiez aucune cote.

## Volet A — Les parties I et II en blocs

Créez dans `blocs/` :

| Fichier | Contenu de la source | Préfixe d'étiquette |
|---|---|---|
| `p1_these_requete.md` | Partie I, §§ 1 à 15 | `p1-` |
| `p2_axe1_plan_juin_2013.md` | Axe 1, §§ 16 à 56 | `ax1-` |
| `p2_axe2_grief.md` | Axe 2, §§ 57 à 80 | `ax2-` |
| `p2_axe3_consentement_aout_2015.md` | Axe 3, §§ 81 à 99 | `ax3-` |
| `p2_axe4_participation.md` | Axe 4, §§ 100 à 111 | `ax4-` |
| `p3_introduction.md` | Partie III, § 112 | `p3-` |

- **En-tête YAML** sur le modèle des blocs existants : `bloc`, `requete` (paragraphes de la requête visés, d'après le texte), `statut: converti, à valider`, `depend_de`, `registre: []`, `remplace: "§§ x à y du document de travail du 19 novembre 2026 (commit d27ef4c)"`.
- **Titres.** Le titre de l'axe (`### Axe 1 — …`) devient le `# ` du bloc. Pour la partie I et l'introduction de la partie III, le `# ` reprend le titre de la partie. Les intertitres (`####`) restent des `#### `. Aucun autre niveau de titre dans un bloc.
- **Notes.** Les commentaires de rédaction éventuels passent après `<!-- fin-du-texte -->`.
- **Ce qui ne va pas dans les blocs**, mais est conservé mot pour mot dans `blocs/notes/document_travail_2026-11-19_hors_blocs.md` (fichier non assemblé) :
  - la note d'en-tête « Document de travail — … » (ligne 3) ;
  - la section « Registre de vérification — hors allégations » (lignes 587 et suivantes).

## Volet B — Les annexes A-1 à A-7

Créez dans `blocs/annexes/` les fichiers `annA1_soirs_de_danse.md` à `annA7_vie_quotidienne.md`, selon les règles de la conversion n° 2 (volet A) : en-tête YAML (`annexe`, `titre`, `requete`, `rattachee_a: p2_axe4_participation`, `statut`, `registre`, `source`) ; `# ` titre sans « Annexe A-n — » ; sections `##` et `###` sans leur numéro, une étiquette `{#aA1-…}` (etc.) par section `##` ; tableaux et listes inchangés ; en-tête de source, ligne de version et notes après `<!-- fin-du-texte -->`. L'inventaire `annexes_axe4/inventaire_courriels_LP_Johanne.md` n'est pas une annexe : laissez-le en place.

## Volet C — Assemblage

1. **Titres de partie.** Ajoutez à `outils/assembler.py` (et au rendu Word) la possibilité d'insérer un titre de partie depuis `blocs/ordre.txt` : une ligne commençant par `## ` (par exemple `## I. La thèse historique présentée au Tribunal`) produit un titre de premier niveau, sans numéro de paragraphe. Les lignes vides et les lignes commençant par `#` autre que `## ` restent interdites ou ignorées comme aujourd'hui ; documentez le choix.
2. **`blocs/ordre.txt` devient :**
   ```
   ## I. La thèse historique présentée au Tribunal
   p1_these_requete.md
   ## II. Contestation de la thèse générale selon quatre axes
   p2_axe1_plan_juin_2013.md
   p2_axe2_grief.md
   p2_axe3_consentement_aout_2015.md
   p2_axe4_participation.md
   ## III. Examen individualisé des autres représentations de la requête
   p3_introduction.md
   (les blocs actuels, dans leur ordre actuel)
   ```
   Reprenez les intitulés exacts de la source.
3. **`blocs/annexes/ordre_annexes.txt` devient :** `annA1` à `annA7`, puis `ann07_role_de_pere.md`, puis `ann09_ete_2013.md`.
4. **Renvois aux annexes.** Dans les blocs de l'axe 4, chaque mention « annexe A-n » devient `{annexe:annAn_…}` (rendu « l'annexe N ») ; adaptez seulement l'article ou la préposition qui précède, si nécessaire, et listez chaque adaptation. « annexes A-1 à A-4 » : remplacez par les renvois individuels ou laissez en texte, et listez.
5. **Les quatre alertes connues de `par14_17_motif.md`** renvoient aux axes du document de travail. Remplacez-les par les renvois calculés correspondants (`{§…}`) ; c'est la seule modification permise dans les blocs de la partie III. Listez-les.

## Ce qui est interdit

- Modifier le fond d'un texte ; découper un paragraphe ; fusionner deux paragraphes.
- Convertir ou modifier la partie IV (§§ 228 à 230).
- Modifier les blocs de la partie III autrement que pour la règle C.5, les annexes 1 et 2, le registre, les fiches `legal/piece_*.md`, ou écrire dans `legal/depots/`.
- Supprimer `sections/contestation_requete_2015_document_travail_2026-11-19.md` ou `annexes_axe4/` : les sources restent intactes.
- Attribuer ou modifier une cote.

## Contrôles à exécuter

```
cd legal/amendements/01_avant_notification
python3 outils/assembler.py --sans-annexes --sortie /tmp/avant          # avant toute modification
python3 outils/verif_citations.py blocs/p1_*.md blocs/p2_*.md blocs/p3_*.md blocs/annexes/annA*.md
python3 outils/assembler.py
soffice --headless --convert-to pdf build/demande_assemblee.docx --outdir build/   # si disponible
```

Attendus :
- aucune `ERREUR` ; aucune nouvelle `ALERTE` ; les quatre `ALERTE` de `par14_17_motif.md` disparaissent ;
- nombre de paragraphes = 145 (actuels) + 111 (§§ 1 à 111) + 1 (§ 112) = **257**, et autant d'étiquettes de bloc ; 9 annexes ;
- **identité du texte** : pour chaque bloc et chaque annexe créés, comparaison mot à mot avec la source, une fois neutralisés les numéros, les étiquettes, les renvois et les désignations ; joignez le résultat ;
- **non-régression de la partie III** : son texte assemblé est identique à `/tmp/avant`, à la numérotation près (les numéros de paragraphes et les renvois calculés changent, rien d'autre) ;
- les renvois calculés des parties I et II pointent vers les mêmes paragraphes que les renvois écrits de la source (table de correspondance ancien numéro → nouveau numéro) ;
- citations : tout `NO` nouveau expliqué (source hors fiches, extraction) ;
- si vous pouvez rendre le PDF, regardez au moins les titres de partie, une page par axe et une page de tableau par annexe.

## Rendu

- Nouvelle branche `conv/parties-I-II`, créée à partir de `fiches/email-16-portee-retrait`. Un commit par volet (A, B, C), puis un pour `METHODE.md` (§ 6 : titres de partie ; § 9 : tableau d'état) et le journal (`journal_modifications.md`, entrée en tête). Poussez la branche.
- Si vous n'avez pas de clone complet, dites-le et précisez quels contrôles ont porté sur une copie partielle.
- **Compte rendu**, en français, un seul message :
  1. fichiers créés, avec leur nombre de paragraphes, de sous-items, d'intertitres et d'étiquettes (annexes : sections, tableaux, lignes) ;
  2. la table de correspondance ancien numéro → nouvelle étiquette, et la liste des renvois laissés en texte (requête, partie IV, autres) ;
  3. chaque changement de forme autre que ceux des règles 3 à 6 et des volets B et C ;
  4. le résultat des contrôles ;
  5. ce que vous avez remarqué et laissé en l'état (erreurs, contradictions entre parties) ;
  6. ce que vous n'avez pas pu faire, et pourquoi.
- Signalez seulement ce que les pièces ou les textes établissent ou contredisent. Ne développez pas d'objections hypothétiques que ni les pièces ni la partie adverse ne soulèvent.
