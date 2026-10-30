# Revue de l'exécution de l'épic VA — par Claude

> Chaque story est jugée sur **son critère et son test** dans
> `EPIC_VA_Verification_appuis_depot.md`, vérifiés **dans le dépôt** (commits,
> fichiers, tests relancés), jamais sur le seul rapport de l'agent.

## VA01 — Instantané du constat · revue du 29 oct. 2026

**Verdict de l'agent** : BLOQUÉ (données réelles non autorisées), recette synthétique réussie.
**Mon verdict** : ✅ **conforme sur la partie synthétique ; BLOQUÉ à juste titre**
pour l'instantané réel. Deux réserves, à lever avant PASS.

### Ce que j'ai vérifié

| Point | Constat |
|---|---|
| Tests | relancés par moi : **3/3 OK**, avec le Python système et celui du `.venv`, `-W error::ResourceWarning` |
| Critère « deux générations identiques à l'octet » | couvert : `constat.json` et `SHA256SUMS` comparés à l'octet |
| Critère « numéro imprimé, jamais celui du `.md` » | couvert : le paragraphe de fixture `43` sort `41`, comme la concordance réelle (md 43 → imprimé 41) |
| Hypothèses du code sur les **données réelles** (lues par moi en lecture seule) | ✅ la concordance réelle a bien les champs `numero_md`, `numero_imprime`, `incipit` (198 lignes) ; les textes du doc 9 ne commencent pas par leur numéro, donc l'appariement par incipit fonctionne ; et `LibraryNode.paragraph_number` porte **déjà le numéro imprimé** (item 43 → `paragraph_number` 41), si bien que le contrôle croisé « numéro stocké » est cohérent avec la concordance |
| Protection des données réelles | sérieuse : accord écrit exigé **avant** toute connexion ; session et transaction PostgreSQL `READ ONLY` ; `ContentType.get`, jamais `get_for_model` (qui peut créer) |
| Écrasement | refusé si le contenu diffère ; sortie limitée à `legal/verification_appuis/` |
| Commits annexes `ed973f0` et `80913a0` | ne contiennent que l'outil d'extraction, ses manifestes et les réponses du 29 oct. : rien d'inattendu |

### Réserves

1. **Pas encore commité.** `legal/verification_appuis/` et
   `docs/verification_appuis/execution/` sont hors suivi. L'épic exige « une
   story = un commit = un verdict » : pas de PASS sans le commit, et son SHA au
   rapport.
2. **Le contrôle croisé du numéro stocké n'est pas testé.** La fixture ne
   porte pas de `numero_stocke` : le refus « numéro stocké divergent », qui
   protège précisément contre une erreur de numérotation, n'est jamais exercé.
   **Ajouter deux tests** : numéro stocké égal à l'imprimé → accepté ; numéro
   stocké différent → refus nommant l'énoncé.

Remarque, sans réserve : `--reel` refuse si les effectifs diffèrent de
287 / 515 / 268. C'est une garde d'ancrage défendable, puisque le constat est
figé ; le message le dit.

### Les deux questions de l'agent

- **Stories conditionnelles** : inclure VA08, VA09, VA10, VA15 — d'accord. VA08
  et VA09 sont les deux qui répondent à la question de LP. **Exclure VA14** est
  cohérent avec la proposition révisée (la relecture vient après l'ensemble).
  Conséquence à accepter : aucune synthèse avant que les 515 liens soient
  validés. VA14 pourra être ajoutée plus tard sans rien refaire. **Décision de
  LP.**
- **Lecture seule des données réelles pour VA01–VA17** : le mécanisme est sain.
  ⚠️ Le fichier d'accords `va-accords/1` est **la trace de l'autorisation de
  LP** : il doit être écrit **par LP**, ou dicté par lui mot pour mot, jamais
  rempli par l'agent de sa propre initiative (même principe que `--atteste`).

### Reprise — vérifiée le 29 oct. 2026

| Réserve | Levée ? | Vérification |
|---|---|---|
| 1. Commit de la story | ✅ | `97d6574` (code, tests, rapports) ; SHA inscrit au rapport par `0d6f470` ; arbre propre |
| 2. Contrôle du numéro stocké | ✅ | `test_numero_stocke_identique_a_limprime_accepte` et `test_numero_stocke_divergent_refuse_et_enonce_nomme` (message : « … pour l'énoncé 1 : 43 / 41 ») ; **5/5** relancés par moi, Python système et `.venv` |

**Verdict VA01 : PASS sur la recette synthétique ; BLOQUÉ pour l'instantané
réel**, dans l'attente de l'accord écrit de LP. Aucun fichier d'accords ni
aucune connexion réelle : vérifié. Les deux commits sont **locaux**, non poussés.

---

## Revue du 29 oct. 2026 (soir) — exécution jusqu'au pilote VA16

**Portée de cette revue.**

- **Conformité d'ensemble** : registre, commits, tests, arrêt au bon endroit.
- **Revue de fond des sept propositions du pilote**, contrôlées sur les pièces
  elles-mêmes.
- VA02 à VA15 n'ont **pas** été relus ligne à ligne.

### Conformité

| Point | Constat |
|---|---|
| Tests | **36/36 OK**, relancés par moi : `.venv/bin/python -B -W error::ResourceWarning -m unittest discover -s legal/verification_appuis/tests -t . -p 'test_va*.py'` |
| Une story = un commit | ✅ VA12 `7a15ff0`, VA13 `b3b29b8`, VA15 `98b2311`, VA16 `ecbe88b`, consolidation `1b42777` ; chemins limités à `legal/verification_appuis/` et `docs/verification_appuis/` |
| Fichiers de l'autre activité | ✅ aucun fichier de `legal/instance/` dans ces commits, y compris le renommage alors indexé |
| Arrêt | ✅ au pilote VA16, qui exige la recette de LP ; VA14 exclue (décision antérieure), VA17 et phase 1 non exécutées |
| VA05 BLOQUÉ | ✅ justifié : liens 240-247 vers P-58 à P-64, sans natif |
| Accords | `accords.json` présent (commit `feba45e`). **À confirmer par LP** : c'est bien sa dictée |
| Push | non fait (interdiction réseau contradictoire). Peut être fait par le superpush de ce poste |

**Écart de vocabulaire, à accepter ou refuser par LP.** L'épic fixe
**Auteur = CLAUDE · LP**. Le code écrit **CODEX** (`journal.py`,
`AUTEUR_AGENT = "CODEX"`). L'attribution est **exacte**, puisque c'est cet agent
qui a examiné. Mais elle sort du contrat. Proposition : amender le vocabulaire
de l'épic en « agent d'examen (CODEX, CLAUDE) · LP ».

**Critère VA16 « au moins une contribution limitée décrite comme telle »** : ✅
satisfait. On compte quatre ECLAIRE_SEULEMENT et trois EN_ETABLIT_UNE_PARTIE,
chacun avec ses limites écrites.

### Fond — les sept propositions, relues sur les pièces

| Lien | Proposition | Mon avis |
|---|---|---|
| 468 — P-40 | EN_ETABLIT_UNE_PARTIE | ✅ juste |
| 469 — P-105 | EN_ETABLIT_UNE_PARTIE + écart DATE | ✅ **l'écart est réel, et plus fort que formulé** — voir ci-dessous |
| 470 — P-34 | EN_ETABLIT_UNE_PARTIE | ✅ juste |
| 471 — P-37 | ECLAIRE_SEULEMENT | ✅ juste |
| 472 — P-38 | ECLAIRE_SEULEMENT | ⚠️ **incomplet** — voir ci-dessous |
| 473 — P-99.1 | ECLAIRE_SEULEMENT + SENS | ✅ juste : en mars 2020, le demandeur se dit encore locataire |
| 474 — P-99.2 | ECLAIRE_SEULEMENT + SENS | ✅ juste : bail renouvelé jusqu'au 30 juin 2021, relocation tentée pour juillet 2020 |

**🔴 Lien 469 — P-105 contredit le § 234 sur la réception par la procureure.**

- Le § 234 dit que la dénonciation « a été reçue par sa procureure et portée à
  sa connaissance le 25 juillet 2023 ».
- P-105 reproduit l'envoi de Me Ayoub à Me Philémon, « Avocate du demandeur »,
  daté du **21 juillet 2023, 16 h 49**. Il porte un bordereau qui énonce : « LA
  PRÉSENTE TRANSMISSION CONSTITUE UNE NOTIFICATION AU SENS DE L'ARTICLE 134 ».
- La pièce établit donc deux faits : une **notification à la procureure le
  21 juillet** et une **communication au demandeur le 25 juillet**.
- La proposition écrit que la pièce « ne dit pas explicitement reçu par la
  procureure le 25 ». C'est trop faible. Au regard de la grille (contredit /
  vrai mais cadré / non étayé), la réception par la procureure le 25 est
  **contredite** par la pièce elle-même.
- Conséquences, hors de la grille :
  1. la défense peut soutenir que la connaissance de l'avocate vaut celle du
     client, ce qui place le point de départ au 21 juillet, et le dépôt du
     24 juillet 2026 hors délai ;
  2. le § 234 contient une inexactitude que la défense peut opposer au
     demandeur, sur le terrain même des art. 51 et suivants.
- **À corriger dans la demande modifiée** : notification à la procureure le
  21 juillet ; connaissance personnelle du demandeur le 25 juillet. L'ancre
  plaidée est la connaissance **personnelle**.
- ⚠️ La jurisprudence sur l'imputation au client de la connaissance de son
  avocat est à réunir. Je n'en cite aucune de mémoire.

**⚠️ Lien 472 — P-38 ne contient pas la réponse que la demande lui attribue.**

- Le § 235 invoque P-38 pour « une entente qu'aucune partie ne reconnaît ». Le
  § 173 et une conclusion lui attribuent les mots de Me Ayoub : le jugement était
  « final » et « ne constituait pas une entente ».
- **La cote P-38 ne contient que le courriel du demandeur** (`Email` 330, 17 avril
  2020).
- La réponse de Me Ayoub est l'**`Email` 4** (20 avril 2020, même fil) : « Il y a
  eu un jugement final et non pas une entente. […] Je ne ferai aucun autre
  demande à la cour. » Elle **n'appartient pas** à la cote déposée. C'est un écart
  **IDENTITE_PIECE**.
- Le courriel du demandeur dit en outre « Il va être temps de finaliser notre
  entente ». La défense peut le lire contre l'allégation qu'« aucune partie ne
  reconnaît » l'entente. C'est un risque de **SENS**, que la proposition
  n'aborde pas.
- **Conséquence pratique** : communiquée telle quelle le 6 novembre, P-38
  n'appuie pas le § 173 ni la conclusion. Ajouter l'`Email` 4 à P-38 changerait
  l'identité d'une cote déposée (verrou des cotes). La voie propre est une
  **cote nouvelle**, au bordereau de la demande modifiée, ou une communication
  supplémentaire annoncée comme telle. **Décision de LP.**

### Verdict

- **Exécution conforme**, à un écart de vocabulaire près (CODEX).
- **VA16 reste BLOQUÉ** jusqu'à la recette de LP, ce qui est correct.
- **Recommandation pour la recette** :
  - valider 468, 470, 471, 473 et 474 ;
  - **corriger** 469 : écart DATE réécrit comme une contradiction sur la
    réception par la procureure ;
  - **corriger** 472 : écart IDENTITE_PIECE (`Email` 4 hors cote) et risque de
    SENS (« notre entente »).
- Ce sont les deux ajustements de grille que le pilote devait faire apparaître
  (VA16, critère 3).

### Suite — décision de LP sur P-38 (29 oct., soir)

- LP a fait rattacher P-38 à l'**`Email` 4**, qui reproduit le courriel du
  17 avril et contient la réponse de Me Ayoub. Ligne `BordereauDepotJuillet`
  377 : 330 → 4. Détail au journal des modifications.
- **Effets sur l'épic** : VA02 signalera la ligne modifiée, et c'est attendu.
  L'instantané VA01 est à reprendre avec l'accord de LP. La proposition du lien
  472 passe **A_REVOIR** et se refait sur l'`Email` 4.

---

## Revue du 30 oct. 2026 — reprise du pilote et série 1

**Conformité.**

- **45/45 tests OK**, relancés par moi.
- Les commits `bd4ad29`, `2316d9f`, `7b580bd`, `117d125`, `08e0440`, `b669584` et
  `92d3e34` restent tous dans `legal/verification_appuis/` et
  `docs/verification_appuis/`.
- L'arrêt après 40 liens est respecté.

**Pilote.**

- Le texte DATE de 469 est reproduit **mot pour mot** de la dictée ✅. Ses
  « Limites » d'origine restent en place, comme LP l'a voulu (« seul le texte de
  l'écart change »). Elles ne contredisent pas l'écart, puisque la phrase
  « Nous avons reçu » ne date pas la réception.
- **472-v2, sur l'`Email` 4 : juste, à valider tel quel.**
  - L'écart **SENS** est fondé : la réponse de Me Ayoub établit **sa** position
    (« jugement final et non pas une entente »), pas l'universel « aucune partie
    ne reconnaît ».
  - L'écart **IDENTITE_PIECE** est exact et honnête : il distingue le verrou du
    dépôt (`Email` 330) du rattachement corrigé (`Email` 4).

**Série 1 — 40 propositions.**

- Répartition : 1 ETABLIT_L_ENONCE, 21 EN_ETABLIT_UNE_PARTIE, 18
  ECLAIRE_SEULEMENT. Aucune contradiction.
- Les **4 écarts sont fondés**. Je les ai vérifiés sur les pages originales :

| Lien | § | Vérification | À reprendre dans la demande modifiée |
|---|---|---|---|
| 40 | 10-C | P-42 § 20 : « monsieur s'est démontré **en désaccord** avec une telle décision », et non « refusé d'accepter » | dire « s'était dit en désaccord avec la contribution envisagée » |
| 43 | 11-A | P-40 § 7 : les quatre cents offres ont été « mis[es] en preuve » **lors de l'audition du 4 novembre 2019** | dater le contenu rapporté (2019), réaffirmé sous serment en 2023 |
| 43 | 11-A | P-40 § 6 : « **Malgré les prétentions du demandeur** eu égard à sa précarité financière […] malgré sa perte importante de revenus » | P-40 **reconnaît la perte de revenus** et **qualifie de « prétentions »** la précarité |
| 273 | 97 | P-19 § 7 : « En 2011 […] séparées pendant un (1) an et ont été en thérapie. À ce moment il est ressorti… » | « ne précisait ni la date **précise**, ni l'auteur, ni les paroles exactes ». L'année et le cadre de la thérapie y sont |

- **Recommandation** : valider les 40 propositions telles quelles. Les quatre
  écarts s'ajoutent à la liste des rectifications de la demande modifiée, avec
  le § 234 (P-105) et le § 173 (P-38).

### Lecture par paragraphe des 47 liens examinés — 30 oct. (question de LP : la pièce appuie-t-elle ce que le paragraphe affirme ?)

- **14 paragraphes entièrement examinés** : 1 établi, 10 en partie, 3 « éclaire
  seulement ». § 97 est partiellement examiné (P-66.5 à P-66.14 restent à voir).
- **Les trois « éclaire seulement » sont des paragraphes de thèse, pas de faits.**
  § 9-F : « Le demandeur soutient… » ; § 9-G : « invoque ainsi… comme noyau
  documentaire du patron allégué » ; § 11 : « allègue qu'en 2023, la dénonciation
  P-40 a renouvelé la substitution ». Une pièce ne peut pas établir une
  interprétation. **Ce n'est pas un défaut d'appui.**
- **Le signal réel est dans les « en partie » et dans les écarts : le paragraphe
  dit un peu plus que la pièce.**
  - « refusé » au lieu d'« en désaccord » (§ 10-C) ;
  - « reconnaissait la précarité » au lieu de « prétentions » (§ 11-A) ;
  - « ni date ni circonstances » (§ 97) ;
  - « aucune partie ne reconnaît » (§ 235) ;
  - « reçue par sa procureure le 25 » (§ 234).

  C'est la règle 2 de `legal/CLAUDE.md` : « Aucun énoncé ne dépasse sa source ».
  Le remède est la règle 5 : rétrograder l'énoncé au niveau prouvé.
- **Lacune de la grille, à corriger** : elle ne distingue pas la **nature du
  paragraphe**. Ajustement proposé :
  1. classer chaque paragraphe **FAIT**, **THÈSE** (interprétation, inférence,
     qualification) ou **MIXTE** ;
  2. ne signaler comme manque d'appui qu'un paragraphe FAIT, ou la partie
     factuelle d'un MIXTE, dont aucune pièce n'établit l'énoncé ;
  3. pour un paragraphe THÈSE, vérifier plutôt qu'il repose sur des paragraphes
     FAIT appuyés.

  C'est le travail de **VA14 (relecture par paragraphe)**, exclue jusqu'ici.
  C'est elle qui répond directement à la question de LP. **À réintégrer**, pour
  les paragraphes dont tous les liens sont validés.
