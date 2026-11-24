# Consigne de découpage n° 5 — lot 3 : la partie III et la partie IV

*Rédigée le 23 novembre 2026. Destinataire : un agent, qu'il ait ou non réalisé les lots précédents. Décision du demandeur (registre P475 et P476) : terminer le découpage, après validation du lot 2 et sa correction.*

## Blocs du lot

Partie III, dans l'ordre de `blocs/ordre.txt`, sauf `par09_ete_2013.md`, déjà découpé et validé :

- `blocs/p3_introduction.md` ;
- `blocs/par07_duree_2011.md` ;
- `blocs/par07_role_de_pere.md` ;
- `blocs/par10_rachat.md` ;
- `blocs/par14_17_motif.md` ;
- `blocs/par19_35_acces_autorite.md` ;
- `blocs/par28_29_mediation.md` ;
- `blocs/par56_58_assurances.md`.

Partie IV : `blocs/p4_portee.md`. Elle a été réécrite le 23 novembre 2026 et acceptée par le demandeur (P465). Ne la scindez que là où un paragraphe énonce plusieurs faits ou plusieurs conclusions que la défense pourrait admettre en partie. Justifiez chaque scission dans la table.

Les annexes 8 et 9 ne sont pas découpées : elles ne comportent pas de paragraphes numérotés.

## Contexte à lire d'abord

Branche : `fiches/email-16-portee-retrait` du dépôt `LPDavidbdeb/court`.

1. `AGENTS.md` (racine) et `legal/CLAUDE.md`.
2. `legal/amendements/01_avant_notification/blocs/METHODE.md` et `blocs/conventions.md`.
3. **`blocs/consignes/decoupage_01_essai.md`, qui s'applique intégralement.** Il comprend le critère, les types (F, C, R, M), « Ne jamais séparer », les connecteurs, « Permis » et « Interdit ». Il comprend aussi les **huit** « Règles de rédaction ». Les règles 6 à 8 sont nouvelles :
   - 6 : énumérations ;
   - 7 : thèses en italique ;
   - 8 : renvois aux annexes.

   L'étape 0 (l'archive) est déjà faite : ne la refaites pas.
4. Les modèles validés :
   - `blocs/par09_ete_2013.md`, le seul bloc de la partie III déjà découpé ;
   - `blocs/par18_entente.md` ;
   - `blocs/p2_axe1_plan_juin_2013.md` ;
   - `blocs/p2_axe4_participation.md`, corrigé par Claude : c'est le modèle des règles 6 à 8 ;
   - `blocs/consignes/decoupage_lot_01_table.md`, pour la forme de la table.
5. L'archive des blocs du lot, dans `blocs/archive/2026-11-23_avant_decoupage/`. Elle ne doit pas être modifiée.

## Ce que les lots 1 et 2 ont appris (à éviter dès le premier jet)

- **Paragraphe sans verbe** (« Le transfert du 21 avril 2015 : sous un objet qui en inverse le sens ») : reprenez le verbe de la phrase d'origine.
- **Paragraphe qui commence par un connecteur** (« Et », « Or », « Donc », « Mais ») : déplacez le connecteur après le sujet, ou retirez-le.
- **Pronom ou démonstratif en tête sans antécédent dans le paragraphe** (« Elle », « Il », « Ce », « Ces ») : nommez ce qu'il désigne.
- **Renvois** : ne renvoyez pas au paragraphe qui précède immédiatement, et ne mettez pas un renvoi dans chaque paragraphe. Les thèses font exception (règle 7).
- **Renvois entrants** : ne les redirigez jamais vers d'autres paragraphes (règle 5).
- **Énumération scindée** : l'axe 4 avait d'abord séparé « les repas », « les bains », « les couchers » et « les jeux » en quatre paragraphes tirés de la même annexe. Une énumération d'actes de même nature, tirés de la même source, reste un seul paragraphe (règle 6).
- **Thèses incohérentes** : dans l'axe 4, une seule thèse sur sept était détachée, et sans renvoi. Traitez toutes les thèses d'un bloc de la même façon (règle 7).
- **Cotes écrites à la main** (« annexes A-1 à A-4 ») : un renvoi à une annexe passe par `{annexe:id}` (règle 8).

## Points propres à ce lot

- **Intertitres en italique (`par19_35_acces_autorite.md`).** Plusieurs paragraphes commencent par une mention en italique, par exemple « *Paragraphes 19 et 26.* » ou « *Paragraphe 20.* », suivie de plusieurs phrases. Cette mention n'est pas une phrase. Faites-en un intertitre `#### Paragraphes 19 et 26 de la requête`, ou intégrez-la dans la première phrase (« Le paragraphe 20 de la requête dit… »). Puis découpez les phrases qui suivent selon le critère. Notez dans la table l'option retenue, et appliquez-la à tout le bloc.
- **Cotes de la requête.** « pièce P-5 » ou « pièce R-… » désigne une pièce produite par la partie adverse avec la requête de 2015. Ce n'est pas une cote de l'ancien régime visée par P467. Ne la retirez pas ; signalez chaque occurrence dans la table.
- **Notes.** Ce qui suit `<!-- fin-du-texte -->` n'est pas découpé.
- **Bloc d'un seul paragraphe** (`p3_introduction.md`). Appliquez le critère. Si rien ne justifie une scission, laissez-le tel quel et dites-le.

## Ce qu'il faut faire

1. Découpez les neuf blocs selon le critère et les règles 1 à 8.
2. Vérifiez les renvois entrants vers les étiquettes des blocs du lot dans tous les blocs, puis appliquez la règle 5 :
   ```
   grep -rn "{§par07-\|{§par10-\|{§par14-\|{§par19-\|{§par28-\|{§par56-\|{§p3-\|{§p4-" blocs/*.md blocs/annexes/*.md
   ```
   Les renvois cités en exemple dans `METHODE.md` et `objections_en_attente.md` ne sont pas modifiés. Signalez seulement ceux qui deviendraient invalides.
3. Remplissez `blocs/consignes/decoupage_lot_03_table.md` sur le modèle de `decoupage_lot_01_table.md` :
   - une ligne par ancien paragraphe : ancienne étiquette, type, scindé ou non, raison, nouvelles étiquettes ;
   - puis, pour chaque bloc, le relevé mot à mot par rapport à l'archive.

## Contrôles à exécuter

```
cd legal/amendements/01_avant_notification
python3 outils/verif_citations.py blocs/p3_introduction.md blocs/par07_duree_2011.md blocs/par07_role_de_pere.md blocs/par10_rachat.md blocs/par14_17_motif.md blocs/par19_35_acces_autorite.md blocs/par28_29_mediation.md blocs/par56_58_assurances.md blocs/p4_portee.md
python3 outils/assembler.py
python3 outils/assembler.py --sans-annexes --sortie /tmp/lot3
```

Attendus :

- **Erreurs et citations.** Aucune `ERREUR` ni `ALERTE`, et aucune nouvelle citation `NO`. Les citations sont identiques à l'archive, caractère par caractère et dans le même ordre.
- **Comparaison mot à mot avec l'archive.**
  - Mots ajoutés permis : des sujets, des verbes repris de la phrase d'origine, des dates, des noms de documents, des fiches et des renvois.
  - Mots retirés permis : des connecteurs, et des pronoms ou démonstratifs remplacés par ce qu'ils désignent.
  - Joignez la liste exacte.
- **Dans `/tmp/lot3/demande_assemblee.md`, pour les parties III (sauf le § 9) et IV :**
  - aucun paragraphe dont la proposition principale n'a pas de verbe conjugué ;
  - aucun paragraphe qui commence par un connecteur ;
  - aucun paragraphe qui commence par une mention en italique suivie d'un point ;
  - la liste des paragraphes qui commencent par un pronom ou un démonstratif, avec l'antécédent qui les justifie ;
  - le nombre de paragraphes qui portent un renvoi ;
  - la liste des thèses en italique, chacune avec son renvoi ;
  - aucune cote d'annexe écrite à la main.
- **Autres blocs.** Ils restent inchangés, sauf les renvois entrants ajustés selon la règle 5 (listez-les).

## Rendu

- **Branche.** Créez la branche `decoupage/lot-03` à partir de `fiches/email-16-portee-retrait`. Faites un commit par bloc, un pour les renvois entrants éventuels, et un pour la table et le journal (`journal_modifications.md`, entrée en tête). Poussez la branche.
- **À ne pas modifier :**
  - `METHODE.md`, `conventions.md` et les consignes existantes ;
  - le registre, les fiches et l'archive ;
  - tout bloc hors du lot, sauf pour ajuster un renvoi entrant ;
  - `legal/depots/`, où vous ne devez rien écrire.
- **Compte rendu**, en français, en un seul message :
  1. pour chaque bloc : le nombre de paragraphes avant et après, les paragraphes scindés par type, et les paragraphes portant un renvoi ;
  2. la liste des mots ajoutés et retirés par rapport à l'archive ;
  3. les renvois entrants ajustés ;
  4. l'option retenue pour les intertitres en italique de `par19_35`, et les cotes de la requête relevées ;
  5. les cas où vous avez hésité, avec la décision prise ;
  6. le résultat des contrôles ;
  7. ce que vous n'avez pas pu faire, et pourquoi.
- Signalez seulement ce que les textes établissent. Ne développez pas d'objections hypothétiques.
