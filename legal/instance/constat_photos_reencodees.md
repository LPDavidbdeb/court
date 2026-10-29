# 🔴 Les photographies en base sont des réencodages, pas les originaux

> **Constat du 26 octobre 2026**, établi en vérifiant une remarque du demandeur
> sur `photos/services.py`. Il dépasse la question du script d'extraction et
> touche la **valeur probante** des pièces photographiques.

---

## 1. Le fait

`photos/services.py` — `PhotoProcessingService` — fait ceci avant d'enregistrer :

```python
self.max_width    = 1600
self.jpeg_quality = 90
...
if w > self.max_width:
    img = img.resize((self.max_width, new_h), Image.Resampling.LANCZOS)
img = img.convert('RGB')
img.save(buffer, "JPEG", quality=self.jpeg_quality, exif=exif_bytes)
photo.file.save(new_filename, ContentFile(processed_image_bytes))
```

**Redimensionnement à 1600 px, conversion en RGB, réenregistrement en JPEG
qualité 90, EXIF réinjecté.**

### Vérifié sur les pièces du bordereau

Sur 15 photos du périmètre dont la base annonce une largeur supérieure à 1600 :

| pk | base | fichier stocké |
|---|---|---|
| 4558 | 2035 × 2511 | **1600 × 1974** |
| 4538 | 2142 × 1294 | **1600 × 966** |
| 4555 | 3264 × 2448 | **1600 × 1200** |
| 4526 | 3223 × 1032 | **1600 × 512** |

**15 sur 15 plafonnées à 1600.** Aucune intacte.

➜ La base conserve les dimensions **de l'original** ; le fichier est la
**version réduite**.

## 2. 🔴 Et l'original n'est pas accessible

Sur les **735 photos** du périmètre :

| | |
|---|---|
| `file.path` existe sur disque | **735** |
| `file_path` existe sur disque | **0** — dont 709 renseignés mais pointant nulle part |

`file_path` désigne l'original sur disque. **Il ne résout pour aucune des 735.**
Le seul octet disponible est le dérivé à 1600 px.

⚠️ `Media/` pèse 6,1 Go : les originaux peuvent s'y trouver, hors d'atteinte du
modèle. **À vérifier, séparément.**

## 3. Ce que cela change, par ordre de gravité

### 3.1 La promesse faite aux parties adverses tient — par chance

Les lettres du 16 octobre disent :

> « le fichier source conservé sera transmis dans son format électronique,
> **sans conversion ni réencodage aux fins de sa communication** »

La réserve « **aux fins de sa communication** » a été ajoutée lors d'une
révision, pour une autre raison. Elle rend l'énoncé **exact** : la communication
ne réencodera rien. Mais ce qui sera communiqué **est déjà un dérivé**.

⚠️ Sans cette réserve, la phrase aurait été fausse.

### 3.2 La valeur probante n'est pas détruite — elle est diminuée et doit être dite

Ce qui subsiste : le contenu de l'image, et l'**EXIF réinjecté** — dont
`DateTimeOriginal`, qui est l'ancre de la preuve de densité
([[feedback_preuve_volume_densite]]).

Ce qui est perdu : la résolution d'origine et l'intégrité binaire du fichier de
l'appareil.

**La méthodologie du dossier tient déjà la règle pour les actes incriminés**
(`METHODOLOGIE_POST_DEPOT.md` § 9.2) : pour eux l'original s'impose, et le rendu
« ne remplace pas l'original pour la communication ». Les photographies relèvent
de l'autre régime — documents du demandeur, dont la génération est légitime
**pourvu que l'intégrité du transfert soit documentée**.

➜ **Ce qui est exigé n'est donc pas l'original, c'est la documentation du
transfert.** Elle n'existe pas aujourd'hui.

### 3.3 Ce que le manifeste doit porter

Pour chaque photographie : **« dérivé réduit à 1600 px, JPEG qualité 90, EXIF
conservé »**, et non « fichier source ». Nommer un dérivé « source » serait une
inexactitude qu'un contentieux relèverait sans effort.

## 4. Décisions à prendre

| | |
|---|---|
| **Chercher les originaux** dans `Media/` (6,1 Go) et les rattacher | les retrouver rendrait le point 3 sans objet |
| À défaut, **documenter le transfert** : paramètres du réencodage, date, et le fait que l'EXIF a été réinjecté | c'est ce qu'exige le régime des documents technologiques |
| **Qualifier les photographies au manifeste** comme dérivés | à faire dans tous les cas |

⚠️ **Rien de tout cela n'est une faute.** Le réencodage date de la constitution
de la base, bien avant le litige, et pour des raisons de stockage. Ce qui
compterait serait de le **taire**.

## 5. Effet immédiat sur le script d'extraction

- `photo.file` est **la seule source accessible** : la règle « privilégier
  `file`, `file_path` en repli » est donc juste pour ce corpus, mais pour une
  raison qu'il faut écrire — `file_path` ne résout pour aucune des 735.
- Le script **ne peut pas** livrer d'original photographique. Il copie le dérivé,
  fidèlement, et le **qualifie** comme tel.
- Le contrôle EXIF reste pertinent : l'EXIF réinjecté doit survivre à la copie.
