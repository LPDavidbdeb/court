# Consigne de découpage n° 4 — lot 2 : la partie I et l'axe 4

*Rédigée le 23 novembre 2026. Destinataire : un agent, qu'il ait ou non réalisé l'essai. Décision du demandeur (registre P472 et P473) : étendre le découpage, par lots, après validation de l'essai sur le paragraphe 18 et l'axe 1.*

## Blocs du lot

- `blocs/p1_these_requete.md` (partie I — la thèse historique présentée au Tribunal) ;
- `blocs/p2_axe4_participation.md` (axe 4 — la participation effective du père). Les annexes 1 à 7 ne sont pas découpées : elles ne comportent pas de paragraphes numérotés.

## Contexte à lire d'abord

Branche : `fiches/email-16-portee-retrait` du dépôt `LPDavidbdeb/court`.

1. `AGENTS.md` (racine) et `legal/CLAUDE.md` ;
2. `legal/amendements/01_avant_notification/blocs/METHODE.md` et `blocs/conventions.md` ;
3. **`blocs/consignes/decoupage_01_essai.md` : le critère, les types (F, C, R, M), « Ne jamais séparer », les connecteurs, « Permis », les cinq « Règles de rédaction » et « Interdit ». Ils s'appliquent intégralement.** L'étape 0 (archive) est déjà faite : ne la refaites pas ;
4. les modèles validés : `blocs/par18_entente.md`, `blocs/p2_axe1_plan_juin_2013.md`, `blocs/p2_axe2_grief.md` et `blocs/p2_axe3_consentement_aout_2015.md` (découpés et validés), et `blocs/consignes/decoupage_lot_01_table.md` (forme de la table) ;
5. l'archive des deux blocs du lot : `blocs/archive/2026-11-23_avant_decoupage/p1_these_requete.md` et `…/p2_axe4_participation.md`. Elle ne doit pas être modifiée.

## Ce que l'essai a appris (à éviter dès le premier jet)

- Un paragraphe sans verbe (« Le transfert du 21 avril 2015 : sous un objet qui en inverse le sens ») : reprenez le verbe de la phrase d'origine.
- Un paragraphe qui commence par « Et », « Or », « Donc » : déplacez ou retirez le connecteur.
- Un « Elle », « Il », « Ce », « Ces » en tête sans antécédent dans le paragraphe : nommez ce qu'il désigne.
- Un renvoi vers le paragraphe qui précède immédiatement, ou dans chaque paragraphe : n'en mettez que là où un raisonnement conclut sur des faits qui ne le précèdent pas immédiatement, ou sur plusieurs faits.
- Un renvoi entrant redirigé vers d'autres paragraphes : interdit (règle 5).

## Ce qu'il faut faire

1. Découpez les deux blocs selon le critère et les règles.
2. Vérifiez les renvois entrants vers les étiquettes `p1-…` et `ax4-…` dans tous les blocs (`grep -rn "{§p1-\|{§ax4-" blocs/*.md`) et appliquez la règle 5.
3. Remplissez `blocs/consignes/decoupage_lot_02_table.md`, sur le modèle de `decoupage_lot_01_table.md` : une ligne par ancien paragraphe (ancienne étiquette, type, scindé ou non, raison, nouvelles étiquettes), puis le relevé mot à mot par rapport à l'archive.

## Contrôles à exécuter

```
cd legal/amendements/01_avant_notification
python3 outils/verif_citations.py blocs/p1_these_requete.md blocs/p2_axe4_participation.md
python3 outils/assembler.py
python3 outils/assembler.py --sans-annexes --sortie /tmp/lot2
```

Attendus :
- aucune `ERREUR` ni `ALERTE` ; aucune citation `NO` nouvelle ; les citations identiques à l'archive, caractère par caractère et dans le même ordre ;
- comparaison mot à mot avec l'archive : les mots ajoutés sont des sujets, des verbes repris de la phrase d'origine, des dates, des noms de documents, des fiches et des renvois ; les mots retirés, des connecteurs, des pronoms et démonstratifs remplacés par ce qu'ils désignent ; joignez la liste exacte ;
- dans `/tmp/lot2/demande_assemblee.md`, pour la partie I et l'axe 4 : aucun paragraphe dont la proposition principale est sans verbe conjugué ; aucun paragraphe commençant par un connecteur ; la liste des paragraphes qui commencent par un pronom ou un démonstratif, avec l'antécédent qui les justifie ; le nombre de paragraphes portant un renvoi ;
- les autres blocs inchangés, sauf les renvois entrants ajustés selon la règle 5 (listez-les).

## Rendu

- Nouvelle branche `decoupage/lot-02`, créée à partir de `fiches/email-16-portee-retrait`. Un commit par bloc, un pour les renvois entrants éventuels, un pour la table et le journal (`journal_modifications.md`, entrée en tête). Poussez la branche.
- Ne modifiez ni `METHODE.md`, ni `conventions.md`, ni les consignes existantes, ni le registre, ni les fiches, ni l'archive, ni aucun autre bloc que ceux du lot (sauf l'ajustement d'un renvoi entrant). N'écrivez pas dans `legal/depots/`.
- **Compte rendu**, en français, un seul message :
  1. pour chaque bloc : paragraphes avant et après ; paragraphes scindés, par type ; paragraphes portant un renvoi ;
  2. la liste des mots ajoutés et retirés par rapport à l'archive ;
  3. les renvois entrants ajustés ;
  4. les cas où vous avez hésité, avec la décision prise ;
  5. le résultat des contrôles ;
  6. ce que vous n'avez pas pu faire, et pourquoi.
- Signalez seulement ce que les textes établissent. Ne développez pas d'objections hypothétiques.
