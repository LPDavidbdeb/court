# Extraction des pièces — notes de l'outil

**Cadre retenu par LP (29 oct. 2026)** : un script autonome, placé sous
`legal/instance/outils/`, et non une commande de `case_manager`. Il lit la base
sans la modifier et n'écrit que dans le dossier de livraison. Ce n'est donc pas
une modification du système, et il échappe au processus de lots (C0-A non
intégré bloque l'ouverture du lot suivant). La spécification d'origine reste
`../prompt_agent_extraction_pieces.md` : copie d'octets seulement, SHA-256 de la
source et de la copie, aucune cote inventée, P-86 exclue, manifeste
d'exhaustivité.

## La source : la table `BordereauDepotJuillet`, et non `cotes.lock.json`

Comparaison faite le 29 oct. 2026, en lecture seule, entre la table (lignes à
cote de juillet) et `legal/depots/2026-07-24_initial/cotes.lock.json`
(`identites_attendues`, membres séparés par « | ») :

| Constat | Nombre |
|---|---|
| Cotes racines dans les deux | **106 / 106**, aucune de part ou d'autre seulement |
| Mêmes membres, **même ordre** | 94 |
| Mêmes membres, **ordre différent** | 8 : P-22, P-43, P-48, P-56, P-57, P-72, P-89, P-99 |
| Référence `Photo` au verrou, `PhotoDocument` à la table | 4 : P-1 (photo 4558 → PhotoDocument 14), P-8 (4526 → 3), P-15 (4551 → 9), P-101 (4554 → 12) |

**Identité des pièces : concordance totale.** Aucune cote ne désigne une autre
pièce dans l'une des deux sources.

**Ordre des liasses : la table suit le bordereau gelé, le verrou non.** Vérifié
sur `candidats/bordereau_pieces.md`, la copie gelée du dépôt :

| Cote | Bordereau gelé | Table | Verrou |
|---|---|---|---|
| P-99 | 644/643 | 644, 643 | 643, 644 |
| P-22 | 6/8/295/306 | 6, 8, 295, 306 | ordre différent |
| P-48 | 81/80/100 (« liasse indexée P-48.1 à P-48.3 ») | 81, 80, 100 | ordre différent |
| P-72 | 67, 114, 66, 116, 115 (« P-72.1 à P-72.5 ») | 67, 114, 66, 116, 115 | ordre différent |

Le bordereau gelé lui-même indexe les sous-cotes dans cet ordre. C'est donc
l'ordre de la table qui fait foi pour nommer P-48.1, P-48.2, etc.

**Les quatre redirections sont des enveloppes.** Chacun de ces `PhotoDocument`
contient **exactement** la photo désignée par le verrou. La pièce n'est pas
élargie à d'autres photos.

➜ **La table est la source.** Le verrou ne sert plus que de contrôle d'identité,
et ce contrôle est fait. Deux règles de la spécification demeurent :

- **ne jamais lire `resolu`** : résoudre chaque ligne en direct par
  `content_object`, et traiter `None` comme un échec. C'est le cas de P-86 ;
- **sélectionner `cote` non nulle** : les lignes ajoutées après le dépôt
  portent `cote = NULL`.

## Première extraction — 29 oct. 2026

```
.venv/bin/python legal/instance/outils/extraire_pieces.py \
  --sortie ~/Documents/Pieces_505-17-016235-261_2026-11-06 --ecrire
```

| | |
|---|---|
| cotées en juillet sélectionnées | 268 |
| exclues | 1 — P-86, décision du 26 oct. |
| attendues | 267 |
| **produites** | **260** — 902 fichiers, 274 Mo |
| à rendre | 7 — P-58 à P-64 (`ChatSequence` : transcription à produire) |
| en échec | **0** |

**Vérification indépendante du script** : `shasum -a 256 -c SHA256SUMS`, 902
lignes sur 902 « OK ». Aucun temporaire résiduel.

- **735 photographies**, toutes qualifiées « dérivé en base ». EXIF identique
  entre la source et la copie pour chacune ; 536 portent `DateTimeOriginal`,
  les autres n'en portent pas, ni dans la source ni dans la copie (captures
  d'écran notamment).
- **167 autres fichiers** (`.eml`, `.pdf`) : l'égalité des empreintes les couvre.
- **Courriels** : la plupart viennent de `eml_file_path`, `eml_file` étant vide.
  Chaque repli est consigné au manifeste.

Manifestes versés dans `legal/instance/sortants/2026-11-06_communication_pieces/`.
Les fichiers eux-mêmes restent dans `~/Documents`, hors Git.

**Limites de cette version** : pas de reprise dans un dossier déjà rempli (il
faut un dossier neuf) ; pas de tests unitaires ; aucun rapprochement de
provenance au moment de l'extraction (fait une fois le 29 oct., ci-dessus).
