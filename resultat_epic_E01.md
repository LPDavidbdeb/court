# Epic E01 — résultat

Synthèse de l'exécution du 14 octobre 2026. Le détail complet, avec la matrice
des 18 critères, les 29 scénarios et leurs preuves, est dans
[`rapport_execution_epic_E01.md`](rapport_execution_epic_E01.md).

    Branche        : epic/E01-numerotation-concordance  (non fusionnée)
    Commit départ  : dae8da2
    Commits livrés : 4e4a4d6, 6f60890
    État global    : PARTIEL — 16 critères validés sur 18

---

## Ce qui est livré

**Chaque version de la demande affiche son propre numéro.** L'acte déposé porte
les 198 numéros de son papier, conservés nœud par nœud
(`LibraryNode.paragraph_number`, `Document.numbering_mode = STORED`) ; la
version modifiée porte ceux que sa structure calcule. La concordance porte le
lien entre les deux — c'est là qu'il appartient.

Le libellé `« 44 (dépôt 28) »` est **abrogé**. Il obligeait à citer deux numéros
ensemble pour éviter une méprise, mais le second n'était pas celui du dépôt :
`item` porte le numéro du Markdown de travail, qui diffère du papier pour 47 des
179 paragraphes à numéro simple.

| Story | Verdict |
|---|---|
| US01 — référent identifié et protégé | **VALIDÉE** |
| US02 — numéro propre à chaque version | **VALIDÉE** |
| US03 — correspondances entre paragraphes | **VALIDÉE** |
| US04 — traçabilité et confirmation des appuis | **VALIDÉE** |
| US05 — anciennes et nouvelles cotes | **PARTIELLE** |
| US06 — concordance reproductible et contrôlable | **VALIDÉE** |

---

## Les contrôles obligatoires ont réussi

Sur une **copie fidèle de la base du dossier** (`createdb -T`), jamais sur la
base de travail.

**T01 — rattachement, sans écriture**

| Assertion | Attendu | Obtenu |
|---|---|---|
| Lignes de référence | 198 | **198** |
| Lignes appariées | 198 | **198** |
| Occurrences distinctes | 198 | **198** |
| Manquante / ambiguë / doublon | 0 | **0 / 0 / 0** |
| Paragraphe admissible oublié | 0 | **0** |
| Contenu incompatible | 0 | **0** |
| Écriture en base | 0 | **0** |

Le contenu est comparé au **texte complet du Markdown archivé**, pas à l'incipit
de 120 caractères de la table — lequel ne démontrerait pas l'intégrité. Les
empreintes du Markdown et du `.docx` candidat correspondent à celles que la
table de concordance déclare.

**T03 — après reprise**

198 valeurs contrôlées une à une, **198 conformes, 0 écart**. 19 suffixes
conservés, 47 divergences d'avec le Markdown. Témoins vérifiés nommément :
43→41, 72→67, 142→139, 22-A→22-A.

Référent intact : **0 écart** de texte, d'arborescence, d'`item`, d'appuis.
Seules les 198 métadonnées de numérotation diffèrent. Seconde application :
**0 écriture**.

**Tests** — 101 méthodes pour les 29 scénarios, 127 au total dans le dépôt,
**aucune régression**. `check` et `makemigrations --check` passent.

---

## Trois choses à signaler

### 1. Quatre divergences du lock, non résolues

Pour **P-1, P-8, P-15 et P-101**, `cotes.lock.json` nomme une `Photo` et le
registre nomme le `PhotoDocument` qui la contient. Vérification faite, chacun ne
contient que cette photo : c'est la même matière désignée à deux niveaux.

Elles ne sont **pas** comptées comme concordantes pour autant. Les tenir
d'emblée pour égales reviendrait à trancher, dans un rapport, une question
d'identité documentaire — la correction silencieuse que le cahier interdit.
Elles sont rapportées sous un verdict propre, `EQUIVALENCE_CONTENANT`, avec la
preuve du contenant ; l'option `--accepter-equivalences-contenant` permet de les
retenir **par décision explicite**, et la sortie en garde la trace.

Par défaut la réconciliation est **NON CONFORME** (102 des 106 cotes
concordent) et la table des cotes **ne se dit pas fidèle au dépôt**. Rien n'a
été corrigé, ni dans le lock, ni en base.

**C13 et C15 restent partiels pour cette seule cause.** C'est une décision à
prendre, pas un correctif à écrire.

### 2. Trois vues ignoraient le mode de numérotation

`schema_detail_view`, `document_public_view` et `argument_manager` appelaient
`numeroter()`, qui calcule **toujours**. Sur l'acte passé en STORED, elles
affichaient donc le numéro recalculé là où le papier en porte un autre.

Corrigées. `numeroter()` n'est plus appelée que par le résolveur commun, et les
douze sorties actives ont été vérifiées sur les données réelles
(`preuves_E01/T17_sorties.log`).

### 3. 🔴 La base de travail n'est pas migrée

**Rien n'a été écrit dans `court_project_pg`** — vérifié après coup : la colonne
`numbering_mode` y est absente, les tables de l'Epic n'existent pas, la dernière
migration reste `0015`, et le document 9 y porte toujours ses 371 nœuds.

C'est ce que le cahier exige, et cela laisse la base en retard d'une migration
sur le code. **L'application ne démarrera pas** avant :

    manage.py migrate

La migration est neutre : les deux champs sont vides par défaut et le mode est
`AUTO`. La reprise des 198 numéros reste ensuite une opération distincte, à
lancer sciemment :

    manage.py designer_referent --document 9 \
        --libelle "Demande introductive d'instance — dépôt du 24 juillet 2026" \
        --depose-le 2026-07-24 \
        --source legal/demande_DEPOT_2026-07-21.md \
        --concordance legal/amendements/01_avant_notification/concordance_md_imprime.json

    manage.py reprendre_numeros_imprimes --document 9 \
        --concordance legal/amendements/01_avant_notification/concordance_md_imprime.json \
        --markdown legal/demande_DEPOT_2026-07-21.md \
        --appliquer --passer-en-stored

Elle refait ses contrôles avant d'écrire et refuse si quoi que ce soit a changé
depuis. Aucune option de forçage n'existe.

Bases créées pendant les travaux, supprimables : `court_e01_copie` et
`court_e01_demo`.

---

## Ce qui reste — et qui n'est pas du développement

Le moteur est livré et testé ; le travail éditorial, lui, n'a pas été fait :

- les **correspondances** entre le document 9 et le document 10 ne sont pas
  établies — 200 occurrences « à établir » ;
- les **appuis** de la version modifiée ne sont pas confirmés ;
- les **citations de pièces** ne sont pas ancrées — l'export réel signale une
  cote écrite sans ancrage (nœud 1243, « P-2 »).

L'export strict les refuse en les nommant : c'est son office. Je n'ai pas
chiffré cette charge, parce qu'elle dépend de la forme de la section « Exposé
des faits », que `AGENTS.md` dit non arrêtée. Les volumes connus : 198
occurrences source, 70 énoncés contestés sur 7 documents, 515 appuis de juillet
consultables, 4 divergences à trancher.

---

## Où sont les preuves

Dans `legal/amendements/01_avant_notification/preuves_E01/` :

| Fichier | Contenu |
|---|---|
| `manifeste_rattachement_198.json` | **dossier réel** — les 198 associations, avec empreintes |
| `T17_sorties.log` | **dossier réel** — les douze sorties vérifiées |
| `demo_concordance.json` / `.csv` | export strict accepté, après décisions |
| `demo_concordance_diagnostique.json` / `.csv` | la même, avant décisions : EX02 et EX05 bloquantes |
| `demo_table_cotes.json` | la table autonome des cotes |
| `demo_reclassement_P12_P13.json` | le cas textuel, avant / après |

Plus `rapport_execution_epic_E01.json` à la racine, pour refaire la vérification.

**Ces fichiers ne sont pas versionnés, et c'est voulu.** `.gitignore` exclut
`*.json` et `*.log`, ce dépôt est public, et le manifeste porte le texte et les
identifiants de l'acte déposé — comme `cotes.lock.json` lui-même, que l'Epic
notait déjà comme non publié pour la même raison. Chacun se régénère par la
commande qui l'a produit.
