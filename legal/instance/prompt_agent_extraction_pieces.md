# Prompt — agent chargé d'écrire l'extraction des pièces et ses tests

> À remettre tel quel à un agent qui n'a pas suivi la conversation. Il est
> autoportant : modèles, champs, contraintes et pièges y figurent.
>
> ⚠️ **Un choix a été fait pour toi, demandeur** : la règle d'arborescence du
> § 3. Si elle ne correspond pas à ton intention, change-la avant d'envoyer —
> tout le reste en dépend.

---

## LE PROMPT

Tu travailles dans un projet Django (`mysite`) qui sert de base de preuve à un
dossier judiciaire réel. Écris une **commande de gestion** qui extrait les pièces
du bordereau de dépôt vers un dossier de livraison, et les **tests unitaires**
qui la couvrent.

Lis le code avant d'écrire. N'invente aucun nom de champ.

### 1. La source — `case_manager.BordereauDepotJuillet`

334 lignes. Champs utiles :

| Champ | Sens |
|---|---|
| `cote` | **La cote de juillet** : `P-43` ou `P-43.7`. **NULL si la pièce n'a pas été déposée** |
| `cote_racine` | La cote de la pièce mère : `P-43`, pour `P-43.7` comme pour `P-43` |
| `rang`, `sous_rang` | Parties numériques, pour le tri |
| `content_type` + `object_id` + `content_object` | **Le couple (modèle, pk) de l'objet réel** |
| `source_type` | `email`, `event`, `pdfdocument`, `photodocument`, `chatsequence`, `emailthread`, `document` |
| `description` | Le libellé du bordereau |
| `resolu` | 🔴 **Drapeau stocké à l'import. NE PAS S'Y FIER** — voir § 6 |

🔴 **Le périmètre est exactement `cote` non nulle : 268 lignes sur 334.** Les 66
autres n'ont pas été déposées en juillet et ne doivent pas être extraites.

⚠️ **Et la cote `P-86` en est retirée** (décision du 26 octobre 2026, consignée
au journal des amendements) : son objet n'existe plus et elle n'appuyait aucun
paragraphe. **Périmètre effectif : 267 lignes.** La commande doit l'exclure par
une règle lisible, pas par un filtre codé en dur sans explication.

### 2. Où vivent les fichiers, par modèle

| Modèle | Lignes | Comment atteindre les fichiers |
|---|---|---|
| `events.Event` | 107 | relation `linked_photos` → `photos.Photo` → `file` / `file_path` |
| `email_manager.Email` | 95 | `eml_file` et `eml_file_path` — **le `.eml` natif** |
| `pdf_manager.PDFDocument` | 42 | `file` |
| `photos.PhotoDocument` | 10 | relation `photos` → `photos.Photo` → `file` / `file_path` |
| `googlechat_manager.ChatSequence` | 7 | relation `messages` — **pas de fichier**, voir § 7 |
| `email_manager.EmailThread` | 4 | relation `emails` → chaque `Email.eml_file` |
| `document_manager.Document` | 3 | `file_source` |

### 3. L'arborescence de sortie — la règle

Une ligne de bordereau = **une cote** = **une entrée** dans le dossier de sortie.

- La ligne produit **un seul fichier** → un fichier nommé par la cote :
  `P-2.pdf`, `P-3.eml`
- La ligne produit **plusieurs fichiers** → un **dossier** nommé par la cote,
  contenant les fichiers numérotés en sous-cote, extension d'origine conservée :

```
P-1/            ← PhotoDocument : 4 photos
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

### 4. 🔴 Les métadonnées — la contrainte qui prime sur tout

Le dossier a promis par écrit aux parties adverses que les fichiers seraient
transmis « **dans leur format électronique, sans conversion ni réencodage** ».
Pour les photographies, l'**EXIF** (horodatage, géolocalisation) **porte la
preuve** : il établit où et quand. Le détruire détruit la pièce.

**Règles absolues :**

1. **Copie d'octets uniquement.** `shutil.copy2` (qui préserve aussi les dates).
   **JAMAIS** `PIL.Image.open(...).save(...)`, jamais de conversion, de
   redimensionnement, de recompression ou de normalisation.
2. **Vérifier après copie.** Pour chaque image, relire l'EXIF de la source et de
   la copie et **comparer**. Un écart est une **erreur**, pas un avertissement.
   *(Bibliothèque au choix — vérifie ce qui est déjà installé avant d'en
   ajouter une.)*
3. **SHA-256 de chaque fichier produit**, calculé sur le fichier écrit.

### 5. Le manifeste et le rapport d'exhaustivité

Produire un `manifeste.json` et un `manifeste.md` donnant, par cote : la cote, le
`cote_racine`, le modèle et le pk, la description, les fichiers produits avec
leur taille et leur SHA-256.

Et un **rapport d'exhaustivité** affiché et écrit :

```
attendu   : 268 lignes à cote de juillet
produites : N
en échec  : M
```

suivi de la **liste des échecs**, cote par cote, avec le motif.

**Sur le périmètre corrigé de 267 lignes, aucun échec n'est attendu.** Si la
commande en rapporte un, c'est une découverte : le rapporter tel quel, sans
tenter de le réparer.

⚠️ **La gestion d'erreur reste obligatoire malgré cela.** Un `try/except` par
ligne, un objet non résolu traité comme un échec rapporté. Le cas s'est produit
une fois — P-86, dont l'objet avait disparu alors que la ligne portait
`resolu=True` — et rien ne garantit qu'il ne se reproduira pas. **Les tests
doivent le couvrir** avec une ligne artificielle pointant un pk inexistant.

### 6. 🔴 Résoudre en direct, jamais lire `resolu`

`resolu` est un booléen **stocké au moment de l'import**. Il dit que le
rattachement a réussi un jour, pas qu'il tient aujourd'hui. En base, les 268
lignes portent `resolu=True` — et pourtant P-86 ne se résout plus.

**Toujours** passer par `content_object` et traiter `None` comme un échec.
Envelopper chaque ligne dans son propre `try/except` : une ligne en échec
n'interrompt pas les 267 autres.

### 7. Les cas sans fichier

`ChatSequence` (7 lignes) n'a pas de fichier : la pièce est une **transcription**
de ses `messages`. **Ne génère rien pour l'instant** — rapporte-les comme
« à rendre », distinctement des échecs. Le rendu est un travail séparé, avec ses
propres exigences d'intégrité.

Même traitement pour toute ligne dont le champ fichier est vide.

### 8. Forme attendue

- Une **commande de gestion Django** dans `case_manager/management/commands/`.
- Nom suggéré : `extraire_pieces_depot`.
- Arguments : `--sortie <dossier>` (obligatoire), `--cote <P-n>` (répétable, pour
  n'extraire que certaines), `--ecrire` (sans quoi la commande **rapporte sans
  rien écrire** — c'est la convention du projet).
- **Idempotente** : relancer sur le même dossier donne le même résultat.
- **Réutilisable** : aucune valeur codée en dur hors des noms de modèles ; elle
  doit servir pour chaque livraison à venir.

**Style de la maison** — lis `case_manager/management/commands/verifier_appuis_depot.py`
et `case_manager/transmission_service.py` avant d'écrire. Docstring en français
qui explique **pourquoi** la commande existe et quels écueils elle évite, pas
seulement ce qu'elle fait. Sorties en français.

### 9. Les tests unitaires

Dans `case_manager/`, sur fixtures, sans toucher la base réelle :

1. Une ligne à **un fichier** produit un fichier nommé par la cote.
2. Une ligne à **plusieurs fichiers** produit un dossier nommé par la cote,
   contenant des fichiers en `-01`, `-02`, extensions conservées.
3. Une ligne dont `content_object` est `None` est **rapportée en échec** et
   **n'interrompt pas** le traitement des suivantes.
4. 🔴 **L'EXIF d'une image est identique entre la source et la copie.** Construis
   une image de test portant de l'EXIF.
5. Le SHA-256 du manifeste correspond au fichier réellement écrit.
6. Le compte d'exhaustivité est exact : attendu = produites + en échec + à rendre.
7. **Idempotence** : deux exécutions successives donnent des manifestes
   identiques.
8. Sans `--ecrire`, **aucun fichier n'est créé**.

### 10. Ce que tu ne fais pas

- Tu **n'envoies rien** et tu n'ajoutes aucune dépendance réseau.
- Tu **ne modifies pas** `BordereauDepotJuillet` ni aucune donnée. Lecture seule.
- Tu **ne corriges pas** P-86. C'est un fait du dossier, traité ailleurs.
- Tu **ne génères pas** les transcriptions de `ChatSequence`.
- Tu n'ajoutes pas de dépendance sans vérifier d'abord ce qui est installé.

Quand tu as fini : exécute la commande **sans `--ecrire`** sur la vraie base et
rapporte les trois chiffres d'exhaustivité, plus la liste des échecs.
