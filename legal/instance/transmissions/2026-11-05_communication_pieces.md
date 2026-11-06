# Transmission figée — communication des pièces du 5 novembre 2026

> **Archive en lecture seule.** `~/Documents/Transmis_505-17-016235-261_2026-11-05/`
> — 920 fichiers, 277 Mo, `chmod a-w` appliqué le 6 nov. 2026 à 7 h 55.
> Le dossier n'est pas versionné : les 276 Mo de pièces sont hors dépôt. **Ce
> fichier-ci est la trace dans le dépôt** ; l'archive en est la matière.

## 1. Ce qui a été transmis, et à qui

| | Élise Marie Ayoub | Me Patricia Timmons |
|---|---|---|
| Adresse | `elise.ayoub@gmail.com` | `patricia.timmons@farpbq.ca` |
| Heure (en-tête `Date`) | **5 nov. 2026, 9 h 34 min 30 s** −0500 | **5 nov. 2026, 9 h 34 min 39 s** −0500 |
| Cc / Cci | aucun | aucun |
| `Message-ID` | `CAEP=yhyGAVKXZOGJJLiRz9+ZPJhRXpHiHvamgvhHG-94dVh_5A@mail.gmail.com` | `CAEP=yhydP705vrNr9wuhna473XF=jcLMeKVxN_1sjVAxmwbYQQ@mail.gmail.com` |
| Destinataire au dossier | `DestinataireInstance` **1** | `DestinataireInstance` **3** |

**Le fondement** : art. 145 al. 1 C.p.c. ; rubrique 36 de la proposition de
protocole révisée (6 nov.) — la communication est faite **la veille**.

## 2. Le contenu de l'archive

| Dossier | Contenu |
|---|---|
| `pieces_transmises/` | **913 fichiers** : les 911 pièces sous 105 cotes, `00_Index_des_pieces.pdf`, `SHA256SUMS`. Contrôle au gel : **911 / 911 conformes** |
| `messages/` | les trois `.eml` réellement envoyés, octets bruts de l'API Gmail |
| `bordereaux/` | les deux bordereaux **transmis** et les deux **estampillés** |
| `SHA256SUMS_ARCHIVE` | empreinte des **920** fichiers de l'archive. Contrôle au gel : **920 / 920** |

### Les messages archivés

| Fichier | Octets | SHA-256 |
|---|---|---|
| `2026-11-05_0934_elise.eml` | 338 540 | `33a7a278c6ad8eba65362d4be56d8017…` |
| `2026-11-05_0934_timmons.eml` | 340 049 | `651b31aecf8523470a9b769c6a5d4094…` |
| `2026-11-06_0752_timmons_bordereau-estampille.eml` | 122 011 | `661aa49c255fca8aae5a57e91d1b0f53…` |

### Les quatre fichiers joints aux envois

| Fichier | Octets | SHA-256 | Vérifié sur |
|---|---|---|---|
| `00_Index_des_pieces.pdf` | 118 259 | `4100b9ab51d0da6d…` | le message envoyé |
| `SHA256SUMS` | 77 658 | `6ff86e517a8874f5…` | le message envoyé |
| bordereau d'Élise | 45 392 | `ada8efa20adbcfe3…` | le message envoyé |
| bordereau de Me Timmons | 45 464 | `1fd15a90a48407c7…` | le message envoyé |
| bordereau estampillé, Me Timmons | 55 301 | `792f8e5f30034530…` | le suivi du 6 nov. |

Chacun a été comparé **au MIME brut du message parti**, non au brouillon.

## 3. Le véhicule

Lien Google Drive public, lecture seule, sans compte ni inscription —
dossier `13KX_CS_kOGxymtnNYnJ3_WQMYqwL-GXs`, permissions vérifiées
(`anyone`/`reader` + propriétaire seul). Dépôt contrôlé **par aller-retour** :
téléchargement complet depuis Drive, puis `shasum -c` — 911 / 911
(`communication_pieces.md` § 30).

⚠️ **Ne pas révoquer le partage** avant confirmation de téléchargement par les
deux destinataires.

Pour Me Timmons, une seconde voie a été employée le 5 nov. : **Secure Exchanges**,
la plateforme du Fonds d'assurance, à la demande de son adjointe. Téléversement
terminé, envoi automatique, aucun accusé émis. Capacité établie : **2 Go**
(§ 32).

## 4. ✅ Inscription au journal, et le défaut qui l'a motivée

**Transmissions `T8` (Élise) et `T9` (Timmons)**, inscrites le 6 nov. 2026, avec
leurs quatre fichiers et leurs empreintes.

L'inscription est **a posteriori** et le dit : l'envoi a été fait **hors du
mécanisme** `preparer_transmission` / `confirmer_transmission` — les bordereaux
ont été rédigés à la main, sans numéro de transmission, contrairement aux T2
à T7. Les cinq attestations sont portées **rétrospectivement** par le demandeur,
dans ses mots : « Tout a été fait en bonne et due forme, seulement pas noté ».
L'horodatage vient de l'en-tête `Date` des messages, non d'une horloge locale.

**Le prix de cet écart**, consigné dans l'entrée : les deux bordereaux transmis
portaient « [HEURE — à estampiller] » au lieu de l'heure exigée par l'art. 134.
C'est exactement ce que le mécanisme existait pour empêcher.

**Curé des deux côtés**, par envoi du bordereau estampillé :

| | Envoyé le | Bordereau |
|---|---|---|
| Me Timmons | 6 nov., **7 h 52 min 34 s** | 55 301 o, `792f8e5f…` |
| Élise | 6 nov., **8 h 21 min 30 s** | 54 589 o, `ea434b72…` |

Les deux vérifiés sur le message parti par `outils/verifier_envoi.py`.

## 5. Vérifier un envoi, désormais

`legal/instance/outils/verifier_envoi.py` prend un identifiant Gmail et compare
chaque pièce jointe **du message réellement parti** à son original :

    python legal/instance/outils/verifier_envoi.py --message-id <id> \
        --attendu SHA256SUMS=~/Documents/Envoi_.../SHA256SUMS

Il détecte en particulier la conversion de texte par un client de bureau, qui a
failli faire partir un `SHA256SUMS` inutilisable (§ 31.2 de
`communication_pieces.md`).
