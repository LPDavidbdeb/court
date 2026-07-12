# Axe argumentatif — Division des tâches parentales lors des activités des enfants

**Portée :** Cet axe est applicable aux allégations contestant l'implication historique du père (Doc id=1, stmts 9, 19, 20 et autres). Il couvre la période 2013–2014 directement documentée, et structurellement toute la période de vie commune.

**Thèse :** Alexia et Nicolas participaient simultanément à plusieurs activités récurrentes sur une base hebdomadaire, organisées en sessions (automne, hiver, printemps). La logistique de ces activités — horaires simultanés, enfants différents, lieux différents — structurait le quotidien des parents et imposait une coordination régulière : un parent avec un enfant à l'activité, l'autre parent avec le second enfant. Post-séparation, Élise a dû embaucher une aide familiale pour assumer seule cette logistique.

---

## Inventaire des pièces — reconstituable en session froide

> **Requêtes DB :** `Email.objects.filter(id__in=[7, 32, 305, 306])`, `Event.objects.filter(id__in=[239, 263])`, `ChatMessage.objects.filter(id__in=[111, 126, 127, 129, 131, 133, 138, 142, 143, 145, 146])` (googlechat_manager.models.ChatMessage, champ text_content)

| # | Date | Type | PK | Protagonistes | Passage pertinent |
|---|------|------|----|---------------|-------------------|
| 1 | 2013-05-28 | Event | **239** | LP, Alexia | LP au Parc Préville avec Alexia — *"LP is taking picture of Alexia while she is playing soccer in St-Lambert league"* |
| 2 | 2013-07-30 | Email | **32** | Johanne → LP | *"Si tu viens demain avec Nicholas on passera chez Josée"* / LP : *"Y a pas de soccer demain mais je passerai peut-être"* — Johanne assume sans explication que LP vient avec Nicolas pendant le soccer d'Alexia |
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
| 15 | 2016-09-16 17:35 | Email | **305** | Élise → LP | *"j'ai une aide familiale pour leurs cours de natation et pour mes soirs de danse"* — aveu exprès post-séparation |
| 16 | 2016-09-16 20:39 | Email | **7** | LP → Élise | *"Quand les enfants avaient des cours, tu les prenais les 2 et moi je restait a la maison et me saoulais pendant ce temps la"* — passage sarcastique au registre identique à celui utilisé pour l'axe danse |
| 17 | 2016-09-16 20:50 | Email | **306** | Élise → LP | Ne conteste pas l'énoncé sur la prise en charge des deux enfants lors des activités — conteste uniquement l'imputation d'alcoolisme |

---

## Principe de l'argument

### 1. Volume d'activités — preuve de nécessité structurelle de coordination

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

**L'argument de volume :** avec deux enfants dans 4 à 5 activités simultanées, sur des horaires hebdomadaires fixes en sessions, la coordination entre les parents est **structurellement nécessaire**. Il est impossible qu'un seul parent gère simultanément deux enfants à deux endroits différents au même moment. La division des tâches n'est pas un choix — c'est une contrainte mathématique.

---

### 2. Instance documentée de coordination — Soccer d'Alexia (2013)

En 2013, Alexia joue dans la ligue de soccer de Saint-Lambert, entraînée par Élise. Pendant ces pratiques et matchs, LP vient avec Nicolas.

- **Event id=239 (2013-05-28)** : LP photographie Alexia en train de jouer au soccer au Parc Préville — il est présent aux matchs
- **Email id=32 (2013-07-30)** : Johanne écrit à LP *"Si tu viens demain avec Nicolas..."* sans expliquer le contexte — elle **présuppose** que LP vient avec Nicolas pendant le soccer. LP répond *"Y a pas de soccer demain"*, confirmant que le schéma habituel est bien LP + Nicolas pendant le soccer d'Alexia
- **Event id=263 (2013-08-24)** : LP à la remise des médailles de soccer avec Alexia en fin de saison

La coordination est tellement établie que Johanne n'a pas besoin de l'expliquer. C'est la preuve que le schéma "un parent avec un enfant à l'activité, l'autre parent avec le second enfant" était **une routine non-verbalisée**.

---

### 3. Aveu exprès post-séparation — Email id=305

Le 16 septembre 2016, Élise écrit à LP :

> *"j'ai une aide familiale pour leurs cours de natation et pour mes soirs de danse"*

Ce passage confirme deux faits distincts :

1. **"leurs cours de natation"** — les enfants avaient des cours de natation récurrents. Post-séparation, une aide familiale les accompagne. Pendant la vie commune, c'était le père.
2. **"mes soirs de danse"** — Élise reconnaît ses propres soirées de danse récurrentes, au présent de l'indicatif.

L'aide familiale est le **substitut post-séparation** du rôle que LP jouait lors de ces moments. Cette déclaration constitue un aveu exprès au sens de l'art. 2850 C.c.Q.

---

### 3bis. Acquiescement tacite — Email id=7 et id=306 (même échange que l'axe danse)

Dans le même courriel du 16 septembre 2016 déjà analysé dans l'axe danse, LP écrit aussi, sur un registre sarcastique :

> *"Quand les enfants avaient des cours, tu les prenait les 2 et moi je restait a la maison et me saoulais pendant ce temps la."*

Ce passage applique à l'axe activités le même mécanisme que celui déjà établi pour l'axe danse : LP décrit, de façon ironique, les conséquences logiques de l'allégation d'Élise selon laquelle il ne s'occupait pas des enfants 50% du temps. Dans sa réponse (Email id=306), Élise conteste **exclusivement** l'imputation d'alcoolisme — elle ne conteste pas l'énoncé selon lequel elle prenait les deux enfants ensemble lors de leurs activités. Cette absence de contestation constitue un acquiescement tacite (art. 2850 C.c.Q.) sur ce point précis.

---

### 4. Ce que cet axe établit structurellement

**A. Engagement parental hebdomadaire récurrent**

Les activités ne sont pas des événements ponctuels. Natation, gym, danse, cheerleading — chaque programme s'organise en sessions (~10–15 semaines) avec un jour et une heure fixes. Sur une année, cela représente des dizaines de semaines où les parents gèrent simultanément les horaires de deux enfants dans des activités différentes.

**B. La division des tâches est la norme, pas l'exception**

L'Email id=32 (soccer) démontre que Johanne connaissait le schéma de coordination sans qu'il ait besoin d'être expliqué — preuve que c'était le **fonctionnement normal** du foyer, et non un arrangement exceptionnel.

**C. LP connaît précisément chaque programme**

Dans le thread d'octobre 2014, LP calcule lui-même les coûts : 210$ natation, 300$ cheerleading, 500$ total partiel, 3 sessions/an. Ce niveau de détail est incompatible avec un père absent ou désengagé de l'organisation familiale.

**D. Le recours à l'aide familiale confirme le rôle de LP**

Élise n'a pas maintenu la même organisation après la séparation — elle a dû embaucher une aide familiale. Cette décision révèle a posteriori que c'est LP qui remplissait cette fonction logistique pendant la vie commune.

---

## Application aux allégations contestées

### Stmt 9 — *"Le défendeur ne s'impliquait que minimalement dans les soins d'Alexia, laissant toute la responsabilité à la demanderesse"*

Le volume d'activités documenté dans le thread d'octobre 2014 (natation, gym, danse, cheerleading, ski — deux enfants, plusieurs sessions par an) démontre que l'organisation de la vie familiale exigeait une coordination parentale constante. LP participe à cette coordination activement : il est présent aux matchs de soccer (Events 239, 263), il vient avec Nicolas pendant les activités d'Alexia (Email 32), et il connaît en détail chaque programme d'activité et son coût (ChatMessages 111–146).

### Stmt 20 — *"C'est la demanderesse qui s'occupait des enfants, qui allait aux activités, etc."*

La demanderesse ne pouvait pas simultanément coacher le soccer d'Alexia ET s'occuper de Nicolas. La preuve documentaire (Email id=32, Events id=239, 263) démontre que c'est LP qui gérait Nicolas pendant ces moments. Le thread Google Chat (oct. 2014) démontre que les deux parents suivaient conjointement l'ensemble du calendrier d'activités.

---

## Note — pièces à corréler

Cet axe est directement lié à l'**Axe 1 (danse d'Élise)** : les "soirs de danse" mentionnés dans Email id=305 renvoient à l'axe danse (voir `axe_agenda_danse_elise.md`). Les deux axes se corroborent mutuellement et s'appuient sur le même aveu exprès d'Élise dans Email id=305.
