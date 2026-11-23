# Consigne de revue contradictoire n° 1 — blocs des §§ 7 et 10, et ajout au bloc des §§ 19 à 35

*Rédigée le 23 novembre 2026. Destinataire : un agent qui n'a pas participé à la rédaction. Travail de fond, en lecture seule : vous êtes l'avocat de la partie adverse qui cherche la faille. Vous ne modifiez aucun fichier.*

## Contexte à lire d'abord

Branche : `fiches/email-16-portee-retrait` du dépôt `LPDavidbdeb/court`. Lisez, dans cet ordre :

1. `AGENTS.md` (racine) et `legal/CLAUDE.md` ;
2. `legal/amendements/01_avant_notification/blocs/METHODE.md` et `blocs/conventions.md` (en particulier la règle sur les allégations de 2013, décision du demandeur P448) ;
3. les textes à examiner :
   - `blocs/par07_duree_2011.md` (paragraphe 7 de la requête : la durée de la séparation de 2011) ;
   - `blocs/par10_rachat.md` (paragraphe 10 : le motif du rachat de la résidence) ;
   - dans `blocs/par19_35_acces_autorite.md`, le paragraphe `par19-circonstances-2013` et le paragraphe `par19-presence-tiers` ;
   - dans `blocs/par18_entente.md`, le paragraphe `par18-conclusion`.
4. Les pièces citées : chaque chemin entre accents graves dans ces paragraphes (`legal/piece_*.md`, `legal/allegation_62_separation_2011.md`). La requête de 2015 est `legal/piece_document-1.md`.

## Ce que vous devez chercher

Pour chaque paragraphe numéroté (avant le marqueur `<!-- fin-du-texte -->`) :

1. **Dérive de source.** L'énoncé dit-il plus que sa pièce ? Une pièce peut être forte pour une proposition et muette pour la suivante (`legal/CLAUDE.md`, liste de faits, règle 2). Citez la phrase et la pièce.
2. **Citations.** Chaque citation entre « » doit se trouver mot pour mot dans la pièce désignée, orthographe source comprise. Lancez `python3 legal/amendements/01_avant_notification/outils/verif_citations.py <bloc>` si vous avez un clone ; sinon, comparez à la main.
3. **Inférence présentée comme fait.** Repérez toute affirmation de cause, d'intention ou de connaissance qui n'est pas écrite dans une pièce. Une juxtaposition de dates est permise ; « en réponse à », « parce que » ne le sont que si une pièce le dit.
4. **Affirmations sur le dossier entier.** « Aucune pièce ne documente… », « les seules circonstances … qu'un écrit … ait énoncées » : dites ce qu'il faudrait vérifier, et où, pour que l'affirmation tienne.
5. **Meilleure objection.** Pour chaque bloc, rédigez l'objection la plus forte que la défense opposera, en une ou deux phrases, puis dites si le bloc y répond, et par quel paragraphe.
6. **Vocabulaire.** Toute qualification juridique ou morale (parjure, mensonge, manipulation, calomnie, mauvaise foi, etc.) est interdite dans le corps. Signalez-la.
7. **Concessions.** Le bloc concède-t-il ce qui est vrai (l'infidélité au § 7 ; le rachat au § 10 ; le séjour au 311, rue Riverside) ? Une concession manquante est une faille.
8. **Me Ayoub.** Elle n'a ni rédigé ni affirmé la requête de 2015. Signalez tout passage qui lui impute une omission dans la requête.

Points connus, à ne pas signaler comme nouveaux : les notes de rédaction de chaque bloc (PhotoDocuments d'Hydro-Québec sans fiche ; prix d'août 2014 retiré ; courriel à Me Pringle écarté pour le secret professionnel ; attribution de la seconde copie au témoignage). Vous pouvez en revanche dire qu'une note sous-estime un risque.

## Ce qui est interdit

- Modifier, créer ou supprimer un fichier ; ouvrir une branche ; écrire dans `legal/depots/`.
- Proposer de retirer les citations des allégations de 2013 : leur répétition est une décision du demandeur (P448). Vous pouvez signaler un écart entre une citation et sa pièce, ou un lien qui dépasse ce que dit la pièce.
- Inventer un fait ou une pièce.

## Compte rendu attendu

Un seul message, en français, structuré ainsi :

1. **Par bloc** (`par07`, `par10`, `par19-circonstances-2013` et `par19-presence-tiers`, `par18-conclusion`) : un tableau `étiquette | problème | pièce | gravité (bloquant / à corriger / mineur) | correction proposée`.
2. **Meilleure objection** par bloc, et la réponse du bloc (ou son absence).
3. **Citations** : résultat du contrôle (nombre vérifié, écarts).
4. **Ce que vous n'avez pas pu vérifier**, et pourquoi.

Soyez bref et précis ; ne reformulez pas les blocs.
