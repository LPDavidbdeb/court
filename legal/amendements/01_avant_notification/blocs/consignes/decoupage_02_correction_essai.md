# Consigne de découpage n° 2 — correction de l'essai sur deux blocs

*Rédigée le 23 novembre 2026. Destinataire : l'agent qui a réalisé l'essai n° 1 ou un autre agent. Décision du demandeur (registre P470) : corriger l'essai avant d'étendre le découpage aux autres blocs.*

## Ce qui a été validé, et ce qui ne l'est pas

L'essai n° 1 (branche `decoupage/essai-01`) est conforme sur le plan mécanique : archive identique, citations intactes, aucun fait ajouté ni retiré, assemblage sans erreur. La structure est améliorée : les faits sont séparés des conclusions, et les conclusions suivent les faits qu'elles visent.

La rédaction ne l'est pas. Après assemblage, on relève :
- **20 paragraphes sans verbe**, où les deux-points remplacent le verbe. Paragraphe 18 : `par18-…` rendus §§ 250, 261, 281, 285, 287, 291, 292, 295, 299. Axe 1 : rendus §§ 17, 21, 27, 39, 50, 60, 70, 73, 115, 117, 118. Exemples : « Le paragraphe 18 de la requête : cette entente une dernière fois sous serment devant le tribunal » ; « Le transfert du 21 avril 2015 : sous un objet qui en inverse le sens » ; « Le courriel du 16 septembre 2016, 22 h 25 UTC : le lien d'attachement des enfants ».
- **5 paragraphes qui commencent par « Et »** : rendus §§ 54, 82, 90 (axe 1), 270, 292 (paragraphe 18).
- **Des pronoms sans antécédent** en tête de paragraphe (par exemple, rendu § 249 : « Elle est affirmée avant même que les parties ne se séparent », qui suit la citation de la requête ; 27 paragraphes commencent par un pronom ou un démonstratif, à revoir un à un).
- **Des renvois trop nombreux** : 106 paragraphes sur 162 en portent, souvent vers le paragraphe immédiatement précédent.
- **Deux renvois entrants redirigés** dans `par14_17_motif.md` au-delà de ce que le découpage exigeait :
  - `par14-plan-2013` : `{§ax1-precedent..ax1-routine-posterieure}` devenu `{§ax1-precedent..ax1-fonction-precedent}` ;
  - `par14-connaissance-objectif` : `{§ax1-accusations-passees..ax1-motifs-successifs}` devenu `{§ax1-bornes-regime..ax1-confirmation-2016}`.

Les numéros « rendus » ci-dessus sont ceux de `build/demande_assemblee.md` produit sur la branche `decoupage/essai-01` ; retrouvez les étiquettes correspondantes dans le Markdown assemblé.

## Ce qu'il faut faire

Travaillez sur la branche existante `decoupage/essai-01` (ne repartez pas de zéro ; l'archive et l'étiquette `avant-decoupage` restent en place).

1. **Lisez d'abord** `blocs/consignes/decoupage_01_essai.md` dans sa version à jour de la branche `fiches/email-16-portee-retrait` (section « Règles de rédaction », ajoutée après l'essai) et la règle correspondante de `blocs/conventions.md`. Récupérez ces deux fichiers à jour sur votre branche (`git checkout origin/fiches/email-16-portee-retrait -- legal/amendements/01_avant_notification/blocs/consignes/decoupage_01_essai.md legal/amendements/01_avant_notification/blocs/conventions.md`).
2. **Corrigez `par18_entente.md` et `p2_axe1_plan_juin_2013.md`** selon les cinq règles de rédaction :
   - chaque paragraphe est une phrase complète ; reprenez le verbe de la phrase d'origine (archive) ; si un fait ne peut tenir seul sans être déformé, **refusionnez-le** avec le paragraphe d'origine (c'est la seule fusion permise, et seulement pour annuler une coupe de l'essai) ;
   - aucun connecteur en tête ;
   - aucun pronom ni démonstratif sans antécédent dans le paragraphe ;
   - renvois seulement quand ils sont utiles (règle 4) ;
   - ne changez aucune citation, aucune pièce, aucun fait.
3. **Rétablissez les deux renvois entrants** de `par14_17_motif.md` selon la règle 5 : un intervalle dont les deux bornes existent encore reste inchangé (donc `{§ax1-precedent..ax1-routine-posterieure}` et `{§ax1-accusations-passees..ax1-motifs-successifs}`, si ces étiquettes existent toujours). Le troisième ajustement (`par14-constat-refus`, b) suit la même règle : une étiquette scindée devient l'intervalle de ses parties. Si une cible d'origine vous paraît mal choisie, signalez-le sans la changer.
4. **Mettez à jour la table de décision** `blocs/consignes/decoupage_01_table.md` : une colonne « Correction n° 2 » indiquant, pour chaque ligne touchée, ce qui a changé (verbe rétabli, connecteur retiré, antécédent rétabli, renvoi retiré, refusion).

## Contrôles à exécuter

```
cd legal/amendements/01_avant_notification
python3 outils/verif_citations.py blocs/par18_entente.md blocs/p2_axe1_plan_juin_2013.md
python3 outils/assembler.py
```

Attendus :
- aucune `ERREUR` ni `ALERTE` ; aucune citation `NO` nouvelle ;
- comparaison mot à mot avec l'**archive** (`blocs/archive/2026-11-23_avant_decoupage/`) : les mots ajoutés sont des sujets, des verbes repris de la phrase d'origine, des dates, des noms de documents et des renvois ; les mots retirés, des connecteurs ; joignez la liste exacte ;
- dans le Markdown assemblé des deux blocs : aucun paragraphe dont la première proposition est sans verbe conjugué ; aucun paragraphe commençant par un connecteur ; liste des paragraphes qui commencent encore par un pronom ou un démonstratif, avec l'antécédent qui les justifie ;
- nombre de paragraphes portant un renvoi, avant et après la correction.

## Rendu

- Sur la branche `decoupage/essai-01` : un commit par bloc corrigé, un pour `par14_17_motif.md`, un pour la table et le journal (`journal_modifications.md`, entrée en tête). Poussez la branche.
- Ne modifiez aucun autre bloc, ni le registre, ni les fiches ; n'écrivez pas dans `legal/depots/`.
- **Compte rendu**, en français, un seul message :
  1. pour chaque bloc : nombre de paragraphes (archive, essai, correction) ; nombre de verbes rétablis, de connecteurs retirés, d'antécédents rétablis, de renvois retirés, de refusions ;
  2. la liste des mots ajoutés et retirés par rapport à l'archive ;
  3. les renvois entrants rétablis ;
  4. les cas où vous avez hésité, avec la décision prise ;
  5. le résultat des contrôles ;
  6. ce que vous n'avez pas pu faire, et pourquoi.
- Signalez seulement ce que les textes établissent. Ne développez pas d'objections hypothétiques.
