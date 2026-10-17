# Fusion des citations — plan

Évaluation du 2026-10-14, révisée deux fois le même jour après les réponses de LP. Chiffres
mesurés ce jour par `mesure_doublons.py` et `mesure_phrases.py` (lecture seule). Les relancer
avant toute écriture, car la base bouge.

> **2026-10-17 — Le ménage est abandonné au profit de deux régimes** (décision de LP). Les
> 394 citations actuelles forment l'**ancien régime** et ne sont ni fusionnées, ni normalisées,
> ni repointées. Le nouveau pont ne prend que des citations du **nouveau régime**, créées sous
> la règle de la phrase, avec position, certification et unicité garanties en base. Les
> §§ 3 à 7 ci-dessous ne s'appliquent plus aux citations existantes. Ce qui survit : la règle
> de la phrase et ses précisions (§ 3.3), la garde à la création, devenue une contrainte
> d'unicité, et le traitement des doublons de **documents** (email 48 / 347). Évaluation :
> `docs/modele_preuve/CONCEPTION_PREUVE.md` § 17.
>
> **2026-10-15 — Modèle Preuve.** LP propose une couche intermédiaire :
> paragraphe → démonstration → preuve → élément de preuve (`docs/modele_preuve/CONCEPTION_PREUVE.md`).
> Elle rouvre le choix « phrase stricte ou suite de phrases » (§3.2) et suspend la ligne de
> précision (§4.4). Le reste du plan tient : la garde, la fusion 1 → 1, les clés génériques et
> l'ordre « ménage avant version 2 ».

## Le plan évalué (LP, mot pour mot)

> chaque app de "document-preuve" on un modele quote. Un lien existe entre le model quote et
> le document duquel elle est originaire, ce qui implique que de la quote, le document est
> récupérable. Un probleme existe entre les quote d'un meme document, elles se répêtent, non
> seulement elles se repetent, mais une instance d'une même quote peut etre découpé
> différement, ce qui fait qu'une fois tokenisé, les quotes entre elles ne seront pas
> exactement pareille. Un ménage devrait etre fait de maniere a pouvoir lier les quotes et les
> document aux paragraphes de la nouvelle version. POur le ménage de quote une fonction
> "merge" qui permetterait de choisir la bonne version de la quote ainsi que les duplicat
> innadéquat et remplacer la fk de la mauvaise version par celle de la bonne partout ou elle
> est utilisée.

## Les réponses de LP (2026-10-14, mot pour mot)

> que penses tu de cette rêgle : une sitation est une phrase. En la définissant ainsi le
> toutefois serait alors inclut dans la citation.

> si une référence a une quote est supprimé, normalement une autre devrait la remplacer, le
> "merge devrait s'en occuper"

> ceci pose probleme : Les 69 citations de plusieurs phrases se scindent ; chaque lien vers
> elles devient plusieurs liens, sans rien perdre. le liens sera remplacer par autant de lien
> qu'il y aura de nouvelle citation. cela demandera un ajustement d,architecture.

Le sort des 80 nœuds-citations des docs 5 et 6 reste **en suspens**.

---

## 1. Verdict

Le diagnostic est juste et le moment est le bon.

**La règle arrêtée : une citation est une phrase, au sens strict** (LP, 2026-10-15, §3.2). Les
bornes de chaque citation tombent sur des fins de phrase, fixées par la source et non par la
main qui découpe. Grâce à cette règle :

- **les doublons ne peuvent être qu'identiques**. Deux extractions de la même phrase donnent la
  même citation : l'inclusion et le chevauchement disparaissent ;
- **« la bonne version » n'a plus à être choisie** : c'est la phrase telle que la source la
  porte ;
- **la scission d'une citation de plusieurs phrases (1 → N) se fait dans l'arbre d'une preuve**
  du nouveau pont (`docs/modele_preuve/CONCEPTION_PREUVE.md`). Elle ne reste coûteuse que pour
  les porteurs de l'ancien pont qui pointent directement vers une citation.

*Une première révision retenait « une phrase ou une suite de phrases contiguës », pour garder
toute opération 1 → 1. Le modèle Preuve a levé cette contrainte. Les chiffres du §3.2
décrivent cette variante. Sous la règle stricte, les 17 groupes de plages qui se chevauchent se
ramènent à des phrases distinctes ou identiques.*

Trois points du plan initial restent entiers :
- **fermer le robinet** (§4.1) ;
- **les références que Django ne voit pas** (§4.2) ;
- **l'ordre** : finir le ménage avant de lier quoi que ce soit à la version 2 (§4.3).

**Taille : petit chantier.** Le travail de LP se concentre sur les 16 citations à examiner une
à une et sur les précisions de la règle (§3.3, §5).

---

## 2. État mesuré

**Deux modèles, pas un par application.** Seuls `email_manager.Quote` et `pdf_manager.Quote`
existent. Le clavardage passe par `ChatSequence` (un M2M de messages) ; photos, événements et
vidéos n'ont pas de citation.

| | Citations | Sources | Paires identiques | Inclusion | Chevauchement partiel | Citations impliquées |
|---|---|---|---|---|---|---|
| courriels | 268 | 203 | 10 | 9 | 11 | **57** |
| PDF | 126 | 44 | 11 | 6 | 15 | **38** |

**Le ménage d'août n'a pas porté sur les doublons.** Sur les 14 groupes listés au §5 de
`CARTE_RELATIONS.md`, **11 sont intacts** : eq-31/194, eq-50/63, eq-101/105, eq-145/198,
eq-146/199, eq-152/186, pq-3/24/51, pq-8/53, pq-14/67, pq-70/72 et pq-75/83.

**Les références vers une citation :**

| Porteur | Mécanisme | Lignes | Vu par Django au `delete` ? |
|---|---|---|---|
| `TrameNarrative.citations_courriel` | M2M | 267 | oui |
| `TrameNarrative.citations_pdf` | M2M | 260 | oui |
| `LibraryNode` | clé générique | 80 (eq 78, pq 2) — docs 5 « Test » et 6 « Affidavit » | **non** |
| `ProducedExhibit` | clé générique | 585 (eq 388, pq 197) — table dérivée | **non** |
| `AppuiFait`, `RattachementAxe`, `BordereauDepotJuillet`, `ExhibitRegistry`, `GeminiResponse` | clé générique | 0 aujourd'hui | **non** |
| `legal/**/*.md` | texte | 0 référence à une PK de citation | — |

---

## 3. La règle : des bornes qui tombent sur des fins de phrase

### 3.1 Ce qu'elle règle

- **L'identité.** Une citation s'identifie par **sa source, sa première phrase et sa dernière
  phrase**. Deux extractions du même passage donnent la même plage, donc la même citation. Un
  chevauchement reste possible (phrases 3-4 contre 4-5), mais il se mesure exactement et se
  traite 1 → 1 (§3.2).
- **Le connecteur.** « Toutefois, » est inclus d'office. pq-141 et pq-31 se calent sur la même
  plage.
- **La version fidèle.** La citation qui survit porte le passage tel que la source le porte.
  Aucune variante n'est *choisie*. Le cas eq-2 / eq-192 se règle de lui-même : la faute de
  frappe reste, parce qu'elle est dans le courriel. Pour un PDF, le passage se lit sur la
  transcription mais **se certifie sur le scan** (§3.4).
- **La troncature.** Une citation qui ne coupe aucune phrase met à l'abri du reproche d'avoir
  tronqué un passage pour en changer le sens.
- **La concordance avec le pont.** Le modèle `BordereauDepotJuillet` décrit la cote du pont en
  ces termes : « il s'appuie en fait sur une **phrase** de P-98, qui devient P-98.1 » (§4.4).

### 3.2 Une phrase, ou une suite de phrases ? — la suite

**L'objection de LP est fondée.** Avec la phrase stricte, chacune des 69 citations de plusieurs
phrases doit être scindée, et chaque lien vers elle devient N liens. Ce passage de 1 à N casse
l'hypothèse sur laquelle repose la fusion : on remplace une clé par une autre. Il touche
plusieurs endroits du schéma :

| Porteur | Ce que la scission y fait |
|---|---|
| `LibraryNode` | un nœud ne pointe que vers un objet. 20 nœuds deviendraient N nœuds frères, ce qui change la structure du document |
| `ConfirmationAppui` | la `portee` décrit ce que le **passage** établit. Elle serait recopiée sur N lignes ou découpée phrase par phrase |
| `AppuiFait` | même chose pour `role` et `note` |
| Le pont | un paragraphe appuyé sur un passage de 3 phrases citerait « P-98.1 à P-98.3 » au lieu de « P-98.1 » |
| La fusion | elle devrait gérer 1 → N au lieu de 1 → 1 |

**Avec la suite de phrases contiguës, rien ne se scinde.** Les 69 citations de plusieurs phrases
complètes sont **déjà conformes**. Le reste se fait par remplacement 1 → 1 :

| Opération | Nombre | Nature |
|---|---|---|
| Déjà conformes (une ou plusieurs phrases entières) | 203 (167 courriels, 36 PDF) | rien à faire |
| Fragments à étendre jusqu'à leurs bornes de phrase | 138 | 1 → 1, le lien couvre un peu plus (×1,6 à ×1,9 en médiane) |
| Groupes de **même plage** une fois calés | 25 (15 courriels, 10 PDF) | fusion 1 → 1, automatique |
| Groupes de plages **qui se chevauchent** | 17 (10 courriels, 7 PDF) | décision de LP, 1 → 1 dans les deux cas : remplacer par l'union, ou garder distincts |

Deux unions dépassent 500 caractères :
- **pdf-5** : pq-92, 93, 97, 98 et 116, 1 065 caractères ;
- **pdf-13** : le procès-verbal horodaté, 515 caractères.

La seconde se réduit dès que les énumérations ont leur règle (§3.3).

**Tranché le 2026-10-15 : la phrase stricte** (LP). Le raisonnement qui suit l'a rendue
praticable.

**Rouvert le 2026-10-15 par le modèle Preuve.** Si le paragraphe pointe vers une démonstration
et non vers une citation, scinder une citation en N phrases revient à remplacer une feuille par
N feuilles sœurs dans l'arbre d'une preuve. Le lien du paragraphe n'est pas touché. L'objection
au passage de 1 à N ne vaut alors que pour les porteurs qui pointent **directement** vers une
citation : les M2M de `TrameNarrative` (sans valeur, cadrage d'août) et les 20 nœuds des docs 5
et 6 (en suspens). La phrase stricte redevient praticable. Le choix dépend de la forme retenue
pour le modèle Preuve.

### 3.3 Où « phrase » n'est pas défini — précisions à arrêter

Les plus grandes expansions mesurées viennent du **pdf-13**, un procès-verbal horodaté.
pq-75, pq-83 et pq-157 sont une ligne terminée par « ; ». Avec la définition minimale, leur
« phrase » couvre 483 caractères sur 9 lignes. Les précisions à arrêter :

- **Les énumérations.** Chaque élément terminé par « ; » ou par un retour à la ligne doit
  compter comme une phrase. Sinon, une citation avale toute la liste.
- **La phrase qui annonce une liste.** Elle se termine par « : ». pq-2, le bloc de P-2 le plus
  repris dans l'analyse, en est un exemple. Elle doit être une unité, sinon elle avale ce
  qu'elle annonce.
- **Les courriels écrits sans ponctuation.** Le retour à la ligne y tient lieu de fin de phrase.

**Formulation proposée :**

> Une citation est une phrase entière, ou une suite de phrases entières contiguës, de la
> source, telle que la source la porte. Une phrase se termine par « . », « ? », « ! », « … »
> ou par un saut de paragraphe. Dans une énumération, la phrase d'introduction (terminée par
> « : ») et chaque élément (terminé par « ; » ou par un retour à la ligne) sont chacun une
> phrase. Un fragment se met en évidence au rendu, jamais dans la base.

### 3.4 Les 48 citations « non localisables » — ce qu'elles sont

La mesure exige que la citation se retrouve **mot pour mot** dans le texte stocké de la source,
aux accents, à la casse et à la ponctuation près. L'étiquette « retouchée ou élidée » donnée au
premier passage était inexacte. Le diagnostic au cas par cas donne ceci :

| Cause | Courriels | PDF | Traitement |
|---|---|---|---|
| **Quelques mots diffèrent.** Courriels : la citation corrige une coquille de l'original (eq-192). PDF : surtout une erreur d'OCR dans la transcription (« modi8cation », « rémunératrices8 ») | 9 | 13 | **Ancrage automatique** : le passage est identifié sans ambiguïté. Reste la question du verbatim : pour un courriel, la source fait foi ; pour un PDF, le scan tranche |
| **Lecture d'un tableau, pas une copie**, avec ancre `position_anchor` | — | 4 | Prévu par le modèle. **Hors de la règle** : une lecture n'est pas une citation |
| **Texte absent de la transcription** : 4 lectures de tableaux chiffrés sans ancre (pq-78 à 81), 2 à examiner (pq-47, pq-77) | — | 6 | Ajouter l'ancre aux 4 ; examiner les 2 |
| **Saut dans la transcription** : 5 au saut de page (en-tête ou pied de page intercalé, dont pq-31 et pq-141), 4 sans marque de page | — | 9 | Ancrage sur la plage qui enjambe le saut, à vérifier |
| **Élision explicite `[...]`** | 3 | 2 | Décision de LP : plage englobante (1 → 1, le passage élidé revient) ou deux citations |
| **Recollage sans marque** (eq-93) ; **bloc de réponse citée « > »** (eq-5) | 2 | — | Manuel |

**Les cas qui demandent vraiment un examen à la main sont 16** : 9 sauts de transcription,
5 élisions, eq-93 et eq-5. S'y ajoutent les 2 textes absents à examiner et 4 ancres à poser.
Les 22 cas où quelques mots diffèrent s'ancrent seuls. Ils posent seulement la question du
verbatim, qui se tranche contre l'original.

---

## 4. Ce qui reste du plan initial

### 4.1 Fermer le robinet

90 citations ont été créées depuis le 11 août. pq-157 (3 sept.) reproduit pq-75 et pq-83, et
pq-141 (28 août) reprend pq-31. **La garde à la création** fonctionne ainsi :
- l'outil cale la sélection sur les bornes de phrase ;
- si une citation de **même plage** existe, il la réutilise ;
- si la sélection **chevauche** une citation existante, il la montre avant d'en créer une autre.

La garde et la normalisation reposent sur le même segmenteur.

### 4.2 La fusion remplace toute référence (décision de LP)

**La fusion ne supprime aucune référence : elle la repointe vers la citation qui survit.** Cela
vaut pour tous les porteurs du §2, `LibraryNode` compris. Le sort des 80 nœuds des docs 5 et 6
est en suspens, mais c'est une question distincte : d'ici là, la fusion les repointe comme le
reste.

Avec la règle du §3.2, **chaque remplacement est 1 → 1**. La seule exception possible concerne
les élisions, si LP choisit de les scinder en deux citations : 5 cas, à recâbler à la main,
trop peu pour justifier une adaptation du schéma.

Points techniques à traiter :
- **Les clés génériques sont invisibles pour le collector de Django.** On réutilise le scanner
  de `purger_quotes.py`, qui refuse de s'exécuter si un modèle inconnu pointe vers une citation.
- **Les contraintes d'unicité.** `AppuiFait (fait, ct, oid)` et `RattachementAxe (axe, ct, oid)`
  sont uniques. Si deux variantes appuient le même fait, il faut dédoublonner avant de
  repointer. Pour les M2M, on fait l'union : une trame qui citait les deux variantes garde une
  seule ligne.
- **L'exécution.** Une seule transaction, précédée de la sauvegarde `backup_avant_purge.py`.
  `ProducedExhibit` est ensuite reconstruite.
- **Un journal de redirection** (ajouté le 2026-10-15). Chaque fusion consigne « citation
  absorbée → citation qui survit ». Le bordereau versionné du nouveau pont donne une sous-cote
  à chaque citation, et une version gelée peut citer une citation absorbée depuis. La
  correspondance entre versions passe par ce journal. Pour la même raison, une citation qu'une
  version gelée utilise ne se supprime plus : elle se redirige
  (`docs/modele_preuve/CONCEPTION_PREUVE.md` §3.4, point 2).

### 4.3 L'ordre : finir le ménage avant la version 2

Le pont **enregistre** ses cotes de façon durable. Si deux variantes d'un même passage y
entraient, elles recevraient deux cotes, P-98.1 et P-98.2. Une fois l'acte notifié, on ne
pourrait plus les fusionner.

La fenêtre est encore ouverte :
- 0 ligne de précision au bordereau ;
- 0 appui de juillet ne porte de précision ;
- 1 seule `ConfirmationAppui`.

### 4.4 Ce qu'est une « ligne de précision »

`BordereauDepotJuillet` contient une ligne par pièce cotée. La ligne de P-98, par exemple,
pointe vers un courriel (modèle + pk). Aujourd'hui, un paragraphe de la version 2 ne peut
s'appuyer que sur **la pièce entière**. C'est le cas du seul lien existant
(`ConfirmationAppui` n° 1 : § 22 de la version 2 → P-19).

L'épopée E01 a prévu le cas où le paragraphe s'appuie sur un passage précis de la pièce. Le
modèle crée alors une **ligne enfant** sous P-98, cotée « P-98.1 ». Ses champs `parent` et
`rang_precision` existent déjà. Ce qui n'est **pas** fixé, c'est **vers quoi pointe cette ligne
enfant**. L'aide du champ `content_type` ne nomme que des modèles de pièces.

**Suspendu le 2026-10-15.** La recommandation précédente faisait pointer la ligne enfant vers
la citation, pour relier le paragraphe à la citation par `ConfirmationAppui`. Le modèle Preuve
remplace ce chemin : paragraphe → démonstration → preuve → élément de preuve. La chaîne donne
déjà le passage précis. Une sous-cote, si l'acte en a besoin, se **calcule** depuis la chaîne
au lieu d'être stockée. Voir `docs/modele_preuve/CONCEPTION_PREUVE.md` §4.

---

## 5. Taille

| Pièce | Effort | Ce qui existe déjà |
|---|---|---|
| Segmenteur de phrases (règle et précisions du §3.3) et ses tests | ½ à 1 jour | `mesure_phrases.py` en donne le noyau |
| Calage : étendre 138 fragments, ancrer 22 variantes | automatique, avec revue | `core.text_matching.locate` |
| Fusion des 25 groupes de même plage | automatique | — |
| Fusion générique 1 → 1 : repointage, transaction, tests | ≈ 1 jour | scanner de `purger_quotes.py`, `backup_avant_purge.py` |
| Garde à la création | ≈ ½ jour | le même segmenteur |
| **Temps de LP** | précisions de la règle (§3.3), 16 cas manuels, 22 questions de verbatim | — |

## 6. Ordre recommandé

0. **Arrêter la forme du modèle Preuve** sur papier (`docs/modele_preuve/CONCEPTION_PREUVE.md`).
   Le choix du §3.2 en dépend.
1. **Arrêter la règle et ses précisions** (§3.2 et §3.3) — décision de LP.
2. **Le segmenteur et la garde à la création**, pour fermer le robinet.
3. **Caler les citations existantes** sur leurs bornes de phrase : étendre et ancrer.
4. **Fusionner** : d'abord les plages identiques (automatique), puis les plages qui se
   chevauchent, selon la décision de LP.
5. **Lier à la version 2** par la chaîne du modèle Preuve.

## 7. Décisions

| Question | État |
|---|---|
| Les connecteurs (« Toutefois, ») font-ils partie de la citation ? | ✅ Oui, par la règle (LP, 2026-10-14) |
| Une référence supprimée doit-elle être remplacée ? | ✅ La fusion repointe toute référence et n'en supprime aucune (LP, 2026-10-14) |
| Les 80 nœuds des docs 5 et 6 | ⏸ En suspens (LP, 2026-10-14). D'ici là, la fusion les repointe |
| Une phrase stricte, ou une suite de phrases contiguës ? (§3.2) | ✅ **Une phrase, au sens strict** (LP, 2026-10-15). Le modèle Preuve absorbe la scission dans l'arbre (`docs/modele_preuve/CONCEPTION_PREUVE.md` §7) |
| Précisions de la règle : énumérations, « : », retours à la ligne (§3.3) | ❓ À arrêter par LP |
| 17 groupes de plages qui se chevauchent : union, ou citations distinctes ? | ✅ Sans objet sous la phrase stricte : chaque plage se scinde en phrases, identiques ou distinctes |
| 5 élisions : plage englobante, ou deux citations ? (§3.4) | ❓ LP, cas par cas |
| La ligne enfant « P-98.1 » pointe-t-elle vers la citation ? (§4.4) | ⏸ Suspendu par le modèle Preuve (2026-10-15) : la sous-cote se calculerait depuis la chaîne |
