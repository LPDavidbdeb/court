# Epic E01 — résultat

Synthèse des trois temps du 14 octobre 2026 : développement (03 h 40 – 04 h 30),
mise en service sur la base de travail (08 h 27 – 08 h 40), clôture de la
validation (09 h 50 – 10 h 25). Le détail complet, avec la matrice des
18 critères, les 29 scénarios et leurs preuves, est dans
[`rapport_execution_epic_E01.md`](rapport_execution_epic_E01.md) ; la mise en
service dans [`mise_en_service_E01.md`](mise_en_service_E01.md).

    Branche        : epic/E01-numerotation-concordance  (non fusionnée)
    Commit départ  : dae8da2
    Commits livrés : 4e4a4d6, 6f60890, 3ed507a, 3df17eb, c11c171
    État global    : VALIDÉE — 18 critères sur 18

**Ce verdict porte sur l'outillage**, non sur la concordance éditoriale réelle.
Celle-ci reste en cours : après l'étape 1 du lot 01, les correspondances et
appuis encore ouverts restent à établir; l'export strict les nomme.

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
| US05 — anciennes et nouvelles cotes | **VALIDÉE** |
| US06 — concordance reproductible et contrôlable | **VALIDÉE** |

---

## Les contrôles obligatoires ont réussi

Sur une **copie fidèle de la base du dossier** (`createdb -T`) pendant le
développement, puis **rejoués sur la base de travail** à la mise en service, avec
les mêmes résultats.

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

### 1. Quatre divergences du lock — tranchées le 14 octobre

Pour **P-1, P-8, P-15 et P-101**, `cotes.lock.json` nomme une `Photo` et le
registre nomme le `PhotoDocument` qui la contient. C'est la même matière
désignée à deux niveaux : l'image, et la pièce d'un seul feuillet qui la
présente.

Elles n'avaient **pas** été comptées comme concordantes. Les tenir d'emblée
pour égales aurait été trancher, dans un rapport, une question d'identité
documentaire — la correction silencieuse que le cahier interdit.

**Le demandeur a tranché** : une Photo appartient au plus à un PhotoDocument,
donc l'équivalence de contenant est retenue pour ces quatre couples. Les deux
identifiants et leurs types distincts sont conservés.

Les **deux sens** du rattachement ont été vérifiés avant la qualification :

| Cote | Au lock | Au registre | Photo → PhotoDocuments | PhotoDocument → Photos |
|---|---|---|---|---|
| P-1 | `Photo:4558` | `photodocument:14` | **[14]** | **[4558]** |
| P-8 | `Photo:4526` | `photodocument:3` | **[3]** | **[4526]** |
| P-15 | `Photo:4551` | `photodocument:9` | **[9]** | **[4551]** |
| P-101 | `Photo:4554` | `photodocument:12` | **[12]** | **[4554]** |

Descriptions identiques de part et d'autre, une seule ligne de registre par
cote, aucun autre couple divergent. **La règle est métier, pas structurelle** :
le champ est un `ManyToManyField`, le schéma n'impose aucune cardinalité. Elle
est donc vérifiée sur l'état examiné — où aucune des 1 733 photos n'appartient à
plus d'un PhotoDocument — et non garantie. Une migration de cardinalité ne fait
pas partie de cette clôture.

    python manage.py table_des_cotes --accepter-equivalences-contenant

**102/106 → 106/106.** La réconciliation est **CONFORME**, la table se qualifie
**fidèle au dépôt**, et les quatre équivalences restent visibles au manifeste
sous leur verdict propre, chacune avec ses deux preuves. Le diagnostic antérieur
est conservé à part et dit toujours 102/106, NON CONFORME.

Rien n'a été corrigé : le lock garde son empreinte, les associations du registre
et la composition des documents sont inchangées, l'archive gelée est vérifiée
par `shasum -c SHA256SUMS`. **C13 et C15 sont validés.**

### 2. Trois vues ignoraient le mode de numérotation

`schema_detail_view`, `document_public_view` et `argument_manager` appelaient
`numeroter()`, qui calcule **toujours**. Sur l'acte passé en STORED, elles
affichaient donc le numéro recalculé là où le papier en porte un autre.

Corrigées. `numeroter()` n'est plus appelée que par le résolveur commun, et les
douze sorties actives ont été vérifiées sur les données réelles
(`preuves_E01/T17_sorties.log`).

### 3. La base de travail est migrée et en service

**Cette mention est corrigée.** Au terme du développement, rien n'avait été
écrit dans `court_project_pg` — c'est ce que le cahier exigeait, et cela laissait
la base en retard d'une migration sur le code. **Ce n'est plus le cas depuis la
mise en service du 14 octobre, 08 h 27 – 08 h 40.**

| Étape | Résultat |
|---|---|
| Sauvegarde datée, hors du dépôt | 14 Mo, `pg_restore --list` lisible |
| `manage.py migrate` | `document_manager 0016`, `case_manager 0015` — **111 appliquées, 0 en attente** |
| `designer_referent --document 9` | référent désigné, 371 nœuds, 515 appuis, empreinte `02d9c468…` |
| `reprendre_numeros_imprimes --appliquer --passer-en-stored` | **198 numéros écrits**, 198/198 conformes, 0 écart |
| Seconde application | **0 écriture** |
| Démarrage de l'application | 4 routes sollicitées, aucune erreur |
| Gardes du référent | 5 tentatives d'écriture interdites, **5 refus** |

L'empreinte du référent relevée sur la base de travail est **identique** à celle
de la copie de contrôle : les deux bases décrivaient le même acte, au même
ordre. Le détail est dans `mise_en_service_E01.md`.

Bases créées pendant les travaux, supprimables : `court_e01_copie` et
`court_e01_demo`.

---

## Ce qui reste — et qui n'est pas du développement

Le moteur est livré et testé. Le travail éditorial, lui, **a commencé** :
l'étape 1 du **lot éditorial 01** a été appliquée en parallèle par une tâche
distincte (`run_id 20261014_a25cfb3d`, 10 h 26 – 10 h 33), non par celle-ci.
Relevé du 14 octobre à 10 h 36 :

| | Au 04 h 30 | Au 10 h 36 |
|---|---|---|
| Lignes de concordance | 200 | **199** |
| Correspondances 9 → 10 | 0 | **1** |
| Occurrences source sans décision | 198 | **197** |
| Ancrages de citation | 0 | **2**, dont 1 littéral |
| Confirmations d'appui | 0 | **1** |
| EX02 / EX04 / EX05 | bloquées | **EX04 satisfaite** ; EX02 (198) et EX05 (1) bloquées |

Ces nombres sont un **relevé**, pas un invariant : ils changent à mesure que la
version 2 s'écrit, et **ni C13 ni C15 n'en dépendent**. Le référent, lui, n'a
pas bougé : 371 nœuds, 198 numéros, 515 appuis, **0 écart**.

**EX04 exigeait les deux tâches.** Le lot 01 a levé la cote sans ancrage ; la
clôture a levé la réconciliation du lock. Le diagnostic du lot 01, produit sans
l'option d'acceptation, portait encore ce second motif.

L'export strict refuse ce qui manque en le nommant : c'est son office. Cette
charge n'est pas chiffrée, parce qu'elle dépend de la forme de la section
« Exposé des faits », que `AGENTS.md` dit non arrêtée. Les volumes connus :
198 occurrences source au total, dont **197 sans décision** à ce relevé;
70 énoncés contestés sur 7 documents,
515 appuis de juillet consultables.

**Le 18/18 ne couvre pas ce travail.** Il porte sur l'outillage et sur la
fidélité historique des cotes. **Aucune décision du lot éditorial n'a été
enregistrée par cette tâche**, ni au développement, ni à la mise en service, ni
à la clôture.

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

Et pour la clôture du 14 octobre :

| Fichier | Contenu |
|---|---|
| `preuve_equivalences_contenant.json` / `.log` | **dossier réel** — les quatre couples, les deux sens du rattachement, 32 assertions |
| `table_cotes_diagnostique_avant_qualification.json` / `.csv` / `.log` | **le diagnostic conservé** — 102/106, NON CONFORME |
| `table_cotes_qualifiee.json` / `.csv` / `.log` | après décision — 106/106, CONFORME AU LOCK |
| `concordance_apres_qualification.json` / `.csv` / `.log` | même état de cotation ; EX04 réduite à son motif éditorial |
| `revalidation_C13_C15.json` / `.log` | C13, C15, T24–T26 et T28 sur les données réelles — 0 échec |
| `integrite_apres_cloture.log` | archive gelée, lock et référent, après la clôture |
| `tests_apres_cloture.log` | 133 tests, OK |

Plus `rapport_execution_epic_E01.json` à la racine, pour refaire la vérification.

**Ces fichiers ne sont pas versionnés, et c'est voulu.** `.gitignore` exclut
`*.json` et `*.log`, ce dépôt est public, et le manifeste porte le texte et les
identifiants de l'acte déposé — comme `cotes.lock.json` lui-même, que l'Epic
notait déjà comme non publié pour la même raison. Chacun se régénère par la
commande qui l'a produit.
