# Pièce — Thread 94 / email-377 (Johanne Bazinet → LP, 4 janvier 2014) — « As tu eu des nouvelles des enfants à Cuba? »

> **Source de vérité** (règle `feedback-piece-extraction-workflow`). `EmailThread` id=94 (thread_id `1435de7fea31c2a4`), objet « _MG_0053 Nicolas qui vient de sortir du ventre de sa maman ». Correspondants : Louis Philippe David ↔ Johanne Bazinet (mère de LP). Cinq courriels, id=376 à 380.
>
> La fiche couvre le courriel de la mère (email-377) **et** la réponse de LP (email-378) : le texte de 377 n'est attesté que par la citation qu'en fait 378 (voir « Défaut de la base »).

**Note de LP sur le fil** (`EmailThread.note`) : « Ce fils de discussion documente que la demanderesse partait seule en vacance a Cuba avec les enfants ».

---

## Le fil

| Email | Date base (UTC) | Heure locale (HNE) | De → À | Contenu |
|---|---|---|---|---|
| 376 | 2014-01-04 15:38:31 | sam. 4 janv., 10 h 38 | LP → Johanne | Photo `_MG_0053.jpg` (objet : « Nicolas qui vient de sortir du ventre de sa maman ») |
| **377** | 2014-01-04 15:54:57 | **sam. 4 janv., 10 h 54** | Johanne → LP | **Souper ; « As tu eu des nouvelles des enfants à Cuba? »** |
| **378** | 2014-01-04 18:15:45 | **sam. 4 janv., 13 h 15** | LP → Johanne | **Réponse sur le souper ; rien sur Cuba** |
| 379 | 2014-01-05 03:51:21 | sam. 4 janv., 22 h 51 | Johanne → LP | « Ok je vérifie avec AC et Hugo » |
| 380 | 2014-01-06 14:01:35 | lun. 6 janv., 9 h 01 | LP → Johanne | Souper du jeudi déjà prévu ailleurs |

---

## Transcription verbatim

### email-377 — Johanne Bazinet → LP, samedi 4 janvier 2014, 10 h 54

Texte tiré de la citation dans email-378 (« On Jan 4, 2014, at 10:54 AM, Johanne Bazinet <johannebazinet@gmail.com> wrote: »), identique aux citations dans 379 et 380 :

> *« merci - pour le prochain souper pour manger le ragout, préfères tu jeudi sans les enfants ou dimanche avec les enfants.  J'ai même offert à AC d'aller chez elle si elle préfère ne pas sortir bb. quel est ton avis*
> *As tu eu des nouvelles des enfants à Cuba? »*

### email-378 — LP → Johanne Bazinet, samedi 4 janvier 2014, 13 h 15

En-tête du `.eml` : `Date: Sat, 4 Jan 2014 13:15:45 -0500`.

> *« Tu as recut les autres que je t'ai envoyées?*
>
> *Pour le souper, si on le fait chez elle je préfères y aller seul, donc Jeudi, sinon ca ne me déranges pas, Jeudi ou Dimanche.*
>
> *Tiens moi au courant! »*

(suivi de la citation intégrale de 377)

### Suite du fil (pour mémoire)

- **379** (22 h 51) : *« Ok je vérifie avec AC et Hugo »*
- **380** (6 janv., 9 h 01) : *« Salut j'avais oublier mais jeudi j'avais deja un souper de planifier...je viens de voir ça dans  mon agenda au travail... »*

Aucun des deux ne revient sur Cuba.

---

## Citations extraites

### C1 — la question de la grand-mère (email-377)
> *« As tu eu des nouvelles des enfants à Cuba? »*
- Le 4 janvier 2014, les enfants sont à **Cuba**, et LP n'y est pas : sa mère lui demande s'il a eu de leurs nouvelles, et le reste du fil le montre au Québec (souper « Jeudi ou Dimanche »).
- En base : **Quote n° 70** (régime HERITE, non certifiée), rattachée à **email-380**, qui ne contient la phrase que comme citation.

### C2 — la réponse de LP (email-378)
> *« Pour le souper, si on le fait chez elle je préfères y aller seul, donc Jeudi, sinon ca ne me déranges pas, Jeudi ou Dimanche. »*
- LP répond le jour même, à 13 h 15, **au sujet du souper seulement**. Il ne répond pas à la question sur Cuba, ni dans 378 ni dans 380.

---

## Calibration / portée

- **Ce qui est établi** : à la date du 4 janvier 2014, les enfants sont en voyage à Cuba **sans leur père**. La question de la mère le présuppose et la réponse de LP ne le conteste pas.
- **Ce qui ne l'est pas** :
  - Le courriel ne dit pas **qui accompagnait** les enfants. Il établit « seule » au sens de **sans LP**, pas au sens de **sans autre adulte** (en 2011, les parents d'Élise étaient du voyage : P-71).
  - Le **silence** de LP sur la question ne prouve pas qu'il était sans nouvelles. Une absence de réponse ne prouve pas une absence de contact (`feedback-evidentiary-calibration`). C'est un fait du fil, pas une preuve de l'état de LP.
- **Premier repère daté du voyage à Cuba de l'Épisode 1** de [piece_vacances_2013_cape_cod_cuba_chalet.md](piece_vacances_2013_cape_cod_cuba_chalet.md) (fait 5 : « Élise est partie à Cuba avec les enfants », sans date ; le voyage que le courriel du 11 juin 2013 renvoyait à après l'éviction : « Cela peut attendre ! »). ⚠️ **À vérifier auprès de LP** : s'il s'agit du même voyage, il a eu lieu à l'hiver 2013-2014 et non à l'été 2013, et la ligne « Été 2013 | Cuba (Élise + enfants) » du tableau de cette fiche est à corriger.

---

## Défaut de la base (constaté le 17 nov. 2026)

- **Le corps de l'email-377 est faux en base.** `Email.body_plain_text` de 377 contient le texte de **379** (« Ok je vérifie avec AC et Hugo » et sa citation de 378), alors que 377 porte bien la date et le `message_id` (`1435df6e26dfa76b`) du message de 10 h 54.
- **Cause** : les deux courriels de Johanne du 4 janvier ont le même nom de fichier, `storage/Email/gmail/20140104_J_L_Re_MG_0053_Nicolas_qui_vient_de_sortir_du_ventre_de_sa_maman.eml`, sans suffixe hexadécimal. Celui de 22 h 51 a écrasé celui de 10 h 54 sur disque (en-tête restant : `Date: Sat, 4 Jan 2014 22:51:21 -0500`). Le `.eml` original de 377 n'existe plus dans `storage/`.
- **Conséquence** : le texte de 377 se certifie sur la **citation** qu'en fait email-378, qui est le `.eml` envoyé par LP (`Message-Id: <209FC875-449B-41E9-B5E5-3554F6871169@gmail.com>`). Pour produire l'original lui-même, il faut le retirer de Gmail.

---

## Renvois

[piece_vacances_2013_cape_cod_cuba_chalet.md](piece_vacances_2013_cape_cod_cuba_chalet.md) (Épisodes 0 et 1) · P-71 (Cuba, sept.-oct. 2011)
