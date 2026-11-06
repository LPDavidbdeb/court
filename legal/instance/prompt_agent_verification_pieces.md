# Prompt — agent chargé de la vérification indépendante des pièces à communiquer

> Spécification destinée à un agent qui n'a pas suivi la conversation. Rédigée le
> 1er nov. 2026, à la demande du demandeur : « propose-moi un script qui va
> permettre à un agent d'IA de faire une vérification indépendante ».

## Avant d'envoyer — ce qui a été choisi, et pourquoi

*(Cette section s'adresse au demandeur. Elle ne fait pas partie du prompt.)*

1. **L'agent écrit ses propres contrôles.** Il ne réutilise ni
   `extraire_pieces.py`, ni `rendre_pieces.py`, ni `index_pieces.py`, ni le
   `manifeste.json`. Ces outils et ce manifeste sont **l'objet** de la
   vérification. Un contrôle qui les réemploierait reproduirait leurs erreurs au
   lieu de les trouver. Le prompt décrit donc **quoi** vérifier et **contre quoi**,
   jamais **comment** l'extraction a été faite.
2. **Il ne lit pas mes conclusions avant d'avoir conclu.** `communication_pieces.md`
   (§§ 13-19) ne lui sert qu'**après** les tests, pour classer un constat comme
   « déjà connu ». Seule la liste fermée des décisions postérieures au dépôt
   (§ 2 du prompt) lui est donnée d'avance : ce sont des faits, pas des
   conclusions.
3. **Lecture seule partout.** Base, stockage, dépôt Git, dossier des pièces,
   export Takeout. Il n'écrit que dans son propre dossier de sortie, hors du
   dépôt. Lancer l'agent vaut autorisation de lire la **base réelle** dans ce
   périmètre, et de rien d'autre.
4. **Le contrôle par l'API Gmail est désactivé par défaut** (§ 4, G-5). Il
   comparerait chaque `.eml` à l'original de Google, ce qui est le contrôle
   d'intégrité le plus fort pour les courriels. Mais il utilise ton jeton
   d'accès. Active-le en remplaçant « désactivé » par « autorisé » au § 4.
5. **Quand le lancer.** Dès maintenant, sur ce qui est prêt : les fichiers
   natifs, P-58 à P-64 et l'index. **Une seconde fois** quand les rendus des
   courriels existeront (§ 5, C-4), sur la livraison complète, juste avant
   l'envoi.

6. **Second passage (mis à jour le 1er nov., après le premier rapport)** :
   - le § 2 liste maintenant les quatre enveloppes `PhotoDocument`, que le
     premier passage avait signalées faute de les y trouver ;
   - le dossier des **rendus** est ajouté à l'objet sous test (C-4 détaillé) ;
   - les constats du premier passage dont LP a pris connaissance sont nommés
     au § 7, pour être classés « connus ».

---

## LE PROMPT

Tu fais une **vérification indépendante** d'une livraison de pièces dans un
dossier judiciaire réel (Cour supérieure, district de Longueuil, n°
505-17-016235-261). Le demandeur, qui se représente seul, doit communiquer ces
pièces aux défenderesses le **6 novembre 2026**. Ce qui est communiqué doit
correspondre **exactement** au bordereau déposé au greffe le 24 juillet 2026,
sauf les décisions postérieures listées au § 2.

Ton rôle est de **trouver les erreurs**, pas de confirmer que tout va bien. Un
test qui ne peut pas échouer ne prouve rien : tu démontres que chacun de tes
contrôles sait échouer (§ 6).

### 0. Cadre

- **Projet** : Django (`mysite`), base PostgreSQL. Racine :
  `/Users/Louis-Philippe/Documents/GitHub/court`. Interpréteur : `.venv/bin/python`.
  Pour lire la base, utilise `manage.py shell`, ou un script qui appelle
  `django.setup()` avec `DJANGO_SETTINGS_MODULE=mysite.settings`.
- **Lecture seule, sans exception.** Au début de chaque session de base,
  exécute `SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY`. N'appelle
  jamais `save()`, `create()`, `update()` ou `delete()`. Ne modifie aucun
  fichier du dépôt, du stockage, de l'export ni du dossier des pièces. Ne
  committe rien.
- **Sortie** : un dossier neuf,
  `~/Documents/Verification_pieces_505-17-016235-261_<AAAA-MM-JJ_HHMM>/`. Il
  contient tes scripts, leurs sorties brutes, `rapport.md` et `resultats.json`.
- **Interdits** :
  - importer ou exécuter quoi que ce soit sous `legal/instance/outils/` ;
  - tenir `manifeste.json` ou `manifeste.md` pour vrais (tu les testes, § 5,
    C-5) ;
  - lire `legal/instance/communication_pieces.md` avant d'avoir terminé tous
    les tests (§ 7).
- **Lis le code des modèles avant d'écrire une requête.** N'invente aucun nom de
  champ.

### 1. Les références, par ordre d'autorité

| # | Référence | Chemin | Rôle |
|---|---|---|---|
| R1 | **Bordereau déposé** | `legal/depots/2026-07-24_initial/candidats/bordereau_bloc_depot.md` | La liste des cotes (106 lignes `- **P-n** — date — description ;`) et la table des sous-cotes (159 lignes `\| P-n.k \| date \| source interne \| description \|`). Le Markdown écrit certains caractères en entités HTML (`&lt;`) : décode-les. Les `**` marquent du gras. |
| R2 | **Verrou des cotes au dépôt** | `legal/depots/2026-07-24_initial/cotes.lock.json` | La source de chaque cote **au 24 juillet** (`source_resolue`, `identites_attendues`). |
| R3 | **Décisions postérieures** | § 2 ci-dessous, et `legal/amendements/01_avant_notification/journal_modifications.md` | Les seuls écarts permis par rapport à R2. |
| R4 | **La base** | modèle `case_manager.BordereauDepotJuillet` et les objets qu'il désigne (`content_type`, `object_id`) | Ce qui est rattaché aujourd'hui à chaque cote. |
| R5 | **Les originaux** | les fichiers désignés par la base (champs de fichier ou chemins des modèles `Email`, `Photo`, `PDFDocument`, `Document`), sous `storage/` ou ailleurs | Ce dont chaque fichier livré doit être la copie exacte. |
| R6 | **L'export Google Takeout** | `/Users/Louis-Philippe/Library/Mobile Documents/com~apple~CloudDocs/chat gpt lega brief/Requete Elise/eta de la relation/Elise/messages.json` | La source de P-58 à P-64 (`googlechat_manager.ChatSequence`). |
| R7 | **La demande déposée** | `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.md` | Les cotes citées par l'acte. |

Le répertoire `legal/depots/2026-07-24_initial/` est **gelé** : lecture seule.

**L'objet sous test** : `~/Documents/Pieces_505-17-016235-261_2026-11-06/`.
- Fichiers des pièces : `P-n.ext`, `P-n.k.ext`, ou un dossier `P-n/` contenant
  `P-n-01.ext`, etc.
- `SHA256SUMS`.
- `00_Index_des_pieces.pdf` : l'index qui sera transmis.
- `manifeste.json` et `manifeste.md` : registres internes, qui **ne seront pas
  transmis**.

**Second objet sous test : les rendus lisibles**,
`~/Documents/Rendus_505-17-016235-261_2026-11-06_tirage_2026-11-04/` :
- 105 PDF, un par cote (P-86 exclue), 869 pages au total ;
- `SHA256SUMS` et `manifeste_rendus.json`.

⚠️ Un dossier `~/Documents/Rendus_505-17-016235-261_2026-11-06/` subsiste : c'est
le tirage **du 3 novembre**, périmé, qui ne doit pas être testé. Le tirage à
tester est celui dont le nom porte `_tirage_2026-11-04`.

Ils sont produits par `legal/instance/outils/rendre_pieces.py` à partir du seul
dossier des pièces. Ils serviront de copie de lecture et de base à la version
imprimée pour le greffe. **Le natif fait foi.**

**Troisième objet sous test : le dossier qui part réellement**,
`~/Documents/Envoi_505-17-016235-261_2026-11-06/`. C'est un clone du dossier des
pièces dont **trois fichiers ont été retirés** à l'emballage : `.DS_Store`,
`manifeste.json`, `manifeste.md`. Attendu : il contient **exactement** les
fichiers des pièces de `SHA256SUMS`, plus `SHA256SUMS` et
`00_Index_des_pieces.pdf`, et rien d'autre ; chaque fichier est **identique
octet pour octet** à son homologue du dossier des pièces ; aucun `.DS_Store` à
aucune profondeur. Tout autre écart entre les deux dossiers est un constat
bloquant.

Les copies de lecture attendent une décision du demandeur et se trouvent hors du
dossier d'envoi, dans
`~/Documents/Envoi_505-17-016235-261_2026-11-06_EN_ATTENTE_copies_de_lecture/Copies_de_lecture/`
(les 105 PDF du tirage du 4 novembre et leur `SHA256SUMS`, sans
`manifeste_rendus.json`). Attendu : identiques octet pour octet au second objet
sous test.

### 2. Les décisions postérieures au dépôt — liste fermée

Tout écart par rapport à R2 qui ne figure pas ici est un **constat bloquant**.

| Cote | Décision | Date | Attendu dans la livraison |
|---|---|---|---|
| P-86 | retirée | 26 oct. | aucun fichier ; l'index porte « Non communiquée : le demandeur retire cette pièce. » |
| P-38 | rattachée à l'`Email` 4 au lieu de l'`Email` 330 | 29 oct. | `P-38.eml` = copie exacte de l'original de l'`Email` 4 |
| P-22 | `Email` 267 ajouté (P-22.5) | 31 oct. | cinq courriels (`Email` 6, 8, 295, 306, 267) |
| P-20 | `Email` 237 ajouté (P-20.2), avec sa pièce jointe `image.png` | 1er nov. | `P-20.eml` (`Email` 16) et `P-20.2.eml` (`Email` 237) |
| P-58 à P-64 | rendues en PDF à partir de R6, mêmes messages que les séquences de la base | 1er nov. | un PDF par cote (§ 4, G-6) |
| **P-28** | **masquage du numéro d'assurance sociale** de la défenderesse Élise sur son TP-1 2018 | **4 nov.** | **le fichier livré n'est PAS identique à l'original de R5** : `P-28.jpg` est une copie dérivée où le numéro seul est couvert d'un rectangle noir, le libellé « NAS » restant visible. Attendu : mêmes dimensions, même `DateTimeOriginal` (2019:12:31 12:03:00), mêmes tables de quantification JPEG que l'original ; hors du masque, aucun écart de pixel supérieur à 3/255 ; **aucun chiffre du numéro lisible** par OCR, et le numéro n'apparaît nulle part ailleurs sur la page. Le masquage doit être **déclaré** à trois endroits : le bloc `caviardage` de `manifeste.json`, la ligne de P-28 dans l'index (« — numéro d'assurance sociale masqué »), et la page de garde de son rendu. **L'absence de l'une de ces trois mentions est un constat bloquant**, de même que tout écart hors du masque. L'original non masqué (`ac0f6e0c…`, 870 275 octets) ne doit **pas** se trouver dans le dossier des pièces ni dans le dossier d'envoi |
| P-1, P-8, P-15, P-101 | `Photo` du verrou → `PhotoDocument` qui l'enveloppe (respectivement 14, 3, 9, 12) | 29 oct. (`legal/instance/outils/README_extraction_pieces.md`, « Les quatre redirections sont des enveloppes ») | **la même photographie**, octet pour octet ; tout autre contenu est un constat |

### 3. Tests d'intégralité — tout ce qui est annoncé est livré, et rien d'autre

| ID | Test | Attendu |
|---|---|---|
| I-1 | Chaque cote de R1 a au moins un fichier livré | 105 cotes sur 106 ; seule P-86 n'en a pas |
| I-2 | Chaque sous-cote de la table de R1 a son ou ses fichiers | 159 sur 159 |
| I-3 | **Composition** : pour chaque ligne de R4, détermine **toi-même**, à partir des modèles, quels fichiers constituent l'objet (un courriel, tous les courriels d'un fil, toutes les photos d'un événement…). Compare à ce qui est livré : nombre de fichiers et identité, par empreinte contre R5. | égalité pour chaque cote |
| I-4 | **Écarts au dépôt** : compare R4 à R2, cote par cote | seuls les écarts du § 2 |
| I-5 | Quand une description de R1 annonce un nombre (« liasse de 14 courriels », « 19 courriels »), compte les fichiers livrés | égalité, sinon réserve |
| I-6 | **Aucun fichier orphelin** : tout fichier du dossier appartient à une cote de R1, ou est l'un des quatre fichiers de service (`SHA256SUMS`, `00_Index_des_pieces.pdf`, `manifeste.json`, `manifeste.md`). Fichiers cachés (`.DS_Store`) et temporaires compris. | 0 orphelin |
| I-7 | `SHA256SUMS` liste chaque fichier de pièce une fois et une seule, et rien d'autre | égalité stricte des ensembles |
| I-8 | Chaque cote citée par R7 (`P-n`, `P-n.k`) a ses fichiers | toutes, P-86 exceptée si elle est citée (à signaler) |
| I-9 | **P-58 à P-64** : chaque message de la `ChatSequence` rattachée (R4) figure dans le PDF, et le PDF n'en contient pas d'autre | égalité des ensembles d'identifiants (`message_id`) |

### 4. Tests d'intégrité — chaque fichier est exactement l'original

| ID | Test | Attendu |
|---|---|---|
| G-1 | Recalcule le SHA-256 de chaque fichier et compare à `SHA256SUMS` | 0 écart |
| G-2 | **Copie = original** : SHA-256 et taille de chaque fichier livré, comparés à l'original de R5, que tu résous toi-même depuis la base | 0 écart. Si la base désigne deux originaux différents pour un même objet (champ de fichier et chemin), c'est un constat. |
| G-3 | Chaque fichier s'ouvre dans son format : `.eml` analysable (`email`, `policy.default`), PDF lisible et non chiffré, JPEG décodable | 0 échec |
| G-4 | **Courriels** : `Date`, `From` et `Message-ID` présents ; la date et l'expéditeur concordent avec l'`Email` de la base | 0 écart, sinon réserve motivée |
| G-5 | *(désactivé — voir l'en-tête)* Pour chaque courriel issu de Gmail, l'original brut (`format=raw`) obtenu par l'API est identique au `.eml` livré | 0 écart |
| G-6 | **P-58 à P-64**, contre R6. Pour chaque message rendu : texte identique **au caractère près** (un émoji peut être remplacé par le marqueur visible `[U+XXXX]`) ; expéditeur ; heure = `created_date` UTC convertie en `America/Montreal` ; date du jour exacte. Dans l'annexe : horodatage UTC et `message_id` identiques à R6. Sur la page de garde : l'empreinte annoncée de R6 = l'empreinte que tu calcules. | 0 écart |
| G-7 | **Photographies** : lis `DateTimeOriginal` dans chaque JPEG livré et compare-le aux dates de la cote ou sous-cote dans R1 | informatif ; une date hors de la période annoncée est une **réserve** |
| G-8 | Aucun caractère de remplacement (U+FFFD), et aucun « ? » substitué à un caractère de la source, dans les PDF produits pour la livraison (index, P-58 à P-64) | 0 |

### 5. Tests de conformité des documents produits

| ID | Test | Attendu |
|---|---|---|
| C-1 | **Index = bordereau** : pour chaque cote et sous-cote, la date et la description de l'index sont identiques à R1, au caractère près (entités décodées, `**` retirés ; les sauts de ligne du PDF ne comptent pas) | 0 écart |
| C-2 | **Index = dossier** : les fichiers nommés sous chaque cote sont exactement ceux du dossier. Pour une liasse d'images résumée sur une ligne (« n images, X à Y »), n, X et Y sont exacts. Le nombre de pages annoncé pour chaque PDF est exact. | 0 écart |
| C-3 | **Index = en-têtes** : pour chaque courriel, la date (heure de Montréal), l'expéditeur, le destinataire, l'objet et les pièces jointes de l'index concordent avec le `.eml` | 0 écart |
| C-4 | **Rendus** (second objet sous test), pour chaque cote : <br>a) **page de garde** : cote, date et description = R1 au caractère près ; la liste des fichiers = les fichiers de la cote dans le dossier des pièces, chacun avec son empreinte **réelle** ; <br>b) **courriels** : les en-têtes (De, À, Cc, Date, Objet) et **chaque ligne** du corps du `.eml` se retrouvent dans le rendu, **dans l'ordre**, sans rien de tronqué ni de coupé en marge ; **toutes** les pièces jointes du `.eml`, à n'importe quelle profondeur de la structure MIME, sont listées, et chaque PDF ou image joint y est reproduit (pages du PDF, image) ; <br>c) **photographies** : une image rendue par fichier de la cote ; <br>d) **PDF** : même nombre de pages que le natif (une copie allégée à 150 ppp est permise et déclarée sur la page de garde) ; <br>e) **P-58 à P-64** : le rendu est **identique octet pour octet** au PDF du dossier des pièces ; <br>f) `SHA256SUMS` des rendus exact et complet | 0 écart |
| C-5 | **Manifeste interne** : `manifeste.json` concorde-t-il avec le dossier (fichiers, empreintes, décomptes) ? | informatif. Ses descriptions viennent de la base et diffèrent de R1 : c'est connu, et c'est pourquoi il n'est pas transmis. |

### 6. Tests d'hygiène, et preuve que tes contrôles savent échouer

| ID | Test | Attendu |
|---|---|---|
| H-1 | **Doublons** : fichiers d'empreinte identique, dans une même cote ou entre deux cotes | liste ; réserve |
| H-2 | **Renseignements personnels** : cherche dans le texte des PDF et des corps de courriels les numéros d'assurance sociale (9 chiffres, groupés ou non, **valides selon Luhn**) | liste ; réserve |
| H-3 | **Fichiers de service** : signale ceux qui ne doivent pas partir (`manifeste.*`, fichiers cachés) | liste |
| H-4 | **Volume** : taille totale, nombre de fichiers, les dix plus gros | informatif (envoi par Google Drive) |
| S-1 | **Sensibilité.** Sur une **copie** du dossier dans ton dossier de sortie, provoque une à une les fautes suivantes et montre que le bon test échoue : un octet modifié dans un `.eml` et dans un JPEG (G-1, G-2) ; un fichier supprimé (I-1 ou I-2) ; un fichier orphelin ajouté (I-6) ; une ligne retirée de `SHA256SUMS` (I-7) ; un mot changé dans une description de l'index rendu en texte (C-1) ; un message retiré du texte de P-62 (G-6, I-9) | chaque faute est détectée par le test prévu |

### 7. Classer les constats

1. Termine **tous** les tests.
2. Lis ensuite `legal/instance/communication_pieces.md` (§§ 13 à 19) et
   `legal/amendements/01_avant_notification/journal_modifications.md`.
3. Marque chaque constat **connu** (déjà relevé, avec sa référence) ou
   **nouveau**.
4. Ne retire rien : un constat connu reste un constat.

Défauts déjà relevés, pour mémoire. Vérifie-les : ne les présume pas.
- P-45.2 (photos sans rapport) ;
- doublons dans P-24, P-55, P-66 et P-70 ;
- dates EXIF de P-55 et P-80 ;
- annotations de P-91 ;
- NAS lisible sur P-28 ;
- P-104 « interne » ;
- P-33 incomplète (4 pages sur 8) ;
- dates du bordereau pour P-58 et P-59 (« août 2014 ») ;
- P-38 datée au bordereau du 17 avril, fichier du 20 avril.
- **Constats du premier passage (rapport du 1er nov., 12 h 03), connus de LP**,
  à classer « connus » s'ils réapparaissent (`communication_pieces.md` § 22) :
  - `.DS_Store` : fichier de service, exclu à l'emballage (H-3, pas un orphelin) ;
  - P-62, message 40 : deux espaces finales non reproduites dans le PDF ;
    décision de LP en attente ;
  - G-4 : écarts entre la base et les en-têtes de P-4, P-10, P-24, P-70
    (messages connus seulement par citation, rattachés en base à la réponse) ;
  - G-7 : dates EXIF de P-13, P-28 et P-91 (photographies de documents) ;
  - doublons de P-4 (P-4-02/03, P-4-04/05).
  - **Corrigé depuis** : le point final de P-104 et P-106 dans l'index (index
    régénéré le 1er nov.). Il doit maintenant concorder (C-1).

### 8. Critères de succès et verdict

| Niveau | Définition | Exemples |
|---|---|---|
| **Bloquant** | La livraison ne peut pas partir en l'état | toute empreinte fausse (G-1, G-2) ; une cote ou sous-cote annoncée sans fichier (I-1, I-2) ; une composition différente de la base (I-3) ; un écart au dépôt hors du § 2 (I-4) ; un orphelin (I-6) ; `SHA256SUMS` incomplet (I-7) ; un fichier illisible (G-3) ; un message de clavardage faux ou manquant (G-6, I-9) ; une description de l'index différente du bordereau (C-1) ; l'index qui nomme un fichier absent ou en omet un (C-2) ; un test de sensibilité non détecté (S-1) |
| **Réserve** | Peut partir, mais le demandeur doit trancher en connaissance de cause | défauts de contenu (§ 7) ; nombre annoncé ≠ nombre livré (I-5) ; date EXIF hors période (G-7) ; doublons (H-1) ; NAS (H-2) ; écart d'en-tête (G-4, C-3) |
| **Information** | Aucune action requise | volumes, statistiques, C-5 |

**Verdict**, en une ligne en tête du rapport :
- **CONFORME** : 0 bloquant, 0 réserve nouvelle ;
- **CONFORME AVEC RÉSERVES** : 0 bloquant, au moins une réserve ;
- **NON CONFORME** : au moins un bloquant.

### 9. Le rapport

Deux fichiers dans ton dossier de sortie.

**`rapport.md`**, dans cet ordre :

1. **Verdict** : une ligne, puis le compte des constats bloquants, des réserves
   (nouvelles / connues) et des informations.
2. **Périmètre** : date et heure ; commit Git (`git rev-parse HEAD`) ; chemin et
   SHA-256 de R1, R2, R6, `SHA256SUMS` et `00_Index_des_pieces.pdf` ; nombre de
   fichiers vérifiés ; tests non exécutés, avec leur motif.
3. **Tableau des tests** : `ID | test | attendu | observé | statut (✅ / ❌ / ⚠️) | preuve`.
   La preuve est le chemin de la sortie brute, ou la commande qui reproduit le
   résultat.
4. **Constats bloquants**, un par ligne, chacun en deux lignes : ce qui est
   attendu (avec sa référence R1 à R7), ce qui est observé (cote, fichier,
   valeurs). Aucune recommandation.
5. **Réserves**, séparées en nouvelles et connues, sur le même modèle.
6. **Écarts postérieurs au dépôt** : les lignes du § 2, chacune vérifiée
   (✅ / ❌), avec sa preuve.
7. **Tests de sensibilité** : chaque faute provoquée, le test qui l'a détectée.
8. **Limites**. Au minimum :
   - le papier déposé au greffe n'a pas été comparé (R1 en est la source
     d'impression présumée) ;
   - G-5 non exécuté, s'il est resté désactivé ;
   - la pertinence des pièces n'a pas été appréciée.
9. **Annexe A — cote par cote** (106 lignes) : `cote | fichiers attendus |
   livrés | G-1/G-2 | index | statut`.

**`resultats.json`** : les mêmes résultats, lisibles par une machine.

```json
{
  "schema": "verification-pieces/1",
  "dossier": "505-17-016235-261",
  "execute_le": "…",
  "commit": "…",
  "entrees": {"R1": {"chemin": "…", "sha256": "…"}},
  "verdict": "CONFORME | CONFORME AVEC RÉSERVES | NON CONFORME",
  "decomptes": {"bloquants": 0, "reserves_nouvelles": 0, "reserves_connues": 0, "informations": 0},
  "tests": [{"id": "G-1", "statut": "ok | echec | reserve | non_execute", "attendu": "…", "observe": "…", "preuves": ["…"]}],
  "constats": [{"niveau": "bloquant | reserve | information", "connu": false, "reference": "…",
                "cote": "P-…", "fichier": "…", "attendu": "…", "observe": "…", "test": "…"}],
  "cotes": [{"cote": "P-1", "attendus": 1, "livres": 1, "integrite": "ok", "index": "ok", "statut": "ok"}]
}
```

### 10. Ce que tu ne fais pas

- Tu ne corriges rien, même une erreur évidente : tu la décris.
- Tu ne juges ni la pertinence ni la force probante d'une pièce.
- Tu ne proposes ni texte, ni stratégie.
- Tu n'arrondis pas un écart (« quasi identique » n'existe pas : c'est égal ou
  différent).
- Tu ne déclares pas un test réussi s'il n'a pas été exécuté.
