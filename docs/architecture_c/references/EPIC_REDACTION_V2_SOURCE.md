# EPIC — Rédaction d'actes judiciaires, cotation chronologique et versionnement probatoire

**Version :** 2 — Proposition de conception  
**Dépôt :** `LPDavidbdeb/court`  
**Référence examinée :** `main`, commit `34bc98ac9132b1`  
**Statut :** Cahier fonctionnel, développement non autorisé

## 1. Finalité

Faire évoluer l'application existante pour permettre à l'utilisateur de construire un raisonnement juridique appuyé par la preuve, de rédiger les faits d'un acte judiciaire et de produire automatiquement les documents et pièces correspondants.

La collecte et la conservation de la preuve sont considérées comme des fonctionnalités existantes à préserver.

La nouvelle fonctionnalité doit intégrer la rédaction, l'utilisation des preuves, la préparation des pièces, leur cotation chronologique et la conservation des versions successives.

## 2. Invariants architecturaux

### INV-01 — Identité permanente des sources

Chaque élément probatoire possède une identité stable déterminée par son modèle et sa clé primaire.

Cette identité ne dépend ni de la rédaction d'un acte, ni des pièces produites, ni des cotes attribuées.

La base documentaire originale demeure indépendante des structures de raisonnement et de production.

### INV-02 — Distinction entre source et pièce produite

Un élément probatoire n'est pas nécessairement une pièce procédurale.

Une pièce produite peut correspondre à un document complet, à une sélection de passages ou à un assemblage documentaire.

Le système doit donc distinguer les sources documentaires de leur composition en pièces produites.

Les règles d'identité, de regroupement et de réutilisation des pièces composites doivent être définies explicitement.

### INV-03 — Chaîne de justification

Le système doit permettre de parcourir la chaîne :

Paragraphe d'allégation → Démonstration → Preuve → Élément probatoire → Source.

La démonstration décrit le raisonnement permettant d'appuyer une proposition. La preuve organise les éléments utilisés pour la soutenir.

Les relations peuvent être réutilisées dans plusieurs démonstrations sans dupliquer les sources.

### INV-04 — Cotation chronologique intégrale

Chaque version de travail calcule ses cotes à partir des seules pièces retenues pour sa production.

Le classement est chronologique, déterministe et reproductible.

Toute insertion, suppression ou modification de l'ensemble des pièces produites entraîne une nouvelle évaluation de l'ordre et des cotes.

Les cotes d'une version ne sont pas des identifiants universels.

### INV-05 — Immutabilité des versions figées

Une version figée conserve son texte, sa structure, ses démonstrations, ses utilisations probatoires, son bordereau, sa cotation et ses artefacts documentaires.

Une nouvelle version ne modifie aucune de ces informations historiques.

Le gel doit préserver le contenu effectivement figé, et non uniquement des pointeurs vers des objets de travail susceptibles de changer ultérieurement.

### INV-06 — Concordance entre versions

Toute nouvelle version figée permet de produire une correspondance complète entre ses pièces et celles des versions antérieures.

Les correspondances sont établies à partir de l'identité des pièces et de leur composition documentaire, jamais à partir de la seule valeur des cotes.

### INV-07 — Conservation des archives historiques

Le dépôt du 24 juillet 2026 et ses cotes originales sont préservés comme état historique.

La nouvelle politique de recotation ne réécrit pas ce dépôt. Elle s'applique aux nouvelles versions et conserve les correspondances avec la version historique.

### INV-08 — Une seule source de vérité pour la production

La rédaction, le bordereau, les références dans le texte, les noms des fichiers et le cahier des pièces doivent découler du même état de version et du même calcul de cotation.

Aucun de ces artefacts ne doit posséder une attribution parallèle et indépendante des cotes.

---

## 3. User stories proposées

### US-01 — Gestion des actes et de leurs versions

**En tant qu'utilisateur**, je veux créer un acte judiciaire, le rédiger et conserver ses versions successives.

**Critères d'acceptation**

- AC01 — Un dossier contient plusieurs actes.
- AC02 — Chaque acte possède une identité permanente.
- AC03 — Chaque acte peut posséder plusieurs versions.
- AC04 — Une seule version de travail active est permise par parcours de rédaction, sauf gestion explicite de branches.
- AC05 — Une version de travail peut être créée à partir d'une version figée.
- AC06 — Chaque version connaît son acte, son état et son antécédent.
- AC07 — Une version figée n'est plus modifiable.

### US-02 — Rédaction structurée des faits

**En tant qu'utilisateur**, je veux rédiger et réorganiser les paragraphes de mon acte sans perdre les liens avec les preuves qui les soutiennent.

**Critères d'acceptation**

- AC01 — Les paragraphes peuvent être créés, modifiés, déplacés et retirés.
- AC02 — Chaque occurrence possède une identité stable indépendante de son numéro affiché.
- AC03 — La numérotation est calculée selon l'ordre documentaire.
- AC04 — Un même contenu réutilisable peut apparaître dans différents contextes sans imposer un numéro unique.
- AC05 — Les opérations de rédaction préservent les liens de justification.
- AC06 — Les paragraphes d'une version figée sont conservés avec leur texte et leur position historique.

### US-03 — Construction des démonstrations et preuves

**En tant qu'utilisateur**, je veux construire les démonstrations qui soutiennent mes allégations à partir de la preuve conservée.

**Critères d'acceptation**

- AC01 — Un paragraphe peut être soutenu par plusieurs démonstrations.
- AC02 — Une démonstration peut utiliser plusieurs preuves.
- AC03 — Une preuve peut organiser plusieurs éléments probatoires.
- AC04 — Un élément peut être réutilisé sans duplication de sa source.
- AC05 — Les rôles probatoires et les limites d'un appui peuvent être conservés.
- AC06 — L'application distingue la justification interne du texte destiné à être plaidé.
- AC07 — Une version figée conserve l'état des démonstrations et des preuves qu'elle mobilise.

### US-04 — Détermination des pièces à produire

**En tant qu'utilisateur**, je veux que les pièces documentaires nécessaires soient déterminées à partir de l'utilisation de la preuve dans l'acte.

**Critères d'acceptation**

- AC01 — Le système détermine les sources impliquées dans les utilisations probatoires de la version.
- AC02 — Les règles de production identifient les unités documentaires correspondantes.
- AC03 — Une utilisation répétée ne crée pas automatiquement plusieurs copies d'une même pièce.
- AC04 — Les citations et passages restent reliés à leurs sources.
- AC05 — Les liasses et assemblages conservent leurs composantes et leur ordre.
- AC06 — L'utilisateur peut distinguer les preuves exploitées à des fins analytiques de celles destinées à la production.
- AC07 — Une pièce sans utilisation pertinente n'est pas ajoutée automatiquement au bordereau.

### US-05 — Cotation chronologique dynamique

**En tant qu'utilisateur**, je veux que le système ordonne et recote automatiquement les pièces pendant la rédaction.

**Critères d'acceptation**

- AC01 — Le périmètre de calcul est l'ensemble des pièces retenues pour la version.
- AC02 — L'ordre chronologique est déterminé par une règle unique.
- AC03 — Les dates manquantes, incertaines ou atemporelles reçoivent un traitement explicite.
- AC04 — Les égalités de date sont départagées de manière déterministe.
- AC05 — L'insertion d'une pièce recalcule les cotes concernées.
- AC06 — Le retrait d'une pièce provoque le recalcul.
- AC07 — Le recalcul ne modifie jamais les associations d'une version figée.
- AC08 — Les règles de classement sont identiques pour l'interface, le bordereau et l'exportation.
- AC09 — Les filtres d'affichage ne modifient pas la cotation de référence.

### US-06 — Référencement automatique dans le texte

**En tant qu'utilisateur**, je veux que les renvois aux pièces demeurent exacts même après une recotation.

**Critères d'acceptation**

- AC01 — Les références internes désignent une identité stable.
- AC02 — La cote affichée est obtenue à partir de la cotation de la version.
- AC03 — Toute recotation actualise les références du brouillon.
- AC04 — Les références aux sous-cotes et aux liasses sont prises en charge.
- AC05 — Une référence non résolue est détectée.
- AC06 — Aucune référence périmée ne peut subsister silencieusement dans une exportation validée.
- AC07 — Les références figées sont restituées selon leur version historique.

### US-07 — Gel d'une version et de son dossier probatoire

**En tant qu'utilisateur**, je veux figer une version complète et vérifiable de mon acte.

**Critères d'acceptation**

- AC01 — Le texte et sa structure sont conservés.
- AC02 — Les démonstrations, preuves et utilisations sont conservées dans leur état de version.
- AC03 — Le bordereau et les associations pièce–cote sont enregistrés.
- AC04 — Les paramètres chronologiques ayant déterminé l'ordre sont conservés.
- AC05 — Les fichiers produits sont vérifiables par des empreintes d'intégrité.
- AC06 — Une erreur de validation empêche la finalisation.
- AC07 — Le système ne publie jamais un dossier partiellement finalisé.
- AC08 — Le gel logique en base et la publication des fichiers suivent un protocole garantissant la cohérence, y compris en cas d'échec.
- AC09 — Une fois figée, la version ne peut être modifiée rétroactivement.

### US-08 — Concordance exhaustive entre versions

**En tant qu'utilisateur**, je veux pouvoir retrouver les anciennes et nouvelles cotes des pièces afin d'interpréter les références contenues dans n'importe quelle version de l'acte.

**Critères d'acceptation**

- AC01 — La concordance compare deux versions explicitement identifiées.
- AC02 — Elle couvre toutes les pièces des deux versions.
- AC03 — Elle distingue les pièces conservées, ajoutées et retirées.
- AC04 — Elle identifie les changements de cote.
- AC05 — Elle reconnaît qu'une même cote peut désigner deux pièces différentes dans deux versions.
- AC06 — Elle traite les sous-cotes, les liasses et les changements de composition.
- AC07 — Les correspondances non univoques sont signalées.
- AC08 — La concordance repose sur les états historiques figés.
- AC09 — Elle peut être consultée et exportée.
- AC10 — Le système peut retrouver l'historique des cotes d'une pièce à travers toutes les versions où elle apparaît.

### US-09 — Génération du bordereau

**En tant qu'utilisateur**, je veux générer le bordereau directement à partir de la cotation de la version.

**Critères d'acceptation**

- AC01 — Le bordereau ne nécessite aucune ressaisie manuelle des cotes.
- AC02 — Il contient exactement les pièces retenues pour la production.
- AC03 — Son ordre et ses cotes correspondent au calcul de référence.
- AC04 — Les descriptions sont reliées aux identités des pièces.
- AC05 — Les liasses et sous-cotes sont correctement représentées.
- AC06 — Le bordereau d'une version figée peut être restitué à l'identique.

### US-10 — Production et exportation des pièces

**En tant qu'utilisateur**, je veux produire un dossier documentaire contenant les pièces nommées selon les cotes attribuées.

**Critères d'acceptation**

- AC01 — L'exportation utilise la cotation de la version sélectionnée.
- AC02 — Chaque pièce possède un fichier ou un ensemble de fichiers explicitement représenté dans le manifeste.
- AC03 — Les noms des fichiers reflètent les cotes.
- AC04 — Toutes les composantes d'une pièce composite sont conservées.
- AC05 — Le dossier comprend le bordereau correspondant.
- AC06 — Le dossier comprend un manifeste des identités, cotes et empreintes.
- AC07 — Les fichiers sources originaux ne sont jamais modifiés.
- AC08 — Une exportation historique ne recalcule pas les cotes.
- AC09 — Les erreurs de rendu ou de correspondance sont détectées.
- AC10 — L'exportation d'une version figée est reproductible et vérifiable.

### US-11 — Création d'une version amendée

**En tant qu'utilisateur**, je veux modifier un acte déjà figé et recalculer l'ensemble des cotes en conservant les références de sa version antérieure.

**Critères d'acceptation**

- AC01 — L'utilisateur peut créer une nouvelle version de travail depuis une version figée.
- AC02 — Il peut ajouter ou retirer des paragraphes, démonstrations, preuves et pièces.
- AC03 — Le bordereau est intégralement recalculé.
- AC04 — Les renvois aux pièces sont actualisés.
- AC05 — La version précédente reste intacte.
- AC06 — La nouvelle version conserve une référence à son antécédent.
- AC07 — Le gel produit une concordance avec les versions pertinentes.

### US-12 — Historique de dépôt et de communication

**En tant qu'utilisateur**, je veux associer chaque dépôt ou communication à la version réellement concernée.

**Critères d'acceptation**

- AC01 — Une communication désigne une version identifiée.
- AC02 — Les dates, destinataires et modalités de communication sont conservés.
- AC03 — Les fichiers transmis sont identifiés par leur nom et leur empreinte.
- AC04 — Une même version peut faire l'objet de plusieurs communications.
- AC05 — Les événements de dépôt et de communication sont distincts du gel.
- AC06 — Les communications papier peuvent être documentées sans supposer automatiquement une identité parfaite avec un fichier numérique.

---

## 4. Contrat transversal — Exemple de recotation

Version V1 :

| Identité | Date | Cote V1 |
|---|---|---|
| A | 2013-06-10 | P-1 |
| B | 2014-03-05 | P-2 |
| C | 2015-04-20 | P-3 |

La version V1 est figée.

L'utilisateur crée V2, ajoute une pièce D datée de 2012 et retire B.

Version V2 :

| Identité | Date | Cote V2 |
|---|---|---|
| D | 2012-01-15 | P-1 |
| A | 2013-06-10 | P-2 |
| C | 2015-04-20 | P-3 |

Table de concordance :

| Identité | Cote V1 | Cote V2 | Statut |
|---|---|---|---|
| A | P-1 | P-2 | Recotée |
| B | P-2 | — | Retirée |
| C | P-3 | P-3 | Inchangée |
| D | — | P-1 | Ajoutée |

Ce scénario démontre qu'une concordance ne peut pas être fondée sur la valeur des cotes.

La cote P-1 de V1 désigne A, alors que la cote P-1 de V2 désigne D.

La cote P-3 désigne C dans les deux versions, mais cette égalité n'est qu'une conséquence du classement.

Les correspondances doivent être établies à partir des identités permanentes.

---

## 5. Architecture logique à étudier

Les responsabilités suivantes doivent être représentées, sans préjuger du nombre exact de modèles Django :

| Concept | Responsabilité |
|---|---|
| `Acte` | Identité permanente de l'acte |
| `VersionActe` | État de rédaction ou état historique figé |
| `OccurrenceParagraphe` | Position et contenu du paragraphe dans la version |
| `Demonstration` / `Preuve` | Structures de justification et de réutilisation |
| `UtilisationProbatoire` | Relation entre le contenu plaidé et ses appuis |
| `PieceProduite` | Identité de l'unité documentaire produite |
| `CotationVersion` | Association figée entre version, pièce et cote |
| `ArtefactVersion` | Document, bordereau, pièce, manifeste et empreinte |
| `Communication` | Historique des dépôts et transmissions |

Ces noms sont des concepts de conception, pas une prescription de nouvelles tables.

L'architecte doit d'abord examiner les modèles existants et déterminer quelles responsabilités peuvent être réutilisées ou étendues.

## 6. Contraintes de compatibilité

Le développement doit préserver :

- Les sources et leurs clés primaires.
- Les données déjà rattachées aux modèles de preuve.
- Les documents reproduits et produits.
- Les archives du dépôt historique.
- Les correspondances historiques pièce–cote.
- Les moteurs de rendu existants, lorsque compatibles.
- Les fonctions de contrôle et d'audit déjà opérationnelles.

Les scripts qui reconstruisent des répertoires ou des tables de travail ne doivent jamais recevoir comme cible un état figé.

## 7. Tests transversaux minimaux

T01 — Ajout chronologique avant toutes les pièces existantes.

T02 — Ajout entre deux pièces et mise à jour des renvois.

T03 — Retrait d'une pièce utilisée plusieurs fois, avec conservation tant qu'une utilisation demeure.

T04 — Retrait définitif d'une pièce et recalcul complet.

T05 — Insertion de deux pièces de même date, avec ordre déterministe.

T06 — Pièce sans date, date incertaine et pièce atemporelle.

T07 — Gel V1, modification du brouillon V2 et vérification de l'intégrité de V1.

T08 — Concordance V1–V2 couvrant ajouts, retraits et recotations.

T09 — Même cote, pièces différentes selon les versions.

T10 — Pièce composite ou liasse dont les composantes changent.

T11 — Échec du gel après préparation des fichiers, sans publication partielle.

T12 — Réexportation d'une version historique sans recalcul.

T13 — Correspondance exacte entre renvois dans l'acte, bordereau, fichiers et manifeste.

T14 — Préservation intégrale des associations du dépôt du 24 juillet 2026.

## 8. Travaux préalables au développement

L'agent architecte devra produire :

1. Un inventaire des modèles et services existants réutilisables.
2. Une analyse des différences entre le code de `main` et les travaux non encore intégrés.
3. Une définition de l'identité d'une pièce simple ou composite.
4. Un contrat unique de classement et de cotation chronologiques.
5. Une proposition de conservation des versions et de leurs artefacts.
6. Une stratégie de migration additive protégeant la base existante.
7. Une analyse des risques de suppression, modification et désynchronisation.
8. Une décomposition technique des user stories, de leurs dépendances et de leurs tests.

Aucune migration de la base réelle ni modification des archives historiques ne doit être effectuée pendant cette phase de conception.