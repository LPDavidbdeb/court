# Citations atomiques et compositions — reconstructibilité

Généré par `docs/purge_quotes/decomposition_citations.py`. Lecture seule.

Une citation est **atomique** si aucune autre citation de la même source ne s'y trouve incluse. Elle est **composée** sinon. Pour chaque composition, on mesure quelle part de son texte est déjà couverte par des blocs atomiques existants : c'est le taux qui dit si elle peut être reconstruite sans rien créer.

| | |
|---|---|
| citations examinées | 310 |
| **atomiques** | **310** |
| — dont reprises comme prémisse d'une composition | 0 |
| **composées** | **0** |
| — **reconstructibles sans rien créer** | **0** |
| — exigeant la création d'au moins un bloc | 0 |

Une composition est dite **reconstructible sans rien créer** quand tout son texte se retrouve dans des blocs atomiques existants, aux liaisons près (moins de 12 caractères : ponctuation, conjonction, marqueur d'élision). Ce n'est pas un seuil de pourcentage, c'est l'absence de passage réellement manquant.

Les 0 compositions ainsi couvertes sont **redondantes** : leur contenu existe déjà, réparti en blocs simples. Elles peuvent disparaître sans perte. Les 0 autres contiennent des passages qui ne sont dans aucun bloc — rendus verbatim ci-dessous, ce sont exactement les blocs à créer.

---

## 1. Compositions reconstructibles sans rien créer (0)

Supprimer ces compositions ne fait perdre aucun texte : tout leur contenu existe déjà en blocs atomiques.

| id | source | longueur | couverture | parties atomiques | trames |
|---|---|---|---|---|---|

## 2. Compositions incomplètes (0)

Chacune porte un ou plusieurs passages absents de tout bloc atomique. Le texte de ces manques est donné tel quel : c'est le contenu des blocs à créer pour rendre la composition reconstructible — après quoi elle devient elle aussi supprimable.

---

## 3. Blocs atomiques servant de prémisse (0)

Ces blocs sont corrects tels quels. Ils sont listés parce qu'une ou plusieurs compositions les répètent — c'est la redondance à supprimer.

| id | source | longueur | repris dans | trames |
|---|---|---|---|---|

## 4. Blocs atomiques isolés (310)

Atomiques et repris par aucune composition : rien à faire.
