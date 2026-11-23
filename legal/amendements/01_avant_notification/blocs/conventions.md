# Conventions de rédaction des blocs

*Version minimale du 23 novembre 2026. À lire avec `METHODE.md` avant de rédiger ou de modifier un bloc. Les règles viennent des décisions du demandeur consignées au registre des précisions ; le numéro de l'entrée est donné entre parenthèses quand il existe.*

## 1. Personnes et désignations

- **Le demandeur** : Louis-Philippe David. Ne jamais écrire « le défendeur » pour lui, sauf dans une citation de la requête de 2015.
- **Élise Ayoub** : « la défenderesse Élise Ayoub » à la première mention dans un bloc, puis « la défenderesse » ou « Élise Ayoub ». Pour ses actes et déclarations, son nom (P229).
- **Me Marie-Josée Ayoub** : « Me Marie-Josée Ayoub », puis « Me Ayoub ». Ne jamais écrire « Mme Ayoub » (confusion avec Élise Ayoub).
- **Règle par personne.** Me Ayoub n'a ni rédigé la requête de 2015 ni représenté sa sœur devant le tribunal (2013 à janvier 2016). Elle répond de ses propres écrits (courriel du 11 juin 2013 ; lettres de négociation de 2015), jamais de la requête ni de l'audience.
- Les enfants : Alexia, Nicolas.

## 2. Ce que le texte ne fait pas

- **Aucune qualification juridique ou morale.** Mots exclus du texte des blocs : « parjure », « calomnie », « mensonge », « manipulation », « tromperie », « gaslighting », « domination », « hostile », « agressif », « témérité », « chantage », « tricher », « mauvaise foi ». On décrit les actes et on juxtapose les pièces ; le tribunal conclut (P363, P365, P367, P386).
- **Pas de règle de droit affirmée sans validation.** Une référence législative ou jurisprudentielle n'entre dans un bloc que si elle est solide et utile ; sinon, en note, « à valider par un avocat » (P322).
- **Allégations de 2013.** Ne pas les citer, ni en discuter le fond ; les mentionner comme des allégations ni étayées ni retirées (P438).
- **« accès supervisés »** : jamais. Écrire « en présence de tiers » (P428, P429).
- **Pas de présomption légale** quant au régime de garde (P359) ; écrire « le poids du statu quo ».
- **Pas de reproche professionnel** aux tiers (psychologue, avocats du demandeur).

## 3. Dates et fenêtre de preuve

- Ce que la défenderesse savait s'apprécie **au 19 novembre 2015** (assermentation), pour les faits survenus depuis le départ du demandeur (23 février 2015) (P315).
- **Le 14 janvier 2016** (audience, jugement rendu en l'absence du demandeur) est une seconde date : celle de la présentation au tribunal (P370).
- Les écrits de 2016 et de 2020 **éclairent la conception**, ils ne prouvent pas les faits de 2015 (P358). À placer en note ou en annexe, sauf décision contraire.

## 4. Citations et pièces

- **Orthographe source**, sans correction ni « [sic] ». « […] » pour une coupure ; crochets pour un ajout éditorial.
- Toute citation doit se retrouver dans une fiche `piece_*.md` (`outils/verif_citations.py`). Une source hors corpus (courriel Gmail non versé, par exemple) est signalée en note.
- Pièces désignées par le chemin de leur fiche, entre accents graves : (`legal/piece_pdf-3.md`). Les cotes seront substituées à l'assemblage. Ne jamais recycler une cote.
- **Secret professionnel.** Les courriels du demandeur à ses avocats (Me Poirier, Me Pringle) ne sont pas cités sans sa décision de renoncer au secret.
- **Négociation.** Les lettres « Sous toutes réserves » peuvent être citées dans les blocs, mais leur production reste à valider par un avocat (note dans le bloc).

## 5. Forme

- Phrases courtes ; un paragraphe numéroté = une idée.
- Concéder d'abord ce qui est exact, puis contester ce qui ne l'est pas.
- Présenter une inférence comme telle (« en découle par élimination », « le rapprochement repose sur… »).
- Les paragraphes de la requête de 2015 s'écrivent en toutes lettres (« paragraphe 20 de la requête ») ; les renvois internes passent par des étiquettes (`METHODE.md`, § 4).
