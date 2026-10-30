# Prompt — agent d'exécution de l'épic VA : recette du pilote, puis série 1

> **Projet rédigé par Claude le 29 oct. 2026 au soir, à relire par LP avant
> envoi.** Les décisions de la section 1 sont **celles que LP doit confirmer**.
> Une fois le message envoyé par LP, elles valent dictée, au même titre que
> `accords.json`. Biffer ou modifier toute ligne avec laquelle LP n'est pas
> d'accord.

---

## LE PROMPT

Branche `epic/E01-numerotation-concordance`. Ta revue d'exécution est faite
(`docs/verification_appuis/REVUE_EXECUTION.md`, « Revue du 29 oct. 2026
(soir) » et sa « Suite »). Lis-la d'abord.

**Cadre inchangé** :

- lecture seule de la base, par le socket local et en transactions READ ONLY ;
- aucun accès réseau ; **ne pousse pas**, la publication est faite depuis le
  poste de LP ;
- une story = un commit = un verdict ;
- chemins limités à `legal/verification_appuis/` et `docs/verification_appuis/`.

### 0. Un fait nouveau à intégrer avant tout

Le 29 oct. au soir, sur décision de LP, la ligne P-38 de `BordereauDepotJuillet`
(`id` 377) a été rattachée à l'**`Email` 4** (20 avril 2020), au lieu de l'`Email`
330. L'`Email` 4 reproduit le courriel du demandeur du 17 avril 2020 et contient
la réponse de Me Ayoub que citent le § 173 et les conclusions. Détail :
`legal/amendements/01_avant_notification/journal_modifications.md`, entrée du
29 octobre.

1. **VA01 réel** : produis un nouvel instantané (accord VA01 en vigueur, lecture
   seule). Conserve l'ancien.
2. **VA02** : constate et consigne que la seule différence avec l'instantané
   précédent est la ligne 377 (`object_id` 330 → 4 ; `source_ref`). Toute autre
   différence est un **arrêt**, à me rapporter.
3. **VA05** : régénère la fiche des liens qui pointent la ligne 377, avec le
   nouveau support et son empreinte.
4. **VA13** : la proposition du lien 472 doit passer **A_REVOIR**. Vérifie-le.

### 1. Recette du pilote VA16 — décisions de LP

Références à inscrire : « Message de LP du [date d'envoi] à l'agent
d'exécution de l'épic VA — recette du pilote ».

| Lien | Décision de LP |
|---|---|
| 468 — P-40 | **VALIDER** `VA16-L468-v1` |
| 469 — P-105 | **CORRIGER**, puis **VALIDER** la version corrigée. Seul le texte de l'écart DATE change, remplacé **mot pour mot** par le texte ci-dessous |
| 470 — P-34 | **VALIDER** `VA16-L470-v1` |
| 471 — P-37 | **VALIDER** `VA16-L471-v1` |
| 472 — P-38 | **REFAIRE** sur l'`Email` 4, en nouvelle proposition. Pas de décision maintenant |
| 473 — P-99.1 | **VALIDER** `VA16-L473-v1` |
| 474 — P-99.2 | **VALIDER** `VA16-L474-v1` |

**Texte de l'écart DATE du lien 469 (dicté) :**

> La pièce établit la communication de la dénonciation au demandeur le
> 25 juillet 2023. Elle reproduit aussi sa notification à la procureure du
> demandeur, Me Philémon, le 21 juillet 2023 à 16 h 49, sous un bordereau de
> l'article 134 C.p.c. L'énoncé du § 234 selon lequel la dénonciation a été
> « reçue par sa procureure » le 25 juillet 2023 est **contredit** par la pièce.
> La pièce ne prouve pas, à elle seule, l'absence de connaissance du demandeur
> avant le 25 juillet.

**Pour la nouvelle proposition du lien 472**, examine aussi deux points :

- le § 235 invoque P-38 pour « une entente qu'aucune partie ne reconnaît » :
  dis ce que la réponse de Me Ayoub établit à cet égard ;
- le courriel du demandeur dit « Il va être temps de finaliser notre entente » :
  dis si cela crée un écart de **SENS**.

### 2. Ajustements de grille issus du pilote — à consigner

Inscris-les au **journal des versions de l'épic** (v1.1), conformément au
troisième critère de VA16 :

1. **Auteur** : le vocabulaire devient « agent d'examen (CODEX, CLAUDE) · LP ».
   L'attribution CODEX est acceptée.
2. **Degré de l'écart** : chaque écart précise si la pièce **contredit**
   l'énoncé, l'**établit en le cadrant autrement**, ou **ne l'établit pas**. On
   n'écrit jamais « ne dit pas explicitement » quand la pièce dit le contraire.
3. **Contrôle d'attribution** : quand un paragraphe attribue des mots ou un fait
   à une pièce, vérifie que ces mots sont **dans la cote**. Sinon, cherche dans le
   même fil ou le même document où ils se trouvent, nomme l'objet (modèle et pk)
   et propose l'écart **IDENTITE_PIECE**. Cette règle vient du lien 472.

### 3. VA05 — liens 240 à 247 (P-58 à P-64), décision de LP

Ces cotes n'ont pas de natif : la transcription **est** la pièce
(méthodologie post-dépôt, § 9.2 b). LP accepte comme support de ces liens le
PDF `pieces_pdf/P-5x.pdf` / `P-6x.pdf`, **pages 2 et suivantes seulement**. La
page de garde de juillet est défectueuse, des caractères y étant remplacés par
« ? » (`legal/instance/communication_pieces.md` § 13.2), et elle n'est pas lue.
Consigne l'empreinte du fichier entier et la plage de pages lue. VA05 peut alors
passer PASS.

### 4. Série 1 — priorité 1, les 40 premiers liens

Après les §§ 0 à 3, examine les **40 premiers liens de priorité 1** de la liste
VA03 (`travail/travail.json`, ordre de la liste) : les paragraphes qui citent
P-19, P-40 ou P-42.

- Propositions seulement (PROPOSE), avec la grille ajustée du § 2.
- Dossier à valider sur le modèle du pilote :
  `legal/verification_appuis/serie_1/A_VALIDER_PAR_LP.md`.
- En tête de ce dossier, un tableau des seuls **écarts**, du plus grave au moins
  grave. LP lit d'abord ce qui contredit.
- **Arrête-toi après ces 40 liens.** Aucune autre série, ni VA14, VA17 ou phase 1.

### 5. Rapport attendu

Dans `REGISTRE_EXECUTION.md` :

- SHA par commit ;
- verdicts VA01 (nouvel instantané), VA02, VA05, VA13 et VA16 ;
- couverture après recette, avec le pourcentage validé sur le périmètre du
  pilote, qui doit être de 100 % si 472 est validé à la prochaine recette, sinon
  6 sur 7 ;
- nombre de propositions de la série 1 et nombre d'écarts par degré ;
- **rien n'est poussé**.
