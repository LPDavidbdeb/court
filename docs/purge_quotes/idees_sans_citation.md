# Idées sans citation — appariements candidats

Généré par `docs/purge_quotes/idees_sans_citation.py`. Lecture seule.

Objectif : ne pas laisser une idée non étayée quand une citation existe en base pour l'appuyer. Chaque entrée met un **paragraphe non étayé** du corpus en regard d'une **citation disponible**, avec les termes distinctifs qui les rapprochent.

Le score n'établit pas la pertinence : c'est un **ordre de lecture**. Un terme rare partagé peut relever du hasard ; c'est à la lecture que se décide si la citation étaye vraiment l'idée.

| | |
|---|---|
| fichiers `.md` parcourus | 490 |
| paragraphes-idées (≥ 15 mots, hors verbatim/tableaux/titres) | 10011 |
| dont **étayés** (citation, cote P-n, renvoi, ou bloc verbatim suivant) | 3336 (33 %) |
| dont **verbatim** (le paragraphe reproduit une citation ≥ 35%) | 59 |
| dont **idées non étayées** | **6616** (66 %) |
| citations indexées | 312 |
| paires au-dessus du seuil (score ≥ 8.0) | 240 |
| paragraphes concernés | 138 |

---

## Appariements, par score décroissant (les 150 premiers)

### 1. `legal/compilation_griefs.md` ligne ~1251 → `pq-99`

- **rang** 15.6 = score 25.3 × couverture 62%
- **termes partagés** : `dentaire`, `avr`, `fournisseur`, `juil`, `transactions`, `fév`, `oct`, `type`, `dimanche`
- **source de la citation** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 6. Les relevés d'assurance (Industrielle Alliance, 2015-2016) documentent **douze transactions par Paiement Direct au fournisseur (type P)** au nom des enfants, entre le 25 février 2015 et le 16 mai 2016, **toutes en dehors du dimanche** :
>    - **2015** : 25 fév. (mer., Nicolas), 16 avr. (jeu., Nicolas), 4 mai (lun., Nicolas), 7 juil. (mar., Alexia - dentaire), 17 sept. (jeu., Alexia), 1er oct. (jeu., Nicolas), 17 oct. (sam., Nicolas - fait 1).
>    - **2016** : 11 jan. (lun., Nicolas - fait 10), 10 fév. (mer., Nicolas), 27 fév. (sam., Nicolas), 4 mai (mer., Nicolas), 16 mai (lun., Alexia).

**Citation disponible :**

```text
Transactions 2015 — Paiements directs au fournisseur (type P) : 25 fév (Nicolas/Santé), 16 avr (Nicolas/Santé), 4 mai (Nicolas/Santé), 7 juil (Alexia/Dentaire), 17 sep (Alexia/Santé), 1 oct (Nicolas/Santé), 17 oct (Nicolas/Santé). Toutes hors dimanche.
```

### 2. `legal/analyse/Responsabilité Déonthologique/2013 juin.md` ligne ~566 → `pq-72`

- **rang** 12.5 = score 18.9 × couverture 66%
- **termes partagés** : `comité`, `consultatif`, `barreau`, `jeunesse`, `droit`, `québec`
- **source de la citation** : pdf-8 p.2 — Commission spéciale sur les droits des enfants et la protect — trames 48, 55

**Idée non étayée :**

> Me Ayoub est avocate spécialisée en droit de la jeunesse et membre du Comité consultatif en droit de la jeunesse du Barreau du Québec. Les effets documentés d'une rupture brutale de la relation père-enfant sur le développement affectif de l'enfant sont connus et enseignés tant en droit qu'en sciences du développement de l'enfant.

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de son Comité consultatif en droit de la jeunesse : Me Marie-Josée Ayoub
```

### 3. `legal/analyse/Responsabilité Déonthologique/2013 juin.md` ligne ~566 → `pq-70`

- **rang** 12.5 = score 18.9 × couverture 66%
- **termes partagés** : `comité`, `consultatif`, `barreau`, `jeunesse`, `droit`, `québec`
- **source de la citation** : pdf-8 p.2 — Commission spéciale sur les droits des enfants et la protect — trames 62

**Idée non étayée :**

> Me Ayoub est avocate spécialisée en droit de la jeunesse et membre du Comité consultatif en droit de la jeunesse du Barreau du Québec. Les effets documentés d'une rupture brutale de la relation père-enfant sur le développement affectif de l'enfant sont connus et enseignés tant en droit qu'en sciences du développement de l'enfant.

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de son Comité consultatif en droit de la jeunesse : Me Marie-Josée Ayoub
```

### 4. `legal/analyse/Responsabilité Déonthologique/2013 juin.md` ligne ~620 → `pq-72`

- **rang** 12.5 = score 18.9 × couverture 66%
- **termes partagés** : `comité`, `consultatif`, `barreau`, `jeunesse`, `droit`, `québec`
- **source de la citation** : pdf-8 p.2 — Commission spéciale sur les droits des enfants et la protect — trames 48, 55

**Idée non étayée :**

> Un document du ministère de la Justice du Canada destiné aux praticiens du droit de la famille (*Types of Intimate Partner Violence*, HELP Toolkit - DOC-MJ) identifie explicitement parmi les expressions documentées de violence coercitive contrôlante post-séparation : le dépôt de faux signalements auprès d'une agence de protection de la jeunesse et l'utilisation de tactiques abusives en relation avec le processus judiciaire. Ce document est destiné précisément aux avocats de droit de la famille pour leur permettre d'identifier ces dynamiques dans leur pratique. Me Ayoub, à titre de spécialiste en droit de la jeunesse et membre du Comité consultatif en droit de la jeunesse du Barreau du Québec, connaît ou devrait connaître cette littérature professionnelle.

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de son Comité consultatif en droit de la jeunesse : Me Marie-Josée Ayoub
```

### 5. `legal/analyse/Responsabilité Déonthologique/2013 juin.md` ligne ~620 → `pq-70`

- **rang** 12.5 = score 18.9 × couverture 66%
- **termes partagés** : `comité`, `consultatif`, `barreau`, `jeunesse`, `droit`, `québec`
- **source de la citation** : pdf-8 p.2 — Commission spéciale sur les droits des enfants et la protect — trames 62

**Idée non étayée :**

> Un document du ministère de la Justice du Canada destiné aux praticiens du droit de la famille (*Types of Intimate Partner Violence*, HELP Toolkit - DOC-MJ) identifie explicitement parmi les expressions documentées de violence coercitive contrôlante post-séparation : le dépôt de faux signalements auprès d'une agence de protection de la jeunesse et l'utilisation de tactiques abusives en relation avec le processus judiciaire. Ce document est destiné précisément aux avocats de droit de la famille pour leur permettre d'identifier ces dynamiques dans leur pratique. Me Ayoub, à titre de spécialiste en droit de la jeunesse et membre du Comité consultatif en droit de la jeunesse du Barreau du Québec, connaît ou devrait connaître cette littérature professionnelle.

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de son Comité consultatif en droit de la jeunesse : Me Marie-Josée Ayoub
```

### 6. `legal/faits/faits_par10_2015.md` ligne ~22 → `pq-23`

- **rang** 11.7 = score 21.9 × couverture 53%
- **termes partagés** : `marchande`, `mandat`, `avenue`, `macaulay`, `saint`, `lambert`, `fins`, `valeur`, `partage`
- **source de la citation** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> **66.4.** Le 27 juin 2013, l'évaluateur Louis-Philippe Robert reçoit le mandat d'évaluer la valeur marchande de la maison au 245 avenue Macaulay, Saint-Lambert, à des fins de partage (PDFDocument id=11).

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

### 7. `legal/analyse/Responsabilité Déonthologique/2023-07-21.md` ligne ~60 → `pq-80`

- **rang** 11.2 = score 15.0 × couverture 74%
- **termes partagés** : `reer`, `prestations`, `d'assurance`, `revenus`, `emploi`, `revenu`, `total`
- **source de la citation** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> Le formulaire de fixation des pensions alimentaires, préparé par Me Ayoub, inscrit à la ligne 200 - « Salaire brut » - le montant de 64 028,34$ pour le père. Ce montant correspond au revenu total de 2018 figurant sur l'avis de cotisation transmis par le demandeur. L'avis de cotisation établit que ce revenu total se compose de quatre éléments distincts : revenus d'emploi (47 520,51$), prestations d'assurance-emploi (12 034,00$), prestations REER (4 089,60$), et autres revenus (384,23$). Ces quatre composantes sont inscrites à la ligne 200 sans ventilation aux lignes correspondantes du formulaire - notamment les lignes 203 (assurance-emploi) et 208 (autres revenus).

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

### 8. `legal/pont/pont_par56-57_2015.md` ligne ~41 → `pq-102`

- **rang** 11.1 = score 20.3 × couverture 55%
- **termes partagés** : `fournisseur`, `réclamation`, `transaction`, `paiement`, `soumise`, `assurances`, `type`, `direct`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 1. Les enfants étaient bénéficiaires du régime d'assurance collective auquel adhérait le défendeur.
> 2. Une réclamation par paiement direct était soumise au fournisseur ou à l'assureur à partir des renseignements du régime, puis traitée selon l'admissibilité du bénéficiaire, la dépense et les conditions de la couverture.
> 3. Le participant n'avait pas à autoriser chaque réclamation présentée au bénéfice des enfants.
> 4. Entre le 25 février 2015 et le 16 mai 2016, treize transactions de type P ont été portées au nom des enfants ; l'assureur a versé la portion couverte au fournisseur.
> 5. Durant l'été 2015, trois transactions de type N ont été portées au nom des enfants : 110 $ ont été soumis pour chacune, puis 88 $ ont été versés au compte du participant, laissant 22 $ non remboursés.
> 6. Aucune de ces seize transactions n'a eu lieu un dimanche.
> 7. Le 17 octobre 2015, une transaction a été portée au nom de Nicolas, soit la dernière transaction documentée avant la Requête.
> 8. Le 19 novembre 2015, la Requête a allégué que le défendeur refusait l'utilisation des assurances et que lui seul pouvait en bénéficier lorsqu'il avait les enfants.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

### 9. `legal/ponts_requete_2015_consolides.md` ligne ~1593 → `pq-102`

- **rang** 11.1 = score 20.3 × couverture 55%
- **termes partagés** : `fournisseur`, `réclamation`, `transaction`, `paiement`, `soumise`, `assurances`, `type`, `direct`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 1. Les enfants étaient bénéficiaires du régime d'assurance collective auquel adhérait le défendeur.
> 2. Une réclamation par paiement direct était soumise au fournisseur ou à l'assureur à partir des renseignements du régime, puis traitée selon l'admissibilité du bénéficiaire, la dépense et les conditions de la couverture.
> 3. Le participant n'avait pas à autoriser chaque réclamation présentée au bénéfice des enfants.
> 4. Entre le 25 février 2015 et le 16 mai 2016, treize transactions de type P ont été portées au nom des enfants ; l'assureur a versé la portion couverte au fournisseur.
> 5. Durant l'été 2015, trois transactions de type N ont été portées au nom des enfants : 110 $ ont été soumis pour chacune, puis 88 $ ont été versés au compte du participant, laissant 22 $ non remboursés.
> 6. Aucune de ces seize transactions n'a eu lieu un dimanche.
> 7. Le 17 octobre 2015, une transaction a été portée au nom de Nicolas, soit la dernière transaction documentée avant la Requête.
> 8. Le 19 novembre 2015, la Requête a allégué que le défendeur refusait l'utilisation des assurances et que lui seul pouvait en bénéficier lorsqu'il avait les enfants.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

### 10. `legal/memoire faille structurelle.md` ligne ~254 → `pq-72`

- **rang** 10.5 = score 17.3 × couverture 61%
- **termes partagés** : `comité`, `consultatif`, `barreau`, `jeunesse`, `droit`
- **source de la citation** : pdf-8 p.2 — Commission spéciale sur les droits des enfants et la protect — trames 48, 55

**Idée non étayée :**

> Me Ayoub n'est pas une avocate généraliste qui prendrait un dossier familial par hasard. Son implication institutionnelle - Comité consultatif en droit de la jeunesse, rédaction de mémoires au nom du Barreau - établit qu'elle maîtrise l'état de l'art dans ce domaine. Il lui est institutionnellement impossible de plaider l'ignorance des fondements scientifiques et juridiques de la stabilité de l'enfant. C'est précisément parce qu'elle connaît ces fondements qu'elle est capable d'en concevoir l'instrumentalisation.

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de son Comité consultatif en droit de la jeunesse : Me Marie-Josée Ayoub
```

### 11. `legal/memoire faille structurelle.md` ligne ~254 → `pq-70`

- **rang** 10.5 = score 17.3 × couverture 61%
- **termes partagés** : `comité`, `consultatif`, `barreau`, `jeunesse`, `droit`
- **source de la citation** : pdf-8 p.2 — Commission spéciale sur les droits des enfants et la protect — trames 62

**Idée non étayée :**

> Me Ayoub n'est pas une avocate généraliste qui prendrait un dossier familial par hasard. Son implication institutionnelle - Comité consultatif en droit de la jeunesse, rédaction de mémoires au nom du Barreau - établit qu'elle maîtrise l'état de l'art dans ce domaine. Il lui est institutionnellement impossible de plaider l'ignorance des fondements scientifiques et juridiques de la stabilité de l'enfant. C'est précisément parce qu'elle connaît ces fondements qu'elle est capable d'en concevoir l'instrumentalisation.

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de son Comité consultatif en droit de la jeunesse : Me Marie-Josée Ayoub
```

### 12. `legal/piece_pdf-75.md` ligne ~28 → `pq-72`

- **rang** 10.5 = score 17.3 × couverture 61%
- **termes partagés** : `comité`, `consultatif`, `barreau`, `jeunesse`, `droit`
- **source de la citation** : pdf-8 p.2 — Commission spéciale sur les droits des enfants et la protect — trames 48, 55

**Idée non étayée :**

> - **C1** nomme, dans une source institutionnelle destinée aux avocats de droit de la famille, deux comportements qui correspondent à la structure documentée du dossier : le **faux signalement à une agence de protection de la jeunesse** et l'**emploi de tactiques abusives en lien avec le processus judiciaire** - répertoriés comme expressions du **contrôle coercitif post-séparation**. Pertinent à l'analyse abus/contrôle et au scienter d'une spécialiste (MJ, membre du Comité consultatif en droit de la jeunesse du Barreau, est censée connaître cette littérature).
> - **C2** éclaire la **substitution d'intérêts** (rôle parental subordonné à l'objectif de l'adulte).

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de son Comité consultatif en droit de la jeunesse : Me Marie-Josée Ayoub
```

### 13. `legal/piece_pdf-75.md` ligne ~28 → `pq-70`

- **rang** 10.5 = score 17.3 × couverture 61%
- **termes partagés** : `comité`, `consultatif`, `barreau`, `jeunesse`, `droit`
- **source de la citation** : pdf-8 p.2 — Commission spéciale sur les droits des enfants et la protect — trames 62

**Idée non étayée :**

> - **C1** nomme, dans une source institutionnelle destinée aux avocats de droit de la famille, deux comportements qui correspondent à la structure documentée du dossier : le **faux signalement à une agence de protection de la jeunesse** et l'**emploi de tactiques abusives en lien avec le processus judiciaire** - répertoriés comme expressions du **contrôle coercitif post-séparation**. Pertinent à l'analyse abus/contrôle et au scienter d'une spécialiste (MJ, membre du Comité consultatif en droit de la jeunesse du Barreau, est censée connaître cette littérature).
> - **C2** éclaire la **substitution d'intérêts** (rôle parental subordonné à l'objectif de l'adulte).

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de son Comité consultatif en droit de la jeunesse : Me Marie-Josée Ayoub
```

### 14. `legal/pont/pont_par10_2015.md` ligne ~65 → `pq-23`

- **rang** 10.5 = score 20.8 × couverture 50%
- **termes partagés** : `marchande`, `avenue`, `macaulay`, `saint`, `lambert`, `fins`, `valeur`, `partage`, `rapport`
- **source de la citation** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> 1. En août 2009, les parties ont acquis conjointement la résidence familiale au 245, avenue Macaulay, à Saint-Lambert.
> 2. Le 11 juin 2013, Me Marie-Josée Ayoub a écrit à la demanderesse un plan prévoyant l'usage exclusif de la résidence familiale, la relocalisation du défendeur et le paiement par lui de 50 % des charges afférentes à la maison.
> 3. Le 26 juin 2013, le défendeur a écrit à Me Suzanne Pringle que la soeur avocate de sa conjointe la guidait « de façon à [le] piéger » et que la demanderesse lui écrivait qu'elle le trouvait agressif et avait peur de lui.
> 4. Le 27 juin 2013, le défendeur a écrit à son supérieur : « je dois vendre ma maison ».
> 5. Le même jour, il a mandaté l'évaluateur agréé Louis-Philippe Robert pour établir la valeur marchande de la résidence à des fins de partage.
> 6. Le 28 juin 2013, l'évaluateur a inspecté la propriété.
> 7. Le 11 juillet 2013, l'évaluateur a produit son rapport d'évaluation marchande à des fins de partage.
> 8. Le 1er août 2014, le défendeur a vendu sa part de la résidence à la demanderesse au prix établi par ce rapport.

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

### 15. `legal/ponts_requete_2015_consolides.md` ligne ~798 → `pq-23`

- **rang** 10.5 = score 20.8 × couverture 50%
- **termes partagés** : `marchande`, `avenue`, `macaulay`, `saint`, `lambert`, `fins`, `valeur`, `partage`, `rapport`
- **source de la citation** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> 1. En août 2009, les parties ont acquis conjointement la résidence familiale au 245, avenue Macaulay, à Saint-Lambert.
> 2. Le 11 juin 2013, Me Marie-Josée Ayoub a écrit à la demanderesse un plan prévoyant l'usage exclusif de la résidence familiale, la relocalisation du défendeur et le paiement par lui de 50 % des charges afférentes à la maison.
> 3. Le 26 juin 2013, le défendeur a écrit à Me Suzanne Pringle que la soeur avocate de sa conjointe la guidait « de façon à [le] piéger » et que la demanderesse lui écrivait qu'elle le trouvait agressif et avait peur de lui.
> 4. Le 27 juin 2013, le défendeur a écrit à son supérieur : « je dois vendre ma maison ».
> 5. Le même jour, il a mandaté l'évaluateur agréé Louis-Philippe Robert pour établir la valeur marchande de la résidence à des fins de partage.
> 6. Le 28 juin 2013, l'évaluateur a inspecté la propriété.
> 7. Le 11 juillet 2013, l'évaluateur a produit son rapport d'évaluation marchande à des fins de partage.
> 8. Le 1er août 2014, le défendeur a vendu sa part de la résidence à la demanderesse au prix établi par ce rapport.

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

### 16. `legal/compilation_griefs.md` ligne ~1251 → `pq-101`

- **rang** 9.5 = score 15.4 × couverture 62%
- **termes partagés** : `jan`, `fournisseur`, `transactions`, `fév`, `type`, `dimanche`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 6. Les relevés d'assurance (Industrielle Alliance, 2015-2016) documentent **douze transactions par Paiement Direct au fournisseur (type P)** au nom des enfants, entre le 25 février 2015 et le 16 mai 2016, **toutes en dehors du dimanche** :
>    - **2015** : 25 fév. (mer., Nicolas), 16 avr. (jeu., Nicolas), 4 mai (lun., Nicolas), 7 juil. (mar., Alexia - dentaire), 17 sept. (jeu., Alexia), 1er oct. (jeu., Nicolas), 17 oct. (sam., Nicolas - fait 1).
>    - **2016** : 11 jan. (lun., Nicolas - fait 10), 10 fév. (mer., Nicolas), 27 fév. (sam., Nicolas), 4 mai (mer., Nicolas), 16 mai (lun., Alexia).

**Citation disponible :**

```text
Transactions 2016 — Paiements directs au fournisseur (type P) : 11 jan (Nicolas/Santé), 10 fév (Nicolas/Santé), 27 fév (Nicolas/Santé), 4 mai (Nicolas/Santé), 16 mai (Alexia/Santé). Toutes hors dimanche.
```

### 17. `legal/these_test_sincerite_2013.md` ligne ~67 → `pq-58`

- **rang** 9.1 = score 14.2 × couverture 64%
- **termes partagés** : `intervenant`, `dpj`, `compromis`, `développement`, `sécurité`, `conjugale`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> 1. **Il porte sur l'enfant**, non sur la relation conjugale. C'est la sécurité et le développement d'Alexia qui sont dits compromis.
> 2. **Il est structurel**, non événementiel. « Depuis sa naissance » - soit, au 11 juin 2013, environ trois ans et huit mois. Il ne décrit pas un incident mais un état continu.
> 3. **Il est de gravité maximale dans son registre.** Il annonce la conclusion qu'« tout intervenant de la DPJ » tirerait - c'est-à-dire le seuil de compromission au sens de la *Loi sur la protection de la jeunesse*.
> 4. **Il est présenté comme actuel** au moment où il est écrit.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
```

### 18. `legal/piece_thread-6_reconstruction.md` ligne ~287 → `eq-120` — *citation encore inexploitée*

- **rang** 9.1 = score 22.4 × couverture 41%
- **termes partagés** : `paieraient`, `comprendrait`, `savais`, `prix`, `eux`, `qu'on`, `aurait`
- **source de la citation** : email-295 — Re: Visite — trames —

**Idée non étayée :**

> * Tu penses que mes décisions étaient rationnelles? Tu penses que ma vie je
> l'aurais choisie ainsi? Non je sacrifie tout pour eux car ils sont les deux
> êtres les plus précieux à mes yeux. Ma vie aurait été bien plus simple en
> garde partagée, je le sais. Mais je savais qu'on ne se comprendrait pas
> plus et que c'est eux qui en paieraient le prix...*

**Citation disponible :**

```text
Mais je savais qu'on ne se comprendrait pas plus et que c'est eux qui en paieraient le prix. Par contre en vieillissant les enfants sont plus capables de s'exprimer et aurait pu palier au fait que nous on ne se parle pas et on ne se comprend pas en ayant une base claire.
```

### 19. `legal/analyse/Responsabilité Déonthologique/2023-07-21.md` ligne ~66 → `pq-79`

- **rang** 8.9 = score 19.7 × couverture 45%
- **termes partagés** : `région`, `montérégie`, `gouvernement`, `guichet`, `emplois`, `canada`
- **source de la citation** : pdf-67 p.1 — Salaire Technicien/technicienne en pharmacie au Québec - 202 — trames 62

**Idée non étayée :**

> Les données du Guichet-Emplois du gouvernement du Canada pour la région de la Montérégie établissent les salaires médians suivants pour deux des trois catégories d'emplois définies par Me Ayoub dans la déclaration assermentée de 2019 :

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION, Technicien/technicienne en pharmacie au Québec, Région de la Montérégie bas 15,25 median 17,00 haut 25,00 - Date de modification : 2023-01-23
```

### 20. `legal/analyse/Responsabilité Déonthologique/2023-07-21.md` ligne ~23 → `pq-79`

- **rang** 8.8 = score 19.6 × couverture 45%
- **termes partagés** : `technicienne`, `montérégie`, `guichet`, `pharmacie`, `technicien`, `emplois`
- **source de la citation** : pdf-67 p.1 — Salaire Technicien/technicienne en pharmacie au Québec - 202 — trames 62

**Idée non étayée :**

> - Dénonciation du moyen déclinatoire, signée par Me Ayoub, 21 juillet 2023 - **DMD-2023**
> - Déclaration assermentée du 21 octobre 2019 - **DA-2019** *(référence croisée Bloc 3)*
> - Procès-verbal d'audience du 4 novembre 2019 - **PV-2019**
> - Formulaire de fixation des pensions alimentaires du 4 novembre 2019, préparé par Me Ayoub - **FPA-2019**
> - Avis de cotisation 2018, transmis par le père à Me Ayoub - **AC-2018**
> - Jugement intérimaire du 27 septembre 2019 - **JI-2019** *(référence croisée Bloc 4)*
> - Données Guichet-Emplois, Montérégie, janvier 2024 - technicien/technicienne en pharmacie - **GE-1**
> - Données Guichet-Emplois, Montérégie, janvier 2024 - représentant/représentante au service à la clientèle - services financiers - **GE-2**

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION, Technicien/technicienne en pharmacie au Québec, Région de la Montérégie bas 15,25 median 17,00 haut 25,00 - Date de modification : 2023-01-23
```

### 21. `legal/journal_ete2013.md` ligne ~25 → `pq-23`

- **rang** 8.8 = score 19.0 × couverture 46%
- **termes partagés** : `marchande`, `avenue`, `macaulay`, `saint`, `lambert`, `fins`, `valeur`, `partage`
- **source de la citation** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> **2013-06-27** - PDFDocument PDF11 : LP reçoit l'étude de la valeur marchande de la résidence familiale (245 avenue Macaulay, Saint-Lambert) commandée aux fins de partage. LP est à Saint-Lambert et est activement impliqué dans le règlement des affaires familiales.

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

### 22. `legal/pont/pont_par56-57_2015.md` ligne ~41 → `pq-100`

- **rang** 8.7 = score 14.1 × couverture 62%
- **termes partagés** : `remboursements`, `participant`, `assurances`, `lorsqu'il`, `type`, `direct`
- **source de la citation** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 1. Les enfants étaient bénéficiaires du régime d'assurance collective auquel adhérait le défendeur.
> 2. Une réclamation par paiement direct était soumise au fournisseur ou à l'assureur à partir des renseignements du régime, puis traitée selon l'admissibilité du bénéficiaire, la dépense et les conditions de la couverture.
> 3. Le participant n'avait pas à autoriser chaque réclamation présentée au bénéfice des enfants.
> 4. Entre le 25 février 2015 et le 16 mai 2016, treize transactions de type P ont été portées au nom des enfants ; l'assureur a versé la portion couverte au fournisseur.
> 5. Durant l'été 2015, trois transactions de type N ont été portées au nom des enfants : 110 $ ont été soumis pour chacune, puis 88 $ ont été versés au compte du participant, laissant 22 $ non remboursés.
> 6. Aucune de ces seize transactions n'a eu lieu un dimanche.
> 7. Le 17 octobre 2015, une transaction a été portée au nom de Nicolas, soit la dernière transaction documentée avant la Requête.
> 8. Le 19 novembre 2015, la Requête a allégué que le défendeur refusait l'utilisation des assurances et que lui seul pouvait en bénéficier lorsqu'il avait les enfants.

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

### 23. `legal/ponts_requete_2015_consolides.md` ligne ~1593 → `pq-100`

- **rang** 8.7 = score 14.1 × couverture 62%
- **termes partagés** : `remboursements`, `participant`, `assurances`, `lorsqu'il`, `type`, `direct`
- **source de la citation** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 1. Les enfants étaient bénéficiaires du régime d'assurance collective auquel adhérait le défendeur.
> 2. Une réclamation par paiement direct était soumise au fournisseur ou à l'assureur à partir des renseignements du régime, puis traitée selon l'admissibilité du bénéficiaire, la dépense et les conditions de la couverture.
> 3. Le participant n'avait pas à autoriser chaque réclamation présentée au bénéfice des enfants.
> 4. Entre le 25 février 2015 et le 16 mai 2016, treize transactions de type P ont été portées au nom des enfants ; l'assureur a versé la portion couverte au fournisseur.
> 5. Durant l'été 2015, trois transactions de type N ont été portées au nom des enfants : 110 $ ont été soumis pour chacune, puis 88 $ ont été versés au compte du participant, laissant 22 $ non remboursés.
> 6. Aucune de ces seize transactions n'a eu lieu un dimanche.
> 7. Le 17 octobre 2015, une transaction a été portée au nom de Nicolas, soit la dernière transaction documentée avant la Requête.
> 8. Le 19 novembre 2015, la Requête a allégué que le défendeur refusait l'utilisation des assurances et que lui seul pouvait en bénéficier lorsqu'il avait les enfants.

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

### 24. `legal/analyse/Responsabilité Déonthologique/2023-07-21.md` ligne ~60 → `pq-81`

- **rang** 8.6 = score 11.6 × couverture 74%
- **termes partagés** : `reer`, `prestations`, `d'assurance`, `revenus`, `emploi`
- **source de la citation** : pdf-30 p.1 — Avis de cotisation 2019 — trames 62

**Idée non étayée :**

> Le formulaire de fixation des pensions alimentaires, préparé par Me Ayoub, inscrit à la ligne 200 - « Salaire brut » - le montant de 64 028,34$ pour le père. Ce montant correspond au revenu total de 2018 figurant sur l'avis de cotisation transmis par le demandeur. L'avis de cotisation établit que ce revenu total se compose de quatre éléments distincts : revenus d'emploi (47 520,51$), prestations d'assurance-emploi (12 034,00$), prestations REER (4 089,60$), et autres revenus (384,23$). Ces quatre composantes sont inscrites à la ligne 200 sans ventilation aux lignes correspondantes du formulaire - notamment les lignes 203 (assurance-emploi) et 208 (autres revenus).

**Citation disponible :**

```text
Revenus Net : 41788,58
Prestations d'assurance emploi : 8752.00
Retrait REER : 37991.58
```

### 25. `legal/allegation_stmt66_residence_2014.md` ligne ~27 → `pq-15`

- **rang** 8.6 = score 22.0 × couverture 39%
- **termes partagés** : `orages`, `dégâts`, `pluie`, `dommages`, `montréal`
- **source de la citation** : pdf-60 p.1 — Pluie diluvienne 2012 — trames 13

**Idée non étayée :**

> 2. Le 30 mai 2012, des pluies diluviennes causent des dommages importants dans la région de Montréal (PDFDocument id=60 - *Orages : une pluie de dégâts sur Montréal*, Daphné Cameron, La Presse). La résidence familiale est affectée : le sous-sol subit des dommages.

**Citation disponible :**

```text
Les violents orages qui sont passés au-dessus de Montréal ont laissé dans leur sillage une pluie de dégâts. En l'espace de 15 minutes, commerçants et citoyens de Montréal ont vu l'eau monter et les dommages s'accumuler.
```

### 26. `legal/dossier_plaidoirie/01_arc_garde_2013-2016.md` ligne ~1120 → `pq-7`

- **rang** 7.9 = score 11.2 × couverture 71%
- **termes partagés** : `intervenant`, `arriver`, `pourra`, `développement`, `sécurité`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 7, 48, 49, 70, 72

**Idée non étayée :**

> **Amendement proposé :** circonscrire plutôt que supprimer. P‐2 n'est pas
> invoquée comme preuve autonome de la fausseté de tout le registre de violence
> entre les adultes; elle l'est quant à la **proposition de compromission de la
> sécurité et du développement des enfants**, laquelle est démentie par les
> prescriptions du même écrit et n'y est d'ailleurs pas posée comme un fait établi
> mais comme une conclusion qu'un intervenant « pourra arriver » à tirer (¶ 40).

**Citation disponible :**

```text
tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.
```

### 27. `legal/analyse/Responsabilité Déonthologique/2023-07-21.md` ligne ~23 → `pq-78`

- **rang** 7.7 = score 23.2 × couverture 33%
- **termes partagés** : `représentante`, `guichet`, `clientèle`, `représentant`, `financiers`, `emplois`, `services`, `service`
- **source de la citation** : pdf-66 p.1 — Revenus représentant au service à la clientèle — trames 62

**Idée non étayée :**

> - Dénonciation du moyen déclinatoire, signée par Me Ayoub, 21 juillet 2023 - **DMD-2023**
> - Déclaration assermentée du 21 octobre 2019 - **DA-2019** *(référence croisée Bloc 3)*
> - Procès-verbal d'audience du 4 novembre 2019 - **PV-2019**
> - Formulaire de fixation des pensions alimentaires du 4 novembre 2019, préparé par Me Ayoub - **FPA-2019**
> - Avis de cotisation 2018, transmis par le père à Me Ayoub - **AC-2018**
> - Jugement intérimaire du 27 septembre 2019 - **JI-2019** *(référence croisée Bloc 4)*
> - Données Guichet-Emplois, Montérégie, janvier 2024 - technicien/technicienne en pharmacie - **GE-1**
> - Données Guichet-Emplois, Montérégie, janvier 2024 - représentant/représentante au service à la clientèle - services financiers - **GE-2**

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION Représentant/représentante au service à la clientèle - services financiers au Québec Date de modification : 2024-01-23
Région de Montréal Salaire Bas : 16,28 Median 21,00 Haut : 26,99 
https://www.guichet-emplois.gc.ca/salaire-horaire/representant-representante-service-clientele-services-financiers/montreal
```

### 28. `legal/these_test_sincerite_2013.md` ligne ~67 → `pq-34`

- **rang** 7.7 = score 14.2 × couverture 54%
- **termes partagés** : `intervenant`, `dpj`, `compromis`, `développement`, `sécurité`, `conjugale`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 48

**Idée non étayée :**

> 1. **Il porte sur l'enfant**, non sur la relation conjugale. C'est la sécurité et le développement d'Alexia qui sont dits compromis.
> 2. **Il est structurel**, non événementiel. « Depuis sa naissance » - soit, au 11 juin 2013, environ trois ans et huit mois. Il ne décrit pas un incident mais un état continu.
> 3. **Il est de gravité maximale dans son registre.** Il annonce la conclusion qu'« tout intervenant de la DPJ » tirerait - c'est-à-dire le seuil de compromission au sens de la *Loi sur la protection de la jeunesse*.
> 4. **Il est présenté comme actuel** au moment où il est écrit.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Tu dois le faire sortir de la maison [...]
```

### 29. `legal/these_test_sincerite_2013.md` ligne ~67 → `pq-7`

- **rang** 7.7 = score 11.0 × couverture 70%
- **termes partagés** : `intervenant`, `dpj`, `compromis`, `développement`, `sécurité`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 7, 48, 49, 70, 72

**Idée non étayée :**

> 1. **Il porte sur l'enfant**, non sur la relation conjugale. C'est la sécurité et le développement d'Alexia qui sont dits compromis.
> 2. **Il est structurel**, non événementiel. « Depuis sa naissance » - soit, au 11 juin 2013, environ trois ans et huit mois. Il ne décrit pas un incident mais un état continu.
> 3. **Il est de gravité maximale dans son registre.** Il annonce la conclusion qu'« tout intervenant de la DPJ » tirerait - c'est-à-dire le seuil de compromission au sens de la *Loi sur la protection de la jeunesse*.
> 4. **Il est présenté comme actuel** au moment où il est écrit.

**Citation disponible :**

```text
tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.
```

### 30. `legal/analyse/Responsabilité civile/requete 21 octobre 2019/analyse preliminaire - echec negociations 2015 et paragraphe 3.md` ligne ~642 → `pq-67`

- **rang** 7.6 = score 19.5 × couverture 39%
- **termes partagés** : `jeudis`, `lundis`, `prenne`, `mardis`, `mercredis`, `danse`
- **source de la citation** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames 56

**Idée non étayée :**

> - il accepte expressément le principe d'une progression;
> - il ne demande pas que la garde partagée prenne effet immédiatement;
> - il propose qu'elle commence le 7 février 2016, soit une transition d'environ cinq mois après sa réponse et d'environ six mois après le projet maternel d'août;
> - il laisse à la mère le choix entre les lundis-mardis et les mercredis-jeudis;
> - il motive expressément ce choix par la prise en compte de ses cours de danse;
> - pour les fêtes, il propose subsidiairement un principe d'alternance;

**Citation disponible :**

```text
En ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse;
```

### 31. `legal/analyse/Responsabilité civile/requete 21 octobre 2019/analyse preliminaire - echec negociations 2015 et paragraphe 3.md` ligne ~642 → `pq-14` — *citation encore inexploitée*

- **rang** 7.6 = score 19.5 × couverture 39%
- **termes partagés** : `jeudis`, `lundis`, `prenne`, `mardis`, `mercredis`, `danse`
- **source de la citation** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames —

**Idée non étayée :**

> - il accepte expressément le principe d'une progression;
> - il ne demande pas que la garde partagée prenne effet immédiatement;
> - il propose qu'elle commence le 7 février 2016, soit une transition d'environ cinq mois après sa réponse et d'environ six mois après le projet maternel d'août;
> - il laisse à la mère le choix entre les lundis-mardis et les mercredis-jeudis;
> - il motive expressément ce choix par la prise en compte de ses cours de danse;
> - pour les fêtes, il propose subsidiairement un principe d'alternance;

**Citation disponible :**

```text
En ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse;
```

### 32. `legal/dossier_plaidoirie/01_arc_garde_2013-2016.md` ligne ~1120 → `pq-58`

- **rang** 7.4 = score 12.8 × couverture 58%
- **termes partagés** : `intervenant`, `arriver`, `pourra`, `développement`, `sécurité`, `violence`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> **Amendement proposé :** circonscrire plutôt que supprimer. P‐2 n'est pas
> invoquée comme preuve autonome de la fausseté de tout le registre de violence
> entre les adultes; elle l'est quant à la **proposition de compromission de la
> sécurité et du développement des enfants**, laquelle est démentie par les
> prescriptions du même écrit et n'y est d'ailleurs pas posée comme un fait établi
> mais comme une conclusion qu'un intervenant « pourra arriver » à tirer (¶ 40).

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
```

### 33. `legal/compilation_griefs.md` ligne ~1257 → `pq-102`

- **rang** 7.0 = score 16.1 × couverture 43%
- **termes partagés** : `réclamation`, `transaction`, `paiement`, `service`, `type`, `direct`, `point`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 8. Le Paiement Direct (type P) implique la présentation de la carte / du numéro de police **au point de service**, au moment de la transaction, déclenchant le paiement immédiat par l'assureur (la date du service = la date de la réclamation ; aucun décalage possible).

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

### 34. `legal/axe_agenda_danse_elise.md` ligne ~127 → `pq-67`

- **rang** 6.9 = score 18.6 × couverture 37%
- **termes partagés** : `considération`, `disposé`, `prenne`, `choisir`, `laisser`, `l'horaire`, `danse`, `afin`
- **source de la citation** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames 56

**Idée non étayée :**

> 24. Le 2 septembre 2015, l'avocat du demandeur a écrit à l'avocate de la défenderesse que le demandeur était disposé à laisser la défenderesse choisir les jours de garde afin que l'horaire de garde prenne en considération ses cours de danse (P-X, PDFDocument 6).

**Citation disponible :**

```text
En ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse;
```

### 35. `legal/axe_agenda_danse_elise.md` ligne ~127 → `pq-14` — *citation encore inexploitée*

- **rang** 6.9 = score 18.6 × couverture 37%
- **termes partagés** : `considération`, `disposé`, `prenne`, `choisir`, `laisser`, `l'horaire`, `danse`, `afin`
- **source de la citation** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames —

**Idée non étayée :**

> 24. Le 2 septembre 2015, l'avocat du demandeur a écrit à l'avocate de la défenderesse que le demandeur était disposé à laisser la défenderesse choisir les jours de garde afin que l'horaire de garde prenne en considération ses cours de danse (P-X, PDFDocument 6).

**Citation disponible :**

```text
En ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse;
```

### 36. `legal/piece_thread-91_emails-369-370.md` ligne ~29 → `eq-177`

- **rang** 6.9 = score 12.0 × couverture 57%
- **termes partagés** : `passerai`, `porter`, `chercher`, `aller`, `matin`
- **source de la citation** : email-369 — Fwd: Éléments à imprimer — trames 65

**Idée non étayée :**

> - Dans « Je passerai **les** chercher », le pronom « les » désigne les **éléments à imprimer**, non les enfants.
> - L'heure `05:02 UTC` de la base correspond à **00 h 02 HNE** dans l'en-tête original. Le message ne prouve pas que LP était levé à 5 h du matin.
> - Le courriel dit « aller porter Alexia », sans nommer la destination. L'attribution à la garderie ou au milieu préscolaire est une inférence contextuelle à authentifier par LP et par les autres pièces.
> - La pièce établit directement une prise en charge de transport annoncée; elle ne prouve pas, seule, chaque dépôt de la semaine.

**Citation disponible :**

```text
Je passerai les chercher demain matin apres etre aller porter Alexia.
```

### 37. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 56 57.md` ligne ~33 → `pq-102`

- **rang** 6.9 = score 16.0 × couverture 43%
- **termes partagés** : `fournisseur`, `réclamation`, `transaction`, `paiement`, `type`, `direct`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> Les relevés distinguent deux mécanismes. Pour une transaction de type **P**, l'assureur verse la portion couverte au fournisseur. Pour une transaction de type **N**, la dépense est déboursée intégralement hors du paiement direct, puis la portion couverte est remboursée au compte du participant. Industrielle Alliance décrit le premier mécanisme : le pharmacien soumet lui-même la réclamation après présentation de la carte d'assurance collective ([iA, réclamation de médicaments](https://ia.ca/faire-une-reclamation/collective/medicaments)).

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

### 38. `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/10_synthese_coherence_predictive_P2_P9_P16_P18_P19.md` ligne ~202 → `pq-92`

- **rang** 6.9 = score 11.0 × couverture 62%
- **termes partagés** : `samedi`, `mardi`, `l'école`, `matin`, `garderie`, `dimanche`
- **source de la citation** : pdf-5 p.3 — 20150813 MJ projet consentement — trames 50

**Idée non étayée :**

> - la première semaine, du samedi matin au dimanche soir, soit une nuitée;
> - la deuxième semaine, du dimanche 16 h au mardi matin, soit **deux nuitées
>   consécutives**, avec retour à l'école ou à la garderie;
> - au total, trois nuitées sur quatorze.

**Citation disponible :**

```text
À compter de ce jour jusqu'au 28 août 2016 : Semaine 1 De samedi 10h30 (directement à la piscine) à Dimanche 20h00; Semaine 2 Dimanche 16h00 à Mardi matin directement à l'école et/ou la garderie;
```

### 39. `legal/analyse/Responsabilité Déonthologique/2015 avril, aout.md` ligne ~310 → `pq-72`

- **rang** 6.4 = score 13.5 × couverture 47%
- **termes partagés** : `comité`, `consultatif`, `jeunesse`, `droit`
- **source de la citation** : pdf-8 p.2 — Commission spéciale sur les droits des enfants et la protect — trames 48, 55

**Idée non étayée :**

> L'article 21 du Code de déontologie impose à l'avocat d'exercer avec compétence. En droit de la famille, l'application légitime de la norme de stabilité exige la compréhension de sa finalité - la hiérarchie des stabilités, dont la primauté de la continuité relationnelle sur la routine temporelle, est le fondement documenté de toute intervention en droit de la jeunesse. Un avocat qui invoque cette norme est présumé en connaître les fondements. Pour Me Ayoub, cette présomption est renforcée par sa participation institutionnelle documentée - membre du Comité consultatif en droit de la jeunesse, co-auteure de mémoires institutionnels sur la protection de l'enfance. Il lui est institutionnellement impossible d'invoquer l'ignorance de ces fondements.

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de son Comité consultatif en droit de la jeunesse : Me Marie-Josée Ayoub
```

### 40. `legal/analyse/Responsabilité Déonthologique/2015 avril, aout.md` ligne ~310 → `pq-70`

- **rang** 6.4 = score 13.5 × couverture 47%
- **termes partagés** : `comité`, `consultatif`, `jeunesse`, `droit`
- **source de la citation** : pdf-8 p.2 — Commission spéciale sur les droits des enfants et la protect — trames 62

**Idée non étayée :**

> L'article 21 du Code de déontologie impose à l'avocat d'exercer avec compétence. En droit de la famille, l'application légitime de la norme de stabilité exige la compréhension de sa finalité - la hiérarchie des stabilités, dont la primauté de la continuité relationnelle sur la routine temporelle, est le fondement documenté de toute intervention en droit de la jeunesse. Un avocat qui invoque cette norme est présumé en connaître les fondements. Pour Me Ayoub, cette présomption est renforcée par sa participation institutionnelle documentée - membre du Comité consultatif en droit de la jeunesse, co-auteure de mémoires institutionnels sur la protection de l'enfance. Il lui est institutionnellement impossible d'invoquer l'ignorance de ces fondements.

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de son Comité consultatif en droit de la jeunesse : Me Marie-Josée Ayoub
```

### 41. `legal/axe_agenda_danse_elise.md` ligne ~71 → `pq-12`

- **rang** 6.4 = score 25.2 × couverture 25%
- **termes partagés** : `urban`, `element`, `ballets`, `modernes`, `depot`, `l'école`, `québec`, `danse`
- **source de la citation** : pdf-59 p.1 — Biographie d'Elise Ayoub publiée sur le site web du studio d — trames 12, 64

**Idée non étayée :**

> **Fait d'inscription (base de l'inférence sur la fréquence hebdomadaire) :** La défenderesse était inscrite à l'école Les Ballets Modernes du Québec (Hugo Depot) de 1999 à 2016 (P-X, PDFDocument 59). Une inscription à une école de danse - par opposition à des cours "drop-in" comme Urban Element - implique structurellement un horaire hebdomadaire fixe pendant la durée d'une session. Cette inférence ne dépend pas du calendrier 2025-2026 (PhotoDocument 4), qui reste disponible comme illustration mais n'est pas nécessaire pour établir la récurrence elle-même.

**Citation disponible :**

```text
En 1999, fascinée par la danse, elle se joint à l’école de danse Les Ballets Modernes du Québec. En 2005, elle débute ses classes au Urban Element (maintenant le UEZ) , où elle y rencontre plusieurs pionniers de la danse urbaine. Elle continue toutefois ses cours chez Les Ballet Modernes du Québec où elle observe les talents de Direction d'Hugo Depot et Francine St-Yves, et ce jusqu'en 2016.
```

### 42. `legal/dossier_plaidoirie/01_arc_garde_2013-2016.md` ligne ~1120 → `pq-34`

- **rang** 6.3 = score 12.8 × couverture 49%
- **termes partagés** : `intervenant`, `arriver`, `pourra`, `développement`, `sécurité`, `violence`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 48

**Idée non étayée :**

> **Amendement proposé :** circonscrire plutôt que supprimer. P‐2 n'est pas
> invoquée comme preuve autonome de la fausseté de tout le registre de violence
> entre les adultes; elle l'est quant à la **proposition de compromission de la
> sécurité et du développement des enfants**, laquelle est démentie par les
> prescriptions du même écrit et n'y est d'ailleurs pas posée comme un fait établi
> mais comme une conclusion qu'un intervenant « pourra arriver » à tirer (¶ 40).

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Tu dois le faire sortir de la maison [...]
```

### 43. `legal/these_test_sincerite_2013.md` ligne ~208 → `pq-7`

- **rang** 6.1 = score 9.9 × couverture 62%
- **termes partagés** : `intervenant`, `arriver`, `dpj`, `pourra`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 7, 48, 49, 70, 72

**Idée non étayée :**

> Or **la DPJ n'a jamais été saisie** - par la partie même qui invoquait son critère, et qui ne l'a mobilisée que comme **pronostic** de ce qu'un intervenant « pourra arriver à la conclusion » d'établir (premier étage, *infra* ; §IV.1). **La seule voie capable de combler l'écart était disponible, et elle a été écartée.**

**Citation disponible :**

```text
tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.
```

### 44. `legal/these_test_sincerite_2013.md` ligne ~239 → `pq-7`

- **rang** 6.1 = score 9.9 × couverture 62%
- **termes partagés** : `intervenant`, `arriver`, `dpj`, `pourra`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 7, 48, 49, 70, 72

**Idée non étayée :**

> Le tell est net : **la DPJ n'est jamais saisie.** Elle n'est invoquée que comme *pronostic* de ce qu'un intervenant « pourra arriver à la conclusion » d'établir. On emprunte l'**autorité** du critère sans en accepter le **mécanisme**.

**Citation disponible :**

```text
tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.
```

### 45. `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/03_anteriorite_preference_et_fonction_du_registre.md` ligne ~335 → `pq-104`

- **rang** 6.1 = score 11.3 × couverture 54%
- **termes partagés** : `maternité`, `congé`, `jeune`, `disponibilité`, `âge`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 70

**Idée non étayée :**

> Le registre de la violence conjugale et de la compromission; le jeune âge des
> enfants; la disponibilité fondée sur le congé de maternité; le mieux‐être
> observé pendant une semaine d'absence du père. La question n'est pas leur
> existence dans le document.

**Citation disponible :**

```text
Dans cette requête d'urgence on plaide le jeune âge des enfants, la disponibilité des parents, le fait que tu sois en congé de maternité et un plus car plus disponible
```

### 46. `legal/these_repartition_parentale_tribunal_vs_pere.md` ligne ~149 → `pq-104`

- **rang** 6.1 = score 11.3 × couverture 54%
- **termes partagés** : `maternité`, `congé`, `jeune`, `disponibilité`, `âge`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 70

**Idée non étayée :**

> - de plaider la violence, la compromission, le jeune âge, la disponibilité actuelle et le congé de maternité;
> - de faire sortir LP de la résidence;
> - de réduire ses accès en excluant les couchers;
> - de laisser ensuite une routine mère-enfants **s'installer** pendant la procédure.

**Citation disponible :**

```text
Dans cette requête d'urgence on plaide le jeune âge des enfants, la disponibilité des parents, le fait que tu sois en congé de maternité et un plus car plus disponible
```

### 47. `legal/pont/pont_par10_2015.md` ligne ~65 → `eq-150`

- **rang** 5.9 = score 19.0 × couverture 31%
- **termes partagés** : `piéger`, `agressif`, `trouvait`, `peur`, `conjointe`, `façon`, `parce`, `avocate`
- **source de la citation** : email-365 — Conseils — trames 72

**Idée non étayée :**

> 1. En août 2009, les parties ont acquis conjointement la résidence familiale au 245, avenue Macaulay, à Saint-Lambert.
> 2. Le 11 juin 2013, Me Marie-Josée Ayoub a écrit à la demanderesse un plan prévoyant l'usage exclusif de la résidence familiale, la relocalisation du défendeur et le paiement par lui de 50 % des charges afférentes à la maison.
> 3. Le 26 juin 2013, le défendeur a écrit à Me Suzanne Pringle que la soeur avocate de sa conjointe la guidait « de façon à [le] piéger » et que la demanderesse lui écrivait qu'elle le trouvait agressif et avait peur de lui.
> 4. Le 27 juin 2013, le défendeur a écrit à son supérieur : « je dois vendre ma maison ».
> 5. Le même jour, il a mandaté l'évaluateur agréé Louis-Philippe Robert pour établir la valeur marchande de la résidence à des fins de partage.
> 6. Le 28 juin 2013, l'évaluateur a inspecté la propriété.
> 7. Le 11 juillet 2013, l'évaluateur a produit son rapport d'évaluation marchande à des fins de partage.
> 8. Le 1er août 2014, le défendeur a vendu sa part de la résidence à la demanderesse au prix établi par ce rapport.

**Citation disponible :**

```text
Je vous contacte parce que je suis incapable de gérer cette
situation seule et de manière appropriée, la sœur de ma conjointe est
avocate et la guide de façon à me piéger.
J’ai coupé toute communication avec ma conjointe ce matin du fait que sans
raison elle m’écrive qu’elle trouvait que j’étais agressif et qu’elle avait
peur de moi.
```

### 48. `legal/ponts_requete_2015_consolides.md` ligne ~798 → `eq-150`

- **rang** 5.9 = score 19.0 × couverture 31%
- **termes partagés** : `piéger`, `agressif`, `trouvait`, `peur`, `conjointe`, `façon`, `parce`, `avocate`
- **source de la citation** : email-365 — Conseils — trames 72

**Idée non étayée :**

> 1. En août 2009, les parties ont acquis conjointement la résidence familiale au 245, avenue Macaulay, à Saint-Lambert.
> 2. Le 11 juin 2013, Me Marie-Josée Ayoub a écrit à la demanderesse un plan prévoyant l'usage exclusif de la résidence familiale, la relocalisation du défendeur et le paiement par lui de 50 % des charges afférentes à la maison.
> 3. Le 26 juin 2013, le défendeur a écrit à Me Suzanne Pringle que la soeur avocate de sa conjointe la guidait « de façon à [le] piéger » et que la demanderesse lui écrivait qu'elle le trouvait agressif et avait peur de lui.
> 4. Le 27 juin 2013, le défendeur a écrit à son supérieur : « je dois vendre ma maison ».
> 5. Le même jour, il a mandaté l'évaluateur agréé Louis-Philippe Robert pour établir la valeur marchande de la résidence à des fins de partage.
> 6. Le 28 juin 2013, l'évaluateur a inspecté la propriété.
> 7. Le 11 juillet 2013, l'évaluateur a produit son rapport d'évaluation marchande à des fins de partage.
> 8. Le 1er août 2014, le défendeur a vendu sa part de la résidence à la demanderesse au prix établi par ce rapport.

**Citation disponible :**

```text
Je vous contacte parce que je suis incapable de gérer cette
situation seule et de manière appropriée, la sœur de ma conjointe est
avocate et la guide de façon à me piéger.
J’ai coupé toute communication avec ma conjointe ce matin du fait que sans
raison elle m’écrive qu’elle trouvait que j’étais agressif et qu’elle avait
peur de moi.
```

### 49. `legal/requete_secton_faits_lp.md` ligne ~1161 → `pq-81`

- **rang** 5.9 = score 9.6 × couverture 61%
- **termes partagés** : `reer`, `prestations`, `d'assurance`, `emploi`
- **source de la citation** : pdf-30 p.1 — Avis de cotisation 2019 — trames 62

**Idée non étayée :**

> 399-M. Les prestations d'assurance-emploi de 12 034,00 $ et les prestations d'un régime de retraite ou d'un REER de 4 089,60 $ du demandeur sont ainsi comprises dans la somme inscrite à la ligne « Salaire brut » plutôt qu'aux lignes qui leur sont propres.

**Citation disponible :**

```text
Revenus Net : 41788,58
Prestations d'assurance emploi : 8752.00
Retrait REER : 37991.58
```

### 50. `legal/faits/faits_par56-57_2015.md` ligne ~18 → `pq-102`

- **rang** 5.6 = score 14.5 × couverture 39%
- **termes partagés** : `fournisseur`, `réclamation`, `paiement`, `service`, `direct`, `point`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 4. Dans le mécanisme de paiement direct, la carte ou les renseignements de la police sont présentés au point de service et le fournisseur soumet la réclamation à l'assureur.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

### 51. `legal/analyse/Responsabilité civile/requete 21 octobre 2019/analyse preliminaire - echec negociations 2015 et paragraphe 3.md` ligne ~642 → `pq-28`

- **rang** 5.6 = score 21.3 × couverture 27%
- **termes partagés** : `jeudis`, `lundis`, `prenne`, `mardis`, `mercredis`, `progression`, `danse`
- **source de la citation** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames 34, 40

**Idée non étayée :**

> - il accepte expressément le principe d'une progression;
> - il ne demande pas que la garde partagée prenne effet immédiatement;
> - il propose qu'elle commence le 7 février 2016, soit une transition d'environ cinq mois après sa réponse et d'environ six mois après le projet maternel d'août;
> - il laisse à la mère le choix entre les lundis-mardis et les mercredis-jeudis;
> - il motive expressément ce choix par la prise en compte de ses cours de danse;
> - pour les fêtes, il propose subsidiairement un principe d'alternance;

**Citation disponible :**

```text
notre client est tout à fait disposé à établir une progression dans les droits d'accès auprès des enfants. Cependant, il souhaite ajouter un sous-paragraphe « e) » afin de prévoir qu'à compter du 7 février 2016 l'horaire de garde sera en alternance 2-2-3/2-2-3. En ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse;
```

### 52. `legal/analyse/Responsabilité Déonthologique/2023-07-21.md` ligne ~70 → `pq-78`

- **rang** 5.5 = score 19.7 × couverture 28%
- **termes partagés** : `représentante`, `clientèle`, `représentant`, `financiers`, `services`, `salaire`, `service`
- **source de la citation** : pdf-66 p.1 — Revenus représentant au service à la clientèle — trames 62

**Idée non étayée :**

> - Représentant/représentante au service à la clientèle - services financiers : salaire médian de 20,50$/heure, soit 42 640$ annuellement sur une base de 2 080 heures.

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION Représentant/représentante au service à la clientèle - services financiers au Québec Date de modification : 2024-01-23
Région de Montréal Salaire Bas : 16,28 Median 21,00 Haut : 26,99 
https://www.guichet-emplois.gc.ca/salaire-horaire/representant-representante-service-clientele-services-financiers/montreal
```

### 53. `legal/piece_thread-6_reconstruction.md` ligne ~172 → `eq-105` — *citation encore inexploitée*

- **rang** 5.5 = score 14.1 × couverture 39%
- **termes partagés** : `t'aiment`, `stp`, `sais`
- **source de la citation** : email-299 — Re: Visite — trames —

**Idée non étayée :**

> Louis Philippe pourquoi tu m'accuses tout le temps de vouloir te nuire? Je
> te dis que tu as raison de le faire et tu me réponds des insultes? Pourquoi
> tu ne vois pas que je ne veux pas me chicaner et t'accuser de rien??? Au
> contraire! Ma mère EST MORTE! Je ne sais pas si tu es capable de comprendre
> ça mais je ne VEUX PAS de chicane, je veux au contraire lui faire honneur
> en faisant le meilleur pour les enfants, je te dis que tu as eu raison de
> lui dire tu me reviens en t'obstinant sur un mot...Câline tu fais vraiment
> exprès pour que cela ne s'améliore pas.  Ça ne me dérange pas pour Noël si

**Citation disponible :**

```text
Louis Philippe, stp, les journées ne se reprennent pas. Le temps passe vite et les enfants t'aiment beaucoup et je sais que tu les aimes.
```

### 54. `legal/piece_thread-6_reconstruction.md` ligne ~172 → `eq-101`

- **rang** 5.5 = score 14.1 × couverture 39%
- **termes partagés** : `t'aiment`, `stp`, `sais`
- **source de la citation** : email-299 — Re: Visite — trames 55

**Idée non étayée :**

> Louis Philippe pourquoi tu m'accuses tout le temps de vouloir te nuire? Je
> te dis que tu as raison de le faire et tu me réponds des insultes? Pourquoi
> tu ne vois pas que je ne veux pas me chicaner et t'accuser de rien??? Au
> contraire! Ma mère EST MORTE! Je ne sais pas si tu es capable de comprendre
> ça mais je ne VEUX PAS de chicane, je veux au contraire lui faire honneur
> en faisant le meilleur pour les enfants, je te dis que tu as eu raison de
> lui dire tu me reviens en t'obstinant sur un mot...Câline tu fais vraiment
> exprès pour que cela ne s'améliore pas.  Ça ne me dérange pas pour Noël si

**Citation disponible :**

```text
Louis Philippe, stp, les journées ne se reprennent pas. Le temps passe vite
et les enfants t'aiment beaucoup et je sais que tu les aimes.
```

### 55. `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/10_synthese_coherence_predictive_P2_P9_P16_P18_P19.md` ligne ~202 → `pq-97`

- **rang** 5.4 = score 9.3 × couverture 58%
- **termes partagés** : `samedi`, `mardi`, `l'école`, `garderie`, `dimanche`
- **source de la citation** : pdf-5 p.3 — 20150813 MJ projet consentement — trames 50

**Idée non étayée :**

> - la première semaine, du samedi matin au dimanche soir, soit une nuitée;
> - la deuxième semaine, du dimanche 16 h au mardi matin, soit **deux nuitées
>   consécutives**, avec retour à l'école ou à la garderie;
> - au total, trois nuitées sur quatorze.

**Citation disponible :**

```text
À partir du 29 août 2016 au 27 août 2017 : Semaine 1 De samedi 10h30 (directement à la piscine) au Lundi 8h00 directement à l'école et/ou la garderie; Semaine 2 Dimanche 16h00 au mardi 8h00 directement à l'école et/ou la garderie;
```

### 56. `legal/allegation_stmt56_57_58_assurances.md` ligne ~29 → `pq-30`

- **rang** 5.4 = score 21.5 × couverture 25%
- **termes partagés** : `group`, `insurance`, `conseiller`, `espace`, `demandes`, `règlement`
- **source de la citation** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> - **2015.pdf** - Relevé Industrielle Alliance (Espace conseiller, Group Insurance), demandes de règlement 1 janv.-31 déc. 2015.
> - **2016.pdf** - Relevé Industrielle Alliance, demandes de règlement 1 janv.-31 déc. 2016.
> - **Jugement_1.pdf** - Procès-verbal d'audience, Hon. Sophie Picard j.c.s., district de Longueuil, dossier 505-04-024603-151, 14 janvier 2016 (jugement par défaut).

**Citation disponible :**

```text
Espace conseiller - Group Insurance - Participant Page 1 sur 2

## Critères de recherche

Du | Au | Statut
:---|:---|:---
1 janvier 2015 | 31 décembre 2015 | Payé

## Demandes de règlement

| Statut | Date d'effet du statut | Nom (Lien familial) | Type règlement | Période | Montant soumis | Montant Payé | Payé à | Numéro de chèque |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
```

### 57. `legal/allegation_stmt19_20_21_acces.md` ligne ~104 → `pq-58`

- **rang** 5.4 = score 10.9 × couverture 49%
- **termes partagés** : `dpj`, `développement`, `sécurité`, `conjugale`, `violence`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> 9. Les circonstances documentées aux faits 1 et 2 - violence conjugale alléguée depuis la naissance d'Alexia, compromission possible de sa sécurité et de son développement et risque d'intervention de la DPJ - sont suffisamment graves pour rendre objectivement cohérente une conduite prudente quant aux conditions d'accès. Elles ne sont pas établies comme la cause subjective exclusive de chacune des décisions du demandeur.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
```

### 58. `legal/compilation_griefs.md` ligne ~1241 → `pq-102`

- **rang** 5.3 = score 14.1 × couverture 38%
- **termes partagés** : `fournisseur`, `transaction`, `paiement`, `type`, `direct`, `d'accès`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 1. Le **17 octobre 2015** (un **samedi**), une transaction de type P (Paiement Direct au fournisseur) a été effectuée au bénéfice de **Nicolas (santé)** - **hors** du seul créneau d'accès du défendeur (dimanche 16-20h ; voir fait 5). C'est la **dernière** transaction avant la rédaction de la Requête du 19 novembre 2015.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

### 59. `legal/faits/faits_par10_2015.md` ligne ~22 → `pq-16`

- **rang** 5.3 = score 9.3 × couverture 57%
- **termes partagés** : `marchande`, `fins`, `valeur`, `partage`
- **source de la citation** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 20

**Idée non étayée :**

> **66.4.** Le 27 juin 2013, l'évaluateur Louis-Philippe Robert reçoit le mandat d'évaluer la valeur marchande de la maison au 245 avenue Macaulay, Saint-Lambert, à des fins de partage (PDFDocument id=11).

**Citation disponible :**

```text
Étude de la valeur marchande en date des présentes à des fins de partage
```

### 60. `legal/pont/pont_par10_2015.md` ligne ~65 → `pq-16`

- **rang** 5.3 = score 9.3 × couverture 57%
- **termes partagés** : `marchande`, `fins`, `valeur`, `partage`
- **source de la citation** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 20

**Idée non étayée :**

> 1. En août 2009, les parties ont acquis conjointement la résidence familiale au 245, avenue Macaulay, à Saint-Lambert.
> 2. Le 11 juin 2013, Me Marie-Josée Ayoub a écrit à la demanderesse un plan prévoyant l'usage exclusif de la résidence familiale, la relocalisation du défendeur et le paiement par lui de 50 % des charges afférentes à la maison.
> 3. Le 26 juin 2013, le défendeur a écrit à Me Suzanne Pringle que la soeur avocate de sa conjointe la guidait « de façon à [le] piéger » et que la demanderesse lui écrivait qu'elle le trouvait agressif et avait peur de lui.
> 4. Le 27 juin 2013, le défendeur a écrit à son supérieur : « je dois vendre ma maison ».
> 5. Le même jour, il a mandaté l'évaluateur agréé Louis-Philippe Robert pour établir la valeur marchande de la résidence à des fins de partage.
> 6. Le 28 juin 2013, l'évaluateur a inspecté la propriété.
> 7. Le 11 juillet 2013, l'évaluateur a produit son rapport d'évaluation marchande à des fins de partage.
> 8. Le 1er août 2014, le défendeur a vendu sa part de la résidence à la demanderesse au prix établi par ce rapport.

**Citation disponible :**

```text
Étude de la valeur marchande en date des présentes à des fins de partage
```

### 61. `legal/ponts_requete_2015_consolides.md` ligne ~798 → `pq-16`

- **rang** 5.3 = score 9.3 × couverture 57%
- **termes partagés** : `marchande`, `fins`, `valeur`, `partage`
- **source de la citation** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 20

**Idée non étayée :**

> 1. En août 2009, les parties ont acquis conjointement la résidence familiale au 245, avenue Macaulay, à Saint-Lambert.
> 2. Le 11 juin 2013, Me Marie-Josée Ayoub a écrit à la demanderesse un plan prévoyant l'usage exclusif de la résidence familiale, la relocalisation du défendeur et le paiement par lui de 50 % des charges afférentes à la maison.
> 3. Le 26 juin 2013, le défendeur a écrit à Me Suzanne Pringle que la soeur avocate de sa conjointe la guidait « de façon à [le] piéger » et que la demanderesse lui écrivait qu'elle le trouvait agressif et avait peur de lui.
> 4. Le 27 juin 2013, le défendeur a écrit à son supérieur : « je dois vendre ma maison ».
> 5. Le même jour, il a mandaté l'évaluateur agréé Louis-Philippe Robert pour établir la valeur marchande de la résidence à des fins de partage.
> 6. Le 28 juin 2013, l'évaluateur a inspecté la propriété.
> 7. Le 11 juillet 2013, l'évaluateur a produit son rapport d'évaluation marchande à des fins de partage.
> 8. Le 1er août 2014, le défendeur a vendu sa part de la résidence à la demanderesse au prix établi par ce rapport.

**Citation disponible :**

```text
Étude de la valeur marchande en date des présentes à des fins de partage
```

### 62. `legal/journal_ete2013.md` ligne ~25 → `pq-16`

- **rang** 5.3 = score 9.3 × couverture 57%
- **termes partagés** : `marchande`, `fins`, `valeur`, `partage`
- **source de la citation** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 20

**Idée non étayée :**

> **2013-06-27** - PDFDocument PDF11 : LP reçoit l'étude de la valeur marchande de la résidence familiale (245 avenue Macaulay, Saint-Lambert) commandée aux fins de partage. LP est à Saint-Lambert et est activement impliqué dans le règlement des affaires familiales.

**Citation disponible :**

```text
Étude de la valeur marchande en date des présentes à des fins de partage
```

### 63. `legal/compilation_griefs.md` ligne ~510 → `pq-16`

- **rang** 5.3 = score 9.3 × couverture 57%
- **termes partagés** : `marchande`, `fins`, `valeur`, `partage`
- **source de la citation** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 20

**Idée non étayée :**

> 3. Le 27 juin 2013, le défendeur a mandaté l'évaluateur Louis-Philippe Robert pour établir la valeur marchande de la résidence à des fins de partage (PDFDocument id=11).

**Citation disponible :**

```text
Étude de la valeur marchande en date des présentes à des fins de partage
```

### 64. `legal/expose_faits_volet_2015.md` ligne ~139 → `pq-16`

- **rang** 5.3 = score 9.3 × couverture 57%
- **termes partagés** : `marchande`, `fins`, `valeur`, `partage`
- **source de la citation** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 20

**Idée non étayée :**

> 56. Le même jour, le demandeur a mandaté l'évaluateur agréé Louis-Philippe Robert pour établir la valeur marchande de la résidence à des fins de partage (pièce à coter : mandat et rapport).

**Citation disponible :**

```text
Étude de la valeur marchande en date des présentes à des fins de partage
```

### 65. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 20 21.md` ligne ~23 → `pq-58`

- **rang** 5.2 = score 10.7 × couverture 49%
- **termes partagés** : `compromis`, `développement`, `sécurité`, `conjugale`, `violence`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> - qualifié la situation de violence conjugale depuis la naissance d'Alexia;
> - affirmé que la sécurité et le développement de l'enfant pouvaient être considérés comme compromis;
> - envisagé une procédure urgente, la relocalisation du père, la garde exclusive à la mère et des accès sans coucher;
> - expliqué que le maintien de cette situation installerait une routine que les juges hésiteraient ensuite à modifier.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
```

### 66. `legal/dossier_plaidoirie/05_argumentaire_violence_substitution_interets_execution_plan.md` ligne ~170 → `pq-58`

- **rang** 5.2 = score 10.7 × couverture 49%
- **termes partagés** : `compromis`, `développement`, `sécurité`, `conjugale`, `violence`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> P‐2 ne décrit pas une simple mésentente conjugale. Le document affirme une
> violence vécue « depuis la naissance » et place la situation au seuil où la
> sécurité et le développement de l'enfant pourraient être compromis. La garde
> exclusive urgente, la sortie du père et l'absence de couchers correspondent à
> la gravité ainsi posée.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
```

### 67. `legal/pont/pont_par3_2019.md` ligne ~381 → `pq-58`

- **rang** 5.2 = score 10.7 × couverture 49%
- **termes partagés** : `compromis`, `développement`, `sécurité`, `conjugale`, `violence`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> - un **danger structurel** : violence conjugale depuis la naissance, sécurité et développement compromis ;
> - des **mesures initiales très restrictives** : accès sans coucher et relocalisation ;
> - un **objectif stable différent de ces mesures** : garde maternelle et contacts paternels plusieurs fois par semaine, davantage qu'une fin de semaine sur deux ;
> - la possibilité d'amender la procédure ou de régler même la veille du procès.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
```

### 68. `legal/ponts_requete_2019_consolides.md` ligne ~395 → `pq-58`

- **rang** 5.2 = score 10.7 × couverture 49%
- **termes partagés** : `compromis`, `développement`, `sécurité`, `conjugale`, `violence`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> - un **danger structurel** : violence conjugale depuis la naissance, sécurité et développement compromis ;
> - des **mesures initiales très restrictives** : accès sans coucher et relocalisation ;
> - un **objectif stable différent de ces mesures** : garde maternelle et contacts paternels plusieurs fois par semaine, davantage qu'une fin de semaine sur deux ;
> - la possibilité d'amender la procédure ou de régler même la veille du procès.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
```

### 69. `legal/faits/faits_par28-29_2015.md` ligne ~20 → `eq-203`

- **rang** 5.2 = score 17.4 × couverture 30%
- **termes partagés** : `heureux`, `profiter`, `aient`, `services`, `rendez`, `vous`
- **source de la citation** : email-180 — Re: renocntre — trames 69, 75

**Idée non étayée :**

> 5. Le 7 octobre, après qu'Écrement lui eut offert de devancer le rendez-vous, le demandeur a demandé l'annulation de celui du 19 octobre et a écrit être heureux que ses enfants aient pu profiter de ses services.

**Citation disponible :**

```text
Bon matin Mme Écremment, je ne pourais pas ce soir, de plus, je souhaites annuler mon rendez vous du 19. Je suis bien heureux que mes enfants aient pu profiter de vos services.
```

### 70. `legal/compilation_griefs.md` ligne ~2024 → `pq-79`

- **rang** 5.2 = score 15.0 × couverture 34%
- **termes partagés** : `montérégie`, `guichet`, `pharmacie`, `technicien`, `emplois`
- **source de la citation** : pdf-67 p.1 — Salaire Technicien/technicienne en pharmacie au Québec - 202 — trames 62

**Idée non étayée :**

> 234. Les emplois invoqués au §7 correspondent aux catégories définies par Me Ayoub dans la DA-2019 (analyste, technicien en laboratoire, représentant au service à la clientèle - services bancaires). Le Guichet-Emplois (Montérégie, janv. 2024) établit : technicien en pharmacie - **35 360 $/an** ; représentant au service à la clientèle - services financiers - **42 640 $/an**. Ces données constituant une **borne haute** pour 2019, les salaires 2019 étaient vraisemblablement inférieurs *(fait déductif - Guichet-Emplois + fait 212)*.

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION, Technicien/technicienne en pharmacie au Québec, Région de la Montérégie bas 15,25 median 17,00 haut 25,00 - Date de modification : 2023-01-23
```

### 71. `legal/compilation_griefs.md` ligne ~2040 → `pq-79`

- **rang** 5.2 = score 15.0 × couverture 34%
- **termes partagés** : `montérégie`, `guichet`, `pharmacie`, `technicien`, `emplois`
- **source de la citation** : pdf-67 p.1 — Salaire Technicien/technicienne en pharmacie au Québec - 202 — trames 62

**Idée non étayée :**

> 237. La DA-2019 (rédigée par Me Ayoub) définit le profil du Demandeur en trois catégories (analyste, technicien en laboratoire, représentant au service à la clientèle - services financiers). Le Guichet-Emplois (Montérégie, 2019) établit : technicien en pharmacie - **31 470 $/an** ; représentant au service à la clientèle - services financiers - **37 939 $/an**. Ces niveaux sont **inférieurs** au revenu déclaré 2019 (46 743,58 $) et aux revenus d'emploi 2018 (47 520,51 $) *(fait déductif)*.

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION, Technicien/technicienne en pharmacie au Québec, Région de la Montérégie bas 15,25 median 17,00 haut 25,00 - Date de modification : 2023-01-23
```

### 72. `legal/faits/faits_par7-8_2023.md` ligne ~140 → `pq-79`

- **rang** 5.2 = score 15.0 × couverture 34%
- **termes partagés** : `montérégie`, `guichet`, `pharmacie`, `technicien`, `emplois`
- **source de la citation** : pdf-67 p.1 — Salaire Technicien/technicienne en pharmacie au Québec - 202 — trames 62

**Idée non étayée :**

> 234. Les emplois invoqués au §7 correspondent aux catégories définies par Me Ayoub dans la DA-2019 (analyste, technicien en laboratoire, représentant au service à la clientèle - services bancaires). Le Guichet-Emplois (Montérégie, janv. 2024) établit : technicien en pharmacie - **35 360 $/an** ; représentant au service à la clientèle - services financiers - **42 640 $/an**. Ces données constituant une **borne haute** pour 2019, les salaires 2019 étaient vraisemblablement inférieurs *(fait déductif - Guichet-Emplois + fait 212)*.

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION, Technicien/technicienne en pharmacie au Québec, Région de la Montérégie bas 15,25 median 17,00 haut 25,00 - Date de modification : 2023-01-23
```

### 73. `legal/faits/faits_par7-8_2023.md` ligne ~156 → `pq-79`

- **rang** 5.2 = score 15.0 × couverture 34%
- **termes partagés** : `montérégie`, `guichet`, `pharmacie`, `technicien`, `emplois`
- **source de la citation** : pdf-67 p.1 — Salaire Technicien/technicienne en pharmacie au Québec - 202 — trames 62

**Idée non étayée :**

> 237. La DA-2019 (rédigée par Me Ayoub) définit le profil du Demandeur en trois catégories (analyste, technicien en laboratoire, représentant au service à la clientèle - services financiers). Le Guichet-Emplois (Montérégie, 2019) établit : technicien en pharmacie - **31 470 $/an** ; représentant au service à la clientèle - services financiers - **37 939 $/an**. Ces niveaux sont **inférieurs** au revenu déclaré 2019 (46 743,58 $) et aux revenus d'emploi 2018 (47 520,51 $) *(fait déductif)*.

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION, Technicien/technicienne en pharmacie au Québec, Région de la Montérégie bas 15,25 median 17,00 haut 25,00 - Date de modification : 2023-01-23
```

### 74. `legal/analyse/Responsabilité civile/courriel 11 juin 2013 - responsabilite de Me Ayoub.md` ligne ~205 → `pq-60`

- **rang** 5.0 = score 9.3 × couverture 54%
- **termes partagés** : `n'entend`, `témoin`, `juge`, `procédure`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> **Axe 1 - la connaissance de l'*exigence probante* (tirée de la profession, confirmée par le document).**
> On n'évalue pas abstraitement toutes les formes possibles d'une procédure ; on évalue ce que **la proposition opérationnelle de Me Ayoub impliquait nécessairement** au moment où elle l'a formulée. En sa qualité d'avocate, elle savait ou devait savoir que :
> - une **plaidoirie** d'avocat **ne constitue pas une preuve** ;
> - l'éviction du père, l'usage exclusif de la résidence et la restriction des accès **exigeaient une base factuelle admissible** ;
> - des faits **contestés** relevant de la **connaissance personnelle d'Élise** devaient être introduits par un **mode de preuve reconnu** ;
> - l'**absence de témoignages oraux** (« le juge n'entend pas de témoin ») **ne supprimait pas** cette exigence probatoire ;
> - la procédure projetée devait donc comprendre une preuve **écrite, documentaire, testimoniale assermentée ou déjà admise**.

**Citation disponible :**

```text
Lors de cette procédure d'urgence le juge en question n'entend pas de témoin c'est seulement les avocats qui plaident.
```

### 75. `legal/organisation_preuve/2023_par_7_8.md` ligne ~228 → `pq-80`

- **rang** 5.0 = score 10.1 × couverture 50%
- **termes partagés** : `reer`, `revenus`, `emploi`, `total`, `revenu`
- **source de la citation** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> 16. **La comparaison entre salaire et revenu total demeure une inférence.** Les revenus totaux incluent de l'assurance-emploi et des retraits de REER qui ne sont pas équivalents à un salaire récurrent.

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

### 76. `legal/expose_faits_volet_2015.md` ligne ~135 → `eq-150`

- **rang** 5.0 = score 17.4 × couverture 29%
- **termes partagés** : `piéger`, `agressif`, `trouvait`, `peur`, `conjointe`, `façon`, `avocate`
- **source de la citation** : email-365 — Conseils — trames 72

**Idée non étayée :**

> 54. Le 26 juin 2013, le demandeur écrivait à Me Suzanne Pringle que la sœur avocate de sa conjointe la guidait « de façon à [le] piéger » et que la défenderesse lui écrivait qu'elle le trouvait agressif et avait peur de lui (pièce à coter : Email id=365 ; renonciation à délimiter).

**Citation disponible :**

```text
Je vous contacte parce que je suis incapable de gérer cette
situation seule et de manière appropriée, la sœur de ma conjointe est
avocate et la guide de façon à me piéger.
J’ai coupé toute communication avec ma conjointe ce matin du fait que sans
raison elle m’écrive qu’elle trouvait que j’étais agressif et qu’elle avait
peur de moi.
```

### 77. `legal/dossier_plaidoirie/01_arc_garde_2013-2016.md` ligne ~1261 → `pq-98`

- **rang** 4.9 = score 8.9 × couverture 55%
- **termes partagés** : `samedi`, `mercredi`, `matin`, `garderie`, `dimanche`
- **source de la citation** : pdf-5 p.3 — 20150813 MJ projet consentement — trames 50

**Idée non étayée :**

> **Offre du 27 avril 2015 (¶ 72)** - Semaine 1 : mercredi après la garderie →
> jeudi matin à la garderie; samedi 14 h → dimanche 16 h. Semaine 2 : mercredi
> après la garderie → jeudi matin; dimanche 15 h → 20 h.

**Citation disponible :**

```text
Du 28 août 2017 au 25 août 2018 : Semaine 1 De samedi 10h30 (directement à la piscine) au Lundi 8h00 directement à l'école et/ou la garderie; Semaine 2 Dimanche 16h00 à mercredi matin à l'école et/ou la garderie;
```

### 78. `legal/pont/pont_par56-57_2015.md` ligne ~33 → `pq-101`

- **rang** 4.9 = score 11.0 × couverture 44%
- **termes partagés** : `fournisseur`, `paiements`, `directs`, `hors`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> - L'absence de veto établit que le défendeur ne pouvait discriminer entre les réclamations selon l'identité de l'accompagnateur.
> - Les relevés établissent objectivement seize demandes au bénéfice des enfants : treize paiements au fournisseur et trois remboursements au participant. Rapprochées du §20, leurs dates excluent le défendeur comme accompagnateur.
> - La combinaison démontre que l'utilisation effective hors de sa présence ne dépendait pas de son autorisation. Il est inutile d'identifier positivement l'autre adulte présent.
> - La connaissance personnelle de chaque transaction par la demanderesse doit être établie séparément avant d'en tirer une conclusion relative à son état d'esprit.
> - Aucun document ne rapporte une demande de remise des dépôts directs ou de paiement d'une différence déterminée, ni le refus d'une telle demande. Le seul dépôt au compte du participant ne constitue pas une réponse négative.

**Citation disponible :**

```text
Transactions 2016 — Paiements directs au fournisseur (type P) : 11 jan (Nicolas/Santé), 10 fév (Nicolas/Santé), 27 fév (Nicolas/Santé), 4 mai (Nicolas/Santé), 16 mai (Alexia/Santé). Toutes hors dimanche.
```

### 79. `legal/ponts_requete_2015_consolides.md` ligne ~1585 → `pq-101`

- **rang** 4.9 = score 11.0 × couverture 44%
- **termes partagés** : `fournisseur`, `paiements`, `directs`, `hors`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> - L'absence de veto établit que le défendeur ne pouvait discriminer entre les réclamations selon l'identité de l'accompagnateur.
> - Les relevés établissent objectivement seize demandes au bénéfice des enfants : treize paiements au fournisseur et trois remboursements au participant. Rapprochées du §20, leurs dates excluent le défendeur comme accompagnateur.
> - La combinaison démontre que l'utilisation effective hors de sa présence ne dépendait pas de son autorisation. Il est inutile d'identifier positivement l'autre adulte présent.
> - La connaissance personnelle de chaque transaction par la demanderesse doit être établie séparément avant d'en tirer une conclusion relative à son état d'esprit.
> - Aucun document ne rapporte une demande de remise des dépôts directs ou de paiement d'une différence déterminée, ni le refus d'une telle demande. Le seul dépôt au compte du participant ne constitue pas une réponse négative.

**Citation disponible :**

```text
Transactions 2016 — Paiements directs au fournisseur (type P) : 11 jan (Nicolas/Santé), 10 fév (Nicolas/Santé), 27 fév (Nicolas/Santé), 4 mai (Nicolas/Santé), 16 mai (Alexia/Santé). Toutes hors dimanche.
```

### 80. `legal/piece_thread-6_reconstruction.md` ligne ~81 → `eq-156`

- **rang** 4.9 = score 11.8 × couverture 41%
- **termes partagés** : `préfères`, `sois`, `toi`, `besoin`, `vie`
- **source de la citation** : email-4 — Re: suite des choses — trames 62

**Idée non étayée :**

> Encore une fois que tu ne sois pas d'accord ou que tu ne comprennes pas
> moins de vue par la rapport à ce qui était en mars 2015 n'a rien à voir
> avec ce qui se passe aujourd'hui...on est pas daccord, il y a juste toi qui
> continues de m'insulter car tu préfères faire ça que juste accepter qu'on
> était pas du même avis. Les enfants je m'en occupe et je ne te demande pas
> de t'organiser avec quand tu les vois justement, ça ne change rien pour moi
> que tu les prennes le dimanche soir, tu penses que ça change quelque chose
> dans ma vie à moi? Non. Car si j'ai besoin de faire quelque chose, j'ai des

**Citation disponible :**

```text
Dommage tout ce temps perdu!  Tes enfants ont besoin que tu sois dans leur vie et toi tu préfères t’accrocher à un courriel qui date d’environ 5 ans…
```

### 81. `legal/compilation_griefs.md` ligne ~2024 → `pq-78`

- **rang** 4.8 = score 18.4 × couverture 26%
- **termes partagés** : `guichet`, `clientèle`, `représentant`, `financiers`, `emplois`, `services`, `service`
- **source de la citation** : pdf-66 p.1 — Revenus représentant au service à la clientèle — trames 62

**Idée non étayée :**

> 234. Les emplois invoqués au §7 correspondent aux catégories définies par Me Ayoub dans la DA-2019 (analyste, technicien en laboratoire, représentant au service à la clientèle - services bancaires). Le Guichet-Emplois (Montérégie, janv. 2024) établit : technicien en pharmacie - **35 360 $/an** ; représentant au service à la clientèle - services financiers - **42 640 $/an**. Ces données constituant une **borne haute** pour 2019, les salaires 2019 étaient vraisemblablement inférieurs *(fait déductif - Guichet-Emplois + fait 212)*.

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION Représentant/représentante au service à la clientèle - services financiers au Québec Date de modification : 2024-01-23
Région de Montréal Salaire Bas : 16,28 Median 21,00 Haut : 26,99 
https://www.guichet-emplois.gc.ca/salaire-horaire/representant-representante-service-clientele-services-financiers/montreal
```

### 82. `legal/compilation_griefs.md` ligne ~2040 → `pq-78`

- **rang** 4.8 = score 18.4 × couverture 26%
- **termes partagés** : `guichet`, `clientèle`, `représentant`, `financiers`, `emplois`, `services`, `service`
- **source de la citation** : pdf-66 p.1 — Revenus représentant au service à la clientèle — trames 62

**Idée non étayée :**

> 237. La DA-2019 (rédigée par Me Ayoub) définit le profil du Demandeur en trois catégories (analyste, technicien en laboratoire, représentant au service à la clientèle - services financiers). Le Guichet-Emplois (Montérégie, 2019) établit : technicien en pharmacie - **31 470 $/an** ; représentant au service à la clientèle - services financiers - **37 939 $/an**. Ces niveaux sont **inférieurs** au revenu déclaré 2019 (46 743,58 $) et aux revenus d'emploi 2018 (47 520,51 $) *(fait déductif)*.

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION Représentant/représentante au service à la clientèle - services financiers au Québec Date de modification : 2024-01-23
Région de Montréal Salaire Bas : 16,28 Median 21,00 Haut : 26,99 
https://www.guichet-emplois.gc.ca/salaire-horaire/representant-representante-service-clientele-services-financiers/montreal
```

### 83. `legal/faits/faits_par7-8_2023.md` ligne ~140 → `pq-78`

- **rang** 4.8 = score 18.4 × couverture 26%
- **termes partagés** : `guichet`, `clientèle`, `représentant`, `financiers`, `emplois`, `services`, `service`
- **source de la citation** : pdf-66 p.1 — Revenus représentant au service à la clientèle — trames 62

**Idée non étayée :**

> 234. Les emplois invoqués au §7 correspondent aux catégories définies par Me Ayoub dans la DA-2019 (analyste, technicien en laboratoire, représentant au service à la clientèle - services bancaires). Le Guichet-Emplois (Montérégie, janv. 2024) établit : technicien en pharmacie - **35 360 $/an** ; représentant au service à la clientèle - services financiers - **42 640 $/an**. Ces données constituant une **borne haute** pour 2019, les salaires 2019 étaient vraisemblablement inférieurs *(fait déductif - Guichet-Emplois + fait 212)*.

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION Représentant/représentante au service à la clientèle - services financiers au Québec Date de modification : 2024-01-23
Région de Montréal Salaire Bas : 16,28 Median 21,00 Haut : 26,99 
https://www.guichet-emplois.gc.ca/salaire-horaire/representant-representante-service-clientele-services-financiers/montreal
```

### 84. `legal/faits/faits_par7-8_2023.md` ligne ~156 → `pq-78`

- **rang** 4.8 = score 18.4 × couverture 26%
- **termes partagés** : `guichet`, `clientèle`, `représentant`, `financiers`, `emplois`, `services`, `service`
- **source de la citation** : pdf-66 p.1 — Revenus représentant au service à la clientèle — trames 62

**Idée non étayée :**

> 237. La DA-2019 (rédigée par Me Ayoub) définit le profil du Demandeur en trois catégories (analyste, technicien en laboratoire, représentant au service à la clientèle - services financiers). Le Guichet-Emplois (Montérégie, 2019) établit : technicien en pharmacie - **31 470 $/an** ; représentant au service à la clientèle - services financiers - **37 939 $/an**. Ces niveaux sont **inférieurs** au revenu déclaré 2019 (46 743,58 $) et aux revenus d'emploi 2018 (47 520,51 $) *(fait déductif)*.

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION Représentant/représentante au service à la clientèle - services financiers au Québec Date de modification : 2024-01-23
Région de Montréal Salaire Bas : 16,28 Median 21,00 Haut : 26,99 
https://www.guichet-emplois.gc.ca/salaire-horaire/representant-representante-service-clientele-services-financiers/montreal
```

### 85. `legal/piece_thread-6_reconstruction.md` ligne ~309 → `eq-116` — *citation encore inexploitée*

- **rang** 4.8 = score 10.5 × couverture 46%
- **termes partagés** : `dedans`, `tes`, `rien`
- **source de la citation** : email-319 — Re: dimanche prochain — trames —

**Idée non étayée :**

> *Pourquoi mêler ma soeur la dedans? Je n'en sais rien, ton constant besoin
> de vouloir blâmer ma soeur ou moi ne change en rien que ce sont tes enfants
> pas juste les miens, et que si ne veux pas être leur père c'est ton choix.*

**Citation disponible :**

```text
Qu'est ce que ça va prendre pour que tu comprennes que tes enfants n'ont rien à voir là dedans?
```

### 86. `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/10_synthese_coherence_predictive_P2_P9_P16_P18_P19.md` ligne ~202 → `pq-98`

- **rang** 4.8 = score 8.8 × couverture 55%
- **termes partagés** : `samedi`, `l'école`, `matin`, `garderie`, `dimanche`
- **source de la citation** : pdf-5 p.3 — 20150813 MJ projet consentement — trames 50

**Idée non étayée :**

> - la première semaine, du samedi matin au dimanche soir, soit une nuitée;
> - la deuxième semaine, du dimanche 16 h au mardi matin, soit **deux nuitées
>   consécutives**, avec retour à l'école ou à la garderie;
> - au total, trois nuitées sur quatorze.

**Citation disponible :**

```text
Du 28 août 2017 au 25 août 2018 : Semaine 1 De samedi 10h30 (directement à la piscine) au Lundi 8h00 directement à l'école et/ou la garderie; Semaine 2 Dimanche 16h00 à mercredi matin à l'école et/ou la garderie;
```

### 87. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 56 57.md` ligne ~126 → `pq-101`

- **rang** 4.8 = score 10.9 × couverture 44%
- **termes partagés** : `fournisseur`, `paiements`, `transactions`, `hors`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 1. les seize transactions, soit treize paiements au fournisseur et trois remboursements au participant, ont eu lieu lorsque la Requête ne situe pas les enfants avec lui ;
> 2. il n'avait aucun pouvoir d'autorisation transaction par transaction ;
> 3. l'identité de l'accompagnateur n'affectait pas l'admissibilité de l'enfant ;
> 4. les prestations étaient donc utilisées hors de sa présence sans dépendre de sa permission ;
> 5. aucun événement constitutif d'un refus - demande communiquée, connaissance et réponse négative - n'est documenté, que ce soit pour l'utilisation de l'assurance ou pour la remise d'un remboursement.

**Citation disponible :**

```text
Transactions 2016 — Paiements directs au fournisseur (type P) : 11 jan (Nicolas/Santé), 10 fév (Nicolas/Santé), 27 fév (Nicolas/Santé), 4 mai (Nicolas/Santé), 16 mai (Alexia/Santé). Toutes hors dimanche.
```

### 88. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 56 57.md` ligne ~136 → `pq-101`

- **rang** 4.8 = score 10.9 × couverture 44%
- **termes partagés** : `fournisseur`, `paiements`, `transactions`, `hors`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> La réfutation résulte de la **combinaison** de la structure du régime et des relevés. Les seize transactions - treize paiements au fournisseur et trois remboursements au participant - ont eu lieu lorsque, selon la Requête, les enfants n'étaient pas avec le défendeur. Le défendeur ne pouvait par ailleurs ni les autoriser ni les refuser selon l'identité de l'accompagnateur. Elles étaient donc effectuées hors de sa présence sans dépendre de sa permission. Cette combinaison réfute l'intégralité du refus d'utilisation du §57 et du monopole allégué dans la première branche du §57a.

**Citation disponible :**

```text
Transactions 2016 — Paiements directs au fournisseur (type P) : 11 jan (Nicolas/Santé), 10 fév (Nicolas/Santé), 27 fév (Nicolas/Santé), 4 mai (Nicolas/Santé), 16 mai (Alexia/Santé). Toutes hors dimanche.
```

### 89. `legal/expose_faits_volet_2015.md` ligne ~139 → `pq-23`

- **rang** 4.7 = score 14.0 × couverture 34%
- **termes partagés** : `marchande`, `mandat`, `fins`, `valeur`, `partage`, `rapport`
- **source de la citation** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> 56. Le même jour, le demandeur a mandaté l'évaluateur agréé Louis-Philippe Robert pour établir la valeur marchande de la résidence à des fins de partage (pièce à coter : mandat et rapport).

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

### 90. `legal/chronologie_emploi_2018-2023.md` ligne ~39 → `eq-133`

- **rang** 4.7 = score 11.2 × couverture 42%
- **termes partagés** : `terminées`, `chômage`, `emploi`
- **source de la citation** : email-425 — Mise a jour — trames 62

**Idée non étayée :**

> - **Non-emploi : 29 juin 2018 → ≈ août 2019 (~13 mois)** - recherche active, transmise à Me Ayoub (15 oct. 2019).
> - **Chômage (A-E) : 22 juillet 2018 → ≈ mi-avril 2019 (38 sem.).**
> - **Revenu 2018 ≈ 64 k = COMPOSITE** : emploi BNC (janv.-29 juin) **+** assurance-emploi (juill.-déc.) - les **deux sources sont terminées** (emploi perdu, A-E épuisée). C'est ce 2018 composite qui sert d'assise au « 65 k » imputé.
> - **Revenu 2019 = A-E + retrait REER** (survie), **non** un revenu d'emploi refusé.

**Citation disponible :**

```text
Salut MJ, Mes 38 semaines de chômage sont terminées. Je te laisserai savoir quand je me trouverai un emploi
```

### 91. `legal/allegation_stmt56_57_58_assurances.md` ligne ~39 → `pq-102`

- **rang** 4.7 = score 13.2 × couverture 35%
- **termes partagés** : `fournisseur`, `paiement`, `service`, `type`, `direct`, `point`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> - **Type P** : l'assureur verse la portion couverte au fournisseur ; la personne présente au point de service n'avance que le solde non couvert.
> - **Type N** : la dépense est déboursée intégralement hors du paiement direct, puis l'assureur verse la portion couverte au compte du participant. Le relevé n'identifie pas la personne qui a fait le débours initial.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

### 92. `legal/piece_pdf-63.md` ligne ~14 → `pq-102`

- **rang** 4.7 = score 13.2 × couverture 35%
- **termes partagés** : `fournisseur`, `paiement`, `service`, `type`, `direct`, `point`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> - **Type (P) = Paiement au fournisseur** : l'assureur verse directement au fournisseur la portion couverte ; la personne présente au point de service n'avance que le solde non couvert.
> - **Type (N) = Dépôt Direct au participant** : la dépense est d'abord déboursée intégralement hors du mécanisme de paiement direct, puis l'assureur verse la portion couverte au **compte du participant**. Le relevé n'identifie pas la personne qui a fait le débours initial.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

### 93. `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/02_securite_fondement_objectif.md` ligne ~11 → `pq-58`

- **rang** 4.6 = score 10.1 × couverture 46%
- **termes partagés** : `intervenant`, `dpj`, `sécurité`, `conjugale`, `violence`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> L'analyse distingue le fondement allégué de l'intervention - l'affirmation
> qu'Alexia vit dans la violence conjugale et la prédiction qu'un intervenant de
> la DPJ pourrait conclure à une compromission - des résultats opérationnels du
> plan. Elle soutient que la sécurité justifie l'urgence sans constituer un
> objectif documenté et structurant.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
```

### 94. `legal/requete_secton_faits_lp.md` ligne ~1161 → `pq-80`

- **rang** 4.6 = score 9.6 × couverture 48%
- **termes partagés** : `reer`, `prestations`, `d'assurance`, `emploi`
- **source de la citation** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> 399-M. Les prestations d'assurance-emploi de 12 034,00 $ et les prestations d'un régime de retraite ou d'un REER de 4 089,60 $ du demandeur sont ainsi comprises dans la somme inscrite à la ligne « Salaire brut » plutôt qu'aux lignes qui leur sont propres.

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

### 95. `legal/allegation_stmt14_15_16_17_garde_partagee.md` ligne ~211 → `eq-119` — *citation encore inexploitée*

- **rang** 4.6 = score 10.5 × couverture 44%
- **termes partagés** : `respecter`, `parler`, `comprendre`, `moins`
- **source de la citation** : email-295 — Re: Visite — trames —

**Idée non étayée :**

> 6. Le 16 septembre 2016 à 12 h 07, la demanderesse invoque aussi l'« incapacité à se comprendre » et affirme que les parents en garde partagée sont au moins capables de se comprendre, de se parler et de se respecter (Email id=295).

**Citation disponible :**

```text
On ne se comprend pas, on a toujours eu de la difficulté, les gens en garde partagée sont au moins capable de se comprendre, de se parler et de se respecter. Nous non...
```

### 96. `legal/allegation_stmt19_20_21_acces.md` ligne ~104 → `pq-34`

- **rang** 4.6 = score 10.9 × couverture 42%
- **termes partagés** : `dpj`, `développement`, `sécurité`, `conjugale`, `violence`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 48

**Idée non étayée :**

> 9. Les circonstances documentées aux faits 1 et 2 - violence conjugale alléguée depuis la naissance d'Alexia, compromission possible de sa sécurité et de son développement et risque d'intervention de la DPJ - sont suffisamment graves pour rendre objectivement cohérente une conduite prudente quant aux conditions d'accès. Elles ne sont pas établies comme la cause subjective exclusive de chacune des décisions du demandeur.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Tu dois le faire sortir de la maison [...]
```

### 97. `legal/analyse/Responsabilité civile/requete 21 juillet 2023/DMD2023 paragraphes7 8 responsabilite civile.md` ligne ~33 → `pq-78`

- **rang** 4.4 = score 17.6 × couverture 25%
- **termes partagés** : `représentante`, `clientèle`, `représentant`, `financiers`, `services`, `service`
- **source de la citation** : pdf-66 p.1 — Revenus représentant au service à la clientèle — trames 62

**Idée non étayée :**

> - **Technicien/technicienne en pharmacie** : 17,00 $/heure - soit 35 360 $ annuellement
> - **Représentant/représentante au service à la clientèle - services financiers** : 20,50 $/heure - soit 42 640 $ annuellement

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION Représentant/représentante au service à la clientèle - services financiers au Québec Date de modification : 2024-01-23
Région de Montréal Salaire Bas : 16,28 Median 21,00 Haut : 26,99 
https://www.guichet-emplois.gc.ca/salaire-horaire/representant-representante-service-clientele-services-financiers/montreal
```

### 98. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 20 21.md` ligne ~23 → `pq-34`

- **rang** 4.4 = score 10.7 × couverture 41%
- **termes partagés** : `compromis`, `développement`, `sécurité`, `conjugale`, `violence`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 48

**Idée non étayée :**

> - qualifié la situation de violence conjugale depuis la naissance d'Alexia;
> - affirmé que la sécurité et le développement de l'enfant pouvaient être considérés comme compromis;
> - envisagé une procédure urgente, la relocalisation du père, la garde exclusive à la mère et des accès sans coucher;
> - expliqué que le maintien de cette situation installerait une routine que les juges hésiteraient ensuite à modifier.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Tu dois le faire sortir de la maison [...]
```

### 99. `legal/dossier_plaidoirie/05_argumentaire_violence_substitution_interets_execution_plan.md` ligne ~170 → `pq-34`

- **rang** 4.4 = score 10.7 × couverture 41%
- **termes partagés** : `compromis`, `développement`, `sécurité`, `conjugale`, `violence`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 48

**Idée non étayée :**

> P‐2 ne décrit pas une simple mésentente conjugale. Le document affirme une
> violence vécue « depuis la naissance » et place la situation au seuil où la
> sécurité et le développement de l'enfant pourraient être compromis. La garde
> exclusive urgente, la sortie du père et l'absence de couchers correspondent à
> la gravité ainsi posée.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Tu dois le faire sortir de la maison [...]
```

### 100. `legal/pont/pont_par3_2019.md` ligne ~381 → `pq-34`

- **rang** 4.4 = score 10.7 × couverture 41%
- **termes partagés** : `compromis`, `développement`, `sécurité`, `conjugale`, `violence`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 48

**Idée non étayée :**

> - un **danger structurel** : violence conjugale depuis la naissance, sécurité et développement compromis ;
> - des **mesures initiales très restrictives** : accès sans coucher et relocalisation ;
> - un **objectif stable différent de ces mesures** : garde maternelle et contacts paternels plusieurs fois par semaine, davantage qu'une fin de semaine sur deux ;
> - la possibilité d'amender la procédure ou de régler même la veille du procès.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Tu dois le faire sortir de la maison [...]
```

### 101. `legal/ponts_requete_2019_consolides.md` ligne ~395 → `pq-34`

- **rang** 4.4 = score 10.7 × couverture 41%
- **termes partagés** : `compromis`, `développement`, `sécurité`, `conjugale`, `violence`, `naissance`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 48

**Idée non étayée :**

> - un **danger structurel** : violence conjugale depuis la naissance, sécurité et développement compromis ;
> - des **mesures initiales très restrictives** : accès sans coucher et relocalisation ;
> - un **objectif stable différent de ces mesures** : garde maternelle et contacts paternels plusieurs fois par semaine, davantage qu'une fin de semaine sur deux ;
> - la possibilité d'amender la procédure ou de régler même la veille du procès.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Tu dois le faire sortir de la maison [...]
```

### 102. `legal/axe_agenda_danse_elise.md` ligne ~97 → `eq-40`

- **rang** 4.4 = score 9.1 × couverture 49%
- **termes partagés** : `dansait`, `mardi`, `mercredi`, `dit`
- **source de la citation** : email-100 — Re: Alexia — trames 5, 64

**Idée non étayée :**

> 9. Le 9 décembre 2010, le demandeur a répondu à Johanne Bazinet qu'il lui avait déjà dit que les mardi et mercredi, la défenderesse dansait (P-X, Email 100).

**Citation disponible :**

```text
 mais je t'ai deja dit que les mardi et mercredi elise dansait.
```

### 103. `legal/these_test_sincerite_2013.md` ligne ~208 → `pq-58`

- **rang** 4.4 = score 9.9 × couverture 45%
- **termes partagés** : `intervenant`, `arriver`, `dpj`, `pourra`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> Or **la DPJ n'a jamais été saisie** - par la partie même qui invoquait son critère, et qui ne l'a mobilisée que comme **pronostic** de ce qu'un intervenant « pourra arriver à la conclusion » d'établir (premier étage, *infra* ; §IV.1). **La seule voie capable de combler l'écart était disponible, et elle a été écartée.**

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
```

### 104. `legal/these_test_sincerite_2013.md` ligne ~239 → `pq-58`

- **rang** 4.4 = score 9.9 × couverture 45%
- **termes partagés** : `intervenant`, `arriver`, `dpj`, `pourra`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> Le tell est net : **la DPJ n'est jamais saisie.** Elle n'est invoquée que comme *pronostic* de ce qu'un intervenant « pourra arriver à la conclusion » d'établir. On emprunte l'**autorité** du critère sans en accepter le **mécanisme**.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
```

### 105. `legal/compilation_griefs.md` ligne ~1241 → `pq-101`

- **rang** 4.3 = score 10.3 × couverture 41%
- **termes partagés** : `fournisseur`, `type`, `santé`, `hors`, `dimanche`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 1. Le **17 octobre 2015** (un **samedi**), une transaction de type P (Paiement Direct au fournisseur) a été effectuée au bénéfice de **Nicolas (santé)** - **hors** du seul créneau d'accès du défendeur (dimanche 16-20h ; voir fait 5). C'est la **dernière** transaction avant la rédaction de la Requête du 19 novembre 2015.

**Citation disponible :**

```text
Transactions 2016 — Paiements directs au fournisseur (type P) : 11 jan (Nicolas/Santé), 10 fév (Nicolas/Santé), 27 fév (Nicolas/Santé), 4 mai (Nicolas/Santé), 16 mai (Alexia/Santé). Toutes hors dimanche.
```

### 106. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~415 → `eq-122` — *citation encore inexploitée*

- **rang** 4.3 = score 9.6 × couverture 44%
- **termes partagés** : `d'incapable`, `d'attachement`, `parlé`, `lien`
- **source de la citation** : email-6 — Re: Visite — trames —

**Idée non étayée :**

> 171. Le 16 septembre 2016, la défenderesse a par ailleurs écrit au demandeur qu'elle ne l'avait jamais traité d'incapable et qu'elle lui avait plutôt parlé du lien d'attachement des enfants, comme il appert de l'échange produit comme pièce P-[12].

**Citation disponible :**

```text
[...] Je ne t'ai jamais traiter d'incapable je t'ai parlé de leur lien d'attachement, je ne t'ai jamais accusé de rien depuis que tu es parti [...]
```

### 107. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~415 → `eq-122` — *citation encore inexploitée*

- **rang** 4.3 = score 9.6 × couverture 44%
- **termes partagés** : `d'incapable`, `d'attachement`, `parlé`, `lien`
- **source de la citation** : email-6 — Re: Visite — trames —

**Idée non étayée :**

> 171. Le 16 septembre 2016, la défenderesse a par ailleurs écrit au demandeur qu'elle ne l'avait jamais traité d'incapable et qu'elle lui avait plutôt parlé du lien d'attachement des enfants, comme il appert de l'échange produit comme pièce P-[12].

**Citation disponible :**

```text
[...] Je ne t'ai jamais traiter d'incapable je t'ai parlé de leur lien d'attachement, je ne t'ai jamais accusé de rien depuis que tu es parti [...]
```

### 108. `legal/analyse/Responsabilité civile/courriel 11 juin 2013 - responsabilite de Me Ayoub.md` ligne ~96 → `pq-64`

- **rang** 4.2 = score 11.1 × couverture 38%
- **termes partagés** : `aille`, `qu'on`, `vendredi`, `vacances`, `cour`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> - qualification de l'ordonnance de sauvegarde;
> - choix du véhicule procédural;
> - identification des arguments à plaider;
> - description des conclusions recherchées;
> - calcul des effets résidentiels et financiers;
> - répétition du pronom « on » : « on appelle », « on plaide », « on accorde », « on l'oblige », « on peut demander »;
> - passage final à une action commune et datée : « qu'on aille à la cour vendredi »;
> - arrimage du calendrier aux vacances imminentes du père.

**Citation disponible :**

```text
[...] le meilleur moment pour lui envoyer la procédure est jeudi pour qu'on aille à la cour vendredi avant son départ. Une pierre deux coups. La procédure et tu lui gâche ses vacances [...]
```

### 109. `legal/analyse/Responsabilité civile/courriel 11 juin 2013 - responsabilite de Me Ayoub.md` ligne ~96 → `pq-53`

- **rang** 4.2 = score 11.1 × couverture 38%
- **termes partagés** : `aille`, `qu'on`, `vendredi`, `vacances`, `cour`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 55

**Idée non étayée :**

> - qualification de l'ordonnance de sauvegarde;
> - choix du véhicule procédural;
> - identification des arguments à plaider;
> - description des conclusions recherchées;
> - calcul des effets résidentiels et financiers;
> - répétition du pronom « on » : « on appelle », « on plaide », « on accorde », « on l'oblige », « on peut demander »;
> - passage final à une action commune et datée : « qu'on aille à la cour vendredi »;
> - arrimage du calendrier aux vacances imminentes du père.

**Citation disponible :**

```text
le meilleur moment pour lui envoyer la procédure est jeudi pour qu'on aille à la cour vendredi avant son départ. Une pierre deux coups. La procédure et tu lui gâche ses vacances
```

### 110. `legal/analyse/Responsabilité civile/courriel 11 juin 2013 - responsabilite de Me Ayoub.md` ligne ~96 → `pq-8`

- **rang** 4.2 = score 11.1 × couverture 38%
- **termes partagés** : `aille`, `qu'on`, `vendredi`, `vacances`, `cour`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 70

**Idée non étayée :**

> - qualification de l'ordonnance de sauvegarde;
> - choix du véhicule procédural;
> - identification des arguments à plaider;
> - description des conclusions recherchées;
> - calcul des effets résidentiels et financiers;
> - répétition du pronom « on » : « on appelle », « on plaide », « on accorde », « on l'oblige », « on peut demander »;
> - passage final à une action commune et datée : « qu'on aille à la cour vendredi »;
> - arrimage du calendrier aux vacances imminentes du père.

**Citation disponible :**

```text
le meilleur moment pour lui envoyer la procédure est jeudi pour qu'on aille à la cour vendredi avant son départ. Une pierre deux coups. La procédure et tu lui gâche ses vacances
```

### 111. `legal/pont/pont_par56-57_2015.md` ligne ~67 → `pq-100`

- **rang** 4.2 = score 9.8 × couverture 43%
- **termes partagés** : `utilisait`, `remboursements`, `participant`
- **source de la citation** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> - Ne pas chercher à identifier positivement la personne qui accompagnait les enfants ou présentait les renseignements d'assurance au point de service.
> - Les jours de transaction et les périodes de garde peuvent exclure le défendeur selon le récit de la Requête ; ils ne permettent pas, à eux seuls, d'identifier l'autre accompagnateur.
> - Ne pas confondre la fonction des deux éléments : les dates établissent l'absence factuelle du défendeur ; le mécanisme du régime établit son absence de veto. Leur combinaison porte la réfutation complète.
> - Ne pas affirmer que le défendeur ou la demanderesse « utilisait » personnellement l'assurance : les prestations étaient accordées au bénéfice des enfants.
> - Ne pas confondre l'acceptation d'une réclamation par l'assureur avec le versement ultérieur du remboursement au compte du participant.
> - Ne pas assimiler les remboursements de 88 $, qui correspondent aux montants couverts, aux soldes de 22 $ non couverts.
> - Ne pas attribuer le débours initial de 110 $ à la demanderesse ou au défendeur : le relevé ne l'identifie pas.
> - Ne pas affirmer que le défendeur a conservé ou refusé de remettre les dépôts : en l'absence d'une demande déterminée et de sa réponse, ce refus n'est pas établi.

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

### 112. `legal/ponts_requete_2015_consolides.md` ligne ~1619 → `pq-100`

- **rang** 4.2 = score 9.8 × couverture 43%
- **termes partagés** : `utilisait`, `remboursements`, `participant`
- **source de la citation** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> - Ne pas chercher à identifier positivement la personne qui accompagnait les enfants ou présentait les renseignements d'assurance au point de service.
> - Les jours de transaction et les périodes de garde peuvent exclure le défendeur selon le récit de la Requête ; ils ne permettent pas, à eux seuls, d'identifier l'autre accompagnateur.
> - Ne pas confondre la fonction des deux éléments : les dates établissent l'absence factuelle du défendeur ; le mécanisme du régime établit son absence de veto. Leur combinaison porte la réfutation complète.
> - Ne pas affirmer que le défendeur ou la demanderesse « utilisait » personnellement l'assurance : les prestations étaient accordées au bénéfice des enfants.
> - Ne pas confondre l'acceptation d'une réclamation par l'assureur avec le versement ultérieur du remboursement au compte du participant.
> - Ne pas assimiler les remboursements de 88 $, qui correspondent aux montants couverts, aux soldes de 22 $ non couverts.
> - Ne pas attribuer le débours initial de 110 $ à la demanderesse ou au défendeur : le relevé ne l'identifie pas.
> - Ne pas affirmer que le défendeur a conservé ou refusé de remettre les dépôts : en l'absence d'une demande déterminée et de sa réponse, ce refus n'est pas établi.

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

### 113. `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/10_synthese_coherence_predictive_P2_P9_P16_P18_P19.md` ligne ~168 → `pq-31`

- **rang** 4.1 = score 11.2 × couverture 37%
- **termes partagés** : `réitère`, `samedi`, `jeudi`, `mercredi`, `dimanche`
- **source de la citation** : pdf-3 p.2 — Réponse à l'offre de garde partagée — trames 46, 47, 49, 52, 55, 73, 76

**Idée non étayée :**

> Dans la même lettre, la position maternelle réitère pourtant une offre qui
> aurait modifié cette routine si elle avait été acceptée : deux nuitées du
> mercredi au jeudi, une chaque semaine, et une nuitée du samedi au dimanche la
> première semaine, soit trois nuitées par cycle de quatorze jours.

**Citation disponible :**

```text
notre cliente réitère son offre à l'élargissement des droits d'accès du père auprès de leurs enfants à savotr :
- Semaine 1 : 
- Du mercredi après la garderie et ce jusqu'au jeudi matin à la garderie; Du samedi 14h 00 au dimanche 16h00.
-Semaine 2 : 
-Du mercredi après la garderie et ce jusqu'au jeudi matin à la garderie; Dimanche de 15h00 à 20h00.
```

### 114. `legal/piece_thread-6_reconstruction.md` ligne ~81 → `eq-104`

- **rang** 4.1 = score 12.7 × couverture 32%
- **termes partagés** : `daccord`, `aujourd'hui`, `car`, `toi`, `quand`
- **source de la citation** : email-305 — Re: Visite — trames 55

**Idée non étayée :**

> Encore une fois que tu ne sois pas d'accord ou que tu ne comprennes pas
> moins de vue par la rapport à ce qui était en mars 2015 n'a rien à voir
> avec ce qui se passe aujourd'hui...on est pas daccord, il y a juste toi qui
> continues de m'insulter car tu préfères faire ça que juste accepter qu'on
> était pas du même avis. Les enfants je m'en occupe et je ne te demande pas
> de t'organiser avec quand tu les vois justement, ça ne change rien pour moi
> que tu les prennes le dimanche soir, tu penses que ça change quelque chose
> dans ma vie à moi? Non. Car si j'ai besoin de faire quelque chose, j'ai des

**Citation disponible :**

```text
je n'ai pas décidé de la situation actuelle, je n'étais simplement pas d,accord avec et toi et je paie le prix aujourd'hui de ça, car c'est comme ça quand on est pas daccord avec toi, il n'y avait aucune autre option selon toi.
```

### 115. `legal/dossier_plaidoirie/01_arc_garde_2013-2016.md` ligne ~1261 → `pq-31`

- **rang** 4.0 = score 11.1 × couverture 36%
- **termes partagés** : `samedi`, `jeudi`, `mercredi`, `matin`, `garderie`, `dimanche`
- **source de la citation** : pdf-3 p.2 — Réponse à l'offre de garde partagée — trames 46, 47, 49, 52, 55, 73, 76

**Idée non étayée :**

> **Offre du 27 avril 2015 (¶ 72)** - Semaine 1 : mercredi après la garderie →
> jeudi matin à la garderie; samedi 14 h → dimanche 16 h. Semaine 2 : mercredi
> après la garderie → jeudi matin; dimanche 15 h → 20 h.

**Citation disponible :**

```text
notre cliente réitère son offre à l'élargissement des droits d'accès du père auprès de leurs enfants à savotr :
- Semaine 1 : 
- Du mercredi après la garderie et ce jusqu'au jeudi matin à la garderie; Du samedi 14h 00 au dimanche 16h00.
-Semaine 2 : 
-Du mercredi après la garderie et ce jusqu'au jeudi matin à la garderie; Dimanche de 15h00 à 20h00.
```

### 116. `legal/faits_chronologiques_2010-11-20_2012-02-06.md` ligne ~120 → `eq-153`

- **rang** 4.0 = score 9.6 × couverture 42%
- **termes partagés** : `hugo`, `annie`, `merci`
- **source de la citation** : email-62 — Merci — trames 31

**Idée non étayée :**

> **56.** Le 9 mai 2011, la famille paternelle - grand-mère, sœur Annie-Claude et beau-frère Hugo Sarkisian - échange des remerciements pour un souper familial récent. Le Demandeur fait partie du fil. `[Emails id=62, 119 | Johanne Bazinet, Hugo Sarkisian, LP, Annie-Claude | Sujet : Merci]`

**Citation disponible :**

```text
merci à Annie et à
Hugo pour la préparation et à Louis-Philippe pour avoir répondu à ma demande
et de m'avoir laissé Alexia.
```

### 117. `legal/pont/pont_par56-57_2015.md` ligne ~99 → `pq-100`

- **rang** 4.0 = score 9.5 × couverture 42%
- **termes partagés** : `remboursements`, `participant`, `lorsqu'il`, `dépôt`
- **source de la citation** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 1. Les enfants étaient bénéficiaires du régime d'assurance collective auquel adhérait le demandeur.
> 2. Le demandeur ne conteste pas cette couverture.
> 3. Les relevés documentent treize transactions où l'assureur a payé la portion couverte au fournisseur et trois dépenses de 110 $ déboursées intégralement, suivies d'un remboursement de 88 $ au compte du participant.
> 4. Aucune de ces seize transactions n'a eu lieu un dimanche, alors que la Requête situe les accès du demandeur le dimanche de 16 h à 20 h ; selon le propre récit de la Requête, il n'était donc l'accompagnateur ou l'auteur matériel d'aucune d'elles.
> 5. Le demandeur ne pouvait par ailleurs autoriser ou refuser les réclamations individuelles : elles étaient traitées selon l'admissibilité de l'enfant, la dépense et les conditions du régime, sans distinction fondée sur l'identité de l'accompagnateur.
> 6. Les transactions avaient ainsi lieu hors de sa présence sans dépendre de sa permission.
> 7. Cette combinaison réfute tant le refus d'utilisation allégué au §57 que l'affirmation voulant que lui seul puisse bénéficier du service lorsqu'il avait les enfants.
> 8. En l'absence d'une couverture de remplacement effectivement assumée par l'autre parent, le demandeur ne disposait pas non plus d'un pouvoir discrétionnaire lui permettant de laisser les enfants sans assurance médicaments.

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

### 118. `legal/ponts_requete_2015_consolides.md` ligne ~1651 → `pq-100`

- **rang** 4.0 = score 9.5 × couverture 42%
- **termes partagés** : `remboursements`, `participant`, `lorsqu'il`, `dépôt`
- **source de la citation** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 1. Les enfants étaient bénéficiaires du régime d'assurance collective auquel adhérait le demandeur.
> 2. Le demandeur ne conteste pas cette couverture.
> 3. Les relevés documentent treize transactions où l'assureur a payé la portion couverte au fournisseur et trois dépenses de 110 $ déboursées intégralement, suivies d'un remboursement de 88 $ au compte du participant.
> 4. Aucune de ces seize transactions n'a eu lieu un dimanche, alors que la Requête situe les accès du demandeur le dimanche de 16 h à 20 h ; selon le propre récit de la Requête, il n'était donc l'accompagnateur ou l'auteur matériel d'aucune d'elles.
> 5. Le demandeur ne pouvait par ailleurs autoriser ou refuser les réclamations individuelles : elles étaient traitées selon l'admissibilité de l'enfant, la dépense et les conditions du régime, sans distinction fondée sur l'identité de l'accompagnateur.
> 6. Les transactions avaient ainsi lieu hors de sa présence sans dépendre de sa permission.
> 7. Cette combinaison réfute tant le refus d'utilisation allégué au §57 que l'affirmation voulant que lui seul puisse bénéficier du service lorsqu'il avait les enfants.
> 8. En l'absence d'une couverture de remplacement effectivement assumée par l'autre parent, le demandeur ne disposait pas non plus d'un pouvoir discrétionnaire lui permettant de laisser les enfants sans assurance médicaments.

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

### 119. `legal/piece_thread-6_reconstruction.md` ligne ~515 → `eq-176` — *citation encore inexploitée*

- **rang** 4.0 = score 9.4 × couverture 42%
- **termes partagés** : `meme`, `aller`, `suis`, `quand`
- **source de la citation** : email-367 — Re: Je t ai laissé un message tel. — trames —

**Idée non étayée :**

> le passé est fait et on ne se tue pas, je n'ai pas l'impression de te tué
> ou que toi tu me tue, mais non, ce que j'ai perdu ne se récupère pas, quand
> j'ai laisser aller les enfants, je l'ai fait sous certaines conditions,
> j'ai fait mon deuil, ce qui n'a pas été facile, mais maintenant mon
> attachement n'est plus le meme. J'ai accepter, je me suis adapté à la
> situation actuelle et je ne retournerai pas en arriere.

**Citation disponible :**

```text
nous nous sonmmes bien rendu, la maison etait propre, je suis quand meme aller souper a la maison avec Imad.
```

### 120. `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/02_securite_fondement_objectif.md` ligne ~11 → `pq-34`

- **rang** 3.9 = score 10.1 × couverture 39%
- **termes partagés** : `intervenant`, `dpj`, `sécurité`, `conjugale`, `violence`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 48

**Idée non étayée :**

> L'analyse distingue le fondement allégué de l'intervention - l'affirmation
> qu'Alexia vit dans la violence conjugale et la prédiction qu'un intervenant de
> la DPJ pourrait conclure à une compromission - des résultats opérationnels du
> plan. Elle soutient que la sécurité justifie l'urgence sans constituer un
> objectif documenté et structurant.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Tu dois le faire sortir de la maison [...]
```

### 121. `legal/procedure_introductive_instance_brouillon_workflow.md` ligne ~178 → `pq-65`

- **rang** 3.9 = score 10.8 × couverture 36%
- **termes partagés** : `disposé`, `progression`, `droits`, `auprès`, `établir`, `d'accès`
- **source de la citation** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames 56

**Idée non étayée :**

> 71. Le 2 septembre 2015, le demandeur a répondu qu'il était disposé à établir une progression dans les droits d'accès auprès des enfants.

**Citation disponible :**

```text
En ce qui a trait aux droits d'accès proposés au paragraphe 7 de votre projet d'entente, notre client est tout à fait disposé à établir une progression dans les droits d'accès auprès des enfants.
```

### 122. `legal/piece_thread-6_reconstruction.md` ligne ~172 → `eq-103`

- **rang** 3.8 = score 11.2 × couverture 34%
- **termes partagés** : `stp`, `vraiment`, `fais`
- **source de la citation** : email-287 — Re: Visite — trames 55

**Idée non étayée :**

> Louis Philippe pourquoi tu m'accuses tout le temps de vouloir te nuire? Je
> te dis que tu as raison de le faire et tu me réponds des insultes? Pourquoi
> tu ne vois pas que je ne veux pas me chicaner et t'accuser de rien??? Au
> contraire! Ma mère EST MORTE! Je ne sais pas si tu es capable de comprendre
> ça mais je ne VEUX PAS de chicane, je veux au contraire lui faire honneur
> en faisant le meilleur pour les enfants, je te dis que tu as eu raison de
> lui dire tu me reviens en t'obstinant sur un mot...Câline tu fais vraiment
> exprès pour que cela ne s'améliore pas.  Ça ne me dérange pas pour Noël si

**Citation disponible :**

```text
LP stp penses à eux je ne peux pas croire que tu décides délibérément de leur faire aussi mal....tu leur fais vraiment mal.
```

### 123. `legal/compilation_griefs.md` ligne ~1259 → `pq-100`

- **rang** 3.8 = score 9.3 × couverture 41%
- **termes partagés** : `remboursements`, `participant`, `direct`, `dépôt`
- **source de la citation** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 9. Durant l'été 2015, trois remboursements par dépôt direct ont été versés au compte du défendeur **en tant que participant au régime** (le remboursement va au preneur, quel que soit l'auteur de la dépense) pour des soins aux enfants : 9 juillet (Alexia, 88 $), 24 juillet (Nicolas, 88 $), 30 juillet (Alexia, 88 $).

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

### 124. `legal/piece_thread-91_emails-369-370.md` ligne ~29 → `eq-64`

- **rang** 3.8 = score 12.0 × couverture 31%
- **termes partagés** : `passerai`, `porter`, `chercher`, `aller`, `matin`
- **source de la citation** : email-370 — Re: Éléments à imprimer — trames 4

**Idée non étayée :**

> - Dans « Je passerai **les** chercher », le pronom « les » désigne les **éléments à imprimer**, non les enfants.
> - L'heure `05:02 UTC` de la base correspond à **00 h 02 HNE** dans l'en-tête original. Le message ne prouve pas que LP était levé à 5 h du matin.
> - Le courriel dit « aller porter Alexia », sans nommer la destination. L'attribution à la garderie ou au milieu préscolaire est une inférence contextuelle à authentifier par LP et par les autres pièces.
> - La pièce établit directement une prise en charge de transport annoncée; elle ne prouve pas, seule, chaque dépôt de la semaine.

**Citation disponible :**

```text
Salut peux tu m inprimer ca on a plus d encre a la maison. Je passerai les chercher demain matin apres etre aller porter Alexia.
```

### 125. `legal/axe_agenda_danse_elise.md` ligne ~107 → `eq-41`

- **rang** 3.8 = score 12.0 × couverture 31%
- **termes partagés** : `serviette`, `apporter`, `bain`
- **source de la citation** : email-66 — ce soir — trames 5, 31, 64

**Idée non étayée :**

> 14. Le 15 mars 2011, Johanne Bazinet a écrit au demandeur qu'elle souhaitait être appelée au moment du bain d'Alexia pour lui apporter une serviette (P-X, Email 66).

**Citation disponible :**

```text
Appelle moi quand tu entres la petite dans le bain - j'ai une serviette pour elle et j'aimerais lui apporter juste comme elle sort du bain
```

### 126. `legal/these_test_sincerite_2013.md` ligne ~208 → `pq-34`

- **rang** 3.7 = score 9.9 × couverture 38%
- **termes partagés** : `intervenant`, `arriver`, `dpj`, `pourra`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 48

**Idée non étayée :**

> Or **la DPJ n'a jamais été saisie** - par la partie même qui invoquait son critère, et qui ne l'a mobilisée que comme **pronostic** de ce qu'un intervenant « pourra arriver à la conclusion » d'établir (premier étage, *infra* ; §IV.1). **La seule voie capable de combler l'écart était disponible, et elle a été écartée.**

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Tu dois le faire sortir de la maison [...]
```

### 127. `legal/these_test_sincerite_2013.md` ligne ~239 → `pq-34`

- **rang** 3.7 = score 9.9 × couverture 38%
- **termes partagés** : `intervenant`, `arriver`, `dpj`, `pourra`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 48

**Idée non étayée :**

> Le tell est net : **la DPJ n'est jamais saisie.** Elle n'est invoquée que comme *pronostic* de ce qu'un intervenant « pourra arriver à la conclusion » d'établir. On emprunte l'**autorité** du critère sans en accepter le **mécanisme**.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Tu dois le faire sortir de la maison [...]
```

### 128. `legal/faits_chronologiques_2010-11-20_2012-02-06.md` ligne ~86 → `eq-154`

- **rang** 3.6 = score 9.5 × couverture 38%
- **termes partagés** : `passant`, `voiture`, `devant`
- **source de la citation** : email-67 — message — trames 5

**Idée non étayée :**

> **39.** Le 7 mars 2011, la grand-mère paternelle écrit au Demandeur avoir aperçu la voiture d'Élise en passant devant la résidence familiale en revenant de Montréal. `[Email id=67 | Johanne Bazinet → LP | Sujet : message]`

**Citation disponible :**

```text
en passant devant
chez toi la voiture d'Élise était là donc j'ai pensé que je ne devais pas
arrêter.
```

### 129. `legal/axe_absences_travail_enfants_malades.md` ligne ~61 → `eq-196`

- **rang** 3.6 = score 13.6 × couverture 26%
- **termes partagés** : `cmoc`, `dîner`, `d'équipe`
- **source de la citation** : email-28 — (sans objet) — trames 67

**Idée non étayée :**

> Email id=58 : la supérieure de LP reporte une réunion PnL (*"Je reporterai la rencontre PnL"*) pour accommoder son absence. Email id=28 : LP annonce qu'il manquera un *CMOC* et un dîner d'équipe. Ces conséquences corroborent que certaines adaptations ont effectivement affecté l'organisation professionnelle.

**Citation disponible :**

```text
Salut voici le papier du medicine, je vais manquer le CMOC et le dîner d'équipe, mais je suis malade et en plus je dois m occuper de mon gars
```

### 130. `legal/piece_document-1.md` ligne ~87 → `pq-95`

- **rang** 3.6 = score 13.9 × couverture 26%
- **termes partagés** : `l'égard`, `mineurs`, `conjointement`, `d'exercer`, `l'autorité`, `concernant`
- **source de la citation** : pdf-5 p.2 — 20150813 MJ projet consentement — trames 50

**Idée non étayée :**

> **§30** `[CONTESTÉ] [FALSIFIABLE]` - De plus, le défendeur refuse d'exercer conjointement l'autorité parentale à l'égard de leurs enfants mineurs préférant que toutes les décisions les concernant reposent sur la demanderesse.

**Citation disponible :**

```text
Les parties continueront d'exercer conjointement l'autorité parentale à l'égard des enfants mineurs et, sans limiter la généralité de ce qui précède, ils se consulteront sur toutes les questions d'importance concernant l'éducation, la santé, les soins médicaux, le bien-être des enfants, le choix des écoles, et ce dans le meilleur intérêt des enfants;
```

### 131. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~640 → `pq-95`

- **rang** 3.6 = score 13.9 × couverture 26%
- **termes partagés** : `l'égard`, `mineurs`, `conjointement`, `d'exercer`, `l'autorité`, `concernant`
- **source de la citation** : pdf-5 p.2 — 20150813 MJ projet consentement — trames 50

**Idée non étayée :**

> « 30. De plus, le défendeur refuse d'exercer conjointement l'autorité parentale à l'égard de leurs enfants mineurs préférant que toutes les décisions les concernant reposent sur la demanderesse.

**Citation disponible :**

```text
Les parties continueront d'exercer conjointement l'autorité parentale à l'égard des enfants mineurs et, sans limiter la généralité de ce qui précède, ils se consulteront sur toutes les questions d'importance concernant l'éducation, la santé, les soins médicaux, le bien-être des enfants, le choix des écoles, et ce dans le meilleur intérêt des enfants;
```

### 132. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~640 → `pq-95`

- **rang** 3.6 = score 13.9 × couverture 26%
- **termes partagés** : `l'égard`, `mineurs`, `conjointement`, `d'exercer`, `l'autorité`, `concernant`
- **source de la citation** : pdf-5 p.2 — 20150813 MJ projet consentement — trames 50

**Idée non étayée :**

> « 30. De plus, le défendeur refuse d'exercer conjointement l'autorité parentale à l'égard de leurs enfants mineurs préférant que toutes les décisions les concernant reposent sur la demanderesse.

**Citation disponible :**

```text
Les parties continueront d'exercer conjointement l'autorité parentale à l'égard des enfants mineurs et, sans limiter la généralité de ce qui précède, ils se consulteront sur toutes les questions d'importance concernant l'éducation, la santé, les soins médicaux, le bien-être des enfants, le choix des écoles, et ce dans le meilleur intérêt des enfants;
```

### 133. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~640 → `pq-95`

- **rang** 3.6 = score 13.9 × couverture 26%
- **termes partagés** : `l'égard`, `mineurs`, `conjointement`, `d'exercer`, `l'autorité`, `concernant`
- **source de la citation** : pdf-5 p.2 — 20150813 MJ projet consentement — trames 50

**Idée non étayée :**

> « 30. De plus, le défendeur refuse d'exercer conjointement l'autorité parentale à l'égard de leurs enfants mineurs préférant que toutes les décisions les concernant reposent sur la demanderesse.

**Citation disponible :**

```text
Les parties continueront d'exercer conjointement l'autorité parentale à l'égard des enfants mineurs et, sans limiter la généralité de ce qui précède, ils se consulteront sur toutes les questions d'importance concernant l'éducation, la santé, les soins médicaux, le bien-être des enfants, le choix des écoles, et ce dans le meilleur intérêt des enfants;
```

### 134. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~640 → `pq-95`

- **rang** 3.6 = score 13.9 × couverture 26%
- **termes partagés** : `l'égard`, `mineurs`, `conjointement`, `d'exercer`, `l'autorité`, `concernant`
- **source de la citation** : pdf-5 p.2 — 20150813 MJ projet consentement — trames 50

**Idée non étayée :**

> « 30. De plus, le défendeur refuse d'exercer conjointement l'autorité parentale à l'égard de leurs enfants mineurs préférant que toutes les décisions les concernant reposent sur la demanderesse.

**Citation disponible :**

```text
Les parties continueront d'exercer conjointement l'autorité parentale à l'égard des enfants mineurs et, sans limiter la généralité de ce qui précède, ils se consulteront sur toutes les questions d'importance concernant l'éducation, la santé, les soins médicaux, le bien-être des enfants, le choix des écoles, et ce dans le meilleur intérêt des enfants;
```

### 135. `legal/requete_secton_faits_lp.md` ligne ~735 → `pq-95`

- **rang** 3.6 = score 13.9 × couverture 26%
- **termes partagés** : `l'égard`, `mineurs`, `conjointement`, `d'exercer`, `l'autorité`, `concernant`
- **source de la citation** : pdf-5 p.2 — 20150813 MJ projet consentement — trames 50

**Idée non étayée :**

> « 30. De plus, le défendeur refuse d'exercer conjointement l'autorité parentale à l'égard de leurs enfants mineurs préférant que toutes les décisions les concernant reposent sur la demanderesse.

**Citation disponible :**

```text
Les parties continueront d'exercer conjointement l'autorité parentale à l'égard des enfants mineurs et, sans limiter la généralité de ce qui précède, ils se consulteront sur toutes les questions d'importance concernant l'éducation, la santé, les soins médicaux, le bien-être des enfants, le choix des écoles, et ce dans le meilleur intérêt des enfants;
```

### 136. `legal/analyse/Responsabilité Déonthologique/2013 juin.md` ligne ~566 → `pq-73`

- **rang** 3.6 = score 9.7 × couverture 37%
- **termes partagés** : `barreau`, `jeunesse`, `droit`, `québec`
- **source de la citation** : pdf-9 p.2 — Projet de loi no 15 — Loi modifiant la Loi sur la protection — trames 48, 55, 62

**Idée non étayée :**

> Me Ayoub est avocate spécialisée en droit de la jeunesse et membre du Comité consultatif en droit de la jeunesse du Barreau du Québec. Les effets documentés d'une rupture brutale de la relation père-enfant sur le développement affectif de l'enfant sont connus et enseignés tant en droit qu'en sciences du développement de l'enfant.

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de ses Groupes d’experts en droit de la jeunesse et du droit en regard des peuples autochtones : Me Marie-Josée Ayoub
```

### 137. `legal/analyse/Responsabilité Déonthologique/2013 juin.md` ligne ~620 → `pq-73`

- **rang** 3.6 = score 9.7 × couverture 37%
- **termes partagés** : `barreau`, `jeunesse`, `droit`, `québec`
- **source de la citation** : pdf-9 p.2 — Projet de loi no 15 — Loi modifiant la Loi sur la protection — trames 48, 55, 62

**Idée non étayée :**

> Un document du ministère de la Justice du Canada destiné aux praticiens du droit de la famille (*Types of Intimate Partner Violence*, HELP Toolkit - DOC-MJ) identifie explicitement parmi les expressions documentées de violence coercitive contrôlante post-séparation : le dépôt de faux signalements auprès d'une agence de protection de la jeunesse et l'utilisation de tactiques abusives en relation avec le processus judiciaire. Ce document est destiné précisément aux avocats de droit de la famille pour leur permettre d'identifier ces dynamiques dans leur pratique. Me Ayoub, à titre de spécialiste en droit de la jeunesse et membre du Comité consultatif en droit de la jeunesse du Barreau du Québec, connaît ou devrait connaître cette littérature professionnelle.

**Citation disponible :**

```text
Le Barreau du Québec remercie les membres de ses Groupes d’experts en droit de la jeunesse et du droit en regard des peuples autochtones : Me Marie-Josée Ayoub
```

### 138. `legal/analyse/Responsabilité Déonthologique/2019-09-27.md` ligne ~208 → `pq-80`

- **rang** 3.6 = score 8.5 × couverture 42%
- **termes partagés** : `prestations`, `d'assurance`, `emploi`, `revenu`
- **source de la citation** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> Deuxièmement - elle masque un événement documentairement établi. Les 12 034,00$ de prestations d'assurance-emploi signalent une interruption d'emploi en 2018 - information déterminante pour modéliser la capacité de payer future du père, notamment dans le contexte de sa situation d'emploi documentée en 2019. En agrégeant ces prestations avec le revenu d'emploi à la ligne 200, Me Ayoub a privé le tribunal de la granularité nécessaire à cette appréciation.

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

### 139. `legal/pont/pont_par14-15_2019.md` ligne ~92 → `pq-80`

- **rang** 3.6 = score 8.5 × couverture 42%
- **termes partagés** : `prestations`, `d'assurance`, `emploi`, `revenu`
- **source de la citation** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> 1. Les §14-15 soutiennent l'imputation au défendeur d'une capacité de gain d'environ 64-65 k.
> 2. Son revenu 2019 réel est de 46 744 $, avec un revenu d'emploi de 0 $ ; le chiffre de 64 028 $ est un composite 2018.
> 3. Ce composite additionne un salaire d'un poste où l'employeur atteste que le défendeur ne répondait pas aux attentes et des prestations d'assurance-emploi non récurrentes.
> 4. Le §15 présente en outre comme « expérience » deux emplois occupés durant les études du défendeur, élargissant artificiellement son employabilité.
> 5. Les offres déposées à l'appui du §14 valent environ 30 k une fois déflatées, sous le revenu réel 2019 ; elles ont été déposées par surprise à l'audience, le défendeur non représenté, et leurs salaires n'ont pas été retenus par le tribunal.

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

### 140. `legal/ponts_requete_2019_consolides.md` ligne ~978 → `pq-80`

- **rang** 3.6 = score 8.5 × couverture 42%
- **termes partagés** : `prestations`, `d'assurance`, `emploi`, `revenu`
- **source de la citation** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> 1. Les §14-15 soutiennent l'imputation au défendeur d'une capacité de gain d'environ 64-65 k.
> 2. Son revenu 2019 réel est de 46 744 $, avec un revenu d'emploi de 0 $ ; le chiffre de 64 028 $ est un composite 2018.
> 3. Ce composite additionne un salaire d'un poste où l'employeur atteste que le défendeur ne répondait pas aux attentes et des prestations d'assurance-emploi non récurrentes.
> 4. Le §15 présente en outre comme « expérience » deux emplois occupés durant les études du défendeur, élargissant artificiellement son employabilité.
> 5. Les offres déposées à l'appui du §14 valent environ 30 k une fois déflatées, sous le revenu réel 2019 ; elles ont été déposées par surprise à l'audience, le défendeur non représenté, et leurs salaires n'ont pas été retenus par le tribunal.

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

### 141. `legal/pont/pont_par56-57_2015.md` ligne ~41 → `pq-101`

- **rang** 3.5 = score 9.4 × couverture 38%
- **termes partagés** : `fournisseur`, `transactions`, `type`, `dimanche`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 1. Les enfants étaient bénéficiaires du régime d'assurance collective auquel adhérait le défendeur.
> 2. Une réclamation par paiement direct était soumise au fournisseur ou à l'assureur à partir des renseignements du régime, puis traitée selon l'admissibilité du bénéficiaire, la dépense et les conditions de la couverture.
> 3. Le participant n'avait pas à autoriser chaque réclamation présentée au bénéfice des enfants.
> 4. Entre le 25 février 2015 et le 16 mai 2016, treize transactions de type P ont été portées au nom des enfants ; l'assureur a versé la portion couverte au fournisseur.
> 5. Durant l'été 2015, trois transactions de type N ont été portées au nom des enfants : 110 $ ont été soumis pour chacune, puis 88 $ ont été versés au compte du participant, laissant 22 $ non remboursés.
> 6. Aucune de ces seize transactions n'a eu lieu un dimanche.
> 7. Le 17 octobre 2015, une transaction a été portée au nom de Nicolas, soit la dernière transaction documentée avant la Requête.
> 8. Le 19 novembre 2015, la Requête a allégué que le défendeur refusait l'utilisation des assurances et que lui seul pouvait en bénéficier lorsqu'il avait les enfants.

**Citation disponible :**

```text
Transactions 2016 — Paiements directs au fournisseur (type P) : 11 jan (Nicolas/Santé), 10 fév (Nicolas/Santé), 27 fév (Nicolas/Santé), 4 mai (Nicolas/Santé), 16 mai (Alexia/Santé). Toutes hors dimanche.
```

### 142. `legal/ponts_requete_2015_consolides.md` ligne ~1593 → `pq-101`

- **rang** 3.5 = score 9.4 × couverture 38%
- **termes partagés** : `fournisseur`, `transactions`, `type`, `dimanche`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 1. Les enfants étaient bénéficiaires du régime d'assurance collective auquel adhérait le défendeur.
> 2. Une réclamation par paiement direct était soumise au fournisseur ou à l'assureur à partir des renseignements du régime, puis traitée selon l'admissibilité du bénéficiaire, la dépense et les conditions de la couverture.
> 3. Le participant n'avait pas à autoriser chaque réclamation présentée au bénéfice des enfants.
> 4. Entre le 25 février 2015 et le 16 mai 2016, treize transactions de type P ont été portées au nom des enfants ; l'assureur a versé la portion couverte au fournisseur.
> 5. Durant l'été 2015, trois transactions de type N ont été portées au nom des enfants : 110 $ ont été soumis pour chacune, puis 88 $ ont été versés au compte du participant, laissant 22 $ non remboursés.
> 6. Aucune de ces seize transactions n'a eu lieu un dimanche.
> 7. Le 17 octobre 2015, une transaction a été portée au nom de Nicolas, soit la dernière transaction documentée avant la Requête.
> 8. Le 19 novembre 2015, la Requête a allégué que le défendeur refusait l'utilisation des assurances et que lui seul pouvait en bénéficier lorsqu'il avait les enfants.

**Citation disponible :**

```text
Transactions 2016 — Paiements directs au fournisseur (type P) : 11 jan (Nicolas/Santé), 10 fév (Nicolas/Santé), 27 fév (Nicolas/Santé), 4 mai (Nicolas/Santé), 16 mai (Alexia/Santé). Toutes hors dimanche.
```

### 143. `legal/analyse/Responsabilité civile/courriel 11 juin 2013 - responsabilite de Me Ayoub.md` ligne ~205 → `pq-55`

- **rang** 3.5 = score 11.4 × couverture 31%
- **termes partagés** : `n'entend`, `témoin`, `exclusif`, `juge`, `procédure`
- **source de la citation** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 55

**Idée non étayée :**

> **Axe 1 - la connaissance de l'*exigence probante* (tirée de la profession, confirmée par le document).**
> On n'évalue pas abstraitement toutes les formes possibles d'une procédure ; on évalue ce que **la proposition opérationnelle de Me Ayoub impliquait nécessairement** au moment où elle l'a formulée. En sa qualité d'avocate, elle savait ou devait savoir que :
> - une **plaidoirie** d'avocat **ne constitue pas une preuve** ;
> - l'éviction du père, l'usage exclusif de la résidence et la restriction des accès **exigeaient une base factuelle admissible** ;
> - des faits **contestés** relevant de la **connaissance personnelle d'Élise** devaient être introduits par un **mode de preuve reconnu** ;
> - l'**absence de témoignages oraux** (« le juge n'entend pas de témoin ») **ne supprimait pas** cette exigence probatoire ;
> - la procédure projetée devait donc comprendre une preuve **écrite, documentaire, testimoniale assermentée ou déjà admise**.

**Citation disponible :**

```text
[...] Si j'étais ton avocate le plan serait le suivant: faire une requête pour garde exclusive d'urgence, et usage exclusif de la résidence familiale. En urgence on appelle cela une ordonnance de sauvegarde. Lors de cette procédure d'urgence le juge en question n'entend pas de témoin
```

### 144. `legal/journal_fevrier2011_fevrier2012.md` ligne ~57 → `eq-88`

- **rang** 3.5 = score 8.4 × couverture 41%
- **termes partagés** : `pâques`, `lundi`, `souper`
- **source de la citation** : email-396 — Pâques — trames 31

**Idée non étayée :**

> **2011-04-12** - Emails M396 / M397 / M398 : Johanne organise le souper de Pâques en fonction des disponibilités d'Alexia et d'Annie-Claude. LP confirme sa disponibilité - Alexia disponible le samedi ou le lundi. Johanne confirme le lundi, avec souper tôt pour permettre à Alexia d'être présente.

**Citation disponible :**

```text
Nous ferons un souper de Pâques dimanche ou lundi dépendamment de l'horaire d'Alexia et de AC.
```

### 145. `legal/faits_chronologiques_2010-11-20_2012-02-06.md` ligne ~26 → `eq-39`

- **rang** 3.4 = score 13.5 × couverture 26%
- **termes partagés** : `oublie`, `vite`, `âge`, `danse`, `cet`
- **source de la citation** : email-81 — Alexia — trames 5, 64

**Idée non étayée :**

> **9.** Le 7 décembre 2010, la grand-mère paternelle écrit au Demandeur pour demander à voir Alexia lors des cours de danse d'Élise : « on oublie vite à cet âge. » `[Email id=81 | Johanne Bazinet → LP | Sujet : Alexia]`

**Citation disponible :**

```text
J'aimerais aller voir Alexia lorsque Élise sera à la danse.  Tu sais on oublie vite à cet âge et comme j'ai une bonne relation avec elle, je ne voudrais pas la perdre alors si Élise n'est pas là demain soir, j'aimerais passer.  Fais moi signe.  Merci
```

### 146. `legal/piece_thread-6_reconstruction.md` ligne ~669 → `eq-119` — *citation encore inexploitée*

- **rang** 3.4 = score 9.0 × couverture 37%
- **termes partagés** : `gens`, `capable`, `moins`
- **source de la citation** : email-295 — Re: Visite — trames —

**Idée non étayée :**

> Et si je suis capable ou non, on le saura jamais, mais y à des gens
> beaucoup moins fonctionels que moi qui le font... Tu penses que de
> s'occuper d'enfants c'est une tache tellement compliqué que peut de monde
> arrivent le faire ou peut etre penses tu que je suis si incompétant que moi
> personelement je n'y arriverait pas?

**Citation disponible :**

```text
On ne se comprend pas, on a toujours eu de la difficulté, les gens en garde partagée sont au moins capable de se comprendre, de se parler et de se respecter. Nous non...
```

### 147. `legal/faits/faits_par56-57_2015.md` ligne ~51 → `pq-102`

- **rang** 3.4 = score 11.2 × couverture 30%
- **termes partagés** : `fournisseur`, `réclamation`, `transaction`, `laquelle`
- **source de la citation** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> - **§56 est concédé.** La couverture des enfants est établie.
> - **L'identité de l'accompagnateur est sans pertinence pour l'admissibilité.** Elle ne modifie ni le statut de bénéficiaire de l'enfant ni les critères contractuels de traitement de la réclamation.
> - **La combinaison réfute le refus d'utilisation.** Les jours de garde excluent le défendeur comme accompagnateur ou auteur matériel ; l'absence de veto démontre que les transactions effectuées hors de sa présence ne dépendaient pas de sa permission. L'identité de l'autre accompagnateur est sans conséquence.
> - **La combinaison réfute également le monopole allégué.** Les prestations étaient accordées aux enfants alors que, selon la Requête, ils n'étaient pas avec le défendeur.
> - **Deux modes doivent être distingués.** Pour les treize transactions P, l'assureur paie la portion couverte au fournisseur. Pour les trois transactions N, 110 $ sont avancés intégralement, puis 88 $ sont remboursés au participant et 22 $ demeurent non couverts.
> - **Le seul résidu possible est monétaire.** Les remboursements de 88 $ pourraient devoir être remis à la personne qui avait avancé les 110 $, mais les relevés n'identifient pas cette personne et aucune demande de remise n'est produite.
> - **Une somme à remettre n'est pas un refus.** Même en supposant que la demanderesse ait avancé les 110 $, le dépôt des 88 $ au compte du participant peut créer une question comptable, mais aucun refus n'existe sans une demande communiquée au défendeur et rejetée par lui.
> - **« Refuse de payer la différence » est inopérant sans demande - non « insuffisamment prouvé ».** Un refus suppose une demande à laquelle on oppose un non. Absente une demande documentée, l'énoncé n'est pas seulement *non prouvé* : il n'énonce **aucune proposition falsifiable**, n'entretient **aucun lien avec la réalité**, et ne convoie que la connotation de l'enchaînement des mots (registre de l'**insinuation** - pertinent à l'abus / la diffamation). Il ne devient **significatif et falsifiable que dans le cas** où une telle demande, refusée, est établie ; §57a n'en cite aucune. Le traiter comme **inopérant**, non comme faux.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

### 148. `legal/piece_pdf-30.md` ligne ~15 → `pq-80`

- **rang** 3.4 = score 8.2 × couverture 41%
- **termes partagés** : `reer`, `revenus`, `retrait`, `revenu`
- **source de la citation** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> *(La ligne 154 « autres revenus » - établie à 37 991,58 $ par Revenu Québec, contre 1 591 $ déclarés - inclut le **retrait de REER** du Demandeur ; voir C2 pour la déduction REER corrélative.)*

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

### 149. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 28 29.md` ligne ~11 → `eq-67`

- **rang** 3.4 = score 9.2 × couverture 37%
- **termes partagés** : `guider`, `répondre`, `questions`, `afin`
- **source de la citation** : email-174 — renocntre — trames 43, 69, 75

**Idée non étayée :**

> Le 16 septembre 2015, Écrement a écrit au demandeur après avoir rencontré Élise Ayoub seule. Elle lui a offert une rencontre individuelle afin de le guider et de répondre à ses questions concernant la garde. Elle a précisé :

**Citation disponible :**

```text
Je voulais vous offrir de me rencontrer afin de vous guider / répondre à vos questions quant à la garde des enfants
```

### 150. `legal/piece_thread-6_reconstruction.md` ligne ~11 → `eq-118`

- **rang** 3.3 = score 9.2 × couverture 36%
- **termes partagés** : `n'as`, `sais`, `chose`, `demandé`
- **source de la citation** : email-267 — Re: Visite — trames 9

**Idée non étayée :**

> Salut, je sais que tu étais dépassé par dimanche dernier, mais les enfants
> étaient fatigués, tu n'as pas eu un traitement différent de ce qu'ils sont
> habituellement. Ils étaient réellement fatigués et Alexia vit beaucoup
> d'émotions à l'école, elle est la seule de toutes ses amies à avoir été
> mise dans la classe de 1ere - 2e année, elle a recommencé ses activités et
> elle a des devoirs à presque tous les jours. Oui c'est plate que tu les
> voies juste 4 heures et que cela se passe dans le conflit, mais le dimanche
> soir en général ils sont épuisés. Voudrais tu les prendre le vendredi soir

**Citation disponible :**

```text
Je sais que c'est ce que tu m'as demandé et moi je t'ai demandé autre chose. Aujourd'hui tu n'as pas de garde partagée et je n'ai pas ce que je t'ai demandé non plus, une garde avec visites multiples par semaine.
```

---

## Appariement sémantique

Modèle `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` — 768 dimensions, multilingue. Les paragraphes longs sont découpés en fenêtres glissantes ; on retient la meilleure similarité obtenue. Le cosinus n'expose pas *pourquoi* deux textes se ressemblent : cette section demande donc plus de lecture que la précédente, mais elle attrape les idées formulées avec d'autres mots que leur citation d'appui.

- paires retenues (cosinus ≥ 0.55 **et** distinction z ≥ 4.0) : **194**

> Le seuil de cosinus seul ne suffit pas : le corpus ne traite que d'un dossier, tout y est proche de tout. À 0,55 sans autre critère, la moitié des paragraphes trouvait un « appui ». Le **z-score** rapporte la similarité d'une paire à la distribution propre du paragraphe face aux 312 citations : il ne retient que les rapprochements qui se détachent de ce fond topique.

- dont déjà trouvées par l'appariement lexical : 24 (**convergence des deux méthodes — les plus sûres**)
- dont **invisibles au lexical** : **170** — c'est l'apport propre de cette passe

### Convergence lexical + sémantique (24)

Les deux méthodes indépendantes désignent la même paire. Ce sont les candidats les plus solides du rapport.

#### 1. `legal/allegation_stmt66_residence_2014.md` ligne ~27 → `pq-15`

- **distinction z = 7.5** — cosinus 0.773  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : pdf-60 p.1 — Pluie diluvienne 2012 — trames 13

**Idée non étayée :**

> 2. Le 30 mai 2012, des pluies diluviennes causent des dommages importants dans la région de Montréal (PDFDocument id=60 - *Orages : une pluie de dégâts sur Montréal*, Daphné Cameron, La Presse). La résidence familiale est affectée : le sous-sol subit des dommages.

**Citation disponible :**

```text
Les violents orages qui sont passés au-dessus de Montréal ont laissé dans leur sillage une pluie de dégâts. En l'espace de 15 minutes, commerçants et citoyens de Montréal ont vu l'eau monter et les dommages s'accumuler.
```

#### 2. `legal/compilation_griefs.md` ligne ~1257 → `pq-102`

- **distinction z = 5.4** — cosinus 0.712
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 8. Le Paiement Direct (type P) implique la présentation de la carte / du numéro de police **au point de service**, au moment de la transaction, déclenchant le paiement immédiat par l'assureur (la date du service = la date de la réclamation ; aucun décalage possible).

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 3. `legal/compilation_griefs.md` ligne ~1259 → `pq-100`

- **distinction z = 5.1** — cosinus 0.847
- **source** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 9. Durant l'été 2015, trois remboursements par dépôt direct ont été versés au compte du défendeur **en tant que participant au régime** (le remboursement va au preneur, quel que soit l'auteur de la dépense) pour des soins aux enfants : 9 juillet (Alexia, 88 $), 24 juillet (Nicolas, 88 $), 30 juillet (Alexia, 88 $).

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

#### 4. `legal/faits/faits_par10_2015.md` ligne ~22 → `pq-23`

- **distinction z = 4.8** — cosinus 0.719  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> **66.4.** Le 27 juin 2013, l'évaluateur Louis-Philippe Robert reçoit le mandat d'évaluer la valeur marchande de la maison au 245 avenue Macaulay, Saint-Lambert, à des fins de partage (PDFDocument id=11).

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

#### 5. `legal/piece_pdf-63.md` ligne ~14 → `pq-102`

- **distinction z = 4.7** — cosinus 0.620
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> - **Type (P) = Paiement au fournisseur** : l'assureur verse directement au fournisseur la portion couverte ; la personne présente au point de service n'avance que le solde non couvert.
> - **Type (N) = Dépôt Direct au participant** : la dépense est d'abord déboursée intégralement hors du mécanisme de paiement direct, puis l'assureur verse la portion couverte au **compte du participant**. Le relevé n'identifie pas la personne qui a fait le débours initial.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 6. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 56 57.md` ligne ~49 → `pq-101`

- **distinction z = 4.6** — cosinus 0.680
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> Les relevés Industrielle Alliance documentent treize transactions de type P, pour lesquelles l'assureur a versé la portion couverte au fournisseur, entre le 25 février 2015 et le 16 mai 2016.

**Citation disponible :**

```text
Transactions 2016 — Paiements directs au fournisseur (type P) : 11 jan (Nicolas/Santé), 10 fév (Nicolas/Santé), 27 fév (Nicolas/Santé), 4 mai (Nicolas/Santé), 16 mai (Alexia/Santé). Toutes hors dimanche.
```

#### 7. `legal/requete_secton_faits_lp.md` ligne ~1161 → `pq-80`

- **distinction z = 4.5** — cosinus 0.720
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> 399-M. Les prestations d'assurance-emploi de 12 034,00 $ et les prestations d'un régime de retraite ou d'un REER de 4 089,60 $ du demandeur sont ainsi comprises dans la somme inscrite à la ligne « Salaire brut » plutôt qu'aux lignes qui leur sont propres.

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 8. `legal/allegation_stmt66_residence_2014.md` ligne ~41 → `pq-23`

- **distinction z = 4.5** — cosinus 0.579
- **source** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> 9. Le 11 juillet 2013, l'évaluateur Louis-Philippe Robert produit son rapport d'évaluation marchande. La propriété du 245 Macaulay est formellement évaluée à des fins de partage.

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

#### 9. `legal/expose/sections/01_par4-6_implication_parentale.md` ligne ~119 → `eq-98`

- **distinction z = 4.5** — cosinus 0.663
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> [XX]. Le 27 février 2015, la défenderesse a écrit au demandeur que les parties avaient été conjointes de fait jusqu'à la rupture de février 2015, qu'elles ne faisaient pas chambre à part et qu'elles avaient des activités communes, tel qu'il appert de la pièce P-[●].

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 10. `legal/allegation_stmt56_57_58_assurances.md` ligne ~39 → `pq-102`

- **distinction z = 4.4** — cosinus 0.635
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> - **Type P** : l'assureur verse la portion couverte au fournisseur ; la personne présente au point de service n'avance que le solde non couvert.
> - **Type N** : la dépense est déboursée intégralement hors du paiement direct, puis l'assureur verse la portion couverte au compte du participant. Le relevé n'identifie pas la personne qui a fait le débours initial.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 11. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~115 → `eq-98`

- **distinction z = 4.4** — cosinus 0.648
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> 47. Le 27 février 2015, la défenderesse a écrit au demandeur que les parties avaient été conjointes de fait jusqu'à la rupture de février 2015, qu'elles ne faisaient pas chambre à part et qu'elles avaient des activités communes, tel qu'il appert de la pièce P-[●].

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 12. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~115 → `eq-98`

- **distinction z = 4.4** — cosinus 0.648
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> 47. Le 27 février 2015, la défenderesse a écrit au demandeur que les parties avaient été conjointes de fait jusqu'à la rupture de février 2015, qu'elles ne faisaient pas chambre à part et qu'elles avaient des activités communes, tel qu'il appert de la pièce P-[●].

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 13. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~115 → `eq-98`

- **distinction z = 4.4** — cosinus 0.648
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> 47. Le 27 février 2015, la défenderesse a écrit au demandeur que les parties avaient été conjointes de fait jusqu'à la rupture de février 2015, qu'elles ne faisaient pas chambre à part et qu'elles avaient des activités communes, tel qu'il appert de la pièce P-[●].

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 14. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~115 → `eq-98`

- **distinction z = 4.4** — cosinus 0.648
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> 47. Le 27 février 2015, la défenderesse a écrit au demandeur que les parties avaient été conjointes de fait jusqu'à la rupture de février 2015, qu'elles ne faisaient pas chambre à part et qu'elles avaient des activités communes, tel qu'il appert de la pièce P-[●].

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 15. `legal/compilation_griefs.md` ligne ~1251 → `pq-99`

- **distinction z = 4.3** — cosinus 0.758
- **source** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 6. Les relevés d'assurance (Industrielle Alliance, 2015-2016) documentent **douze transactions par Paiement Direct au fournisseur (type P)** au nom des enfants, entre le 25 février 2015 et le 16 mai 2016, **toutes en dehors du dimanche** :
>    - **2015** : 25 fév. (mer., Nicolas), 16 avr. (jeu., Nicolas), 4 mai (lun., Nicolas), 7 juil. (mar., Alexia - dentaire), 17 sept. (jeu., Alexia), 1er oct. (jeu., Nicolas), 17 oct. (sam., Nicolas - fait 1).
>    - **2016** : 11 jan. (lun., Nicolas - fait 10), 10 fév. (mer., Nicolas), 27 fév. (sam., Nicolas), 4 mai (mer., Nicolas), 16 mai (lun., Alexia).

**Citation disponible :**

```text
Transactions 2015 — Paiements directs au fournisseur (type P) : 25 fév (Nicolas/Santé), 16 avr (Nicolas/Santé), 4 mai (Nicolas/Santé), 7 juil (Alexia/Dentaire), 17 sep (Alexia/Santé), 1 oct (Nicolas/Santé), 17 oct (Nicolas/Santé). Toutes hors dimanche.
```

#### 16. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 56 57.md` ligne ~33 → `pq-102`

- **distinction z = 4.3** — cosinus 0.647
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> Les relevés distinguent deux mécanismes. Pour une transaction de type **P**, l'assureur verse la portion couverte au fournisseur. Pour une transaction de type **N**, la dépense est déboursée intégralement hors du paiement direct, puis la portion couverte est remboursée au compte du participant. Industrielle Alliance décrit le premier mécanisme : le pharmacien soumet lui-même la réclamation après présentation de la carte d'assurance collective ([iA, réclamation de médicaments](https://ia.ca/faire-une-reclamation/collective/medicaments)).

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 17. `legal/requete_secton_faits_lp.md` ligne ~1161 → `pq-81`

- **distinction z = 4.2** — cosinus 0.672
- **source** : pdf-30 p.1 — Avis de cotisation 2019 — trames 62

**Idée non étayée :**

> 399-M. Les prestations d'assurance-emploi de 12 034,00 $ et les prestations d'un régime de retraite ou d'un REER de 4 089,60 $ du demandeur sont ainsi comprises dans la somme inscrite à la ligne « Salaire brut » plutôt qu'aux lignes qui leur sont propres.

**Citation disponible :**

```text
Revenus Net : 41788,58
Prestations d'assurance emploi : 8752.00
Retrait REER : 37991.58
```

#### 18. `legal/dossier_plaidoirie/05_argumentaire_violence_substitution_interets_execution_plan.md` ligne ~137 → `pq-58`

- **distinction z = 4.1** — cosinus 0.777
- **source** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 56, 62

**Idée non étayée :**

> Cette réserve était mal cadrée. La proposition à éprouver n'est pas une
> affirmation universelle visant tout événement concevable. Elle concerne le
> portrait précis formulé dans P‐2 : une violence conjugale vécue par Alexia
> « depuis sa naissance », susceptible de compromettre sa sécurité et son
> développement, et nécessitant la mesure urgente proposée.

**Citation disponible :**

```text
[...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
```

#### 19. `legal/procedure_introductive_instance_brouillon_workflow.md` ligne ~182 → `pq-14` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.780
- **source** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames —

**Idée non étayée :**

> 73. Le demandeur se disait également disposé à laisser la défenderesse choisir les jours de garde afin que l'horaire tienne compte de ses cours de danse.

**Citation disponible :**

```text
En ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse;
```

#### 20. `legal/procedure_introductive_instance_brouillon_workflow.md` ligne ~182 → `pq-67`

- **distinction z = 4.1** — cosinus 0.780
- **source** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames 56

**Idée non étayée :**

> 73. Le demandeur se disait également disposé à laisser la défenderesse choisir les jours de garde afin que l'horaire tienne compte de ses cours de danse.

**Citation disponible :**

```text
En ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse;
```

#### 21. `legal/expose_faits_volet_2015.md` ligne ~135 → `eq-150`

- **distinction z = 4.1** — cosinus 0.744  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-365 — Conseils — trames 72

**Idée non étayée :**

> 54. Le 26 juin 2013, le demandeur écrivait à Me Suzanne Pringle que la sœur avocate de sa conjointe la guidait « de façon à [le] piéger » et que la défenderesse lui écrivait qu'elle le trouvait agressif et avait peur de lui (pièce à coter : Email id=365 ; renonciation à délimiter).

**Citation disponible :**

```text
Je vous contacte parce que je suis incapable de gérer cette
situation seule et de manière appropriée, la sœur de ma conjointe est
avocate et la guide de façon à me piéger.
J’ai coupé toute communication avec ma conjointe ce matin du fait que sans
raison elle m’écrive qu’elle trouvait que j’étais agressif et qu’elle avait
peur de moi.
```

#### 22. `legal/journal_ete2013.md` ligne ~25 → `pq-23`

- **distinction z = 4.1** — cosinus 0.644
- **source** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> **2013-06-27** - PDFDocument PDF11 : LP reçoit l'étude de la valeur marchande de la résidence familiale (245 avenue Macaulay, Saint-Lambert) commandée aux fins de partage. LP est à Saint-Lambert et est activement impliqué dans le règlement des affaires familiales.

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

#### 23. `legal/compilation_griefs.md` ligne ~1241 → `pq-102`

- **distinction z = 4.1** — cosinus 0.735
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 1. Le **17 octobre 2015** (un **samedi**), une transaction de type P (Paiement Direct au fournisseur) a été effectuée au bénéfice de **Nicolas (santé)** - **hors** du seul créneau d'accès du défendeur (dimanche 16-20h ; voir fait 5). C'est la **dernière** transaction avant la rédaction de la Requête du 19 novembre 2015.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 24. `legal/allegation_stmt56_57_58_assurances.md` ligne ~29 → `pq-30`

- **distinction z = 4.1** — cosinus 0.715
- **source** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> - **2015.pdf** - Relevé Industrielle Alliance (Espace conseiller, Group Insurance), demandes de règlement 1 janv.-31 déc. 2015.
> - **2016.pdf** - Relevé Industrielle Alliance, demandes de règlement 1 janv.-31 déc. 2016.
> - **Jugement_1.pdf** - Procès-verbal d'audience, Hon. Sophie Picard j.c.s., district de Longueuil, dossier 505-04-024603-151, 14 janvier 2016 (jugement par défaut).

**Citation disponible :**

```text
Espace conseiller - Group Insurance - Participant Page 1 sur 2

## Critères de recherche

Du | Au | Statut
:---|:---|:---
1 janvier 2015 | 31 décembre 2015 | Payé

## Demandes de règlement

| Statut | Date d'effet du statut | Nom (Lien familial) | Type règlement | Période | Montant soumis | Montant Payé | Payé à | Numéro de chèque |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
```

### Apport propre du sémantique (170)

L'idée et la citation ne partagent pas de vocabulaire distinctif, mais se rejoignent sur le sens. À lire une par une : c'est ici que le bruit est le plus probable, et aussi les rapprochements que rien d'autre ne trouverait.

#### 1. `legal/expose_faits_volet_2015.md` ligne ~145 → `eq-62`

- **distinction z = 8.7** — cosinus 0.741
- **source** : email-137 — Re: Des nouvelles un peu sombres — trames 14

**Idée non étayée :**

> 58. Le sous-sol de la résidence avait été démoli en 2012 à la suite d'une inondation et n'avait pas été reconstruit (pièce à coter).

**Citation disponible :**

```text
Le sous sol on l'a démolie suite a une inondation l'année dernière et nous ne l'avons jamais terminé, préférant utiliser l'argent de l'assurance pour changer le système de chauffage.
```

#### 2. `legal/pont/pont_par9_2015.md` ligne ~249 → `eq-62`

- **distinction z = 8.0** — cosinus 0.703  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-137 — Re: Des nouvelles un peu sombres — trames 14

**Idée non étayée :**

> 15. Le sous-sol de la résidence avait été démoli en 2012 à la suite d'une inondation et n'avait pas été reconstruit (PDFDocument id=60 ; Email id=137).

**Citation disponible :**

```text
Le sous sol on l'a démolie suite a une inondation l'année dernière et nous ne l'avons jamais terminé, préférant utiliser l'argent de l'assurance pour changer le système de chauffage.
```

#### 3. `legal/ponts_requete_2015_consolides.md` ligne ~720 → `eq-62`

- **distinction z = 8.0** — cosinus 0.703  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-137 — Re: Des nouvelles un peu sombres — trames 14

**Idée non étayée :**

> 15. Le sous-sol de la résidence avait été démoli en 2012 à la suite d'une inondation et n'avait pas été reconstruit (PDFDocument id=60 ; Email id=137).

**Citation disponible :**

```text
Le sous sol on l'a démolie suite a une inondation l'année dernière et nous ne l'avons jamais terminé, préférant utiliser l'argent de l'assurance pour changer le système de chauffage.
```

#### 4. `legal/compilation_griefs.md` ligne ~432 → `eq-62`

- **distinction z = 7.9** — cosinus 0.698  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-137 — Re: Des nouvelles un peu sombres — trames 14

**Idée non étayée :**

> 13. Le sous-sol de la résidence avait été démoli en 2012 à la suite d'une inondation et n'avait pas été reconstruit (PDFDocument id=60 ; Email id=137).

**Citation disponible :**

```text
Le sous sol on l'a démolie suite a une inondation l'année dernière et nous ne l'avons jamais terminé, préférant utiliser l'argent de l'assurance pour changer le système de chauffage.
```

#### 5. `legal/faits/faits_par9_2015.md` ligne ~83 → `eq-62`

- **distinction z = 7.9** — cosinus 0.698  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-137 — Re: Des nouvelles un peu sombres — trames 14

**Idée non étayée :**

> 13. Le sous-sol de la résidence avait été démoli en 2012 à la suite d'une inondation et n'avait pas été reconstruit (PDFDocument id=60 ; Email id=137).

**Citation disponible :**

```text
Le sous sol on l'a démolie suite a une inondation l'année dernière et nous ne l'avons jamais terminé, préférant utiliser l'argent de l'assurance pour changer le système de chauffage.
```

#### 6. `legal/axe_agenda_danse_elise.md` ligne ~85 → `pq-12`

- **distinction z = 7.5** — cosinus 0.806  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : pdf-59 p.1 — Biographie d'Elise Ayoub publiée sur le site web du studio d — trames 12, 64

**Idée non étayée :**

> 3. La défenderesse a déclaré dans sa biographie auto-publiée avoir suivi des cours à Urban Element de 2005 à 2016, parallèlement à ses cours aux Ballets Modernes du Québec (P-X, PDFDocument 59).

**Citation disponible :**

```text
En 1999, fascinée par la danse, elle se joint à l’école de danse Les Ballets Modernes du Québec. En 2005, elle débute ses classes au Urban Element (maintenant le UEZ) , où elle y rencontre plusieurs pionniers de la danse urbaine. Elle continue toutefois ses cours chez Les Ballet Modernes du Québec où elle observe les talents de Direction d'Hugo Depot et Francine St-Yves, et ce jusqu'en 2016.
```

#### 7. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~646 → `eq-93`

- **distinction z = 6.6** — cosinus 0.687
- **source** : email-343 — Re: Baptême de Nicolas — trames 44

**Idée non étayée :**

> 250. Le 19 juillet 2015, Nicolas a été baptisé sans que le demandeur ait préalablement été informé de la tenue du baptême ni invité à y assister, tel qu'il appert du courriel contemporain produit comme pièce P-[●].

**Citation disponible :**

```text
Moi j y vais pas j ai pas ete invité et en fait je savais pas qu elle le
faisias baptiser.... Bonjour, demain le 19 juillet à 14:00 je ferais baptiser Nicolas a l'église st Thomas d'aquin. Si vous avez envie d'être présentes à la cérémonie vous êtes les bienvenus.
```

#### 8. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~646 → `eq-93`

- **distinction z = 6.6** — cosinus 0.687
- **source** : email-343 — Re: Baptême de Nicolas — trames 44

**Idée non étayée :**

> 250. Le 19 juillet 2015, Nicolas a été baptisé sans que le demandeur ait préalablement été informé de la tenue du baptême ni invité à y assister, tel qu'il appert du courriel contemporain produit comme pièce P-[●].

**Citation disponible :**

```text
Moi j y vais pas j ai pas ete invité et en fait je savais pas qu elle le
faisias baptiser.... Bonjour, demain le 19 juillet à 14:00 je ferais baptiser Nicolas a l'église st Thomas d'aquin. Si vous avez envie d'être présentes à la cérémonie vous êtes les bienvenus.
```

#### 9. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~646 → `eq-93`

- **distinction z = 6.6** — cosinus 0.687
- **source** : email-343 — Re: Baptême de Nicolas — trames 44

**Idée non étayée :**

> 250. Le 19 juillet 2015, Nicolas a été baptisé sans que le demandeur ait préalablement été informé de la tenue du baptême ni invité à y assister, tel qu'il appert du courriel contemporain produit comme pièce P-[●].

**Citation disponible :**

```text
Moi j y vais pas j ai pas ete invité et en fait je savais pas qu elle le
faisias baptiser.... Bonjour, demain le 19 juillet à 14:00 je ferais baptiser Nicolas a l'église st Thomas d'aquin. Si vous avez envie d'être présentes à la cérémonie vous êtes les bienvenus.
```

#### 10. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~646 → `eq-93`

- **distinction z = 6.6** — cosinus 0.687
- **source** : email-343 — Re: Baptême de Nicolas — trames 44

**Idée non étayée :**

> 250. Le 19 juillet 2015, Nicolas a été baptisé sans que le demandeur ait préalablement été informé de la tenue du baptême ni invité à y assister, tel qu'il appert du courriel contemporain produit comme pièce P-[●].

**Citation disponible :**

```text
Moi j y vais pas j ai pas ete invité et en fait je savais pas qu elle le
faisias baptiser.... Bonjour, demain le 19 juillet à 14:00 je ferais baptiser Nicolas a l'église st Thomas d'aquin. Si vous avez envie d'être présentes à la cérémonie vous êtes les bienvenus.
```

#### 11. `legal/axe_agenda_danse_elise.md` ligne ~87 → `pq-12`

- **distinction z = 5.9** — cosinus 0.595  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : pdf-59 p.1 — Biographie d'Elise Ayoub publiée sur le site web du studio d — trames 12, 64

**Idée non étayée :**

> 4. La défenderesse a déclaré dans cette même biographie que l'intérêt pour la danse orientale s'est manifesté en 2005, et que ses débuts dans l'enseignement de cette danse se sont concrétisés en 2010 (P-X, PDFDocument 59).

**Citation disponible :**

```text
En 1999, fascinée par la danse, elle se joint à l’école de danse Les Ballets Modernes du Québec. En 2005, elle débute ses classes au Urban Element (maintenant le UEZ) , où elle y rencontre plusieurs pionniers de la danse urbaine. Elle continue toutefois ses cours chez Les Ballet Modernes du Québec où elle observe les talents de Direction d'Hugo Depot et Francine St-Yves, et ce jusqu'en 2016.
```

#### 12. `legal/expose_faits_volet_2015.md` ligne ~65 → `pq-12`

- **distinction z = 5.8** — cosinus 0.625
- **source** : pdf-59 p.1 — Biographie d'Elise Ayoub publiée sur le site web du studio d — trames 12, 64

**Idée non étayée :**

> 24. Dans une biographie qu'elle a publiée, la défenderesse indique avoir suivi des cours de danse de 1999 à 2016, enseigné la danse dès 2010 et été gestionnaire d'événements de danse de 2013 à 2018 (pièce à coter : biographie publiée).

**Citation disponible :**

```text
En 1999, fascinée par la danse, elle se joint à l’école de danse Les Ballets Modernes du Québec. En 2005, elle débute ses classes au Urban Element (maintenant le UEZ) , où elle y rencontre plusieurs pionniers de la danse urbaine. Elle continue toutefois ses cours chez Les Ballet Modernes du Québec où elle observe les talents de Direction d'Hugo Depot et Francine St-Yves, et ce jusqu'en 2016.
```

#### 13. `legal/pont/pont_par4-5-6_2015.md` ligne ~101 → `pq-12`

- **distinction z = 5.5** — cosinus 0.634
- **source** : pdf-59 p.1 — Biographie d'Elise Ayoub publiée sur le site web du studio d — trames 12, 64

**Idée non étayée :**

> 20. Dans une biographie qu'elle a publiée, la demanderesse indique avoir suivi des cours de danse de 1999 à 2016, enseigné dès 2010 et été gestionnaire d'événements de danse de 2013 à 2018.

**Citation disponible :**

```text
En 1999, fascinée par la danse, elle se joint à l’école de danse Les Ballets Modernes du Québec. En 2005, elle débute ses classes au Urban Element (maintenant le UEZ) , où elle y rencontre plusieurs pionniers de la danse urbaine. Elle continue toutefois ses cours chez Les Ballet Modernes du Québec où elle observe les talents de Direction d'Hugo Depot et Francine St-Yves, et ce jusqu'en 2016.
```

#### 14. `legal/ponts_requete_2015_consolides.md` ligne ~113 → `pq-12`

- **distinction z = 5.5** — cosinus 0.634
- **source** : pdf-59 p.1 — Biographie d'Elise Ayoub publiée sur le site web du studio d — trames 12, 64

**Idée non étayée :**

> 20. Dans une biographie qu'elle a publiée, la demanderesse indique avoir suivi des cours de danse de 1999 à 2016, enseigné dès 2010 et été gestionnaire d'événements de danse de 2013 à 2018.

**Citation disponible :**

```text
En 1999, fascinée par la danse, elle se joint à l’école de danse Les Ballets Modernes du Québec. En 2005, elle débute ses classes au Urban Element (maintenant le UEZ) , où elle y rencontre plusieurs pionniers de la danse urbaine. Elle continue toutefois ses cours chez Les Ballet Modernes du Québec où elle observe les talents de Direction d'Hugo Depot et Francine St-Yves, et ce jusqu'en 2016.
```

#### 15. `legal/piece_document-1.md` ligne ~20 → `eq-98`

- **distinction z = 5.4** — cosinus 0.627
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> **§1** - Les parties se sont fréquentées et fait vie commune pendant pour une période d'environ onze (11) ans, soit du 31 décembre 2003 au 23 février 2015.

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 16. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 56 57.md` ligne ~84 → `pq-100`

- **distinction z = 5.4** — cosinus 0.791
- **source** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> Trois dépenses de 110 $ relatives à des soins aux enfants ont été traitées selon le mode N durant l'été 2015 : le 9 juillet pour Alexia, le 24 juillet pour Nicolas et le 30 juillet pour Alexia. Pour chacune, la dépense a été déboursée intégralement hors du paiement direct, puis 88 $ ont été versés au compte du défendeur comme participant, laissant 22 $ non remboursés.

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

#### 17. `legal/piece_vacances_2013_cape_cod_cuba_chalet.md` ligne ~98 → `eq-71`

- **distinction z = 5.3** — cosinus 0.739
- **source** : email-78 — (sans objet) — trames 44, 62

**Idée non étayée :**

> - **Asymétrie symétrique documentée :** Élise emmène Alexia à Cuba à 14 mois (déc. 2010) sans opposition de LP. En 2013, Élise oppose à LP que Cape Cod est impossible car Alexia est « trop jeune » - Alexia a alors 3 ans et 9 mois, soit plus de deux fois et demi l'âge qu'elle avait lors du voyage à Cuba initié par Élise. Le motif « trop jeune » est incompatible avec le précédent que la demanderesse a elle-même créé.

**Citation disponible :**

```text
Elise veut partir a Cuba au mois de fevrier avec la petite, peut elle faire
ca?
```

#### 18. `legal/axe_agenda_danse_elise.md` ligne ~160 → `pq-12`

- **distinction z = 5.2** — cosinus 0.697
- **source** : pdf-59 p.1 — Biographie d'Elise Ayoub publiée sur le site web du studio d — trames 12, 64

**Idée non étayée :**

> **Constat :** De **1999 à 2016** - soit bien avant la naissance d'Alexia et jusqu'après la séparation définitive - la Défenderesse fréquentait assidûment les Ballets Modernes du Québec (Hugo Depot / Danse HDP). Cette formation constituait un engagement hebdomadaire continu sur toute la période 2009-2015 visée par les allégations. En parallèle, à partir de 2010, elle enseignait la danse plusieurs soirs par semaine, participait à des spectacles professionnels, et à partir de 2013 gérait les événements d'une troupe internationale. Ces engagements s'ajoutent à - et ne remplacent pas - l'engagement HDP.

**Citation disponible :**

```text
En 1999, fascinée par la danse, elle se joint à l’école de danse Les Ballets Modernes du Québec. En 2005, elle débute ses classes au Urban Element (maintenant le UEZ) , où elle y rencontre plusieurs pionniers de la danse urbaine. Elle continue toutefois ses cours chez Les Ballet Modernes du Québec où elle observe les talents de Direction d'Hugo Depot et Francine St-Yves, et ce jusqu'en 2016.
```

#### 19. `legal/compilation_griefs.md` ligne ~169 → `pq-12`

- **distinction z = 5.2** — cosinus 0.568  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : pdf-59 p.1 — Biographie d'Elise Ayoub publiée sur le site web du studio d — trames 12, 64

**Idée non étayée :**

> 44. Dans une biographie qu'elle a publiée, la demanderesse déclare avoir suivi des cours de danse de 1999 à 2016, enseigné dès 2010, et été gestionnaire d'événements de la danseuse Aziza de 2013 à 2018 (PDFDocument id=59).

**Citation disponible :**

```text
En 1999, fascinée par la danse, elle se joint à l’école de danse Les Ballets Modernes du Québec. En 2005, elle débute ses classes au Urban Element (maintenant le UEZ) , où elle y rencontre plusieurs pionniers de la danse urbaine. Elle continue toutefois ses cours chez Les Ballet Modernes du Québec où elle observe les talents de Direction d'Hugo Depot et Francine St-Yves, et ce jusqu'en 2016.
```

#### 20. `legal/faits/faits_par4-5-6_2015.md` ligne ~157 → `pq-12`

- **distinction z = 5.2** — cosinus 0.568  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : pdf-59 p.1 — Biographie d'Elise Ayoub publiée sur le site web du studio d — trames 12, 64

**Idée non étayée :**

> 44. Dans une biographie qu'elle a publiée, la demanderesse déclare avoir suivi des cours de danse de 1999 à 2016, enseigné dès 2010, et été gestionnaire d'événements de la danseuse Aziza de 2013 à 2018 (PDFDocument id=59).

**Citation disponible :**

```text
En 1999, fascinée par la danse, elle se joint à l’école de danse Les Ballets Modernes du Québec. En 2005, elle débute ses classes au Urban Element (maintenant le UEZ) , où elle y rencontre plusieurs pionniers de la danse urbaine. Elle continue toutefois ses cours chez Les Ballet Modernes du Québec où elle observe les talents de Direction d'Hugo Depot et Francine St-Yves, et ce jusqu'en 2016.
```

#### 21. `legal/implication_parentale_recurrence/05_synthese_evenements_cycliques.md` ligne ~26 → `pq-12`

- **distinction z = 5.1** — cosinus 0.676
- **source** : pdf-59 p.1 — Biographie d'Elise Ayoub publiée sur le site web du studio d — trames 12, 64

**Idée non étayée :**

> La [biographie d'Élise](01_cours_danse_mere.md) décrit une pratique poursuivie aux Ballets Modernes du Québec de 1999 à 2016, sans pause documentée. La structure de l'école comporte deux sessions totalisant environ trente semaines de cours par année, selon un créneau hebdomadaire fixe.

**Citation disponible :**

```text
En 1999, fascinée par la danse, elle se joint à l’école de danse Les Ballets Modernes du Québec. En 2005, elle débute ses classes au Urban Element (maintenant le UEZ) , où elle y rencontre plusieurs pionniers de la danse urbaine. Elle continue toutefois ses cours chez Les Ballet Modernes du Québec où elle observe les talents de Direction d'Hugo Depot et Francine St-Yves, et ce jusqu'en 2016.
```

#### 22. `legal/analyse/Responsabilité civile/requete 21 juillet 2023/DMD2023 paragraphes7 8 responsabilite civile.md` ligne ~36 → `pq-80`

- **distinction z = 5.1** — cosinus 0.596
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> Ces niveaux de revenus sont inférieurs au revenu effectivement déclaré par le demandeur pour l'année 2019 - 46 743,58 $ - et inférieurs aux revenus d'emploi de 2018 - 47 520,51 $.

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 23. `legal/journal_ete2013.md` ligne ~87 → `eq-9`

- **distinction z = 5.0** — cosinus 0.728
- **source** : email-359 — Fwd: 22 Glenwood Ave. Cape Cod summer rental — trames 2

**Idée non étayée :**

> **2013-08-01** - Email M359 : Confirmation de l'enregistrement de la location de la maison familiale à Cape Cod (22 Glenwood Ave) pour le séjour d'août - transmise par Vincent Deschênes.

**Citation disponible :**

```text
Hi Doug, We are preparing for our vacation in Cape Cod from August 10-17 at the house on 22 Glenwood Drive West Yarmouth, properties no 320. I just wanted to double check everything is OK and the house will be ready for us on August 10. We were wondering why we can not find the house anymore on http://www.weneedavacation.com.
```

#### 24. `legal/piece_vacances_2013_cape_cod_cuba_chalet.md` ligne ~47 → `eq-71`

- **distinction z = 5.0** — cosinus 0.640
- **source** : email-78 — (sans objet) — trames 44, 62

**Idée non étayée :**

> 5. LP a finalement **capitulé et signé les papiers** de voyage. Élise est partie à Cuba avec les enfants. LP est allé à Cape Cod **sans Alexia** (comme en 2012).

**Citation disponible :**

```text
Elise veut partir a Cuba au mois de fevrier avec la petite, peut elle faire
ca?
```

#### 25. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~308 → `eq-62`

- **distinction z = 5.0** — cosinus 0.652
- **source** : email-137 — Re: Des nouvelles un peu sombres — trames 14

**Idée non étayée :**

> 125. Le demandeur expliquait également qu'il ne pouvait dormir dans le sous-sol de la résidence familiale puisque celui-ci avait été démoli à la suite d'une inondation survenue en 2012 et n'avait pas été reconstruit, tel qu'il appert des pièces P-[13] et P-[14].

**Citation disponible :**

```text
Le sous sol on l'a démolie suite a une inondation l'année dernière et nous ne l'avons jamais terminé, préférant utiliser l'argent de l'assurance pour changer le système de chauffage.
```

#### 26. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~308 → `eq-62`

- **distinction z = 5.0** — cosinus 0.652
- **source** : email-137 — Re: Des nouvelles un peu sombres — trames 14

**Idée non étayée :**

> 125. Le demandeur expliquait également qu'il ne pouvait dormir dans le sous-sol de la résidence familiale puisque celui-ci avait été démoli à la suite d'une inondation survenue en 2012 et n'avait pas été reconstruit, tel qu'il appert des pièces P-[13] et P-[14].

**Citation disponible :**

```text
Le sous sol on l'a démolie suite a une inondation l'année dernière et nous ne l'avons jamais terminé, préférant utiliser l'argent de l'assurance pour changer le système de chauffage.
```

#### 27. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~308 → `eq-62`

- **distinction z = 5.0** — cosinus 0.652
- **source** : email-137 — Re: Des nouvelles un peu sombres — trames 14

**Idée non étayée :**

> 125. Le demandeur expliquait également qu'il ne pouvait dormir dans le sous-sol de la résidence familiale puisque celui-ci avait été démoli à la suite d'une inondation survenue en 2012 et n'avait pas été reconstruit, tel qu'il appert des pièces P-[13] et P-[14].

**Citation disponible :**

```text
Le sous sol on l'a démolie suite a une inondation l'année dernière et nous ne l'avons jamais terminé, préférant utiliser l'argent de l'assurance pour changer le système de chauffage.
```

#### 28. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~308 → `eq-62`

- **distinction z = 5.0** — cosinus 0.652
- **source** : email-137 — Re: Des nouvelles un peu sombres — trames 14

**Idée non étayée :**

> 125. Le demandeur expliquait également qu'il ne pouvait dormir dans le sous-sol de la résidence familiale puisque celui-ci avait été démoli à la suite d'une inondation survenue en 2012 et n'avait pas été reconstruit, tel qu'il appert des pièces P-[13] et P-[14].

**Citation disponible :**

```text
Le sous sol on l'a démolie suite a une inondation l'année dernière et nous ne l'avons jamais terminé, préférant utiliser l'argent de l'assurance pour changer le système de chauffage.
```

#### 29. `legal/analyse/Responsabilité Déonthologique/2023-07-21.md` ligne ~136 → `pq-80`

- **distinction z = 4.9** — cosinus 0.659
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> Les données disponibles établissent que ces emplois se situent dans une fourchette de 35 360$ à 42 640$ selon les données gouvernementales disponibles en 2024, et que le demandeur a déclaré un revenu de 46 743,58$ en 2019, incluant des décaissements REER pour financer sa recherche d'emploi à temps plein.

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 30. `legal/requete_secton_faits_lp.md` ligne ~1025 → `pq-19` — *citation encore inexploitée*

- **distinction z = 4.9** — cosinus 0.622
- **source** : pdf-62 p.1 — Recherche CANLII MJA-Adelia Ferreira — trames —

**Idée non étayée :**

> 357. La requête du 19 novembre 2015 ayant été rédigée par Me Adelia Ferreira, le demandeur n'allègue aucune instruction ou communication entre Me Marie-Josée Ayoub et Me Ferreira qui ne soit établie par une preuve distincte.

**Citation disponible :**

```text
Le document est une recherche du site web CanLii qui retourne 266 résultats pour lesquels les avocate Marie-Josée Ayoub et Adélia Ferreira apparaissent ensemble
```

#### 31. `legal/allegation_stmt19_20_21_acces.md` ligne ~34 → `eq-71`

- **distinction z = 4.9** — cosinus 0.768  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-78 — (sans objet) — trames 44, 62

**Idée non étayée :**

> 0b. La demanderesse a déjà emmené Alexia en voyage à l'étranger depuis que celle-ci avait 14 à 16 mois (Cuba, hiver 2010-2011 ; voir thread 63, email id=78). Son prochain déplacement - un voyage à Cuba avec les deux enfants - est prévu peu après le retour du défendeur de Cape Cod.

**Citation disponible :**

```text
Elise veut partir a Cuba au mois de fevrier avec la petite, peut elle faire
ca?
```

#### 32. `legal/pont/pont_par4-5-6_2015.md` ligne ~299 → `eq-96`

- **distinction z = 4.9** — cosinus 0.846  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-16 — Re: Dépenses — trames 50, 56, 74

**Idée non étayée :**

> 15. Le même jour, la demanderesse a répondu qu'elle avait demandé à son avocate d'enlever cette partie, car elle ne voulait pas que cela soit écrit comme cela, ajoutant que la question posée portait sur le fait de savoir si le défendeur s'en occupait 50 % du temps (Email id=16).

**Citation disponible :**

```text
J'ai dit à l'avocat d'enlever cette partie car je ne voulais pas que cela soit écrit comme ça elle m'a seulement demandé si tu t'en occupais 50% du temps et si tu es honnête tu saurais que non.
```

#### 33. `legal/ponts_requete_2015_consolides.md` ligne ~311 → `eq-96`

- **distinction z = 4.9** — cosinus 0.846  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-16 — Re: Dépenses — trames 50, 56, 74

**Idée non étayée :**

> 15. Le même jour, la demanderesse a répondu qu'elle avait demandé à son avocate d'enlever cette partie, car elle ne voulait pas que cela soit écrit comme cela, ajoutant que la question posée portait sur le fait de savoir si le défendeur s'en occupait 50 % du temps (Email id=16).

**Citation disponible :**

```text
J'ai dit à l'avocat d'enlever cette partie car je ne voulais pas que cela soit écrit comme ça elle m'a seulement demandé si tu t'en occupais 50% du temps et si tu es honnête tu saurais que non.
```

#### 34. `legal/faits/faits_par56-57_2015.md` ligne ~31 → `pq-100`

- **distinction z = 4.7** — cosinus 0.739
- **source** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 9. Les mêmes relevés documentent trois transactions de type N au nom des enfants durant l'été 2015. Pour chacune, une dépense de 110 $ a été déboursée intégralement hors du paiement direct, puis 88 $ ont été remboursés au compte du participant, laissant 22 $ non remboursés : 9 juillet (Alexia), 24 juillet (Nicolas) et 30 juillet (Alexia).

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

#### 35. `legal/compilation_griefs.md` ligne ~1940 → `pq-79`

- **distinction z = 4.7** — cosinus 0.609
- **source** : pdf-67 p.1 — Salaire Technicien/technicienne en pharmacie au Québec - 202 — trames 62

**Idée non étayée :**

> 209. Le Guichet-Emplois de Statistique Canada établit le taux horaire médian 2024 pour technicien en laboratoire à **17 $/h** (source : Guichet-Emplois - connaissance d'office).

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION, Technicien/technicienne en pharmacie au Québec, Région de la Montérégie bas 15,25 median 17,00 haut 25,00 - Date de modification : 2023-01-23
```

#### 36. `legal/faits/faits_par7-8_2023.md` ligne ~56 → `pq-79`

- **distinction z = 4.7** — cosinus 0.609
- **source** : pdf-67 p.1 — Salaire Technicien/technicienne en pharmacie au Québec - 202 — trames 62

**Idée non étayée :**

> 209. Le Guichet-Emplois de Statistique Canada établit le taux horaire médian 2024 pour technicien en laboratoire à **17 $/h** (source : Guichet-Emplois - connaissance d'office).

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION, Technicien/technicienne en pharmacie au Québec, Région de la Montérégie bas 15,25 median 17,00 haut 25,00 - Date de modification : 2023-01-23
```

#### 37. `legal/analyse/Responsabilité Déonthologique/2023-07-21.md` ligne ~118 → `pq-80`

- **distinction z = 4.6** — cosinus 0.620
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> Par ailleurs, les emplois invoqués correspondent à des niveaux de revenus inférieurs au revenu réel déclaré par le demandeur en 2019 - 46 743,58$ - sans que cette relation ne soit explicitée.

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 38. `legal/compilation_griefs.md` ligne ~319 → `eq-181`

- **distinction z = 4.6** — cosinus 0.706  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-118 — Re: RE: Today — trames 50, 67

**Idée non étayée :**

> 30. Le 3 mai 2011, le défendeur a contesté un diagnostic médical concernant Alexia ; un second médecin, consulté ensuite, a confirmé son appréciation : « it turns out i was right » (Email id=118).

**Citation disponible :**

```text
i went to the doctor yesterday he prescribed something that i believed not adequate and my girlfriend went to see another doctor today and it turns out i was right
```

#### 39. `legal/faits/faits_par7_2015.md` ligne ~95 → `eq-181`

- **distinction z = 4.6** — cosinus 0.706  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-118 — Re: RE: Today — trames 50, 67

**Idée non étayée :**

> 30. Le 3 mai 2011, le défendeur a contesté un diagnostic médical concernant Alexia ; un second médecin, consulté ensuite, a confirmé son appréciation : « it turns out i was right » (Email id=118).

**Citation disponible :**

```text
i went to the doctor yesterday he prescribed something that i believed not adequate and my girlfriend went to see another doctor today and it turns out i was right
```

#### 40. `legal/analyse/Responsabilité Déonthologique/2023-07-21.md` ligne ~136 → `pq-81`

- **distinction z = 4.6** — cosinus 0.625
- **source** : pdf-30 p.1 — Avis de cotisation 2019 — trames 62

**Idée non étayée :**

> Les données disponibles établissent que ces emplois se situent dans une fourchette de 35 360$ à 42 640$ selon les données gouvernementales disponibles en 2024, et que le demandeur a déclaré un revenu de 46 743,58$ en 2019, incluant des décaissements REER pour financer sa recherche d'emploi à temps plein.

**Citation disponible :**

```text
Revenus Net : 41788,58
Prestations d'assurance emploi : 8752.00
Retrait REER : 37991.58
```

#### 41. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~37 → `eq-98`

- **distinction z = 4.6** — cosinus 0.601
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> 13. Les parties ont néanmoins repris la vie commune après cette séparation temporaire, laquelle s'est poursuivie jusqu'au départ du demandeur le 23 février 2015, tel qu'il appert de la pièce P-[●].

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 42. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~37 → `eq-98`

- **distinction z = 4.6** — cosinus 0.601
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> 13. Les parties ont néanmoins repris la vie commune après cette séparation temporaire, laquelle s'est poursuivie jusqu'au départ du demandeur le 23 février 2015, tel qu'il appert de la pièce P-[●].

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 43. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~37 → `eq-98`

- **distinction z = 4.6** — cosinus 0.601
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> 13. Les parties ont néanmoins repris la vie commune après cette séparation temporaire, laquelle s'est poursuivie jusqu'au départ du demandeur le 23 février 2015, tel qu'il appert de la pièce P-[●].

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 44. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~37 → `eq-98`

- **distinction z = 4.6** — cosinus 0.601
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> 13. Les parties ont néanmoins repris la vie commune après cette séparation temporaire, laquelle s'est poursuivie jusqu'au départ du demandeur le 23 février 2015, tel qu'il appert de la pièce P-[●].

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 45. `legal/analyse/Responsabilité Déonthologique/2015 avril, aout.md` ligne ~106 → `eq-93`

- **distinction z = 4.6** — cosinus 0.675
- **source** : email-343 — Re: Baptême de Nicolas — trames 44

**Idée non étayée :**

> Élise Ayoub informe les grands-parents paternels par courriel que Nicolas sera baptisé le lendemain à 14h00. Le père apprend l'existence de ce baptême par la réponse de sa mère aux grands-parents. Il indique qu'il n'a pas été invité et qu'il ignorait que Nicolas allait être baptisé. Le baptême constitue une décision relevant de l'autorité parentale en droit québécois - il engage l'appartenance religieuse de l'enfant et constitue une décision d'importance au sens des obligations parentales reconnues par la loi.

**Citation disponible :**

```text
Moi j y vais pas j ai pas ete invité et en fait je savais pas qu elle le
faisias baptiser.... Bonjour, demain le 19 juillet à 14:00 je ferais baptiser Nicolas a l'église st Thomas d'aquin. Si vous avez envie d'être présentes à la cérémonie vous êtes les bienvenus.
```

#### 46. `legal/expose/sections/01_par4-6_implication_parentale.md` ligne ~41 → `eq-98`

- **distinction z = 4.6** — cosinus 0.609
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> [XX]. Les parties ont néanmoins repris la vie commune après cette séparation temporaire, laquelle s'est poursuivie jusqu'au départ du demandeur le 23 février 2015, tel qu'il appert de la pièce P-[●].

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 47. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~1064 → `eq-142`

- **distinction z = 4.6** — cosinus 0.704
- **source** : email-410 — Re: Vacation à la cour — trames 62

**Idée non étayée :**

> 417. Le jugement rendu à la suite de cette audience a fixé la pension alimentaire sur le fondement d'un revenu retenu de 64 028,34 $, sans retenir les salaires des offres d'emploi ainsi déposées, tel qu'il appert de la même pièce.

**Citation disponible :**

```text
la pension alimentaire ne sera pas modifiée à ce stade-ci.  Nous avons procédé à des représentations aux stades intérimaires et malgré tes demandes de réduction et/ou de suspension de la pension, la juge a décidé que tu devais payer la pension même si tu n’avais pas d’emploi, vu entre autre tes économies et les besoins des enfants.
```

#### 48. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~1064 → `eq-142`

- **distinction z = 4.6** — cosinus 0.704
- **source** : email-410 — Re: Vacation à la cour — trames 62

**Idée non étayée :**

> 417. Le jugement rendu à la suite de cette audience a fixé la pension alimentaire sur le fondement d'un revenu retenu de 64 028,34 $, sans retenir les salaires des offres d'emploi ainsi déposées, tel qu'il appert de la même pièce.

**Citation disponible :**

```text
la pension alimentaire ne sera pas modifiée à ce stade-ci.  Nous avons procédé à des représentations aux stades intérimaires et malgré tes demandes de réduction et/ou de suspension de la pension, la juge a décidé que tu devais payer la pension même si tu n’avais pas d’emploi, vu entre autre tes économies et les besoins des enfants.
```

#### 49. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~1064 → `eq-142`

- **distinction z = 4.6** — cosinus 0.704
- **source** : email-410 — Re: Vacation à la cour — trames 62

**Idée non étayée :**

> 417. Le jugement rendu à la suite de cette audience a fixé la pension alimentaire sur le fondement d'un revenu retenu de 64 028,34 $, sans retenir les salaires des offres d'emploi ainsi déposées, tel qu'il appert de la même pièce.

**Citation disponible :**

```text
la pension alimentaire ne sera pas modifiée à ce stade-ci.  Nous avons procédé à des représentations aux stades intérimaires et malgré tes demandes de réduction et/ou de suspension de la pension, la juge a décidé que tu devais payer la pension même si tu n’avais pas d’emploi, vu entre autre tes économies et les besoins des enfants.
```

#### 50. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~1064 → `eq-142`

- **distinction z = 4.6** — cosinus 0.704
- **source** : email-410 — Re: Vacation à la cour — trames 62

**Idée non étayée :**

> 417. Le jugement rendu à la suite de cette audience a fixé la pension alimentaire sur le fondement d'un revenu retenu de 64 028,34 $, sans retenir les salaires des offres d'emploi ainsi déposées, tel qu'il appert de la même pièce.

**Citation disponible :**

```text
la pension alimentaire ne sera pas modifiée à ce stade-ci.  Nous avons procédé à des représentations aux stades intérimaires et malgré tes demandes de réduction et/ou de suspension de la pension, la juge a décidé que tu devais payer la pension même si tu n’avais pas d’emploi, vu entre autre tes économies et les besoins des enfants.
```

#### 51. `legal/requete_secton_faits_lp.md` ligne ~1241 → `eq-142`

- **distinction z = 4.6** — cosinus 0.704
- **source** : email-410 — Re: Vacation à la cour — trames 62

**Idée non étayée :**

> 417. Le jugement rendu à la suite de cette audience a fixé la pension alimentaire sur le fondement d'un revenu retenu de 64 028,34 $, sans retenir les salaires des offres d'emploi ainsi déposées, tel qu'il appert de la même pièce.

**Citation disponible :**

```text
la pension alimentaire ne sera pas modifiée à ce stade-ci.  Nous avons procédé à des représentations aux stades intérimaires et malgré tes demandes de réduction et/ou de suspension de la pension, la juge a décidé que tu devais payer la pension même si tu n’avais pas d’emploi, vu entre autre tes économies et les besoins des enfants.
```

#### 52. `legal/compilation_griefs.md` ligne ~135 → `eq-181`

- **distinction z = 4.6** — cosinus 0.692  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-118 — Re: RE: Today — trames 50, 67

**Idée non étayée :**

> 31. Le 3 mai 2011, le défendeur a contesté un diagnostic médical concernant Alexia ; un second médecin l'a confirmé : « it turns out i was right » (Email id=118).

**Citation disponible :**

```text
i went to the doctor yesterday he prescribed something that i believed not adequate and my girlfriend went to see another doctor today and it turns out i was right
```

#### 53. `legal/faits/faits_par4-5-6_2015.md` ligne ~123 → `eq-181`

- **distinction z = 4.6** — cosinus 0.692  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-118 — Re: RE: Today — trames 50, 67

**Idée non étayée :**

> 31. Le 3 mai 2011, le défendeur a contesté un diagnostic médical concernant Alexia ; un second médecin l'a confirmé : « it turns out i was right » (Email id=118).

**Citation disponible :**

```text
i went to the doctor yesterday he prescribed something that i believed not adequate and my girlfriend went to see another doctor today and it turns out i was right
```

#### 54. `legal/journal_ete2013.md` ligne ~41 → `eq-14`

- **distinction z = 4.6** — cosinus 0.684
- **source** : email-38 — Consultation — trames 2

**Idée non étayée :**

> **2013-07-02** - Emails M38 / M131 / M132 / M133 / M129 / M130 : LP contacte le thérapeute François St-Père pour un rendez-vous de thérapie de couple. LP confirme sa disponibilité - en soirée de préférence, sinon le matin. LP est en congé jusqu'au 12 juillet.

**Citation disponible :**

```text
Bonjours M St-Pere, Je vous contact afin de m'informer de vos disponibilités pour une thérapie de couple. Merci
```

#### 55. `legal/piece_pdf-84.md` ligne ~9 → `pq-77` — *citation encore inexploitée*

- **distinction z = 4.5** — cosinus 0.692
- **source** : pdf-72 p.1 — Permis de travail — trames —

**Idée non étayée :**

> - **Requérante principale : SILVIA FLORENTINA BALAN** (conjointe du défendeur), née le **30 août 1986**, Medgidia, **Roumanie** ; citoyenne roumaine ; passeport roumain 050578518.
> - **Date du dépôt : 2016-06-13.** N° de demande : **D0000001500**.
> - **Programme : régulier des travailleurs qualifiés.** Région d'établissement visée : **Montréal**.
> - Formation : maîtrise (gestion et communication d'entreprise), licence (communication / relations publiques) ; IELTS 2015.
> - Emploi : Parc Hôtel Roumanie (relations publiques) à Bucarest.
> - Famille au Québec : sœur (Balan Elena-Ligia, Saint-Hubert). Numéro d'identification CIC : 30007083.

**Citation disponible :**

```text
MINISTÈRE DES AFFAIRES INTÉRIEURES INSPECTION GÉNÉRALE DE L'IMMIGRATION 
Exemplaire n°1 du 12.02.2020 
Sur la base de la demande enregistrée sous le numéro 948264 et de la documentation déposée par ALLIANZ TECHNOLOGY SE MUNCHEN SUCCURSALE BUCAREST ayant son siège/domicile à Bucarest n° d'enreg. au Registre du commerce J40/7518/2013 code fiscal/CNP 31824525 
L'INSPECTION GÉNÉRALE DE L'IMMIGRATION accorde 
L'AVIS DE TRAVAIL 
n° 2005418 
du 04.03.2020 
nécessaire à l'obtention du visa de long séjour / permis de séjour à des fins de travail, en qualité de travailleur PERMANENT code fonction COR 242102 
à Madame/Monsieur DAVID LOUIS-PHILIPPE né/née le 22.07.1976 au CANADA passeport n° GJ094299 délivré par CANADA 
Date de remise :
10.03.2020 
INSPECTEUR GÉNÉRAL 
```

#### 56. `legal/pont/pont_par4-5-6_2015.md` ligne ~155 → `eq-96`

- **distinction z = 4.5** — cosinus 0.782
- **source** : email-16 — Re: Dépenses — trames 50, 56, 74

**Idée non étayée :**

> 44. Le même jour, la demanderesse a répondu qu'elle avait demandé à son avocate d'enlever cette partie, car elle ne voulait pas que cela soit écrit comme cela.

**Citation disponible :**

```text
J'ai dit à l'avocat d'enlever cette partie car je ne voulais pas que cela soit écrit comme ça elle m'a seulement demandé si tu t'en occupais 50% du temps et si tu es honnête tu saurais que non.
```

#### 57. `legal/ponts_requete_2015_consolides.md` ligne ~167 → `eq-96`

- **distinction z = 4.5** — cosinus 0.782
- **source** : email-16 — Re: Dépenses — trames 50, 56, 74

**Idée non étayée :**

> 44. Le même jour, la demanderesse a répondu qu'elle avait demandé à son avocate d'enlever cette partie, car elle ne voulait pas que cela soit écrit comme cela.

**Citation disponible :**

```text
J'ai dit à l'avocat d'enlever cette partie car je ne voulais pas que cela soit écrit comme ça elle m'a seulement demandé si tu t'en occupais 50% du temps et si tu es honnête tu saurais que non.
```

#### 58. `legal/piece_formulaire_pension_2019.md` ligne ~15 → `pq-80`

- **distinction z = 4.5** — cosinus 0.651
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> → Le **99 271,79 $ = le revenu NET** de la déclaration 2018 d'Élise (l. 275), **inscrit à la ligne « Salaire BRUT »**. Cette déclaration indique plutôt un revenu d'emploi de **111 818,72 $** (l. 101) et un revenu total de **112 569,08 $** (l. 199). *(Le père : ligne 200 = 64 028,34 = son revenu composite, sans ventilation.)*

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 59. `legal/demande_DEPOT_2026-07-21.md` ligne ~573 → `pq-100`

- **distinction z = 4.5** — cosinus 0.703
- **source** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 217. Le montant total réclamé est de 244 779 $, composé de 128 059 $ en dommages-intérêts compensatoires réclamés solidairement et de 116 720 $ en dommages-intérêts punitifs individualisés. Le demandeur réclame, sur les dommages-intérêts compensatoires, les intérêts au taux légal et l'indemnité additionnelle prévue à l'article 1619 C.c.Q. depuis l'assignation.

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

#### 60. `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.md` ligne ~573 → `pq-100`

- **distinction z = 4.5** — cosinus 0.703
- **source** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 217. Le montant total réclamé est de 244 779 $, composé de 128 059 $ en dommages-intérêts compensatoires réclamés solidairement et de 116 720 $ en dommages-intérêts punitifs individualisés. Le demandeur réclame, sur les dommages-intérêts compensatoires, les intérêts au taux légal et l'indemnité additionnelle prévue à l'article 1619 C.c.Q. depuis l'assignation.

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

#### 61. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 56 57.md` ligne ~49 → `pq-99`

- **distinction z = 4.4** — cosinus 0.657
- **source** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> Les relevés Industrielle Alliance documentent treize transactions de type P, pour lesquelles l'assureur a versé la portion couverte au fournisseur, entre le 25 février 2015 et le 16 mai 2016.

**Citation disponible :**

```text
Transactions 2015 — Paiements directs au fournisseur (type P) : 25 fév (Nicolas/Santé), 16 avr (Nicolas/Santé), 4 mai (Nicolas/Santé), 7 juil (Alexia/Dentaire), 17 sep (Alexia/Santé), 1 oct (Nicolas/Santé), 17 oct (Nicolas/Santé). Toutes hors dimanche.
```

#### 62. `legal/organisation_preuve/2015_par_23_24.md` ligne ~131 → `eq-90`

- **distinction z = 4.4** — cosinus 0.560
- **source** : email-402 — Re: Ayoub c. David — trames 9, 34, 38, 39, 42, 49, 52

**Idée non étayée :**

> Elles expliquent le motif interne du maintien des accès existants, mais ne sont pas nécessaires pour établir la contradiction temporelle centrale.

**Citation disponible :**

```text
Puisqu'il n'est pas dans l'intérêt des enfants de modifier une routine établie depuis plus deux mois, nous garderons les droits d'acces tels qu'ils sont actuelement.
```

#### 63. `legal/expose_faits_volet_2015.md` ligne ~195 → `pq-100`

- **distinction z = 4.4** — cosinus 0.562
- **source** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> 82. En août 2014, la défenderesse a reçu du demandeur un prêt de 9 000 $, remboursable par crédit de loyer de 750 $ par mois (pièce à coter : messagerie des parties).

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

#### 64. `legal/piece_formulaire_pension_2019.md` ligne ~15 → `pq-81`

- **distinction z = 4.4** — cosinus 0.645
- **source** : pdf-30 p.1 — Avis de cotisation 2019 — trames 62

**Idée non étayée :**

> → Le **99 271,79 $ = le revenu NET** de la déclaration 2018 d'Élise (l. 275), **inscrit à la ligne « Salaire BRUT »**. Cette déclaration indique plutôt un revenu d'emploi de **111 818,72 $** (l. 101) et un revenu total de **112 569,08 $** (l. 199). *(Le père : ligne 200 = 64 028,34 = son revenu composite, sans ventilation.)*

**Citation disponible :**

```text
Revenus Net : 41788,58
Prestations d'assurance emploi : 8752.00
Retrait REER : 37991.58
```

#### 65. `legal/expose_faits_volet_2015.md` ligne ~233 → `eq-98`

- **distinction z = 4.4** — cosinus 0.646
- **source** : email-171 — Re: Cle — trames 53, 74

**Idée non étayée :**

> 98. Le 27 février 2015, la défenderesse a écrit au demandeur qu'ils ne faisaient pas chambre à part et qu'ils avaient des activités communes (même pièce).

**Citation disponible :**

```text
[...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
```

#### 66. `legal/demande_DEPOT_2026-07-21.md` ligne ~42 → `pq-19` — *citation encore inexploitée*

- **distinction z = 4.4** — cosinus 0.633
- **source** : pdf-62 p.1 — Recherche CANLII MJA-Adelia Ferreira — trames —

**Idée non étayée :**

> 4. De 2013 à 2023, la défenderesse Me Marie-Josée Ayoub a rédigé, préparé ou présenté plusieurs des courriels, projets et actes qui lui sont précisément attribués dans l'exposé des faits. La Requête du 19 novembre 2015 a toutefois été rédigée par Me Adelia Ferreira; le demandeur n'allègue aucune instruction ou communication entre Me Marie-Josée Ayoub et Me Ferreira qui ne soit établie par une preuve distincte.

**Citation disponible :**

```text
Le document est une recherche du site web CanLii qui retourne 266 résultats pour lesquels les avocate Marie-Josée Ayoub et Adélia Ferreira apparaissent ensemble
```

#### 67. `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.md` ligne ~42 → `pq-19` — *citation encore inexploitée*

- **distinction z = 4.4** — cosinus 0.633
- **source** : pdf-62 p.1 — Recherche CANLII MJA-Adelia Ferreira — trames —

**Idée non étayée :**

> 4. De 2013 à 2023, la défenderesse Me Marie-Josée Ayoub a rédigé, préparé ou présenté plusieurs des courriels, projets et actes qui lui sont précisément attribués dans l'exposé des faits. La Requête du 19 novembre 2015 a toutefois été rédigée par Me Adelia Ferreira; le demandeur n'allègue aucune instruction ou communication entre Me Marie-Josée Ayoub et Me Ferreira qui ne soit établie par une preuve distincte.

**Citation disponible :**

```text
Le document est une recherche du site web CanLii qui retourne 266 résultats pour lesquels les avocate Marie-Josée Ayoub et Adélia Ferreira apparaissent ensemble
```

#### 68. `legal/piece_event-278.md` ligne ~28 → `eq-61`

- **distinction z = 4.4** — cosinus 0.613
- **source** : email-116 — Re: ce soir — trames 31

**Idée non étayée :**

> - LP et Élise n'apparaissent pas dans les photographies.
> - Les images ne prouvent pas seules qu'Élise se trouve à la danse ni que LP est présent hors champ.
> - La séquence photographique couvre moins de deux minutes; elle ne décrit pas toute la soirée.
> - L'extension aux autres lundis dépend de la preuve combinée de la structure fixe de la session et du témoignage sur le mode normal de prise en charge; elle ne découle pas de cette photographie isolément.

**Citation disponible :**

```text
salut ce soir elise ne va pas a son premier cour de danse je sais pas a quelle heure elle va partit
```

#### 69. `legal/piece_thread-6_email-8.md` ligne ~39 → `eq-60`

- **distinction z = 4.4** — cosinus 0.645
- **source** : email-8 — Re: Visite — trames 11, 50

**Idée non étayée :**

> **Analyse calibrée :** la critique d'Élise présuppose une participation de LP à une activité de natation organisée sur dix semaines. Elle est pertinente pour établir qu'il ne demeurait pas étranger aux activités des enfants. Elle lui reproche d'avoir été « tanné » après cette période, ce qui peut limiter l'appréciation de son endurance ou de sa motivation, mais ne transforme pas la participation reconnue en absence d'implication.

**Citation disponible :**

```text
Apres un cours de 10 semaines de natation tu étais tanné....
```

#### 70. `legal/piece_pdf-15.md` ligne ~18 → `pq-74`

- **distinction z = 4.4** — cosinus 0.753
- **source** : pdf-13 p.2 — Jugement sur le fond (perte emplois) — trames 62

**Idée non étayée :**

> Appel de la cause → représentations de M. David (discussion avec le tribunal) → 11 h 29 représentations de Me Ayoub → 11 h 31 réplique de Monsieur (salaire / arrérages) → 11 h 32 représentations de Me Ayoub → échanges Tribunal / Me Ayoub / Monsieur → 11 h 39 discussion Tribunal / Me Ayoub → 11 h 41 discussion Tribunal / M. David → 11 h 41 réplique de Me Ayoub → échange Tribunal / Madame → 11 h 55 jugement → 11 h 59 fin.

**Citation disponible :**

```text
10h13:11 Témoignage de M. David – Questions du Tribunal.
Objection de Me Ayoub (un jugement a été prononcé en 2016 sur ces sujets) ;
Le Tribunal prend connaissance du jugement de 2016 ;

10h17:04 Le Tribunal informe Monsieur de ne pas parler de ce qui s'est passé avant 2016.
Suite du témoignage de M. David
```

#### 71. `legal/demande_DEPOT_2026-07-21.md` ligne ~543 → `eq-142`

- **distinction z = 4.4** — cosinus 0.687
- **source** : email-410 — Re: Vacation à la cour — trames 62

**Idée non étayée :**

> 208. Le demandeur allègue que le solde de pension et ses conséquences demeurent actuels parce que la pension n'a pas été ajustée à sa capacité réelle de payer. Cette allégation de continuité ne remplace pas la preuve de la causalité propre à chacun des deux postes compensatoires réclamés.

**Citation disponible :**

```text
la pension alimentaire ne sera pas modifiée à ce stade-ci.  Nous avons procédé à des représentations aux stades intérimaires et malgré tes demandes de réduction et/ou de suspension de la pension, la juge a décidé que tu devais payer la pension même si tu n’avais pas d’emploi, vu entre autre tes économies et les besoins des enfants.
```

#### 72. `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.md` ligne ~543 → `eq-142`

- **distinction z = 4.4** — cosinus 0.687
- **source** : email-410 — Re: Vacation à la cour — trames 62

**Idée non étayée :**

> 208. Le demandeur allègue que le solde de pension et ses conséquences demeurent actuels parce que la pension n'a pas été ajustée à sa capacité réelle de payer. Cette allégation de continuité ne remplace pas la preuve de la causalité propre à chacun des deux postes compensatoires réclamés.

**Citation disponible :**

```text
la pension alimentaire ne sera pas modifiée à ce stade-ci.  Nous avons procédé à des représentations aux stades intérimaires et malgré tes demandes de réduction et/ou de suspension de la pension, la juge a décidé que tu devais payer la pension même si tu n’avais pas d’emploi, vu entre autre tes économies et les besoins des enfants.
```

#### 73. `legal/analyse/Responsabilité civile/requete 21 octobre 2019/analyse preliminaire - echec negociations 2015 et paragraphe 3.md` ligne ~666 → `eq-93`

- **distinction z = 4.4** — cosinus 0.628
- **source** : email-343 — Re: Baptême de Nicolas — trames 44

**Idée non étayée :**

> Le 18 juillet, la mère informe les grands-parents paternels que Nicolas sera baptisé le lendemain. Le 19 juillet, le père écrit :

**Citation disponible :**

```text
Moi j y vais pas j ai pas ete invité et en fait je savais pas qu elle le
faisias baptiser.... Bonjour, demain le 19 juillet à 14:00 je ferais baptiser Nicolas a l'église st Thomas d'aquin. Si vous avez envie d'être présentes à la cérémonie vous êtes les bienvenus.
```

#### 74. `legal/axe_agenda_danse_elise.md` ligne ~109 → `eq-61`

- **distinction z = 4.3** — cosinus 0.637  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : email-116 — Re: ce soir — trames 31

**Idée non étayée :**

> 15. Le 15 mars 2011, le demandeur a répondu à Johanne Bazinet que la défenderesse n'allait pas à son premier cours de danse ce soir-là (P-X, Email 116).

**Citation disponible :**

```text
salut ce soir elise ne va pas a son premier cour de danse je sais pas a quelle heure elle va partit
```

#### 75. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~1050 → `pq-80`

- **distinction z = 4.3** — cosinus 0.621
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> 411. Le revenu déclaré du demandeur pour l'année 2019 était de 46 743,58 $, et son revenu d'emploi pour l'année 2018 était de 47 520,51 $, tel qu'il appert des pièces P-[●] et P-[●].

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 76. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~1050 → `pq-80`

- **distinction z = 4.3** — cosinus 0.621
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> 411. Le revenu déclaré du demandeur pour l'année 2019 était de 46 743,58 $, et son revenu d'emploi pour l'année 2018 était de 47 520,51 $, tel qu'il appert des pièces P-[●] et P-[●].

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 77. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~1050 → `pq-80`

- **distinction z = 4.3** — cosinus 0.621
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> 411. Le revenu déclaré du demandeur pour l'année 2019 était de 46 743,58 $, et son revenu d'emploi pour l'année 2018 était de 47 520,51 $, tel qu'il appert des pièces P-[●] et P-[●].

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 78. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~1050 → `pq-80`

- **distinction z = 4.3** — cosinus 0.621
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> 411. Le revenu déclaré du demandeur pour l'année 2019 était de 46 743,58 $, et son revenu d'emploi pour l'année 2018 était de 47 520,51 $, tel qu'il appert des pièces P-[●] et P-[●].

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 79. `legal/organisation_preuve/2015_par_20.md` ligne ~145 → `pq-79`

- **distinction z = 4.3** — cosinus 0.677
- **source** : pdf-67 p.1 — Salaire Technicien/technicienne en pharmacie au Québec - 202 — trames 62

**Idée non étayée :**

> [1]: https://www.legisquebec.gouv.qc.ca/fr/version/lc/C-26?code=se%3A60_4&historique=20220520&utm_source=chatgpt.com "Code des professions - Légis Québec"

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION, Technicien/technicienne en pharmacie au Québec, Région de la Montérégie bas 15,25 median 17,00 haut 25,00 - Date de modification : 2023-01-23
```

#### 80. `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/03_anteriorite_preference_et_fonction_du_registre.md` ligne ~164 → `pq-7`

- **distinction z = 4.3** — cosinus 0.713
- **source** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 7, 48, 49, 70, 72

**Idée non étayée :**

> Si la sécurité et le développement sont réellement compromis, le maintien des
> liens affectifs ne peut justifier, **avant que ce risque soit maîtrisé**, un
> régime autonome comportant de nombreuses nuitées et proche du partage égal. Le
> lien pourrait être préservé par des accès adaptés ou supervisés; il ne peut
> servir à contourner le risque affirmé.

**Citation disponible :**

```text
tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.
```

#### 81. `legal/analyse/Responsabilité Déonthologique/2023-07-21.md` ligne ~118 → `pq-81`

- **distinction z = 4.3** — cosinus 0.586
- **source** : pdf-30 p.1 — Avis de cotisation 2019 — trames 62

**Idée non étayée :**

> Par ailleurs, les emplois invoqués correspondent à des niveaux de revenus inférieurs au revenu réel déclaré par le demandeur en 2019 - 46 743,58$ - sans que cette relation ne soit explicitée.

**Citation disponible :**

```text
Revenus Net : 41788,58
Prestations d'assurance emploi : 8752.00
Retrait REER : 37991.58
```

#### 82. `legal/poursuite_expose_des_faits.md` ligne ~76 → `eq-164` — *citation encore inexploitée*

- **distinction z = 4.3** — cosinus 0.634
- **source** : email-130 — Re: Consultation — trames —

**Idée non étayée :**

> 26. Pendant la période alléguée, Élise Marie Ayoub a organisé une fête surprise pour le demandeur (Pièce [fête 2013]). `[à sourcer]`

**Citation disponible :**

```text
Elise Marie Ayoub, je vous donnes une reponse demain.
```

#### 83. `legal/memoire faille structurelle.md` ligne ~196 → `pq-68`

- **distinction z = 4.3** — cosinus 0.763
- **source** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 62

**Idée non étayée :**

> Lorsqu'une procédure d'urgence aboutit à un résultat qui révèle a posteriori que les allégations ne correspondaient pas à la réalité invoquée, aucun mécanisme institutionnel automatique ne déclenche un examen de la sincérité initiale. La procédure disciplinaire du Barreau n'est déclenchée que par une plainte. La plainte exige que la partie adverse dispose des éléments documentaires nécessaires pour la formuler - éléments qui sont précisément protégés par le secret professionnel.

**Citation disponible :**

```text
En urgence on appelle cela une ordonnance de sauvegarde. Lors de cette procédure d'urgence le juge en question n'entend pas de témoin c'est seulement les avocats qui plaident. C'est rapide et urgent
```

#### 84. `legal/allegation_stmt56_57_58_assurances.md` ligne ~123 → `pq-100`

- **distinction z = 4.3** — cosinus 0.628
- **source** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> Les transactions N établissent, pour chacune, un débours de 110 $, un remboursement de 88 $ au participant et un solde non couvert de 22 $. Elles n'établissent pas qui a avancé les 110 $.

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

#### 85. `legal/implication_parentale_recurrence/04_journees_maladie.md` ligne ~35 → `eq-181`

- **distinction z = 4.3** — cosinus 0.672
- **source** : email-118 — Re: RE: Today — trames 50, 67

**Idée non étayée :**

> - LP a accompagné Alexia chez le premier médecin;
> - il connaissait le traitement prescrit;
> - il jugeait ce traitement inadéquat;
> - Élise a consulté un second médecin le lendemain;
> - selon le compte rendu fait par LP à sa supérieure, la seconde consultation a confirmé son appréciation.

**Citation disponible :**

```text
i went to the doctor yesterday he prescribed something that i believed not adequate and my girlfriend went to see another doctor today and it turns out i was right
```

#### 86. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~831 → `pq-66`

- **distinction z = 4.3** — cosinus 0.674
- **source** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames 56

**Idée non étayée :**

> 322. Il proposait que la progression mène à une garde partagée selon un horaire 2-2-3 à compter du 7 février 2016, soit après une période transitoire d'environ six mois suivant le projet du 13 août 2015.

**Citation disponible :**

```text
Cependant, il souhaite ajouter un sous-paragraphe « e) » afin de prévoir qu'à compter du 7 février 2016 l'horaire de garde sera en alternance 2-2-3/2-2-3.
```

#### 87. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~831 → `pq-66`

- **distinction z = 4.3** — cosinus 0.674
- **source** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames 56

**Idée non étayée :**

> 322. Il proposait que la progression mène à une garde partagée selon un horaire 2-2-3 à compter du 7 février 2016, soit après une période transitoire d'environ six mois suivant le projet du 13 août 2015.

**Citation disponible :**

```text
Cependant, il souhaite ajouter un sous-paragraphe « e) » afin de prévoir qu'à compter du 7 février 2016 l'horaire de garde sera en alternance 2-2-3/2-2-3.
```

#### 88. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~831 → `pq-66`

- **distinction z = 4.3** — cosinus 0.674
- **source** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames 56

**Idée non étayée :**

> 322. Il proposait que la progression mène à une garde partagée selon un horaire 2-2-3 à compter du 7 février 2016, soit après une période transitoire d'environ six mois suivant le projet du 13 août 2015.

**Citation disponible :**

```text
Cependant, il souhaite ajouter un sous-paragraphe « e) » afin de prévoir qu'à compter du 7 février 2016 l'horaire de garde sera en alternance 2-2-3/2-2-3.
```

#### 89. `legal/requete_secton_faits_lp.md` ligne ~933 → `pq-66`

- **distinction z = 4.3** — cosinus 0.674
- **source** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames 56

**Idée non étayée :**

> 322. Il proposait que la progression mène à une garde partagée selon un horaire 2-2-3 à compter du 7 février 2016, soit après une période transitoire d'environ six mois suivant le projet du 13 août 2015.

**Citation disponible :**

```text
Cependant, il souhaite ajouter un sous-paragraphe « e) » afin de prévoir qu'à compter du 7 février 2016 l'horaire de garde sera en alternance 2-2-3/2-2-3.
```

#### 90. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~831 → `pq-66`

- **distinction z = 4.3** — cosinus 0.674
- **source** : pdf-6 p.2 — 20150902 FP réponse projet consentement — trames 56

**Idée non étayée :**

> 322. Il proposait que la progression mène à une garde partagée selon un horaire 2-2-3 à compter du 7 février 2016, soit après une période transitoire d'environ six mois suivant le projet du 13 août 2015.

**Citation disponible :**

```text
Cependant, il souhaite ajouter un sous-paragraphe « e) » afin de prévoir qu'à compter du 7 février 2016 l'horaire de garde sera en alternance 2-2-3/2-2-3.
```

#### 91. `legal/compilation_griefs.md` ligne ~727 → `pq-19` — *citation encore inexploitée*

- **distinction z = 4.3** — cosinus 0.637
- **source** : pdf-62 p.1 — Recherche CANLII MJA-Adelia Ferreira — trames —

**Idée non étayée :**

> - **Note rédactrice.** La Requête de 2015 est rédigée par **Me Ferreira** ; Me Ayoub est l'avocate correspondante, autrice de la lettre du 27 avril et du projet du 13 août, et sœur de la demanderesse.

**Citation disponible :**

```text
Le document est une recherche du site web CanLii qui retourne 266 résultats pour lesquels les avocate Marie-Josée Ayoub et Adélia Ferreira apparaissent ensemble
```

#### 92. `legal/analyse/Responsabilité Déonthologique/2023-07-21.md` ligne ~66 → `pq-78`

- **distinction z = 4.3** — cosinus 0.626
- **source** : pdf-66 p.1 — Revenus représentant au service à la clientèle — trames 62

**Idée non étayée :**

> Les données du Guichet-Emplois du gouvernement du Canada pour la région de la Montérégie établissent les salaires médians suivants pour deux des trois catégories d'emplois définies par Me Ayoub dans la déclaration assermentée de 2019 :

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION Représentant/représentante au service à la clientèle - services financiers au Québec Date de modification : 2024-01-23
Région de Montréal Salaire Bas : 16,28 Median 21,00 Haut : 26,99 
https://www.guichet-emplois.gc.ca/salaire-horaire/representant-representante-service-clientele-services-financiers/montreal
```

#### 93. `legal/faits_chronologiques_2010-11-20_2012-02-06.md` ligne ~62 → `pq-79`

- **distinction z = 4.3** — cosinus 0.625  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : pdf-67 p.1 — Salaire Technicien/technicienne en pharmacie au Québec - 202 — trames 62

**Idée non étayée :**

> **27.** Le 9 février 2011, les données d'Hydro Québec confirment que le Demandeur est demeuré responsable du compte d'électricité conjoint pour le 245 avenue MacAulay, Saint-Lambert (résidence familiale), ouvert depuis le 18 août 2009 au nom de Louis-Philippe David et Élise Ayoub. `[PhotoDocument id=2 | Chat Hydro Québec 245 ave Macaulay]`

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION, Technicien/technicienne en pharmacie au Québec, Région de la Montérégie bas 15,25 median 17,00 haut 25,00 - Date de modification : 2023-01-23
```

#### 94. `legal/dossier_plaidoirie/01_arc_garde_2013-2016.md` ligne ~1364 → `pq-10`

- **distinction z = 4.3** — cosinus 0.662
- **source** : pdf-3 p.2 — Réponse à l'offre de garde partagée — trames 9, 38, 55, 56, 71, 72, 73, 76

**Idée non étayée :**

> **La réponse est dans le silence de la lettre :** elle **ne précise pas** quelle
> composante de la routine devait être préservée, ni pourquoi les transitions
> qu'elle propose sont compatibles avec le jeune âge alors que celles d'un horaire
> 2‐2‐3 ne le seraient pas. Aucune comparaison n'y est faite, et aucun critère de
> progression n'y est posé.

**Citation disponible :**

```text
il y a contre-indication à l'établissement de la garde parlagée des deux (2) enfants mineurs vu leur jeune âge et qu'il n'est pas dans leur intérêt de modifier une routine établie depuis plus deux mois.
```

#### 95. `legal/allegation_stmt56_57_58_assurances.md` ligne ~60 → `pq-100`

- **distinction z = 4.2** — cosinus 0.566
- **source** : pdf-63 p.1 — relevé assurance 2015 — trames 68

**Idée non étayée :**

> Pour chacune de ces transactions, une dépense de 110 $ a été déboursée intégralement hors du paiement direct, puis 88 $ ont été remboursés au compte du participant, laissant 22 $ non remboursés.

**Citation disponible :**

```text
Remboursements au participant (dépôt direct, type N) — été 2015 : 9 juil (Alexia, 88,00$), 24 juil (Nicolas, 88,00$), 30 juil (Alexia, 88,00$). Confirme que le défendeur utilisait lui-même les assurances lorsqu'il avait les enfants.
```

#### 96. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 56 57.md` ligne ~49 → `pq-102`

- **distinction z = 4.2** — cosinus 0.632
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> Les relevés Industrielle Alliance documentent treize transactions de type P, pour lesquelles l'assureur a versé la portion couverte au fournisseur, entre le 25 février 2015 et le 16 mai 2016.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 97. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 20 21.md` ligne ~53 → `pq-10`

- **distinction z = 4.2** — cosinus 0.783
- **source** : pdf-3 p.2 — Réponse à l'offre de garde partagée — trames 9, 38, 55, 56, 71, 72, 73, 76

**Idée non étayée :**

> La lettre du 27 avril affirme qu'il n'est pas dans l'intérêt des enfants de modifier la routine établie depuis plus de deux mois. Elle ne distingue pas les changements brusques des changements graduels, ni les modifications importantes des modifications limitées.

**Citation disponible :**

```text
il y a contre-indication à l'établissement de la garde parlagée des deux (2) enfants mineurs vu leur jeune âge et qu'il n'est pas dans leur intérêt de modifier une routine établie depuis plus deux mois.
```

#### 98. `legal/piece_thread-26_emails-33-32.md` ligne ~20 → `eq-8`

- **distinction z = 4.2** — cosinus 0.643
- **source** : email-32 — Re: passe de plage Cape Cod — trames 2, 11, 66

**Idée non étayée :**

> Le fait qu'il n'y ait pas de soccer le lendemain est la première raison donnée en réponse au projet de venue avec Nicolas. LP ajoute qu'il passera peut-être malgré cette exception.

**Citation disponible :**

```text
  Y a pas dw soccer demain mais je passerai peut etre
```

#### 99. `legal/these_revenu_mere_verifiabilite.md` ligne ~9 → `pq-80`

- **distinction z = 4.2** — cosinus 0.698
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> Les **talons de paie transmis** à la partie adverse permettent d'inférer (au moins) **trois** revenus annuels distincts selon la méthode :
> - **89 566,88 $** - brut réel affiché (3 444,88 $ × 26), incluant **14 h de congé non rémunéré/période** ;
> - **111 671,82 $** - **taux de salaire** plein cycle (4 295,07 $ × 26) ;
> - **≈ 112 847 $** - cumulatif annualisé (65 104,42 $ ÷ 15 × 26).

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 100. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 20 21.md` ligne ~53 → `pq-27`

- **distinction z = 4.2** — cosinus 0.781
- **source** : pdf-3 p.2 — Réponse à l'offre de garde partagée — trames 34, 39, 42, 49, 71, 72, 73, 76

**Idée non étayée :**

> La lettre du 27 avril affirme qu'il n'est pas dans l'intérêt des enfants de modifier la routine établie depuis plus de deux mois. Elle ne distingue pas les changements brusques des changements graduels, ni les modifications importantes des modifications limitées.

**Citation disponible :**

```text
nous considérons qu'il y a contre-indication à l'établissement de la garde parlagée des deux (2) enfants mineurs vu leur jeune âge et qu'il n'est pas dans leur intérêt de modifier une routine établie depuis plus deux mois.
```

#### 101. `legal/analyse/Responsabilité Déonthologique/2019-09-27.md` ligne ~122 → `eq-142`

- **distinction z = 4.2** — cosinus 0.675
- **source** : email-410 — Re: Vacation à la cour — trames 62

**Idée non étayée :**

> Un talon ne représentant pas la rémunération à temps plein, utilisé comme base de calcul de la pension alimentaire, produirait un revenu annuel artificiellement réduit de 20% par rapport au taux contractuel. La pension alimentaire pour enfants étant d'ordre public, elle ne peut pas être diminuée par l'utilisation de pièces produisant une base de calcul artificiellement réduite.

**Citation disponible :**

```text
la pension alimentaire ne sera pas modifiée à ce stade-ci.  Nous avons procédé à des représentations aux stades intérimaires et malgré tes demandes de réduction et/ou de suspension de la pension, la juge a décidé que tu devais payer la pension même si tu n’avais pas d’emploi, vu entre autre tes économies et les besoins des enfants.
```

#### 102. `legal/compilation_griefs.md` ligne ~2034 → `pq-80`

- **distinction z = 4.2** — cosinus 0.679
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> 235-quinquies. Une pension alimentaire était **payable sur le revenu déclaré** du Demandeur pour **2018** (revenu total 64 028,34 $) et **2019** (revenu total 46 743,58 $) ; ces deux montants sont **supérieurs** aux salaires des emplois suggérés (b)/(c) (31 470 $ - 42 640 $ selon l'année) *(fait déductif - faits 221, 235, 234/237)*.

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 103. `legal/faits/faits_par7-8_2023.md` ligne ~150 → `pq-80`

- **distinction z = 4.2** — cosinus 0.679
- **source** : pdf-35 p.1 — Avis de cotisation 2018 — trames 62

**Idée non étayée :**

> 235-quinquies. Une pension alimentaire était **payable sur le revenu déclaré** du Demandeur pour **2018** (revenu total 64 028,34 $) et **2019** (revenu total 46 743,58 $) ; ces deux montants sont **supérieurs** aux salaires des emplois suggérés (b)/(c) (31 470 $ - 42 640 $ selon l'année) *(fait déductif - faits 221, 235, 234/237)*.

**Citation disponible :**

```text
Revenu total : 64028,34
Revenus d'emplois (janvier a juin) : 47520, 51
Prestations d'assurance emploi : 12034,00
Retrait REER : 4089,60
```

#### 104. `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 20 21.md` ligne ~73 → `pq-19` — *citation encore inexploitée*

- **distinction z = 4.2** — cosinus 0.569
- **source** : pdf-62 p.1 — Recherche CANLII MJA-Adelia Ferreira — trames —

**Idée non étayée :**

> La Requête de novembre 2015 a toutefois été rédigée par Me Adelia Ferreira et jurée par Élise Ayoub. L'analyse ne doit pas attribuer à Me Ayoub une instruction donnée à Me Ferreira sans preuve distincte.

**Citation disponible :**

```text
Le document est une recherche du site web CanLii qui retourne 266 résultats pour lesquels les avocate Marie-Josée Ayoub et Adélia Ferreira apparaissent ensemble
```

#### 105. `legal/allegation_stmt66_residence_2014.md` ligne ~82 → `pq-16`

- **distinction z = 4.2** — cosinus 0.571
- **source** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 20

**Idée non étayée :**

> **Le prix de vente est incompatible avec le motif allégué.** La vente s'effectue au prix de l'évaluateur indépendant, sans décote pour état dégradé - ce qui est incompatible avec un bien laissé à l'abandon par refus systématique d'entretien.

**Citation disponible :**

```text
Étude de la valeur marchande en date des présentes à des fins de partage
```

#### 106. `legal/organisation_preuve/2015_par_4_5_6.md` ligne ~284 → `pq-41` — *citation encore inexploitée*

- **distinction z = 4.2** — cosinus 0.558  
- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, pas l'identification de la pièce
- **source** : pdf-57 p.1 — Facture Pistorio 2011-05-31 — trames —

**Idée non étayée :**

> * `Event id=17`
> * `Event id=25`
> * `Event id=36`
> * `Event id=37`
> * `Event id=45`
> * `Event id=49`
> * `Event id=53`
> * `Event id=54`

**Citation disponible :**

```text
| | SÉANCE DU 03 MAI 2011 | 80,00 | 80,00 |
| | SÉANCE DU 17 MAI 2011 | 80,00 | 80,00 |
| | SÉANCE DU 24 MAI 2011 | 80,00 | 80,00 |
| | SÉANCE DU 31 MAI 2011 | 80,00 | 80,00 |
```

#### 107. `legal/expose/sections/01_par4-6_implication_parentale.md` ligne ~49 → `eq-75` — *citation encore inexploitée*

- **distinction z = 4.2** — cosinus 0.680
- **source** : email-1 — Re: Date des visites au Allez up — trames —

**Idée non étayée :**

> [XX]. Ces absences comprennent notamment celles des 7 mars, 2 mai, 25 mai, 6 juillet, 29 août, 6 septembre, 12 décembre et 16 décembre 2011, ainsi que celles des 22 mai, 4 juillet et 10 septembre 2012.

**Citation disponible :**

```text
Non! pas oublié! Les voici:

7 février 2015
16 mars 2014
16 février 2014
2 février 2014
7 décembre 2013
19 octobre 2013
31 aout 2013
26 aout 2013
18 aout 2013
7 juillet 2013
```

#### 108. `legal/demande_DEPOT_2026-07-21.md` ligne ~9 → `pq-23`

- **distinction z = 4.2** — cosinus 0.622
- **source** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> **LOUIS-PHILIPPE DAVID**, domicilié et résidant au 465, avenue Curzon, Saint-Lambert (Québec) J4P 2V6,
> &nbsp;&nbsp;&nbsp;&nbsp;*Demandeur*

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

#### 109. `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.md` ligne ~9 → `pq-23`

- **distinction z = 4.2** — cosinus 0.622
- **source** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> **LOUIS-PHILIPPE DAVID**, domicilié et résidant au 465, avenue Curzon, Saint-Lambert (Québec) J4P 2V6,
> &nbsp;&nbsp;&nbsp;&nbsp;*Demandeur*

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

#### 110. `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.md` ligne ~678 → `pq-23`

- **distinction z = 4.2** — cosinus 0.642
- **source** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> _______________________________________
> **LOUIS-PHILIPPE DAVID**
> *Demandeur, agissant en son propre nom*
> 465, avenue Curzon  
> Saint-Lambert (Québec) J4P 2V6  
> Courriel : louisphilippe.david@gmail.com

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

#### 111. `legal/demande_DEPOT_2026-07-21.md` ligne ~678 → `pq-23`

- **distinction z = 4.2** — cosinus 0.642
- **source** : pdf-11 p.1 — Étude de la valeur marchande à des fins de partage — trames 33

**Idée non étayée :**

> _______________________________________
> **LOUIS-PHILIPPE DAVID**
> *Demandeur, agissant en son propre nom*
> 465, avenue Curzon  
> Saint-Lambert (Québec) J4P 2V6  
> Courriel : louisphilippe.david@gmail.com

**Citation disponible :**

```text
Requérant(e): Monsieur Louis-Philippe David
Lieux: 245, avenue Macaulay Saint-Lambert, Qc
Fins du rapport: Étude de la valeur marchande en date des présentes à des fins de partage.
Mandat en date du: 27 juin 2013
```

#### 112. `legal/expose_faits_volet_2015.md` ligne ~69 → `eq-40`

- **distinction z = 4.1** — cosinus 0.716
- **source** : email-100 — Re: Alexia — trames 5, 64

**Idée non étayée :**

> 25-A. Les communications contemporaines identifient les mardis et mercredis comme soirs de danse dans les sessions encadrant l'année 2011, et les communications entre le demandeur et sa mère montrent que les visites de celle-ci étaient organisées lorsque la défenderesse était absente pour la danse.

**Citation disponible :**

```text
 mais je t'ai deja dit que les mardi et mercredi elise dansait.
```

#### 113. `legal/faits_substitution_premeditee_2013-2015.md` ligne ~54 → `pq-74`

- **distinction z = 4.1** — cosinus 0.726
- **source** : pdf-13 p.2 — Jugement sur le fond (perte emplois) — trames 62

**Idée non étayée :**

> 17. Le 14 janvier 2016, le jugement est rendu, le défendeur étant **absent**, et confie la garde à la demanderesse avec des accès au défendeur le dimanche de 16 h à 20 h (source : Jugement_1.pdf ; [faits_par3_2019.md](faits/faits_par3_2019.md) faits 34-35).

**Citation disponible :**

```text
10h13:11 Témoignage de M. David – Questions du Tribunal.
Objection de Me Ayoub (un jugement a été prononcé en 2016 sur ces sujets) ;
Le Tribunal prend connaissance du jugement de 2016 ;

10h17:04 Le Tribunal informe Monsieur de ne pas parler de ce qui s'est passé avant 2016.
Suite du témoignage de M. David
```

#### 114. `legal/piece_pdf-70.md` ligne ~9 → `eq-134`

- **distinction z = 4.1** — cosinus 0.641
- **source** : email-3 — emplois — trames 62

**Idée non étayée :**

> - **Employeur** : Allianz Technology SE München, Succursale de **Bucarest** (Reg. Comm. J40/2673/2014 ; TVA RO31824525), représentée par Mme Ionescu Alina-Mihaela, directrice de succursale.
> - **Employé** : **Louis-Philippe David**, domicilié à Saint-Lambert (54, rue Reid), passeport canadien.
> - **Lieu de travail** : siège d'Allianz à **Bucarest** (Floreasca Park, Șoseaua Pipera nr. 43) et/ou adresse déclarée de l'employé sur demande écrite.
> - **Poste** : permanent.

**Citation disponible :**

```text
Bonjour,

Le 1er juillet je vais avoir une conférence téléphonique avec Allianz, la
compagnie d'assurance avec laquelle j'ai une offre d'emplois à Bucarest.

Pour l'instant, comme tu le sais, mon passeport est suspendu et si rien ne
change je serai dans l'obligation de refuser leur offre.

Je t'invite à reconsidérer ta position dans dans cette situation, il s'agit
d'un bon travail en actuariat qui me permettra de reprendre de la valeur
sur le marché du travail au Canada. En terme de flux monétaires futur,
c'est la meilleur option pour les enfants,
```

#### 115. `legal/expose_faits_volet_2015.md` ligne ~161 → `eq-75` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.632
- **source** : email-1 — Re: Date des visites au Allez up — trames —

**Idée non étayée :**

> 66. Entre le 27 juin et le 31 août 2013, le demandeur a fait de l'escalade avec Alexia à au moins cinq (5) reprises, soit les 27 juin, 7 juillet, 18, 26 et 31 août (liasse escalade, fait 20).

**Citation disponible :**

```text
Non! pas oublié! Les voici:

7 février 2015
16 mars 2014
16 février 2014
2 février 2014
7 décembre 2013
19 octobre 2013
31 aout 2013
26 aout 2013
18 aout 2013
7 juillet 2013
```

#### 116. `legal/demande_DEPOT_2026-07-21.md` ligne ~9 → `eq-170` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.618
- **source** : email-355 — Reçu pour votre transaction Ludik — trames —

**Idée non étayée :**

> **LOUIS-PHILIPPE DAVID**, domicilié et résidant au 465, avenue Curzon, Saint-Lambert (Québec) J4P 2V6,
> &nbsp;&nbsp;&nbsp;&nbsp;*Demandeur*

**Citation disponible :**

```text
Direction Loisirs, culture et vie communautaire
600, avenue Oak, Saint-Lambert
```

#### 117. `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.md` ligne ~9 → `eq-170` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.618
- **source** : email-355 — Reçu pour votre transaction Ludik — trames —

**Idée non étayée :**

> **LOUIS-PHILIPPE DAVID**, domicilié et résidant au 465, avenue Curzon, Saint-Lambert (Québec) J4P 2V6,
> &nbsp;&nbsp;&nbsp;&nbsp;*Demandeur*

**Citation disponible :**

```text
Direction Loisirs, culture et vie communautaire
600, avenue Oak, Saint-Lambert
```

#### 118. `legal/memoire faille structurelle.md` ligne ~190 → `pq-68`

- **distinction z = 4.1** — cosinus 0.680
- **source** : pdf-1 p.1 — Courriel suggérant de faire une plainte pour violence conjug — trames 62

**Idée non étayée :**

> La procédure d'urgence sans témoins - conçue pour protéger rapidement un enfant en danger réel - ne contient aucun mécanisme de vérification préalable de la sincérité des allégations. Ce vide est fonctionnel : la vérification prendrait du temps, et le danger ne peut pas attendre.

**Citation disponible :**

```text
En urgence on appelle cela une ordonnance de sauvegarde. Lors de cette procédure d'urgence le juge en question n'entend pas de témoin c'est seulement les avocats qui plaident. C'est rapide et urgent
```

#### 119. `legal/piece_vacances_2013_cape_cod_cuba_chalet.md` ligne ~35 → `eq-71`

- **distinction z = 4.1** — cosinus 0.683
- **source** : email-78 — (sans objet) — trames 44, 62

**Idée non étayée :**

> 2. Élise souhaitait emmener les enfants à **Cuba**. LP a dans un premier temps **refusé de signer les papiers** permettant aux enfants de quitter le pays.

**Citation disponible :**

```text
Elise veut partir a Cuba au mois de fevrier avec la petite, peut elle faire
ca?
```

#### 120. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~791 → `eq-164` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.624
- **source** : email-130 — Re: Consultation — trames —

**Idée non étayée :**

> 306. Le 21 avril 2015, soit le lendemain de la transmission de cette position officielle, la défenderesse Élise Ayoub a transféré à Me Marie-Josée Ayoub les messages du 7 avril sous l'objet :

**Citation disponible :**

```text
Elise Marie Ayoub, je vous donnes une reponse demain.
```

#### 121. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~791 → `eq-164` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.624
- **source** : email-130 — Re: Consultation — trames —

**Idée non étayée :**

> 306. Le 21 avril 2015, soit le lendemain de la transmission de cette position officielle, la défenderesse Élise Ayoub a transféré à Me Marie-Josée Ayoub les messages du 7 avril sous l'objet :

**Citation disponible :**

```text
Elise Marie Ayoub, je vous donnes une reponse demain.
```

#### 122. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~791 → `eq-164` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.624
- **source** : email-130 — Re: Consultation — trames —

**Idée non étayée :**

> 306. Le 21 avril 2015, soit le lendemain de la transmission de cette position officielle, la défenderesse Élise Ayoub a transféré à Me Marie-Josée Ayoub les messages du 7 avril sous l'objet :

**Citation disponible :**

```text
Elise Marie Ayoub, je vous donnes une reponse demain.
```

#### 123. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~791 → `eq-164` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.624
- **source** : email-130 — Re: Consultation — trames —

**Idée non étayée :**

> 306. Le 21 avril 2015, soit le lendemain de la transmission de cette position officielle, la défenderesse Élise Ayoub a transféré à Me Marie-Josée Ayoub les messages du 7 avril sous l'objet :

**Citation disponible :**

```text
Elise Marie Ayoub, je vous donnes une reponse demain.
```

#### 124. `legal/requete_secton_faits_lp.md` ligne ~887 → `eq-164` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.624
- **source** : email-130 — Re: Consultation — trames —

**Idée non étayée :**

> 306. Le 21 avril 2015, soit le lendemain de la transmission de cette position officielle, la défenderesse Élise Ayoub a transféré à Me Marie-Josée Ayoub les messages du 7 avril sous l'objet :

**Citation disponible :**

```text
Elise Marie Ayoub, je vous donnes une reponse demain.
```

#### 125. `legal/allegation_stmt56_57_58_assurances.md` ligne ~115 → `pq-102`

- **distinction z = 4.1** — cosinus 0.827
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 2. **Intervalle « nouvel avis → audition » (7 janv. 2016 → 14 janv. 2016) :** la transaction (P) du **11 janvier 2016** y tombe - soit 4 jours après la re-signification au défendeur et 3 jours avant l'audition au cours de laquelle la demanderesse maintient sous serment que le défendeur refuse l'accès aux assurances.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 126. `legal/demande_introductive_instance.md` ligne ~304 → `eq-142`

- **distinction z = 4.1** — cosinus 0.723
- **source** : email-410 — Re: Vacation à la cour — trames 62

**Idée non étayée :**

> 26. **La faute est continue.** Le demandeur perd son emploi en juin 2018. La pension alimentaire n'a **jamais** été ajustée pour refléter sa capacité réelle de payer - ni alors, ni depuis. Le maintien de cette dissociation, et des arrérages qui en découlent, constitue une **faute continue** (§ III, palier 2 ; voir § IX).

**Citation disponible :**

```text
la pension alimentaire ne sera pas modifiée à ce stade-ci.  Nous avons procédé à des représentations aux stades intérimaires et malgré tes demandes de réduction et/ou de suspension de la pension, la juge a décidé que tu devais payer la pension même si tu n’avais pas d’emploi, vu entre autre tes économies et les besoins des enfants.
```

#### 127. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~707 → `pq-102`

- **distinction z = 4.1** — cosinus 0.647
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 278. Une autre transaction a été traitée le 15 décembre 2015, soit après la production de la requête, et une transaction subséquente a été traitée le 11 janvier 2016, soit peu avant l'audition du 14 janvier 2016.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 128. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~707 → `pq-102`

- **distinction z = 4.1** — cosinus 0.647
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 278. Une autre transaction a été traitée le 15 décembre 2015, soit après la production de la requête, et une transaction subséquente a été traitée le 11 janvier 2016, soit peu avant l'audition du 14 janvier 2016.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 129. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~707 → `pq-102`

- **distinction z = 4.1** — cosinus 0.647
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 278. Une autre transaction a été traitée le 15 décembre 2015, soit après la production de la requête, et une transaction subséquente a été traitée le 11 janvier 2016, soit peu avant l'audition du 14 janvier 2016.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 130. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~707 → `pq-102`

- **distinction z = 4.1** — cosinus 0.647
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 278. Une autre transaction a été traitée le 15 décembre 2015, soit après la production de la requête, et une transaction subséquente a été traitée le 11 janvier 2016, soit peu avant l'audition du 14 janvier 2016.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 131. `legal/requete_secton_faits_lp.md` ligne ~803 → `pq-102`

- **distinction z = 4.1** — cosinus 0.647
- **source** : pdf-64 p.1 — relevé assurance 2016 — trames 68

**Idée non étayée :**

> 278. Une autre transaction a été traitée le 15 décembre 2015, soit après la production de la requête, et une transaction subséquente a été traitée le 11 janvier 2016, soit peu avant l'audition du 14 janvier 2016.

**Citation disponible :**

```text
Transaction du 11 janvier 2016 (type P — Paiement Direct au Fournisseur) : réclamation soumise au point de service lors d'un rendez-vous tenu pendant la période de garde de la demanderesse, trois jours avant l'audition du 14 janvier 2016 au cours de laquelle l'allégation de refus d'accès aux assurances a été maintenue.
```

#### 132. `legal/piece_document-1.md` ligne ~130 → `pq-32`

- **distinction z = 4.1** — cosinus 0.708
- **source** : pdf-5 p.4 — 20150813 MJ projet consentement — trames 48, 49, 50, 55

**Idée non étayée :**

> **§49** - Le défendeur a versé une pension alimentaire pour les enfants de 425.00$ par deux semaines après la réparation, ce qui avait été augmenté à 443.00$ par deux semaines à compter d'octobre 2015.

**Citation disponible :**

```text
Si le père ne désire pas exercer ses droits d’accès prévus audit consentement auprès des enfants sur une base régulière, la pensionv alimentaire pour enfants sera majoré de 20% à raison de 465.41$ aux deux semaines;
```

#### 133. `legal/piece_pdf-84.md` ligne ~9 → `eq-134`

- **distinction z = 4.1** — cosinus 0.643
- **source** : email-3 — emplois — trames 62

**Idée non étayée :**

> - **Requérante principale : SILVIA FLORENTINA BALAN** (conjointe du défendeur), née le **30 août 1986**, Medgidia, **Roumanie** ; citoyenne roumaine ; passeport roumain 050578518.
> - **Date du dépôt : 2016-06-13.** N° de demande : **D0000001500**.
> - **Programme : régulier des travailleurs qualifiés.** Région d'établissement visée : **Montréal**.
> - Formation : maîtrise (gestion et communication d'entreprise), licence (communication / relations publiques) ; IELTS 2015.
> - Emploi : Parc Hôtel Roumanie (relations publiques) à Bucarest.
> - Famille au Québec : sœur (Balan Elena-Ligia, Saint-Hubert). Numéro d'identification CIC : 30007083.

**Citation disponible :**

```text
Bonjour,

Le 1er juillet je vais avoir une conférence téléphonique avec Allianz, la
compagnie d'assurance avec laquelle j'ai une offre d'emplois à Bucarest.

Pour l'instant, comme tu le sais, mon passeport est suspendu et si rien ne
change je serai dans l'obligation de refuser leur offre.

Je t'invite à reconsidérer ta position dans dans cette situation, il s'agit
d'un bon travail en actuariat qui me permettra de reprendre de la valeur
sur le marché du travail au Canada. En terme de flux monétaires futur,
c'est la meilleur option pour les enfants,
```

#### 134. `legal/piece_declaration_revenus_elise_2018.md` ligne ~22 → `pq-81`

- **distinction z = 4.1** — cosinus 0.663
- **source** : pdf-30 p.1 — Avis de cotisation 2019 — trames 62

**Idée non étayée :**

> La déclaration indique une déduction pour travailleur de **1 150 $** (ligne 201), une cotisation à un régime de pension agréé de **12 118,29 $** (ligne 205) et une déduction pour REER ou RPAC/RVER de **29 $** (ligne 214), pour un total de **13 297,29 $** (ligne 254). Le montant de 1 638 $ visible dans la case « RAP ou REEP » ne constitue pas l'une des déductions additionnées à la ligne 254.

**Citation disponible :**

```text
Revenus Net : 41788,58
Prestations d'assurance emploi : 8752.00
Retrait REER : 37991.58
```

#### 135. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~45 → `eq-75` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.670
- **source** : email-1 — Re: Date des visites au Allez up — trames —

**Idée non étayée :**

> 16. Ces absences comprennent notamment celles des 7 mars, 2 mai, 25 mai, 6 juillet, 29 août, 6 septembre, 12 décembre et 16 décembre 2011, ainsi que celles des 22 mai, 4 juillet et 10 septembre 2012.

**Citation disponible :**

```text
Non! pas oublié! Les voici:

7 février 2015
16 mars 2014
16 février 2014
2 février 2014
7 décembre 2013
19 octobre 2013
31 aout 2013
26 aout 2013
18 aout 2013
7 juillet 2013
```

#### 136. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~45 → `eq-75` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.670
- **source** : email-1 — Re: Date des visites au Allez up — trames —

**Idée non étayée :**

> 16. Ces absences comprennent notamment celles des 7 mars, 2 mai, 25 mai, 6 juillet, 29 août, 6 septembre, 12 décembre et 16 décembre 2011, ainsi que celles des 22 mai, 4 juillet et 10 septembre 2012.

**Citation disponible :**

```text
Non! pas oublié! Les voici:

7 février 2015
16 mars 2014
16 février 2014
2 février 2014
7 décembre 2013
19 octobre 2013
31 aout 2013
26 aout 2013
18 aout 2013
7 juillet 2013
```

#### 137. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~45 → `eq-75` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.670
- **source** : email-1 — Re: Date des visites au Allez up — trames —

**Idée non étayée :**

> 16. Ces absences comprennent notamment celles des 7 mars, 2 mai, 25 mai, 6 juillet, 29 août, 6 septembre, 12 décembre et 16 décembre 2011, ainsi que celles des 22 mai, 4 juillet et 10 septembre 2012.

**Citation disponible :**

```text
Non! pas oublié! Les voici:

7 février 2015
16 mars 2014
16 février 2014
2 février 2014
7 décembre 2013
19 octobre 2013
31 aout 2013
26 aout 2013
18 aout 2013
7 juillet 2013
```

#### 138. `legal/requete_secton_faits_lp.md` ligne ~55 → `eq-75` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.670
- **source** : email-1 — Re: Date des visites au Allez up — trames —

**Idée non étayée :**

> 16. Ces absences comprennent notamment celles des 7 mars, 2 mai, 25 mai, 6 juillet, 29 août, 6 septembre, 12 décembre et 16 décembre 2011, ainsi que celles des 22 mai, 4 juillet et 10 septembre 2012.

**Citation disponible :**

```text
Non! pas oublié! Les voici:

7 février 2015
16 mars 2014
16 février 2014
2 février 2014
7 décembre 2013
19 octobre 2013
31 aout 2013
26 aout 2013
18 aout 2013
7 juillet 2013
```

#### 139. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~45 → `eq-75` — *citation encore inexploitée*

- **distinction z = 4.1** — cosinus 0.670
- **source** : email-1 — Re: Date des visites au Allez up — trames —

**Idée non étayée :**

> 16. Ces absences comprennent notamment celles des 7 mars, 2 mai, 25 mai, 6 juillet, 29 août, 6 septembre, 12 décembre et 16 décembre 2011, ainsi que celles des 22 mai, 4 juillet et 10 septembre 2012.

**Citation disponible :**

```text
Non! pas oublié! Les voici:

7 février 2015
16 mars 2014
16 février 2014
2 février 2014
7 décembre 2013
19 octobre 2013
31 aout 2013
26 aout 2013
18 aout 2013
7 juillet 2013
```

#### 140. `legal/requete_secton_faits_lp.backup_2026-07-12_161812_avant_lot_contextuel_1.md` ligne ~1060 → `pq-74`

- **distinction z = 4.1** — cosinus 0.610
- **source** : pdf-13 p.2 — Jugement sur le fond (perte emplois) — trames 62

**Idée non étayée :**

> 415. La preuve du demandeur, qui se représentait seul à cette audience, était close depuis 10 h 29, tel qu'il appert de la même pièce.

**Citation disponible :**

```text
10h13:11 Témoignage de M. David – Questions du Tribunal.
Objection de Me Ayoub (un jugement a été prononcé en 2016 sur ces sujets) ;
Le Tribunal prend connaissance du jugement de 2016 ;

10h17:04 Le Tribunal informe Monsieur de ne pas parler de ce qui s'est passé avant 2016.
Suite du témoignage de M. David
```

#### 141. `legal/requete_secton_faits_lp.md` ligne ~1237 → `pq-74`

- **distinction z = 4.1** — cosinus 0.610
- **source** : pdf-13 p.2 — Jugement sur le fond (perte emplois) — trames 62

**Idée non étayée :**

> 415. La preuve du demandeur, qui se représentait seul à cette audience, était close depuis 10 h 29, tel qu'il appert de la même pièce.

**Citation disponible :**

```text
10h13:11 Témoignage de M. David – Questions du Tribunal.
Objection de Me Ayoub (un jugement a été prononcé en 2016 sur ces sujets) ;
Le Tribunal prend connaissance du jugement de 2016 ;

10h17:04 Le Tribunal informe Monsieur de ne pas parler de ce qui s'est passé avant 2016.
Suite du témoignage de M. David
```

#### 142. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~1060 → `pq-74`

- **distinction z = 4.1** — cosinus 0.610
- **source** : pdf-13 p.2 — Jugement sur le fond (perte emplois) — trames 62

**Idée non étayée :**

> 415. La preuve du demandeur, qui se représentait seul à cette audience, était close depuis 10 h 29, tel qu'il appert de la même pièce.

**Citation disponible :**

```text
10h13:11 Témoignage de M. David – Questions du Tribunal.
Objection de Me Ayoub (un jugement a été prononcé en 2016 sur ces sujets) ;
Le Tribunal prend connaissance du jugement de 2016 ;

10h17:04 Le Tribunal informe Monsieur de ne pas parler de ce qui s'est passé avant 2016.
Suite du témoignage de M. David
```

#### 143. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~1060 → `pq-74`

- **distinction z = 4.1** — cosinus 0.610
- **source** : pdf-13 p.2 — Jugement sur le fond (perte emplois) — trames 62

**Idée non étayée :**

> 415. La preuve du demandeur, qui se représentait seul à cette audience, était close depuis 10 h 29, tel qu'il appert de la même pièce.

**Citation disponible :**

```text
10h13:11 Témoignage de M. David – Questions du Tribunal.
Objection de Me Ayoub (un jugement a été prononcé en 2016 sur ces sujets) ;
Le Tribunal prend connaissance du jugement de 2016 ;

10h17:04 Le Tribunal informe Monsieur de ne pas parler de ce qui s'est passé avant 2016.
Suite du témoignage de M. David
```

#### 144. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~1060 → `pq-74`

- **distinction z = 4.1** — cosinus 0.610
- **source** : pdf-13 p.2 — Jugement sur le fond (perte emplois) — trames 62

**Idée non étayée :**

> 415. La preuve du demandeur, qui se représentait seul à cette audience, était close depuis 10 h 29, tel qu'il appert de la même pièce.

**Citation disponible :**

```text
10h13:11 Témoignage de M. David – Questions du Tribunal.
Objection de Me Ayoub (un jugement a été prononcé en 2016 sur ces sujets) ;
Le Tribunal prend connaissance du jugement de 2016 ;

10h17:04 Le Tribunal informe Monsieur de ne pas parler de ce qui s'est passé avant 2016.
Suite du témoignage de M. David
```

#### 145. `legal/dossier_plaidoirie/01_arc_garde_2013-2016.md` ligne ~1364 → `pq-27`

- **distinction z = 4.1** — cosinus 0.643
- **source** : pdf-3 p.2 — Réponse à l'offre de garde partagée — trames 34, 39, 42, 49, 71, 72, 73, 76

**Idée non étayée :**

> **La réponse est dans le silence de la lettre :** elle **ne précise pas** quelle
> composante de la routine devait être préservée, ni pourquoi les transitions
> qu'elle propose sont compatibles avec le jeune âge alors que celles d'un horaire
> 2‐2‐3 ne le seraient pas. Aucune comparaison n'y est faite, et aucun critère de
> progression n'y est posé.

**Citation disponible :**

```text
nous considérons qu'il y a contre-indication à l'établissement de la garde parlagée des deux (2) enfants mineurs vu leur jeune âge et qu'il n'est pas dans leur intérêt de modifier une routine établie depuis plus deux mois.
```

#### 146. `legal/demande_DEPOT_2026-07-21.md` ligne ~489 → `pq-78`

- **distinction z = 4.1** — cosinus 0.685
- **source** : pdf-66 p.1 — Revenus représentant au service à la clientèle — trames 62

**Idée non étayée :**

> 184. Pour évaluer la perte alléguée au Régime de rentes du Québec de 2019 à 2025, le demandeur suppose qu'il aurait gagné chaque année au moins le maximum des gains admissibles et, en 2024 et 2025, le maximum supplémentaire. Selon les tables annuelles publiées par Revenu Québec et Retraite Québec, les cotisations salariales maximales sous le premier plafond étaient respectivement de 2 991,45 $, 3 146,40 $, 3 427,90 $, 3 776,10 $, 4 038,40 $, 4 160 $ et 4 339,20 $, soit 25 879,45 $.

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION Représentant/représentante au service à la clientèle - services financiers au Québec Date de modification : 2024-01-23
Région de Montréal Salaire Bas : 16,28 Median 21,00 Haut : 26,99 
https://www.guichet-emplois.gc.ca/salaire-horaire/representant-representante-service-clientele-services-financiers/montreal
```

#### 147. `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.md` ligne ~489 → `pq-78`

- **distinction z = 4.1** — cosinus 0.685
- **source** : pdf-66 p.1 — Revenus représentant au service à la clientèle — trames 62

**Idée non étayée :**

> 184. Pour évaluer la perte alléguée au Régime de rentes du Québec de 2019 à 2025, le demandeur suppose qu'il aurait gagné chaque année au moins le maximum des gains admissibles et, en 2024 et 2025, le maximum supplémentaire. Selon les tables annuelles publiées par Revenu Québec et Retraite Québec, les cotisations salariales maximales sous le premier plafond étaient respectivement de 2 991,45 $, 3 146,40 $, 3 427,90 $, 3 776,10 $, 4 038,40 $, 4 160 $ et 4 339,20 $, soit 25 879,45 $.

**Citation disponible :**

```text
Gouvernement du Canada, Guichet-Emplois, RÉMUNÉRATION Représentant/représentante au service à la clientèle - services financiers au Québec Date de modification : 2024-01-23
Région de Montréal Salaire Bas : 16,28 Median 21,00 Haut : 26,99 
https://www.guichet-emplois.gc.ca/salaire-horaire/representant-representante-service-clientele-services-financiers/montreal
```

#### 148. `legal/requete_secton_faits_lp.backup_2026-07-12_163110_avant_p43.md` ligne ~1050 → `pq-81`

- **distinction z = 4.1** — cosinus 0.591
- **source** : pdf-30 p.1 — Avis de cotisation 2019 — trames 62

**Idée non étayée :**

> 411. Le revenu déclaré du demandeur pour l'année 2019 était de 46 743,58 $, et son revenu d'emploi pour l'année 2018 était de 47 520,51 $, tel qu'il appert des pièces P-[●] et P-[●].

**Citation disponible :**

```text
Revenus Net : 41788,58
Prestations d'assurance emploi : 8752.00
Retrait REER : 37991.58
```

#### 149. `legal/requete_secton_faits_lp.backup_2026-07-12_164022_avant_integration_finale.md` ligne ~1050 → `pq-81`

- **distinction z = 4.1** — cosinus 0.591
- **source** : pdf-30 p.1 — Avis de cotisation 2019 — trames 62

**Idée non étayée :**

> 411. Le revenu déclaré du demandeur pour l'année 2019 était de 46 743,58 $, et son revenu d'emploi pour l'année 2018 était de 47 520,51 $, tel qu'il appert des pièces P-[●] et P-[●].

**Citation disponible :**

```text
Revenus Net : 41788,58
Prestations d'assurance emploi : 8752.00
Retrait REER : 37991.58
```

#### 150. `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` ligne ~1050 → `pq-81`

- **distinction z = 4.1** — cosinus 0.591
- **source** : pdf-30 p.1 — Avis de cotisation 2019 — trames 62

**Idée non étayée :**

> 411. Le revenu déclaré du demandeur pour l'année 2019 était de 46 743,58 $, et son revenu d'emploi pour l'année 2018 était de 47 520,51 $, tel qu'il appert des pièces P-[●] et P-[●].

**Citation disponible :**

```text
Revenus Net : 41788,58
Prestations d'assurance emploi : 8752.00
Retrait REER : 37991.58
```
