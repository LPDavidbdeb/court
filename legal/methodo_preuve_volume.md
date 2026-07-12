# Méthodologie — présenter une preuve qui repose sur le VOLUME (densité + étalement)

> **Quand l'appliquer.** Chaque fois que la démonstration repose non sur une pièce isolée mais sur le **volume** : densité + étalement sur toute la période + les deux enfants + plusieurs dimensions. Cas type : réfuter une allégation **vague et structurelle** (« rarement disponible », « difficulté à assumer son rôle de père », « s'occupait minimalement »). Complète la règle #7 de [CLAUDE.md](CLAUDE.md) (allégation structurelle → volume distribué) en y ajoutant le **mécanisme de production procédural**.

---

## Le principe
Contre une allégation **vague/structurelle**, aucune pièce isolée ne convainc (l'adversaire répond « exception »). C'est la **distribution** qui réfute — densité + étalement sur toute la période, les deux enfants, plusieurs dimensions. Fondement : **proportionnalité (art. 18 C.p.c.)** — *la largeur de la réponse égale la largeur de l'accusation.*

## Les trois couches

**① Exposé des faits — un fait de *densité* (un seul paragraphe par axe).**
> Ex. : « Entre 2010 et 2014, le demandeur a accompagné l'un ou l'autre des enfants à au moins **47 sorties** documentées par photographies horodatées (P-X, **en liasse**). »

→ **Pas N paragraphes** pour N événements. Un fait de densité par axe (cf. document_de_faits, faits C11, C12, C13).

**② Agrégation — un *tableau récapitulatif* produit comme pièce.**
Tableau chronologique **neutre** : **date | lieu | enfant(s) | description | réf.**. C'est le **résumé digestible** présenté au juge. En droit québécois, un **tableau-synthèse de documents volumineux** est admissible pour assister le tribunal, **à condition que les documents sous-jacents soient produits**.

**③ Photos — produites *en liasse* sous une seule cote (le substrat vérifiable).**
Produites (sur support / en liasse ; **art. 2855 C.c.Q.** — documents technologiques horodatés), **disponibles pour vérification et contre-interrogatoire**, mais le juge n'a **pas** à les examiner une à une. Elles **corroborent** ; elles ne sont pas plaidées individuellement.

## La distinction-clé : *produire* ≠ *plaider*
- On **produit** les photos (en liasse) — le **substrat**.
- On **plaide** l'agrégation (le fait de densité + le tableau) — la **démonstration**.

## Le verrou de calibration (à ne jamais rater)
L'agrégation **doit elle-même être vérifiable** : chaque ligne du tableau renvoie à un Event/photo **réellement produit**. Sinon on commet le péché exact qu'on reproche au formulaire de pension ([these_revenu_mere_verifiabilite.md](these_revenu_mere_verifiabilite.md)) — un résumé qu'on ne peut reconstituer depuis les pièces transmises. *Notre résumé doit être adossé à son substrat.*
- Tableau **art. 99** : descriptions factuelles, **zéro qualificatif**, chaque ligne sourcée.
- Fait de densité **calibré** : réfute « rarement/minimalement », **n'overclaime pas** l'égalité (≈ 40-46 % concédé).

## Le moteur : le modèle `Event`
Tout étant dans la base (`Event` + photos liées), le **tableau récapitulatif se génère automatiquement** depuis la DB (date · lieu · enfants · description · Event id · présence de photo) — la DB garantit exhaustivité et exactitude. C'est l'exhibit (couche ②) qui adosse les faits de densité.

---

## Gabarit d'application (par axe)
1. Écrire **un** fait de densité dans l'exposé (« au moins N… P-X en liasse »).
2. Générer le **tableau** depuis `Event` (P-X) — neutre, sourcé.
3. Produire les **photos en liasse** (même cote P-X ou P-X-bis).
4. Vérifier le **verrou** : chaque ligne ↔ une pièce produite.

*Voir aussi : [[feedback_evidentiary_calibration]] ; règle #7 de CLAUDE.md.*
