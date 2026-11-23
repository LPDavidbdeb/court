# Consigne de conversion n° 3 — l'annexe du paragraphe 9 (l'été 2013)

*Rédigée le 23 novembre 2026. Destinataire : un agent qui n'a pas participé aux travaux précédents. Travail mécanique : changer la forme, jamais le fond. Modèle : la conversion n° 2 (`blocs/consignes/conversion_02_annexe_par07.md`, volet A), validée le 23 novembre 2026. L'assembleur rend déjà les annexes : aucun outil n'est à modifier.*

## Contexte à lire d'abord

Branche : `fiches/email-16-portee-retrait` du dépôt `LPDavidbdeb/court`. Lisez, dans cet ordre :

1. `AGENTS.md` (racine) et `legal/CLAUDE.md` ;
2. `legal/amendements/01_avant_notification/blocs/METHODE.md` (§§ 4 à 6, 8 et 10) et `blocs/conventions.md` ;
3. le modèle : `blocs/annexes/ann07_role_de_pere.md` ;
4. la source à convertir : `analyses_experimentales/annexe_par9_ete_2013.md` (version 2 du 20 novembre 2026) ;
5. les blocs qui citent des pièces de la même période, pour le volet « écarts » du compte rendu : `blocs/par10_rachat.md` (courriels des 26 et 27 juin et du 19 juillet 2013) et `blocs/par19_35_acces_autorite.md` (`par19-presence-tiers`, fil du 30 juin 2013).

## Ce qu'il faut faire

Créez `blocs/annexes/ann09_ete_2013.md`. La source reste intacte.

1. **Le fond ne change pas.** Le texte de chaque section, de chaque ligne de tableau et de chaque citation est repris mot pour mot. Si vous remarquez une erreur ou une contradiction, ne la corrigez pas : signalez-la dans votre compte rendu.
2. **En-tête YAML :**
   ```yaml
   ---
   annexe: ann09_ete_2013
   titre: "La présence du père pendant l'été 2013"
   requete: [9]
   rattachee_a: "par09_ete_2013 (bloc à rédiger)"
   statut: à valider
   registre: []   # reprenez les entrées Pxxx citées dans la source, dans l'ordre croissant
   source: "analyses_experimentales/annexe_par9_ete_2013.md (version 2, 20 novembre 2026)"
   ---
   ```
3. **Titre et introduction.** `# ` suivi du titre. La ligne en italique qui suit le titre de la source passe dans les notes (règle 7).
4. **La section « 0. Texte proposé pour la demande »** n'appartient pas à l'annexe : c'est le texte du futur bloc de la demande. Déplacez-la, mot pour mot, en tête des notes, sous l'intitulé « Texte proposé pour le bloc `par09_ete_2013` ».
5. **Sections.** Les sections 1 à 9 deviennent des titres `## ` sans leur numéro ; les sous-sections, des titres `### ` sans leur numéro. Une étiquette `{#ann09-mot-cle}` unique à la fin de chaque titre `##`. Les listes restent des listes `- ` ; les tableaux restent des tableaux Markdown, colonnes inchangées.
6. **Désignation des pièces.** Chemin `legal/…` entre accents graves pour chaque fiche (`piece_event-244.md` devient `` `legal/piece_event-244.md` ``). Quatre fiches existent depuis le 23 novembre pour des courriels que la source cite par l'extraction :
   - courriel 39 du 27 juin 2013 → `` `legal/piece_email-39_grimmel_2013-06-27.md` `` ;
   - courriel 137 du 19 juillet 2013 (le sous-sol) → `` `legal/piece_email-137_brunet_2013-07-19.md` `` ;
   - courriels 382 et 383 du 12 septembre 2011, s'ils sont cités → `` `legal/piece_thread-95_email-382.md` ``, `` `legal/piece_thread-95_email-383.md` ``.
   
   Avant de remplacer une mention « extraction » par une fiche, vérifiez que la citation figure dans cette fiche. Toute autre mention « extraction », tout Event sans fiche et tout PhotoDocument restent tels quels ; énumérez-les dans votre compte rendu. Ne créez aucune fiche.
7. **Cotes.** N'ajoutez ni ne modifiez aucune cote. Si la source mentionne une cote (P-xx), vérifiez-la dans `legal/bordereau_pieces.md` et signalez tout écart, sans corriger.
8. **Renvois.** Les mentions des annexes A-1 à A-7, des blocs du document de travail, du registre et des paragraphes de la requête restent en texte. Ne créez aucun renvoi `{§…}`.
9. **Notes.** Le texte se termine par `<!-- fin-du-texte -->`, suivi de `## Notes de rédaction`. Y placer, dans cet ordre : le texte proposé pour le bloc (règle 4), la ligne d'en-tête déplacée (règle 3), puis le contenu de la section « Notes (à retirer) » de la source, mot pour mot.
10. **Ordre d'assemblage.** Ajoutez `ann09_ete_2013.md` à la fin de `blocs/annexes/ordre_annexes.txt`.
11. **`METHODE.md`, § 9.** Ligne « § 9 » : `blocs/annexes/ann09_ete_2013.md` ; « annexe convertie, en attente de validation ; bloc à rédiger ».

## Ce qui est interdit

- Modifier le fond de l'annexe, retirer ou ajouter un passage.
- Rédiger le bloc de la demande qui renverra à l'annexe.
- Modifier les blocs, les autres annexes, les outils, le registre, les fiches `legal/piece_*.md`, ou écrire dans `legal/depots/`.
- Attribuer ou modifier une cote.

## Contrôles à exécuter

```
cd legal/amendements/01_avant_notification
python3 outils/assembler.py --sans-annexes --sortie /tmp/avant     # avant toute modification
python3 outils/verif_citations.py blocs/annexes/ann09_ete_2013.md
python3 outils/assembler.py
python3 outils/assembler.py --sans-annexes --sortie /tmp/apres
cmp /tmp/avant/demande_assemblee.md /tmp/apres/demande_assemblee.md
soffice --headless --convert-to pdf build/demande_assemblee.docx --outdir build/   # si LibreOffice est disponible
```

Attendus :
- aucune `ERREUR` ; 8 blocs, 128 paragraphes, 128 étiquettes ; 2 annexes ;
- les quatre `ALERTE` connues de `par14_17_motif.md`, la citation `NO` connue de `par28_29_mediation.md` et les trois `NO` attendus de l'annexe 1 (art. 599, « puissance paternelle », « relation d'activation »), rien d'autre que les `NO` de l'annexe 2, chacun expliqué (citation de l'extraction, fiche absente) ;
- la partie des blocs identique octet pour octet avant et après (`cmp` sans sortie) ;
- l'annexe 2 rendue à la suite de l'annexe 1, sur une nouvelle page ; si vous pouvez rendre le PDF, regardez au moins une page de chaque tableau.

## Rendu

- Nouvelle branche `conv/annexe-par09`, créée à partir de `fiches/email-16-portee-retrait`. Un commit pour l'annexe, un pour `ordre_annexes.txt`, `METHODE.md` et le journal (`journal_modifications.md`, entrée en tête, sur le modèle des précédentes). Poussez la branche.
- Si vous n'avez pas de clone complet, dites-le et précisez quels contrôles ont porté sur une copie partielle.
- **Compte rendu**, en français, un seul message :
  1. nombre de sections, de sous-sections, de tableaux, de lignes de tableau et d'étiquettes ; chaque changement de forme autre que ceux des règles 3 à 6 ;
  2. les mentions « extraction », les Events sans fiche, les PhotoDocuments et les cotes laissés tels quels ;
  3. les écarts entre l'annexe et les blocs `par10_rachat.md` et `par19_35_acces_autorite.md` (dates, citations, faits au témoignage), sans les corriger ;
  4. le résultat des contrôles (citations, assembleur, non-régression, rendu) ;
  5. ce que vous n'avez pas pu faire, et pourquoi.
- Signalez seulement ce que les pièces établissent ou contredisent. Ne développez pas d'objections hypothétiques que ni les pièces ni la partie adverse ne soulèvent.
