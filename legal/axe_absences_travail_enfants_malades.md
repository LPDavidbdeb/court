# Axe argumentatif — Absences au travail pour soins aux enfants malades (2011–2016)

**Portée :** Cet axe est applicable aux allégations contestant l'implication historique du père dans les soins quotidiens des enfants (Doc id=1, stmts 9, 19, 20 et autres). Il couvre la période 2011–2016, avec une densité maximale en 2011–2012.

**Sous-périodes de référence :**
- **(B) Fév. 2011 – fév. 2012** : **8 adaptations professionnelles distinctes** (7 mars, 2 mai, 25 mai, 6 juillet, 29 août, 6 septembre, 12 décembre et 16 décembre 2011), auxquelles s'ajoute le suivi médical du 3 mai (id=118), qui n'est pas une absence additionnelle. Cette sous-période comprend la résidence distincte jusqu'au 29 mai 2011, puis la période suivant la fin du logement distinct.
- **(C) Été 2013** : **1 absence documentée** (id=40, 2013-06-03) — *"je vais rester à la maison pour aider ma conjointe avec le bébé, elle ne se sent pas très bien et ma belle-mère n'est pas disponible"* — Nicolas a ~3 mois

**Thèse :** Sur une période de cinq ans, le corpus documente **18 adaptations professionnelles distinctes** reliées aux soins des enfants, à des rendez-vous médicaux ou à un besoin familial imprévu. **Seize** surviennent pendant la cohabitation et **deux** après la séparation. Le suivi médical du 3 mai 2011 (id=118) constitue une **preuve qualitative additionnelle de responsabilité médicale** : il ne s'agit pas d'une seconde absence, puisqu'il prolonge l'épisode du 2 mai, mais il documente la connaissance du traitement, l'inquiétude exprimée par LP et son suivi de la seconde consultation. Le message du 8 février 2013 (id=41), envoyé un vendredi matin à un supérieur, annonce un retour au travail le lundi : il établit donc une absence ce vendredi, même s'il ne permet pas de déterminer quand elle a commencé. Les communications sont adressées directement aux supérieurs de LP à la Banque Nationale du Canada et constituent des communications professionnelles contemporaines adressées à des tiers extérieurs au conflit parental.

**Précision sur la portée de l'argument :** chacune des **18 adaptations professionnelles** documente une instance où le demandeur a modifié ses obligations de travail en lien avec un besoin des enfants ou une situation familiale de soins. Le suivi médical du 3 mai ajoute une preuve de responsabilité parentale, sans ajouter une journée au décompte des absences. **Cet axe n'affirme pas que le demandeur était l'unique parent à prodiguer des soins de santé aux enfants sur l'ensemble de la période.** Il est probable, et non contesté, que la défenderesse ait elle aussi assuré de tels soins à d'autres moments non documentés ici. La présence ou l'absence de la défenderesse doit être affirmée uniquement lorsqu'elle ressort du courriel concerné.

---

## Inventaire complet des pièces — reconstituable en session froide

> **Requête DB :** `Email.objects.filter(id__in=[15, 21, 27, 28, 30, 40, 41, 42, 45, 47, 51, 53, 55, 56, 58, 59, 61, 64, 68, 69, 118, 488]).order_by('date_sent')`

| # | Date | Type | PK | Destinataire | Passage pertinent |
|---|------|------|----|--------------|-------------------|
| 1 | 2011-03-07 | Email | **69** | Catherine Liepins (patron BNC) | *"je dois rester avec ma petite aujourd'hui. J'imagine qu'il y a des journées prévues pour ça à la banque. Sinon je vais prendre une journée de congé."* |
| 2 | 2011-03-07 | Email | **68** | Liepins | *"La gardienne ne pouvait pas se déplacer… elle n'a pas de place en garderie"* — la gardienne est indisponible et Alexia n'a pas de place en garderie |
| 3 | 2011-05-02 | Email | **64** | Liepins | *"i have to stay with my daughter. She is sick and must go to the doctor."* |
| 4 | 2011-05-03 | Email | **118** | Liepins | *"my girlfriend went to see another doctor today and it turns out i was right"* — LP avait jugé le premier diagnostic inadéquat; un second médecin a confirmé son appréciation |
| 5 | 2011-05-25 | Email | **61** | Liepins | *"demain je dois aller chez le pédiatre pour les vaccins de ma fille. On doit la remettre à vendredi"* — LP accompagne Alexia au pédiatre pour les vaccins |
| 6 | 2011-07-06 | Email | **59** | Liepins + Tessier | *"j'ai essayé de convaincre ma copine que tu avais plus besoin de moi que ma fille mais en vain — je resterai donc à la maison avec elle"* |
| 7 | 2011-07-06 | Email | **58** | Réponse Liepins | *"J'espère qu'elle aille mieux. Je reporterai la rencontre PnL."* — supérieure reporte une réunion de performance pour accommoder l'absence |
| 8 | 2011-08-29 | Email | **56** | Liepins | *"je dois rester avec ma fille cet avant-midi — je rentrerai au travail cet après-midi"* — demi-journée |
| 9 | 2011-09-06 | Email | **55** | Liepins | *"I have to stay home today with my daughter because she is sick. I will be reachable all day at my house number 450-550-2998"* |
| 10 | 2011-12-12 | Email | **53/488** | Liepins | *"my daughter is sick and I'll be staying at home today with her"* |
| 11 | 2011-12-16 | Email | **51** | Liepins | *"i have to stay home again today — my mother in law can't come in"* — la mère d'Élise est indisponible, LP reste à la maison |
| 12 | 2012-05-22 | Email | **47** | Tessier + Liepins | *"Je reste à la maison avec ma fille aujourd'hui"* |
| 13 | 2012-07-04 | Email | **45** | Tessier | *"ma fille a la gastro je dois rester à la maison — je serai disponible au 450 550 2998"* |
| 14 | 2012-09-10 | Email | **42** | Karl Grimmel (patron BNC) | *"je vais rester à la maison avec ma petite qui est malade et qui ne dort pas"* |
| 15 | 2013-02-08 | Email | **41** | Grimmel | *"je vais etre au travail lundi [...] nous ne dormons que quelques heures par nuit depuis une semaine et je suis épuisé. Non seulement le bébé ne dort pas, mais ma plus vieille fait de même."* — envoyé le vendredi matin, ce message établit l'absence du vendredi et le retour prévu le lundi |
| 16 | 2013-06-03 | Email | **40** | Grimmel | *"je vais rester à la maison pour aider ma conjointe avec le bébé, elle ne se sent pas très bien et ma belle-mère n'est pas disponible"* |
| 17 | 2014-05-05 | Email | **30** | Grimmel | *"je vais à la clinique ce matin avec mon gars — en fonction de ce qu'ils me disent, je vais rester ici ou rentrer travailler"* — Nicolas, 2014 |
| 18 | 2014-12-16 | Email | **28** | Grimmel | *"je vais manquer le CMOC et le dîner d'équipe, mais je suis malade et en plus je dois m'occuper de mon gars"* — billet médical joint |
| 19 | 2014-12-19 | Email | **27** | Grimmel | *"Aucun des enfants ni moi avons dormi la nuit dernière — c'est au tour de ma fille d'être malade. Je serai au bureau lundi. **Élise ma conjointe va prendre la relève** si nécessaire"* |
| 20 | 2015-08-03 | Email | **21** | Grimmel | *"Nicolas est malade je reste à la maison"* |
| 21 | 2016-02-10 | Email | **15** | Grimmel | *"demain je vais rester à la maison pour m'occuper de Nicolas et possiblement vendredi"* |

---

## Principe de l'argument

### 1. Nature et valeur probatoire des documents

Ces 22 courriels, regroupés en 19 occurrences datées, présentent des caractéristiques qui en font des preuves de **haute valeur probatoire** :

**A. Communications à des tiers sans lien avec le litige**

Les destinataires — Catherine Liepins et Karl Grimmel, supérieurs hiérarchiques de LP à la Banque Nationale — sont extérieurs au conflit parental. Ce sont des communications professionnelles ordinaires et contemporaines : elles n'ont pas été rédigées rétrospectivement pour reconstituer la période. Leur contenu demeure néanmoins soumis à l'appréciation de la crédibilité, comme toute déclaration de son auteur.

**B. Documents produits sans anticipation d'un contexte judiciaire**

Il s'agit de communications produites au moment où LP devait informer son employeur de sa présence ou de son absence. Elles sont particulièrement probantes quant à l'adaptation professionnelle annoncée ou exécutée. Les courriels de 2011 à 2014 précèdent la requête de novembre 2015; les deux faits postérieurs à la séparation doivent être utilisés seulement pour établir la continuité.

**C. Les absences ont des conséquences professionnelles réelles**

Email id=58 : la supérieure de LP reporte une réunion PnL (*"Je reporterai la rencontre PnL"*) pour accommoder son absence. Email id=28 : LP annonce qu'il manquera un *CMOC* et un dîner d'équipe. Ces conséquences corroborent que certaines adaptations ont effectivement affecté l'organisation professionnelle.

---

### 2. Chronologie — densité et continuité

| Période | Absences documentées | Enfant(s) |
|---------|---------------------|-----------|
| Mars–septembre 2011 | 6 adaptations distinctes, dont 1 demi-journée; suivi médical additionnel le 3 mai | Alexia |
| Décembre 2011 | 2 absences consécutives (12 et 16 déc.) | Alexia |
| Mai–septembre 2012 | 3 absences | Alexia |
| Février–juin 2013 | 2 absences : 8 février et 3 juin | Nicolas (bébé) + Alexia |
| Mai–décembre 2014 | 3 absences | Nicolas + Alexia |
| Août 2015 | 1 absence | Nicolas |
| Février 2016 | 1 absence (+ possiblement vendredi) | Nicolas |

**Couverture temporelle :** de mars 2011 à février 2016. Les adaptations concernent d'abord Alexia seule (2011–2012), puis les deux enfants à partir de 2013.

---

### 3. Pièces particulièrement probantes

**Email id=118 (2011-05-03) — implication dans les décisions médicales**

> *"my girlfriend went to see another doctor today and it turns out i was right"*

LP n'a pas seulement assuré la présence physique lors de la maladie d'Alexia : il écrit avoir jugé inadéquat le traitement prescrit par le premier médecin. Élise a ensuite consulté un second médecin et, selon le compte rendu fait par LP à sa supérieure, cette seconde consultation a confirmé son appréciation. Ce passage documente sa connaissance et sa participation au suivi médical; il n'établit ni qu'il a décidé seul de la seconde consultation ni la justesse médicale objective de son opinion.

**Email id=27 (2014-12-19) — coordination LP↔Élise explicite**

> *"Je serai au bureau lundi. Élise ma conjointe va prendre la relève si nécessaire"*

Ce passage confirme explicitement le système de coordination entre les deux parents pour les soins des enfants malades : LP assure les soins jusqu'à son retour au bureau, puis Élise prend le relais. Les deux parents sont co-responsables — ni l'un ni l'autre n'assume seul cette responsabilité.

**Email id=51 (2011-12-16) — réseau de soutien et LP comme parent de dernier recours**

> *"i have to stay home again today — my mother in law can't come in"*

LP reste à la maison parce que **la belle-mère d'Élise** n'est pas disponible. Cette occurrence documente qu'en l'absence de cette ressource familiale, LP adapte son travail et demeure au domicile. Elle ne suffit pas à le qualifier de « dernier recours » de manière générale.

---

### 4. Ce que cet axe établit structurellement

**A. Engagement parental sur cinq ans, documenté en temps réel**

Les **18 adaptations professionnelles distinctes** sont distribuées de mars 2011 à février 2016. Seize précèdent la séparation et deux lui sont postérieures. Ce total est un plancher documentaire : il décrit seulement les adaptations retrouvées dans les courriels de la base et ne permet pas d'affirmer combien d'autres absences auraient pu être communiquées autrement.

**B. Sacrifice professionnel comme preuve d'engagement parental**

Les courriels documentent des adaptations professionnelles réelles : réunion reportée, disponibilité à distance, congé envisagé et obligations manquées. Leur répétition cadre mal avec la caractérisation d'un père *"rarement disponible"* ou *"minimalement impliqué"*.

**C. Les deux enfants, pas seulement Alexia**

À partir de 2013, les absences concernent Nicolas (Email id=30, 28, 21, 15) — preuve que l'engagement de LP ne se limitait pas à son aînée mais s'étendait au second enfant dès sa naissance.

**D. Dimensions documentées**

Rester à la maison avec un enfant malade documente la présence physique et l'adaptation du travail. Les rendez-vous documentent l'accompagnement médical. L'email id=118 documente la connaissance du traitement et la participation au suivi médical. Ces dimensions doivent être considérées avec les autres axes du rôle parental, et non comme une preuve autonome d'implication adéquate.

---

## Application aux allégations contestées

### Stmt 9 — *"Le défendeur ne s'impliquait que minimalement dans les soins d'Alexia, laissant toute la responsabilité à la demanderesse"*

**Directement et fortement réfuté.** LP a documenté **11 adaptations professionnelles distinctes** pour Alexia entre mars 2011 et septembre 2012, dont une demi-journée, auxquelles s'ajoute le suivi médical du 3 mai 2011. Ces faits sont documentés par des courriels à ses supérieurs à la Banque Nationale — tiers neutres, sans lien avec le litige. Leur force tient à leur répétition et à leur distribution, non à un décompte gonflé de courriels appartenant à la même occurrence.

### Stmt 19 — *"Les enfants sont jeunes et de plus, le défendeur était rarement disponible pour prendre soin d'eux"*

Les adaptations documentées couvrent l'intégralité de la période 2011–2016. Elles établissent que LP réorganisait ses obligations professionnelles pour répondre aux besoins des enfants. Leur continuité et leur répétition cadrent mal avec la caractérisation *"rarement disponible"*.

### Stmt 20 — *"C'est la demanderesse qui s'occupait des enfants, qui allait aux activités, etc."*

Email id=27 démontre explicitement que LP et Élise se coordonnaient pour les soins des enfants malades : *"Élise ma conjointe va prendre la relève si nécessaire"*. Il ne s'agit pas d'une prise en charge exclusive par la demanderesse — c'est un système de coordination entre deux parents co-responsables.

---

## Synthèse — valeur probatoire comparative

Cet axe présente une forte valeur probatoire documentaire pour les raisons suivantes :

1. **Documents à des tiers neutres** — supérieurs hiérarchiques sans lien avec le litige
2. **Contemporanéité** — communications faites lorsque l'horaire professionnel devait être adapté
3. **Conséquences professionnelles réelles documentées** — réunions reportées, congés pris
4. **Couverture temporelle continue** — 5 ans, les deux enfants, toute la période alléguée
5. **Formulations directes dans plusieurs occurrences** — par exemple : *"je reste à la maison avec ma fille parce qu'elle est malade"*

Contrairement aux axes 1–3, qui établissent une récurrence à partir d'une structure externe, cet axe établit la récurrence par la distribution d'occurrences contemporaines. Certaines sont directes; d'autres exigent une inférence contextuelle précisément identifiée, comme l'absence du 8 février 2013.

---

## Lien avec les autres axes

- **Axe 1 (danse)** : les cours de danse établissent une disponibilité planifiée du père le soir; le présent axe établit séparément sa capacité d'adapter son travail lorsqu'un besoin imprévu survient. Aucune coïncidence précise entre une absence de jour et un cours de danse n'est affirmée sans pièce propre à la date concernée.
- **Axe 3 (garderie)** : Email id=68 (*"La gardienne ne pouvait pas se déplacer"*) s'articule directement avec l'axe garderie — quand la garderie ou la gardienne tombe, c'est LP qui reste. C'est la même logique de coordination quotidienne.
- **Email id=27** (*"Élise va prendre la relève"*) est la preuve directe que la coordination documentée dans l'Axe 3 (Email id=54 : *"vas tu la chercher ou j'y vais?"*) s'applique aussi aux situations d'enfants malades.
