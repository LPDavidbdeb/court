# Un agent de vérification avant envoi — faisabilité, conception, et une mise en garde

> **Idée du demandeur, 13 octobre 2026** : un agent, ou une compétence d'agent,
> qui vérifie l'historique des communications entre les parties avant chaque
> envoi, en tenant compte de l'ensemble des étapes du processus — celles qui sont
> déterminées d'avance, celle où nous sommes, celles à venir. *« Il m'apparaît
> que nous sommes dans un jeu : nous jouons chacun notre tour, notre réponse
> dépend de celle de l'autre joueur et des règles qui gèrent le jeu. »*
>
> **Réalisable : oui, et moins cher qu'il n'y paraît — l'essentiel des entrées
> existe déjà.** Le cadre est juste : le processus est structuré et prévisible,
> les étapes se succèdent, et **l'issue ne dépend pas du demandeur seul**. Ses
> décisions tiennent compte de ce que l'autre a fait et de ce qu'on peut
> anticiper, dans les règles.
>
> Les étapes elles-mêmes sont désormais écrites :
> [`carte_de_l_instance.md`](carte_de_l_instance.md).

---

## 1. Le cadre du jeu — où il tient

Ce n'est pas une métaphore commode : la procédure civile **est** un jeu fini, et
quatre de ses propriétés sont littérales.

| Propriété | Dans l'instance |
|---|---|
| **Tour par tour** | chaque acte appelle une réponse, et ouvre un délai |
| **Règles énumérées** | le C.p.c. nomme les coups : contester, amender, s'opposer, demander le rejet, inscrire |
| **États ordonnés** | dépôt → signification → réponse → protocole → mise en état → inscription → instruction |
| **Information presque complète** | le plumitif et la correspondance sont partagés ; peu de coups sont cachés |

À cela s'ajoute ce qui fait vraiment un jeu : **les coups forcés**. Un délai qui
expire joue à votre place.

## 2. Ce qui existe déjà — l'agent n'aurait presque rien à inventer

| Élément du jeu | Où il vit aujourd'hui |
|---|---|
| **État courant et horloges** | [`echeancier.md`](echeancier.md) |
| **Historique des coups** | [`journal.md`](journal.md), `entrants/`, et la table `Email` |
| **Lecture des coups adverses** | `analyses/`, une fiche par prétention |
| **Coups prévisibles de l'adversaire** | [`pieges.md`](pieges.md) § A, par ordre de probabilité |
| **Prochain point de décision** | [`protocole_instance.md`](protocole_instance.md) |
| **Ce qui ne se concède jamais** | `pieges.md` § D, liste fermée |
| **Contrôles mécaniques** | `preparer_transmission` (adresse, copie croisée, empreintes, refroidissement) |
| **Qui reçoit, et où, à quelle date** | `DestinataireInstance`, avec ses fenêtres de validité |

**Deux choses manquent, et une seule est du travail.**

## 3. Ce qu'il faudrait construire

### 3.1 La carte des étapes — ✅ faite le 13 octobre

[`carte_de_l_instance.md`](carte_de_l_instance.md) donne les neuf étapes, leur
disposition au Code, leur délai, les coups ouverts à chaque partie et les coups
forcés. Elle n'a pas à être réinventée ici.

Rappel de la succession :

| État | Horloges | Nos coups | Leurs coups | Forcé |
|---|---|---|---|---|
| `DEPOSEE` | 2892 (60 j), 107 (3 mois) | signifier | — | signifier, sinon l'interruption tombe |
| `SIGNIFIEE` | réponse 15 j | communiquer les pièces | répondre, ne pas répondre | — |
| 🔵 `CONTESTEE` | **protocole 45 j** | amender, communiquer, proposer le protocole | dénoncer un moyen préliminaire, proposer le protocole | **déposer le protocole** |
| `PROTOCOLE_DEPOSE` | acceptation présumée 20 j | — | demander une gestion | — |
| `MISE_EN_ETAT` | rigueur 6 mois | interroger, amender encore | irrecevabilité, rejet pour abus | être prêt |
| `INSCRITE` | — | — | — | — |

🔵 **Nous sommes ici**, depuis le 29 septembre. Échéance du protocole :
**1er novembre**.

### 3.2 La compétence — une *skill*, pas un sous-agent

**Une *skill*, invoquée dans la session principale.** Un sous-agent démarre à
froid et redérive le contexte ; or toute la valeur tient précisément à **avoir
lu le dossier**. Le coût serait plus élevé et le résultat moins bon.

Forme : `/verifier-envoi <fichier du sortants/>`.

### 3.3 Ce que l'agent apporte que la commande ne peut pas

`preparer_transmission` fait du **mécanique** et du **lexical**. Un agent fait du
**contextuel** — c'est-à-dire exactement ce qu'une expression régulière ne peut
pas faire :

1. **La lettre répond-elle à tout ce que la leur demandait ?** Quatre demandes le
   5 octobre ; en laisser une sans réponse est un reproche gratuit.
2. **Contredit-elle un écrit antérieur ?** Il faut avoir lu tous les sortants.
3. **Est-ce le bon coup à cette étape ?** Prématuré, tardif, ou hors séquence.
4. **Concède-t-elle quelque chose de la liste fermée — en substance, pas par
   mot-clé ?** Une concession ne contient pas forcément le mot.
5. **Ouvre-t-elle une porte qu'on avait décidé de garder fermée ?** Par exemple
   caractériser l'amendement, décision expressément retirée le 8 octobre.
6. **Quel coup lui ouvre-t-on en retour ?** Chaque acte appelle une réponse ; il
   vaut mieux savoir laquelle avant d'envoyer.

## 4. Ce que l'agent vérifie, concrètement

L'office est étroit, et c'est une qualité : **savoir où l'on est, ce qu'on doit,
et ce que l'écrit qui part expose.** Il ne touche pas au fond — la thèse se
travaille ailleurs, dans `legal/` et `redaction_v2/`.

### 4.1 Contre l'étape

Un écrit ne se juge pas dans l'abstrait mais **contre l'étape où il paraît**
([`carte_de_l_instance.md`](carte_de_l_instance.md)).

- Ce que l'étape **oblige** à faire est-il fait ? *(Au 13 octobre : l'art. 147
  al. 3 oblige à informer chaque partie des réponses reçues et du nom des
  avocats. Obligation qui, au 13 octobre, avait couru **quatorze jours** sans être
  remplie — exactement le genre d'écart qu'une vérification contre l'étape
  attrape.)*
- L'écrit est-il **prématuré** ? Engage-t-il sur un point qui se décide à
  l'étape suivante ?
- Fait-il courir ou expirer un délai, et lequel ?

### 4.2 Contre l'historique

- Répond-il à **tout** ce que leur dernier écrit demandait ? *(Quatre demandes
  le 5 octobre ; en laisser une sans réponse est un reproche gratuit.)*
- **Contredit-il** un écrit antérieur ? Il faut avoir lu tous les sortants, pas
  seulement le dernier.
- Rouvre-t-il une question **tranchée** ? *(La caractérisation de l'amendement a
  été retirée le 8 octobre. La réintroduire par inadvertance annulerait la
  décision sans que personne ne le remarque.)*

### 4.3 Contre l'anticipation

C'est le volet proprement interdépendant, et il ne cherche pas un avantage : il
cherche à **ne pas être surpris**.

- **Quel coup cet écrit leur ouvre-t-il ?** Chaque acte appelle une réponse ;
  mieux vaut savoir laquelle avant d'envoyer que de la découvrir.
- Le coup qu'on anticipe d'eux à cette étape est-il **prévu** ?
  `pieges.md` § A les classe par probabilité ; la carte les rattache à l'étape
  où ils peuvent survenir.
- Quelque chose dans l'écrit **facilite-t-il** un de ces coups ?

### 4.4 Contre la liste fermée

`pieges.md` § D, mais **en substance plutôt que par mot-clé** — une concession ne
contient pas forcément le mot. C'est ce qu'une expression régulière ne peut pas
faire, et c'est la raison d'être de l'agent à côté de `preparer_transmission`.

## 5. La contrainte non négociable : il signale, il ne dédouane jamais

La même discipline que `preparer_transmission`, et pour la même raison : **un
contrôle qui prétend couvrir un jugement humain est pire que pas de contrôle, il
rassure.**

- **Jamais de « ✅ tout est bon ».** La sortie est une liste de constats et de
  questions, pas un feu vert.
- **L'agent n'atteste pas.** Les cinq attestations de `sortants/README.md`
  restent celles du demandeur, portées à son nom. *(Cette règle a une histoire :
  elle a été enfreinte une fois, le 13 octobre, lors d'un essai de la commande ;
  la ligne a été supprimée le jour même.)*
- **Il travaille en amont, pas à la place.** Sa sortie se lit **avant** de porter
  les attestations — elle les éclaire, elle ne les remplace pas.

## 6. L'ordre de construction

| Étape | Effort | Quand |
|---|---|---|
| 1. La machine à états en un fichier | le seul vrai travail | utile **avant le 1er novembre** : elle sert au protocole |
| 2. La *skill* `/verifier-envoi` | modeste — elle lit ce qui existe | après |
| 3. Rendre `journal.md` lisible par machine | optionnel | seulement si le reste sert |

⚠️ **Et la question du moment.** Le protocole est au 1er novembre, la réécriture
est le chemin critique, et deux lettres attendent d'être envoyées. L'étape 1 a un
rendement propre — elle oblige à écrire noir sur blanc ce qu'on doit, et quand —
mais l'étape 2 peut attendre que les lettres soient parties.

➜ **Rien n'est implémenté. Ce fichier est une conception, pas un chantier
ouvert.**
