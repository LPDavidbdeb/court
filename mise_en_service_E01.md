# Mise en service d'E01 sur la base de travail

Exécutée le **14 octobre 2026, 08 h 27 – 08 h 40 (UTC−4)**.

    Branche  : epic/E01-numerotation-concordance   (non fusionnée)
    Commit   : 3df17eb6c4f804eb66071be657ec79930a18902a
    Base     : court_project_pg  —  PostgreSQL 18.1, localhost:5432
    Verdict  : EN SERVICE. C13/C15 demeurent PARTIELS.

> **Mise à jour du 14 octobre, 10 h 36.** Les quatre divergences du § 7 ont été
> tranchées : la qualification explicite est appliquée, la réconciliation est
> **CONFORME** (106/106), et **C13 et C15 sont validés** — E01 est VALIDÉE,
> 18 critères sur 18. Le verdict ci-dessus et le § 8 décrivent l'état
> antérieur et sont conservés comme tels. Voir le **complément de clôture**
> aux § 11 à 20.
>
> Pendant cette clôture, la **rédaction a commencé** dans l'application : une
> correspondance, deux ancrages de citation et une confirmation d'appui ont été
> enregistrés, et EX04 est passée à satisfaite. Ce n'est pas l'œuvre de cette
> tâche ; le § 16 bis le relève et le date. Les comptes du § 6 sont donc ceux
> de 08 h 40.

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

> Les comptes de ce § sont ceux de 08 h 40. Le relevé du § 16 bis les actualise
> au 14 octobre, 10 h 36 : la rédaction a commencé. Les **gestes** décrits
> ci-dessous restent valables tels quels.

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

> **Tranchées le 14 octobre à 09 h 50.** Ce § consigne l'état où la décision
> était attendue ; le § 11 porte la décision prise et le § 12 les vérifications
> faites dans les **deux** sens du rattachement, que ce § n'établissait pas
> encore.

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

**La première option a été retenue** — § 11. La seconde, qui aurait modifié des
associations du dépôt, n'a pas été exercée.

---

## 8. Limites restantes

> État au 08 h 40. La première ligne est levée depuis le § 11 ; les autres
> demeurent.

| Limite | Nature |
|---|---|
| ~~**C13 / C15 PARTIELS**~~ | ~~4 divergences en attente de votre décision (§ 7)~~ — **levée le 14 octobre, § 11 à 16** |
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

> État au 08 h 40 ; la dernière ligne a cessé d'être vraie à 09 h 50. L'état
> définitif est au § 20.

- **La branche n'est pas fusionnée** et rien n'est déployé.
- **Le lock n'a pas été modifié**, ni les associations du registre.
- **`legal/depots/2026-07-24_initial/` est intact** — vérifié par empreinte et
  par `git status`.
- **Aucune décision éditoriale ou probatoire n'a été confirmée** à votre place.
- ~~**`--accepter-equivalences-contenant` n'a pas été activé.**~~ — **activé le
  14 octobre à 09 h 50, par décision explicite (§ 14).**

---

# Complément du 14 octobre 2026 — clôture de la validation

Exécuté le **14 octobre 2026, 09 h 50 – 10 h 25 (UTC−4)**.

    Branche  : epic/E01-numerotation-concordance   (toujours non fusionnée)
    Commit   : c11c171236e31ebafc3f2f887fdf84cadbe01433
    Base     : court_project_pg  —  PostgreSQL 18.1, localhost:5432
    Verdict  : E01 VALIDÉE — 18 critères sur 18. C13 et C15 ne sont plus partiels.

Le § 7 ci-dessus demandait une décision. Elle a été prise.

---

## 11. La décision, et ce qu'elle dit

**Règle métier précisée par le demandeur :** *une Photo appartient au plus à un
PhotoDocument.*

Sur ce fondement, l'**équivalence de contenant** est retenue pour les quatre
couples P-1, P-8, P-15 et P-101. La décision reconnaît **une même matière
documentaire désignée à deux niveaux** — l'image, et la pièce d'un seul feuillet
qui la présente. Elle **conserve les deux identifiants et leurs types
distincts** : rien n'est fusionné, renommé ni réaffecté.

### Règle métier ≠ contrainte du schéma

C'est la distinction à ne pas perdre. `photos.PhotoDocument.photos` est un
**`ManyToManyField`** (table de jonction `photos_photodocument_photos`) : le
schéma n'impose **aucune** cardinalité, ni dans un sens ni dans l'autre.

| | |
|---|---|
| Règle métier | une Photo appartient au plus à un PhotoDocument |
| Garantie par le schéma | **aucune** — plusieurs-à-plusieurs des deux côtés |
| Donc | la règle est **vérifiée sur l'état examiné**, non **garantie** |

Une migration de cardinalité ne fait pas partie de cette clôture. Ce qui a été
fait à la place : le contrôle vérifie désormais la règle **à chaque exécution**,
dans les deux sens, et porte ses deux preuves dans sa sortie (§ 13).

---

## 12. Les vérifications, dans les deux sens

Refaites sur l'état courant de `court_project_pg`. Huit assertions par couple,
**trente-deux en tout, toutes satisfaites**.

| Cote | Au lock | Au registre | Photo → PhotoDocuments | PhotoDocument → Photos | Descriptions | Lignes de registre |
|---|---|---|---|---|---|---|
| **P-1** | `Photo:4558` | `photodocument:14` | **[14]** | **[4558]** | identiques | 1 |
| **P-8** | `Photo:4526` | `photodocument:3` | **[3]** | **[4526]** | identiques | 1 |
| **P-15** | `Photo:4551` | `photodocument:9` | **[9]** | **[4551]** | identiques | 1 |
| **P-101** | `Photo:4554` | `photodocument:12` | **[12]** | **[4554]** | identiques | 1 |

Les deux colonnes du milieu sont les deux sens du rattachement. La première —
*cette photo n'appartient qu'à ce PhotoDocument* — est celle que le § 7 n'avait
pas encore établie : il ne montrait que le sens du contenant.

### L'état des données examiné

| | |
|---|---|
| Photos | 1 733 |
| PhotoDocument | 20 |
| Photos rattachées à au moins un PhotoDocument | 35 |
| **Photos rattachées à plus d'un PhotoDocument** | **0** |
| PhotoDocument d'un seul feuillet | 15 |
| Entrées au registre | 334 |

La règle métier est donc respectée par **l'ensemble** des données, non seulement
par les quatre couples. C'est un constat sur cet état, pas une garantie.

### Le périmètre est exactement ces quatre couples

Divergences observées : `P-1, P-8, P-15, P-101`. **0** cote absente du registre,
**0** identité illisible, **aucun** autre couple découvert pendant le contrôle.
La décision n'a été étendue à rien.

Preuve : `preuves_E01/preuve_equivalences_contenant.json` et son `.log`.

---

## 13. Le mécanisme, resserré pour exiger les deux sens

`_equivalence_contenant` ne vérifiait que le sens du contenant. La condition
réciproque est désormais vérifiée aussi, et le refus est conservateur : si une
photo figure dans un second PhotoDocument, il n'y a **pas** d'équivalence, et la
cote reste `DIVERGE`.

**Pourquoi le changer plutôt que de s'en tenir au contrôle fait à la main.**
Sans ce resserrement, la qualification reposerait à chaque exécution future sur
un test **plus faible que la décision qu'elle met en œuvre**. Si une photo
visée était un jour rattachée à un second feuillet, l'équivalence continuerait
d'être acceptée alors que sa condition aurait cessé d'être vraie.

Résultat **inchangé** sur l'état examiné — les quatre équivalences sont
identifiées comme avant. Aucune migration, aucun changement de schéma.

Six tests nouveaux, `case_manager.test_e01_cotes_concordance.T24EquivalenceDeContenant` :

| Test | Ce qu'il fixe |
|---|---|
| sans acceptation, elle compte comme divergence | le défaut reste le refus |
| acceptée explicitement, elle concorde avec sa preuve | les deux preuves sont dans la sortie |
| une photo dans deux feuillets n'est pas une équivalence | le sens réciproque |
| un feuillet portant une autre photo n'est pas une équivalence | le sens du contenant |
| l'acceptation n'écrit rien | la qualification est une lecture |
| la table porte la fidélité quand l'équivalence est acceptée | l'effet sur C15 |

---

## 14. La qualification appliquée

    python manage.py table_des_cotes --accepter-equivalences-contenant \
        --liasses \
        --json …/preuves_E01/table_cotes_qualifiee.json \
        --csv  …/preuves_E01/table_cotes_qualifiee.csv

Code de retour **0** — il était de 1 avant la décision.

| Mesure | Avant (diagnostic conservé) | Après |
|---|---|---|
| Cotes contrôlées | 106 | 106 |
| **Concordantes** | **102** | **106** |
| Absentes du registre | 0 | 0 |
| Identités illisibles | 0 | 0 |
| **Divergentes** | **4** | **0** |
| Équivalences de contenant | 4, comptées comme divergences | **4, retenues et visibles** |
| Ajouts sans cote de juillet | 66 | 66 |
| **Verdict** | **NON CONFORME** | **CONFORME** |
| Fidélité de la table | DIVERGENCES — voir le rapport | **CONFORME AU LOCK** |

Les quatre équivalences **restent lisibles au manifeste** sous leur verdict
propre `EQUIVALENCE_CONTENANT`, chacune avec sa preuve du contenant, sa preuve
réciproque et la mention que le schéma ne garantit pas la règle.

### Le diagnostic antérieur est conservé

`preuves_E01/table_cotes_diagnostique_avant_qualification.json` / `.csv` /
`.log` disent toujours **102/106, NON CONFORME**, les quatre comptées comme
divergences. La décision n'efface pas l'état qui l'a appelée.

---

## 15. Ce qui n'a pas été touché

| | Vérification |
|---|---|
| `cotes.lock.json` | sha256 toujours `d1193dcb4ef2a38d2b7adbb12bb463604805e4b03f772ae917d3b072a50fd56a` |
| `legal/depots/2026-07-24_initial/` | `shasum -c SHA256SUMS` — **les 8 candidats : OK** ; `git status legal/depots/` ne rapporte rien |
| Associations historiques du registre | les 4 entrées pointent toujours le `photodocument` ; aucune autre cote réalignée |
| Composition des documents | `photodocument 14 → [4558]`, `3 → [4526]`, `9 → [4551]`, `12 → [4554]` |
| Référent historique | empreinte `02d9c468c95b2c4294103c162b6ce4f253b7cef2ad27a5c8c57650b1d23fbf14`, contenu intact, **0 écart** sur les sept catégories |
| État de cotation | `dda2ee0d2270bf16…` — **identique** à celui de la mise en service de 08 h 40 |

**La qualification est une lecture, pas une correction.** Un test le vérifie en
relisant le registre et la composition du document après l'acceptation.

Preuve : `preuves_E01/integrite_apres_cloture.log`.

---

## 16. Revalidation de C13 et C15 sur les données réelles

Contrôles de **T24–T26 et T28** rejoués sur `court_project_pg`, attentes
calculées depuis le lock et à la main, jamais demandées au service contrôlé.
**0 échec.**

### C13 — le contrôle historique

| Contrôle | Résultat |
|---|---|
| Cotes contrôlées / concordantes | 106 / **106** (le dénominateur vient du lock) |
| Manquantes / divergentes / ambiguës | **0 / 0 / 0** |
| Équivalences visibles au manifeste | **P-1, P-8, P-15, P-101** |
| Les quatre portent la preuve du contenant | **oui** |
| Les quatre portent la preuve réciproque | **oui** |
| Associations corrigées hors équivalences | **aucune** |
| Diagnostic antérieur | **102, NON CONFORME** — toujours lisible |
| Ajouts sans cote de juillet | 66, **aucun compté comme manque** |

### T24 — la table autonome

| Contrôle | Résultat |
|---|---|
| Une ligne par entrée du registre | **334** |
| Même ordre que `cotation_chronologique()`, au pk près | **oui** |
| Rangs consécutifs depuis 1 | **1 … 334** |
| Fidélité historique | **CONFORME AU LOCK** |
| Les ajouts n'imposent pas P-107 | **oui** — leur rang chronologique gouverne |
| Les ajouts restent identifiables | **oui** — « (sans cote de juillet) » |
| Source non résolue | **0** |
| Deux lectures, même empreinte | **oui** |

### T25 — liasses, dates, départage

| Contrôle | Résultat |
|---|---|
| Composition des liasses de juillet préservée | **identique au registre**, entrée par entrée |
| Liasses de juillet | 30, dont **20 dispersées** |
| Un passage prend la date de sa pièce | **oui** — 0 écart sur les passages contrôlés |
| Départage stable sur les horodatages égaux | **oui** |

### T26 — les trois groupes

| Groupe | Entrées |
|---|---|
| `datee` | 331 |
| `a_dater` | 1 |
| `atemporelle` | 2 |

Les trois blocs se suivent dans cet ordre, et les atemporelles sont exactement
celles que le registre déclare telles — « à dater » et « atemporelle » ne se
confondent pas.

### T28 — reproductibilité et citations rendues

| Contrôle | Résultat |
|---|---|
| Deux exports sur le même état | **même empreinte, mêmes lignes** |
| L'export et la table partagent l'état de cotation | **oui** — `dda2ee0d…` |
| Lignes de concordance | **199** au relevé de 10 h 36 (200 à 08 h 40 — § 16 bis) |
| JSON sans échappement d'accents | **oui** |
| Index des cotes cibles | **334** — couvre le registre |
| Textes stockés modifiés par le rendu | **0** |
| EX07 — un seul état de cotation | **satisfaite** |

**Effet de la décision sur EX04.** La condition portait deux motifs. La
décision en lève **un seul**, et un contrôle le vérifie en comparant les motifs
d'avant et d'après — elle ne résout rien d'autre.

| | Motifs d'EX04 |
|---|---|
| Avant la décision | réconciliation du lock non conforme **+** nœud 1243, « P-2 », cote écrite sans ancrage |
| Après la décision | nœud 1243 seulement — **motif éditorial** |

L'export strict reste refusé, pour EX02 et EX05. C'est son office.

Preuve : `preuves_E01/revalidation_C13_C15.json` et son `.log`.

---

## 16 bis. Le travail éditorial a commencé — relevé du 14 octobre, 10 h 36

**À signaler, parce que les nombres ci-dessus et ceux du § 6 ont changé pendant
la clôture.** L'**étape 1 du lot éditorial 01** a été appliquée en parallèle par
une tâche distincte — `run_id 20261014_a25cfb3d`, 10 h 26 – 10 h 33, sur
autorisation « commençons par 1 ». **Elle ne vient pas de cette tâche-ci**, qui
n'a confirmé aucune correspondance, aucun appui et aucun ancrage.

Ce qu'elle a enregistré : correspondance 985 → 1233 (§ 93 → § 1), `REFORMULE`,
déplacée, état courant **CONFIRME** ; confirmation d'appui sur l'entrée P-19,
portée « teneur de l'acte, non véracité des énoncés », état **CONFIRME** ;
ancrage courant « P-19 » au nœud 1233, rendu **P-249** ; ancrage **littéral**
« P-2 » au nœud 1243, rendu conservé **P-2**. Le chapeau cible a été réécrit;
le rendu de ses cotes n'altère pas le texte stocké. La citation historique et
le référent sont intacts. Détail : `legal/amendements/01_avant_notification/lot_editorial_01.md`
§ 11.

| | Au 08 h 40 | Au 10 h 36 |
|---|---|---|
| Lignes de concordance | 200 | **199** |
| Correspondances 9 → 10 | 0 | **1** |
| Occurrences source sans décision | 198 | **197** |
| Ancrages de citation | 0 | **2**, dont 1 littéral |
| Confirmations d'appui | 0 | **1** |
| Citations non résolues sur la cible | 1 | **0** |
| EX02 | bloquée, 200 motifs | bloquée, **198** motifs |
| EX04 | bloquée, 2 motifs | **SATISFAITE** |
| EX05 | bloquée, 2 motifs | bloquée, **1** motif |

**EX04 est donc satisfaite pour deux causes distinctes**, qu'il ne faut pas
confondre : la part « réconciliation du lock » par la décision de 09 h 50, la
part « cote sans ancrage » par l'ancrage littéral du lot 01. La seconde n'est
pas un effet de la première — et le diagnostic du lot 01, produit sans l'option
d'acceptation, portait encore le premier motif. **Les deux tâches étaient
nécessaires**, chacune pour sa moitié.

Le § 2 (nœud 1244) reste ouvert : 0 correspondance, 0 appui examiné, 0 ancrage.
C'est le motif unique qui subsiste à EX05.

**Ces nombres sont un relevé, pas un invariant.** Ils changeront à chaque
exécution à mesure que la version 2 s'écrit, et **ni C13 ni C15 n'en dépendent**
— ces deux critères portent sur les cotes et sur le lock, dont l'état est
inchangé.

**Le référent a tenu pendant ce travail.** Document 9 toujours en `STORED`,
371 nœuds, 198 `paragraph_number`, 515 appuis de juillet, empreinte
`02d9c468c95b2c42…`, **0 écart** sur les sept catégories. Les gardes font leur
office pendant que la version 2 s'écrit — c'est précisément ce pour quoi elles
ont été posées.

---

## 17. Tests et contrôles du dépôt

    python manage.py check                        → aucun problème
    python manage.py makemigrations --check       → « No changes detected »
    python manage.py test                         → 133 tests, OK

**Aucune régression.** 127 tests avant la clôture, **133 après** — les six
ajoutés sont ceux du § 13. Pour les 29 scénarios du cahier : **107 méthodes**
(51 dans `document_manager`, 56 dans `case_manager`).

---

## 18. Ce que ce verdict dit, et ce qu'il ne dit pas

**E01 est VALIDÉE — 18 critères sur 18.** C13 et C15 étaient les deux seuls
partiels, pour une cause unique, et elle est levée. Aucun autre critère n'a
régressé : `check`, `makemigrations --check` et les 133 tests passent, les douze
sorties restent conformes, le référent reste intact.

**Ce verdict porte sur l'outillage** et sur la fidélité historique de la table
des cotes. Il ne dit rien de la **concordance éditoriale réelle** :

| | État au 14 octobre, 10 h 36 |
|---|---|
| Correspondances document 9 → document 10 | **1 enregistrée** ; 198 occurrences source sans décision |
| Confirmations d'appui de la version 2 | **1** |
| Ancrages de citation de la version 2 | **2**, dont 1 littéral |
| EX02, EX05 | **bloquées** — travail éditorial |
| EX04 | satisfaite — voir le § 16 bis sur ses deux causes |

**Aucune décision du lot éditorial n'a été enregistrée par cette tâche.** Celles
qui figurent ci-dessus ont été prises dans l'application, pendant la clôture, et
sont consignées au § 16 bis sans être attribuées ici. Les gestes pour la
rédaction sont au § 6, et ils restent entiers.

---

## 19. Preuves de la clôture

Dans `legal/amendements/01_avant_notification/preuves_E01/`, **non versionnées**
pour les raisons du § 9 :

| Fichier | Contenu |
|---|---|
| `preuve_equivalences_contenant.json` / `.log` | les quatre couples, les deux sens, 32 assertions, l'état des données |
| `table_cotes_diagnostique_avant_qualification.json` / `.csv` / `.log` | **le diagnostic antérieur** — 102/106, NON CONFORME |
| `table_cotes_qualifiee.json` / `.csv` / `.log` | la table qualifiée — 106/106, CONFORME AU LOCK, équivalences visibles |
| `concordance_apres_qualification.json` / `.csv` / `.log` | la concordance sur le même état ; EX04 réduite à son motif éditorial |
| `revalidation_C13_C15.json` / `.log` | C13, C15, T24–T26 et T28 sur les données réelles — 0 échec |
| `integrite_apres_cloture.log` | archive gelée, lock, référent — empreintes après la clôture |
| `tests_apres_cloture.log` | la suite du dépôt — 133 tests, OK |

---

## 20. Ce qui n'a toujours pas été fait

- **La branche n'est pas fusionnée** et rien n'est déployé.
- **Le lock n'a pas été modifié**, ni les associations historiques du registre,
  ni la composition des documents.
- **`legal/depots/2026-07-24_initial/` est intact** — vérifié par empreinte et
  par `git status`.
- **Aucune décision éditoriale ou probatoire n'a été confirmée.**
- **La décision n'a pas été étendue** à un autre couple.
- **Aucune migration de cardinalité** n'a été proposée ni appliquée.
