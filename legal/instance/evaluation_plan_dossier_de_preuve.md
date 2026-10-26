# Plan de préparation du dossier de preuve — angles morts

> **Demande du 26 octobre 2026** : n'envoyer que les **fils de courriels au
> complet** ; développer un script s'appuyant sur le bordereau, la table de
> correspondance en base et la requête ; vérifier d'abord le rapprochement
> pièce ↔ cote ; sauvegarder chaque pièce sous son numéro de cote ; puis faire
> valider par un agent le lien entre le paragraphe et le contenu de la pièce.
>
> **Évaluation seulement. Rien n'est implémenté.**
>
> **Le plan est bon.** Les trois sources retenues sont les bonnes autorités, la
> sauvegarde par cote est ce dont le destinataire a besoin, et la validation
> paragraphe ↔ contenu est le seul contrôle qui prouve quelque chose.
>
> ⚠️ **Deux objections de la première version étaient fausses** — § 1, conservé
> et nommé. Ce qui reste : **une exclusion dure** (§ 4), **un contrôle plus fort
> que celui prévu** (§ 5) et **deux décisions à prendre** (§ 11).

---

## 1. ❌ RETIRÉ — deux objections fausses, corrigées le 26 octobre

Une première version de cette fiche opposait deux obstacles au plan. **Les deux
étaient faux.** Ils sont conservés ici, nommés, parce qu'un angle mort inventé
coûte du temps comme un vrai.

### 1.1 « Les fils au complet redéfiniraient 39 cotes » — hors sujet

J'avais lu « envoyer les fils au complet » comme un remplacement de la cote par
son fil. **Ce n'est pas le plan** : le plan est d'envoyer **la pièce**, entière
plutôt qu'en extrait, le fil servant à la localiser. La cote reste la cote, le
verrou n'est pas touché, et le plan est aligné sur ce qui est coté.

**Ce qui subsiste, et qui est une simple question d'emballage** : trois formes de
cote coexistent et le script doit les distinguer —

| Forme | Occurrences | Unité livrée |
|---|---|---|
| `email:<pk>` | 39 | un `.eml` |
| `email:<pk>,<pk>,…` | liasses (ex. P-30 = `email:485,486`) | plusieurs `.eml` sous une cote |
| `thread:<pk>` | 4 | le fil, car **c'est le fil qui est coté** |

### 1.2 « Le corpus de fils est amputé » — faux, et l'erreur est récurrente

J'avais tiré de la note [[reference_corpus_courriel_unilateral]] que 40 fils
seraient « troués ». **La note dit exactement l'inverse**, en toutes lettres :

> ⚠️ « **Ce n'est PAS une lacune de contenu.** La conversation est complète : les
> messages adverses sont là, dans la chaîne citée. […] **Ne jamais en tirer qu'un
> fil serait "troué"** […] *(Erreur commise le 21 septembre 2026 […].)* »

**Elle nomme l'erreur, et je l'ai refaite** — le 26 octobre. Deuxième occurrence.

**Vérification en base, sur les 43 cotes adossées à un courriel ou à un fil :**

| | Cotes |
|---|---|
| **Bilatérales** — les deux parties figurent comme expéditeurs | **31** |
| **LP + chaîne citée** — ses envois, portant les propos adverses dans l'historique | **7** |
| **LP seul, sans chaîne** | **5** |

➜ **38 des 43 portent les mots de l'autre partie.** Et les cinq restantes ne sont
pas des conversations amputées : ce sont des **messages sortants uniques** —
P-3 (lettre à Me Pringle, son propre avocat), P-25 et P-30 (lettres à Me Ayoub),
P-44, P-73. **Une lettre qu'on écrit n'a pas d'« autre côté » manquant ; elle est
complète parce qu'elle est entière.**

➜ **Aucun marqueur d'unilatéralité n'est requis.** La note ajoute d'ailleurs
qu'« aucun des passages concernés ne figure dans l'acte déposé ni au bordereau du
24 juillet 2026 » : la question d'attribution ne touche pas les pièces communiquées.

## 3. ⚠️ « Sans conversion ni réencodage » : un fil natif, c'est N fichiers

Ce qui a été promis aux deux défenderesses le 16 octobre :

> « le fichier source conservé sera transmis dans son format électronique,
> **sans conversion ni réencodage aux fins de sa communication**, accompagné,
> lorsque nécessaire, d'un rendu lisible. »

Pour un courriel, le fichier source est le `.eml`. **Un fil natif est donc N
fichiers `.eml`, pas un document.** Exporter un fil en PDF unique serait une
conversion — exactement ce qui a été exclu.

Conséquences sur le plan :

- « sauvegarder la pièce sous son numéro de cote » donne un **dossier** par cote,
  pas un fichier. *(C'est peut-être déjà l'intention — à confirmer.)*
- Le manifeste doit porter **une empreinte par fichier**, pas une par cote.
- Le rendu lisible s'ajoute au natif ; il ne le remplace pas.

## 4. ⚠️ Trois cotes ne doivent jamais être générées par le script

`METHODOLOGIE_POST_DEPOT.md` § 9.2 : pour les **actes incriminés**, l'original
s'impose (art. 2860 C.c.Q.), et le rendu depuis le modèle « **ne remplace pas
l'original pour la communication** ».

| Cote | Objet |
|---|---|
| **P-19** | Requête du 19 nov. 2015 |
| **P-40** | Dénonciation du 21 juil. 2023 |
| **P-42** | Déclaration assermentée du 21 oct. 2019 |

Les originaux sont en main (`media/evidence_files/`, `Document.file_source`).
➜ **Exclusion dure à inscrire dans le script**, sans quoi il produira exactement
ce qui ne doit pas partir. Même traitement pour **P-58 à P-64** (placeholders) et
**P-106** (non assemblée).

## 5. Une vérification plus forte que celle prévue, et gratuite

Le plan vérifie **bordereau ↔ cote**. C'est une vérification de cohérence
interne : elle prouve que la description et le numéro concordent, pas que le
fichier est le bon.

`cotes.lock.json` porte déjà, par cote, `source_resolue` (model:pk),
`fichier_appui` et **`sha256_assemble`**. Donc :

| Contrôle | Ce qu'il prouve |
|---|---|
| bordereau ↔ cote *(prévu)* | la description correspond au numéro |
| **cote ↔ source en base** (`model:pk`) | le numéro désigne le bon objet — [[feedback_referencing_cotes]] : vérifier par le **contenu**, jamais par le numéro |
| **fichier sur disque ↔ `sha256_assemble`** | le fichier est **celui qui a été assemblé au dépôt**, et il n'a pas bougé |

Le troisième est le seul qui détecte une dérive silencieuse, et il ne coûte rien.

## 6. L'agent paragraphe ↔ contenu : utile, mais un tiers existe déjà

**Ce qui existe.** `AppuiDepotJuillet` porte **515 lignes** statement → cote
citée, et la commande `verifier_appuis_depot` compare déjà ce que la prose
invoque à ce que la base sait, en trois écarts : NON PERSISTÉ, NON CITÉ,
ORPHELINE. L'agent ne bâtit donc pas le lien — **il le qualifie**.

**Ce que l'agent ajoute, et que rien d'autre ne peut faire** : *la pièce
soutient-elle ce pour quoi elle est citée ?* Un lien peut exister en base, être
cohérent, et ne rien prouver.

**Deux contraintes.**

⚠️ **a) Contre quel acte ?** Les paragraphes de l'acte déposé vont être
renumérotés et réécrits. Valider contre l'acte déposé maintenant, c'est un
travail à refaire ; valider contre l'acte modifié, c'est attendre qu'il existe.
**Trancher avant d'écrire une ligne.** *(La voie économique : valider contre les
`Statement`, qui survivent à la renumérotation — `suivi_paragraphes_en_base.md`.)*

⚠️ **b) Il signale, il ne dédouane pas.** Même discipline que
`preparer_transmission` : pas de « ✅ le lien tient ». Un contrôle qui prétend
couvrir un jugement est pire que pas de contrôle.

## 7. Le périmètre : 43 cotes sur 106

Le plan est centré sur les courriels. Ils comptent pour **43 cotes** (39 `email`
+ 4 `thread`). Restent **63 cotes** : 29 pdf, 15 event, 5 photodoc, 4 photo,
7 chatsequence, 3 document — dont les liasses photographiques, où la
**vérification EXIF après empaquetage** est le contrôle critique
(`communication_pieces.md` § 3).

➜ Soit le script les couvre, soit c'est une **phase 1** assumée. Dans ce second
cas, le dire au destinataire plutôt que de livrer partiellement sans l'annoncer.

## 8. L'exposition des tiers — réduite par le § 1.1

L'objection supposait l'envoi de fils entiers là où la cote ne porte qu'un
courriel. Le plan n'élargissant pas les cotes, **ce qui part est ce que la cote
contenait déjà**.

Reste le cas des 4 cotes `thread:` et des liasses, où des tiers figurent
(grand-mère paternelle, procureurs antérieurs, psychologue). Ce sont des pièces
cotées et assemblées au dépôt : la question a été tranchée en les cotant.

## 9. Le calendrier — et une bonne nouvelle

| Engagement | Échéance |
|---|---|
| Premier lot à Élise | **31 octobre 2026** |
| Communication complète à Élise | 15 décembre 2026 |
| Dépôt de la proposition de protocole | **2 novembre 2026** |

✅ **Le premier lot ne dépend pas du script.** L'ordre arrêté
(`communication_pieces.md` § 8) commence par **P-40, P-42, P-19 en original**,
puis P-105 — c'est-à-dire précisément les cotes que le script ne doit **pas**
toucher (§ 4). Le lot 1 se prépare à la main, et le script sert aux suivants.

⚠️ Mais le **2 novembre** passe avant tout : c'est la seule échéance dont la
chaîne 173 → 177 → 2894 fait dépendre la survie du recours.

## 10. Ce que le plan a juste

- **Les trois sources sont les bonnes autorités** : le bordereau dit ce qui est
  promis, la base dit ce qui existe, la requête dit à quoi ça sert. Les croiser
  est exactement le bon contrôle.
- **La sauvegarde par cote** est ce dont le destinataire a besoin pour lire la
  demande en tenant les pièces.
- **Procéder par tests** suit le motif déjà en place dans le dépôt
  (`verifier_*`, `audit_*`) : des commandes qui **constatent** sans corriger.
- **La validation paragraphe ↔ contenu** est le seul contrôle qui prouve autre
  chose que de la cohérence formelle. C'est la bonne idée du plan.

## 11. Ordre suggéré

1. **Trancher le § 1** — voie A ou voie B. Tout le reste en dépend.
2. **Trancher le § 6 a** — valider contre quoi.
3. Le contrôle `sha256_assemble` du § 5 — quelques lignes, détecte les dérives.
4. L'extraction par cote, avec les exclusions dures du § 4 et le marqueur
   d'unilatéralité du § 2.
5. L'agent du § 6, en dernier.

➜ **Rien n'est implémenté. Les points 1 et 2 sont des décisions, pas du code.**
