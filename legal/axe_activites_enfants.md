# Axe argumentatif — Division des tâches parentales lors des activités des enfants

> **Document de référence actuel :** [implication_parentale_recurrence/03_activites_enfants.md](implication_parentale_recurrence/03_activites_enfants.md). Le présent inventaire antérieur demeure utile pour localiser les sources, mais ses inférences sont subordonnées aux calibrations du document de référence et des pièces atomiques.

**Portée :** Cet axe est applicable aux allégations contestant l'implication historique du père (Doc id=1, stmts 9, 19, 20 et autres). Il couvre la période 2013–2014 directement documentée, et structurellement toute la période de vie commune.

**Thèse :** Alexia et Nicolas participaient à plusieurs activités récurrentes sur une base hebdomadaire, organisées en sessions (automne, hiver, printemps). Il n'est pas nécessaire que deux activités différentes soient concomitantes. Dès qu'un enfant devait être accompagné à un cours, deux fonctions existaient : un parent accompagnait l'enfant participant et l'autre prenait en charge le second enfant. Après la séparation, Élise indique recourir à une aide familiale pour les cours de natation et ses soirs de danse; cette aide n'est ni LP ni l'une de ses sœurs, mais son identité positive et son statut ne sont pas établis.

---

## Inventaire des pièces — reconstituable en session froide

> **Requêtes DB :** `Email.objects.filter(id__in=[7, 32, 305, 306])`, `Event.objects.filter(id__in=[239, 263])`, `ChatMessage.objects.filter(id__in=[111, 126, 127, 129, 131, 133, 138, 142, 143, 145, 146])` (googlechat_manager.models.ChatMessage, champ text_content)

| # | Date | Type | PK | Protagonistes | Passage pertinent |
|---|------|------|----|---------------|-------------------|
| 1 | 2013-05-28 | Event | **239** | LP, Alexia | LP au Parc Préville avec Alexia — *"LP is taking picture of Alexia while she is playing soccer in St-Lambert league"* |
| 2 | 2013-07-29 | Emails | **33, 32** | Johanne ↔ LP | Johanne envisage que LP vienne le lendemain *« avec Nicholas »*; LP répond *« Y a pas de soccer demain mais je passerai peut etre »* — la venue avec Nicolas est rattachée à la tenue du soccer |
| 3 | 2013-08-24 | Event | **263** | LP, Alexia | *"LP is at 'la remise des médailles de soccer' with Alexia"* |
| 4 | 2014-10-23 14:23 | ChatMessage | **111** | LP → Élise | *"La garderie va passer bientôt"* — LP surveille les prélèvements garderie, inclus dans la comptabilité des activités |
| 5 | 2014-10-23 14:31 | ChatMessage | **126** | Élise → LP | *"la piscine et la gym passe sur ma visa"* — Élise gère les paiements natation et gym |
| 6 | 2014-10-23 14:32 | ChatMessage | **127** | Élise → LP | *"la danse c'est plus chère car il y a les deux cours et c'est genre 250$ moi je te donne juste la moitié car **je paie le mien** mais mon chèque a les 2"* — Élise confirme qu'elle paie son propre cours de danse séparément des cours des enfants |
| 7 | 2014-10-23 14:32 | ChatMessage | **129** | Élise → LP | *"la piscine c'est 70$ chaque"* — 70$/enfant/session de natation |
| 8 | 2014-10-23 14:33 | ChatMessage | **131** | Élise → LP | *"la gym c'est 110 je pense il faudrait que j'aille voir"* — AcroGym ~110$/session/enfant |
| 9 | 2014-10-23 14:34 | ChatMessage | **133** | Élise → LP | Transaction : *"VILLE DE SAINT LAMBERT 70,00$"* du 20-21 oct. 2014 — paiement natation |
| 10 | 2014-10-23 14:35 | ChatMessage | **138** | Élise → LP | Transaction : *"VILLE DE SAINT LAMBERT 70,00$"* du 10-11 sept. 2014 — deuxième session natation |
| 11 | 2014-10-23 14:36 | ChatMessage | **142** | LP → Élise | *"3X par annes right"* — LP confirme 3 sessions de natation par année |
| 12 | 2014-10-23 14:37 | ChatMessage | **143** | Élise → LP | Transaction : *"AMILIA *AcroGym Montreal 100,00$"* du 16-17 juill. 2014 — paiement gym |
| 13 | 2014-10-23 14:38 | ChatMessage | **145** | Élise → LP | *"200$ par enfant"* par année pour la gym |
| 14 | 2014-10-23 14:38 | ChatMessage | **146** | Élise → LP | *"par année"* — confirmation |
| 15 | 2016-09-16 17:35 | Email | **305** | Élise → LP | *"j'ai une aide familiale pour leurs cours de natation et pour mes soirs de danse"* — affirmation directe d'un relais post-séparation distinct de LP et des sœurs |
| 16 | 2016-09-16 20:39 | Email | **7** | LP → Élise | *"Quand les enfants avaient des cours, tu les prenais les 2 et moi je restait a la maison et me saoulais pendant ce temps la"* — passage sarcastique au registre identique à celui utilisé pour l'axe danse |
| 17 | 2016-09-16 20:50 | Email | **306** | Élise → LP | Nie l'imputation sarcastique d'alcoolisme et maintient seulement que LP ne s'occupait pas des enfants 50 % du temps; ne répond pas séparément au fonctionnement entourant les activités |

---

## Principe de l'argument

### 1. Volume d'activités — besoin structurel de coordination

Le thread Google Chat du 23 octobre 2014 (ChatMessages id=111–311) documente un inventaire complet des activités des deux enfants que les deux parents gèrent conjointement :

| Activité | Enfant(s) | Fréquence | Coût annuel |
|----------|-----------|-----------|-------------|
| Natation (Ville de Saint-Lambert) | Les deux | 3 sessions × ~10 semaines | 70$ × 3 = 210$/enfant/an |
| Gym / AcroGym Montréal | Les deux | ~2 sessions/an | ~100–110$/session/enfant |
| Danse (cours enfants) | Les deux | sessions automne/hiver | ~125$/session |
| Cheerleading | — | sessions | ~300$/an |
| Ski | — | saison hivernale | variable |
| Danse d'Élise (son propre cours) | Élise | sessions automne/hiver | ~125$/session (elle paie le sien) |

LP calcule lui-même, dans le thread, les totaux annuels activité par activité. Ce niveau de détail — il connaît précisément chaque programme, chaque session, chaque montant — est la preuve d'un parent activement impliqué dans la gestion logistique des activités.

**L'argument de volume :** avec deux enfants et plusieurs activités organisées selon des horaires hebdomadaires fixes, le besoin d'accompagner un enfant se reproduit pendant chaque session. La coordination ne dépend pas de la tenue simultanée de deux cours différents. Lorsqu'un enfant participe à une activité sans le second, un adulte doit l'accompagner pendant qu'un autre adulte prend en charge l'enfant qui ne participe pas. Le témoignage et les occurrences documentées établiront que les parents se répartissaient habituellement ces deux fonctions.

---

### 2. Instance documentée de coordination — Soccer d'Alexia (2013)

> **Analyse particulière et calibrée :** [implication_parentale_recurrence/03a_soccer_alexia_ete_2013.md](implication_parentale_recurrence/03a_soccer_alexia_ete_2013.md).

En 2013, Alexia participe au soccer de Saint-Lambert. LP témoignera qu'Élise animait bénévolement deux ateliers par semaine et que, pendant ces ateliers, il prenait normalement Nicolas en charge.

- **Event id=239 (2013-05-28)** : les photographies montrent Alexia participant à un atelier; l'explication attribue les images à LP, à authentifier
- **Emails id=33 et 32 (soir du 29 juillet)** : Johanne envisage que LP vienne le lendemain *« avec Nicholas »*; LP rattache sa réponse au fait qu'il n'y a pas de soccer le 30 juillet
- **Event id=263 (2013-08-24)** : les photographies montrent Alexia avec sa médaille et les autres jeunes joueurs; l'explication attribue la présence à LP, à authentifier

Le fil ne nomme ni Alexia ni Élise. Sa portée apparaît lorsqu'il est combiné au témoignage sur le rôle d'Élise : Johanne intègre Nicolas au déplacement envisagé et LP répond en fonction de l'exception au calendrier de soccer. Cette formulation corrobore un fonctionnement familial déjà connu, sans constituer seule la preuve de chaque atelier.

---

### 3. Aveu exprès post-séparation — Email id=305

Le 16 septembre 2016, Élise écrit à LP :

> *"j'ai une aide familiale pour leurs cours de natation et pour mes soirs de danse"*

Ce passage confirme deux faits distincts :

1. **"leurs cours de natation"** — les enfants avaient des cours de natation récurrents. Après la séparation, une aide familiale répond au besoin associé à ces cours.
2. **"mes soirs de danse"** — Élise reconnaît ses propres soirées de danse récurrentes, au présent de l'indicatif.

Le contexte du fil distingue cette aide familiale de LP et des sœurs d'Élise. Le message n'établit toutefois ni son identité positive, ni sa rémunération, ni le partage historique exact pendant la cohabitation. Il corrobore l'existence d'un besoin logistique récurrent après la séparation; le rôle historique de LP doit être établi par les autres pièces et son témoignage.

---

### 3bis. Réponse quantitative — Email id=7 et id=306 (même échange que l'axe danse)

Dans le même courriel du 16 septembre 2016 déjà analysé dans l'axe danse, LP écrit aussi, sur un registre sarcastique :

> *"Quand les enfants avaient des cours, tu les prenait les 2 et moi je restait a la maison et me saoulais pendant ce temps la."*

Ce passage applique à l'axe activités le même mécanisme que celui déjà établi pour l'axe danse : LP décrit, de façon ironique, les conséquences logiques de l'allégation d'Élise selon laquelle il ne s'occupait pas des enfants 50 % du temps. Dans sa réponse (Email id=306), Élise nie l'imputation d'alcoolisme et maintient que LP ne s'occupait pas des enfants 50 % du temps. Elle ne répond pas séparément au fonctionnement entourant les activités.

Cette absence de dénégation précise ne constitue pas un aveu formel de chaque occurrence. Sa valeur est contextuelle : dans la discussion directe, Élise défend une asymétrie quantitative, non la représentation judiciaire d'un père étranger aux activités ou rarement disponible. Les pièces contemporaines doivent corroborer le fonctionnement général décrit par LP.

---

### 4. Ce que cet axe établit structurellement

**A. Engagement parental hebdomadaire récurrent**

Les activités ne sont pas des événements ponctuels. Natation, gym, danse, cheerleading — chaque programme s'organise en sessions (~10–15 semaines) avec un jour et une heure fixes. Sur une année, cela représente des dizaines de semaines où le besoin d'accompagner un enfant et de prendre en charge l'autre se répète, sans qu'il soit nécessaire que deux cours différents aient lieu en même temps.

**B. La division des tâches est la norme, pas l'exception**

L'Email id=32 (soccer) démontre que Johanne connaissait le schéma de coordination sans qu'il ait besoin d'être expliqué — preuve que c'était le **fonctionnement normal** du foyer, et non un arrangement exceptionnel.

**C. LP connaît précisément chaque programme**

Dans le thread d'octobre 2014, LP calcule lui-même les coûts : 210$ natation, 300$ cheerleading, 500$ total partiel, 3 sessions/an. Ce niveau de détail est incompatible avec un père absent ou désengagé de l'organisation familiale.

**D. Le recours à l'aide familiale confirme un besoin logistique récurrent**

Après la séparation, Élise affirme recourir à une aide familiale pour les cours de natation et ses soirs de danse. Cette affirmation confirme que ces événements récurrents créent un besoin de prise en charge. Elle n'identifie pas, à elle seule, la personne qui remplissait chaque fonction pendant la vie commune; cette attribution repose sur les autres pièces et le témoignage.

---

## Application aux allégations contestées

### Stmt 9 — *"Le défendeur ne s'impliquait que minimalement dans les soins d'Alexia, laissant toute la responsabilité à la demanderesse"*

Le volume d'activités documenté dans le thread d'octobre 2014 (natation, gym, danse, cheerleading, ski — deux enfants, plusieurs sessions par an) démontre que l'organisation de la vie familiale exigeait une coordination parentale constante. LP participe à cette coordination activement : il est présent aux matchs de soccer (Events 239, 263), il vient avec Nicolas pendant les activités d'Alexia (Email 32), et il connaît en détail chaque programme d'activité et son coût (ChatMessages 111–146).

### Stmt 20 — *"C'est la demanderesse qui s'occupait des enfants, qui allait aux activités, etc."*

La demanderesse ne pouvait pas simultanément coacher le soccer d'Alexia ET s'occuper de Nicolas. La preuve documentaire (Email id=32, Events id=239, 263) démontre que c'est LP qui gérait Nicolas pendant ces moments. Le thread Google Chat (oct. 2014) démontre que les deux parents suivaient conjointement l'ensemble du calendrier d'activités.

---

## Note — pièces à corréler

Cet axe est directement lié à l'**Axe 1 (danse d'Élise)** : les « soirs de danse » mentionnés dans Email id=305 renvoient à l'axe danse (voir `axe_agenda_danse_elise.md`). Le même message corrobore l'existence postérieure de deux besoins récurrents — natation et danse — auxquels Élise répond par une aide familiale distincte de LP et des sœurs.
