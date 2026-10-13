# Évaluation du cahier E01 — numérotation et concordance

> **Objet.** `epic_numerotation_concordance_prompt_tests_rapport.md` (racine du
> dépôt, 437 lignes, daté du 13 octobre 2026) est un cahier d'exécution destiné
> à être transmis intégralement à un agent : 6 user stories, 16 critères
> C01–C16, 29 scénarios T01–T29, gabarit de rapport. Il n'a pas été exécuté et
> est **exclu du suivi git**.
>
> **Verdict : bon prompt, plan mal calibré.** La discipline de preuve est juste
> et le verrou de prescription est correctement traduit en logiciel. Mais le
> cahier bâtit ses 16 critères sur un référent que le dossier a déjà qualifié
> de faux, coupe la moitié bon marché du livrable, laisse sans réponse les
> trois décisions que [`suivi_paragraphes_en_base.md`](suivi_paragraphes_en_base.md)
> § 6 dit conditionner la migration, et abolit sans le dire la seule protection
> que `numerotation.py` avait installée.

Référence examinée par le cahier : `34bc98a` (main). Vérifié : ce commit
contient l'état courant de la branche de travail ; le diagnostic n'est pas
périmé. Les onze fichiers qu'il demande d'examiner existent tous.

---

## 1. 🔴 Le référent est faux à la racine

### 1.1 Ce que le cahier promet

Le cahier ouvre sur ceci : « La demande introductive déposée le 24 juillet 2026
contient des interruptions de numérotation et des numéros suffixés. Sa
représentation dans l'application doit pouvoir afficher **les numéros
d'origine**. » Sa première *user story* s'intitule « Lire la numérotation
d'origine » et se justifie ainsi : « je veux retrouver **les numéros qu'il
porte**, afin de pouvoir le citer et le comparer sans corriger silencieusement
son histoire. »

Il promet donc une chose précise : que l'application puisse afficher, pour
chaque paragraphe, **le numéro que ce paragraphe porte sur l'acte déposé au
greffe**.

### 1.2 D'où viendraient réellement ces numéros

Un seul endroit du logiciel contient aujourd'hui des numéros d'origine : le
champ `LibraryNode.item`. Le cahier le dit lui-même (point 8) : la commande de
reprise doit « recopier les numéros reconnus des paragraphes depuis `item` ».

Ces valeurs ont été écrites par une seule commande, `import_demande_depot`, qui
déclare à sa ligne 47 la source qu'elle lit :

```python
SOURCE = Path(settings.BASE_DIR) / "legal" / "demande_DEPOT_2026-07-21.md"
```

C'est un **fichier Markdown de travail**. Il est identique, empreinte SHA-256 à
l'appui (`0f141193…`), au candidat gelé
`legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.md`. Il
contient **198 paragraphes numérotés**, dont **19 à suffixe littéral**
(`8-A`, `9-B`, `103-C`…).

Les numéros de ce fichier sont **écrits à la main dans le texte source**. Ce ne
sont pas les numéros de l'acte imprimé : ce sont les numéros de la version de
travail à partir de laquelle l'acte a été mis en page, puis imprimé, puis
déposé.

### 1.3 Pourquoi ce n'est pas la même numérotation

`legal/amendements/01_avant_notification/verification_ancrages_paragraphes_acte_depose.md`
(7 octobre 2026) a comparé ce `.md` à la sortie mise en page. Le mécanisme est
mécanique et connu : à la conversion, Word repart du **premier** numéro de
chaque bloc de liste puis incrémente de 1. Un numéro sauté **à l'intérieur**
d'un bloc décale donc tout le reste du bloc.

| | Nombre |
|---|---|
| Paragraphes numérotés dans le `.md` | 198 |
| À suffixe littéral, conservés tels quels | 19 |
| **Paragraphes comparés** | **179** |
| Numéro **identique** à l'impression | 132 |
| **Numéro différent à l'impression** | **47** |

Exemple donné par la vérification : les ¶ 41 et ¶ 42 **n'existent pas** dans le
`.md`, mais existent à l'impression, où ils portent le texte que le `.md`
numérote 43 et 44.

[`communication_pieces.md`](communication_pieces.md) § 10.2 c en tire la règle,
et compte **trois** numérotations :

| | Numérotation |
|---|---|
| 1 | celle du `.md` de travail — **c'est elle qui est dans `item`** |
| 2 | celle de l'acte **imprimé et déposé** — différente pour 47 paragraphes |
| 3 | celle de l'acte amendé, à venir |

> 🔴 « La concordance doit ancrer sur la numérotation 2, pas sur la 1. Une table
> bâtie sur le `.md` serait fausse pour 47 paragraphes — et c'est la table qui
> servira à démontrer que le fond n'a pas changé. »

### 1.4 Le défaut, en une phrase

Le cahier promet « les numéros que l'acte porte » (numérotation 2) et fait
recopier `item` (numérotation 1), qui en diffère pour 47 paragraphes sur 179.
Ce qui serait livré sous le nom de « numérotation du dépôt » serait **la
numérotation du brouillon**, fausse pour un paragraphe comparé sur quatre.

### 1.5 Pourquoi la précaution que le cahier a prise ne suffit pas

Le cahier n'ignore pas la question. Son point 9 dit, correctement : « Une
référence aux sources Markdown archivées ne prouve pas à elle seule l'identité
du papier remis au greffe : préciser le référent effectivement contrôlé. » Puis
il ajoute : « **Une incertitude sur le papier ne bloque pas les tests logiciels
sur une source clairement identifiée.** »

Cette seconde phrase est vraie — mais elle ne répond qu'à **une moitié** du lot
A. Il faut distinguer deux travaux que le cahier confond :

| Travail | L'incertitude bloque-t-elle ? |
|---|---|
| Faire passer T01–T29 sur des **fixtures** inventées (une source qui porte 1, 2, 4, 4-A, 9) | **Non.** Une fixture est son propre référent ; rien à vérifier |
| Exécuter la **reprise sur le document 9** — les 371 nœuds de la demande réelle | **Oui.** C'est là que la numérotation 1 serait figée sous le nom de « numéro d'origine » |

Le cahier applique la réponse du premier cas au second. Or c'est le second qui
a une valeur de dossier : les tests sur fixtures ne produisent aucune donnée
utilisable à la Cour.

Et § 10.2 c pose l'établissement de l'ancrage comme un **préalable**, pas comme
un détail à régler ensuite : « une table bâtie sur le mauvais référent est à
refaire **en entier** ».

> ## ✅ Mise à jour du 13 octobre 2026 — l'ancrage est fixé
>
> L'acte déposé est identifié : la **version simple de 44 pages, endos inclus**
> (`demande_DEPOT_2026-07-21.docx` ou son PDF), numérotée **1 … 241**, confirmée
> sur le papier par le demandeur. Voir
> [`../amendements/01_avant_notification/identification_du_fichier_imprime.md`](../amendements/01_avant_notification/identification_du_fichier_imprime.md).
>
> **Le préalable est levé ; le défaut décrit ici ne l'est pas — il est
> désormais entièrement quantifié.** La numérotation imprimée est établie et
> calculable ; `LibraryNode.item` porte toujours celle du `.md`, et les deux
> diffèrent pour **47 paragraphes sur 179**. Le cahier ferait recopier `item`
> sous le nom de « numéro d'origine ».
>
> Ce que cela change au correctif du § 1.6 : la reprise sur le document 9 n'est
> plus **bloquée**, elle est **réorientée**. Elle doit lire la numérotation
> imprimée — reconstituée mécaniquement depuis le `.docx`, ou lue dans le PDF —
> et non `item`.

### 1.6 Correctif

Scinder le lot A en deux.

1. **Les 16 critères et les 29 scénarios sur fixtures** peuvent se faire
   immédiatement : ils ne dépendent d'aucun ancrage.
2. **La reprise sur le document 9** s'exécute seulement **après** avoir
   déterminé quel candidat a été imprimé, et elle doit lire **la numérotation 2**
   — pas `item`. Tant que l'ancrage n'est pas fixé, `paragraph_number` ne doit
   pas être peuplé sur le document 9, ou doit l'être sous un nom qui dit ce
   qu'il contient réellement (le numéro du `.md` de travail, pas celui du
   dépôt).

## 2. La double désignation disparaît, et c'est voulu

*Section récrite le 13 octobre 2026. La version précédente réclamait le maintien
d'un libellé double. C'était une erreur : elle prenait un contournement pour une
règle.*

### 2.1 Le dessin retenu

> **Décision du demandeur, 13 octobre 2026.** « Le numéro de paragraphe sera
> consigné au niveau de l'arbre dans le modèle `LibraryNode`, et son utilisation
> plutôt que la numérotation automatique sera spécifiée au niveau du
> `Document`. Seule la demande a un problème de numérotation. C'est la
> numérotation de la demande **imprimée** qui sera consignée, et elle servira à
> faire la correspondance avec le nouveau numéro de la nouvelle demande, le cas
> échéant. »

Trois points, et ils suffisent :

| Où | Quoi |
|---|---|
| `LibraryNode` | le **numéro imprimé** du paragraphe — une occurrence dans un document |
| `Document` | si ce document lit son numéro consigné ou le calcule |
| Un seul document concerné | la demande déposée. Tout le reste calcule |

Le numéro ne va **pas** sur `Statement` : un même `Statement` peut se retrouver
dans la demande déposée et dans la demande modifiée, avec un numéro différent
dans chacune. Le numéro appartient à l'**occurrence**, pas au contenu.

### 2.2 Pourquoi le libellé double existait

L'en-tête de `document_manager/numerotation.py` pose la règle :

> « On désigne un paragraphe par **`§ 44 (dépôt 28)`**, jamais par l'un des deux
> seul. »

Cette règle répondait à un manque : **le vrai numéro du dépôt n'était consigné
nulle part.** `LibraryNode.item` contenait le numéro du `.md` de travail, et le
schéma en recalculait un autre. Aucun des deux n'était celui du papier. Faute de
pouvoir afficher le bon, on affichait les deux, pour que la méprise soit au moins
visible.

### 2.3 Dès que le bon numéro est consigné, la raison tombe

Le numéro imprimé consigné sur le nœud, la demande déposée affiche **son** numéro
— celui que la Cour lit. La demande modifiée affiche **le sien**, calculé depuis
sa propre structure. Chacune dit vrai, seule.

Le pont entre les deux n'est pas un libellé composé : **c'est la table de
correspondance.** C'est elle qui porte « § déposé → § modifié », et elle le fait
mieux qu'une parenthèse, puisqu'elle survit aux déplacements et aux
reformulations.

➜ Sur ce point, **le cahier E01 a raison et ma critique était infondée.** Son
point 1 (le mode appartient au `Document`), son point 2 (le numéro appartient au
`LibraryNode`, pas au `Statement`) et son point 7 (les index de concordance
identifient par `LibraryNode.pk`) décrivent exactement le dessin retenu.

### 2.4 Ce qui reste vrai, et qui est une consigne de transition

Un seul point survit, et il ne concerne que la période d'ici à la reprise :

**Tant que le numéro imprimé n'est pas consigné, tout libellé qui annonce
« dépôt » est faux.** `index_numeros()` écrit aujourd'hui :

```python
libelle = f"{numero} (dépôt {item})"
```

`item` porte le numéro du `.md`, qui diffère de l'imprimé pour **47 paragraphes
sur 179**. Ces libellés n'apparaissent que dans deux commandes de vérification
(`verifier_appuis_depot`, `persister_appuis_depot`) ; les vues et la vue publique
n'affichent que le numéro calculé.

**Deux suites possibles, au choix :**

- écrire `(md {item})` d'ici à la reprise, puis supprimer la parenthèse une fois
  le numéro imprimé consigné ;
- ne rien faire et supprimer la parenthèse à la reprise, en considérant que deux
  commandes de vérification internes ne justifient pas un passage.

La seconde est défendable. Ce qui ne l'est pas, c'est de **conserver** le libellé
« dépôt » après la reprise : il n'aurait alors plus d'objet, et resterait faux.

### 2.5 Conséquence pour la suite du présent document

Les sections qui suivent conservent leur objet. Mais la critique tirée de
« AUTO/STORED est un choix exclusif » est retirée : le choix exclusif est le
dessin voulu. Reste le § 1 — **la source du numéro consigné doit être la table
`concordance_md_imprime.json`, jamais `item`** — et le § 3, le sort des appuis
lorsqu'un paragraphe réécrit reçoit un nouveau `Statement`.

## 3. 🔴 Le pont manquant : concordance sur les nœuds, poids probatoire sur les statements

Le cahier modélise les correspondances **entre occurrences** (`LibraryNode`,
points 7 et 10) — c'est le bon niveau. Mais tout ce qui porte la valeur du
dossier est accroché au **`Statement`** :

| Porteur | Volume |
|---|---|
| `AppuiDepotJuillet` — `statement → entrée / cote_citee` | **515 lignes** |
| Énoncés contestés | 39 |
| `Fait`, `Axe`, `is_true`, `is_falsifiable` | sur le statement |

Le point 12 exige — à juste titre, c'est la règle du § 4 de
`suivi_paragraphes_en_base.md` — qu'un paragraphe réécrit utilise un **nouveau
Statement**. Mais **un nouveau statement part nu**, et aucun des seize critères
ne dit ce que deviennent ses appuis.

`suivi_paragraphes_en_base.md` § 6 pose exactement cette question (décision n° 2)
et affirme qu'elle **conditionne la migration**. Le cahier ne la mentionne pas.

➜ **Conséquence concrète : à la fin d'E01, le document 10 réécrit aurait une
table de concordance de paragraphes et zéro appui.** La table à quatre colonnes
du § 10.2 (`§ dépôt | § amendé | ancienne cote | nouvelle cote`) reste
inatteignable — non parce que les cotes sont hors périmètre, mais parce que la
dérivation a coupé le chaînon `statement → appui`.

## 4. Le hors-périmètre des cotes coupe la moitié bon marché

Exclure la concordance des cotes et l'écrire (C16) est, en soi, de l'hygiène
correcte. Mais :

- [`echeancier.md`](echeancier.md), 7 octobre : « Le demandeur réécrit sa
  demande avant de communiquer — paragraphes **et cotes** renumérotés ».
- § 10.2 a : la table `P-ancien | P-nouveau | source (model:pk)` est
  « générable mécaniquement depuis le lock ». `cotes.lock.json` est vérifié :
  **106 cotes**, chacune résolue en `model:pk`.

C'est la moitié **courte et mécanique** du livrable, et c'est elle qui est
coupée ; la moitié chère est gardée. **Prochaine échéance : protocole,
1er novembre.** Si un seul livrable doit exister d'ici là, c'est la table des
cotes à trois colonnes, pas l'infrastructure AUTO/STORED.

## 5. Le coût réel de l'appareil de test n'est pas nommé

| Constat vérifié | |
|---|---|
| Tests touchant la base dans le dépôt | **aucun** |
| Fichiers de tests réels | 4, tous `SimpleTestCase`, ~450 lignes au total |
| `tests.py` vides (3 lignes) | 11 |
| Backend | PostgreSQL + pgvector — 23 `VectorField`, migration `enable_pgvector_extension` |
| `coverage` | **non installé** (simple commentaire dans `requirements-dev.txt`) |

T01–T29 sont presque tous des tests avec base, et T12 demande un test de
migration avec données. Ce n'est pas un ajout à un appareil existant : c'est la
**construction** de l'appareil. Le cahier le présente comme un accompagnement
(« Les tests accompagnent chaque lot »), alors que c'est le poste le plus lourd
des trois lots.

## 6. Deux doublons durables, sans plan de sortie

`LibraryNode.item` porte déjà trois sens : titre court du nœud, numéro du dépôt
sur les actes importés, **incipit** du paragraphe sur les actes reproduits (le
commentaire de `index_numeros` le dit). Le cahier y ajoute `paragraph_number`,
qui duplique le deuxième sens, et **interdit de vider `item`** (point 8).

La détection de conflit n'existe qu'**au moment de la reprise** (T13, T15). Rien
ne garde contre la dérive ultérieure des deux champs, et aucun plan de retrait
n'est prévu. Le dépôt vit avec le doublon indéfiniment.

## 7. Le garde-fou que le cahier laisse tomber

`suivi_paragraphes_en_base.md` § 4 et § 6 (décision n° 3) proposent un
`verifier_integrite_depot` : comparer les empreintes des **287 statements du
document 9** à un instantané gelé, sur le modèle de `SHA256SUMS` dans
`legal/depots/`.

Le cahier fait écrire une commande de reprise qui **écrit sur les nœuds du
document 9** et se contente d'un avant/après dans un test (T27, C08). *Un test
sur fixture ne protège pas la base réelle.* S'il faut écrire une seule chose
avant la reprise, c'est l'empreinte.

---

## 8. Ce que le cahier fait bien — à garder tel quel

- **Point 11 — le verrou de prescription, correctement traduit.** « L'absence
  d'un lien signifie *à établir*, pas automatiquement *ajout*, *retrait* ou
  *fait nouveau* » ; une suggestion par similarité ne doit jamais être réputée
  confirmée. C'est exactement le balayage *amendé → déposé* du § 10.2 b, rendu
  en logiciel. T22 et T23 le testent par le bon côté.
- **Point 10 — relation plusieurs-à-plusieurs rattachée au couple de
  documents**, capable de porter une **fusion**. C'est une **correction** du FK
  réflexif `Statement.derive_de` proposé par `suivi_paragraphes_en_base.md` § 2,
  qui ne portait pas la fusion et laissait la question ouverte (§ 6, décision
  n° 1). **À reporter dans la note.** Les liens sur les **nœuds** et non sur les
  numéros affichés : également juste.
- **Point 9** — ne pas coder en dur l'id 9 ; faire vérifier la provenance.
- **Point 14** — pas de remplacement global des nombres dans `Statement.text` :
  un renvoi à la requête adverse, une date, une somme, `P-19` ne sont pas des
  numéros de paragraphe.
- **Point 5** — numéros calculés sur le périmètre complet **avant** tout
  filtrage d'affichage (T10).
- **Point 12 + T18** — nouveau Statement pour la cible, texte source et appuis
  inchangés : la règle du § 4 de la note, bien posée.
- **Gabarit § 4.2** — « le code existe », « le test a été écrit », « un autre
  test similaire passe » ne valent pas VALIDÉ ; NON EXÉCUTÉ et BLOQUÉ
  obligatoires ; pour un test négatif, PASS = le refus a été vérifié. C'est la
  bonne discipline, et elle est rare.

## 9. Ordre proposé à sa place, avant le 1er novembre

1. ~~Fixer l'ancrage~~ — **✅ fait le 13 octobre 2026.** L'acte déposé est la
   version simple de 44 pages, et la table
   [`../amendements/01_avant_notification/concordance_md_imprime.md`](../amendements/01_avant_notification/concordance_md_imprime.md)
   donne les 198 numéros imprimés. C'est la **source** du numéro à consigner.
2. **Geler l'empreinte** des 287 statements du document 9 (§ 7 ci-dessus).
3. **Table des cotes à trois colonnes** depuis `cotes.lock.json` — mécanique,
   courte, et c'est le livrable qui accompagne la demande amendée.
4. **Le lien de concordance au niveau des nœuds** — le point 10 du cahier, qui
   est bon — *et* la décision sur le sort des appuis à la dérivation (§ 3).
5. **AUTO/STORED et l'inventaire des consommateurs.** Le mode sur le
   `Document`, le numéro imprimé sur le `LibraryNode`, STORED pour la seule
   demande déposée (§ 2). Vérifier au passage que chaque sortie lit bien le
   résolveur, et supprimer le libellé « (dépôt …) » devenu sans objet.

Les points 1 à 3 ne dépendent d'aucune décision de conception. Le point 4 dépend
de la décision n° 2 de `suivi_paragraphes_en_base.md` § 6, toujours ouverte.
