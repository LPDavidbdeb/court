# Mise en service d'E01 sur la base de travail

Exécutée le **14 octobre 2026, 08 h 27 – 08 h 40 (UTC−4)**.

    Branche  : epic/E01-numerotation-concordance   (non fusionnée)
    Commit   : 3df17eb6c4f804eb66071be657ec79930a18902a
    Base     : court_project_pg  —  PostgreSQL 18.1, localhost:5432
    Verdict  : EN SERVICE. C13/C15 demeurent PARTIELS.

**L'outillage est utilisable pour la rédaction.** La demande déposée affiche
désormais, dans toutes les sorties, les 198 numéros de son papier. Son contenu
est protégé contre l'écriture. La concordance, les appuis et les citations
s'enregistrent dès maintenant.

Ce qui demeure partiel n'est pas un défaut technique : ce sont **quatre
divergences du lock** qui appellent votre décision (§ 7), et le **travail
éditorial** lui-même, que l'outil réclame explicitement plutôt que de le
supposer fait.

---

## 1. Sauvegarde

    pg_dump --format=custom --compress=9 --no-owner --no-privileges \
            --dbname=court_project_pg \
            --file=~/Backups/court/archives/court_project_pg_avant_E01_20261014_082737.dump

| | |
|---|---|
| Emplacement | `~/Backups/court/archives/` — hors du dépôt, non versionné |
| Taille | 14 Mo, `chmod 600` |
| Vérification | `pg_restore --list` : dump lisible |
| Restauration | `pg_restore -d court_project_pg --clean --if-exists <fichier>` |

La sauvegarde quotidienne de `scripts/backup_db.sh` **écrase toujours le même
fichier** ; j'ai donc pris un dump daté à part plutôt que de la consommer. Celle
de 01 h 03 ce matin reste intacte dans `~/Backups/court/court_project_pg.dump`.

**État des migrations avant intervention** — deux en attente :

    document_manager.0016_document_numbering_mode_librarynode_paragraph_number_and_more  [ ]
    case_manager.0015_ancragecitation_confirmationappui                                  [ ]

---

## 2. Migrations

    python manage.py migrate

Les deux migrations se sont appliquées sans erreur. **111 appliquées, 0 en
attente.** `manage.py check` : aucun problème.

**Démarrage de l'application** — serveur lancé sur `127.0.0.1:8899`, quatre
routes sollicitées :

| Route | Code |
|---|---|
| `/document/9/` (publique) | **200**, 131 ko |
| `/` | 302 — redirection d'authentification attendue |
| `/documents/list/` | 302 — idem |
| `/documents/schema/9/` | 302 — idem |

Aucune erreur au journal du serveur.

---

## 3. Le référent historique

**Provenance vérifiée avant toute désignation.**

Les deux sources archivées portent exactement les empreintes que la table de
concordance déclare :

| Source | sha256 relevé = déclaré |
|---|---|
| `legal/demande_DEPOT_2026-07-21.md` | `0f141193300fed12…` ✓ |
| `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.docx` | `6f1818262835e9c0…` ✓ |

**Le document 9 est le seul candidat possible.** Confrontation des dix
documents de la base aux 198 numéros de la table :

| Document | Items numérotés | Communs avec la table |
|---|---|---|
| 1 à 8 | 0 | 0 |
| **9** | **198** | **198 — correspondance exacte** |
| 10 | 11 | 11 |

Le document 10 réutilise onze numéros parce qu'il est la version 2 en cours de
rédaction ; il n'en porte pas 198 et n'est pas un candidat.

    python manage.py designer_referent --document 9 \
        --libelle "Demande introductive d'instance — dépôt du 24 juillet 2026, dossier 505-17-016235-261" \
        --depose-le 2026-07-24 \
        --source      legal/demande_DEPOT_2026-07-21.md \
        --concordance legal/amendements/01_avant_notification/concordance_md_imprime.json

| | |
|---|---|
| Document | 9 — `DocumentSource.PRODUCED` |
| Instantané | 371 nœuds, 515 appuis de juillet |
| Empreinte globale | `02d9c468c95b2c4294103c162b6ce4f253b7cef2ad27a5c8c57650b1d23fbf14` |

**Cette empreinte est identique à celle relevée le matin même sur la copie de
contrôle.** Les deux bases décrivaient donc bien le même acte, au même ordre —
ce qui transporte sur la base de travail la valeur probante des essais faits
sur la copie.

Le référent est **PRODUCED**. Sa protection ne pouvait donc pas se déduire de
`DocumentSource` ; elle vient de la table `ReferentHistorique`, que les gardes
consultent avant chaque écriture.

---

## 4. Reprise des numéros imprimés

### T01 — sans écriture

    python manage.py reprendre_numeros_imprimes --document 9 \
        --concordance legal/amendements/01_avant_notification/concordance_md_imprime.json \
        --markdown    legal/demande_DEPOT_2026-07-21.md \
        --manifeste   …/preuves_E01/manifeste_T01_base_de_travail.json

| Assertion | Attendu | Obtenu |
|---|---|---|
| Lignes de référence | 198 | **198** |
| Lignes appariées | 198 | **198** |
| Occurrences distinctes | 198 | **198** |
| Sans occurrence / ambiguë / doublon | 0 | **0 / 0 / 0** |
| Paragraphe admissible oublié | 0 | **0** |
| Contenu incompatible | 0 | **0** |
| Occurrence d'un autre document | 0 | **0** |

**Absence d'écriture vérifiée après coup**, et non seulement annoncée :
0 `paragraph_number` renseigné, mode resté `AUTO`, aucune dérive depuis
l'instantané.

### Application

    … --appliquer --passer-en-stored

**198 numéros écrits.** Contrôle immédiat :

| Contrôle | Attendu | Obtenu |
|---|---|---|
| Valeurs contrôlées | 198 | **198** |
| Conformes | 198 | **198** |
| Écarts | 0 | **0** |
| Suffixes conservés | 19 | **19** |
| Divergents du Markdown | 47 | **47** |

Contre-vérification faite **depuis la table publiée**, sans repasser par le
résolveur :

| `item` (Markdown) | Table | Affiché |
|---|---|---|
| 43 | 41 | **41** |
| 72 | 67 | **67** |
| 142 | 139 | **139** |
| 22-A | 22-A | **22-A** |
| 1 | 1 | **1** |
| 241 | 241 | **241** |

Numéros requis manquants : **0**.

### Intégrité historique

Comparaison à l'instantané pris avant la reprise :

| Catégorie | Écarts |
|---|---|
| Textes | **0** |
| Arborescence | **0** |
| `item` | **0** |
| Appuis de juillet | **0** |
| Nœuds disparus / apparus | **0 / 0** |
| `paragraph_number` | **198** — la métadonnée autorisée |

`AppuiDepotJuillet` : 515 avant, **515 après**. Nœuds du document 9 : 371 avant,
**371 après**.

### Idempotence

Seconde application : **0 numéro écrit**, 198/198 toujours conformes, référent
intact.

### Les gardes, éprouvées sur la base de travail

| Tentative | Résultat |
|---|---|
| Supprimer un nœud du référent | **refusée** — `SuppressionRefusee` |
| Réécrire le texte d'un paragraphe | **refusée** — `ModificationRefusee` |
| Modifier son `item` | **refusée** — `ModificationRefusee` |
| Supprimer en lot | **refusée** — `SuppressionRefusee` |
| Supprimer le document entier | **refusée** — `ProtectedError` |

Après ces cinq tentatives : 371 nœuds intacts, texte du § 41 inchangé.

La suppression du document est arrêtée par `ProtectedError` et non par ma garde,
parce que `ReferentHistorique.document` est un `OneToOneField(on_delete=PROTECT)`
dont la contrainte se déclenche en amont du signal. Le refus est obtenu, par un
mécanisme plus fort encore ; je le signale pour que le message d'erreur ne
surprenne pas.

---

## 5. Les sorties réelles

Contrôle **indépendant du balisage** : on cherche le texte du paragraphe dans
la page, puis le numéro attendu juste avant lui.

| Sortie | Code | Témoins | Justes | Libellé `(dépôt …)` |
|---|---|---|---|---|
| clean 9 | 200 | 4 | **4** | absent |
| interactive 9 | 200 | 4 | **4** | absent |
| cinematic 9 | 200 | 4 | **4** | absent |
| **schéma 9** | 200 | 4 | **4** | absent |
| **publique 9** | 200 | 4 | **4** | absent |
| éditeur PRODUCED 9 | 200 | 235 | **235** | absent |
| éditeur PRODUCED 10 | 200 | 2 | **2** | absent |
| backbone 1 | 200 | 23 | **23** | absent |
| énoncés contestés | 200 | 70 | **70** | absent |
| contestation 9 et 1 | 200 | — | — | gabarit sans numéro |

**VERDICT : CONFORME.**

### Le PDF

Le rendu PDF passe par `_numbered_nodes`, qui appelle le formateur de la vue
« clean ». Les deux ont été contrôlés :

- **formateur** : 198 paragraphes numérotés, **198 conformes à la table, 0 écart** ;
- **PDF produit** : 28 pages ; texte extrait, les numéros précèdent bien leurs
  paragraphes —

| Markdown | Imprimé | Extrait du PDF |
|---|---|---|
| 43 | 41 | `… P-16 à P-19. ` **`41.`** |
| 72 | 67 | `… appert de P-9. ` **`67.`** |
| 142 | 139 | `… pièce P-26. ` **`139.`** |
| 22-A | 22-A | `… paternelle. ` **`22-A.`** |

### Une trace nettoyée

Le script de contrôle crée un compte `e01_controle` pour ouvrir une session.
Vérifié sans mot de passe utilisable — la correction de `3df17eb` tient — puis
**supprimé** de la base de travail. Il n'en reste rien.

---

## 6. Concordance diagnostique — et comment la renseigner

    python manage.py exporter_concordance --source 9 --cible 10 \
        --json …/preuves_E01/concordance_base_de_travail.json \
        --csv  …/preuves_E01/concordance_base_de_travail.csv

| Périmètre | |
|---|---|
| Source | document 9, 198 paragraphes, `STORED` |
| Cible | document 10, **2 paragraphes**, `AUTO` — la version 2 est à son début |
| État de cotation | `dda2ee0d2270bf16…`, 334 entrées |
| Lignes produites | 200 |

### Verdicts

| | Condition | État |
|---|---|---|
| **EX01** | périmètre et référent | **satisfaite** |
| EX02 | correspondances et traitements confirmés | **bloquée** — 200 motifs |
| **EX03** | numéros requis résolus | **satisfaite** |
| EX04 | citations et cotes résolues | **bloquée** — 2 motifs |
| EX05 | appuis confirmés | **bloquée** — 2 motifs |
| **EX06** | suppressions sans perte | **satisfaite** |
| **EX07** | un seul état de cotation | **satisfaite** |

Export strict refusé ; la sortie diagnostique reste disponible, et c'est elle
qui nomme ce qui manque.

### Ce qui reste à établir

| | Nombre |
|---|---|
| Correspondances enregistrées | **0** |
| Occurrences source sans décision | 198 |
| Occurrences cible sans décision | 2 |
| Confirmations d'appui (version 2) | 0 |
| Ancrages de citation (version 2) | 0 |
| Citations non résolues | 1 — nœud 1243, « P-2 » écrite sans ancrage |

Rien de tout cela n'a été confirmé automatiquement. **L'absence de lien
signifie « à établir », et rien d'autre** — ni ajout, ni retrait.

Déjà disponible sans effort : **515 appuis de juillet** remontent par la
concordance dès qu'un lien existe, dont **148 paragraphes** de la source en
portent au moins un.

### Les gestes, pendant la rédaction

**a. Relier un paragraphe réécrit à son antécédent**

```python
from document_manager import concordance as svc
from document_manager.models import Document, LibraryNode, TraitementEditorial

src = Document.objects.get(pk=9); cib = Document.objects.get(pk=10)
s = LibraryNode.objects.get(document=src, item="43")   # § 41 au papier
c = LibraryNode.objects.get(document=cib, item="1")

corr = svc.relier(src, cib, [s], [c],
                  traitement=TraitementEditorial.REFORMULE, deplace=True)
```

Une **scission** : `[s], [c1, c2]`. Une **fusion** : `[s1, s2], [c]`. Un
**ajout** : `sources=[]`. Un **retrait** : `cibles=[]` — les deux derniers avec
un `motif`, puisque ce sont des décisions.

**b. Consulter ce que l'antécédent invoquait**

```python
for a in svc.appuis_dorigine(c):
    print(a['cote_de_juillet'], a['origine'])   # « VERSION SOURCE — appui du dépôt »
```

Consultable, jamais repris d'office : un appui d'origine ne confirme pas le
nouveau texte.

**c. Décider du traitement éditorial**

```python
svc.confirmer_traitement(corr, TraitementEditorial.REFORMULE,
                         motif="resserrement, même fait")
```

La décision retient les textes examinés. Si le texte cible est réécrit ensuite,
`corr.etat_courant()` repasse à `A_REEXAMINER` et la décision d'origine reste
consultable.

**d. Réécrire sans abîmer l'acte déposé**

```python
svc.detacher_pour_edition(c, "le nouveau texte")
```

Tant que le paragraphe est conservé tel quel, les deux versions partagent le
même `Statement` — c'est ce qui rend la conservation lisible. Cette fonction
donne à la cible le sien **au moment de la divergence**, et le texte déposé
reste intact. Écrire directement dessus est refusé par la garde.

**e. Confirmer un appui, ou documenter son absence**

```python
from case_manager.models import ConfirmationAppui, EtatAppui, BordereauDepotJuillet
from document_manager.models import VersionTexte

ConfirmationAppui.objects.create(
    noeud=c, entree=BordereauDepotJuillet.objects.get(cote="P-52"),
    version_examinee=VersionTexte.capter(c.content_object),
    etat=EtatAppui.CONFIRME, role="attestation",
    portee="la date de l'envoi, non son interprétation",
    portee_sha256=ConfirmationAppui.empreinte_portee(
        "la date de l'envoi, non son interprétation"))
```

Pour une absence assumée : `entree=None`, `etat=SANS_APPUI`, **avec un motif** —
un champ vide ne vaut pas décision et bloque EX05.

**f. Ancrer une citation de pièce**

```python
from case_manager import citations
from case_manager.models import AncrageCitation

for p in citations.proposer_ancrages(c):       # propose, ne pose rien
    AncrageCitation.objects.create(
        noeud=c, entree=p['entree'], libelle_ecrit=p['libelle_ecrit'],
        debut=p['debut'], fin=p['fin'])
```

Une cote appartenant à une **citation historique** se marque `litterale=True` :
elle ne sera jamais recalculée. Le texte stocké n'est modifié dans aucun cas ;
`citations.rendre(c)` donne le texte tel qu'il doit se lire.

**g. Suivre l'avancement**

    python manage.py exporter_concordance --source 9 --cible 10

Les motifs d'EX02, EX04 et EX05 forment la liste de travail. Quand elle est
vide, `--strict` passe.

---

## 7. Les quatre divergences — pour votre décision

**Non acceptées. Le lock n'a pas été touché** : son sha256 est toujours
`d1193dcb4ef2a38d2b7adbb12bb463604805e4b03f772ae917d3b072a50fd56a`, et
`git status legal/depots/` ne rapporte rien. L'archive gelée est intacte.

Réconciliation : **102 cotes concordantes sur 106**, 0 absente du registre,
0 identité illisible, **4 divergentes**.

Dans les quatre cas, le lock nomme une `Photo` et le registre le
`PhotoDocument` qui la contient — **et les descriptions sont identiques de part
et d'autre** :

| Cote | Lock | Registre | Contenu vérifié | Description | § qui l'invoquent |
|---|---|---|---|---|---|
| **P-1** | `Photo:4558` | `photodocument:14` | ne contient que `[4558]` | « Dossier RQAP du demandeur (naissance d'Alexia) » — identique | 2 |
| **P-8** | `Photo:4526` | `photodocument:3` | ne contient que `[4526]` | « iMessages du demandeur, transférés par la défenderesse… » — identique | 2 |
| **P-15** | `Photo:4551` | `photodocument:9` | ne contient que `[4551]` | « Courriel Claudia Écrement → Élise — ancienne cote R2 » — identique | 2 |
| **P-101** | `Photo:4554` | `photodocument:12` | ne contient que `[4554]` | « Discussion Messenger du demandeur ↔ tiers… » — identique | 1 |

Les quatre photos existent. Aucun `PhotoDocument` ne contient autre chose que
la photo attendue.

### Ce que je propose, et pourquoi je ne l'ai pas fait

**Proposition : accepter les quatre comme équivalences de contenant.** Trois
raisons convergent — l'identité du contenu (un conteneur d'une seule photo), la
stricte identité des descriptions, et l'absence de tout autre candidat.

**Mais c'est une qualification d'identité documentaire, pas un calcul.** Dire
« la pièce P-1, c'est la photo » ou « c'est le document qui la présente » touche
à ce qui a été déposé. Le laisser décider par un rapport serait exactement la
correction silencieuse que la méthodologie interdit.

Deux façons de trancher :

1. **Accepter l'équivalence** — la table se qualifie alors fidèle au dépôt, et
   la décision est tracée dans chaque sortie :

       python manage.py table_des_cotes --accepter-equivalences-contenant

2. **Aligner le registre sur le lock** — faire pointer les quatre entrées vers
   la `Photo` plutôt que vers le `PhotoDocument`. Plus fidèle à la lettre du
   lock, mais cela modifie des associations du dépôt et doit être journalisé au
   titre de `METHODOLOGIE_POST_DEPOT.md § 3.3`.

Tant que ni l'une ni l'autre n'est choisie, **C13 et C15 restent PARTIELS** et
la table porte la mention « DIVERGENCES — voir le rapport de réconciliation ».

---

## 8. Limites restantes

| Limite | Nature |
|---|---|
| **C13 / C15 PARTIELS** | 4 divergences en attente de votre décision (§ 7) |
| EX02, EX04, EX05 bloquées | travail éditorial non fait — l'outil le réclame, c'est son office |
| `/documents/contestation/<pk>/` | la vue utilise le résolveur, le gabarit n'affiche aucun numéro — état antérieur inchangé |
| Paragraphe cible sans `item` | par convention de l'importateur, un `item` vide à la profondeur des paragraphes désigne une mention de clôture et ne se numérote pas. Piège pour qui crée un paragraphe à l'éditeur sans lui donner d'`item` |
| `.env` en clair | mot de passe de la base et deux clés d'API — hors périmètre, signalé |

**Retour arrière**, si nécessaire :

    pg_restore -d court_project_pg --clean --if-exists \
        ~/Backups/court/archives/court_project_pg_avant_E01_20261014_082737.dump

Ou, plus finement : `python manage.py migrate document_manager 0015` et
`migrate case_manager 0014` retirent les champs et les tables — les 198 numéros,
le mode, le référent et les instantanés sont alors perdus, mais la reprise se
rejoue à l'identique, étant idempotente et fondée sur des sources archivées.

---

## 9. Preuves

Dans `legal/amendements/01_avant_notification/preuves_E01/`, **non versionnées**
(`.gitignore` exclut `*.json` et `*.log`, le dépôt est public, et ces fichiers
portent le texte et les identifiants de l'acte déposé) :

| Fichier | Contenu |
|---|---|
| `manifeste_T01_base_de_travail.json` | les 198 associations, avec empreintes |
| `T01_base_de_travail.log` | le contrôle sans écriture |
| `manifeste_T03_base_de_travail.json`, `T03_base_de_travail.log` | l'application et son contrôle |
| `T17_base_de_travail.log` | les douze sorties vérifiées |
| `concordance_base_de_travail.json` / `.csv` / `.log` | la concordance diagnostique |
| `table_cotes_base_de_travail.json` / `.csv` / `.log` | la table des cotes et la réconciliation |

Suite de tests du dépôt après mise en service : **127 tests, OK, aucune
régression.**

---

## 10. Ce qui n'a pas été fait

- **La branche n'est pas fusionnée** et rien n'est déployé.
- **Le lock n'a pas été modifié**, ni les associations du registre.
- **`legal/depots/2026-07-24_initial/` est intact** — vérifié par empreinte et
  par `git status`.
- **Aucune décision éditoriale ou probatoire n'a été confirmée** à votre place.
- **`--accepter-equivalences-contenant` n'a pas été activé.**
