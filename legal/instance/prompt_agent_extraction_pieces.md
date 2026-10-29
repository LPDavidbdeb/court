# Prompt — agent chargé d'écrire l'extraction des pièces et ses tests

> Spécification destinée à un agent qui n'a pas suivi la conversation.
> Elle décrit le travail attendu, sous réserve des préalables du § 0.
> Elle ne remplace ni les règles du dépôt ni le mandat de lot.
>
> ⚠️ **Un choix a été fait pour toi, demandeur** : la règle d'arborescence du
> § 3. Si elle ne correspond pas à ton intention, change-la avant d'envoyer —
> tout le reste en dépend.

## Relecture du 26 octobre 2026 — ce qui a été vérifié, et ce qui reste à décider

*(Cette section s'adresse au demandeur. Elle ne fait pas partie du prompt.)*

**Vérifié en base et au dépôt :** `pillow 12.0.0`, `piexif 1.1.3` et
`ExifRead 3.5.1` sont dans `requirements.txt` et installés ·
`photos.Photo.datetime_original` existe · les quatre fichiers de cadrage du § 0
existent · `docs/architecture_c/lots/C0-A` existe. **Aucune affirmation
factuelle fausse.**

**Ajout du 26 octobre — la méthode EXIF vient du projet, pas d'une invention.**
Le § 4.3 emploie désormais `exifread.process_file()`, celle de
`photos/management/commands/process_photos.py`. Deux constats l'accompagnent, et
le second évitait un piège : la base ne porte **pas** l'EXIF complet de ces
photos (375 `all_metadata_json` vides sur 735) alors que **les fichiers le
portent** — 250 fichiers lus : 187 avec `Make = Canon` et `DateTimeOriginal`,
63 sans EXIF du tout ; et `datetime_original` est un **minimum de trois
candidats**, pas la date EXIF. Vérifier contre la base aurait produit des échecs
en masse sur des fichiers intacts.

⚠️ **Correction du même jour, apport du demandeur** : « la majorité des fichiers
n'auront pas de lat/long, l'appareil était trop vieux ». Vérifié — **aucun des
250 fichiers lus ne porte de coordonnées GPS** (38 n'ont qu'un marqueur `GPS*`
sans coordonnées, 212 aucun tag GPS). Un premier relevé annonçait « GPS sur 11
fichiers sur 12 » : il comptait des tags dont le **nom** commence par `GPS`, pas
des coordonnées. **Le contrôle du § 4.3 ne repose donc plus sur le GPS.**

**Deux apports de la révision valent d'être signalés** parce qu'ils corrigent
des faiblesses de la version initiale :

1. 🔴 **Comparer SHA-256 source et destination** (§ 4.2) **subsume le contrôle
   EXIF**. Une copie identique octet pour octet préserve nécessairement l'EXIF,
   et détecte en plus ce qu'aucun contrôle EXIF ne verrait — un PDF tronqué, un
   `.eml` altéré. La version initiale ne hachait que la sortie, ce qui ne
   prouvait rien sur la fidélité.
2. **`sha256_assemble` désigne le PDF assemblé, pas le fichier natif** (§ 1).
   Précision nécessaire : une comparaison fautive sur ce point a déjà été faite
   dans ce dossier, et elle avait produit un faux constat de 95 divergences.

### ⚠️ Une décision avant d'envoyer — le § 1, « contrôle de provenance préalable »

Il demande à la commande d'extraction de rapprocher chaque ligne de
`cotes.lock.json`, de vérifier la composition des liasses et de documenter les
redirections `Photo → PhotoDocument` — et fait d'un écart « un échec de la
cote ».

**C'est un second travail, et il porte son propre risque.** Un désaccord de
provenance sans rapport avec les fichiers bloquerait la livraison des cotes
concernées. Et la sémantique du verrou s'est déjà révélée piégeuse.

➜ **Recommandation : l'extraire en commande distincte** — `verifier_provenance_cotes`,
exécutée **avant**, dont le résultat conditionne l'extraction. Deux commandes
testables séparément plutôt qu'une qui fait deux métiers. Le test 15 et une
partie du § 5 suivraient.

*Contre-argument à peser : extraire sans contrôler la provenance peut livrer une
pièce qui n'est pas ce que le bordereau annonce. C'est une question de séquence,
pas de suppression.*

### ⚠️ Une confirmation — le § 3 tranche par défaut

« La ligne produit un seul fichier → un fichier nommé par la cote. » Donc
`P-5.1`, qui ne porte qu'une photo, devient **`P-5.1.jpg`** et non un dossier.

La forme de l'arborescence dépend alors du contenu : on ne peut pas la prévoir
depuis le bordereau seul. C'est défendable, mais **c'est la question restée sans
réponse** le 26 octobre. La confirmer ou la renverser.

### Verdict

**Prêt à soumettre**, une fois le § 1 tranché et le § 3 confirmé. Le reste tient.

Une réserve de forme, sans gravité : 392 lignes et 15 tests noient les trois
contraintes qui priment — **copie d'octets vérifiée, résolution en direct, ne
jamais fabriquer de cote**. Trois lignes en tête du prompt qui les rappellent
coûteraient peu.

---

## LE PROMPT

Tu travailles dans un projet Django (`mysite`) qui sert de base de preuve à un
dossier judiciaire réel. Le travail attendu, une fois les préalables du § 0
remplis, est une **commande de gestion** qui extrait les pièces cotées en juillet,
avec l'exclusion documentée ci-dessous, vers un dossier de livraison, et les
**tests unitaires** qui la couvrent.

Lis le code avant d'écrire. N'invente aucun nom de champ.

### 0. Cadre d'exécution et autorisations

Lis d'abord `AGENTS.md`, `PROJECT_CONTEXT.md`,
`legal/METHODOLOGIE_POST_DEPOT.md` et `docs/PROCESSUS_CHANGEMENT.md`.

L'implantation relève d'un **lot** : avant toute modification du code, identifier
son mandat écrit dans `docs/architecture_c/lots/<LOT>/MANDAT.md`, le SHA de
départ, les fichiers modifiables, les interdictions, les critères d'acceptation
et la configuration de test isolée. Vérifier les préalables de conception du
processus : quatre vues UML par use case touché, revue B, approbation utilisateur
de la version précise et dépendances satisfaites. Le présent prompt ne constate
pas que ces préalables sont remplis et ne les autorise pas par lui-même.

Si le mandat manque ou si un préalable n'est pas satisfait, relever ce qui
manque sans commencer l'implantation. Ne pas élargir les fichiers autorisés
pendant l'exécution.
Développer et tester dans une copie de travail isolée, sur une base jetable et
des fichiers synthétiques, sans accès aux ressources réelles.

Le diagnostic final sur la **base réelle**, même sans `--ecrire`, demande une
autorisation écrite explicite qui précise la base, les stockages consultables
et le périmètre. Elle peut figurer dans le mandat ou une instruction utilisateur
distincte; ne pas la redemander si elle existe déjà. En son absence, fournir
la commande à exécuter et indiquer « diagnostic réel non exécuté ».

Conserver le diff, les résultats de tests et les limites dans le répertoire du
lot. Le lot n'est « fait » qu'après les six conditions d'intégration du § 5 du
processus, dont la fusion dans `main`.

L'archive `legal/depots/2026-07-24_initial/` est **en lecture seule**. L'extraction
ne modifie ni les originaux, ni les cotes, ni les données de l'application.

### 1. La source — `case_manager.BordereauDepotJuillet`

Le relevé du 26 octobre 2026 mentionne **334 lignes**. Les nombres ci-dessous
sont des repères datés, à recalculer dans l'environnement autorisé, jamais des
constantes à imposer au résultat. Champs utiles :

| Champ | Sens |
|---|---|
| `cote` | **La cote de juillet** : `P-43` ou `P-43.7`. **NULL si la pièce n'a pas été déposée** |
| `cote_racine` | La cote de la pièce mère : `P-43`, pour `P-43.7` comme pour `P-43` |
| `rang`, `sous_rang` | Parties numériques, pour le tri |
| `content_type` + `object_id` + `content_object` | **Le couple (modèle, pk) de l'objet réel** |
| `source_type` | `email`, `event`, `pdfdocument`, `photodocument`, `chatsequence`, `emailthread`, `document` |
| `description` | Le libellé du bordereau |
| `resolu` | 🔴 **Drapeau stocké à l'import. NE PAS S'Y FIER** — voir § 6 |

🔴 **Le périmètre de départ est `cote` non nulle : 268 lignes sur 334 selon ce
relevé.** Les 66 autres n'ont pas de cote de juillet et ne sont pas extraites.

⚠️ **Et la cote `P-86` en est retirée** (décision du 26 octobre 2026, consignée
au journal des amendements) : son objet n'existe plus et elle n'appuyait aucun
paragraphe. **Périmètre effectif du relevé : 267 lignes.** Définir une règle
d'exclusion nommée et documentée, avec sa date et sa référence à
`legal/amendements/01_avant_notification/journal_modifications.md`, rubrique
« 26 octobre 2026 — Retrait de P-86 du bordereau amendé ». La liste de cette
livraison peut contenir explicitement `P-86`; le mécanisme de copie ne décide
pas lui-même des retraits. Conserver P-86 dans le rapport des exclusions,
sans modifier son identité historique ni sa ligne en base.

**Contrôle de provenance préalable.** Rapprocher les lignes sélectionnées de
`legal/depots/2026-07-24_initial/cotes.lock.json`, en lecture seule. Pour une
liasse, vérifier la cote racine, le couple modèle/pk de chaque sous-cote et
l'ordre du développement, à partir du verrou et du bordereau gelé si nécessaire.
L'import `import_bordereau_depot_juillet.py` a pu rediriger une référence
`Photo` vers un `PhotoDocument` : documenter la référence gelée, la cible réelle
et la justification de cette correspondance, sans supposer que la redirection
autorise à élargir la pièce à d'autres photos. Une concordance préalable datée
et référencée dans le mandat peut être réutilisée si ses données n'ont pas changé.
Une identité ou une composition non justifiée est un échec de la cote, jamais
une correction automatique. Conserver le résultat du rapprochement au manifeste.

`sha256_assemble` désigne le **PDF assemblé** : ce n'est pas l'empreinte du
fichier natif et il ne doit pas lui être comparé comme s'il s'agissait du même
fichier.

### 2. Où vivent les fichiers, par modèle

Répartition du relevé **avant exclusion de P-86** (268 lignes) :

| Modèle | Lignes | Comment atteindre les fichiers |
|---|---|---|
| `events.Event` | 107 | relation `linked_photos` → `photos.Photo` → `file` / `file_path` |
| `email_manager.Email` | 95 | `eml_file` et `eml_file_path` — **le `.eml` natif** |
| `pdf_manager.PDFDocument` | 42 | `file` |
| `photos.PhotoDocument` | 10 | relation `photos` → `photos.Photo` → `file` / `file_path` |
| `googlechat_manager.ChatSequence` | 7 | relation `messages` — **pas de fichier**, voir § 7 |
| `email_manager.EmailThread` | 4 | relation `emails` → fichiers natifs de chaque `Email`, selon la même règle que pour un courriel seul |
| `document_manager.Document` | 3 | `file_source` |

Après exclusion, le nombre de `PDFDocument` passe de 42 à 41 dans ce relevé.
Si une référence directe à `photos.Photo` est rencontrée, appliquer la règle
`file` / `file_path` sans la rediriger vers un autre objet. Tout autre modèle
non pris en charge est un échec explicite.

**Choisir la source sans la transformer :**

- Pour une photo, privilégier `file`; utiliser `file_path` comme repli local
  si le champ est vide ou sa source inaccessible. Même règle pour un courriel :
  `eml_file` avant `eml_file_path`. Consigner tout repli et son motif.
- Si les deux sources sont accessibles, comparer leurs SHA-256. Si elles
  diffèrent, rapporter une ambiguïté en échec; ne pas choisir silencieusement.
- Pour un `FileField`, utiliser son stockage Django. Une source locale peut
  être copiée par `shutil.copy2`; une source distante est lue en binaire via
  `FieldFile.open("rb")` avec le stockage déjà configuré. Ne pas supposer que
  `.path` existe sur Google Cloud Storage. Aucun ajout de dépendance réseau;
  les accès réels restent soumis au § 0.
- Pour chaque fichier, consigner le champ ou le repli utilisé, le nom source
  et le chemin local ou la clé de stockage. Conserver l'extension source.

### 3. L'arborescence de sortie — la règle

Une ligne de bordereau = **une cote** = **une entrée** dans le dossier de sortie.

- La ligne produit **un seul fichier** → un fichier nommé par la cote :
  `P-2.pdf`, `P-3.eml`
- La ligne produit **plusieurs fichiers** → un **dossier** nommé par la cote,
  contenant les fichiers numérotés par rang interne, extension d'origine conservée :

```
P-1/            ← exemple d'un PhotoDocument à plusieurs photos
   P-1-01.jpg
   P-1-02.jpg
P-5.1/          ← Event pk=242 : la sous-cote vient DÉJÀ du bordereau
   P-5.1-01.jpg
   P-5.1-02.jpg
P-2.pdf         ← PDFDocument : un fichier
```

⚠️ **Ne jamais réinventer les sous-cotes du bordereau.** `P-5.1` à `P-5.6` sont
six **lignes distinctes** de la table, chacune pointant un `Event` différent. La
numérotation `-01`, `-02` est un rang **interne** à une ligne, et c'est autre
chose.

Fixer un ordre total et reproductible : lignes par `(rang, sous_rang, pk)`,
photos par `(datetime_original, pk)`, courriels d'un fil par `(date_sent, pk)`.
Placer explicitement les dates absentes après les dates renseignées. Inscrire
chaque rang interne et le modèle/pk du membre au manifeste. Une même source
invoquée sous deux cotes conserve ses deux entrées : pas de dédoublonnage
qui ferait disparaître une cote.

### 4. 🔴 Les métadonnées — la contrainte qui prime sur tout

Le dossier a promis par écrit aux parties adverses que les fichiers seraient
transmis « **dans leur format électronique, sans conversion ni réencodage** ».
Pour les photographies, l'**EXIF** **porte la preuve** : `DateTimeOriginal`
établit **quand**. Le détruire détruit la pièce. ⚠️ **Pas où** — ce corpus ne
porte aucune coordonnée GPS (§ 4.3).

**Règles absolues :**

1. **Copie d'octets uniquement**, par le moyen adapté au stockage (§ 2).
   **JAMAIS** `PIL.Image.open(...).save(...)`, jamais de conversion, de
   redimensionnement, de recompression ou de normalisation. `copy2` conserve
   les dates système qu'il peut préserver; ne pas promettre toutes les dates
   de création de tous les systèmes. La preuve d'intégrité porte sur les octets.
2. **Pour chaque fichier, quel que soit son format**, calculer le SHA-256 de
   la source et recalculer celui de la destination après écriture. Exiger
   `SHA256(source) == SHA256(destination)` et des tailles identiques. Ne jamais
   recopier l'empreinte source dans le champ destiné à la copie. Un écart est
   une erreur et interdit de publier la cote comme produite.
3. **Contrôle EXIF complémentaire — par la méthode déjà éprouvée du projet.**

   **Employer `exifread.process_file(f, details=False)`** sur le fichier ouvert
   en binaire : c'est la méthode de
   `photos/management/commands/process_photos.py`, elle est **en lecture seule**
   et n'écrit jamais dans le fichier. `exifread==3.5.1`, `pillow==12.0.0` et
   `piexif==1.1.3` sont dans `requirements.txt` et installés.

   Lire ainsi **la source et la copie**, et comparer **les tags retournés par
   cette lecture**. ⚠️ Pas « tout l'EXIF » : `details=False` omet notamment les
   **MakerNotes**. La conservation de la totalité des métadonnées est garantie
   par l'**égalité des empreintes**, pas par ce contrôle.

   🔴 **Comparer des valeurs normalisées, jamais les objets.** `exifread`
   retourne des `IfdTag` dont l'égalité n'est pas documentée comme portant sur
   la valeur : une comparaison directe des dictionnaires peut échouer sur deux
   fichiers pourtant identiques octet pour octet. Comparer
   `{k: str(v) for k, v in tags.items()}`, ou lire avec `builtin_types=True`.

   L'ancre utile de ce corpus est **`EXIF DateTimeOriginal`**. Un écart entre
   source et copie est une erreur.

   ⚠️ **Ne pas bâtir le contrôle sur le GPS.** **Aucune coordonnée GPS relevée
   dans les 250 fichiers examinés** sur les 735 du périmètre ; leur présence
   n'est **pas requise** pour valider une copie. *(Le relevé porte sur
   l'échantillon, pas sur le corpus entier : les champs GPS nuls en base ne
   l'étendent pas, puisque la base est elle-même incomplète.)* Un contrôle
   centré sur le GPS donnerait l'illusion d'une vérification.

   ⚠️ **Et 63 fichiers sur 250 n'ont aucun EXIF** — captures d'écran ou images
   dépouillées. Pour eux, « absence des deux côtés » est le **résultat
   attendu**, pas une anomalie. Seule l'égalité des empreintes les couvre.

   Si le format n'est pas pris en charge, indiquer « contrôle EXIF non
   disponible » et la raison; ne pas le prétendre exécuté. L'égalité des
   empreintes reste obligatoire dans tous les cas.

   🔴 **Ne jamais vérifier l'EXIF contre la base, ni le reconstruire depuis
   elle.** Sur les **735 photos** du périmètre, `all_metadata_json` est vide
   pour **375** et `gps_latitude` nul pour les **735**, alors que les fichiers
   portent de l'EXIF. **La base est un référent incomplet ; le fichier est le
   référent.**

   *(Ne pas en inférer que `process_photos.py` « n'extrait que la date » : il
   délègue à `PhotoProcessingService`, qui extrait d'autres champs. Seul l'appel
   de lecture `exifread.process_file()` est repris ici.)*

   🔴 **Et les photographies stockées sont des DÉRIVÉS, pas les originaux.**
   `PhotoProcessingService` redimensionne à **1600 px**, convertit en RGB et
   réenregistre en **JPEG qualité 90** avec l'EXIF réinjecté. Vérifié : 15 photos
   du périmètre sur 15 sont plafonnées à 1600 alors que la base annonce leur
   dimension d'origine. **`file_path` ne résout pour aucune des 735** : l'original
   n'est pas accessible.

   ➜ **Conséquences pour toi :** `photo.file` est la **seule** source — ce n'est
   pas une préférence mais un fait. Et le manifeste doit qualifier chaque
   photographie **« dérivé réduit à 1600 px, JPEG qualité 90, EXIF conservé »**,
   **jamais « fichier source »**. Constat complet :
   `legal/instance/constat_photos_reencodees.md`.

   ⚠️ **`Photo.datetime_original` n'est pas l'EXIF.** `populate_photos.py` le
   calcule comme `min(DateTimeOriginal, date tirée du nom de fichier, mtime)`.
   Il **sert de clé d'ordre déterministe** (§ 3), **jamais de preuve de
   l'horodatage**.

### 5. Le manifeste et le rapport d'exhaustivité

Avec `--ecrire`, produire un `manifeste.json` et un `manifeste.md` contenant le
même inventaire. Inclure une version du schéma de manifeste, la sélection
résolue, la règle d'exclusion appliquée et les décomptes. Pour chaque cote
attendue ou exclue, donner :

- la cote, `cote_racine`, le modèle/pk de l'objet et la description;
- son statut et son motif éventuel, ainsi que le contrôle de provenance (§ 1);
- pour chaque fichier membre, son modèle/pk, son rang interne, son nom source,
  le champ et la localisation utilisés, et le chemin de sortie relatif;
- les tailles et SHA-256 **source et copie**, ainsi que le résultat du contrôle
  EXIF. Seuls les fichiers complètement écrits et vérifiés sont « produits ».

Afficher le rapport d'exhaustivité et l'inclure dans les deux manifestes.
Exemple **conditionnel**, si tous les fichiers hors transcriptions sont accessibles :

```
cotées en juillet sélectionnées : 268
exclues                        :   1 — P-86, motif et décision référencés
attendues                      : 267
produites                      : 260
à rendre                       :   7
en échec                       :   0
```

Compter des **lignes de bordereau**, pas les fichiers membres ni seulement les
cotes racines. Calculer les nombres depuis la sélection effective (§ 8) :

```text
cotées sélectionnées = exclues + attendues
attendues = produites + à rendre + en échec
```

Suivre ces chiffres de la liste des exclusions, des « à rendre » et des échecs,
cote par cote, avec leur motif. Le relevé de 267 objets résolus ne prouve pas
que leurs fichiers existent et sont lisibles. Rapporter toute découverte sans
réparer les données ou les fichiers sources.

**Sans `--ecrire`**, construire le plan et afficher le rapport sans créer ni
modifier aucun fichier ou dossier, y compris les manifestes et les temporaires.
Les copies accessibles portent le statut « prévue », jamais « produite ».
Afficher `attendues = prévues + à rendre + en échec` et `produites = 0`.
Calculer les empreintes sources; laisser les tailles et empreintes de copie
absentes ou nulles puisque les copies n'existent pas. Ne pas déclarer vérifié
un contrôle source/copie qui n'a pas eu lieu.

⚠️ **La gestion d'erreur par cote est obligatoire.** Un `try/except` par
ligne, un objet non résolu traité comme un échec rapporté. Le cas s'est produit
une fois — P-86, dont l'objet avait disparu alors que la ligne portait
`resolu=True` — et rien ne garantit qu'il ne se reproduira pas. **Les tests
doivent le couvrir** avec une ligne artificielle pointant un pk inexistant.

### 6. 🔴 Résoudre en direct, jamais lire `resolu`

`resolu` est un booléen **stocké au moment de l'import**. Il dit que le
rattachement a réussi un jour, pas qu'il tient aujourd'hui. Dans le relevé
du 26 octobre 2026, les 268 lignes portaient `resolu=True`, alors que P-86
ne se résolvait plus.

Pour chaque ligne attendue **après exclusion**, passer par `content_object`
et traiter `None` comme un échec. Envelopper chaque ligne dans son propre
`try/except` : une ligne en échec n'interrompt pas le traitement des autres.
P-86 reste une exclusion documentée, sans tentative de résolution nécessaire.

### 7. Les cas sans fichier

`ChatSequence` (7 lignes) n'a pas de fichier : la pièce est une **transcription**
de ses `messages`. **Ne génère rien pour l'instant** — rapporte-les comme
« à rendre », distinctement des échecs. Le rendu est un travail séparé, avec ses
propres exigences d'intégrité.

Ce statut est réservé à un rendu volontairement différé et identifié, ici les
`ChatSequence`. Un original attendu mais absent, un champ fichier vide sans
repli utilisable, une source illisible, un fil sans courriel ou un conteneur
photographique vide sont des **échecs**, avec des motifs distincts.

Une cote n'est « produite » que si **tous** ses fichiers attendus sont copiés
et vérifiés. Si une photo manque dans un ensemble de cinq, la cote entière est
en échec; les quatre autres ne constituent pas une livraison complète. Ne pas
réduire silencieusement la liste des membres ni remplacer le natif manquant
par un rendu, une transcription ou un document reconstruit.

### 8. Forme attendue

- Une **commande de gestion Django** dans `case_manager/management/commands/`.
- Nom suggéré : `extraire_pieces_depot`.
- Arguments : `--sortie <dossier>` (obligatoire), `--cote <P-n>` (répétable, pour
  n'extraire que certaines), `--ecrire` (sans quoi la commande **rapporte sans
  rien écrire** — c'est la convention du projet).
- Sans `--cote`, sélectionner toutes les lignes à cote de juillet, puis
  appliquer l'exclusion. Une cote racine demandée, par exemple `P-43`, sélectionne
  toutes les lignes de cette racine; une sous-cote, par exemple `P-43.7`,
  sélectionne cette seule ligne. Réunir les sélections sans doublon. Une demande
  de P-86 figure comme exclue avec son motif. Une cote inconnue, non déposée ou
  mal formée est une erreur d'argument signalée avant toute écriture.
- Valider le dossier de sortie : il doit être distinct des répertoires sources
  et hors de l'archive gelée; ne jamais y copier sur un original.
- **Réutilisable** : ne pas coder en dur les décomptes ni les chemins de
  fichiers. Calculer les décomptes depuis la sélection et recevoir le dossier
  de sortie en argument. L'exclusion de P-86 doit être explicite, documentée
  et reliée à la décision du 26 octobre 2026 consignée dans
  `legal/amendements/01_avant_notification/journal_modifications.md`.

**Publication et reprises :**

1. Pour une première exécution, utiliser un dossier absent ou vide. Écrire
   chaque cote dans un espace temporaire distinct des entrées livrables,
   vérifier tous ses fichiers, puis publier son fichier ou dossier complet.
   En cas d'échec, retirer seulement les temporaires créés par cette exécution
   et poursuivre les autres cotes. Aucun fichier d'une cote en échec ne doit
   rester parmi les entrées livrables.
2. Un dossier déjà rempli n'est réutilisable que s'il porte les deux manifestes
   concordants d'une exécution achevée sans échec, pour **la même sélection et
   la même règle d'exclusion**. Vérifier à nouveau les sources et les copies,
   leur composition, leur provenance et leurs empreintes. Si tout est
   identique, conserver les fichiers et les manifestes identiques octet pour
   octet. Pas d'horodatage d'exécution variable dans ces manifestes.
3. Si le périmètre change — notamment un `--cote` différent —, si une source ou
   une copie diffère, s'il manque un fichier ou s'il reste une entrée inconnue,
   refuser la réutilisation avant de modifier le dossier. Ne rien supprimer
   ni écraser silencieusement : demander l'utilisation d'un nouveau dossier.
   Après une interruption, des temporaires résiduels ou une exécution avec
   échecs, la reprise se fait également dans un **nouveau dossier**.
4. Si une cote échoue, terminer le rapport des autres cotes, écrire les
   manifestes quand `--ecrire` est actif, puis retourner un code de sortie non
   nul. En simulation, appliquer la même règle de code de sortie aux erreurs
   détectables. Les « à rendre » restent visibles et ne sont pas des erreurs
   de copie. Une erreur globale empêchant l'écriture du rapport est signalée
   comme telle, sans annoncer un succès.

**Style de la maison** — lis `case_manager/management/commands/verifier_appuis_depot.py`
et `case_manager/transmission_service.py` avant d'écrire. Docstring en français
qui explique **pourquoi** la commande existe et quels écueils elle évite, pas
seulement ce qu'elle fait. Sorties en français.

### 9. Les tests unitaires

Dans les fichiers de test autorisés par le mandat, sur base dédiée et fixtures
synthétiques, avec stockages locaux temporaires ou doubles sans réseau :

1. Une ligne à **un fichier** produit un fichier nommé par la cote.
2. Une ligne à **plusieurs fichiers** produit un dossier nommé par la cote,
   contenant des fichiers en `-01`, `-02`, extensions conservées.
3. Une ligne artificielle avec `resolu=True` dont `content_object` est `None`
   est **rapportée en échec** et
   **n'interrompt pas** le traitement des suivantes.
4. 🔴 **L'EXIF d'une image est identique entre la source et la copie.** Construis
   une image de test portant horodatage **et** GPS — non parce que le corpus en
   contient, il n'en contient pas, mais pour prouver que le mécanisme préserve
   **tout** l'EXIF et non les seuls tags qu'on a pensé à comparer. Couvrir aussi
   l'absence totale d'EXIF — **63 fichiers sur 250 sont dans ce cas**, c'est le
   résultat attendu et non un échec — et un format dont le contrôle EXIF n'est
   pas disponible.
5. Les SHA-256 source et copie du manifeste sont égaux et correspondent aux
   fichiers réellement lus. Une altération simulée lors de la copie est
   détectée et empêche de publier la cote, y compris pour un fichier non image.
6. Le compte d'exhaustivité respecte les égalités du § 5 en écriture et en
   simulation, avec des nombres calculés plutôt que 267 imposé aux fixtures.
7. **Idempotence** : deux exécutions successives donnent des manifestes
   identiques octet pour octet et des copies inchangées.
8. Sans `--ecrire`, **aucun fichier ou dossier n'est créé ni modifié**; les
   copies restent « prévues », sans empreinte de destination inventée.
9. P-86 est exclue avec sa raison, même si son objet existe dans la fixture;
   une ligne sans cote de juillet n'est pas extraite.
10. Les filtres sélectionnent correctement une racine ou une sous-cote,
    éliminent les doublons et rapportent P-86 comme exclue. Une cote inconnue,
    non déposée ou mal formée provoque une erreur avant écriture.
11. Un original absent, un champ vide et un conteneur vide sont des échecs;
    une `ChatSequence` est « à rendre » sans transcription générée. Une liasse
    dont un membre manque ne laisse aucune copie partielle livrable.
12. Des dates identiques ou absentes ne changent pas le rang des membres entre
    deux exécutions; le manifeste identifie chaque membre par modèle/pk.
13. La priorité des champs, le repli documenté et le conflit entre deux sources
    accessibles sont couverts. Une source distante est simulée par un stockage
    Django dont `.path` n'est pas disponible.
14. Un dossier inconnu, un changement de sélection, une copie manquante ou
    altérée, une source modifiée et les traces d'une interruption provoquent
    un refus sans écraser ni supprimer les fichiers présents. Une panne
    pendant une cote n'empêche pas le rapport des suivantes; le résultat en
    échec retourne un code non nul.
15. Le rapprochement au verrou couvre une liasse et une redirection
    `Photo → PhotoDocument` justifiée; une identité divergente ou un ajout
    non justifié de membre est rapporté en échec. Employer un petit verrou
    synthétique pour les tests, sans écrire dans l'archive gelée.

### 10. Ce que tu ne fais pas

- Tu **n'envoies rien** et tu n'ajoutes aucune dépendance réseau.
- Tu **ne modifies pas** `BordereauDepotJuillet` ni aucune donnée. Lecture seule.
- Tu **ne corriges pas** P-86. C'est un fait du dossier, traité ailleurs.
- Tu **ne génères pas** les transcriptions de `ChatSequence`.
- Tu **ne régénères pas** les actes P-19, P-40 et P-42 depuis les modèles :
  seule la copie binaire de leur `Document.file_source` est dans ce périmètre.
- Tu n'ajoutes pas de dépendance sans vérifier d'abord ce qui est installé.

Quand l'implantation et les tests sont terminés, fournir le rapport du lot,
les vérifications exécutées et les limites. **Si le diagnostic réel du § 0
est explicitement autorisé**, exécuter la commande sans `--ecrire` sur la base
et les stockages désignés. Rapporter les cotes sélectionnées, exclues,
attendues, les copies prévues, les « à rendre » et les échecs, avec leurs listes
et motifs. Ne pas présenter ce diagnostic comme une extraction effectuée ni
comme une validation de l'ensemble du dossier prêt à communiquer.
