# Modéliser l'instance en base — évaluation

> **Demande du 13 octobre 2026** : une nouvelle application Django (ou une
> architecture plus OOP) modélisant l'ensemble, avec une vue sur l'état et la
> possibilité d'interagir avec les éléments du protocole. Avantage perçu : les
> pièces sont déjà en base, tous les documents peuvent l'être, et la base permet
> de lier chaque élément de support à chaque allégation, position ou demande.
>
> **Évaluation seulement. Rien n'a été implémenté, aucun modèle, aucune
> migration.**
>
> **Verdict en une phrase : l'intuition sur la base est juste, mais elle vise le
> mauvais objet.** Le protocole ne la mérite pas ; l'acte amendé et ses appuis,
> oui — et c'est à moitié bâti.

---

## 1. La prémisse est déjà réalisée, en partie

Le lien **support → allégation** que la demande décrit comme un avantage à venir
**existe et il est peuplé** :

| Lien | Modèle | État |
|---|---|---|
| allégation → cote citée | `case_manager.AppuiDepotJuillet` | **515 lignes** |
| acte → paragraphes → énoncés | `document_manager` : `Document` → `LibraryNode` (treebeard) → `Statement` | acte déposé = doc 9, 371 nœuds, 287 statements |
| énoncé réutilisable entre actes | `Statement`, générique | 20 statements déjà partagés |
| courriels, fils, pièces, photos, événements | `email_manager`, `pdf_manager`, `photos`, `events` | peuplés |
| envois et bordereaux | `case_manager.Transmission` | créé le 13 oct. |

➜ Ce n'est donc pas « est-ce possible ». C'est **« qu'est-ce qui manque, et
est-ce que ça vaut le détour »**.

## 2. Le critère qui tranche : traversé une fois, ou accumulé ?

C'est la ligne de partage, et elle sépare proprement les quatre objets en jeu.

| Objet | Nature | Verdict |
|---|---|---|
| **Les 9 étapes de l'instance** | **traversées une fois chacune**, en deux ans | ❌ ne pas modéliser |
| **Les délais** | **calculés** depuis des événements qui, eux, accumulent | ✅ oui — mais c'est une fonction, pas une application |
| **Les 9 points du protocole** | négociés sur six semaines, puis **gelés** | 🟡 un document, pas un modèle — § 4 |
| **Acte amendé ↔ appuis** | **accumule**, et se reconstruit entièrement | ✅ **c'est là que la base paye** — § 5 |

**Pourquoi les étapes ne méritent pas un modèle.** Neuf lignes, visitées une fois
chacune, sur deux ans. Une table dont on met à jour une colonne neuf fois n'est
pas un problème de base de données. `carte_de_l_instance.md` suffit, et se lit
sans requête.

**Pourquoi les délais, si.** Ils dérivent d'événements déjà en base
(signification, réponses, dépôt du protocole). Un délai **calculé** ne peut pas
dériver ; un délai recopié, si — et le dossier a déjà vu trois dérives de ce
genre : la falaise corrigée de 19 à 23 septembre, les 47 paragraphes qui
divergent entre le `.md` et l'imprimé, les trois adresses successives de la
seconde défenderesse. Mais c'est **une fonction sur des données existantes**,
pas une application.

## 3. Ce que coûte l'application, et contre quoi

| | |
|---|---|
| **Coût** | modèles + migrations + vues + gabarits + peuplement, soit plusieurs jours |
| **Concurrence** | la réécriture intégrale est le chemin critique, et l'art. 173 al. 3 vient d'établir que manquer le protocole du 1er novembre coûte **66 jours** de mise en état et la discrétion du tribunal de prolonger |
| **Durée de vie de l'objet visé** | le protocole est accepté puis **s'impose aux parties** (art. 150 al. 2) et ne se modifie plus sans l'accord du tribunal |

⚠️ **C'est le point décisif du calendrier** : construire l'outil du protocole
pendant les six semaines où il faut écrire le protocole, c'est dépenser le temps
de l'objet sur son contenant.

## 4. Le protocole : pourquoi un document, et non un modèle

L'argument en faveur du modèle est réel, et il faut le dire avant de l'écarter :
l'art. 148 **énumère** les neuf points. Le schéma est donné par la loi, il n'y a
rien à concevoir — c'est le cas idéal pour modéliser. Et la négociation est
relationnelle : *point × partie × position × version*.

Trois faits l'emportent malgré tout :

1. **Le volume est minuscule.** Neuf points, deux parties, deux ou trois rondes.
   Quelques dizaines de cellules. `protocole_instance.md` porte déjà les neuf
   positions avec leurs motifs ; ce qu'il ne porte pas encore — les leurs —
   arrivera dans **un seul document**, bientôt.
2. **L'objet gèle.** Après acceptation, il ne bouge plus qu'avec l'accord du
   tribunal. Un modèle conçu pour suivre des versions n'aura presque rien à
   suivre.
3. **Le risque est dans le contenu, pas dans la tenue.** Ce qui peut mal tourner,
   c'est de remplir les cases laissées en blanc par leur projet, ou d'y engager
   un délai intenable. Un modèle ne protège d'aucun des deux.

➜ **Ce qui aiderait réellement au protocole** n'est pas une application : c'est
une **grille de lecture à neuf lignes** — leur position, la nôtre, l'écart,
ce qui ne se concède pas — posée en face de leur projet quand il arrivera. Une
page.

## 5. Là où la base paye vraiment — et c'est déjà engagé

**L'acte amendé et ses appuis.** C'est l'objet qui accumule, qui se reconstruit
entièrement, et dont la tenue à la main dériverait à coup sûr.

[`suivi_paragraphes_en_base.md`](suivi_paragraphes_en_base.md) l'a déjà établi :
la numérotation y est **calculée** et non stockée, un `Statement` est
réutilisable entre actes et l'est déjà, `AppuiDepotJuillet` porte le lien
cote ↔ allégation pour le dépôt. **Il manque un seul champ** — `derive_de` — pour
que les deux balayages de concordance deviennent trois requêtes.

➜ **C'est exactement la capacité que la demande décrit** — « lier chaque élément
de support à chaque allégation » — **appliquée à l'objet qui en a besoin**, et
sur le chemin critique plutôt qu'à côté.

## 6. La vue — séparable, et c'est elle qui vaut le détour

Le souhait de **voir l'état** ne dépend ni d'une nouvelle application ni d'un
modèle d'étapes. Toutes les données existent :

| Ce qu'on verrait | D'où ça vient |
|---|---|
| Étape courante, prochaine échéance | `carte_de_l_instance.md` + dates calculées |
| Qui reçoit, et où, aujourd'hui | `DestinataireInstance` |
| Dernier écrit entrant, dernier sortant | `Email`, `Transmission` |
| Pièces communiquées / restantes | `BordereauDepotJuillet`, `FichierTransmis` |
| Obligations en cours et en retard | `echeancier.md` § 3 |

**Une vue en lecture seule sur des données existantes**, sans modèle nouveau.
Coût : faible. Durée de vie : les deux ans de l'instance. C'est le meilleur
rapport des quatre objets.

## 7. Sur « une architecture plus OOP »

Le projet a déjà un étagement qui tient : modèles → `*_service.py` → commandes de
gestion, avec des mixins transverses (`ExhibitableMixin`, `ChampsEditables`). Les
commandes `verifier_*` / `audit_*` forment un motif cohérent et lisible.

Une couche d'objets supplémentaire ajouterait de l'indirection sans ajouter de
capacité. ⚠️ Et elle coûterait là où ce dossier ne peut pas se le permettre :
**en lisibilité**. Ce dépôt est public et sera relu — par le demandeur dans six
mois, peut-être par d'autres. Le motif actuel se lit.

## 8. Synthèse

| Proposition | Verdict | Motif |
|---|---|---|
| Application « instance » avec modèle d'étapes | ❌ | neuf lignes traversées une fois ; le Markdown suffit |
| Protocole modélisé et interactif | 🟡 → **non maintenant** | volume minuscule, objet qui gèle, et le risque est dans le contenu |
| Délais calculés depuis les événements | ✅ | une fonction, pas une application ; supprime une classe d'erreur attestée |
| **Appuis de l'acte amendé** | ✅✅ | **l'objet qui accumule, sur le chemin critique, à moitié bâti** |
| **Vue en lecture seule sur l'état** | ✅ | aucun modèle nouveau, deux ans d'usage |
| Couche OOP supplémentaire | ❌ | indirection sans capacité, coût en lisibilité |

**Ordre si l'on décide d'avancer** : la vue (faible coût, usage immédiat) → le
champ `derive_de` (chemin critique) → les délais calculés. L'application d'étapes
et le protocole modélisé ne figurent pas dans cet ordre.

---

⚠️ **La demande est tronquée** : elle s'arrête sur « il serait possible, ». Cette
évaluation porte sur ce qui a été écrit. Ce qui manque n'est pas évalué.
