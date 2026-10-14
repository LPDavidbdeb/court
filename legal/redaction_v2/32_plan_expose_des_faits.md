# 32 — Plan de l'EXPOSÉ DES FAITS : par actes de la partie adverse, chronologiquement

> **Décision du demandeur, 14 octobre 2026.** Deux éléments, et ils sont
> distincts :
>
> 1. **Périmètre.** La modification porte **uniquement sur la structure de la
>    section « EXPOSÉ DES FAITS »**. Les autres sections de l'acte déposé ne
>    sont pas rouvertes.
> 2. **Principe organisateur.** Le plan se fait **par actes de la partie
>    adverse, de manière chronologique** : d'abord la requête de novembre 2015,
>    ensuite la déclaration assermentée de 2019, enfin la dénonciation d'un
>    moyen déclinatoire.
>
> C'est la décision que `legal/METHODOLOGIE_POST_DEPOT.md` § 4.1 réservait au
> demandeur. Elle est prise pour cette section. Elle remplace, pour l'exposé
> des faits, la question ouverte au [31](31_etat_du_plan_de_redaction.md) § 4.1.

**État du plan — précisions du demandeur, 14 octobre 2026.** Ce document
consigne la **structure de rédaction de la nouvelle requête**, pour la section
« EXPOSÉ DES FAITS ». Cette structure est **incomplète**. Sa base est l'analyse
des trois actes de la partie adverse. Pour chacun, elle comprend **une
démonstration majeure complexe et plusieurs démonstrations plus simples**.
Les **trois démonstrations complexes sont désormais précisées** (§§ 5.1, 5.4
et 5.6); **aucune démonstration simple n'est précisée à ce stade** (§ 5.0).

**Continuité des réponses.** Avant toute nouvelle évaluation des
démonstrations, consulter le **§ 5.7 — Objections déjà examinées** et appliquer
sa règle de consultation et de réouverture.

---

## 1. Les trois axes, dans l'ordre retenu

| Rang | Acte | Date | Auteur de l'acte | Cote | Objet en base |
|---|---|---|---|---|---|
| **1** | Requête en garde, fixation de pension et ordonnance de sauvegarde | 19 nov. 2015 | Me Adélia Ferreira | **P-19** | `document:1` |
| **2** | Déclaration assermentée de la demanderesse | 21 oct. 2019 | Me Marie-Josée Ayoub | **P-42** | `document:3` |
| **3** | Dénonciation de la défenderesse d'un moyen déclinatoire | 21 juil. 2023 | Élise Marie Ayoub | **P-40** | `document:2` |

L'ordre des `pk` en base (1, 3, 2) n'est pas l'ordre chronologique. **L'ordre
du plan est 1 → 3 → 2.** Ne pas se laisser guider par le numéro de document.

**Ce que l'ordre chronologique par actes apporte.** Chaque acte est signé,
daté, et attribuable à une personne nommée. L'axe du plan devient une
**séquence d'actes posés**, et non une suite de périodes où il faut d'abord
établir ce qui s'est passé avant de dire ce qui est reproché. La cible et le
reproche se tiennent au même endroit.

**Ce que l'autorat est, et n'est pas.** L'auteur de chaque acte est un fait,
jamais un maillon de la démonstration. Me Ferreira demeure hors de la chaîne
de concert alléguée (`PROJECT_CONTEXT.md`; `../instance/regle_prudence_Ferreira_P20.md`).

---

## 2. Le périmètre exact dans l'acte déposé

La section visée est **`§ II — EXPOSÉ DES FAITS`**, nœud **`898`** du
`document:9` (acte déposé, `numbering_mode = STORED`), numéro de section
résolu **III**.

| | |
|---|---|
| Nœuds du sous-arbre, racine incluse | **199** |
| Porteurs de texte | **168** |
| Porteurs d'un numéro résolu | **136** |
| Bornes | de `898` à `1096` — `1097` ouvre `§ III — LES FAUTES ALLÉGUÉES` |

### Structure actuelle — chronologique par période

| | Sous-section | Nœud | Descendants |
|---|---|---|---|
| A | LA VIE FAMILIALE ET L'IMPLICATION PARENTALE AVANT LA RUPTURE | `899` | 58 |
| B | LA RUPTURE ET LES POSITIONS ÉCHANGÉES EN 2015 | `958` | 23 |
| C | LA REQUÊTE ASSERMENTÉE DU 19 NOVEMBRE 2015 | `982` | 42 |
| D | LE JUGEMENT DU 14 JANVIER 2016 ET LES ÉCRITS POSTÉRIEURS | `1025` | 15 |
| E | LA MODIFICATION DE LA PENSION ET LES REPRÉSENTATIONS DE 2019 | `1041` | 34 |
| F | LES CONSÉQUENCES DOCUMENTÉES EN 2020 | `1076` | 6 |
| G | LA DÉNONCIATION ASSERMENTÉE DU 21 JUILLET 2023 | `1083` | 7 |
| H | LES PERTES ALLÉGUÉES ET LE SOLDE RELEVÉ EN 2026 | `1091` | 5 |

**Ce que le changement de principe déplace.** Les trois actes sont **déjà**
des sous-sections — C, E et G. Mais ils sont intercalés entre des
sous-sections de période (A, B, D, F, H), de sorte que l'axe réel du texte
déposé reste le temps, non les actes. Le nouveau principe fait des trois
actes l'**ossature**, et oblige à décider, pour chacune des cinq autres
sous-sections, à quel acte sa matière se rattache — ou si elle sort de
l'exposé.

⚠️ **Ce rattachement n'est pas fait et n'est pas présumé ici.** C'est le
premier travail du plan (§ 5).

---

## 3. Confirmation demandée — oui, les paragraphes des trois actes sont identifiables

**Oui**, et par un chemin vérifié. Il n'y a pas de clé étrangère
`Statement → Document` : le lien passe par l'arbre `treebeard`.

```python
from document_manager.models import Document
from document_manager import numerotation

d = Document.objects.get(pk=1)                    # 1 = P-19, 3 = P-42, 2 = P-40
noeuds = list(d.nodes.all().order_by('path'))     # LibraryNode, chemin matérialisé
idx = numerotation.index_par_noeud(d)             # nœud.pk → NumeroResolu
for n in noeuds:
    numero = idx.get(n.pk)
    texte = numerotation.texte_du_noeud(n)
    statement = n.content_object                  # GenericFK → Statement
```

**Trois mises en garde sur ce que le numéro vaut.**

1. **Les trois actes sont en `numbering_mode = AUTO`** : leur numéro est
   **recalculé** depuis la profondeur du nœud et le schéma du document. Ce
   n'est pas un numéro conservé depuis le papier — contrairement au
   `document:9`, qui est en `STORED` précisément parce que son papier porte
   des numéros qu'aucune règle ne retrouve.
2. **La concordance avec le corpus a été vérifiée, pas supposée.** Les
   références que le corpus emploie depuis des mois tombent exactement sur
   les nœuds attendus :

   | Référence du corpus | Nœud | Texte vérifié |
   |---|---|---|
   | P-19 § 4 | `7` | « La continuation de la vie commune étant devenue impossible… 23 février 2015 » |
   | P-19 § 5 | `8` | « **En effet**, depuis la naissance d'Alexia… » |
   | P-19 § 6 | `9` | « **En effet**, le défendeur ne s'impliquait que minimalement… » |
   | P-19 § 7 | `10` | « En 2011, suite à une infidélité… » — **pas** introduit par « En effet » |
   | P-19 § 14 | `18` | « Dès la rupture, le défendeur voulait instaurer une garde partagée, que la demanderesse a refusé… » |
   | P-19 § 15 | `19` | « les enfants sont jeunes et de plus, le défendeur était rarement disponible… » |
   | P-19 § 16 | `20` | « C'est la demanderesse qui s'occupait des enfants, qui allait aux activités, etc… » |
   | P-19 § 17 | `21` | « Le défendeur aidait lorsque la demanderesse n'était pas disponible. » |
   | P-19 § 18 | `22` | « Les parties ont donc convenu que la demanderesse aurait la garde… » |
   | P-42 § 3 | `96` | « Puisque le défendeur refusait de régler le litige à l'amiable… » |
   | P-42 § 14 | `119` | « Bien que le défendeur allègue avoir envoyé plusieurs candidatures… » |
   | P-42 § 15 | `120` | « …expérience à titre d'analyste, de technicien en laboratoire et au service à la clientèle… » |
   | P-40 § 8 | `89` | « Le demandeur a fait le choix de ne pas travailler… » |

   ➜ La chaîne grammaticale **§ 4 ← § 5 ← § 6** du `08_these_substitution_des_fondements.md`
   est confirmée sur la base : le § 7 n'est pas introduit par « En effet ».

3. **Un numéro résolu n'est pas un verbatim.** Toute citation se certifie sur
   le **scan**, jamais sur la fiche ni sur l'incipit des tables ci-dessous
   (`reference_verbatim_sur_original`; `METHODOLOGIE_POST_DEPOT.md` § 9.2). Les
   scans sont liés par `Document.file_source` et se lisent avec `fitz` à
   100 ppp, puis 300 ppp sur le paragraphe visé.

---

## 4. Trois écarts relevés — tranchés par le demandeur le 14 octobre 2026

Les trois points relevés au relevé initial ont été tranchés le jour même. Leur
formulation d'origine est conservée au § 4 bis.

### 4.1 Date de P-19 — **19 novembre 2015, et c'est la date de l'assermentation**

> **Demandeur, 14 octobre 2026** : « Pour P-19, nous n'avons pas la date de
> rédaction, seulement celle de l'assermentation et c'est le 19 novembre 2015. »

Deux conséquences, et il faut les tenir séparées.

1. **La date de rédaction de P-19 est inconnue.** Elle n'est pas « probablement
   proche » du 19 novembre : elle n'est pas au dossier. Aucun raisonnement ne
   peut s'appuyer sur un délai entre la rédaction et le serment, dans un sens
   ou dans l'autre.
2. **Le 19 novembre 2015 est la date du serment**, non celle de la rédaction ni
   celle de la présentation. C'est la date que porte le verrou des cotes et
   tout le corpus. Elle est exacte, et sa qualification l'est aussi : ce qui
   est daté, c'est l'**acte d'affirmer solennellement**.

➜ **Ce qui est utile, et qui est déjà la thèse.** Ce que P-19 réalise, c'est
l'affirmation sous serment. La date de ce serment est précisément la date
pertinente. L'ignorance de la date de rédaction ne retire rien — elle écarte
seulement une inférence qui n'était pas disponible.

⚠️ **Le champ `document_original_date` du `document:1` porte `2015-11-27`.**
Cette valeur n'a pas de source identifiée au dossier et **contredit le
référent établi**. Ne jamais la reprendre. La base n'est pas corrigée ici :
une mutation sur un acte de la partie adverse ne se fait pas sans décision
expresse, et il reste à savoir si ce 27 novembre provient de l'acte (une date
de présentation, par exemple) ou d'une saisie sans source.

### 4.2 Le doublon — **la requête compte 66 paragraphes; le 67e est une erreur de transcription**

> **Demandeur, 14 octobre 2026** : « le doublon est un détail, la requête
> contient 66 paragraphes donc le 67 est une erreur de transcription, mais il
> n'affecte rien dans notre travail, l'éliminer ne sert aucune fonction. »

**Décompte confirmé sur la base.** 77 nœuds hors titre = 67 au niveau du
paragraphe + 10 sous-items. Retirer le 67e donne **66**.

**Pourquoi il n'affecte rien, et c'est vérifiable.** Le nœud surnuméraire est
le **dernier** du document (`78`). Un numéro dupliqué en fin de suite ne décale
rien : **les §§ 1 à 66 portent tous leur numéro réel.** Si le doublon s'était
trouvé au milieu, tout l'aval serait décalé et chaque référence du corpus
serait à revérifier.

➜ **Ne pas l'éliminer.** Aucune fonction, et une suppression dans un acte de la
partie adverse est un geste qui se défend mal pour un gain nul. **Règle de
travail : ne jamais citer un « § 67 » de P-19.** Le dernier paragraphe de la
requête est le **§ 66**.

### 4.3 Les sous-items — **des ajouts qui ne figurent pas dans la requête**

> **Demandeur, 14 octobre 2026** : « Les sous-items sont des ajouts qui
> n'apparaissent pas dans la requête. »

Les dix nœuds de niveau inférieur du `document:1` — `4`, `5`, `11`, `32`, `38`,
`47`, `63`, `64`, `65`, `68` — **ne sont pas des paragraphes de l'acte**. Ils
procèdent du travail de lecture, non de la requête.

➜ **Règle de travail, absolue.** **Aucun sous-item ne se cite comme paragraphe
de P-19.** Ni « § 7a », ni « § 27a », ni « § 32a », ni « § 40a », ni « § 57a »,
ni une lettre sous les §§ 2 et 55. La matière d'un sous-item appartient au
paragraphe qui le porte, et se cite sous le numéro de ce paragraphe.

| Sous-item | Se cite sous |
|---|---|
| `4`, `5` | **§ 2** |
| `11` | **§ 7** |
| `32` | **§ 27** |
| `38` | **§ 32** |
| `47` | **§ 40** |
| `63`, `64`, `65` | **§ 55** |
| `68` | **§ 57** |

⚠️ **La distinction par la puce imprimée ne tient pas ici.** Le schéma de
numérotation traite une puce présente dans le texte comme l'indice d'une
énumération propre à l'acte (`numerotation.RE_PUCE`). Les nœuds `4`, `5` et
`63`-`65` portent « a) », « b) », « c) » **dans leur texte** et étaient donc
lus comme des énumérations de la requête. La réponse du demandeur écarte cette
lecture pour P-19. **L'indice est donc faillible** : il mesure la présence d'un
caractère, pas l'origine du découpage.

➜ **Reste à vérifier, et ne pas étendre par analogie** : les sous-items `100`
à `106` du **P-42** (6a-6g) sont cités dans le corpus sous la forme
« § 6 c) ». La réponse ci-dessus porte sur la **requête**. Le statut des
sous-items de P-42 et de P-40 (`85`, `86`) n'est pas tranché par elle et doit
l'être séparément, sur le scan.

### 4.4 Ce que les deux règles périment dans le corpus

Les règles des § 4.2 et § 4.3 ne sont pas des points de forme : le corpus cite
un « § 67 » et un « § 57a » de P-19 qui ne sont pas des paragraphes de l'acte.
Balayage fait le 14 octobre 2026.

**a) Le « § 57a ».** C'est le nœud `68` — « Lui seul peut bénéficier d'utiliser
le service lorsqu'il a les enfants et refuse de payer la différence non
couverte par les assurances. » Le texte existe; il appartient au **§ 57**.

| Fichier | Ce qui y est écrit |
|---|---|
| `legal/ponts_requete_2015_consolides.md` (≈ 1561-1583) | « §57a » traité comme une allégation distincte du § 57, avec ses deux branches et sa propre évaluation |
| `legal/these_refus_garde_partagee.md` (70, 74, 86) | « §57a » au tableau de réfutation, puis dans « §14-18, §57a » et « §57a, §14-17 et §18 » |
| `legal/inventaire_allegations_blocage.md` (16) | « §57a-2 » — **cas fondateur de la grille** du refus sans référent |
| `legal/compilation_griefs.md` (1232) | « §57a *(stmt 68)* » cité comme énoncé |

⚠️ **Ce qui change et ce qui ne change pas.** Les deux propositions demeurent
dans l'acte, et la réfutation de chacune demeure valable : le monopole allégué
et le refus de payer la différence sont bien dans le texte du § 57. Ce qui
tombe est leur **statut de paragraphe autonome**. Conséquences :

- un énoncé se cite désormais **« P-19 § 57, seconde proposition »**, jamais
  « § 57a »;
- le § 57 porte **deux** propositions, et les réfuter exige de les traiter
  **ensemble** : on ne peut plus réfuter « le § 57a » en laissant « le § 57 »
  debout. Le prédicat à variable supprimée vit à l'intérieur du § 57;
- la grille du refus sans référent conserve son cas fondateur — c'est le même
  texte — mais son adresse change.

**b) Le « § 67 ».**

| Fichier | Ce qui y est écrit |
|---|---|
| `legal/piece_document-1.md` (170) | « **§67** — … *(doublon de §66)* » — le doublon y était déjà repéré |
| `legal/ponts_requete_2019_consolides.md` (249) | « Aux §66 et §67, la Requête affirme… » |
| `legal/pont/pont_par3_2019.md` (235) | même phrase |
| `legal/redaction_v2/01_cible_these_adverse.md` (52) | ✅ **corrigé le 14 oct.** : *intérêt* = **2** (§14, §66), et le relevé lexical porte sur **66** paragraphes |

⚠️ **Le cas de `01_cible_these_adverse.md` était le seul à conséquence
plaidable** : il annonçait trois occurrences du mot « intérêt » dans l'acte
alors qu'il y en a **deux**, la troisième étant le doublon. Un compte avancé
contre un acte adverse doit tomber juste. Recompté sur la base, hors sous-items
et hors doublon : *stable* 1 (§ 25), *intérêt* **2** (§§ 14, 66), « En effet » 3
(§§ 5, 6, 15), « donc » 2 (§§ 18, 34), « Conséquemment » 1 (§ 26) — **un seul
compte changeait.**

➜ **« Aux §66 et §67 » doit se dire « au § 66 ».** L'affirmation est faite une
fois, pas deux. La présenter deux fois surexpose un énoncé qui se tient très
bien une seule.

### 4.5 Ce qui n'est pas corrigé, et pourquoi

Les fichiers nommés au § 4.4 **hors de `redaction_v2/`** ne sont pas modifiés :
la règle absolue de l'atelier l'interdit, et la base de la première demande
demeure le point de repli ([00](00_README.md)). La correction s'écrit **ici**,
avec le renvoi — c'est le régime prévu.

Ce qui reste donc à faire, et qui n'est pas fait :

1. reprendre ces renvois **lorsque leur matière entre dans la nouvelle
   rédaction**, sous la bonne adresse — et non par une passe de correction du
   corpus;
2. trancher le statut des sous-items de **P-42** (`100`-`106`, cités au corpus
   sous la forme « § 6 c) ») et de **P-40** (`85`, `86`). La réponse du
   demandeur porte sur la **requête**; elle ne s'étend pas par analogie.

---

---

## 4 bis. Formulation initiale des trois écarts — conservée

> **Périmée par le § 4.** Conservée parce qu'elle montre ce que la base
> laissait croire : que la puce imprimée distinguait l'énumération de l'acte
> de la scission de la lecture, et que la date de la base pouvait être celle
> de la présentation. Les deux lectures sont écartées pour P-19.

| | Écart | Ce qu'il faut faire |
|---|---|---|
| a | **Date du `document:1`.** La base porte `document_original_date = 2015-11-27`. Le verrou des cotes et tout le corpus portent **19 nov. 2015**. Les deux ne peuvent pas être vrais | Vérifier sur le scan laquelle est la date de l'assermentation et laquelle celle de la présentation. Ne pas écraser le référent du corpus par la donnée de la base |
| b | **Doublon au `document:1`.** Les nœuds `77` (§ 66) et `78` (§ 67) portent un texte **identique** : « La présente requête est formulée dans le meilleur intérêt des enfants et est bien fondée en faits et en droit. » | Vérifier sur le scan si l'acte porte réellement deux fois cette phrase ou si l'import l'a dédoublée. Un paragraphe cité par son numéro exige que la réponse soit connue |
| c | **Sous-items : énumération de l'acte ou scission de la lecture ?** Le schéma distingue les deux par la **puce imprimée dans le texte**. Portent une puce, donc énumérations de l'acte : `4`, `5` (a/b), `63`-`65` (a/b/c), `85`-`86`, `107`-`111`. N'en portent pas, donc lettre **calculée** : P-19 `11` (7a), `32` (27a), `38` (32a), `47` (40a), `68` (57a); P-42 `100`-`106` (6a-6g) | Les 6a-6g de P-42 sont cités dans le corpus sous la forme « § 6 c) », ce qui suppose que l'acte les énumère. Confirmer sur le scan avant de citer l'un des cinq sous-items de P-19 par une lettre |

---

## 5. Les trois démonstrations majeures — une par acte

> **Demandeur, 14 octobre 2026** : « la requête comporte 3 démonstrations
> majeures et complexes, une pour chaque acte. »

C'est le troisième étage du plan, et il se superpose exactement aux trois axes
du § 1 : **une démonstration majeure complexe par acte**, accompagnée de
**plusieurs démonstrations plus simples** (§ 5.0). Les trois démonstrations
complexes sont désormais précisées. L'axe dit *de quoi on parle*; la
démonstration dit *ce qu'on établit contre lui*.

| Axe | Acte | Démonstration majeure |
|---|---|---|
| **1** | Requête du 19 nov. 2015 (**P-19**, `document:1`) | **La contradiction de la thèse principale de la requête** |
| **2** | Déclaration assermentée du 21 oct. 2019 (**P-42**, `document:3`) | **La fausseté du § 3 — la saisine n'est pas l'effet d'un refus** (§ 5.4) |
| **3** | Dénonciation du 21 juil. 2023 (**P-40**, `document:2`) | **La contestation du § 8 — le choix allégué de ne pas travailler pour subvenir aux besoins des enfants** (§ 5.6) |

### 5.0 La rédaction ne se limite pas aux démonstrations majeures

> **Demandeur, 14 octobre 2026** : « la rédaction ne consiste pas uniquement de
> ce que nous avons discuté, nous discutons des éléments principaux, mais
> plusieurs autres, plus simples, demeurent, comme les paragraphes 55, 56, 57
> de la requête, que nous n'avons pas abordés dans le plan à date, mais qui
> figurent dans la démonstration. »

**Précision du demandeur, 14 octobre 2026.** Pour chacun des trois actes, la
structure comprend **une démonstration majeure complexe et plusieurs
démonstrations plus simples**. Les trois démonstrations complexes sont
précisées (§§ 5.1, 5.4 et 5.6). **Aucune des démonstrations simples n'est
précisée à ce stade.** Les §§ 55 à 57 de P-19 sont mentionnés comme exemples,
avec leurs ancrages en base; leur démonstration n'est pas exposée ici.

**Les §§ 55 à 57, cités par le demandeur — ancrage en base.**

| § | nœud | `Statement` | Texte |
|---|---|---|---|
| **55** | `62` | **`62`** | « La demanderesse considère les frais particuliers suivants : » |
| | `63` | `63` | a) les frais de santé non couverts par les assurances |
| | `64` | `64` | b) les frais de camps de jour et de service de garde |
| | `65` | `65` | c) une portion des frais d'activités, environ 2 500 $ par année |
| **56** | `66` | **`66`** | « Les enfants ont toujours été couverts par les assurances médicales et médicaments du défendeur. » |
| **57** | `67` | **`67`** | « À ce jour, le défendeur refuse que la demanderesse utilise les dites assurances lorsqu'elle achète les médicaments… » |
| | `68` | `68` | « Lui seul peut bénéficier d'utiliser le service lorsqu'il a les enfants et refuse de payer la différence non couverte par les assurances. » |

Le statut des nœuds `63`, `64` et `65` reste ouvert au § 5.3 b. Le nœud `68` se
cite sous le § 57 (§ 4.3).

---

### 5.1 Démonstration 1 — la contradiction de la thèse principale de la requête

**Le texte d'ouverture est déjà rédigé.** Le demandeur l'a transmis le
14 octobre; il est **identique, au mot**, à la partie I du
[25](25_presentation_argument_complet.md) § 2 (¶ 1 à 3). Ce n'est donc pas un
texte nouveau : c'est la **confirmation** que cette partie I ouvre la
démonstration 1.

Ce que les trois paragraphes font, dans l'ordre :

| ¶ | Fonction |
|---|---|
| **1** | Reproduit les neuf paragraphes sous serment — le matériau, sans commentaire |
| **2** | Énonce ce qu'ils expliquent **ensemble** : la séparation, le refus de la garde partagée, l'entente sur le régime de garde |
| **3** | Nomme le **socle** sur lequel le tout repose : implication minimale historique, difficulté à assumer le rôle de père, indisponibilité |

➜ **C'est le socle du ¶ 3 qui est la cible.** La démonstration ne conteste pas
d'abord les neuf paragraphes un à un : elle établit qu'ils reposent tous sur un
seul socle, puis contredit ce socle. C'est la méthode du
[09](09_methode_niveau_allegation.md) — contredire au niveau où l'allégation
est faite.

**Objections déjà examinées.** La mention du jeune âge au § 15 et celle de
l'infidélité au § 7 ont reçu les réponses consignées au § 5.7. Elles ne
remettent pas en cause la synthèse du socle parental au ¶ 3 ci-dessus.

### 5.2 Le lien base ↔ plan — les `Statement` des neuf paragraphes

> **Demandeur, 14 octobre 2026** : « enregistre le lien avec les pk des
> statements, question de faire le lien entre la base et le plan. »

Chacun des neuf paragraphes cités au ¶ 1 est un objet de la base. **C'est par
le `Statement` que le plan se raccorde**, non par le numéro de paragraphe : un
`Statement` est réutilisable entre documents, et c'est lui que
`document_manager.concordance` relie.

| § de P-19 | nœud | **`Statement`** | Ce qu'il porte dans la thèse adverse |
|---|---|---|---|
| **4** | `7` | **`7`** | La séparation — vie commune devenue impossible, départ du 23 février 2015 |
| **5** | `8` | **`8`** | « En effet » — la relation difficile depuis la naissance d'Alexia |
| **6** | `9` | **`9`** | « En effet » — **l'implication minimale** : première pierre du socle |
| **7** | `10` | **`10`** | L'infidélité de 2011, la séparation d'un an, la thérapie |
| *(§ 7, 2<sup>e</sup> proposition)* | `11` | **`11`** | **La difficulté à assumer son rôle de père** : deuxième pierre du socle |
| **14** | `18` | **`18`** | Le refus de la garde partagée, dit contraire à l'intérêt des enfants |
| **15** | `19` | **`19`** | « En effet » — le jeune âge et **l'indisponibilité** : troisième pierre |
| **16** | `20` | **`20`** | L'attribution des soins et des activités à la demanderesse |
| **17** | `21` | **`21`** | Le rôle paternel présenté comme supplétif |
| **18** | `22` | **`22`** | **L'entente alléguée** sur le régime de garde, appuyée sur « la pièce P-2 » |

⚠️ **Le `pk` du nœud et celui du `Statement` coïncident pour le `document:1`.**
C'est un effet de l'import, **pas une règle** : ailleurs ils divergent. Toujours
nommer le `Statement` quand c'est lui qu'on vise.

⚠️ **Le nœud `11` n'est pas un « § 7a ».** Il est la seconde proposition du
**§ 7** (§ 4.3). Le texte du demandeur le traite correctement : il le fond dans
le § 7, après un point. Les trois pierres du socle se trouvent donc dans les
`Statement` **`9`**, **`11`** et **`19`**.

### 5.3 Trois constats du scan — verbatim, sous-items, date

Vérification faite le 14 octobre sur `Document.file_source` du `document:1`,
16 pages, sans couche texte. ⚠️ **Le PDF est un ensemble** : la page 2 est une
lettre de Me Ferreira du 12 février 2016. La requête commence à la **page 3**.

**a) La ponctuation finale — votre citation est juste, la base est normalisée.**
Le scan porte « ; » en fin de paragraphe : « …au 23 février 2015**;** »,
« …âgée de 6 ans**;** », « …sous la cote P-1**;** ». Or les `Statement` de la
base portent « **.** » — sur **huit des neuf** paragraphes cités (seul le § 18
concorde, parce qu'il se termine réellement par un point).

➜ **Ne jamais produire un verbatim de P-19 depuis le `Statement`.** La
normalisation silencieuse que l'audit du 8 octobre avait relevée dans l'acte
déposé est **aussi dans la base**. Le texte du demandeur, lui, porte les
points-virgules : il est conforme au scan.

**b) Les sous-items — la réponse du § 4.3 doit être resserrée.** Le scan montre
que les a) et b) du § 2 **figurent dans la requête**, imprimés :

> a) Alexia David, née le 6 octobre 2009, actuellement âgée de 6 ans;
> b) Nicolas David, né le 1 février 2013, actuellement âgé de 2 ans;

Ils ne sont donc pas des ajouts. La règle « les sous-items ne figurent pas dans
la requête » vaut pour ceux que **la lecture** a créés — les nœuds `11`, `32`,
`38`, `47`, `68`, qui ne portent aucune puce. Le statut des nœuds `63`-`65`
(a/b/c des frais particuliers, § 55) n'est pas vérifié : ils sont dans la même
forme imprimée que les a) et b) du § 2, donc probablement eux aussi dans
l'acte. **À confirmer avant de s'en servir.**

➜ Ce qui demeure entier et ne change pas : **aucun sous-item ne se cite comme
un paragraphe numéroté distinct**, ni « § 7a » ni « § 57a ». Qu'un a) soit
imprimé sous le § 2 n'en fait pas un paragraphe : il fait partie du § 2.

**c) La date de la base a une source — le tampon du greffe.** La page 3 porte,
au bord droit, un tampon vertical **« Palais Justice Longueuil »** suivi de
**« 2015-11-2? »**, dernier chiffre tronqué au bord de la page. C'est
vraisemblablement l'origine du `document_original_date = 2015-11-27`.

➜ **Cela confirme la correction du demandeur au lieu de l'infirmer.** Le
2015-11-27 n'est ni la rédaction ni le serment : c'est un **tampon de greffe**.
La date qui qualifie l'acte demeure celle de l'**assermentation, le 19 novembre
2015** (§ 4.1). Le champ reste à requalifier plutôt qu'à corriger.

### 5.4 Démonstration 2 — la fausseté du § 3 de la déclaration de 2019

> **Demandeur, 14 octobre 2026** : « l'autre démonstration complexe est en lien
> avec le paragraphe 3 et 4 (4 sert de contexte à 3). Le paragraphe 3 attribue
> la cause de la saisine du Tribunal au refus du défendeur de régler à l'amiable
> et affirme que ce sont les droits des enfants qui furent défendus devant le
> tribunal. »

**La cible, et son contexte.**

| § de P-42 | nœud | **`Statement`** | Texte |
|---|---|---|---|
| **3** | `96` | **`96`** | « Puisque le défendeur refusait de régler le litige à l'amiable, j'ai été obligée de saisir le Tribunal afin de faire valoir les droits de nos enfants » |
| **4** | `97` | **`97`** | « Le 14 janvier 2016, l'Honorable Sophie Picard, J.C.S. prononçait un jugement, lequel me confiait la garde de nos enfants et des droits d'accès au défendeur tous les dimanches de 16h00 à 20h00 » |

Le § 3 porte **deux** affirmations, qu'il faut tenir distinctes : une **cause**
(le refus de régler) et une **finalité** (faire valoir les droits des enfants).
Le § 4 ne les démontre pas : il fournit le **résultat**, et sert de contexte en
montrant ce que la saisine a produit.

#### La thèse du contre-argument au § 3

> **Demandeur, 14 octobre 2026** : « note ceci comme étant la thèse du
> contre-argument du paragraphe 3. Le plan de juin 2013, les négociations de
> 2015 et la requête de novembre 2015 sont, à leur façon distincte, une
> instanciation de cette thèse. »

**Énoncé gouvernant**, dans les mots du demandeur :

> La garde exclusive était un objectif poursuivi depuis juin 2013, là où
> l'art. 33 C.c.Q. n'en fait qu'un moyen. Ce moyen a été maintenu après le
> constat qu'il n'était pas indiqué par la situation des enfants. Ainsi
> maintenu, il devenait inaccessible par entente : un père qui connaissait la
> situation de ses enfants ne pouvait se voir opposer aucune représentation de
> cette situation. Il ne restait que le forum qui, ne connaissant pas les
> enfants, dépend entièrement de ce que les parties lui en disent. La saisine
> n'est donc pas l'effet d'un refus : elle est, avec le désaccord que le §3
> nomme « refus », le second effet d'une même cause — l'incompatibilité entre
> les conclusions recherchées et la réalité des enfants.
>
> **Sur la finalité.** Si l'intérêt des enfants avait gouverné, ce sont les
> conclusions recherchées qui se seraient ajustées à leur situation. C'est
> l'inverse : les conclusions sont demeurées fixes, et c'est la situation —
> puis sa représentation au Tribunal — qui a été ajustée à elles, en créant
> l'état à faire ratifier (2013), en omettant les causes de cet état et la
> négociation (2015), en inventant un passé (2015). L'intérêt des enfants n'y
> est pas la fin à laquelle la demande se mesure : c'est l'argument par lequel
> elle s'obtient.
>
> **La substitution de l'intérêt.** L'instrumentalisation est la mobilisation
> d'une dimension réelle de l'intérêt de l'enfant à une fin qui lui est
> étrangère. Elle opère la substitution de l'intérêt d'un adulte à celui d'un
> enfant, dans un processus judiciaire qui tire sa légitimité de l'inverse.

⚠️ **Développement canonique hors de l'atelier.** Cette thèse est développée
dans `../instance/pont_these_trois_instances.md` et
`../instance/par3_version_plaidable.md`; l'ordre d'autorité des couches est à
`../instance/INDEX_contre_argument_par3.md`. **Ne rien réécrire sans en partir.**

#### Les quatre termes, et les trois instanciations

L'opération se décompose en **quatre termes** — c'est le « pont » :

| | Terme |
|---|---|
| **T1** | une dimension **réelle** de l'intérêt de l'enfant est mobilisée |
| **T2** | vers une **fin qui lui est étrangère** |
| **T3** | l'opération **substitue** l'intérêt d'un adulte à celui de l'enfant — coût à l'enfant, bénéfice à l'adulte, dimension non servie |
| **T4** | dans un **processus dont la légitimité repose sur l'inverse** |

**Les trois actes sont chacun une instanciation de la thèse**, à leur façon
distincte :

| | Instanciation | Mode du T4 |
|---|---|---|
| **①** | **Le plan de juin 2013** (P-2) | le processus est **choisi** pour ce qu'il ne vérifie pas |
| **②** | **Les négociations de 2015** (P-7, P-9, P-16, P-17, P-18) | **préparé** — terme différé : l'auditoire connaît, donc l'état produit sera soumis ailleurs |
| **③** | **La requête de novembre 2015** (P-19) | **employé** |

**Ce qui varie et ce qui ne varie pas** — c'est de là que la thèse tire sa
force :

- **T2 est la constante.** La fin ne change jamais. Elle est nommée le
  **11 juin 2013**, vingt mois avant la séparation et plus de deux ans avant la
  saisine;
- **T1 est la variable.** La dimension mobilisée change trois fois. Lorsqu'une
  dimension cesse de porter la conclusion, **ce n'est pas la conclusion qui
  cède** : c'est une autre dimension qui est mobilisée;
- **T4 parcourt ses trois modes** : choisi, préparé, employé. C'est lui qui fait
  des trois instanciations **une seule opération**.

➜ **Chaque instanciation se tient seule comme défaut**, puisqu'elle réunit à
elle seule les quatre termes. **C'est leur suite qui porte la thèse** — par la
constante du T2 et par la variation du T1.

#### Comment la thèse atteint les deux affirmations du § 3

| Affirmation du § 3 | Ce qui l'atteint |
|---|---|
| **La cause** — « puisque le défendeur refusait de régler à l'amiable, j'ai été obligée de saisir » | **T2 daté** : une fin déjà poursuivie ne peut pas avoir été causée par un refus postérieur. **T4** : il dit pourquoi la démarche a pris la forme d'une saisine plutôt que d'une entente — devant un père qui connaît la situation de ses enfants, aucune représentation de cette situation ne tient; l'opération requiert un auditoire **sans accès indépendant**. ➜ Le refus allégué et la saisine sont **deux effets d'une même cause** |
| **La finalité** — « afin de faire valoir les droits de nos enfants » | **T1 variable contre T2 constante** : ce qui se remplace est un **argument**, ce qui ne se remplace pas est la **fin**. ➜ L'intérêt des enfants était l'**argument**; les conclusions recherchées étaient la **fin** — exactement l'inversion que le § 3 revendique à l'envers |

➜ **Le T4 atterrit en une étape sur la disposition.** Un processus employé
**contre sa propre condition de légitimité**, c'est ce que l'art. 51 C.p.c.
nomme le détournement des fins de la justice. Aucun état mental n'est requis.

⚠️ **Deux précisions déjà acquises, à ne pas rouvrir.**

1. **Le 13 août 2015 (P-16) n'est pas une quatrième instanciation.** Sa place
   est **dans l'instanciation ②**, dont il est la continuation et le test. La
   version antérieure affirmait que le T1 y faisait défaut : **c'est inexact**,
   l'article 6 du projet réinvoque « compte tenu des circonstances » et « vu
   l'âge des enfants ». Ce que le 13 août fait, c'est n'**avancer** aucune
   dimension tout en maintenant le **même** refus que le 27 avril.
2. **Le « constat » n'a pas le même objet aux trois dates.** À ① et à ②, il
   porte tel quel sur la situation des enfants. À ③, il porte sur les **motifs
   soumis**.

#### Les deux temps, et ce qui existe déjà

> **Demandeur** : « Le premier temps est l'analyse des actes qui ont mené à
> l'écriture de la requête […]. Le deuxième temps consiste à établir que la
> requête de novembre 2015, analysée juste avant comme premier acte, suit le
> même modus operandi. »

**Temps 1 — les actes antérieurs à la requête.** Les cinq pièces de 2015 forment **une seule** instanciation, la ②; le découpage par moments ci-dessous est un ordre de travail, non une subdivision de la thèse.

| Moment | PDF visé | Cote | Date en base | État du travail |
|---|---|---|---|---|
| **Juin 2013** | `pdf:1` | **P-2** | 2013-06-11 | ✅ **Rédigé** — version consolidée du 11 oct., §§ 260-279 : [`2026-10-11_bloc-1-version-consolidee-plan-2013.md`](../instance/analyses/2026-10-11_bloc-1-version-consolidee-plan-2013.md) |
| **Avril 2015** | `pdf:2` | **P-7** | 2015-04-20 | ⚠️ analyse **autonome non commencée** |
| | `pdf:3` | **P-9** | 2015-04-27 | matière à [`2026-10-07_contre-indication-27-avril-instance-2.md`](../instance/analyses/2026-10-07_contre-indication-27-avril-instance-2.md) |
| **Août 2015** | `pdf:5` | **P-16** | 2015-08-13 | ⚠️ non commencée |
| **Septembre 2015** | `pdf:6` | **P-17** | **2015-09-02** | ⚠️ non commencée |
| | `pdf:7` | **P-18** | 2015-09-03 | ⚠️ non commencée |

⚠️ **Une correction de regroupement.** `pdf:6` (**P-17**) est daté du
**2 septembre 2015**, non d'août. Le groupe d'août est donc **P-16 seule**, et
l'échange de septembre en compte deux : **P-17 puis P-18**. Cela ne change pas
la séquence, mais un acte mal daté dans un acte de procédure se paie.

**Temps 2 — la requête de novembre 2015 suit le même modus operandi.**

Matière existante : [`2026-10-07_requete-novembre-2015-instance-3-et-conformite.md`](../instance/analyses/2026-10-07_requete-novembre-2015-instance-3-et-conformite.md).
L'analyse autonome, elle, n'est pas commencée.

#### Deux liens structurels à ne pas perdre

**a) La démonstration 2 s'appuie sur la démonstration 1.** Le temps 2 établit
que la requête « suit le même modus operandi » — or la requête est l'objet de
l'**axe 1**. L'ordre des axes n'est donc pas seulement chronologique : il est
**constructif**. L'axe 1 doit livrer l'analyse de la requête dont l'axe 2 se
sert ensuite. ⚠️ Conséquence : on ne peut pas rédiger l'axe 2 avant que l'axe 1
soit stable.

**b) Les deux temps se superposent exactement aux trois instanciations.**

| | Temps 1 — les actes qui ont mené à la requête | Temps 2 — la requête |
|---|---|---|
| Instanciations | **①** le plan de juin 2013 · **②** les négociations de 2015 | **③** la requête de novembre 2015 |

⚠️ **Le nommage du demandeur tranche une tension du corpus.** Les relevés
antérieurs désignaient parfois l'instanciation ② par une pièce unique — « le
27 avril 2015 (P-9) » — alors que la correction du 3 octobre avait déjà rangé
le 13 août **dans** ② comme sa continuation et son test. **L'instanciation ②
est la négociation**, pas une lettre : P-7, P-9, P-16, P-17 et P-18 y sont une
seule instanciation, dont le 27 avril est l'acte d'ancrage.

Conserver le vocabulaire des instanciations : **P-2 est l'instanciation ①,
jamais un étalon** auquel on mesurerait les autres.

#### Ce qui reste à faire, en clair

1. **L'analyse autonome des négociations n'est pas commencée.** L'INDEX du § 3
   le dit : elle « commencera lorsque le demandeur jugera ce premier exercice
   complet et satisfaisant ». C'est le poste de travail le plus lourd du
   temps 1 — cinq pièces, aucune rédigée.
2. **Le bloc 1 atteint le § 3, et réserve le reste par décision.** Voir
   § 5.5 : la rédaction du 11 octobre consacre son **§ 267** au § 3 de P-42,
   cité intégralement. Les reprises restant à faire sont celles de l'évaluation
   du 9 octobre qui n'ont pas été traitées le 11 — à lire dans la
   [comparaison du 11 octobre](../instance/analyses/2026-10-11_comparaison-bloc-1-9-et-11-octobre.md),
   non dans l'évaluation seule.
3. **Le temps 2 dépend de l'axe 1.**

---

### 5.5 Ce que le bloc de juin 2013 fait du § 3 — rectification du 14 octobre

> **Question du demandeur** : « je ne comprends pas ton affirmation que le bloc
> de juin 2013 ne retombe pas sur la cause de la saisine ? »
>
> **L'affirmation était fausse.** Elle reprenait le point 6 de l'évaluation du
> 9 octobre — « Retomber sur la cause de la saisine : **non faite**, §270 la
> renvoie au bloc suivant » — qui porte sur les **§§260-270 du 9 octobre**. Or
> cette rédaction est **remplacée** par la version consolidée du 11 octobre
> (§§260-279). C'est exactement l'erreur contre laquelle l'INDEX du § 3 met en
> garde : reprendre une couche périmée.

**Ce que la version du 11 octobre fait.** Son **§ 267** s'ouvre sur « Ce constat
atteint déjà deux éléments du §3 de la déclaration assermentée de 2019 »,
reproduit le § 3 **intégralement**, et conclut :

> « La préférence de garde, le désaccord et le recours judiciaire destiné à le
> surmonter sont tous nommés dès le 11 juin 2013. […] **Le « refus » de 2015 ne
> peut expliquer l'origine d'une préférence et d'un projet judiciaire déjà
> formulés en 2013.** »

Le bloc **retombe donc bien sur le § 3**, et par le seul moyen qu'un écrit de
2013 puisse porter seul : **l'antériorité**. Une fin déjà poursuivie ne peut pas
avoir été causée par un refus postérieur.

**Ce qu'il réserve, et pourquoi c'est juste.** La même page poursuit : « Pour
apprécier la cause de la saisine effectivement survenue en 2015, il faut ensuite
examiner si la négociation a ajusté les conclusions à la situation des enfants
ou maintenu cette destination. » La [comparaison du 11 octobre](../instance/analyses/2026-10-11_comparaison-bloc-1-9-et-11-octobre.md)
l'enregistre comme une **décision** : « La cause de la saisine effectivement
survenue reste réservée à l'analyse des négociations, après validation de
l'exercice actuel. »

➜ **La distinction porte sur les deux moitiés du mouvement 1.**

| Moitié | Ce qu'elle dit | Où elle se fait |
|---|---|---|
| **Négative** | Le refus de 2015 **ne peut pas** être la cause : l'objectif lui est antérieur | ✅ **Faite** — bloc de juin 2013, § 267 |
| **Positive** | La saisine est, **avec** le désaccord, le second effet d'une même cause — l'incompatibilité entre les conclusions et la réalité des enfants | ⏳ **Réservée** aux négociations : il faut 2015 pour montrer que l'incompatibilité a persisté |

C'est un découpage correct, non une lacune. La moitié positive exige d'établir
que la négociation **n'a pas** ajusté les conclusions — ce qu'aucun écrit de
2013 ne peut montrer.

⚠️ **Règle de travail qui en découle.** Ne jamais citer l'évaluation du
9 octobre sans passer par la comparaison du 11. L'INDEX le dit en tête :
« les plus récentes **corrigent** les plus anciennes sur plusieurs points. Sans
cet index, on risque de reprendre une version périmée. » Les reprises de
l'évaluation du 9 qui restent dues sont celles que la comparaison du 11 ne
marque pas traitées — pas la liste entière.

---

---

### 5.6 Démonstration 3 — la contestation du § 8 de la dénonciation de 2023

**Cible précisée par le demandeur, 14 octobre 2026.** La troisième
démonstration majeure complexe porte sur l'allégation selon laquelle le
demandeur aurait choisi de ne pas travailler pour subvenir aux besoins de ses
enfants, dans la dénonciation d'un moyen déclinatoire.

**Lien base ↔ plan**, d'après le relevé du § 7 :

| Acte | § visé | nœud | **`Statement`** |
|---|---|---|---|
| **P-40**, `document:2` — dénonciation du 21 juillet 2023 | **8** | `89` | **`89`** |

La démonstration s'articule en **deux temps**, précisés par le demandeur.

#### Temps 1 — les actes ayant mené à l'établissement de la pension alimentaire

Ce premier temps comprend :

- les informations financières échangées;
- le formulaire de pension alimentaire de la mère;
- le manque de concordance entre le salaire projeté pour l'année en fonction
  des emplois déposés en preuve et celui utilisé dans le formulaire.

#### Temps 2 — les communications sur l'évolution de la situation

Ce second temps porte sur les multiples communications entre le demandeur,
Me Ayoub et Élise, dans lesquelles le demandeur les avise de l'évolution de
la situation et des conséquences prévisibles sur sa capacité à occuper un
emploi.

---

### 5.7 Objections déjà examinées

**Règle de continuité approuvée par le demandeur, 14 octobre 2026.** Avant
toute nouvelle évaluation des démonstrations, lire cette section et les
réponses auxquelles elle renvoie. Chaque objection examinée est consignée
avec **la réponse retenue et sa conséquence pour la lecture**.

**Ne rouvrir un point qu'en identifiant un élément nouveau ou une erreur
précise, puis en expliquant pourquoi la réponse déjà retenue ne suffit plus.**
Une nouvelle lecture du même passage ou une reformulation de la même objection
ne constitue pas, à elle seule, une raison de recommencer le débat.

#### 5.7.1 Le jeune âge au § 15 de P-19

**Objection examinée.** Le § 15 invoque aussi le jeune âge des enfants;
cette mention a été opposée à la synthèse selon laquelle le tout repose sur
l'implication minimale historique, la difficulté à assumer le rôle de père et
l'indisponibilité.

**Réponse retenue.** L'âge est une donnée à considérer. **À lui seul, il ne
justifie pas une garde exclusive** : une situation concrète des enfants doit
compléter cette information et expliquer la pertinence du régime demandé.
Cette distinction était déjà consignée dans le
[30](30_evaluation_trois_propositions.md) § 7.2 : « l'âge est une donnée, non
un motif ».

**Conséquence pour la lecture.** La seule mention du jeune âge au § 15 ne
fournit pas un fondement autonome suffisant à la garde exclusive et **ne
réfute pas la synthèse du socle parental** (§ 5.1; partie I, ¶ 3 du
[25](25_presentation_argument_complet.md)). Ne pas la réintroduire comme
objection à cette synthèse sans satisfaire à la règle de réouverture.

#### 5.7.2 L'infidélité et la séparation de 2011 au § 7 de P-19

**Objection examinée.** Le § 7 attribue la séparation de 2011 à
l'infidélité; cette cause conjugale a été opposée à la synthèse du socle
parental.

**Réponse retenue.** **La séparation conjugale de 2011 et la garde sont deux
questions différentes.** L'infidélité ne sert pas, par elle-même, d'appui à
une garde exclusive. Dans le § 7, c'est l'affirmation relative à la difficulté
à assumer le rôle de père et à s'investir — `Statement` **`11`** — qui
appartient au socle parental identifié au § 5.1.

**Conséquence pour la lecture.** L'explication conjugale de la séparation de
2011 **ne réfute pas la synthèse du socle parental**. Ne pas réintroduire
l'infidélité comme objection à cette synthèse sans satisfaire à la règle de
réouverture.

---

## 6. Ce que le plan ne tranche pas encore

1. **Le rattachement des cinq sous-sections de période** (A, B, D, F, H) aux
   trois axes, ou leur sortie de l'exposé.
2. **Où va la matière qui ne se rattache à aucun des trois actes** — les
   conséquences de 2020 (F), le solde de 2026 (H).
3. **Ce que devient l'antériorité** : le plan de juin 2013 (P-2) et les
   positions de 2015 (P-7, P-9, P-16, P-18) ne sont pas des actes de la
   partie adverse au sens de cette section — ils sont antérieurs au premier
   axe et le préparent.
4. **Combien de pièces additionnelles**, et combien sont déjà extraites —
   seule décision du `../instance/communication_pieces.md` § 10.4 encore
   ouverte, et celle qui bloque l'estimation de durée.
5. **La concordance.** Chaque paragraphe réécrit nomme son antécédent **au
   moment où il s'écrit**, par `document_manager.concordance.relier`. Un
   paragraphe écrit sans son antécédent est un paragraphe à refaire
   (§ 10.5 du même fichier).

---

## 7. Références des paragraphes des trois actes

> **Nature de ces tables.** Relevé mécanique de la base, produit le
> 14 octobre 2026. Le § résolu est **calculé** (§ 3, mise en garde 1).
> L'incipit est tronqué à 150 caractères : il **sert à reconnaître** le
> paragraphe, jamais à le citer.




#### P-19 — `document:1` — Requête en garde, fixation de la pension alimentaire pour enfant et ordonnance de sauvegarde

**66 paragraphes.** Assermentée le **19 novembre 2015**; date de rédaction inconnue (§ 4.1). Auteure : **Me Adélia Ferreira**. `source_type` = `REPRODUCED` · `numbering_mode` = `AUTO`.

⚠️ Le champ `document_original_date` porte `2015-11-27` — **valeur sans source, à ne pas reprendre** (§ 4.1). Scan : `evidence_files/requête_en_garde_fixation_de_la_pension_alimentaire_pour_enfant_et_ordonn_Xko74Nt.pdf`.

La colonne **§** ne porte un numéro que pour les 66 paragraphes de l'acte. Un sous-item porte `↳ § n` : ce n'est pas un paragraphe de la requête, et il se cite sous le § qui le porte (§ 4.3).

| § | nœud | `Statement` | Incipit |
|---|---|---|---|
| *titre* | `1` | `1` | REQUÊTE EN GARDE, FIXATION DE LA PENSION ALIMENTAIRE POUR ENFANT ET ORDONNANCE DE SAUVEGARDE |
| **1.** | `2` | `2` | Les parties se sont fréquentées et fait vie commune pendant pour une période d'environ onze (11) ans, soit du 31 décembre 2003 au 23 février 2015. |
| **2.** | `3` | `3` | De cette union sont nés deux enfants à savoir : |
| ↳ § 2 | `4` | `4` | a) Alexia David, née le 6 octobre 2009, actuellement âgée de 6 ans. |
| ↳ § 2 | `5` | `5` | b) Nicolas David, né le 1 février 2013, actuellement âgé de 2 ans. |
| **3.** | `6` | `6` | Les enfants ne font pas l'objet d'une décision de la Cour du Québec, chambre de la jeunesse ni d'une instance en cours, ni d'une entente avec le direc… |
| **4.** | `7` | `7` | La continuation de la vie commune étant devenue impossible, le défendeur a quitté la résidence commune le 23 février 2015 pour se loger dans un appart… |
| **5.** | `8` | `8` | En effet, depuis la naissance d'Alexia, la relation entre les parties était très difficile. |
| **6.** | `9` | `9` | En effet, le défendeur ne s'impliquait que minimalement dans les soins d'Alexia, laissant toute la responsabilité à la demanderesse, ce qui causait de… |
| **7.** | `10` | `10` | En 2011, suite à une infidélité du défendeur, les parties ont vécu séparées pendant un (1) an et ont été en thérapie. |
| ↳ § 7 | `11` | `11` | A ce moment il est ressorti que le défendeur avait de la difficulté à assumer son rôle de père et s'investir. |
| **8.** | `12` | `12` | Les parties ont repris la vie commune mais ont constaté rapidement que leur relation n'allait pas vraiment s'améliorer et devaient se quitter définiti… |
| **9.** | `13` | `13` | En 2013, le défendeur est parti tout l'été et a laissé la demanderesse seule avec les deux (2) enfants. |
| **10.** | `14` | `14` | Au mois d'août 2014, la demanderesse a racheté la part du défendeur dans la résidence commune car il refusait de faire des réparations et rénovations… |
| **11.** | `15` | `15` | Les partie ont continué de cohabiter jusqu'au départ du défendeur le 23 février 2015. |
| **12.** | `16` | `16` | Depuis le départ du défendeur, la demanderesse a la garde des enfants mineurs Alexia et Nicolas. |
| **13.** | `17` | `17` | Bien que le défendeur ait emménagé dans son logement depuis près de neuf (9) mois, à ce jour aucun espace n'a été aménagé pour accueillir les enfants. |
| **14.** | `18` | `18` | Dès la rupture, le défendeur voulait instaurer une garde partagée, que la demanderesse a refusé puisque contraire à l'intérêt des enfants. |
| **15.** | `19` | `19` | En effet, les enfants sont jeunes et de plus, le défendeur était rarement disponible pour prendre soins d'eux. |
| **16.** | `20` | `20` | C'est la demanderesse qui s'occupait des enfants, qui allait aux activités, etc...... |
| **17.** | `21` | `21` | Le défendeur aidait lorsque la demanderesse n'était pas disponible. |
| **18.** | `22` | `22` | Les parties ont donc convenu que la demanderesse aurait la garde des enfants, le tout tel qu'il appert des échanges des messages textes datés du 21 av… |
| **19.** | `23` | `23` | Il avait été également prévu d'augmenter graduellement les droits d'accès du défendeur au fil du temps. |
| **20.** | `24` | `24` | À la demande du défendeur, des droits d'accès du dimanche entre 16h00 et 20h00 ont été établis coïncidant ainsi avec ses visites hebdomadaires chez se… |
| **21.** | `25` | `25` | Lorsque les parents du défendeur s'absentent pour la fin de semaine, ce dernier refuse d'exercer son droit d'accès auprès des enfants. |
| **22.** | `26` | `26` | Afin d'accompagner les enfants dans le processus de la rupture, de consentement entre les parties, la demanderesse a consulté la psychologue Dr. Claud… |
| **23.** | `27` | `27` | Bien que la demanderesse ait à plusieurs reprises offert au défendeur de prendre les enfants sur une base plus régulière et lui a proposé plus d'un sc… |
| **24.** | `28` | `28` | Depuis la rupture des parties, le défendeur a accepté de voir ses enfants sporadiquement au printemps 2015 et régulièrement les dimanches soirs depuis… |
| **25.** | `29` | `29` | La demanderesse est en mesure d'offrir aux enfants un milieu de vie stable, veille à leur éducation, à leur bien-être, leur développement et leur proc… |
| **26.** | `30` | `30` | Conséquemment, la demanderesse demande au tribunal de lui confier la garde des enfants mineurs et, de prendre acte qu'elle offre au défendeur qu'il ex… |
| **27.** | `31` | `31` | En cas d'impossibilité du défendeur de se présenter auxdits droits d'accès, la demanderesse désire en être informé au préalable dans les 72 heures afi… |
| ↳ § 27 | `32` | `32` | Si les parents du défendeur veulent quand même voir les enfants, ils pourront avoir les enfants à la place du défendeur. |
| **28.** | `33` | `33` | Afin de remédier au litige entre les parties, la demanderesse a également proposé au défendeur de participer à des séances de médiation, ce qu'il a re… |
| **29.** | `34` | `34` | Bien que le défendeur ait refusé de rencontrer le Dr. Claudia Écrement il a toutefois, a accepté de communiquer avec ledit docteur pour discuter de la… |
| **30.** | `35` | `35` | De plus, le défendeur refuse d'exercer conjointement l'autorité parentale à l'égard de leurs enfants mineurs préférant que toutes les décisions les co… |
| **31.** | `36` | `36` | Le défendeur a demandé à la demanderesse de faire le nécessaire afin qu'il soit déchu de certains attributs de l'autorité parentale, le tout tel qu'il… |
| **32.** | `37` | `37` | Le défendeur ne répond pas à tous les messages que la demanderesse lui envoie et décide lorsqu'il répond ou pas. |
| ↳ § 32 | `38` | `38` | Il n'a pas répondu en cas d'urgence tel que le lundi 12 octobre 2015, où l'enfant Nicolas a été transporté d'urgence à l'hôpital par ambulance. |
| **33.** | `39` | `39` | Récemment Alexia avait demandé de distancer ses droits d'accès avec son père et conséquemment les visites chez ses grands-parents, à raison d'un diman… |
| **34.** | `40` | `40` | Suite aux verbalisations de l'enfant, le défendeur a donc décidé de ne pas exercer son droit d'accès dimanche soir le 8 novembre 2015 sous prétexte qu… |
| **35.** | `41` | `41` | En ce qui concerne l'enfant Nicolas, il est confus de la présence irrégulière de son père et ne comprend pas les refus du défendeur de le voir lorsqu'… |
| **36.** | `42` | `42` | Effectivement, le défendeur a expliqué à l'enfant de deux ans qu'il refuse de le voir sous prétexte qu'il n'a rien de prévu avec ses parents la fin de… |
| **37.** | `43` | `43` | Depuis, Alexia et le défendeur se sont parlés au téléphone et Alexia est d'accord pour que les visites soient toutes les semaines. |
| **38.** | `44` | `44` | De plus, nonobstant le fait qu'il n'exerçait des accès que quatre (4) heures par semaine, le défendeur ramenait souvent les enfants plus tôt. |
| **39.** | `45` | `45` | Il lui est arrivé de ramener les enfants chez la demanderesse sans lui avoir parlé et demeuré devant l'immeuble en disant aux enfants que leur mère n'… |
| **40.** | `46` | `46` | Le défendeur n'appelle pas les enfants. |
| ↳ § 40 | `47` | `47` | La demanderesse a même pris un vieux IPhone et un IPod et créé une adresse courriel (Gmail) pour les enfants afin que le défendeur puisse parler aux e… |
| **41.** | `48` | `48` | Compte tenu des circonstances, la demanderesse demande de pouvoir signer seule les consentements relativement aux enfants. |
| **42.** | `49` | `49` | De plus, la demanderesse demande de pouvoir voyager avec les enfants à l'extérieur du Canada sans la signature du défendeur et à obtenir un passeport… |
| **43.** | `50` | `50` | La demanderesse offre d'aviser le défendeur de tout voyage è l'extérieur du Canada et de transmettre les coordonnées d'où elle va et également de l'av… |
| **44.** | `51` | `51` | La demanderesse demande au Tribunal d'ordonner au défendeur de payer une pension alimentaire pour le bénéfice exclusif des deux enfants mineurs et ce,… |
| **45.** | `52` | `52` | La demanderesse demande que la pension alimentaire à être versée pour le bénéfice exclusif des enfants soit rétroactive au 1er novembre 2015 en tenant… |
| **46.** | `53` | `53` | La demanderesse demande au Tribunal d'ordonner l'indexation de ladite pension conformément à l'article 590 C.c.Q. |
| **47.** | `54` | `54` | La demanderesse occupe un emploi à titre de comptable chez Hydro-Québec et génère annuellement des revenus d'environ 100 000$. |
| **48.** | `55` | `55` | Le défendeur occupe un emploi à titre d'Analyste à la Banque Nationale du Canada et génère annuellement des revenus d'environ 85 000$. |
| **49.** | `56` | `56` | Le défendeur a versé une pension alimentaire pour les enfants de 425.00$ par deux semaines après la réparation, ce qui avait été augmenté à 443.00$ pa… |
| **50.** | `57` | `57` | Or, le défendeur a décidé unilatéralement de ne verser que 101.00$ aux deux semaines et ce, à compter du début novembre 2015. |
| **51.** | `58` | `58` | Compte tenu des circonstances et des agissements du défendeur, la demanderesse demande que la pension alimentaire soit majorée de 20% pour tenir compt… |
| **52.** | `59` | `59` | La demanderesse maintient des relations étroites avec sa famille et elle a deux sœurs qui parfois sont capables de l'aider avec les enfants mais dans… |
| **53.** | `60` | `60` | Or, les enfants ont des cours, Nicolas a de la natation et de la gymnastique et Alexia a également de la natation, de la danse, du Karaté et de la gym… |
| **54.** | `61` | `61` | La demanderesse consent au partage du paiement des frais particulier au prorata de leurs revenus à savoir 54% pour la demanderesse et 46% pour le défe… |
| **55.** | `62` | `62` | La demanderesse considère les frais particuliers suivants : |
| ↳ § 55 | `63` | `63` | a) Les frais de santé qui ne sont pas couverts par les assurances et sans limiter la généralité de ce qui précède, les médicaments de prescription, le… |
| ↳ § 55 | `64` | `64` | b) Tous les frais de camps de jour et du service de garde qui sont additionnels lors des journées pédagogiques et des congés scolaires, lesquels frais… |
| ↳ § 55 | `65` | `65` | c) Une portion des frais d'activités des enfants, lesquels sont d'environ 2500.00$ par année. |
| **56.** | `66` | `66` | Les enfants ont toujours été couverts par les assurances médicales et médicaments du défendeur. |
| **57.** | `67` | `67` | À ce jour, le défendeur refuse que la demanderesse utilise les dites assurances lorsqu'elle achète les médicaments pour les enfants et pour les consul… |
| ↳ § 57 | `68` | `68` | Lui seul peut bénéficier d'utiliser le service lorsqu'il a les enfants et refuse de payer la différence non couverte par les assurances. |
| **58.** | `69` | `69` | devant la position du défendeur à cet égard, la demanderesse n'a d'autre choix que de s'adresser au tribunal afin qu'il soit ordonné au défendeur de l… |
| **59.** | `70` | `70` | La demanderesse a toujours essayé d'accommoder le défendeur dans ses demandes. |
| **60.** | `71` | `71` | Vu l'urgence de la situation, la demanderesse demande au Tribunal de rendre une ordonnance de sauvegarde sur les points suivants jusqu'à ce que jugeme… |
| **61.** | `72` | `72` | La demanderesse demande la garde des enfants Nicolas et Alexia. |
| **62.** | `73` | `73` | La demanderesse s'engage à communiquer avec le père dans la mesure du possible toutes informations importantes concernant la santé et l'éducation des… |
| **63.** | `74` | `74` | La demanderesse demande au tribunal de lui permettre de faire seule une demande de passeport pour les enfants. |
| **64.** | `75` | `75` | La demanderesse demande au tribunal de lui permettre de voyager avec les enfants sans la permission au préalable du père tel qu'il lui a demandé. |
| **65.** | `76` | `76` | La demanderesse, eu égard aux circonstances, considère qu'il est urgent qu'un cadre clair soit établi tant au plan de la garde, la pension et les accè… |
| **66.** | `77` | `77` | La présente requête est formulée dans le meilleur intérêt des enfants et est bien fondée en faits et en droit. |
| ~~67~~ ⚠️ | `78` | `78` | La présente requête est formulée dans le meilleur intérêt des enfants et est bien fondée en faits et en droit.  ·  **erreur de transcription — l'acte s'arrête au § 66** |

#### P-42 — `document:3` — Déclaration assermentée de la demanderesse (DA-2019)

`document_original_date` = **2019-10-21** · auteur en base : **Marie-Josée Ayoub (Soeur d'Élise, Avocate spécialisée en protection de la jeunesse, représente la mere lors des négociation en 2015)** · `source_type` = `REPRODUCED` · `numbering_mode` = **`AUTO`** (numéro **calculé**, non conservé)

36 nœuds, tous porteurs de texte · 30 portent un numéro résolu · scan d'origine : `evidence_files/déclaration_assermentée_de_la_demanderesse.pdf`

| § résolu | nœud | `Statement` | prof. | Incipit |
|---|---|---|---|---|
| — | `93` | `93` | 1 | DÉCLARATION ASSERMENTÉE DE LA DEMANDERESSE |
| **1.** | `94` | `94` | 2 | Je suis demanderesse en la présente cause |
| **2.** | `95` | `95` | 2 | Depuis que le défendeur a quitté la résidence familiale le ou vers le mois de février 2015, J'ai dû assumer seule la garde, l'entretien et l'éducation… |
| **3.** | `96` | `96` | 2 | Puisque le défendeur refusait de régler le litige à l'amiable, j'ai été obligée de saisir le Tribunal afin de faire valoir les droits de nos enfants |
| **4.** | `97` | `97` | 2 | Le 14 janvier 2016, l'Honorable Sophie Picard, J.C.S. prononçait un jugement, lequel me confiait la garde de nos enfants et des droits d'accès au défe… |
| **5.** | `98` | `98` | 2 | Ledit jugement, prévoyait entre autres que le défendeur devait payer sa quote-part (actuellement 48%) de l'assurance médicale collective, des frais de… |
| **6.** | `99` | `99` | 2 | Or, depuis le prononcé du jugement, des faits nouveaux sont survenus à savoir: |
| **6a.** | `100` | `100` | 3 | De facto, les accès du père auprès des enfants se limitent à un accès au trois (3) semaines pour une durée maximale de 3.5 heures |
| **6b.** | `101` | `101` | 3 | Lesdits droits d'accès entre le défendeur et les enfants ont lieu au domicile des grands-parents paternels lorsque la grand-mère est disponible pour u… |
| **6c.** | `102` | `102` | 3 | En plus de ne pas exercer la totalité de ses droits d'accès, le défendeur refuse de prendre les enfants lors de la période estivale, jours pédagogique… |
| **6d.** | `103` | `103` | 3 | Conséquemment, je dois assumer seule les frais reliés à approximativement quinze (15) semaines de vacances par année |
| **6e.** | `104` | `104` | 3 | Afin de remédier à tous les rendez-vous médicaux nécessaires pour le bien-être de nos enfants je dois m'absenter de mon milieu de travail à raison d'e… |
| **6f.** | `105` | `105` | 3 | Lors du calcul initial de la pension alimentaire pour enfants, les frais particuliers payables par le défendeur à la demanderesse n'ont pas été inclus… |
| **6g.** | `106` | `106` | 3 | Conséquemment, j'ai dû assumer seule au fil du temps les dépenses suivantes eu égard aux enfants |
| — | `107` | `107` | 4 | Les frais reliés aux services de garde |
| — | `108` | `108` | 4 | Les frais reliés aux camps de jour pour la période d'environ 11 semaines |
| — | `109` | `109` | 4 | Les frais du suivi psychologique |
| — | `110` | `110` | 4 | Les frais de santé, dentaires et médicaments |
| — | `111` | `111` | 4 | Tous les frais reliés aux activités sportives |
| **7.** | `112` | `112` | 2 | Bien que les frais de santé qui ne sont pas couverts par les assurances et sans limiter la généralité de ce qui précède, les médicaments de prescripti… |
| **8.** | `113` | `113` | 2 | De plus, le défendeur me doit en date du 1 août 2019, des arrérages de pension alimentaire au montant de 1341,87$ |
| **9.** | `114` | `114` | 2 | Bien que le défendeur allègue avoir perdu son emploi le 29 juin 2018, il a tout de même les moyens de payer la pension alimentaire pour le bénéfice de… |
| **10.** | `115` | `115` | 2 | Effectivement, conformément à l'Annexe 1 produit par le défendeur en date du 13 septembre 2018, il détenait un actif en argent de 26 773,11$ |
| **11.** | `116` | `116` | 2 | ce jour, les actifs en argent dans son compte bancaire sont 10 000$ |
| **12.** | `117` | `117` | 2 | Le défendeur n'a pas de dette, sa seule dépense consiste à être la location de son logement, un 5 et 21​ situé en la ville de St-Lambert, sans télépho… |
| **13.** | `118` | `118` | 2 | Son véhicule lui a été fourni par ses parents |
| **14.** | `119` | `119` | 2 | Bien que le défendeur allègue avoir envoyé plusieurs candidatures d'emploi et qu'il n'a pas été en mesure de trouver du travail, plusieurs offres sont… |
| **15.** | `120` | `120` | 2 | Le défendeur a de l'expérience à titre d'analyste, de technicien en laboratoire et au service à la clientèle service bancaire |
| **16.** | `121` | `121` | 2 | Bien qu'il allègue dans sa demande en modification de la pension alimentaire pour enfants et lors des auditions à la cour, ne pas être en mesure de tr… |
| **17.** | `122` | `122` | 2 | Effectivement, lors de ladite audition, le défendeur nous apprenait qu'il avait trouvé un emploi à Bucarest et que sa rémunération oscillerait autour… |
| **18.** | `123` | `123` | 2 | Que sa décision d'aller travailler à Bucarest est le résultat de la décision du Gouvernement de «L'Honorable monsieur Legault, de réduire les quotas d… |
| **19.** | `124` | `124` | 2 | Bien qu'il y ait plusieurs opportunités d'emploi, il n'est pas de l'intention du défendeur de trouver du travail au Québec |
| **20.** | `125` | `125` | 2 | Le ou vers le mois de 2019, lorsque le défendeur a appris que la Grand-mère paternelle des enfants voulait contribuer financièrement, monsieur s'est d… |
| **21.** | `126` | `126` | 2 | De facto, le défendeur en quittant le pays va abandonner ses enfants et ne va pas subvenir à leurs besoins |
| **22.** | `127` | `127` | 2 | Il me sera difficile, voire impossible d'avoir une pension alimentaire lorsque le défendeur commencera à travailler à l'étranger |
| **23.** | `128` | `128` | 2 | Tous les faits allégués dans la présente sont vrais |

#### P-40 — `document:2` — Dénonciation de la défenderesse d'un moyen déclinatoire

`document_original_date` = **2023-07-21** · auteur en base : **Élise Marie Ayoub (Mère des enfants)** · `source_type` = `REPRODUCED` · `numbering_mode` = **`AUTO`** (numéro **calculé**, non conservé)

14 nœuds, tous porteurs de texte · 13 portent un numéro résolu · scan d'origine : `evidence_files/dénonciation_de_la_défenderesse_dun_moyen_déclinatoire.pdf`

| § résolu | nœud | `Statement` | prof. | Incipit |
|---|---|---|---|---|
| — | `79` | `79` | 1 | DÉNONCIATION DE LA DÉFENDERESSE D'UN MOYEN DÉCLINATOIRE |
| **1.** | `80` | `80` | 2 | La défenderesse entend soulever l'absence de compétence territoriale de la Cour supérieure, du district de Montréal, le 4 août 2023 à 9h00 ou aussitôt… |
| **2.** | `81` | `81` | 2 | Effectivement, vers le ou vers la fin du mois de novembre 2015, une demande introductive d'instance a été introduite par la défenderesse mais demander… |
| **3.** | `82` | `82` | 2 | Le 14 janvier 2016, l'Honorable Sophie Picard, J.C.S., prononçait un jugement, lequel confiait la garde des enfants à la défenderesse et des droits d'… |
| **4.** | `83` | `83` | 2 | Le 24 juillet 2018, le demandeur présentait dans le district judiciaire de Longueuil, une demande en modification de la pension alimentaire pour enfan… |
| **5.** | `84` | `84` | 2 | Le 27 septembre 2019, l'Honorable juge Carole Julien, j.c.s., prononçait un jugement lequel ordonnait entres autres les ordonnances suivantes |
| **5a.** | `85` | `85` | 3 | Suspend l'exécution des versements de la pension alimentaire par M. David à Madame Ayoub pour les enfants en vertu des jugements antérieurs ainsi que… |
| **5b.** | `86` | `86` | 3 | La levée des saisies des comptes bancaires personnels du demandeur |
| **6.** | `87` | `87` | 2 | Malgré les prétentions du demandeur eu égard à sa précarité financière, le 4 novembre 2019, l'Honorable juge Danielle Mayrant, J.C.S., a rendu un juge… |
| **7.** | `88` | `88` | 2 | Lors de l'audition du 4 novembre 2019, il a été mis en preuve qu'une liste de plus de quatre cents offres d'emploi étaient disponibles pour des candid… |
| **8.** | `89` | `89` | 2 | Le demandeur a fait le choix de ne pas travailler pour subvenir aux besoins de ses enfants |
| **9.** | `90` | `90` | 2 | Le dossier complet des parties est dans le district judiciaire de Longueuil |
| **10.** | `91` | `91` | 2 | La défenderesse et les enfants des parties ne sont pas domiciliés dans le district de Montréal où la demande a été introduite, puisqu'ils sont domicil… |
| **11.** | `92` | `92` | 2 | Au surplus, il s'agit d'une demande en matière familiale, soit une demande en annulation de la pension alimentaire, des arrérages et ordonnance de sau… |

---

## 8. Inscriptions

- **14 octobre 2026 — objections déjà examinées.** Ajout du § 5.7, sur
  instruction du demandeur : l'objection du jeune âge (§ 15 de P-19) et celle
  de l'infidélité et de la séparation de 2011 (§ 7) sont consignées avec les
  réponses retenues et leurs conséquences pour la lecture. Elles ne
  remettent pas en cause la synthèse du socle parental. La consultation est
  requise avant toute nouvelle évaluation; la réouverture exige un élément
  nouveau ou une erreur précise et l'explication de ce qui rend la réponse
  antérieure insuffisante. Renvois ajoutés en tête du plan et au § 5.1.
  Aucune donnée en base touchée.
- **14 octobre 2026, nouvelle inscription.** Le cadrage est précisé : une
  structure de rédaction **incomplète**, fondée sur les trois actes, avec
  **une démonstration majeure complexe et plusieurs démonstrations simples
  pour chacun**. La troisième démonstration est désormais précisée au § 5.6 :
  **P-40 § 8**, `Statement` **`89`**, le choix allégué de ne pas travailler
  pour subvenir aux besoins des enfants. Ses deux temps portent sur les actes
  ayant mené à l'établissement de la pension alimentaire (informations
  financières, formulaire de la mère, manque de concordance entre le salaire
  projeté et celui utilisé) et sur les communications avisant Me Ayoub et
  Élise de l'évolution de la situation et des conséquences prévisibles sur
  la capacité du demandeur à occuper un emploi. Les **trois démonstrations
  complexes** sont précisées; **aucune démonstration simple** ne l'est.
  Aucune donnée en base touchée.
- **14 octobre 2026, quatrième inscription.** La **démonstration 2** est
  énoncée (§ 5.4) : la fausseté du § 3 de la déclaration de 2019, avec le § 4
  pour contexte — `Statement` **`96`** et **`97`**. Le § 3 porte **deux**
  affirmations, une cause et une finalité, que trois mouvements atteignent
  séparément. ⚠️ La thèse transmise **figure déjà** dans
  `../instance/par3_version_plaidable.md`, `../instance/pont_these_trois_instances.md`
  et `../instance/INDEX_contre_argument_par3.md` : ne rien réécrire sans partir
  de là. Les six PDF visés sont identifiés — `pdf:1`=P-2, `pdf:2`=P-7,
  `pdf:3`=P-9, `pdf:5`=P-16, `pdf:6`=P-17, `pdf:7`=P-18 — avec une correction
  de regroupement : **P-17 est du 2 septembre**, non d'août. État relevé : le
  bloc de juin 2013 est rédigé mais non clos (il ne retombe pas sur la cause de
  la saisine); **l'analyse autonome des négociations n'est pas commencée**;
  le temps 2 dépend de l'axe 1. Aucune donnée en base touchée.
- **14 octobre 2026, troisième inscription.** Le troisième étage du plan est
  posé : **une démonstration majeure par acte** (§ 5). La démonstration 1 est
  nommée — la contradiction de la thèse principale de la requête — et son texte
  d'ouverture, transmis par le demandeur, est **identique au mot** à la partie I
  du [25](25_presentation_argument_complet.md) § 2 : c'est une confirmation, pas
  un texte nouveau. Le **lien base ↔ plan** est enregistré au § 5.2 : les neuf
  paragraphes cités portent les `Statement` `7`, `8`, `9`, `10`, `11`, `18`,
  `19`, `20`, `21`, `22`, et les trois pierres du socle sont les `Statement`
  **`9`**, **`11`** et **`19`**. Vérification du scan au § 5.3 : la ponctuation
  finale « ; » est **confirmée sur l'original** — la base l'a normalisée en
  « . » sur huit des neuf paragraphes, donc aucun verbatim ne se tire du
  `Statement`; les a) et b) du § 2 **figurent dans la requête**, ce qui resserre
  le § 4.3 sans le renverser; et le `2015-11-27` de la base vient d'un **tampon
  du greffe de Longueuil**, ce qui confirme que la date qualifiante demeure
  l'assermentation du 19 novembre 2015. Les démonstrations 2 et 3 restent à
  énoncer. Aucune donnée en base touchée.
- **14 octobre 2026, deuxième inscription.** Les trois écarts du relevé initial
  sont **tranchés par le demandeur** : P-19 est assermentée le 19 novembre 2015
  et sa date de rédaction est inconnue (§ 4.1); la requête compte **66**
  paragraphes, le 67e est un doublon de transcription qu'il ne faut pas
  éliminer (§ 4.2); les **sous-items ne figurent pas dans la requête** et ne se
  citent jamais comme paragraphes (§ 4.3). Balayage du corpus au § 4.4 : le
  « § 57a » et le « § 67 » y sont cités dans six fichiers. Un seul avait une
  conséquence plaidable — le relevé lexical du
  [01](01_cible_these_adverse.md), qui annonçait trois occurrences de
  « intérêt » au lieu de deux : **corrigé**, avec le relevé ramené à 66
  paragraphes. La table de références de P-19 au § 6 est régénérée en
  conséquence. Rien n'est modifié hors de l'atelier (§ 4.5), et la base n'est
  pas touchée — y compris le champ `document_original_date` du `document:1`,
  qui porte une valeur sans source.
- **14 octobre 2026 — création.** Périmètre et principe organisateur consignés
  sur décision du demandeur. Identification des trois actes en base confirmée
  et vérifiée contre les références du corpus. Références relevées pour les
  trois actes. Trois écarts signalés au § 4, aucun corrigé. Aucun texte d'acte
  modifié, aucune donnée en base touchée, aucune cote attribuée.
