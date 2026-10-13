# Évaluation de la révision — Cahier « Epic E01 », version du 13 octobre 2026

**Objet :** le cahier a été récrit dans le même fichier après la première revue.
Ce document dit, constat par constat, ce qui a été pris en compte, ce qui reste
et ce que la révision introduit de nouveau.

**Verdict : la révision répond à l'ensemble des constats.** Quatre sont réglés,
un est correctement posé comme décision à prendre, et la révision **corrige une
erreur de la première revue**. Deux réserves subsistent, toutes deux portant sur
le périmètre et non sur la justesse.

---

## 1. Contrôles de conformité

| Vérification | Résultat |
|---|---|
| Commit de révision cité `32679609e7…` | ✅ existe, correspond à l'état du dépôt |
| T03 cite « Markdown 43 → imprimé 41 » | ✅ exact |
| T03 cite « 72 → 67 » | ✅ exact |
| T03 cite « 142 → 139 » | ✅ exact |
| « 198 paragraphes, 179 simples dont 47 diffèrent, 19 suffixés » | ✅ conforme à la table publiée |

Les trois exemples de T03 ont été repris de la table de concordance sans erreur,
y compris le moins évident des trois.

---

## 2. Suivi des constats de la première revue

| | Constat initial | Traitement dans la révision |
|---|---|---|
| **1** | La reprise lit `item`, qui ne porte pas les numéros du dépôt | ✅ **Réglé** — § 2.1 |
| **2** | `Fait.statement`, FK unique entre deux versions | 🟡 **Posé comme décision** — § 2.2 |
| **3** | Le coût de l'appareil de test n'est pas nommé | ✅ **Réglé, et corrige la revue** — § 2.3 |
| **4** | Doublon `item` / `paragraph_number` | ✅ **Réglé autrement, et mieux** — § 2.4 |
| **5** | Garde-fou d'empreinte abandonné | ✅ **Réglé, promu en story** — § 2.5 |
| **—** | Critique retirée : la double désignation | ✅ Le dessin retenu est repris tel quel |

### 2.1 Constat 1 — réglé

L'objectif utilisateur énonce désormais le fait lui-même :

> « `LibraryNode.item` contient la numérotation du Markdown et **ne constitue
> pas la source du numéro imprimé**. »

Et le contrat suit : le point 8 fait « lire les numéros imprimés de la
concordance établie », US01 et US02 parlent des « numéros qu'elle porte sur le
papier » plutôt que des « numéros d'origine », et T15 ferme la porte qui
restait ouverte : « L'absence de cette association ne permet pas d'appeler
numéro imprimé le libellé du Markdown. »

Les quatre modifications demandées au § 6.3 de la première revue sont faites.

### 2.2 Constat 2 — correctement posé comme décision

Le point 12 et C12 exigent que « le traitement des liens Fait/Axe et des
appréciations `is_true` / `is_falsifiable` soit explicite », et que pour un
texte modifié ces appréciations soient « réexaminées plutôt que réputées
validées par une copie ou une valeur par défaut ». T23 le contrôle.

La section « Politique d'appuis proposée à évaluer » va plus loin et **nomme la
question sans la trancher** : « L'évaluation doit préciser comment les appuis
courants, leurs rôles et leur état de réexamen s'articulent avec `Fait` et
`AppuiFait`. »

C'est le bon traitement pour un document de proposition : la décision appartient
au demandeur, et elle est désormais visible plutôt qu'absente.

**Ce qui n'est pas encore dit**, et qui aiderait à trancher : `Fait.statement`
est un **ForeignKey unique**. Dès que deux versions de la demande coexistent, il
ne peut en désigner qu'une. Le choix n'est donc pas « copier ou réexaminer »
mais, structurellement, l'un de ces trois :

1. le `Fait` suit la cible — on perd la trace de l'endroit où le fait était
   plaidé dans l'acte déposé, sauf à la relire par la concordance ;
2. le `Fait` reste sur la source — il faut remonter le lien de concordance pour
   savoir où le fait est plaidé aujourd'hui ;
3. le champ devient multiple — un `Fait` peut désigner un paragraphe dans
   chaque version, ce qui est le seul moyen de dire les deux à la fois.

La première revue décrivait ce défaut comme une rupture silencieuse par
`SET_NULL`. C'était excessif, et le compte rendu a été rectifié : rien ne
supprime les `Statement` de l'acte déposé.

### 2.3 Constat 3 — réglé, et la révision corrige la revue

Le diagnostic du cahier relève :

> « `email_manager/tests.py` contient déjà un `TestCase` utilisant la base;
> distinguer l'existence de ce test de la disponibilité effective d'un
> environnement de tests compatible. »

**C'est exact, et la première revue avait écrit « aucun test touchant la
base ».** Vérifié : `email_manager/tests.py:13` est bien un
`django.test.TestCase`. Le compte rendu a été rectifié. Le constat survit sous
sa forme exacte — un test avec base, une méthode, le DAO Gmail simulé — mais
l'énoncé initial était faux, et la distinction que le cahier ajoute est la
bonne.

La demande de dimensionnement est par ailleurs satisfaite : les scénarios « sont
à dimensionner lors de l'évaluation » et « ne constituent pas vingt-neuf tests
isolés à écrire mécaniquement », avec séparation explicite entre moteur sur
fixtures, migrations sur base compatible et contrôles des sources réelles.

### 2.4 Constat 4 — réglé autrement, et mieux

La première revue demandait un invariant ou un calendrier de retrait pour le
doublon `item` / `paragraph_number`. La révision prend un autre chemin, et il
est meilleur : elle déclare la divergence **légitime**.

> Point 8 : « Ne pas recopier `item`, ni forcer `item` et `paragraph_number` à
> égaler : **leur divergence peut être correcte**. »
> T13 : « `item` peut rester 43 alors que `paragraph_number` devient 41. Cette
> divergence légitime n'est pas signalée comme conflit. »

Les deux champs ne disent pas la même chose — l'un le Markdown, l'autre le
papier — et l'écart est précisément l'information que porte la table des
47 écarts. Il n'y a donc pas de dérive à surveiller. Le retrait d'`item` est
rattaché à « l'adaptation de ses consommateurs », ce qui suffit.

### 2.5 Constat 5 — réglé, et promu

L'instantané préalable, que la première revue réclamait comme garde-fou, devient
**US01 tout entière** : point 9 (« avant toute écriture, créer un instantané
durable des textes et de leurs associations aux nœuds et appuis »), C02, et T02
qui compare l'état avant/après. C'est plus que ce qui était demandé.

---

## 3. Ce que la révision introduit

### 3.1 Les cotes entrent dans le périmètre

La première revue observait que la moitié mécanique du livrable — la table
`ancienne cote | nouvelle cote | source` — avait été coupée alors qu'elle est
courte. US05, C13 à C15 et T24 à T26 la réintègrent, et l'ordre proposé la place
**en deuxième position, avant la concordance complète** et sans attendre la fin
de la réécriture. C'est le bon ordre.

⚠️ **Mais US05 est à moitié bloquée par une décision qui n'appartient pas au
logiciel.** C13 le dit : « la règle d'attribution des nouvelles cotes doit être
précisée avant sa validation ». La moitié historique est prête — le registre du
dépôt fige 106 cotes résolues en `model:pk` — mais la cotation cible n'existera
qu'une fois la réécriture avancée. US05 livrera donc sa colonne gauche
immédiatement et restera incomplète jusque-là. Le cahier l'admet ; il vaut
mieux que ce soit dit à l'avance plutôt que constaté dans le rapport final.

### 3.2 Une jointure nouvelle, jamais vérifiée

C01 exige que « chaque ligne de la table des 198 paragraphes soit rattachable
sans ambiguïté à son occurrence en base ». C'est la bonne exigence, et elle
introduit une **troisième** jointure, après `.md` ↔ imprimé déjà établie :

```
table (198 lignes)  →  LibraryNode du document déposé
```

Elle n'a jamais été exécutée. Les indices sont bons : l'importateur écrit le
numéro du Markdown dans `item` pour les seuls paragraphes, et sa sortie annonce
le même compte de 198. La jointure devrait donc se faire par `item`, à
l'identique. Mais tant qu'elle n'est pas passée, US01 repose sur une hypothèse.

➜ **C'est le premier contrôle à exécuter**, avant tout code : il est court, et
s'il révèle une ambiguïté, il déplace US01 avant tout le reste.

### 3.3 Un résidu mineur

Le diagnostic conserve la remarque sur `index_numeros` et `isdigit()`, mais le
cahier ne dit nulle part ce que devient le libellé `f"{numero} (dépôt {item})"`.
Une fois le numéro imprimé consigné, ce libellé annonce « dépôt » en affichant le
Markdown : il doit **disparaître**, non être corrigé. Il n'apparaît que dans deux
commandes de vérification internes, d'où le classement en mineur.

---

## 4. Appréciation d'ensemble

Ce que la révision réussit, et qui n'allait pas de soi : elle **n'empile pas**.
Les critères sont renumérotés C01–C18 avec l'avertissement explicite que « les
identifiants du premier cahier ne constituent pas une équivalence de contenu »,
les stories sont réordonnées autour du référent plutôt qu'autour des champs, et
la section « Politique d'appuis » isole ce qui doit être décidé de ce qui doit
être construit.

Elle corrige aussi une erreur de la revue, ce qui est le signe d'une lecture et
non d'une acceptation.

**Les deux réserves — US05 à moitié dépendante d'une décision de cotation, et la
jointure de C01 jamais exécutée — ne sont pas des objections au cahier.** La
première est signalée par le cahier lui-même ; la seconde est un contrôle de
quelques minutes à passer avant d'ouvrir une branche.
