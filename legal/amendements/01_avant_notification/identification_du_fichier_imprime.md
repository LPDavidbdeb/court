# Identification du fichier imprimé pour le dépôt du 24 juillet 2026

> **Déclarations du demandeur, 13 octobre 2026.** (1) Le fichier d'abord utilisé
> pour l'impression est `legal/docx_file/demande_DEPOT_2026-07-21_double.docx`.
> (2) Cette première impression était une **erreur**, constatée puis écartée ;
> le papier déposé est la version simple de **44 pages, endos inclus**.
>
> **Vérifié.** Le fichier nommé en (1) est **identique bit pour bit** au candidat gelé
> `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21_double.docx` —
> même empreinte SHA-256 `6b65d0117851d1cf982e34709c561f81288c97297a1b6b6b613d5b71386a145e`.
> La question « lequel des cinq candidats a été imprimé »
> (`legal/depots/2026-07-24_initial/README.md` § 2) est **close au niveau du
> fichier**.
>
> Ce fichier contient la demande **deux fois**, et les deux copies ne portent
> **pas** les mêmes numéros de paragraphes (§ 3). Le demandeur a lu le papier le
> 13 octobre : il porte la numérotation de la copie 1 (§ 3 bis) — qui est aussi
> celle de la version simple, finalement imprimée (§ 3 quater).
>
> ✅ **L'ancrage est fixé.** L'impression de `_double` a été un essai écarté.
> **L'acte déposé est la version simple de 44 pages, endos inclus** — le `.docx`
> produit par le service, ou son PDF, qui portent la même numérotation : 1 … 241.
> Voir § 3 quater. Le préalable posé par `communication_pieces.md` § 10.2 c est
> levé.

---

## 1. Ce que contient le fichier

`_double` n'est pas une variante de mise en page : c'est la demande **imprimée
en double**, les deux copies à la suite dans un seul fichier.

| | Copie 1 | Copie 2 |
|---|---|---|
| En-tête de cour (CANADA / COUR SUPÉRIEURE / parties) | oui | oui |
| Corps de l'acte | identique | identique |
| Conclusions, bordereau, signature | oui | oui |
| **Dos de l'acte** (« N° : ____ / COUR SUPÉRIEURE / DISTRICT… / Montant en litige : 244 779 $ ») | **non** | **oui** |

Le texte des deux copies est **mot pour mot identique**. La **seule** différence
de contenu est le dos de l'acte, présent uniquement à la fin de la copie 2.

C'est le schéma habituel du comptoir : deux exemplaires, le greffe en conserve
un et estampille l'autre.

## 2. Comment les autres candidats se distinguaient

Analyse retenue pour mémoire, les cinq candidats n'étant plus en concurrence :

| Candidat | Signe distinctif |
|---|---|
| `_entete.docx` (13 h 57) | « POUR CES MOTIFS » **et** « SIGNATURE » commencent chacun **en haut d'une page neuve** (3 sauts de page) |
| `.docx` (14 h 17) | un seul saut de page, avant le dos ; « POUR CES MOTIFS » et « SIGNATURE » tombent **en cours de page** |
| `.pdf` (14 h 23) | même mise en page que le `.docx` ; **44 pages**, « POUR CES MOTIFS » p. 41, « SIGNATURE » p. 43, dos seul p. 44 |
| **`_double.docx` (14 h 14)** | **l'acte apparaît deux fois** ; dos à la toute fin seulement |
| `bordereau_bloc_depot.docx` (14 h 29) | document distinct — le bordereau, non la demande |

## 3. 🔴 Les deux copies ne portent pas les mêmes numéros

Dans un `.docx`, chaque bloc de liste numérotée est une **instance** désignée
par un `numId`, avec un numéro de départ (`startOverride`). **Réemployer le même
`numId` plus loin dans le fichier ne redémarre pas le compteur : il continue.**

Or la copie 2 réemploie **83 des 85 instances** de la copie 1. Ses compteurs
continuent donc là où la copie 1 les a laissés.

### Prédiction, à vérifier sur le papier

Reconstitution de la numérotation de Word à partir de `document.xml` et de
`numbering.xml`. **La méthode a d'abord été validée contre le PDF rendu**, où
elle retrouve exactement les numéros imprimés (1, 2, 12, 15, 241 aux repères
ci-dessous) :

| Incipit du paragraphe | Copie 1 | Copie 2 |
|---|---|---|
| « La présente demande vise à faire déclarer abusives… » (1er § sous OBJET DE LA DEMANDE) | **1** | **2** |
| « Le demandeur, Louis-Philippe David, et la défenderesse… » (1er § sous § I) | **2** | **8** |
| « À la naissance d'Alexia, la défenderesse a pris… » | **12** | **15** |
| « Le demandeur reconnaît avoir commis une infidélité… » | **15** | **19** |
| « Le 12 septembre 2011, le demandeur écrivait à une amie… » | **18** | **22** |
| « Les pièces P-3, P-10 et P-88 sont des communications… » (dernier §) | **241** | **242** |

**La copie 1 porte exactement la numérotation du PDF.** La copie 2 en diffère
dès le premier paragraphe.

### Le contrôle le plus rapide

Sur la copie papier : lire le numéro du **premier paragraphe numéroté**, celui
qui commence par « La présente demande vise à faire déclarer abusives ».

- Il porte **1** → c'est la **copie 1**.
- Il porte **2** → c'est la **copie 2**.

Le dos de l'acte donne le même renseignement : seule la copie 2 en a un.

## 3 bis. ✅ Le papier exclut la copie 2 — vérifié le 13 octobre 2026

Le demandeur, copie papier en main, a relevé deux choses :

1. le **premier paragraphe numéroté** — « La présente demande vise… » — porte
   **1** ;
2. la numérotation saute **entre 110 et 112, entre 118 et 122, et entre 139 et
   143**.

Les deux **excluent la copie 2**. Ils concordent avec la copie 1 — et aussi,
on le verra au § 3 quater, avec la version simple, qui porte la même
numérotation :

| Contrôle | Copie 1 | Copie 2 | Papier |
|---|---|---|---|
| Premier § numéroté | **1** | 2 | **1** ✅ |
| Trou 110 → 112 | **oui** | non | **oui** ✅ |
| Trou 118 → 122 | **oui** | non | **oui** ✅ |
| Trou 139 → 143 | **oui** | non | **oui** ✅ |

Le PDF rendu porte les mêmes trous : les ¶ 111, 119 à 121 et 140 à 142 n'y
existent pas, et les paragraphes qui encadrent chaque trou y portent les mêmes
incipits.

### Conséquence : les quatre candidats de la demande portent la même numérotation

La reconstitution donne **exactement la même suite de numéros** pour
`demande_DEPOT_2026-07-21.docx`, `_entete.docx` et la **copie 1** de
`_double.docx`. Ces fichiers diffèrent par la **mise en page** — où tombent les
sauts de page — et non par la numérotation. La seule numérotation divergente du
lot est celle de la **copie 2** de `_double`, qui n'a pas été remise.

➜ **Le PDF est donc un substitut fidèle du papier pour tout ce qui touche aux
numéros de paragraphes.** Et la réserve inscrite en tête de
[`verification_ancrages_paragraphes_acte_depose.md`](verification_ancrages_paragraphes_acte_depose.md)
— « le présent constat vaut pour le candidat PDF » — **est levée** : son
résultat, **47 paragraphes sur 179 portant un numéro différent de celui du
`.md`**, vaut pour l'acte déposé lui-même.

### Pourquoi cela comptait

Si la prédiction se vérifie, **l'exemplaire remis au greffe et l'exemplaire
conservé par le demandeur ne portent pas la même numérotation**. Toute
désignation « ¶ n de la demande déposée » doit alors préciser *de quel
exemplaire*, et la concordance doit ancrer sur celui que **le greffe détient** —
pas sur celui qui est sous la main.

## 3 ter. La chaîne de production, et ce qu'elle ne dit pas

### Le `.md` source est bien `legal/demande_DEPOT_2026-07-21.md`

`legal/markdown_to_docx_service.py` reproduit sous `legal/docx_file/` l'arbo­rescence
de la source : « *The output mirrors the source path relative to legal/* —
`legal/analyse/foo.md -> legal/docx_file/analyse/foo.docx` ». Le `.docx` se
trouvant **directement** dans `legal/docx_file/`, sa source se trouvait
**directement** dans `legal/`. Ce fichier existe : `legal/demande_DEPOT_2026-07-21.md`.

### Mais `_double` et `_entete` n'ont pas été produits par ce service

Aucun `legal/demande_DEPOT_2026-07-21_double.md` ni `_entete.md` n'existe. Les
métadonnées internes des trois `.docx` le confirment :

| Fichier | Pages (Word) | Mots | Auteur | Temps d'édition |
|---|---|---|---|---|
| `demande_DEPOT_2026-07-21.docx` | 44 | 12 643 | *(vide)* | **0 min** |
| `_entete.docx` | 45 | 12 644 | David, Louis-Philippe | 7 min |
| `_double.docx` | **88** | 25 206 | David, Louis-Philippe | 1 min |

Le `.docx` de base ne porte ni auteur ni temps d'édition : il sort de la
conversion. Les deux autres ont été ouverts et enregistrés dans Word. 88 = 2 × 44.

➜ **Chaîne : `legal/demande_DEPOT_2026-07-21.md` → (service) →
`demande_DEPOT_2026-07-21.docx` → (Word, à la main) → `_double.docx` → papier.**

*Fil non refermé :* les dates de modification placent `_double` (14 h 14) **avant**
le `.docx` de base (14 h 17). Celui qui est sur le disque a donc été régénéré
après coup. La conversion étant déterministe et la numérotation des deux étant
identique, cela ne change rien au résultat.

### Aucun `.md` ne porte exactement les sauts du papier

Recherche sur **tous** les `.md` du dépôt comptant au moins cent paragraphes
numérotés, en cherchant les trois trous lus sur le papier :

| Fichier | 110→112 | 118→122 | 139→143 |
|---|---|---|---|
| `legal/demande_DEPOT_2026-07-21.md` | ✅ | ✅ | ❌ |
| sa copie gelée dans `candidats/` | ✅ | ✅ | ❌ |
| `demande_amendee.md` (copie du même texte) | ✅ | ✅ | ❌ |
| tous les autres | ❌ | ❌ | ❌ |

**Aucun fichier ne fait 3 sur 3.** Le `.md` saute 139 → **141** puis 143 → 145 ;
le papier saute 139 → **143**. C'est la démonstration locale du mécanisme :

| N° dans le `.md` | N° imprimé | Incipit |
|---|---|---|
| 136 | **135** | Le 23 janvier 2019, Me Marie-Josée Ayoub a reconnu… |
| 138 | **136** | Le 19 août 2019, Allianz Technology SE München… |
| 139 | **137** | Les 26 et 27 septembre 2019, le demandeur a informé… |
| 141 | **138** | Ce jugement ordonnait aussi à la défenderesse… |
| 142 | **139** | Le 15 octobre 2019, le demandeur a transmis à Me Marie-Josée Ayoub… |
| 143 | **143** | Le 21 octobre 2019, la défenderesse Élise Ayoub a signé… |
| 145 | **144** | Au paragraphe 3, la défenderesse a affirmé : |
| 146 | **146** | La déclaration rattachait cette affirmation au jugement… |

Le bloc se recale à 143, et le trou imprimé 139 → 143 naît là. **C'est
exactement le type d'écart que compte le présent dossier : 47 paragraphes sur
179.**

## 3 quater. ✅ Le papier déposé fait 44 pages, endos inclus — la question est close

> **Récit du demandeur, 13 octobre 2026.** Il a lui-même créé `_entete.docx` et
> `_double.docx` pour mettre en forme la présentation du dossier et des parties.
> Il a **imprimé `_double` une première fois, puis constaté son erreur**.
> L'exemplaire papier qu'il détient est la version déposée : **44 pages, page
> d'endos incluse**.

Ce signalement tranche, parce qu'aucune des deux copies de `_double` ne
correspond à cette description :

| | Pages | Endos | 1er § | Trous 110→112, 118→122, 139→143 |
|---|---|---|---|---|
| `_double` copie 1 | ~43 (pagination 1→43) | **non** | 1 | oui |
| `_double` copie 2 | ~45 (pagination 44→88) | oui | **2** | **non** |
| `_entete.docx` | **45** | oui | 1 | oui |
| **`demande_DEPOT_2026-07-21.docx`** | **44** | **oui** | **1** | **oui** |
| **`demande_DEPOT_2026-07-21.pdf`** | **44** | **oui** (seule en p. 44) | **1** | **oui** |

➜ **Le document déposé est la version simple de 44 pages** — le `.docx` produit
par le service, ou le PDF qui en sort. Les deux portent **la même numérotation**,
de sorte que le choix entre eux est sans effet sur les numéros.

L'impression de `_double` a été un essai écarté. Ses deux copies sont donc hors
du dossier : la copie 1 n'avait pas d'endos, la copie 2 était numérotée 2 … 242.

### Hypothèse d'un assemblage physique — sans effet sur l'ancrage

> **Précision du demandeur** : il a peut-être imprimé l'endos **séparément**,
> depuis la version double, et assemblé les feuilles à la main. Le `.docx`
> utilisé pour le corps n'en comporterait alors pas.

**Cette hypothèse ne touche pas la numérotation**, pour une raison simple :
**l'endos ne porte aucun paragraphe numéroté.** C'est une page de couverture —
numéro de dossier, tribunal, district, parties, titre, montant en litige, partie
qui produit l'acte. Le corps, lui, porte la même numérotation dans **tous** les
candidats sauf la copie 2 de `_double`, que la lecture du papier exclut déjà
(premier § « 1 », les trois trous).

Les deux routes donnent d'ailleurs le même nombre de feuilles : le corps occupe
**43 pages** partout, et l'endos en ajoute une.

| Route | Corps | Endos | Total |
|---|---|---|---|
| Version simple imprimée d'un bloc | p. 1 à 43 | p. **44** | 44 |
| Corps de `_double` copie 1 + endos ajouté | p. 1 à 43 | p. **88** (dernière page de `_double`) | 44 |
| Endos pris dans `_entete.docx` | p. 1 à 43 | p. **45** | 44 |

#### Le contrôle qui départage

**Lire le numéro imprimé au bas de la page d'endos.** La pagination est
continue et sans section distincte ; le pied de page figure bien sur l'endos —
vérifié dans le PDF, où il porte **44**, en bas de page (y ≈ 743 sur 792).

- **44** → version simple, imprimée d'un bloc.
- **88** → endos détaché de `_double`, assemblé à la main.
- **45** → endos pris dans `_entete.docx`.

Un saut visible de **43 à 88** entre l'avant-dernière et la dernière feuille
signerait l'assemblage.

Ce contrôle sert à **décrire fidèlement l'acte matériel** — utile si sa
composition est un jour discutée. Il **ne conditionne pas** la table de
concordance.

### Ce qui est désormais établi

1. Le papier déposé porte la numérotation **1 … 241**, avec les trous que le
   demandeur a lus (110→112, 118→122, 139→143) — **quelle que soit la façon dont
   l'endos a été ajouté**.
2. Cette numérotation est **identique** à celle du PDF, du `.docx` simple, de
   `_entete.docx` et de la copie 1 de `_double`. **Les candidats ne différaient
   que par la mise en page.**
3. Le PDF est donc un **substitut exact** du papier pour tout ce qui touche aux
   numéros de paragraphes, et la numérotation déposée est **calculable** sans
   transcription.
4. La réserve de
   [`verification_ancrages_paragraphes_acte_depose.md`](verification_ancrages_paragraphes_acte_depose.md)
   est levée sans résidu : ses **47 paragraphes sur 179** valent pour l'acte
   déposé.

Une **copie conforme** du greffe garde son utilité — figer matériellement le
référent — mais elle n'est plus un préalable à la réécriture.

## 4. Ce que cela règle et ce que cela ne règle pas

**Réglé.**

1. Le **fichier source** est identifié et gelé.
2. **Lequel des deux exemplaires** porte la numérotation du dépôt : la copie 1.
3. La **numérotation imprimée est calculable** — elle n'a pas à être transcrite
   à la main depuis le papier, la reconstitution étant validée contre le PDF et
   contre quatre lectures du papier.
4. La **réserve du PDF est levée** : le constat des 47 paragraphes sur 179 vaut
   pour l'acte déposé.

**Non réglé.**

1. **La numérotation 1 reste dans la base.** `LibraryNode.item` porte les
   numéros du `.md` de travail, que l'importateur lit
   (`import_demande_depot.py:47`). Ils diffèrent des numéros imprimés. Voir
   [`verification_ancrages_paragraphes_acte_depose.md`](verification_ancrages_paragraphes_acte_depose.md)
   et `legal/instance/evaluation_cahier_E01_numerotation.md` § 1.
2. ~~La table `.md → imprimé` n'est pas encore produite.~~ **✅ Produite le
   13 octobre 2026** : [`concordance_md_imprime.md`](concordance_md_imprime.md)
   et `concordance_md_imprime.json`. 198 lignes, appariement sans ambiguïté,
   et accord **11 sur 11** avec l'échantillon publié le 7 octobre.
3. **La copie conforme du greffe** reste utile pour figer matériellement le
   référent papier (`legal/depots/2026-07-24_initial/README.md` § 2, point 3) —
   d'autant plus maintenant qu'on sait que deux numérotations ont été imprimées
   le même jour, et qu'une seule a été remise.

## 5. La table `.md → imprimé` : ce qu'elle est, à quoi elle sert

### Ce qu'elle est

Une ligne par paragraphe numéroté de l'acte déposé — **198 lignes** : les 179
paragraphes à numéro simple et les 19 à suffixe littéral.

| Colonne | Contenu |
|---|---|
| `numero_md` | le numéro écrit à la main dans `legal/demande_DEPOT_2026-07-21.md` |
| `numero_imprime` | le numéro que le paragraphe porte sur le papier |
| `incipit` | les premiers mots, qui servent d'identité du paragraphe |
| `concorde` | vrai ou faux |

Extrait réel, tiré de la zone du trou 139 → 143 :

| `numero_md` | `numero_imprime` | incipit | `concorde` |
|---|---|---|---|
| 136 | 135 | Le 23 janvier 2019, Me Marie-Josée Ayoub a reconnu… | ❌ |
| 139 | 137 | Les 26 et 27 septembre 2019, le demandeur a informé… | ❌ |
| 142 | 139 | Le 15 octobre 2019, le demandeur a transmis à Me Marie-Josée Ayoub… | ❌ |
| 143 | 143 | Le 21 octobre 2019, la défenderesse Élise Ayoub a signé… | ✅ |

Les **19 paragraphes suffixés traversent sans changer** — vérifié : `8-A`,
`9-B`, `103-C`… portent le même libellé dans les deux. Sur les 179 restants,
**132 concordent et 47 non**.

### Pourquoi elle est « mécanique »

Rien n'y est à juger. Les deux numérotations sont déterminées : celle du `.md`
est tapée dans le texte, celle du papier se reconstitue depuis le `.docx`
(méthode validée contre le PDF) ou se lit dans le PDF. L'appariement se fait
par l'incipit, dans l'ordre du document. **Aucun arbitrage, donc un résultat
reproductible et vérifiable ligne à ligne contre le papier.**

### À quoi elle sert — trois usages

**1. Réparer les renvois déjà écrits.** Le corpus désigne les faits par
« ¶ n de la demande déposée » : de l'ordre de **1 600 renvois dans 76 fichiers**
(tous ne visent pas l'acte déposé). Tout ce qui a été écrit avant le 7 octobre
2026 emploie les numéros du `.md`. Environ **un paragraphe sur quatre** ne porte
pas ce numéro sur le papier. L'échantillon déjà publié dans
[`verification_ancrages_paragraphes_acte_depose.md`](verification_ancrages_paragraphes_acte_depose.md)
§ 3 le montre : sur onze ancrages du bloc de juin 2013, **cinq visent un autre
paragraphe que celui qu'on croit** — ¶ 43 → 41, ¶ 45 → 43, ¶ 46 → 44,
¶ 50 → 48, ¶ 72 → 67. Les trois qui portent le cœur de P-2 (¶ 38, 39, 40) sont
justes, mais cela s'est vérifié, cela ne se présumait pas.

**2. Fournir la colonne gauche de la concordance.** La demande modifiée se fera
sous l'**article 206 C.p.c.**, et pourra comporter **toute modification que cette
disposition permet**. Rien n'oblige chaque paragraphe modifié à nommer un
antécédent, et la table ne doit pas être présentée comme une liste de
conformité.

Son objet est **défensif**, au sens du § 10.5 de
[`communication_pieces.md`](../../instance/communication_pieces.md) : « une pièce
de défense, pas de la tenue de livres ». Elle permet, **si la question est
soulevée**, de montrer où chaque élément de l'acte déposé se retrouve dans l'acte
modifié, et d'identifier ce qui a été volontairement abandonné. Le « § déposé »
de cette table doit être le numéro du **papier**, pas celui du brouillon : une
colonne gauche fausse pour un quart de ses lignes rendrait la démonstration
inutilisable, et le § 10.2 c prévient qu'« une table bâtie sur le mauvais
référent est à refaire en entier ».

**3. Corriger la base.** `LibraryNode.item` porte aujourd'hui les numéros du
`.md`, écrits par `import_demande_depot.py` qui lit ce fichier. La table donne
ce qu'il faut stocker à la place — ou à côté. C'est le correctif du § 1.6 de
`legal/instance/evaluation_cahier_E01_numerotation.md`.

### Ce qu'elle ne fait pas

Elle ne touche ni aux pièces ni à leurs cotes, ne modifie aucun texte, ne
tranche aucune question de droit et ne décide rien sur le contenu de la demande
amendée. C'est un dictionnaire de numéros.

### ✅ Produite le 13 octobre 2026

- [`concordance_md_imprime.md`](concordance_md_imprime.md) — table complète,
  triée par numéro imprimé, précédée de la liste des 47 écarts seuls.
- `concordance_md_imprime.json` — mêmes données, plus les empreintes des sources
  et la description de la méthode. ⚠️ Ce fichier est **ignoré par git** (règle
  `*.json` du `.gitignore`), comme les autres `.json` de ce répertoire.

**Contrôle indépendant** : la table retrouve **11 sur 11** des ancrages publiés
le 7 octobre dans
[`verification_ancrages_paragraphes_acte_depose.md`](verification_ancrages_paragraphes_acte_depose.md)
§ 3 — les cinq écarts (¶ 43→41, 45→43, 46→44, 50→48, 72→67) comme les six
concordances (¶ 38, 39, 40, 81, 110, 9-B). Les deux travaux sont partis de
méthodes différentes : comparaison au PDF le 7 octobre, reconstitution depuis
le XML du `.docx` aujourd'hui. Ils donnent **47 écarts sur 179** l'un comme
l'autre.

## 6. Méthode, pour qui voudra refaire le contrôle

```bash
shasum -a 256 legal/docx_file/demande_DEPOT_2026-07-21_double.docx \
              legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21_double.docx
```

La reconstitution de la numérotation lit `word/document.xml` (ordre des
paragraphes, `w:numPr/w:numId`, `w:ilvl`) et `word/numbering.xml`
(`w:startOverride` du niveau 0 de chaque `numId`), puis incrémente par `numId`
dans l'ordre du document. Les paragraphes à suffixe littéral (`8-A`, `9-B`…) ne
sont pas des éléments de liste : ils portent leur numéro dans le texte et
traversent l'opération inchangés.
