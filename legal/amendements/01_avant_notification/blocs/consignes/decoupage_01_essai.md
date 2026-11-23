# Consigne de découpage n° 1 — essai sur deux blocs : un fait par paragraphe

*Rédigée le 23 novembre 2026. Destinataire : un agent qui n'a pas participé aux travaux précédents. Décision du demandeur (registre P461 et P468) : chaque paragraphe numéroté énonce un seul fait. Cet essai porte sur deux blocs ; les autres suivront par lots si l'essai est validé.*

## Contexte à lire d'abord

Branche : `fiches/email-16-portee-retrait` du dépôt `LPDavidbdeb/court`. Lisez, dans cet ordre :

1. `AGENTS.md` (racine) et `legal/CLAUDE.md` (en particulier « Liste de faits », règles 1 à 3) ;
2. `legal/amendements/01_avant_notification/blocs/METHODE.md` et `blocs/conventions.md` (règle « Un fait par paragraphe ») ;
3. le modèle déjà découpé et accepté par le demandeur : `blocs/par09_ete_2013.md` ;
4. les deux blocs de l'essai : `blocs/par18_entente.md` (surtout des faits) et `blocs/p2_axe1_plan_juin_2013.md` (surtout des raisonnements).

## Étape 0 — l'archive

Avant toute modification :

1. Copiez **tous** les fichiers `blocs/*.md` (sauf `METHODE.md`, `conventions.md`, `objections_en_attente.md`) et `blocs/annexes/*.md` dans `blocs/archive/2026-11-23_avant_decoupage/` (même arborescence : `annexes/` en sous-dossier). Ces copies ne sont jamais modifiées ni assemblées.
2. Posez l'étiquette Git `avant-decoupage` sur le commit de départ et poussez-la (`git push origin avant-decoupage`).
3. Produisez la sortie de référence : `python3 outils/assembler.py --sans-annexes --sortie /tmp/avant`.

Les blocs réécrits gardent leur nom ; `blocs/ordre.txt` ne change pas.

## Le critère

**Question à poser pour chaque paragraphe : la défense pourrait-elle admettre une partie de ce paragraphe et en nier une autre ?** Si oui, il contient plusieurs faits : on le scinde. Si non, il n'en contient qu'un, même s'il compte plusieurs phrases.

Classez chaque paragraphe dans l'un de quatre types :

| Type | Définition | Règle |
|---|---|---|
| **F — fait** | Ce qui s'est passé, ou ce qu'un document dit, avec sa source | Un fait par paragraphe. Deux dates, deux acteurs ou deux sources séparément contestables donnent deux paragraphes. |
| **C — citation** | Un ou plusieurs passages d'un même document, avec leur auteur, leur date et leur source | Ne pas scinder : la citation et son attribution forment un seul fait. Plusieurs passages d'un même document restent des sous-items `a)`, `b)`… |
| **R — raisonnement** | Une déduction, une juxtaposition, une conclusion | Une seule conclusion par paragraphe. S'il en contient deux, on le scinde. |
| **M — mixte** | Un ou plusieurs faits suivis d'une ou plusieurs conclusions | Les faits deviennent des paragraphes F (ou C) ; chaque conclusion devient un paragraphe R, placé après eux, qui y renvoie par `{§étiquette}` ou `{§début..fin}` au lieu de les redire. |

**Ne jamais séparer :**
- un fait de la précision sans laquelle il serait faux ou mal attribué (« selon la lettre du 27 avril 2015 », « témoignage du demandeur », « au nom de sa sœur ») ;
- une citation de son auteur, de sa date et de sa source ;
- une concession de sa limite (« Le demandeur admet X ; la requête ne parle pas de X ») ;
- un renvoi à une pièce du fait qu'il appuie.

**Les connecteurs** (« Or », « donc », « ainsi », « pourtant », « en effet ») restent dans le paragraphe de raisonnement. Un paragraphe de fait ne commence pas par un connecteur ; si la coupe en laisse un en tête d'un fait, retirez ce seul mot et listez-le.

**Permis, et seulement cela :**
- répéter le sujet, la date ou le nom du document pour qu'un paragraphe se lise seul ;
- couper une phrase à un point-virgule ou à un « et » qui relie deux faits, en rétablissant le sujet ;
- ajouter des renvois `{§…}` du raisonnement vers les faits ;
- ajouter un intertitre `#### ` si une suite de faits courts a besoin d'un repère (listez-le).

**Règles de rédaction (ajoutées le 23 novembre 2026 après l'essai n° 1 ; elles s'appliquent à tout découpage) :**

1. **Chaque paragraphe est une phrase complète**, avec un sujet et un verbe conjugué. Pour y parvenir, reprenez le verbe de la phrase d'origine (« La requête affirme cette entente une dernière fois sous serment », et non « Le paragraphe 18 de la requête : cette entente une dernière fois sous serment »). Les deux-points ne remplacent jamais un verbe ; ils n'introduisent qu'une citation ou une énumération. Si un fait ne peut tenir seul sans être déformé ou sans un mot qui n'est pas dans la source, ne le détachez pas : laissez-le dans le paragraphe d'origine et notez-le dans la table.
2. **Aucun paragraphe ne commence par un connecteur** (« Et », « Or », « Donc », « Mais », « Puis », « Alors », « Ainsi », « Pourtant », « En effet »). Dans un paragraphe de raisonnement, le connecteur se place après le sujet (« Ces messages ne confirment donc aucune entente ») ou disparaît s'il ne fait que relier deux faits.
3. **Aucun pronom ni démonstratif sans antécédent dans le même paragraphe.** Un « Elle », « Il », « Ce », « Cette », « Ces » en tête de paragraphe est remplacé par le nom qu'il désigne, tiré de la phrase d'origine (« L'entente alléguée est affirmée avant même que les parties ne se séparent »). « Ce décompte », « Cette confrontation » sont admis si le paragraphe qui précède immédiatement les nomme.
4. **Renvois : seulement quand ils sont utiles.** Un paragraphe de raisonnement renvoie aux faits qu'il conclut, sauf si ces faits sont exactement le paragraphe qui le précède immédiatement. Un paragraphe de fait ne renvoie pas au paragraphe voisin pour se justifier : sa source est la pièce. Un même renvoi n'est pas répété dans deux paragraphes consécutifs.
5. **Renvois entrants.** Une étiquette scindée garde son nom sur la première partie. Un renvoi entrant qui visait une étiquette scindée vise désormais l'intervalle `{§première..dernière}` de ses parties. Un intervalle entrant dont les deux bornes existent encore reste inchangé. Ne redirigez jamais un renvoi vers d'autres paragraphes que ceux qu'il visait : si la cible vous paraît mal choisie, signalez-le sans la changer.

**Interdit :** ajouter ou retirer un fait, une nuance, une citation ou une pièce ; changer un mot d'une citation ; changer l'ordre des faits, sauf pour placer un raisonnement après les faits qu'il vise ; fusionner deux paragraphes ; qualifier (aucun mot de `conventions.md`, « Mots exclus »).

## Étiquettes et renvois

- Un paragraphe non scindé garde son étiquette.
- Un paragraphe scindé : la **première** partie garde l'ancienne étiquette ; les suivantes reçoivent des étiquettes nouvelles, au même préfixe (`par18-…`, `ax1-…`).
- Tout renvoi existant, dans tous les blocs, vers une étiquette dont le contenu a été scindé doit continuer de viser le bon fait : vérifiez les renvois entrants (`grep -rn "{§ancienne-etiquette" blocs/`) et ajustez-les si le fait visé est passé dans une nouvelle étiquette (listez chaque ajustement).

## Contrôles à exécuter

```
cd legal/amendements/01_avant_notification
python3 outils/verif_citations.py blocs/par18_entente.md blocs/p2_axe1_plan_juin_2013.md
python3 outils/assembler.py
python3 outils/assembler.py --sans-annexes --sortie /tmp/apres
```

Attendus : aucune `ERREUR` ni `ALERTE` ; aucune citation `NO` nouvelle ; comparaison mot à mot entre l'archive et la réécriture de chaque bloc : les seuls mots ajoutés sont des sujets, dates ou noms de documents répétés et les renvois ; les seuls mots retirés sont des connecteurs en tête de fait (règle ci-dessus). Joignez la liste exacte des mots ajoutés et retirés.

## Rendu

- Nouvelle branche `decoupage/essai-01`, créée à partir de `fiches/email-16-portee-retrait`. Un commit pour l'archive, un par bloc réécrit, un pour le journal (`journal_modifications.md`, entrée en tête). Poussez la branche et l'étiquette.
- Ne modifiez ni `METHODE.md`, ni `conventions.md`, ni le registre, ni les fiches, ni aucun autre bloc que les deux de l'essai (sauf l'ajustement d'un renvoi entrant, listé). N'écrivez pas dans `legal/depots/`.
- **Table de décision**, dans un fichier `blocs/consignes/decoupage_01_table.md`, une ligne par ancien paragraphe :

  | Ancienne étiquette | Type (F, C, R, M) | Scindé ? | Raison (quelques mots) | Nouvelles étiquettes, dans l'ordre |
  |---|---|---|---|---|

- **Compte rendu**, en français, un seul message :
  1. pour chaque bloc : nombre de paragraphes avant et après ; nombre de paragraphes scindés, par type ;
  2. la liste des mots ajoutés et retirés (comparaison mot à mot) ;
  3. les renvois entrants ajustés et les intertitres ajoutés ;
  4. les cas où vous avez hésité, avec la décision prise et pourquoi ;
  5. le résultat des contrôles ;
  6. ce que vous n'avez pas pu faire, et pourquoi.
- Signalez seulement ce que les textes établissent. Ne développez pas d'objections hypothétiques.
