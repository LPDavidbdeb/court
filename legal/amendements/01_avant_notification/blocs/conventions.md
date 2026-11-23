# Conventions de rédaction des blocs

*Version minimale du 23 novembre 2026. À lire avec `METHODE.md` avant de rédiger ou de modifier un bloc. Sauf mention contraire, les règles viennent des décisions du demandeur consignées au registre des précisions (numéro de l'entrée entre parenthèses). Une règle marquée **[proposition, non tranchée]** est une suggestion de Claude que le demandeur n'a pas adoptée : elle n'oblige pas et ne justifie aucune modification d'un bloc tant qu'elle n'est pas tranchée.*

## 1. Personnes et désignations

- **Le demandeur** : Louis-Philippe David. Ne jamais écrire « le défendeur » pour lui, sauf dans une citation de la requête de 2015.
- **Élise Ayoub** : « la défenderesse Élise Ayoub » à la première mention dans un bloc, puis « la défenderesse » ou « Élise Ayoub ». Pour ses actes et déclarations, son nom (P229).
- **Me Marie-Josée Ayoub** : « Me Marie-Josée Ayoub », puis « Me Ayoub ». Ne pas écrire « Mme Ayoub » (confusion avec Élise Ayoub) [proposition, non tranchée ; P422].
- **Règle par personne.** Me Ayoub n'a ni rédigé la requête de 2015 ni représenté sa sœur devant le tribunal (2013 à janvier 2016). Elle répond de ses propres écrits (courriel du 11 juin 2013 ; lettres de négociation de 2015), jamais de la requête ni de l'audience.
- Les enfants : Alexia, Nicolas.

## 2. Ce que le texte ne fait pas

- **Aucune qualification juridique ou morale.** Mots exclus du texte des blocs : « parjure », « calomnie », « mensonge », « manipulation », « tromperie », « gaslighting », « domination », « hostile », « agressif », « témérité », « chantage », « tricher », « mauvaise foi ». On décrit les actes et on juxtapose les pièces ; le tribunal conclut (P363, P365, P367, P386).
- **Pas de règle de droit affirmée sans validation.** Une référence législative ou jurisprudentielle n'entre dans un bloc que si elle est solide et utile ; sinon, en note, « à valider par un avocat » (P322).
- **Allégations de 2013 (décision du demandeur, P448).** Elles sont citées, et répétées chaque fois qu'une restriction des accès est exposée : l'objet de la demande n'est pas de récupérer la garde, mais d'exposer la situation qui a mené aux restrictions. À chaque mention : les mots exacts du courriel du 11 juin 2013 (`legal/piece_pdf-1.md`), leur autrice (Me Marie-Josée Ayoub) et leur destinataire (Élise Ayoub) ; le lien avec la restriction en cause ; le fait qu'elles n'ont été ni étayées ni retirées (aucune plainte, aucun signalement, aucune mesure de protection dans le plan). Ne pas plaider le fond au-delà de ces faits documentés. La proposition contraire de Claude (P438) est écartée.
- **« accès supervisés » [proposition, non tranchée].** Proposition de Claude (P428) : écrire « en présence de tiers », l'expression désignant en droit de la famille une mesure ordonnée en raison d'un risque.
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
- **Un fait par paragraphe (décision du demandeur, P461, 23 novembre 2026).** Chaque paragraphe numéroté énonce un seul fait (voir `legal/CLAUDE.md`, liste de faits, règle 1). La règle s'applique à tout bloc rédigé ou modifié à compter du 23 novembre 2026. Les blocs antérieurs seront découpés lors de la révision d'ensemble (objection O9).
- **Cotes (décision du demandeur, P467, 23 novembre 2026).** Les cotes de l'ancien régime (« P-__ », P113, cotes du dépôt de juillet) ne figurent pas dans le texte. Une pièce est désignée par le nom de sa fiche, qui sert de cote temporaire ; une pièce sans fiche, par son identifiant en base (Event, PhotoDocument). Les cotes de la requête de 2015 (P-2, P-4, P-5) restent, parce qu'elles sont citées. Les cotes définitives seront attribuées au bordereau à partir des noms de fiches, sans jamais recycler une cote du dépôt.
