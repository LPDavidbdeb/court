# Plan de bascule des embeddings vers le modèle multilingue

De `all-mpnet-base-v2` (anglophone) vers
`sentence-transformers/paraphrase-multilingual-mpnet-base-v2`.
État mesuré le 2026-08-11.

> ## ⚠️ Décision prise — ce document devient une référence, pas une marche à suivre
>
> **Le modèle a été changé** le 2026-08-11 à
> [ai_services/services.py:311](../../ai_services/services.py:311).
> **Le vidage des colonnes a été intégré à la phase 4 de la purge des citations**
> ([CARTE_RELATIONS.md](CARTE_RELATIONS.md)), là où `backfill_embeddings` tourne déjà.
> Il n'y a **pas d'opération séparée** à mener.
>
> Ce qui a fait tomber la cérémonie de ce plan : les embeddings n'alimentent **rien**. Leur
> unique consommateur est `global_semantic_search`, derrière une route `/semantic-search/`
> vers laquelle aucune template ne pointe. Le snapshot de la phase 0 et la table
> `EmbeddingState` de la phase 1 sont donc devenus superflus — on ne s'assure pas contre la
> perte de ce que personne ne lit.
>
> **Ce qui reste utile ici** : l'état de départ mesuré, le test de sanité qui attrape une
> bascule ratée (§ phase 3.3), et la procédure de retour arrière si un jour ces vecteurs
> servent à quelque chose. Les phases 0, 1 et 2 sont conservées pour mémoire.

---

## Le seul vrai danger, et l'invariant qui l'annule

Les deux modèles produisent des vecteurs de **768 dimensions**. `VectorField(dimensions=768)`
accepte donc les uns comme les autres **sans lever d'erreur**. Une base qui contiendrait des
vecteurs des deux modèles renverrait des distances cosinus dénuées de sens, silencieusement —
aucun test, aucune contrainte, aucun log ne le signalerait.

Tout le plan tient à un invariant :

> **À tout instant, la colonne `embedding` d'une ligne contient soit `NULL`, soit un vecteur
> du modèle courant. Jamais un vecteur d'un autre modèle.**

`NULL` est un état sûr : il est explicite, `backfill_embeddings` le repère et le remplit.
L'état dangereux n'est pas « incomplet », c'est « mélangé ». D'où la règle : **on vide tout
avant de remplir quoi que ce soit.** Une bascule interrompue laisse une base incomplète —
récupérable en relançant. Une bascule incrémentale laisserait une base corrompue.

---

## État de départ mesuré

| Modèle | Lignes | Avec texte source | Vecteurs actuels | Attendu après |
|---|---|---|---|---|
| `email_manager.Email` | 629 | 628 | 467 | **628** |
| `events.Event` | 319 | 318 | 318 | **318** |
| `pdf_manager.PDFDocument` | 97 | 31 | 31 | **31** |
| `photos.PhotoDocument` | 19 | 13 | 12 | **13** |
| `document_manager.Document` | 8 | 8 | 7 | **8** |
| `email_manager.Quote` | 211 | 211 | 152 | **211** |
| `pdf_manager.Quote` | 103 | 103 | 88 | **103** |
| `document_manager.Statement` | 218 | 217 | 193 | **217** |
| **total** | **1604** | **1529** | **1268** | **1529** |

Deux enseignements.

**Le remplissage actuel est incomplet.** 1268 vecteurs pour 1529 lignes qui ont un texte :
**261 lignes n'ont jamais été encodées**, surtout des courriels (161 manquants). La bascule
répare cela au passage.

**« Toutes les lignes » n'est pas le critère de vérification.** 75 lignes n'ont aucun texte
source — 66 `PDFDocument` sans `ai_analysis`, 6 `PhotoDocument`, 1 `Statement`, 1 `Email`,
1 `Event`. Elles resteront `NULL` légitimement. Le critère est la colonne **« attendu après »**,
pas le total.

**Volume** : 1 529 textes à encoder, ~5 à 10 minutes sur CPU. Snapshot des vecteurs actuels :
1 268 × 768 × 4 octets ≈ **3,9 Mo**. C'est assez petit pour rendre le retour arrière instantané.

---

## Phase 0 — Verrous préalables (aucune écriture)

Un script de contrôle qui **échoue bruyamment** plutôt que de laisser passer :

```python
# 1. les deux modèles sont disponibles hors ligne
from sentence_transformers import SentenceTransformer
ancien = SentenceTransformer("all-mpnet-base-v2")
nouveau = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

# 2. dimensions identiques — sinon il faut une migration de schéma, pas une bascule
assert ancien.get_sentence_embedding_dimension() == 768
assert nouveau.get_sentence_embedding_dimension() == 768

# 3. état de départ figé, pour comparaison en phase 3
```

Puis **le snapshot**, qui est ce qui rend l'opération sans risque :

```python
import numpy as np
for model in (Email, Event, PDFDocument, PhotoDocument, Document,
              EmailQuote, PDFQuote, Statement):
    rows = model.objects.exclude(embedding=None).values_list("pk", "embedding")
    pks = [r[0] for r in rows]
    vecs = np.array([r[1] for r in rows], dtype="float32")
    np.savez_compressed(f"backup_embeddings/{model._meta.label}.npz", pks=pks, vecs=vecs)
```

3,9 Mo au total. Sans lui, un retour arrière coûte un ré-encodage complet ; avec lui, il
coûte une minute.

---

## Phase 1 — Rendre le modèle traçable (la correction de fond)

C'est l'étape que je recommande le plus, parce qu'elle règle la cause et pas le symptôme.
**Aujourd'hui, rien en base n'enregistre quel modèle a produit un vecteur.** C'est ce qui
rend le mélange indétectable, et ce sera vrai à la prochaine bascule comme à celle-ci.

Ajouter une table à une seule ligne, dans `ai_services` :

```python
class EmbeddingState(models.Model):
    """Quel modèle a produit les vecteurs actuellement en base."""
    model_name = models.CharField(max_length=200)
    dimensions = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    vector_count = models.PositiveIntegerField(default=0)
```

Une migration, une table neuve, **aucune modification des modèles existants** — donc aucun
risque sur les données.

Puis un garde-fou dans `backfill_embeddings` :

- si `EmbeddingState.model_name` ≠ modèle configuré → **refuser de tourner**, avec un message
  qui explique et propose `--switch-model` ;
- `--switch-model` exécute la séquence complète : vider les colonnes, mettre l'état à jour,
  remplir.

Après ça, la bascule d'aujourd'hui n'est plus une manœuvre délicate mais une commande, et le
mélange silencieux devient structurellement impossible.

L'état doit vivre **en base**, pas dans un fichier du dépôt : il doit voyager avec les données,
y compris quand la base est restaurée depuis un dump.

---

## Phase 2 — Bascule

**2.1** Changer une seule ligne — [ai_services/services.py:311](../../ai_services/services.py:311) :

```python
_EMBED_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
```

Vérifié : les seuls consommateurs sont [core/services.py:15](../../core/services.py:15)
(`global_semantic_search`) et
[backfill_embeddings.py:132](../../document_manager/management/commands/backfill_embeddings.py:132).
Aucun autre appelant de `generate_embedding` / `generate_embeddings_batch` dans le projet.

**2.2** Vider les huit colonnes, **en une seule transaction** :

```python
with transaction.atomic():
    for model in (Email, Event, PDFDocument, PhotoDocument, Document,
                  EmailQuote, PDFQuote, Statement):
        n = model.objects.exclude(embedding=None).update(embedding=None)
        print(f"{model._meta.label}: {n} vecteurs effacés")
```

Attendu : **1 268 effacés**. Une transaction unique garantit qu'on ne s'arrête pas à
mi-chemin dans un état mixte.

**2.3** Remplir :

```bash
.venv/bin/python manage.py backfill_embeddings
```

`--only-missing` étant vrai par défaut, la commande est **reprenable** : si elle s'interrompt,
on la relance et elle poursuit là où elle en était. C'est vrai *parce que* la phase 2.2 a
tout remis à `NULL`.

---

## Phase 3 — Vérification

**3.1 Comptes.** Chaque modèle doit atteindre exactement sa colonne « attendu après ». Un
écart signale des lignes dont le texte source est vide — à vérifier une par une, pas à ignorer.

**3.2 Aucun résidu.** Aucune ligne avec texte source ne doit rester `NULL`.

**3.3 Contrôle de sanité du nouvel espace.** Sur des paires dont on connaît la réponse :

```
paraphrase FR      attendu ≈ 0,66
appui factuel FR   attendu ≈ 0,70
sans rapport       attendu ≈ 0,08   ← le point qui change tout
```

Si « sans rapport » ressort vers 0,40, c'est l'ancien modèle qui a tourné : la configuration
n'a pas été prise en compte. **C'est le test qui attrape une bascule ratée.**

**3.4 Régression de recherche.** Avant la bascule, noter le top-10 de
`global_semantic_search` pour 5 requêtes types. Après, comparer. On n'attend pas des
résultats identiques — c'est le but — mais des résultats **au moins aussi pertinents**. Si le
nouveau classement est moins bon, on a le snapshot pour revenir.

---

## Phase 4 — Retour arrière

Si la phase 3 déçoit, deux mouvements :

```python
# 1. remettre l'ancien nom dans ai_services/services.py
# 2. restaurer les vecteurs depuis le snapshot
for model in (...):
    z = np.load(f"backup_embeddings/{model._meta.label}.npz")
    objs = []
    for pk, vec in zip(z["pks"], z["vecs"]):
        objs.append(model(pk=int(pk), embedding=vec))
    model.objects.bulk_update(objs, ["embedding"], batch_size=500)
```

On retrouve l'état exact du départ, y compris ses 261 lignes non encodées. Une minute, pas
un ré-encodage.

---

## Articulation avec la purge des citations

Les 314 citations vont être détruites puis refaites. Deux ordonnancements possibles :

| | Bascule d'abord | Purge d'abord |
|---|---|---|
| textes encodés en pure perte | 314 (les citations qui seront détruites) | 0 |
| états intermédiaires à surveiller | 1 | 2 |
| risque de mélange | nul | **réel** — si la purge intervient entre le vidage et le remplissage |

**Recommandation : bascule d'abord, purge ensuite.** Le coût du gaspillage est d'environ deux
minutes de calcul ; le bénéfice est qu'on ne mène qu'un seul changement d'état à la fois. En
phase 4 de la purge, `backfill_embeddings` encodera les nouvelles citations dans l'espace déjà
en place — sans nouvelle décision à prendre.

---

## Ce que la bascule ne corrige pas

**La fenêtre de 128 tokens.** `backfill_embeddings` encode `Email.body_plain_text`, et vos
courriels vont jusqu'à 32 000 caractères : seuls les ~100 premiers mots sont représentés. Le
vecteur d'un long courriel décrit ses salutations, pas son contenu. C'était déjà vrai avec
l'ancien modèle et ça le reste — les deux ont la même fenêtre.

Si la recherche sémantique sur les courriels déçoit, la cause est là. Le correctif serait de
découper les textes longs en fenêtres et de conserver plusieurs vecteurs par courriel — ce qui
suppose une table de fragments, donc un changement de modèle de données. **Hors périmètre de
cette bascule**, mais à garder en tête : c'est probablement le gain le plus important qui
reste disponible.

**Le fondement de la décision.** L'écart mesuré entre les deux modèles repose sur **trois
paires choisies à la main** (plancher de bruit 0,395 contre 0,079). La direction est claire,
mais ce n'est pas une évaluation. Si vous voulez une décision mieux étayée avant d'engager la
bascule, la mesure à faire est un test de classement sur des paires réelles tirées du corpus,
où la bonne réponse est connue d'avance.

---

## Résumé exécutable

```
0. contrôles + snapshot (3,9 Mo)          → aucune écriture en base
1. table EmbeddingState + garde-fou       → 1 migration, table neuve
2. changer _EMBED_MODEL_NAME
   vider les 8 colonnes (1 transaction)   → 1 268 vecteurs effacés
   manage.py backfill_embeddings          → 1 529 vecteurs écrits, ~5-10 min
3. vérifier comptes + sanité + régression
4. (si besoin) restaurer le snapshot      → ~1 min
puis : purge des citations
```
