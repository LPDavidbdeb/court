# Suivre l'évolution des paragraphes en base — disparition, déplacement, ajout

> **Question du demandeur, 7 octobre 2026** : la demande étant traduite dans
> `document_manager`, la nature de la base peut-elle servir à suivre l'évolution
> des paragraphes entre l'acte déposé et l'acte réécrit ?
>
> **Réponse : oui, et les deux tiers du mécanisme existent déjà.** Il manque
> **un seul champ**. Ce fichier dit ce qui existe, ce qui manque, et ce que
> chacun des deux balayages de
> [`communication_pieces.md`](communication_pieces.md) § 10.2 b devient une fois
> le champ ajouté.

---

## 1. Ce qui existe déjà et qu'il ne faut pas rebâtir

### 1.1 La numérotation n'est pas stockée — elle est calculée

`document_manager/numerotation.py` la recalcule depuis la **profondeur du nœud**
et le `SchemaNiveaux` du document. Son propre en-tête pose la règle :

> « `LibraryNode.item` conserve le numéro que le paragraphe avait **AU DÉPÔT** ;
> le schéma en recalcule un autre, qui est celui affiché à l'écran et celui que
> porterait une version amendée. […] La règle est donc : on désigne un
> paragraphe par **`§ 44 (dépôt 28)`**, jamais par l'un des deux seul. »

➜ **« Renuméroter les paragraphes » n'est pas un travail.** C'est une
conséquence de la position dans l'arbre. Déplacer un nœud le renumérote. Le
poste de charge est la **réécriture** et la **concordance**, pas la
numérotation.

### 1.2 Un `Statement` est réutilisable entre documents — et il l'est déjà

Le modèle le dit (« *a single, **reusable** block of content* ») et la base le
confirme : **20 statements sont déjà partagés entre deux documents ou plus**, et
le document 10 — *« DEMANDE INTRODUCTIVE D'INSTANCE — version 2 »* — **réutilise
10 de ses 12 statements du document 1**, la Requête de 2015.

➜ La réutilisation inter-documents n'est pas une capacité théorique : c'est la
pratique courante de cette base.

### 1.3 Le lien statement → cote du dépôt existe

`case_manager.AppuiDepotJuillet` — **515 lignes** : `statement`, `entree`,
`cote_citee`, `via_liasse`, `precision`, `note`. C'est **le côté « ancienne
cote » de la table de concordance**, déjà peuplé.

### 1.4 L'état des deux actes en base

| Document | Titre | Nœuds | Statements |
|---|---|---|---|
| **9** | *Demande introductive d'instance — dépôt du 24 juillet 2026* | 371 | 287 |
| **10** | *Demande introductive d'instance — version 2* | 17 | 12 |

La v2 **existe déjà** et a commencé. Son contenu actuel cite la Requête
adverse ; aucun de ses statements ne vient encore du document 9.

## 2. Ce qui manque : un seul champ

Un paragraphe réécrit tombe dans l'un de trois cas. Deux sont déjà couverts.

| Cas | Mécanisme | État |
|---|---|---|
| **Libellé inchangé** | le **même** `Statement`, pointé par un nœud dans chaque document | ✅ fonctionne aujourd'hui, sans migration |
| **Reformulé** — le cas dominant de cette réécriture | nouveau `Statement` **+ lien vers son antécédent** | ❌ **le trou** |
| **Réellement nouveau** | nouveau `Statement`, **sans** antécédent | ✅ détectable *dès que le lien existe*, par son absence |

Le troisième cas ne se détecte que si le deuxième est modélisé : **sans le lien,
un paragraphe reformulé et un paragraphe nouveau sont indiscernables.** C'est
exactement le verrou de prescription.

### La migration minimale

Sur `Statement` :

```python
derive_de = models.ForeignKey(
    'self', on_delete=models.SET_NULL, null=True, blank=True,
    related_name='derives',
    help_text="Le statement de l'acte déposé que celui-ci reformule."
)
type_derivation = models.CharField(
    max_length=16, blank=True,
    choices=[('REFORMULATION', 'Reformulation'), ('SCISSION', 'Scission'),
             ('FUSION', 'Fusion'), ('NOUVEAU', 'Fait nouveau')],
)
```

Un FK réflexif suffit pour la reformulation et la scission (plusieurs dérivés
d'un même antécédent). **La fusion** — plusieurs paragraphes déposés refondus en
un seul — demande une relation *plusieurs-à-plusieurs* ; à trancher selon que ce
cas se présente ou non.

## 3. Ce que les trois mouvements deviennent

Une fois le champ posé, les balayages ne sont plus un travail de relecture mais
**trois requêtes**.

| Mouvement | Requête | Ce qu'elle protège |
|---|---|---|
| **Disparition** | statements du doc 9 sans nœud dans le doc 10 **et** sans `derives` dans le doc 10 | Qu'aucun fait ne disparaisse par accident. Chaque ligne doit être **abandonnée délibérément** ou récupérée |
| **Ajout** | statements du doc 10 avec `derive_de IS NULL` **et** absents du doc 9 | 🔴 **Le verrou de prescription.** Chaque ligne est un fait nouveau potentiel, hors de l'interruption acquise au dépôt |
| **Déplacement** | pour un statement (ou son dérivé) présent dans les deux : comparer le numéro **recalculé** dans chacun | La carte `§ nouveau ← § dépôt`, c'est-à-dire la table de concordance elle-même |

Et la concordance des cotes se greffe dessus sans travail supplémentaire :
`AppuiDepotJuillet.cote_citee` donne l'ancienne cote de chaque statement ; la
nouvelle vient du bordereau amendé. La table à quatre colonnes
(`§ dépôt | § amendé | ancienne cote | nouvelle cote`) devient un **rapport
généré**.

➜ **C'est un gain qualitatif, pas seulement d'effort.** Une table tenue à la
main dérive ; un rapport généré ne dérive pas, et peut être **régénéré le jour
où elles s'opposent** sous l'art. 207 — voir
[`communication_pieces.md`](communication_pieces.md) § 10.5.

## 4. ⚠️ Le danger immédiat : ne jamais modifier un `Statement` en place

Les **287 statements du document 9 sont la représentation en base de l'acte
déposé**. Les nœuds du document 9 pointent dessus.

**Éditer le texte d'un de ces statements réécrit silencieusement l'acte
déposé.** Le dépôt est gelé *sur papier* ; rien ne protège sa représentation en
base. Une réécriture menée en modifiant les statements existants détruirait le
référent contre lequel toute la concordance doit se mesurer — et le détruirait
sans trace.

**Règle, sans exception :** pour un paragraphe réécrit, **créer un nouveau
`Statement`** et le rattacher à son antécédent. Jamais `statement.text = ...` sur
un statement du document 9.

*(Garde-fou possible, à décider : un `verifier_integrite_depot` qui compare les
empreintes des 287 statements du doc 9 à un instantané gelé, sur le modèle de
`SHA256SUMS` dans `legal/depots/`.)*

## 5. ⚠️ Deux comptes différents à ne pas confondre

| Source | Compare | Résultat |
|---|---|---|
| `numerotation.py` (en-tête) | `LibraryNode.item` (n° du dépôt) **vs** n° recalculé par le schéma, sur le doc 9 | « plus de **deux cents nœuds** diffèrent » |
| `legal/amendements/01_avant_notification/verification_ancrages_paragraphes_acte_depose.md` | le `.md` de travail **vs** le **PDF imprimé** | **47 paragraphes sur 179** diffèrent |

**Ce ne sont pas les mêmes objets ni la même comparaison.** Les rapprocher
produirait un ancrage faux. Et la question de fond reste ouverte : *lequel des
cinq candidats a été imprimé* — préalable déjà signalé
(`communication_pieces.md` § 10.2 c). **L'ancrage se fixe avant la réécriture**,
parce que c'est contre lui que la concordance se mesure.

## 6. Décisions à prendre avant d'écrire une ligne de code

1. **Le FK réflexif suffit-il, ou faut-il gérer la fusion** (plusieurs § déposés
   → un § amendé) ? À trancher sur l'état réel de `legal/redaction_v2/`.
2. **Que deviennent `is_true` / `is_falsifiable`** quand un statement est
   reformulé ? Ils ne suivent pas tout seuls. Les 39 énoncés contestés
   (`contested_statements`) et les liens `AppuiDepotJuillet`, `Fait`, `Axe` sont
   portés par le **statement d'origine** : un nouveau statement part nu. Recopier
   à la dérivation, ou résoudre par remontée via `derive_de` ?
3. **Faut-il geler une empreinte des 287 statements du doc 9** avant de
   commencer (§ 4) ?

Ces trois réponses conditionnent la migration. Elles ne conditionnent pas la
réécriture elle-même, qui peut avancer — **à la seule condition de ne jamais
modifier un statement du document 9**.
