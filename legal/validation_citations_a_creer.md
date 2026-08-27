# Feuille de validation — citations `Cn` à créer en base

> Généré le 26 août 2026 à partir des 283 `piece_*.md`. **Rien n'a été écrit en base.** Chaque entrée est un bloc `Cn` d'un fichier pièce qui n'a pas d'équivalent parmi les citations existantes. Cocher `créer`, `corriger` (en annotant dessous) ou `écarter`, puis me redonner le fichier.

| | n |
|---|---|
| passages verbatim | 125 |
| constats (lecture du document) | 51 |
| objets (chat, photo) | 27 |
| source à trancher | 2 |
| **total** | **205** |

**Contrôle automatique.** Chaque texte proposé a été cherché dans la transcription de sa source (`ai_analysis` pour un PDF, le corps pour un courriel), après repliage par `core.text_matching`. **90 entrées se retrouvent** telles quelles et se créeront sans réserve ; **64** ne se retrouvent pas — citation composite, ellipse `[…]`, ou transcription de la source incomplète — et demandent soit un texte ajusté, soit une `position_anchor`.

## Deux contraintes du schéma, à décider une fois pour toutes

1. **`email_manager.Quote` n'a que `email` et `quote_text`.** Ni titre, ni ancre, ni localisation. Le titre du `Cn` n'a donc **aucun champ où aller** pour les citations de courriels : soit on l'abandonne, soit on ajoute `quote_location_details` au modèle courriel comme il existe déjà côté PDF.

2. **`pdf_manager.Quote.page_number` est obligatoire.** Les fichiers pièce ne portent pas toujours la page. Les entrées marquées ⚠️ en attendent une.
---

## 1. Passages verbatim — `Quote(quote_text=…)` (125)

Le bloc contient un extrait cité entre guillemets. Rien à interpréter : le texte proposé est l'extrait.


### `Email` **3** — « emplois », Louis Philippe David <louisphilippe.david@gmail.com>, 2020-06-22

#### V022 · `piece_thread-3_email-3.md` **C4**
*bonne foi + cadrage « pour les enfants »*

- **source** — `Email` **3** — « emplois », Louis Philippe David <louisphilippe.david@gmail.com>, 2020-06-22
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > si je ne me suis pas trouvé d'emplois ici à ce salaire ce n'est pas par mauvaise foi » ; « la meilleur option pour les enfants ».
- **titre du Cn** — bonne foi + cadrage « pour les enfants » — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **7** — « Re: Visite », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-16

#### V024 · `piece_thread-6_email-7.md` **C1**
*Non-ingérence de LP dans la relation d'Élise avec les enfants*

- **source** — `Email` **7** — « Re: Visite », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Je n'ai jamais interferer dans ta relations avec tes enfants, je t'ai laisser faire ce que tu voulais, comme tu le voulais, j'étais pret a te laisser 7 jours sur 14, je ne t'ai jamais demander de voir tes enfants moins
- **titre du Cn** — Non-ingérence de LP dans la relation d'Élise avec les enfants — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **16** — « Re: Dépenses », Elise Ayoub <elise.ayoub@gmail.com>, 2016-01-11

#### V026 · `piece_thread-12_email-16.md` **C2**
*Corroboration : offre de garde partagée faite « dès le départ », refusée au motif « trop jeunes »*

- **source** — `Email` **16** — « Re: Dépenses », Elise Ayoub <elise.ayoub@gmail.com>, 2016-01-11
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Par choix Elise, dès que je suis partis je t'ai offert une garde partagée, Tu as refusé […] tu m'as dis qu'ils etaient trop jeune […] je t'ai dis que quand tu jugeras qu'ils seront assez vieux, nous pourront commencer une transition vers une garde partagé sur une période de 6 a 8 mois. » « Je t'ai offert de les prendre une fin de semaine sur deux ce que tu refuses de faire donc le 20% je n'ai pas le choix d'engager de l'aide.
- **titre du Cn** — Corroboration : offre de garde partagée faite « dès le départ », refusée au motif « trop jeunes » — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **22** — « Re: Cle », "Élise " <elise.ayoub@gmail.com>, 2015-02-27

#### V027 · `piece_thread-18_27fev2015.md` **C1**
*« conjoints de fait… pas chambre à part… activités communes » (id=171)*

- **source** — `Email` **22** — « Re: Cle », "Élise " <elise.ayoub@gmail.com>, 2015-02-27
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes…. Fais comme tu veux mais moi je n'ai pas envie d'avoir à rembourser, c'est ton choix. La cohabitation est un critère important, mais pas toujours déterminant…
- **titre du Cn** — « conjoints de fait… pas chambre à part… activités communes » (id=171) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V028 · `piece_thread-18_27fev2015.md` **C2**
*« tu étais mon chum… je t'ai embrassé… j'espérais qu'on revienne de cette impasse » (id=22)*

- **source** — `Email` **22** — « Re: Cle », "Élise " <elise.ayoub@gmail.com>, 2015-02-27
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > pour moi tu étais mon chum et je ai a quelque reprise embrasse… pour moi tu étais mon chum et j'espérais quon revienne de cette impasse…
- **titre du Cn** — « tu étais mon chum… je t'ai embrassé… j'espérais qu'on revienne de cette impasse » (id=22) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V029 · `piece_thread-18_27fev2015.md` **C3**
*« conjoint de fait… je ne te considérais pas comme mon coloc » (id=167)*

- **source** — `Email` **22** — « Re: Cle », "Élise " <elise.ayoub@gmail.com>, 2015-02-27
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Nous étions considérés conjoint de fait et donc non on ne peut les faire séparés… je ne te considérais pas comme mon coloc…
- **titre du Cn** — « conjoint de fait… je ne te considérais pas comme mon coloc » (id=167) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **29** — « Re: souper », Louis Philippe David <louisphilippe.david@gmail.com>, 2014-09-18

#### V030 · `piece_thread-23_email-29.md` **C2**
*Planification d’un souper et de l’anniversaire d’Alexia*

- **source** — `Email` **29** — « Re: souper », Louis Philippe David <louisphilippe.david@gmail.com>, 2014-09-18
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Ta soeur revient le 22 - je réserve le 27 pour un souper si tout le monde est libre. » « Veux tu en profiter pour fêter Alexia. » « Oui j'y avais pensé de la fêter. c'est une excellente idée.
- **titre du Cn** — Planification d’un souper et de l’anniversaire d’Alexia — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **33** — « Re: passe de plage Cape Cod », Johanne Bazinet <johannebazinet@gmail.com>, 2013-07-29

#### V031 · `piece_thread-26_emails-33-32.md` **C2**
*LP rattache sa venue à la tenue du soccer*

- **source** — `Email` **33** — « Re: passe de plage Cape Cod », Johanne Bazinet <johannebazinet@gmail.com>, 2013-07-29
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Y a pas dw soccer demain mais je passerai peut etre
- **titre du Cn** — LP rattache sa venue à la tenue du soccer — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **34** — « Re: Bonne fête », Louis Philippe David <louisphilippe.david@gmail.com>, 2013-07-22

#### V032 · `piece_thread-27_email-34.md` **C4**
*Continuité entre la planification et l'événement tenu*

- **source** — `Email` **34** — « Re: Bonne fête », Louis Philippe David <louisphilippe.david@gmail.com>, 2013-07-22
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Ève : « J'ai annulé ma présence mercredi » ; LP : « Elise ne t'en veux pas du tout.
- **titre du Cn** — Continuité entre la planification et l'événement tenu — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **66** — « ce soir », Johanne BAZINET <johannebazinet@gmail.com>, 2011-03-15

#### V033 · `piece_thread-52_emails-66-115-116.md` **C2**
*Le mardi comporte plus d'un cours de danse*

- **source** — `Email` **66** — « ce soir », Johanne BAZINET <johannebazinet@gmail.com>, 2011-03-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > ce soir elise ne va pas a son premier cour de danse je sais pas a quelle heure elle va partit je t'appel si c est pas trops tard sinon on se vois demain
- **titre du Cn** — Le mardi comporte plus d'un cours de danse — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V034 · `piece_thread-52_emails-66-115-116.md` **C3**
*La visite est reportée*

- **source** — `Email` **66** — « ce soir », Johanne BAZINET <johannebazinet@gmail.com>, 2011-03-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > ôk on remet cela à demain
- **titre du Cn** — La visite est reportée — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **80** — « Alexia », Johanne BAZINET <johannebazinet@gmail.com>, 2010-12-09

#### V035 · `piece_thread-65_emails-80-100.md` **C1**
*Confirmation de la visite du mercredi 8 décembre*

- **source** — `Email` **80** — « Alexia », Johanne BAZINET <johannebazinet@gmail.com>, 2010-12-09
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > J'ai adoré ma visite hier avec Alexia - j'aimerais que tu me dises quand ce sera possible car je ne veux pas qu'elle m'oublie.
- **titre du Cn** — Confirmation de la visite du mercredi 8 décembre — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V036 · `piece_thread-65_emails-80-100.md` **C2**
*Énoncé exprès des deux jours hebdomadaires*

- **source** — `Email` **80** — « Alexia », Johanne BAZINET <johannebazinet@gmail.com>, 2010-12-09
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > mais je t'ai deja dit que les mardi et mercredi elise dansait.
- **titre du Cn** — Énoncé exprès des deux jours hebdomadaires — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **87** — « (sans objet) », Louis Philippe David <louisphilippe.david@gmail.com>, 2010-10-12

#### V037 · `piece_emails_petite_enfance_2010.md` **C4**
*Le demandeur coordonne la garde et informe la famille maternelle*

- **source** — `Email` **87** — « (sans objet) », Louis Philippe David <louisphilippe.david@gmail.com>, 2010-10-12
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Oui viens garder vendredi si tu peux, confirme moi pour que j'avertisse la mere à elise !!
- **titre du Cn** — Le demandeur coordonne la garde et informe la famille maternelle — ⚠️ *aucun champ dans le modèle courriel*
- **attribution retirée du texte** — LP → Johanne, 12 octobre 2010 (Email id=87)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **89** — « garde de Alexia », Johanne BAZINET <johannebazinet@gmail.com>, 2010-09-13

#### V038 · `piece_emails_petite_enfance_2010.md` **C5**
*Coordination des jours de garde de Johanne (organisée par le demandeur)*

- **source** — `Email` **89** — « garde de Alexia », Johanne BAZINET <johannebazinet@gmail.com>, 2010-09-13
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Tu m'as demandé si je pouvais changer mes vendredis pour les lundis pour octobre…
- **titre du Cn** — Coordination des jours de garde de Johanne (organisée par le demandeur) — ⚠️ *aucun champ dans le modèle courriel*
- **attribution retirée du texte** — Johanne → LP, 13 septembre 2010 (Email id=89)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **114** — « Re: message », Louis Philippe David <louisphilippe.david@gmail.com>, 2011-03-08

#### V039 · `piece_thread-53_email-114.md` **C2**
*La visite de Johanne dépend de l'absence d'Élise*

- **source** — `Email` **114** — « Re: message », Louis Philippe David <louisphilippe.david@gmail.com>, 2011-03-08
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Je t'ai laissé un message en revenant de Montréal mais en passant devant chez toi la voiture d'Élise était là donc j'ai pensé que je ne devais pas arrêter. Voilà je suis donc revenue chez moi.
- **titre du Cn** — La visite de Johanne dépend de l'absence d'Élise — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **163** — « Re: Cle », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-02-27

#### V040 · `piece_thread-18_email-163.md` **C2**
*LP fait de la nature du plan la preuve de la fin de la relation — analyse (→ thèse)*

- **source** — `Email` **163** — « Re: Cle », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-02-27
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > je pense être en mesure de le prouver […] je pense que toute personne raisonnable pourrait conclure à la même chose.
- **titre du Cn** — LP fait de la nature du plan la preuve de la fin de la relation — analyse (→ thèse) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **174** — « renocntre », "Claudia Écrement" <claudia.ecrement@videotron.ca>, 2015-09-16

#### V041 · `piece_thread-16_ecrement_2015.md` **C1**
*Écrement déclare elle-même n'être « ni avocate, ni médiatrice » [id=174]*

- **source** — `Email` **174** — « renocntre », "Claudia Écrement" <claudia.ecrement@videotron.ca>, 2015-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Je ne suis ni avocate, ni médiatrice mais je pourrais vous donner un point de vue neutre quant au bien-être des enfants selon leurs âges et particularités.
- **titre du Cn** — Écrement déclare elle-même n'être « ni avocate, ni médiatrice » [id=174] — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **184** — « Re: renocntre », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-09-16

#### V042 · `piece_thread-16_ecrement_2015.md` **C3**
*C'est LP qui SOLLICITE la rencontre [id=184]*

- **source** — `Email` **184** — « Re: renocntre », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Je veux vous rencontrer, de préférence le soir et j'aimerais savoir combien ça va me couter.
- **titre du Cn** — C'est LP qui SOLLICITE la rencontre [id=184] — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **268** — « Re: Visite », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-16

#### V043 · `piece_thread-6_email-268.md` **C1**
*Position de LP sur le niveau de participation demandé*

- **source** — `Email` **268** — « Re: Visite », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > si tu avais voulu ma participation tu devais l'accepter à 50% à l'époque, pas 20 pas 30 pas 40...50%.
- **titre du Cn** — Position de LP sur le niveau de participation demandé — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **270** — « Re: Visite », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-16

#### V044 · `piece_thread-6_email-270.md` **C8**
*Asymétrie des voyages (LP n'a jamais bloqué ceux d'Élise)*

- **source** — `Email` **270** — « Re: Visite », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > je n'ai jamais dit que tu n'étais pas apte à t'occuper de tes enfants, je ne t'ai jamais empêché d'aller en vacances avec, ce n'est pas moi qui condamne ici.
- **titre du Cn** — Asymétrie des voyages (LP n'a jamais bloqué ceux d'Élise) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **279** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16

#### V045 · `piece_thread-6_email-279.md` **C5**
*Élise reconnaît la demande de déchéance adressée par LP*

- **source** — `Email` **279** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Oui car dans les faits tu étais confus. Tu m'as envoyé à plusieurs reprises des emails où tu voulais que je demande au juge de me céder l'autorité parentale et après tu m'envoies une mise en demeure qui demande que tu sois consultée. ça s'appelle de la confusion.
- **titre du Cn** — Élise reconnaît la demande de déchéance adressée par LP — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V046 · `piece_thread-6_email-279.md` **C6**
*Pension, intentions, stress/peur*

- **source** — `Email` **279** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > La pension je te l'ai dis, BASÉ SUR LES REVENUS DE L'ANNÉE ANTÉRIEURE. C'est comme ça que la cour le fait et en ce moment c'est ce qui a été fait. Je n'ai jamais eu besoin de te soutirer de l'argent mais si tu veux me dépeindre comme ça c'est toi qui le décide. Je n'ai pas de mauvaises intentions, je n'en ai jamais eu. J'ai eu du stress, de la peur et bien d'autres choses mais JAMAIS DE MAUVAISES INTENTIONS.
- **titre du Cn** — Pension, intentions, stress/peur — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **290** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16

#### V047 · `piece_thread-6_email-290.md` **C7**
*Régime réel des accès : 4h/semaine pendant un an et demi*

- **source** — `Email` **290** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > On a fait un an et demi à 4 heures semaines pourquoi tu changes pas à 8 heures semaine?????? Ou une journée? Pourquoi tu leur retranche du temps avec toi??????? » « Et oui cette année tu serais à 6 jours - 4 nuits. Tu les verrais 3 jours par semaine.
- **titre du Cn** — Régime réel des accès : 4h/semaine pendant un an et demi — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **292** — « Re: Visite », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-16

#### V048 · `piece_thread-6_email-292.md` **C4**
*LP : sœur/avocat et nature de la décision*

- **source** — `Email` **292** — « Re: Visite », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Toi et ta soeur êtes mêler a ca, comment ne pas l'impliquée? dans sa comunication avec mon avocat elle dit que je suis confus, ce sont des faits, que je rapporte c'est tout. » « Ma haine evers toi, qui est bien reel, n'a rien a voir avec ma décision, mais oui c'est mon call, ma décision.
- **titre du Cn** — LP : sœur/avocat et nature de la décision — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **295** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16

#### V050 · `piece_thread-6_email-295.md` **C1**
*Refus de la garde partagée = incapacité de communication (non dangerosité)*

- **source** — `Email` **295** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Louis Philippe ta participation n'a jamais été de 50%. Même quand Alexia était bébé pendant les 13 mois de sa vie avant que tu me trompes et tout devienne encore pire. Jamais. […] ET par dessus tout ceci n'a RIEN à voir avec toi et ce que TOI tu veux. C'était par rapport à leur besoin et le passé que nous avions vécus. Leur relation avec toi et moi, indépendant de ce que toi tu voulais ou moi je voulais. EN PLUS de notre incapacité à se comprendre. […] les gens en garde partagée sont au moins capable de se comprendre, de se parler et de se respecter. Nous non… […] Ma vie aurait été bien plus simple en garde partagée, je le sais. Mais je savais qu'on ne se comprendrait pas plus et que c'est eux qui en paieraient le prix. […] Les options que je t'ai envoyé plus tard en 2015 avaient été réfléchis et pensés en fonction de leur âge et de leur besoin.
- **titre du Cn** — Refus de la garde partagée = incapacité de communication (non dangerosité) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V051 · `piece_thread-6_email-295.md` **C3**
*Diagnostic relationnel (simple désaccord / incompréhension)*

- **source** — `Email` **295** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > On ne se comprend pas, on a toujours eu de la difficulté […]. Je suis passée à autre chose et je suis capable de voir qu'on est pas d'accord et qu'on ne se comprend pas.
- **titre du Cn** — Diagnostic relationnel (simple désaccord / incompréhension) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **304** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16

#### V052 · `piece_thread-6_email-304.md` **C1**
*Recours disponible à des aides ou à des gardiennes*

- **source** — `Email` **304** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Les enfants je m'en occupe et je ne te demande pas de t'organiser avec quand tu les vois justement, ça ne change rien pour moi que tu les prennes le dimanche soir, tu penses que ça change quelque chose dans ma vie à moi? Non. Car si j'ai besoin de faire quelque chose, j'ai des aides ou des gardiennes donc encore une fois tu ne me rends pas service en les prenant.
- **titre du Cn** — Recours disponible à des aides ou à des gardiennes — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V053 · `piece_thread-6_email-304.md` **C2**
*Un père ayant moins de 50 % du temps n'est pas une « nounou »*

- **source** — `Email` **304** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Tu penses que tous les pères qui prennent leurs enfants une fin de semaine sur deux ou moins de 50% du temps sont des nounous?
- **titre du Cn** — Un père ayant moins de 50 % du temps n'est pas une « nounou » — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **308** — « Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16

#### V056 · `piece_thread-6_email-308.md` **C1**
*Aveu : les enfants sont affectés par la rareté des contacts avec le père (préjudice)*

- **source** — `Email` **308** — « Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Tu sais que tu peux les prendre plus souvent aussi, car ils sont agités quand ils ne te voient pas souvent et tu le sais.
- **titre du Cn** — Aveu : les enfants sont affectés par la rareté des contacts avec le père (préjudice) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V057 · `piece_thread-6_email-308.md` **C2**
*Le père est invité à occuper plus de place (contredit le récit « père dangereux / désintéressé »)*

- **source** — `Email` **308** — « Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > les enfants seraient ravis de passer plus de temps avec toi » ; « tu devrais faire un peu plus partie » de leur vie ; « tu peux les prendre plus souvent ».
- **titre du Cn** — Le père est invité à occuper plus de place (contredit le récit « père dangereux / désintéressé ») — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V058 · `piece_thread-6_email-308.md` **C3**
*Réserve de contexte (à ne pas surlire)*

- **source** — `Email` **308** — « Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > les enfants étaient fatigués […] Alexia vit beaucoup d'émotions à l'école […] le dimanche soir en général ils sont épuisés.
- **titre du Cn** — Réserve de contexte (à ne pas surlire) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **313** — « Re: dimanche prochain », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-26

#### V059 · `piece_thread-5_email-5.md` **C5**
*le défendeur demande aussi la cessation (email-313, 15 h 37)*

- **source** — `Email` **313** — « Re: dimanche prochain », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-26
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Elise svp ne m'ecrit plus
- **titre du Cn** — le défendeur demande aussi la cessation (email-313, 15 h 37) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **314** — « Re: dimanche prochain », Elise Ayoub <elise.ayoub@gmail.com>, 2016-09-26

#### V060 · `piece_thread-5_email-5.md` **C2**
*la demanderesse conteste (email-314, 15 h 04)*

- **source** — `Email` **314** — « Re: dimanche prochain », Elise Ayoub <elise.ayoub@gmail.com>, 2016-09-26
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Non tu m'as écris que tu allais continuer à les prendre à chaque semaine et que tu allais m'avertir une semaine à l'avance quand tu n'allais pas les prendre.
- **titre du Cn** — la demanderesse conteste (email-314, 15 h 04) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **316** — « Re: dimanche prochain », Elise Ayoub <elise.ayoub@gmail.com>, 2016-09-26

#### V061 · `piece_thread-5_email-5.md` **C4**
*la demanderesse réitère (email-316, 15 h 18)*

- **source** — `Email` **316** — « Re: dimanche prochain », Elise Ayoub <elise.ayoub@gmail.com>, 2016-09-26
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Non c'est encore une fois ta décisions. Je ne vivrais pas au gré de tes jeux et manipulations si tes enfants ne sont pas importants c'est ta perte et ton choix.
- **titre du Cn** — la demanderesse réitère (email-316, 15 h 18) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **322** — « Re: dimanche prochain », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-26

#### V062 · `piece_thread-5_email-5.md` **C1**
*le défendeur annonce la transition vers une semaine sur deux (email-322, 15 h 02)*

- **source** — `Email` **322** — « Re: dimanche prochain », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-26
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > J'ai dis que je faisais une transition vers une semaine sur 2
- **titre du Cn** — le défendeur annonce la transition vers une semaine sur deux (email-322, 15 h 02) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **343** — « Re: Baptême de Nicolas », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-07-19

#### V065 · `piece_thread-76_email-343.md` **C1**
*Le père n'a pas été invité et ignorait le baptême (contemporain)*

- **source** — `Email` **343** — « Re: Baptême de Nicolas », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-07-19
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Moi j'y vais pas, j'ai pas été invité et en fait je savais pas qu'elle le faisait baptiser…. » (19 juil. 2015)
- **titre du Cn** — Le père n'a pas été invité et ignorait le baptême (contemporain) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **347** — « (sans objet) », Louis Philippe David <louisphilippe.david@gmail.com>, 2012-03-06

#### V067 · `piece_thread-78_email-347.md` **C2**
*LP offre de prendre Alexia en charge*

- **source** — `Email` **347** — « (sans objet) », Louis Philippe David <louisphilippe.david@gmail.com>, 2012-03-06
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Je t'ai ecris que je partais tot, je t'ai offert, avec beinveillance et bonne volonté, de m'occuper d'alexia pour que tu puisse partir du travail plus tard pour que tu puisse egalement partir de la maison plus tard
- **titre du Cn** — LP offre de prendre Alexia en charge — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **349** — « Re: », louis philippe david <louisphilippe.david@icloud.com>, 2013-06-30

#### V068 · `piece_thread-109.md` **C8**
*email-349 (LP) — maintien de l'objectif et offre de thérapie*

- **source** — `Email` **349** — « Re: », louis philippe david <louisphilippe.david@icloud.com>, 2013-06-30
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Tout ce que je veux c est de pouvoir aller passer des fds au chalet avec » ; « avec toi nous pouvons aller en therapie. Je suis pret a recomencer le processus
- **titre du Cn** — email-349 (LP) — maintien de l'objectif et offre de thérapie — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **365** — « Conseils », Louis Philippe David <louisphilippe.david@gmail.com>, 2013-06-26

#### V069 · `piece_thread-89_email-365.md` **C2**
*Récurrence : déjà la même situation en 2011*

- **source** — `Email` **365** — « Conseils », Louis Philippe David <louisphilippe.david@gmail.com>, 2013-06-26
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Nous nous sommes parlé il y a 2 ans de ça dans le cadre de ma séparation […]. 2 ans plus tard, je vous recontacte, dans la même situation avec la même conjointe.
- **titre du Cn** — Récurrence : déjà la même situation en 2011 — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **369** — « Fwd: Éléments à imprimer », Louis Philippe David <louisphilippe.david@gmail.com>, 2013-03-06

#### V070 · `piece_thread-91_emails-369-370.md` **C2**
*La réponse de Johanne confirme seulement l'impression*

- **source** — `Email` **369** — « Fwd: Éléments à imprimer », Louis Philippe David <louisphilippe.david@gmail.com>, 2013-03-06
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Fait -sur la chaise dans l'entrée
- **titre du Cn** — La réponse de Johanne confirme seulement l'impression — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **399** — « Re: Ayoub c. David », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-04-27

#### V071 · `piece_thread-100_email-399.md` **C1**
*Le défendeur maintient les accès en reprenant le critère de la routine posé par Me Ayoub*

- **source** — `Email` **399** — « Re: Ayoub c. David », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-04-27
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Dans le but de ne pas changer la routine établie des enfants, nous garderons alors les droits d'accès tels qu'ils sont.
- **titre du Cn** — Le défendeur maintient les accès en reprenant le critère de la routine posé par Me Ayoub — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **443** — « Re:  », louis philippe david <louisphilippe.david@icloud.com>, 2013-06-30

#### V072 · `piece_thread-109.md` **C1**
*email-443 (LP) — contradiction interne de la thèse sécuritaire*

- **source** — `Email` **443** — « Re:  », louis philippe david <louisphilippe.david@icloud.com>, 2013-06-30
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Quand tu as accouché de Nicolas, pourquoi n'as-tu pas demander a ta mere ou ta soeure d'aller dormir avec Alexia? Si tu as si peur pour sa securité, poirquoi m as tu laisser passer 2 nuits avec elle?
- **titre du Cn** — email-443 (LP) — contradiction interne de la thèse sécuritaire — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **444** — « Re: », Élise Ayoub <elise.ayoub@gmail.com>, 2013-06-30

#### V073 · `piece_thread-109.md` **C2**
*email-444 (Élise) — ligne de démarcation = nuit hors du domicile*

- **source** — `Email` **444** — « Re: », Élise Ayoub <elise.ayoub@gmail.com>, 2013-06-30
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Je l'ai fait...mais a la maison dans sa sécurité c'était au moins rassurant » (suivi de : « mais quand j'ai su qu'elle c'était pissé dessus… »)
- **titre du Cn** — email-444 (Élise) — ligne de démarcation = nuit hors du domicile — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V074 · `piece_thread-109.md` **C3**
*email-444 (Élise) — registre « danger venant du père » (allégation structurelle)*

- **source** — `Email` **444** — « Re: », Élise Ayoub <elise.ayoub@gmail.com>, 2013-06-30
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Tu m'as fais sentir des choses en 11 ans par ta façon d'agir que jamais je ne m'étais faire faire par personne et je te voir le faire a Alexia
- **titre du Cn** — email-444 (Élise) — registre « danger venant du père » (allégation structurelle) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **446** — « Re: », Élise Ayoub <elise.ayoub@gmail.com>, 2013-06-30

#### V075 · `piece_thread-109.md` **C4**
*email-446 (Élise) — « tu préfères toujours le désaccord » (binaire chicane / concilier)*

- **source** — `Email` **446** — « Re: », Élise Ayoub <elise.ayoub@gmail.com>, 2013-06-30
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Alors tu prends encore le chemin de la chicane… tu veux jamais réconcilier tu préfères toujours le désaccord
- **titre du Cn** — email-446 (Élise) — « tu préfères toujours le désaccord » (binaire chicane / concilier) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **447** — « Re: », louis philippe david <louisphilippe.david@icloud.com>, 2013-06-30

#### V076 · `piece_thread-109.md` **C5**
*email-447 (LP) — la structure hiérarchique énoncée par LP*

- **source** — `Email` **447** — « Re: », louis philippe david <louisphilippe.david@icloud.com>, 2013-06-30
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > tu va pouvoir faire les choses que tu veux faire avec ta fille quand je vais etre en confiance que tu vas etre en mesure de repondre a ses besoins » ; « Tu me juge comme inadequat comme parent
- **titre du Cn** — email-447 (LP) — la structure hiérarchique énoncée par LP — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **448** — « Re: », Élise  <elise.ayoub@gmail.com>, 2013-06-30

#### V077 · `piece_thread-109.md` **C6**
*email-448 (Élise) — « les deux chemins le même résultat avec Alexia juste pas avec moi »*

- **source** — `Email` **448** — « Re: », Élise  <elise.ayoub@gmail.com>, 2013-06-30
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > je sais que tu n'es pas d'accord avec moi […] tout dépend de ton objectif final et de […] ce que tu es prêt a sacrifier. Mais encore une fois, les deux chemins le même résultat avec Alexia juste pas avec moi!
- **titre du Cn** — email-448 (Élise) — « les deux chemins le même résultat avec Alexia juste pas avec moi » — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V078 · `piece_thread-109.md` **C7**
*email-448 (Élise) — refus du chalet ; alternatives toujours « tous ensemble »*

- **source** — `Email` **448** — « Re: », Élise  <elise.ayoub@gmail.com>, 2013-06-30
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Le chalet a tes parents me dégoute » ; « si tu veux on peut aller la tout le monde ensemble! » (Groupon Tremblant, Jay Peak, billets ferme)
- **titre du Cn** — email-448 (Élise) — refus du chalet ; alternatives toujours « tous ensemble » — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **453** — « Fin d'emplois », "David, Louis-Philippe" <Louis-Philippe.David@bnc.ca>, 2018-06-06

#### V079 · `piece_thread-111_congediement_bnc.md` **C1**
*Constat patronal : LP ne répond pas aux attentes de son poste (de l'Étoile, 8 juin 2018)*

- **source** — `Email` **453** — « Fin d'emplois », "David, Louis-Philippe" <Louis-Philippe.David@bnc.ca>, 2018-06-06
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > la période de relocalisation est un choix qui vous a été offert comme option alternative au plan d'accompagnement qui a été débuté suite au constat que vous ne répondez malheureusement pas aux attentes de votre poste. […] Si vous refusez la relocalisation et décidez de rester dans votre poste, nous poursuivrons la démarche du plan d'accompagnement qui risque de se terminer en congédiement si votre performance n'est pas au rendez-vous. » (id=455/456)
- **titre du Cn** — Constat patronal : LP ne répond pas aux attentes de son poste (de l'Étoile, 8 juin 2018) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V081 · `piece_thread-111_congediement_bnc.md` **C3**
*LP : le départ est INVOLONTAIRE (refus de fausse qualification, en temps réel)*

- **source** — `Email` **453** — « Fin d'emplois », "David, Louis-Philippe" <Louis-Philippe.David@bnc.ca>, 2018-06-06
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Je n'ai jamais manifesté ma volonté de quitter mon emploi, c'est la Banque qui a manifesté sa volonté de mettre fin à mon emploi. » (id=454) « ces 2 semaines à la maison sont conditionnelles à ce que je signe un document qui affirme que j'ai quitté volontairement mon poste, malgré qu'il ne s'agisse pas d'un départ volontaire […] je me retrouve dans l'impossibilité de signer […]. » (id=455) « mon congédiement ne découle d'aucune faute grave, mais d'une insatisfaction face à mon rendement » (id=455)
- **titre du Cn** — LP : le départ est INVOLONTAIRE (refus de fausse qualification, en temps réel) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **463** — « Re: Salut », "Marie-Josée Ayoub" <mjayoub@ayoubavocats.ca>, 2020-02-18

#### V083 · `piece_thread-113_email-462.md` **C2**
*Me Ayoub reconnaît un projet de départ pour travailler, soutenu depuis ~18 mois*

- **source** — `Email` **463** — « Re: Salut », "Marie-Josée Ayoub" <mjayoub@ayoubavocats.ca>, 2020-02-18
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Peux-tu me dire quelle est ta date de départ prévue ? » (email-463) « cela fait presque 1 an et demi que tu nous affirmes que tu es sur le point de quitter le pays et que tu ne travailles pas entre temps. […] As-tu les visas pour partir? As-tu fais le nécessaire pour sous-louer ton logement? Es-tu sur l'aide sociale? » (email-463/465/467, 18 févr. 2020)
- **titre du Cn** — Me Ayoub reconnaît un projet de départ pour travailler, soutenu depuis ~18 mois — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **475** — « lettre de Marie Josee », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-05-15

#### V086 · `piece_thread-116_email-475.md` **C1**
*Possession et transmission de P-2 pendant les négociations de garde*

- **source** — `Email` **475** — « lettre de Marie Josee », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-05-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Je te joins le courriel de Marie-Josée concernant l'épisode de violence conjugale.
- **titre du Cn** — Possession et transmission de P-2 pendant les négociations de garde — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V087 · `piece_thread-116_email-475.md` **C3**
*Cause contemporaine d'un éventuel recours au Tribunal*

- **source** — `Email` **475** — « lettre de Marie Josee », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-05-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Si elle n'accepte pas et qu'elle demande une pension différente de si j'avais 30% de la garde, je n'ai pas d'autre option que de regeler en cour.
- **titre du Cn** — Cause contemporaine d'un éventuel recours au Tribunal — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **485** — « Frais médicaux impayé (point 7) », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-10-21

#### V090 · `piece_thread-120_email-485.md` **C1**
*demande explicite de la preuve des « demandes répétées »*

- **source** — `Email` **485** — « Frais médicaux impayé (point 7) », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-10-21
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > As-tu des preuves qu'Élise m'a fait des demandes répétées à l'effet qu'il y ait des frais médicaux à rembourser ?
- **titre du Cn** — demande explicite de la preuve des « demandes répétées » — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V091 · `piece_thread-120_email-485.md` **C2**
*aucune communication depuis le 26 sept. 2016*

- **source** — `Email` **485** — « Frais médicaux impayé (point 7) », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-10-21
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > un courriel d'Élise qui date du 26 septembre 2016 qui me demandait de ne plus lui écrire […] nous n'avons eu aucune communication depuis.
- **titre du Cn** — aucune communication depuis le 26 sept. 2016 — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **486** — « refus de prendre les enfants les jours de congé (point 6.C) », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-10-21

#### V092 · `piece_thread-121_email-486.md` **C1**
*l'inversion : le défendeur demandait, la demanderesse refusait*

- **source** — `Email` **486** — « refus de prendre les enfants les jours de congé (point 6.C) », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-10-21
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > durant les 5 années […] malgrés des demandes répétées Elle n'a jamais accepté que je prenne les enfants ne serais-ce que pour passer une nuit au chalet même avec mes parents
- **titre du Cn** — l'inversion : le défendeur demandait, la demanderesse refusait — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V093 · `piece_thread-121_email-486.md` **C2**
*pas d'offre à refuser (on ne refuse pas ce qui n'a pas été proposé)*

- **source** — `Email` **486** — « refus de prendre les enfants les jours de congé (point 6.C) », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-10-21
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Je ne penses pas qu'Élise m'ait une seule fois offert […] contenu du fait qu'elle m'a demandé de ne plus lui écrire en date du 26 septembre 2016. À mon souvenir, je n'ai rien refusé.
- **titre du Cn** — pas d'offre à refuser (on ne refuse pas ce qui n'a pas été proposé) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **590** — « Re: souper », Louis Philippe David <louisphilippe.david@gmail.com>, 2010-01-26

#### V098 · `piece_emails_petite_enfance_2010.md` **C1**
*Le demandeur assure les soins d'Alexia malade (Alexia ~3,5 mois)*

- **source** — `Email` **590** — « Re: souper », Louis Philippe David <louisphilippe.david@gmail.com>, 2010-01-26
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Non la petite est tres malade. Nous allons rester tranquil ce soir !
- **titre du Cn** — Le demandeur assure les soins d'Alexia malade (Alexia ~3,5 mois) — ⚠️ *aucun champ dans le modèle courriel*
- **attribution retirée du texte** — LP → Johanne, 26 janvier 2010 (Email id=590)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **601** — « Alexia », Johanne BAZINET <johannebazinet@gmail.com>, 2010-08-23

#### V099 · `piece_emails_petite_enfance_2010.md` **C2**
*Arrangement hebdomadaire : le demandeur reste à la maison une journée de semaine*

- **source** — `Email` **601** — « Alexia », Johanne BAZINET <johannebazinet@gmail.com>, 2010-08-23
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Je sais que je dois garder le vendredi - tu dois également rester à la maison une journée de la semaine. Si je ne pouvais pas le 1er octobre, est-ce que tu pourrais changer ta journée avec la mienne…
- **titre du Cn** — Arrangement hebdomadaire : le demandeur reste à la maison une journée de semaine — ⚠️ *aucun champ dans le modèle courriel*
- **attribution retirée du texte** — Johanne → LP, 23 août 2010 (Email id=601)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **603** — « Re: 15 nov. », Louis Philippe David <louisphilippe.david@gmail.com>, 2010-11-08

#### V100 · `piece_emails_petite_enfance_2010.md` **C3**
*Le demandeur prend le mercredi*

- **source** — `Email` **603** — « Re: 15 nov. », Louis Philippe David <louisphilippe.david@gmail.com>, 2010-11-08
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Partiellement c est le 8-15 et 22 novembre, elise reste à la maison et je moi je prends le mercredi !!!
- **titre du Cn** — Le demandeur prend le mercredi — ⚠️ *aucun champ dans le modèle courriel*
- **attribution retirée du texte** — LP → Johanne, 8 novembre 2010 (Email id=603)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **615** — « Re: demandes d'emplois », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-10-15

#### V102 · `piece_thread-156_email-615.md` **C2**
*demande des états financiers de l'OSBL d'Élise*

- **source** — `Email` **615** — « Re: demandes d'emplois », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-10-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Élise était propriétaire d'une OSBL […] inclus dans les calculs de l'annexe
- **titre du Cn** — demande des états financiers de l'OSBL d'Élise — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V103 · `piece_thread-156_email-615.md` **C3**
*la réponse de Me Ayoub : « toujours en attente » (déflexion, non critique de fond)*

- **source** — `Email` **615** — « Re: demandes d'emplois », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-10-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > nous sommes toujours en attente de vos preuves de demande d'emplois
- **titre du Cn** — la réponse de Me Ayoub : « toujours en attente » (déflexion, non critique de fond) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **617** — « Re: es tu revenu? », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-11-04

#### V104 · `piece_thread-157_email-617.md` **C1**
*le père vit l'attribution de revenu comme IMPOSÉE par le juge*

- **source** — `Email` **617** — « Re: es tu revenu? », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-11-04
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > le juge m'a attribué un salaire de 65k
- **titre du Cn** — le père vit l'attribution de revenu comme IMPOSÉE par le juge — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V105 · `piece_thread-157_email-617.md` **C2**
*l'imputation bloque le projet d'emploi (Roumanie/Allianz)*

- **source** — `Email` **617** — « Re: es tu revenu? », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-11-04
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > je ne pourrai probablement pas aller en Roumanie » ; « la pension va etre trop elevée
- **titre du Cn** — l'imputation bloque le projet d'emploi (Roumanie/Allianz) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **631** — « Re: certificat », Louis Philippe David <louisphilippe.david@gmail.com>, 2026-06-19

#### V106 · `piece_thread-158_email-633.md` **C1**
*Demande de confirmation (LP → Paroisse, 19 juin / 2 juillet 2026)*

- **source** — `Email` **631** — « Re: certificat », Louis Philippe David <louisphilippe.david@gmail.com>, 2026-06-19
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > je constate qu'une information dont j'ai besoin n'y figure pas : le nom de la marraine. Seriez-vous en mesure de retrouver cette information et de me la confirmer ? Dans mes souvenirs, il s'agit de Marie-Josée Ayoub, mais je souhaiterais en avoir la confirmation officielle. » (email-631, 19 juin 2026 ; relancé email-632, 2 juillet 2026)
- **titre du Cn** — Demande de confirmation (LP → Paroisse, 19 juin / 2 juillet 2026) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **633** — « Re: certificat », "Paroisse Saint Lambert Saint Thomas d'Aquin" <paroisse.slstda@gmail.com>, 2026-07-02

#### V107 · `piece_thread-158_email-633.md` **C2**
*Confirmation officielle de la Paroisse (Paroisse → LP, 2 juillet 2026)*

- **source** — `Email` **633** — « Re: certificat », "Paroisse Saint Lambert Saint Thomas d'Aquin" <paroisse.slstda@gmail.com>, 2026-07-02
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Après vérification dans nos registres, je vous confirme que la marraine inscrite au registre de baptême de votre fils est bien Marie-Josée Ayoub. » (email-633 ; signé Carole-Anne Lodoiska, secrétaire comptable, Paroisse Saint-Lambert-Saint-Thomas-d'Aquin, 450-671-5721)
- **titre du Cn** — Confirmation officielle de la Paroisse (Paroisse → LP, 2 juillet 2026) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **634** — « Liste des coach a l’été 2013 », Louis Philippe David <louisphilippe.david@gmail.com>, 2026-07-02

#### V108 · `piece_thread-159_emails-634-641.md` **C1**
*Demande visant expressément Élise et l'été 2013 ou 2014*

- **source** — `Email` **634** — « Liste des coach a l’été 2013 », Louis Philippe David <louisphilippe.david@gmail.com>, 2026-07-02
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Serait-il possible d'obtenir la liste des entraîneurs qui ont œuvré au cours de l'été 2013 ? Plus précisément, j'aimerais vérifier si c'est à l'été 2013 ou 2014 qu'Élise Ayoub a agi à titre d'entraîneuse au sein de votre organisation.
- **titre du Cn** — Demande visant expressément Élise et l'été 2013 ou 2014 — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **635** — « Fwd: Liste des coach a l’été 2013 », Gilles Lewis <appariteur@assl.ca>, 2026-07-02

#### V109 · `piece_thread-159_emails-634-641.md` **C2**
*Les données anciennes ne se trouvent pas dans le système courant*

- **source** — `Email` **635** — « Fwd: Liste des coach a l’été 2013 », Gilles Lewis <appariteur@assl.ca>, 2026-07-02
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Présentement, le système SPORDLE dont le début en 2018 ne me permet pas d'avoir cette information. Il se peut que les archives de l'ancien système (PTS-Registrariat) nous permettent d'obtenir l'information
- **titre du Cn** — Les données anciennes ne se trouvent pas dans le système courant — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **640** — « Re: Liste des coach a l’été 2013 », Jean-Pierre Gignac <do@assl.ca>, 2026-07-02

#### V110 · `piece_thread-159_emails-634-641.md` **C3**
*Le directeur général confirme que l'information a été récupérée*

- **source** — `Email` **640** — « Re: Liste des coach a l’été 2013 », Jean-Pierre Gignac <do@assl.ca>, 2026-07-02
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Je confirme qu'on récupéré cette information, mais pour que je la donne, il me faudrait plus d'informations.
- **titre du Cn** — Le directeur général confirme que l'information a été récupérée — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **645** — « 2023-07-25 Demande de transfert de district judicaire », "Luneedka Lili Philémon" <lphilemon@ccjm.qc.ca>, 2023-07-25

#### V115 · `piece_courriel_philemon_2023-07-25.md` **C1**
*Connaissance de P-40 le 25 juillet 2023 (dies a quo)*

- **source** — `Email` **645** — « 2023-07-25 Demande de transfert de district judicaire », "Luneedka Lili Philémon" <lphilemon@ccjm.qc.ca>, 2023-07-25
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Nous avons reçu ce document dans votre dossier. C'est une demande de la partie adverse afin de transférer le dossier au district de Longueuil.
- **titre du Cn** — Connaissance de P-40 le 25 juillet 2023 (dies a quo) — ⚠️ *aucun champ dans le modèle courriel*
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **1** — Courriel suggérant de faire une plainte pour violence conjugale (`20130611_MJ_Courriel_violence_conjugale.pdf`)

#### V116 · `piece_pdf-1.md` **C7**
*Calendrier : signifier la procédure avant le départ de LP (« une pierre deux coups »)*

- **source** — `PDFDocument` **1** — Courriel suggérant de faire une plainte pour violence conjugale (`20130611_MJ_Courriel_violence_conjugale.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > le meilleur moment pour lui envoyer la procédure est jeudi pour qu'on aille à la cour vendredi avant son départ. » C7.2 — « Une pierre deux coups. La procédure et tu lui gâche ses vacances comme il te le fait toujours.
- **page_number** — 1
- **quote_location_details** — Calendrier : signifier la procédure avant le départ de LP (« une pierre deux coups »)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V118 · `piece_pdf-1.md` **C12**
*La demande du père, consignée par l'adverse : l'alternance*

- **source** — `PDFDocument` **1** — Courriel suggérant de faire une plainte pour violence conjugale (`20130611_MJ_Courriel_violence_conjugale.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Il veut avoir une coupure avec toi et avoir les enfants une semaine sur deux. » ⚠️ Fragment retiré — ne pas le réintroduire. C12 comportait un second fragment : « Malgré son mépris pour toi sa vie ne change pas […] et voit ses enfants quand il veut ». Il a été retiré parce qu'il ne porte aucune information utile : « quand il veut » fixe une modalité — l'accès était à sa discrétion, personne ne le bloquait — et aucun quantum. Une heure par mois et vingt-quatre heures par jour satisfont également l'énoncé ; il ne réfute donc pas « rarement disponible », qui porte sur la disponibilité et non sur la permission. L'ampleur de la présence paternelle se démontre par la co-résidence que les prescriptions présupposent (C6.1, C5, C15) et par le volume documenté, jamais par cette phrase. Elle demeure à la transcription ¶ 5.
- **page_number** — 1
- **quote_location_details** — La demande du père, consignée par l'adverse : l'alternance
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V119 · `piece_pdf-1.md` **C13**
*La prescription de soin : sa fonction est nommée par le document, et ce n'est pas le soin de l'enfant*

- **source** — `PDFDocument` **1** — Courriel suggérant de faire une plainte pour violence conjugale (`20130611_MJ_Courriel_violence_conjugale.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > La première chose que tu dois faire c'est d'aller consulter un psychologue afin qu'il t'accompagne dans ta démarche. cela est NÉCESSAIRE!
- **page_number** — 1
- **quote_location_details** — La prescription de soin : sa fonction est nommée par le document, et ce n'est pas le soin de l'enfant
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **2** — 20150420 FP premiere offre de garde (envois de la position officielle) (`20150304_FP_premiere_offre.pdf`)

#### V120 · `piece_pdf-2.md` **C1**
*Offre de garde partagée 2-2-3, sans contre-indication*

- **source** — `PDFDocument` **2** — 20150420 FP premiere offre de garde (envois de la position officielle) (`20150304_FP_premiere_offre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > nous ne voyons aucune contre-indication à l'établissement d'une garde partagée […] afin de favoriser un contact optimal entre l'enfant et les deux (2) parents
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Offre de garde partagée 2-2-3, sans contre-indication
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **3** — Réponse à l'offre de garde partagée (`20150427_MJ_reponse_a_premiere_offre.pdf`)

#### V121 · `piece_pdf-3.md` **C1**
*Aveu du conflit d'intérêt*

- **source** — `PDFDocument` **3** — Réponse à l'offre de garde partagée (`20150427_MJ_reponse_a_premiere_offre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > a) Le fait que madame est notre sœur et que nous serions possiblement en conflit d'intérêt advenant que la cause soit contestée ;
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Aveu du conflit d'intérêt
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V122 · `piece_pdf-3.md` **C3**
*Offre d'accès incluant des nuitées (incompatible avec un père dangereux ou incompétent)*

- **source** — `PDFDocument` **3** — Réponse à l'offre de garde partagée (`20150427_MJ_reponse_a_premiere_offre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Semaine 1 : Du mercredi après la garderie et ce jusqu'au jeudi matin à la garderie ; Du samedi 14h00 au dimanche 16h00. Semaine 2 : Du mercredi après la garderie […] jusqu'au jeudi matin ; Dimanche de 15h00 à 20h00.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Offre d'accès incluant des nuitées (incompatible avec un père dangereux ou incompétent)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V123 · `piece_pdf-3.md` **C4**
*L'« entente » sur la garde exclusive datée du 13 février 2015 — AVANT la séparation du 23 février*

- **source** — `PDFDocument` **3** — Réponse à l'offre de garde partagée (`20150427_MJ_reponse_a_premiere_offre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > […] notre seul entretien téléphonique le ou vers le 13 février 2015. Lors de notre dite conversation, nous avons traité des sujets suivants : Le consentement entre les parties à l'effet que les enfants soient en garde exclusive chez la mère et les droits d'accès du père d'une fin de semaine sur deux […] » « Vous n'êtes pas sans savoir que monsieur David a quitté la résidence de notre cliente le ou vers le 23 février 2015 […] » « Nous comprenons mal les intentions de votre client à vouloir modifier une entente déjà intervenue entre les parties.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — L'« entente » sur la garde exclusive datée du 13 février 2015 — AVANT la séparation du 23 février
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V124 · `piece_pdf-3.md` **C5**
*Source de §23 (refus de recevoir les enfants à l'appartement)*

- **source** — `PDFDocument` **3** — Réponse à l'offre de garde partagée (`20150427_MJ_reponse_a_premiere_offre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Bien que notre cliente ait à plusieurs reprises offert au vôtre de prendre les enfants sur une base plus régulière qu'une fin de semaine sur deux votre client a refusé et refuse toujours de les recevoir à son nouvel appartement.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Source de §23 (refus de recevoir les enfants à l'appartement)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V125 · `piece_pdf-3.md` **C6**
*Ouverture de la lettre et rattachement à l'entretien du 13 février*

- **source** — `PDFDocument` **3** — Réponse à l'offre de garde partagée (`20150427_MJ_reponse_a_premiere_offre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > La présente fait suite à votre missive datée du 20 avril dernier eu égard au dossier mentionné en exergue et à notre seul entretien téléphonique le ou vers le 13 février 2015, Lors de notre dite conversation, nous avons traité des sujets suivants : Le consentement entre les parties à l'effet que les enfants soient en garde exclusive chez la mère et les droits d'accès du père d'une fin de semaine sur deux;
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Ouverture de la lettre et rattachement à l'entretien du 13 février
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V126 · `piece_pdf-3.md` **C7**
*La formule d'introduction de l'offre*

- **source** — `PDFDocument` **3** — Réponse à l'offre de garde partagée (`20150427_MJ_reponse_a_premiere_offre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > notre cliente réitère son offre à l'élargissement des droits d'accès du père auprès de leurs enfants à savoir :
- **page_number** — ⚠️ à préciser
- **quote_location_details** — La formule d'introduction de l'offre
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V127 · `piece_pdf-3.md` **C8**
*Élise reçoit directement la position communiquée en son nom*

- **source** — `PDFDocument` **3** — Réponse à l'offre de garde partagée (`20150427_MJ_reponse_a_premiere_offre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > c.c. : Madame Élise Ayoub
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Élise reçoit directement la position communiquée en son nom
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **5** — 20150813 MJ projet consentement (`20150813_MJ_projet_consentement.pdf`)

#### V129 · `piece_pdf-5.md` **C2**
*Art. 3 : « puisque le père refuse de prendre les décisions importantes »*

- **source** — `PDFDocument` **5** — 20150813 MJ projet consentement (`20150813_MJ_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Toutefois, puisque le père refuse de prendre les décisions importantes […] il consent à ce que la mère prenne seule toutes les décisions […].
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Art. 3 : « puisque le père refuse de prendre les décisions importantes »
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V130 · `piece_pdf-5.md` **C3**
*Art. 7 : accès progressif AVEC nuitées en semaine dès la phase a)*

- **source** — `PDFDocument` **5** — 20150813 MJ projet consentement (`20150813_MJ_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Dimanche 16h00 à Mardi matin directement à l'école […] modifier une routine établie
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Art. 7 : accès progressif AVEC nuitées en semaine dès la phase a)
- **attribution retirée du texte** — Dès la phase a), introduite par les mots « À compter de ce jour jusqu'au 28 août 2016 »
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V131 · `piece_pdf-5.md` **C4**
*Art. 17 : assurances « comme ils l'ont toujours été »*

- **source** — `PDFDocument` **5** — 20150813 MJ projet consentement (`20150813_MJ_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > les enfants continueront d'être couverts par les assurances du demandeur comme ils l'ont toujours été » — reconnaît la couverture par LP. Pertinent §56-58 (allegation_stmt56_57_58_assurances.md).
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Art. 17 : assurances « comme ils l'ont toujours été »
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V132 · `piece_pdf-5.md` **C5**
*Art. 4 : voyage à l'étranger sans consentement préalable de LP (non signé)*

- **source** — `PDFDocument` **5** — 20150813 MJ projet consentement (`20150813_MJ_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > le père consent à ce que la mère voyage à l'étranger avec les enfants sans son consentement au préalable » — clause jamais signée. Préfigure §42/§64 de la Requête.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Art. 4 : voyage à l'étranger sans consentement préalable de LP (non signé)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V133 · `piece_pdf-5.md` **C6**
*Art. 21 : validité conditionnée à la signature des deux*

- **source** — `PDFDocument` **5** — 20150813 MJ projet consentement (`20150813_MJ_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > valide uniquement lorsque les parties l'auront signés ; une seule signature ne pourra être opposée à celui qui l'aura signée » — rend l'art. 3 (« le père refuse ») inopposable au défendeur, qui n'a jamais signé.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Art. 21 : validité conditionnée à la signature des deux
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V134 · `piece_pdf-5.md` **C7**
*Art. 5 : « liens préservés et renforcés » / « ne pas diminuer l'affection » ⊥ le plan de 2013*

- **source** — `PDFDocument` **5** — 20150813 MJ projet consentement (`20150813_MJ_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > […] que les liens existants entre les enfants et chacune des parties soient préservés et renforcés ; […] aucune des parties ne tentera de diminuer l'affection des enfants pour l'autre […].
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Art. 5 : « liens préservés et renforcés » / « ne pas diminuer l'affection » ⊥ le plan de 2013
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V135 · `piece_pdf-5.md` **C9**
*Art. 5, texte intégral (l'élision portait sur une obligation positive)*

- **source** — `PDFDocument` **5** — 20150813 MJ projet consentement (`20150813_MJ_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Les parties reconnaissent qu'il est dans le meilleur intérêt des enfants que ceux-ci continuent à avoir accès auprès de leurs parents malgré leur séparation et que les liens existants entre les enfants et chacune des parties soient préservés et renforcés; aucune des parties ne tentera de diminuer l'affection des enfants pour l'autre, mais au contraire, encouragera son développement;
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Art. 5, texte intégral (l'élision portait sur une obligation positive)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V136 · `piece_pdf-5.md` **C10**
*Art. 11, texte intégral*

- **source** — `PDFDocument` **5** — 20150813 MJ projet consentement (`20150813_MJ_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Si le père ne désire pas exercer ses droits d'accès prévus audit consentement auprès des enfants sur une base régulière, la pension alimentaire pour enfants sera majoré de 20%.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Art. 11, texte intégral
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **6** — 20150902 FP réponse projet consentement (`20150902_FP_réponse_projet_consentement.pdf`)

#### V137 · `piece_pdf-6.md` **C1**
*(b) LP exige le RETRAIT de la clause « le père refuse » — il NE consent PAS à ce que la mère prenne « toutes les décisions »*

- **source** — `PDFDocument` **6** — 20150902 FP réponse projet consentement (`20150902_FP_réponse_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > le paragraphe 3 devra être retiré considérant que monsieur David ne consent pas à ce que votre cliente prenne toutes les décisions en ce qui concerne les enfants
- **page_number** — ⚠️ à préciser
- **quote_location_details** — (b) LP exige le RETRAIT de la clause « le père refuse » — il NE consent PAS à ce que la mère prenne « toutes les décisions »
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V138 · `piece_pdf-6.md` **C2**
*(c) Consentement au voyage : réciproque, non unilatéral*

- **source** — `PDFDocument` **6** — 20150902 FP réponse projet consentement (`20150902_FP_réponse_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > le paragraphe 4 devra être reformulé afin que les deux parents consentent et s'autorisent mutuellement […] » — LP refuse la clause unilatérale (mère voyage sans son consentement) et demande la réciprocité. Pertinent §42/§64.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — (c) Consentement au voyage : réciproque, non unilatéral
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V139 · `piece_pdf-6.md` **C3**
*(d, g) LP demande une garde partagée 2-2-3 dès le 7 février 2016 + accommode la danse d'Élise*

- **source** — `PDFDocument` **6** — 20150902 FP réponse projet consentement (`20150902_FP_réponse_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > à compter du 7 février 2016 l'horaire de garde sera en alternance 2-2-3/2-2-3 » ; « disposé à laisser votre cliente choisir afin que l'horaire […] prenne en considération ses cours de danse » ; « les modalités de garde qui établiront éventuellement la garde partagée ». La garde partagée est l'objectif explicite de LP. Renvoi §14-17 Axe 2 (2ᵉ offre).
- **page_number** — ⚠️ à préciser
- **quote_location_details** — (d, g) LP demande une garde partagée 2-2-3 dès le 7 février 2016 + accommode la danse d'Élise
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **7** — Réponse finale à l'offre d'une progression vers une garde partagée (`20150903_MJ_reponse_a_reponse_du_projet_de_consentement.PDF`)

#### V140 · `piece_pdf-7.md` **C1**
*L'art. 3 (« le père refuse ») dit ajouté À LA DEMANDE de LP*

- **source** — `PDFDocument` **7** — Réponse finale à l'offre d'une progression vers une garde partagée (`20150903_MJ_reponse_a_reponse_du_projet_de_consentement.PDF`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > le paragraphe 3 de notre consentement a été ajouté à la demande de votre client. Effectivement, monsieur David indique spécifiquement […] qu'il ne désire pas être impliqué dans aucune décision impliquant les enfants
- **page_number** — ⚠️ à préciser
- **quote_location_details** — L'art. 3 (« le père refuse ») dit ajouté À LA DEMANDE de LP
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V141 · `piece_pdf-7.md` **C2**
*La consultation conjointe était OFFERTE (aucune objection)*

- **source** — `PDFDocument` **7** — Réponse finale à l'offre d'une progression vers une garde partagée (`20150903_MJ_reponse_a_reponse_du_projet_de_consentement.PDF`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Si son désir réel est d'être impliqué dans les décisions concernant les enfants […] nous n'avons absolument aucune objection à modifier l'entente en conséquence puisqu'il en est de l'intérêt des enfants que les parties puissent décider ensemble des décisions importantes
- **page_number** — ⚠️ à préciser
- **quote_location_details** — La consultation conjointe était OFFERTE (aucune objection)
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V142 · `piece_pdf-7.md` **C3**
*Refus de la garde partagée de février 2016 : « prématuré »*

- **source** — `PDFDocument` **7** — Réponse finale à l'offre d'une progression vers une garde partagée (`20150903_MJ_reponse_a_reponse_du_projet_de_consentement.PDF`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > notre cliente considère qu'il est prématuré à ce stade-ci d'entrevoir l'aménagement d'une garde partagée dès février 2016
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Refus de la garde partagée de février 2016 : « prématuré »
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **8** — Commission spéciale sur les droits des enfants et la protection de la jeunesse (`Mémoire_Barreau_-_Commission_Laurent_VF_2019-11-22.pdf`)

#### V144 · `piece_pdf-8.md` **C1**
*Rareté des ressources DPJ (p. 9)*

- **source** — `PDFDocument` **8** — Commission spéciale sur les droits des enfants et la protection de la jeunesse (`Mémoire_Barreau_-_Commission_Laurent_VF_2019-11-22.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > sur le terrain, nous constatons trop souvent une absence de ressources ou des disparités régionales extrêmement importantes et préoccupantes, lesquelles sont exacerbées en milieu autochtone.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Rareté des ressources DPJ (p. 9)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V145 · `piece_pdf-8.md` **C2**
*Obligation du DPJ de soumettre un portrait complet et objectif = devoir de divulgation type procureur (p. 14)*

- **source** — `PDFDocument` **8** — Commission spéciale sur les droits des enfants et la protection de la jeunesse (`Mémoire_Barreau_-_Commission_Laurent_VF_2019-11-22.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > il nous apparaît important qu'il soit précisé que le DPJ ait l'obligation de soumettre un portrait complet et objectif de l'ensemble de la situation d'un enfant, peu importe ses prétentions. Cette obligation peut s'apparenter à celle d'un procureur aux poursuites criminelles et pénales, lequel est à la recherche de la vérité et ce faisant, a l'obligation de divulguer l'ensemble de sa preuve.
- **page_number** — 9
- **quote_location_details** — Obligation du DPJ de soumettre un portrait complet et objectif = devoir de divulgation type procureur (p. 14)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V146 · `piece_pdf-8.md` **C3**
*Importance du développement et de la stabilité affective de l'enfant (p. 18-19)*

- **source** — `PDFDocument` **8** — Commission spéciale sur les droits des enfants et la protection de la jeunesse (`Mémoire_Barreau_-_Commission_Laurent_VF_2019-11-22.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Souligner l'importance du développement et de la stabilité affective de l'enfant dans la LPJ […] nous suggérons donc qu'un ajout soit fait dans le cadre d'un préambule à la loi indiquant que toute décision qui vise la protection de l'enfant soit analysée sous l'angle du développement et de la stabilité affective de l'enfant.
- **page_number** — 14
- **quote_location_details** — Importance du développement et de la stabilité affective de l'enfant (p. 18-19)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **9** — Projet de loi no 15 — Loi modifiant la Loi sur la protection de la jeunesse et d’autres dispositions législatives (`memoire-pl15.pdf`)

#### V147 · `piece_pdf-9.md` **C1**
*Disponibilité et intensité des ressources comme principe directeur (p. 3, repris p. 40)*

- **source** — `PDFDocument` **9** — Projet de loi no 15 — Loi modifiant la Loi sur la protection de la jeunesse et d’autres dispositions législatives (`memoire-pl15.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le projet de loi ne permet pas d'assurer la constance dans la disponibilité de ressources de qualité — Ériger à titre de principe directeur que le ministère de la Santé et des Services sociaux et le DNPJ doivent s'assurer de la disponibilité et de l'intensité des ressources permettant à la loi d'atteindre ses objectifs en matière de protection de la jeunesse.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Disponibilité et intensité des ressources comme principe directeur (p. 3, repris p. 40)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V148 · `piece_pdf-9.md` **C2**
*Stabilité affective comme angle d'analyse de toute décision (p. 20)*

- **source** — `PDFDocument` **9** — Projet de loi no 15 — Loi modifiant la Loi sur la protection de la jeunesse et d’autres dispositions législatives (`memoire-pl15.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > nous accueillons favorablement l'ajout d'un préambule à la loi qui indique que toute décision qui vise la protection de l'enfant doit être analysée sous l'angle du développement et de la stabilité affective de celui-ci. Cet ajout répond à une demande du Barreau du Québec formulée dans le cadre de sa participation à la Commission Laurent.
- **page_number** — 40
- **quote_location_details** — Stabilité affective comme angle d'analyse de toute décision (p. 20)
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V149 · `piece_pdf-9.md` **C3**
*Persistance de la rareté des ressources (p. 24/30)*

- **source** — `PDFDocument` **9** — Projet de loi no 15 — Loi modifiant la Loi sur la protection de la jeunesse et d’autres dispositions législatives (`memoire-pl15.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > sur le terrain, il est constaté trop souvent une absence de ressources ou des disparités régionales extrêmement importantes et préoccupantes.
- **page_number** — 20
- **quote_location_details** — Persistance de la rareté des ressources (p. 24/30)
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **10** — Projet de loi no 37 — Loi sur le commissaire au bien-être et aux droits des enfants (`memoire-pl37.pdf`)

#### V150 · `piece_pdf-10.md` **C1**
*Insuffisance persistante des ressources + délais (p. 5)*

- **source** — `PDFDocument` **10** — Projet de loi no 37 — Loi sur le commissaire au bien-être et aux droits des enfants (`memoire-pl37.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Depuis plusieurs années, le Barreau du Québec a soulevé l'enjeu important de l'insuffisance, voire d'une absence des ressources de première et de deuxième ligne amplifiée par des disparités régionales importantes ainsi que la situation particulière en milieu autochtone. De plus, il y a encore malheureusement de nombreux délais tant dans le traitement des signalements au niveau judiciaire qu'en matière de protection de la jeunesse qui méritent une attention immédiate.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Insuffisance persistante des ressources + délais (p. 5)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **13** — Jugement sur le fond (perte emplois) (`jugement.pdf`)

#### V153 · `piece_pdf-13.md` **C1**
*Le jugement se présente comme une « entente » SUR LES CONCLUSIONS — récital contredit par les deux parties*

- **source** — `PDFDocument` **13** — Jugement sur le fond (perte emplois) (`jugement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Attendu que les parties, après le début de l'audition, se sont entendues à ce qu'un jugement soit rendu avec les conclusions suivantes […] » (verbatim, page 3)
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Le jugement se présente comme une « entente » SUR LES CONCLUSIONS — récital contredit par les deux parties
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V154 · `piece_pdf-13.md` **C2**
*Le Tribunal interdit à LP d'évoquer l'avant-2016*

- **source** — `PDFDocument` **13** — Jugement sur le fond (perte emplois) (`jugement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le Tribunal informe Monsieur de ne pas parler de ce qui s'est passé avant 2016. » (sur objection de Me Ayoub : « un jugement a été prononcé en 2016 sur ces sujets »)
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Le Tribunal interdit à LP d'évoquer l'avant-2016
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **26** — Modele quebecois fixation pension alimentaire (`Le-modele-quebecois-de-fixation-des-pensions-alimentaires-pour-enfants.pdf`)

#### V167 · `piece_modele_fixation_pension.md` **C1**
*Revenu BRUT, pas net (méthode imposée)*

- **source** — `PDFDocument` **26** — Modele quebecois fixation pension alimentaire (`Le-modele-quebecois-de-fixation-des-pensions-alimentaires-pour-enfants.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Pourquoi le modèle prévoit-il l'utilisation du revenu brut plutôt que du revenu net ? […] la table […] a été construite à partir des revenus bruts. » Revenus inscrits aux lignes 200 à 208 (partie 2). Le revenu annuel inclut « les traitements, salaires […] les prestations d'assurance-emploi et d'assurance parentale […] les autres revenus ».
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Revenu BRUT, pas net (méthode imposée)
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V168 · `piece_modele_fixation_pension.md` **C2**
*Revenu disponible = total − déductions admissibles (liste EXHAUSTIVE)*

- **source** — `PDFDocument` **26** — Modele quebecois fixation pension alimentaire (`Le-modele-quebecois-de-fixation-des-pensions-alimentaires-pour-enfants.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le revenu disponible des parents est obtenu en soustrayant du revenu annuel total de chacun des parents les déductions admissibles, soit la déduction de base […] et, s'il y a lieu, les sommes versées à titre de cotisations syndicales et professionnelles. » (partie 3 du formulaire) → Seules deux déductions admissibles : base + cotisations syndicales/professionnelles. Ni REER, ni RPA, ni déductions fiscales.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Revenu disponible = total − déductions admissibles (liste EXHAUSTIVE)
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V169 · `piece_modele_fixation_pension.md` **C3**
*Revenu de l'ANNÉE COURANTE, ou revenu PRÉVISIBLE des 12 prochains mois (PAS l'année passée)*

- **source** — `PDFDocument` **26** — Modele quebecois fixation pension alimentaire (`Le-modele-quebecois-de-fixation-des-pensions-alimentaires-pour-enfants.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Inscrivez aux lignes 200 à 208 […] les revenus de l'année courante pour chacun des parents. Si les revenus de l'année en cours ne représentent pas adéquatement la situation d'un parent, vous pouvez inscrire les revenus prévisibles pour les 12 prochains mois. Par exemple, […] il vient de cesser de recevoir des prestations d'assurance-emploi […] les revenus à inscrire sont ceux qui sont prévisibles pour les 12 mois qui suivent la présentation de la demande. » « À moins d'une exception, les revenus pris en considération sont ceux de l'année courante. » → Règle : année courante par défaut ; si elle ne représente pas la situation (l'exemple cité est la cessation de l'assurance-emploi), revenu prévisible des 12 mois suivants. L'année passée n'est PAS la période de référence du revenu.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Revenu de l'ANNÉE COURANTE, ou revenu PRÉVISIBLE des 12 prochains mois (PAS l'année passée)
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V170 · `piece_modele_fixation_pension.md` **C4**
*Pièces justificatives (VÉRIFICATION — distinctes du revenu à inscrire)*

- **source** — `PDFDocument` **26** — Modele quebecois fixation pension alimentaire (`Le-modele-quebecois-de-fixation-des-pensions-alimentaires-pour-enfants.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Vous devez […] fournir la copie de votre déclaration fiscale provinciale et de votre avis de cotisation […] pour la dernière année fiscale. […] l'absence de ces pièces pourrait avoir comme conséquence que le juge en augmente la valeur. » → La dernière année fiscale sert à vérifier, non à fixer le revenu (qui, lui, est celui de l'année courante / prévisible — C3).
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Pièces justificatives (VÉRIFICATION — distinctes du revenu à inscrire)
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V171 · `piece_modele_fixation_pension.md` **C5**
*Finalité : besoins des enfants / ressources des parents*

- **source** — `PDFDocument` **26** — Modele quebecois fixation pension alimentaire (`Le-modele-quebecois-de-fixation-des-pensions-alimentaires-pour-enfants.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Cette contribution est présumée correspondre aux besoins des enfants et aux ressources des parents. La preuve des besoins des enfants n'est donc pas requise.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Finalité : besoins des enfants / ressources des parents
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **30** — Avis de cotisation 2019 (`avis_de_cotisation_2019.pdf`)

#### V172 · `piece_pdf-30.md` **C1**
*Revenu total 2019 et sa composition*

- **source** — `PDFDocument` **30** — Avis de cotisation 2019 (`avis_de_cotisation_2019.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Ligne 111 Prestations d'assurance-emploi : 8 752,00 $ Ligne 154 Autres revenus : 37 991,58 $ Ligne 199 Revenu total : 46 743,58 $
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Revenu total 2019 et sa composition
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V173 · `piece_pdf-30.md` **C2**
*Déduction REER et revenu net*

- **source** — `PDFDocument` **30** — Avis de cotisation 2019 (`avis_de_cotisation_2019.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Ligne 214 Déduction pour REER ou RPAC/RVER : 4 955,00 $ Ligne 275 Revenu net : 41 788,58 $ Ligne 299 Revenu imposable : 41 788,58 $
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Déduction REER et revenu net
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **59** — Biographie d'Elise Ayoub publiée sur le site web du studio dance C (`Elise_Ayoub_Directrice_du_Studio_Danse_C_Chorégraphe_et_Professeure__Studi_ng5zc7D.pdf`)

#### V176 · `piece_pdf-59.md` **C1**
*Engagement de danse récurrent et continu, 1999→2016*

- **source** — `PDFDocument` **59** — Biographie d'Elise Ayoub publiée sur le site web du studio dance C (`Elise_Ayoub_Directrice_du_Studio_Danse_C_Chorégraphe_et_Professeure__Studi_ng5zc7D.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > elle se joint à l'école de danse Les Ballets Modernes du Québec […] et ce jusqu'en 2016
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Engagement de danse récurrent et continu, 1999→2016
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **75** — Identifying and Responding to Family Violence for Family Law Legal Advisers (`Types_of_Intimate_Partner_Violence.pdf`)

#### V178 · `piece_pdf-75.md` **C1**
*Contrôle coercitif post-séparation : tactiques (p. 49)*

- **source** — `PDFDocument` **75** — Identifying and Responding to Family Violence for Family Law Legal Advisers (`Types_of_Intimate_Partner_Violence.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Coercive controlling violence is more likely than other forms of IPV to continue and to escalate after separation. Risk often increases after separation because the abuser feels a loss of control. Following separation or divorce, an abuser may use different ways to try to assert control over their former partner, either directly or through the children. For example, an abusive spouse may attempt to assert control by: […] - refusing to comply with court orders; - threatening their former partner with the loss of parenting time with a child; - making unilateral decisions about children; […] - filing false reports with the police or a child protection agency; and/or - engaging in abusive tactics in relation to the legal process.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Contrôle coercitif post-séparation : tactiques (p. 49)
- **contrôle** — ➖ la source n'a pas de transcription en base
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V179 · `piece_pdf-75.md` **C2**
*Confusion des rôles conjoint/parent (p. 49)*

- **source** — `PDFDocument` **75** — Identifying and Responding to Family Violence for Family Law Legal Advisers (`Types_of_Intimate_Partner_Violence.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Perpetrators of coercive controlling violence have been found to be less able to differentiate their role as a spouse from their role as a parent, and are more likely to abuse their children after separation and divorce.
- **page_number** — 49
- **quote_location_details** — Confusion des rôles conjoint/parent (p. 49)
- **contrôle** — ➖ la source n'a pas de transcription en base
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V180 · `piece_pdf-75.md` **C3**
*Mise en garde du document lui-même sur l'usage de la typologie (p. 47)*

- **source** — `PDFDocument` **75** — Identifying and Responding to Family Violence for Family Law Legal Advisers (`Types_of_Intimate_Partner_Violence.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Legal professionals should not rely on these typologies to assess risk, but should focus on a client's individual circumstances. In particular, it is important to look for patterns of behaviour and cumulative effects, rather than looking at isolated incidents.
- **page_number** — 49
- **quote_location_details** — Mise en garde du document lui-même sur l'usage de la typologie (p. 47)
- **contrôle** — ➖ la source n'a pas de transcription en base
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **81** — Etat de compte pension alimentaire (`document.pdf`)

#### V181 · `piece_pdf-81.md` **C1**
*paiement de 1 000 $ reçu le 6 juin 2019*

- **source** — `PDFDocument` **81** — Etat de compte pension alimentaire (`document.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Ligne : « 2019-06-10 | prise d'effet 2019-06-06 | Paiement reçu | Crédit 1 000,00 | Solde 3 486,45 » (le solde passe de 4 486,45 à 3 486,45).
- **page_number** — ⚠️ à préciser
- **quote_location_details** — paiement de 1 000 $ reçu le 6 juin 2019
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **91** — Soccer St-Lambert date début et fin de session (`Soccer_enfants_4-8_ans__A.S._Saint-Lambert.pdf`)

#### V188 · `piece_pdf-91.md` **C2**
*Saison d'été de mai à août*

- **source** — `PDFDocument` **91** — Soccer St-Lambert date début et fin de session (`Soccer_enfants_4-8_ans__A.S._Saint-Lambert.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Début : 18 mai » « Fin : 29 août » « Pauses : 23 mai, 25-31 juil., 24 juin » « Fête de fin de saison : 29 août
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Saison d'été de mai à août
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **98** — Les tribunaux ne sont pas tendres (`les_tribunaux_ne_sont_pas_tendre.pdf`)

#### V191 · `piece_jurisprudence_cs-mg-2005.md` **C1**
*« pas tendres » : la branche sévère exige la MAUVAISE FOI / le départ SANS RAISON VALABLE*

- **source** — `PDFDocument` **98** — Les tribunaux ne sont pas tendres (`les_tribunaux_ne_sont_pas_tendre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > [24] « En règle générale, les tribunaux […] ne sont pas tendres à l'endroit du débiteur alimentaire qui, de propos délibéré et par mauvaise foi, inconscience, irréflexion, égoïsme, caprice ou indifférence, quitte son emploi sans raison valable, en prenant prématurément sa retraite ou un congé, ou en réorientant sa carrière vers des activités moins rémunératrices, cherchant ainsi à échapper à ses obligations alimentaires.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — « pas tendres » : la branche sévère exige la MAUVAISE FOI / le départ SANS RAISON VALABLE
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V192 · `piece_jurisprudence_cs-mg-2005.md` **C2**
*la branche protectrice : la PERTE D'EMPLOI est un motif légitime*

- **source** — `PDFDocument` **98** — Les tribunaux ne sont pas tendres (`les_tribunaux_ne_sont_pas_tendre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > [25] « Toutefois, les tribunaux ne sont pas réfractaires à la démarche de réorientation professionnelle lorsque cette démarche repose sur des motifs légitimes et raisonnables (la perte d'un emploi, par exemple, ou des problèmes de santé) et qu'elle n'impose pas de restrictions excessives aux bénéficiaires […].
- **page_number** — ⚠️ à préciser
- **quote_location_details** — la branche protectrice : la PERTE D'EMPLOI est un motif légitime
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V193 · `piece_jurisprudence_cs-mg-2005.md` **C3**
*le débiteur de bonne foi ≠ celui qui cache/sous-estime frauduleusement ses revenus*

- **source** — `PDFDocument` **98** — Les tribunaux ne sont pas tendres (`les_tribunaux_ne_sont_pas_tendre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > [39] « On n'a pas affaire ici à un individu qui cache des revenus ou qui les sous-estime frauduleusement, mais à un individu dont les faibles revenus s'expliquent par une démarche de réorientation professionnelle initialement légitime […].
- **page_number** — ⚠️ à préciser
- **quote_location_details** — le débiteur de bonne foi ≠ celui qui cache/sous-estime frauduleusement ses revenus
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V194 · `piece_jurisprudence_cs-mg-2005.md` **C4**
*le pouvoir de suppléer/établir le revenu (art. 825.12 C.p.c. = art. 446 actuel)*

- **source** — `PDFDocument` **98** — Les tribunaux ne sont pas tendres (`les_tribunaux_ne_sont_pas_tendre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > [39] cite l'art. 825.12 C.p.c. : « Si les informations qui paraissent dans le formulaire ou les documents prescrits sont incomplètes ou contestées […] le tribunal peut y suppléer et, notamment, établir le revenu d'un parent [… en tenant compte] de la valeur des actifs de ce parent et leur attribuer la production de revenus qu'il juge appropriée.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — le pouvoir de suppléer/établir le revenu (art. 825.12 C.p.c. = art. 446 actuel)
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V195 · `piece_jurisprudence_cs-mg-2005.md` **C5**
*un père moins nanti mais présent peut être préférable (art. 599 C.c.Q.)*

- **source** — `PDFDocument` **98** — Les tribunaux ne sont pas tendres (`les_tribunaux_ne_sont_pas_tendre.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > [33] « […] il peut être préférable d'avoir un père moins nanti mais plus présent, qui peut assumer mieux les obligations de garde, de surveillance et d'éducation qui lui incombent de par l'article 599 C.c.Q., qu'un père plus fortuné mais éloigné […].
- **page_number** — ⚠️ à préciser
- **quote_location_details** — un père moins nanti mais présent peut être préférable (art. 599 C.c.Q.)
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **99** — créer une situation financière inexistante (`2004canlii2080-2.pdf`)

#### V196 · `piece_jurisprudence_fl-sj-2004.md` **C1**
*inclure les montants non récurrents « crée une situation financière inexistante »*

- **source** — `PDFDocument` **99** — créer une situation financière inexistante (`2004canlii2080-2.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > [6] « La requérante […] voudrait fixer la pension alimentaire payable en fonction non seulement des prestations d'assurance-emploi, mais également des primes perçues lors de la perte d'emploi de monsieur. Adopter une telle proposition serait de créer une situation financière inexistante présentement.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — inclure les montants non récurrents « crée une situation financière inexistante »
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V197 · `piece_jurisprudence_fl-sj-2004.md` **C2**
*la pension se fixe sur les revenus ACTUELS*

- **source** — `PDFDocument` **99** — créer une situation financière inexistante (`2004canlii2080-2.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > [7] « En effet, la pension alimentaire est basée sur des revenus actuels. Ainsi, tenant compte du revenu annuel de la requérante […] et d'un revenu hebdomadaire de 413 $ par semaine pour l'intimé [= l'A-E seule], la pension alimentaire annuelle payable pour l'enfant est de 3 544,30 $.
- **page_number** — ⚠️ à préciser
- **quote_location_details** — la pension se fixe sur les revenus ACTUELS
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


---

## 2. Constats — `Quote(quote_text=…, position_anchor=…)` (51)

Le bloc énonce ce que le document **établit**, au lieu d'en recopier un passage. C'est le cas prévu par la docstring de `position_anchor` : le texte de la citation ne se retrouve pas tel quel dans la source, et l'ancre sert à la situer. Une entrée sans ancre en demande une.


### `Email` **3** — « emplois », Louis Philippe David <louisphilippe.david@gmail.com>, 2020-06-22

#### V021 · `piece_thread-3_email-3.md` **C1**
*démarche d'emploi active et spécifique (Allianz / Bucarest)*

- **source** — `Email` **3** — « emplois », Louis Philippe David <louisphilippe.david@gmail.com>, 2020-06-22
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Le défendeur poursuit un emploi précis (actuariat, Allianz, Bucarest ; conférence le 1ᵉʳ juillet). → Incompatible avec « choix de ne pas travailler » (§8).
- **position_anchor** — « choix de ne pas travailler »
- **titre du Cn** — démarche d'emploi active et spécifique (Allianz / Bucarest) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **4** — « Re: suite des choses », Marie-Josee Ayoub <mjayoub@ayoubavocats.ca>, 2020-04-20

#### V023 · `piece_thread-4_email-4.md` **C4**
*l'auto-réfutation de 2020 vise le régime d'accès né de l'accusation de 2013*

- **source** — `Email` **4** — « Re: suite des choses », Marie-Josee Ayoub <mjayoub@ayoubavocats.ca>, 2020-04-20
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > - Le lien avec 2013 passe par le fond, non par la pique. « Dommage tout ce temps perdu » (C2) et « tes enfants ont besoin que tu sois dans leur vie » (C1) renvoient à la période d'accès restreint (≈ 4 h/sem., au domicile des grands-parents — fait 14). Ce régime restreint correspondait au risque que Me Ayoub imputait au père dès 2013 (faits 7-8 : « violence conjugale depuis sa naissance », compromission DPJ), accusation jamais rétractée (fait 16-bis). Le père a lui-même exercé ce régime restreint, sans pouvoir ignorer une accusation non retirée (menace permanente).
- L'auto-réfutation. En 2020, l'autrice de cette accusation qualifie le régime de « temps perdu » et affirme que les enfants ont besoin du père — l'exact contraire du risque qu'elle avait elle-même invoqué pour le fonder. Si la restriction avait protégé d'un danger réel, la période ne serait pas « perdue » et la présence du père ne serait pas un « besoin ». Position impossible imposée au père : il ne pouvait ignorer l'accusation tant qu'elle subsistait, et on lui reproche ensuite de l'avoir prise au sérieux.
- La pique ne fait que confirmer le référent. « Tu préfères t'accrocher à un courriel qui date d'environ 5 ans » identifie le courriel visé comme celui du 11 juin 2013 (piece_pdf-1.md). Lien : these_2019_saisine_amiable.md (menace permanente), these_refus_garde_partagee.md.
- Antécédent daté (2016) — même reproche, autre autrice. Reproche identique déjà formulé par Élise elle-même le 16 sept. 2016 (piece_thread-
- **position_anchor** — « Dommage tout ce temps perdu »
- **titre du Cn** — l'auto-réfutation de 2020 vise le régime d'accès né de l'accusation de 2013 — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **7** — « Re: Visite », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-16

#### V025 · `piece_thread-6_email-7.md` **C7**
*Portée cumulative de l'énumération*

- **source** — `Email` **7** — « Re: Visite », Louis Philippe David <louisphilippe.david@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Les exemples choisis par LP ne sont pas quatre événements isolés. Ils correspondent à quatre structures répétitives de la vie familiale :

- tâches et routines du soir;
- cours et activités des enfants;
- cours de danse hebdomadaires d'Élise;
- dépôts et retours de garderie.

La force du passage ne vient donc pas de la seule affirmation rétrospective de LP. Chacune de ces catégories peut être confrontée à ses pièces contemporaines propres. Lorsque les pièces de danse, de garderie et d'activités corroborent l'existence du fonctionnement décrit, la réponse « pas 50 % » ne peut pas raisonnablement être lue comme une confirmation de la caractérisation judiciaire « rarement disponible ».

Contextes d'usage :
- §14-17 (allegation_stmt14_15_16_17_garde_partagee.md Axe 3 Voie 2) : présence quotidienne, incompatible avec « rarement disponible ».
- Renvoi : axe_agenda_danse_elise.md (absences d'Élise pour la danse, LP assumant seul).
- Cadre cumulatif : implication_parentale_recurrence/00_cadre_commun.md.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — Portée cumulative de l'énumération — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **306** — « Re: Visite », Elise Ayoub <elise.ayoub@gmail.com>, 2016-09-16

#### V054 · `piece_thread-6_email-306.md` **C3**
*Portée de la réponse au contre-récit détaillé*

- **source** — `Email` **306** — « Re: Visite », Elise Ayoub <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > L'email-306 répond directement à l'email-7, dans lequel LP invoque sa présence à la maison et énumère les tâches du soir, les activités des enfants, les cours de danse et la garderie.

Élise formule deux réponses expresses :

1. elle nie avoir dit qu'il passait son temps à se saouler;
2. elle maintient qu'il ne s'occupait pas des enfants 50 % du temps.

Elle ne répond pas séparément aux affirmations sur la fréquence de la danse, la participation aux activités, les trajets de garderie ou les catégories de tâches du soir. Cette absence de contestation précise peut corroborer le fait que le différend portait principalement sur la proportion globale. Elle ne constitue cependant pas un aveu formel de chaque détail avancé par LP.

Portée cumulative : l'expression « pas 50 % » ne permet pas de quantifier seule la participation antérieure. Lue avec les occurrences documentées dans plusieurs axes, elle est toutefois incompatible avec une lecture du fil selon laquelle Élise aurait répondu que LP n'accomplissait aucune fonction parentale.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — Portée de la réponse au contre-récit détaillé — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V055 · `piece_thread-6_email-7.md` **C6**
*Portée de la réponse d'Élise*

- **source** — `Email` **306** — « Re: Visite », Elise Ayoub <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Onze minutes plus tard, Élise répond dans email-306 qu'il ne s'occupait pas des enfants « 50 % du temps » et qu'elle n'a pas dit qu'il passait son temps à se saouler. Elle ne répond pas séparément aux exemples de tâches, de danse, d'activités ou de garderie.

Cette réponse situe expressément le différend sur la proportion de l'implication. Elle est importante par sa sélectivité :

1. Élise corrige expressément l'imputation sarcastique d'alcoolisme;
2. elle maintient expressément le seuil quantitatif de 50 %;
3. elle ne remplace pas l'énumération de LP par une version selon laquelle il aurait été absent des routines, étranger aux activités ou indisponible pour le second enfant.

Son absence de réponse distincte à chaque exemple ne doit pas être transformée en aveu formel de chaque fait. Elle a toutefois une valeur contextuelle : dans cet échange direct, le désaccord formulé par Élise n'est pas « tu ne participais pas », mais « tu ne participais pas à 50 % ».
- **position_anchor** — « tu ne participais pas à 50 % »
- **titre du Cn** — Portée de la réponse d'Élise — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **330** — « suite des choses », Louis Philippe David <louisphilippe.david@gmail.com>, 2020-04-17

#### V063 · `piece_thread-4_email-330.md` **C1**
*la contrainte « 65k/année » est nommée comme irréaliste, de bonne foi*

- **source** — `Email` **330** — « suite des choses », Louis Philippe David <louisphilippe.david@gmail.com>, 2020-04-17
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > « je ne me suis pas trouvé d'emplois à 65k/année » : le Demandeur documente, en temps réel, qu'aucun emploi au revenu imputé (≈ 64-65 k$) ne s'est matérialisé — épuisement des économies et du bail à l'appui. Contredit toute lecture de « choix de ne pas travailler » (§8).
- **position_anchor** — « je ne me suis pas trouvé d'emplois à 65k/année »
- **titre du Cn** — la contrainte « 65k/année » est nommée comme irréaliste, de bonne foi — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V064 · `piece_thread-4_email-330.md` **C2**
*offre d'aveu d'outrage, destinée à l'avocate*

- **source** — `Email` **330** — « suite des choses », Louis Philippe David <louisphilippe.david@gmail.com>, 2020-04-17
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Le Demandeur propose de plaider coupable pour outrage pour forcer la révision de sa capacité de payer « en ligne avec la réalité ». Destinataire : Me Ayoub personnellement → la démarche de règlement de bonne foi est adressée à celle qui, en 2023, allèguera au §3/§7-8 le refus de régler.

---
- **position_anchor** — « en ligne avec la réalité »
- **titre du Cn** — offre d'aveu d'outrage, destinée à l'avocate — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **345** — « Re: Baptême de Nicolas », Louis Philippe David <louisphilippe.david@gmail.com>, 2022-02-13

#### V066 · `piece_thread-76_email-343.md` **C2**
*Suite 2022 (email-345) : « obligée » vs « décidait simplement de le faire »*

- **source** — `Email` **345** — « Re: Baptême de Nicolas », Louis Philippe David <louisphilippe.david@gmail.com>, 2022-02-13
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > - Johanne (13 févr. 2022) : « Ça va faire sept ans, Élise est obligée de prendre des décisions unilatérales concernant les enfants. Ça reste ta décision d'être ou non impliqué… »
- LP (13 févr. 2022) : « Élise prenait déjà ses décisions seule par rapport aux enfants il y a 7 ans. Elle n'était pas obligée de prendre ses décisions unilatéralement à ce moment-là, le 18 juillet 2015, elle décidait simplement de le faire. »
- Lecture : LP distingue « obligée » (contrainte) de « décidait simplement de le faire » (choix) — parallèle direct au « j'ai été obligée de saisir » de §3 (effacement de l'agentivité). La grand-mère adopte le registre « obligée » que LP rebute.

---
- **position_anchor** — « Ça va faire sept ans, Élise est obligée de prendre des décisions unilatérales concernant les enfants. Ça reste ta décision d'être ou non impliqué… »
- **titre du Cn** — Suite 2022 (email-345) : « obligée » vs « décidait simplement de le faire » — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **453** — « Fin d'emplois », "David, Louis-Philippe" <Louis-Philippe.David@bnc.ca>, 2018-06-06

#### V080 · `piece_thread-111_congediement_bnc.md` **C2**
*La structure binaire offerte*

- **source** — `Email` **453** — « Fin d'emplois », "David, Louis-Philippe" <Louis-Philippe.David@bnc.ca>, 2018-06-06
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > - Circonstance : un constat écrit de rendement insuffisant → plan d'accompagnement ouvert, menant au congédiement.
- Offre : 3 semaines de transition + 2 semaines de « relocalisation à la maison » (payées, recherche d'emploi).
- Condition : les 2 semaines sont conditionnelles à la signature d'un document affirmant un DÉPART VOLONTAIRE (id=455).
- Alternative : refuser → rester en poste → plan d'accompagnement → congédiement.
- de l'Étoile pousse la qualification : « il n'est pas faux d'affirmer que vous avez décidé de quitter volontairement votre poste » ; LP refuse ; la Banque acte le refus (id=456 : « J'accuse votre refus d'accepter la relocalisation »).
- **position_anchor** — « relocalisation à la maison »
- **titre du Cn** — La structure binaire offerte — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **462** — « Salut », Louis Philippe David <louisphilippe.david@gmail.com>, 2020-02-17

#### V082 · `piece_thread-113_email-462.md` **C1**
*contrainte matérielle portée à la connaissance de Me Ayoub*

- **source** — `Email` **462** — « Salut », Louis Philippe David <louisphilippe.david@gmail.com>, 2020-02-17
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Le défendeur informe personnellement Me Ayoub que la suspension/annulation de son passeport (sous 30 jours) l'empêchera d'aller travailler (à l'étranger). → Élément documentaire que Me Ayoub détenait avant de rédiger la Dénonciation de 2023.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — contrainte matérielle portée à la connaissance de Me Ayoub — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **463** — « Re: Salut », "Marie-Josée Ayoub" <mjayoub@ayoubavocats.ca>, 2020-02-18

#### V084 · `piece_thread-113_email-462.md` **C3**
*canal de connaissance d'Élise : « Je vais voir avec Élise ce qu'elle veut faire » (email-463)*

- **source** — `Email` **463** — « Re: Salut », "Marie-Josée Ayoub" <mjayoub@ayoubavocats.ca>, 2020-02-18
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Me Ayoub relaie à Élise dès février 2020 → la connaissance d'Élise de la situation (contrainte, projet de départ, absence de mauvaise foi) est établie par un canal distinct, en sus du courriel P-386 du 22 juin 2020 qui lui est directement adressé.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — canal de connaissance d'Élise : « Je vais voir avec Élise ce qu'elle veut faire » (email-463) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **466** — « Re: Salut », Louis Philippe David <louisphilippe.david@gmail.com>, 2020-02-18

#### V085 · `piece_thread-113_email-462.md` **C4**
*le départ était réel, abandonné à cause du passeport (email-466)*

- **source** — `Email` **466** — « Re: Salut », Louis Philippe David <louisphilippe.david@gmail.com>, 2020-02-18
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > LP : « je devrais recevoir mon permis de travail le 14 [mars], mais […] mon passeport sera annulé, en fait je ne penses plus partir ». Le projet n'était pas une évasion indéfinie : il se matérialisait (permis attendu le 14 mars 2020) et n'a été abandonné qu'en raison de la suspension du passeport — obstacle que Me Ayoub connaissait (email-467).

---
- **position_anchor** — « je devrais recevoir mon permis de travail le 14 [mars], mais […] mon passeport sera annulé, en fait je ne penses plus partir »
- **titre du Cn** — le départ était réel, abandonné à cause du passeport (email-466) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **475** — « lettre de Marie Josee », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-05-15

#### V088 · `piece_thread-116_email-475.md` **C4**
*Portée probatoire et secret professionnel*

- **source** — `Email` **475** — « lettre de Marie Josee », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-05-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > - Le courriel 475 est une communication du défendeur à son propre avocat. Son utilisation suppose une renonciation volontaire et encadrée à son propre secret professionnel.
- Cette renonciation ne décide pas, à elle seule, du secret professionnel revendiqué par Élise Ayoub à l'égard de P-2, qui doit être tranché séparément.
- Si P-2 est recevable, la pièce jointe établit directement la connaissance de son contenu, y compris le mécanisme de la routine.
- Si P-2 est exclu, le texte non litigieux du courriel 475 demeure à analyser séparément comme preuve de l'état d'esprit du défendeur et de la distinction contemporaine entre refus des modalités et refus du rôle parental, sans contourner la protection accordée au contenu de P-2.
- La réception non privilégiée de la pièce jointe est établie séparément par `Email:487` (P-87). `Email:475` demeure une corroboration réservée jusqu’à la décision du demandeur et de son procureur sur la portée d’une éventuelle renonciation.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — Portée probatoire et secret professionnel — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **476** — « lettre de Marie Josee », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-05-21

#### V089 · `piece_thread-116_email-475.md` **C5**
*Complétude du fil : email-476 du 21 mai 2015*

- **source** — `Email` **476** — « lettre de Marie Josee », Louis Philippe David <louisphilippe.david@gmail.com>, 2015-05-21
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Le fil contient aussi l'email-476, dans lequel le défendeur dit vouloir régler rapidement et énumère trois possibilités, par ordre de préférence : garde partagée ; une fin de semaine sur deux ; arrangement actuel avec transfert de l'autorité parentale. Il ajoute que ces possibilités sont « non négociables » et que les autres options sont exclues.

Portée contradictoire à concéder : ce passage peut être invoqué pour démontrer une position ferme et le refus d'autres modalités. Il ne démontre toutefois pas un refus de l'amiable comme mode : le défendeur propose trois issues et demande que la situation soit réglée. Il renforce la calibration du §3 : ne jamais plaider qu'il n'a refusé aucune proposition ; plaider que le refus de certaines modalités ne constitue pas la cause complète de la saisine et ne signifie pas un refus de ses obligations parentales.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — Complétude du fil : email-476 du 21 mai 2015 — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **487** — « email », Johanne Bazinet <johannebazinet@gmail.com>, 2015-05-15

#### V094 · `piece_thread-122_email-487.md` **C1**
*Transmission du courriel du 11 juin 2013*

- **source** — `Email` **487** — « email », Johanne Bazinet <johannebazinet@gmail.com>, 2015-05-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Le corps du courriel ne contient que la signature de Johanne Bazinet. Le fichier EML contient toutefois une pièce jointe nommée `Courriel du 11 juin 2013.docx`.

La pièce jointe reproduit le courriel de Me Marie-Josée Ayoub à Élise Ayoub du 11 juin 2013 : mêmes expéditrice, destinataire, date, objet et contenu que la pièce P-2, notamment le passage relatif à la violence conjugale, à la garde exclusive urgente, à l’usage exclusif de la résidence, à la relocalisation du père, aux accès sans coucher et à l’installation d’une routine.

Portée directe : le 15 mai 2015, Johanne Bazinet a transmis au demandeur un fichier contenant le texte intégral du courriel du 11 juin 2013. Cette communication n’est pas une communication avocat-client.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — Transmission du courriel du 11 juin 2013 — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V095 · `piece_thread-122_email-487.md` **C2**
*Identification cryptographique de la pièce jointe*

- **source** — `Email` **487** — « email », Johanne Bazinet <johannebazinet@gmail.com>, 2015-05-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > | Propriété | Valeur |
|---|---|
| Nom | `Courriel du 11 juin 2013.docx` |
| Taille | 14 721 octets |
| SHA-256 | `d84bfac0bb4209be86535528c5d633d662dafb1285496abf762eefb380f2202a` |
| Pages déclarées | 2 |
| Mots déclarés | 654 |

La même pièce jointe apparaît dans `Email:475`, transmis par le demandeur à Me François Poirier 33 minutes plus tard. Les deux pièces jointes sont identiques bit pour bit.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — Identification cryptographique de la pièce jointe — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V096 · `piece_thread-122_email-487.md` **C3**
*Métadonnées internes du DOCX*

- **source** — `Email` **487** — « email », Johanne Bazinet <johannebazinet@gmail.com>, 2015-05-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Les propriétés internes `docProps/core.xml` et `docProps/app.xml` indiquent :

| Champ | Valeur |
|---|---|
| Créateur | `Johanne` |
| Dernière modification par | `Johanne` |
| Création | 2013-06-27 13:38:00 UTC (≈ 9 h 38 HAE) |
| Modification | 2013-06-27 13:39:00 UTC (≈ 9 h 39 HAE) |
| Révision | 1 |
| Temps total déclaré | 1 minute |
| Application | Microsoft Office Word 12.0 |
| Société inscrite | `Toshiba` |

Portée calibrée : ces métadonnées établissent que le fichier existait le 27 juin 2013 sous un profil Word identifié « Johanne ». Elles soutiennent son attribution technique à Johanne Bazinet, sans constituer à elles seules une preuve absolue de l’identité de l’opérateur ni de la date à laquelle le fichier a été transmis au demandeur.

Les dates 1980 inscrites dans les entrées ZIP du DOCX sont des valeurs techniques par défaut et n’ont pas de portée chronologique.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — Métadonnées internes du DOCX — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V097 · `piece_thread-122_email-487.md` **C4**
*Concordance avec P-2 et chaîne de transmission*

- **source** — `Email` **487** — « email », Johanne Bazinet <johannebazinet@gmail.com>, 2015-05-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > - Le texte du DOCX a été extrait et comparé au PDF `media/pdf_documents/20130611_MJ_Courriel_violence_conjugale.pdf` (`PDFDocument:1`, P-2).
- L’en-tête et le corps correspondent; les écarts observés proviennent de la mise en page et de l’extraction du texte PDF.
- Le DOCX a été rendu en deux pages et vérifié visuellement.
- À 12 h 00 UTC le 15 mai 2015, le demandeur a retransmis à Me François Poirier une copie strictement identique de la pièce jointe, comme le documente piece_thread-116_email-475.md.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — Concordance avec P-2 et chaîne de transmission — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **615** — « Re: demandes d'emplois », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-10-15

#### V101 · `piece_thread-156_email-615.md` **C1**
*transmission documentée des candidatures (recherche d'emploi)*

- **source** — `Email` **615** — « Re: demandes d'emplois », Louis Philippe David <louisphilippe.david@gmail.com>, 2019-10-15
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Le père transmet à Me Ayoub, le 15 oct. 2019, l'archive complète de ses candidatures (`applications.mbox`) + son annexe 1 — la preuve même de l'effort de recherche (quantité) et du domaine visé (qualité). Document sous-jacent au volet §7-8.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — transmission documentée des candidatures (recherche d'emploi) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **642** — « Fwd: », Mjayoub <mjayoub@ayoubavocats.ca>, 2019-10-21

#### V111 · `piece_thread-160_email-642.md` **C1**
*transmission datée (fait 222)*

- **source** — `Email` **642** — « Fwd: », Mjayoub <mjayoub@ayoubavocats.ca>, 2019-10-21
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Les talons sont fournis au Demandeur par Me Ayoub le 21 octobre 2019 à 10 h 32 (14 h 32 UTC), la veille de l'audition reportée (21 oct.) et de l'affidavit.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — transmission datée (fait 222) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V112 · `piece_thread-160_email-642.md` **C2**
*congés non rémunérés (fait 223)*

- **source** — `Email` **642** — « Fwd: », Mjayoub <mjayoub@ayoubavocats.ca>, 2019-10-21
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Chacun des deux bulletins porte 14 h de « congé non rémunéré » — la période de travail documentée n'est pas pleine.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — congés non rémunérés (fait 223) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V113 · `piece_thread-160_email-642.md` **C3**
*datation juin / juillet (fait 224)*

- **source** — `Email` **642** — « Fwd: », Mjayoub <mjayoub@ayoubavocats.ca>, 2019-10-21
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Bulletin 2 : fin de période 23 juin 2019 ; Bulletin 1 : fin de période 7 juillet 2019. Les deux talons couvrent juin et juillet 2019.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — datation juin / juillet (fait 224) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V114 · `piece_thread-160_email-642.md` **C4**
*le cumulatif corrobore le chiffre du PÈRE (112 k), non la déclaration de la mère (99 k)*

- **source** — `Email` **642** — « Fwd: », Mjayoub <mjayoub@ayoubavocats.ca>, 2019-10-21
- **cible** — `email_manager.Quote`
- **quote_text** — 
  > Au 7 juillet 2019 (période 15/26), le brut cumulatif d'Élise atteint déjà 65 104,42 $. Extrapolé sur l'année (≈ 4 340 $/période × 26 ≈ 112 800 $), il corrobore le montant que le père a inscrit pour la mère au formulaire — 112 569,08 $ (piece_pdf-82.md) — et contredit la sous-déclaration de la mère à son propre formulaire — 99 271,79 $ (piece_pdf-16.md). Asymétrie : le père impute la mère au plus juste, la mère se déclare en deçà.

---
- **position_anchor** — ⚠️ **à choisir dans la source**
- **titre du Cn** — le cumulatif corrobore le chiffre du PÈRE (112 k), non la déclaration de la mère (99 k) — ⚠️ *aucun champ dans le modèle courriel*
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **1** — Courriel suggérant de faire une plainte pour violence conjugale (`20130611_MJ_Courriel_violence_conjugale.pdf`)

#### V117 · `piece_pdf-1.md` **C11**
*Deux plans distincts : mesure initiale et plage d'accès durable*

- **source** — `PDFDocument` **1** — Courriel suggérant de faire une plainte pour violence conjugale (`20130611_MJ_Courriel_violence_conjugale.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > P-2 juxtapose, sans les confondre :

1. une mesure initiale rattachée au registre de la violence et de la compromission : relocalisation du père et accès sans coucher;
2. la préférence durable attribuée à Élise : qu'elle ait la garde, que les enfants voient leur père plus d'une fin de semaine sur deux et plusieurs fois par semaine, mais non selon l'alternance « une semaine sur deux » souhaitée par le père.

Le courriel ne préconçoit aucun horaire précis ni aucune progression. Il fixe plutôt les contraintes de destination : garde maternelle, contacts paternels plus fréquents qu'une fin de semaine sur deux, mais inférieurs à une garde partagée. La fréquence souhaitée n'est pas, à elle seule, incompatible avec les accès sans coucher : plusieurs contacts diurnes pouvaient satisfaire les deux propositions.

La difficulté probatoire apparaît dans la transition ultérieure. P-2 n'identifie aucun événement, évaluation, traitement, rétractation ou condition de sécurité susceptible de faire passer d'une compromission décrite comme structurelle et présente « depuis la naissance » à des nuitées autonomes. La seule évolution anticipée est l'écoulement du temps et la possibilité que les parents deviennent amis; le même courriel affirme par ailleurs que « Lp ne changera pas d'idée ». Les offres d'avril et d'août 2015 introduiront pourtant des nuitées non supervisées, puis une progression déclenchée par des dates, sans nommer le changement relatif au risque qui rendrait cette évolution compat
- **position_anchor** — « Lp ne changera pas d'idée »
- **page_number** — 1
- **quote_location_details** — Deux plans distincts : mesure initiale et plage d'accès durable
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **5** — 20150813 MJ projet consentement (`20150813_MJ_projet_consentement.pdf`)

#### V128 · `piece_pdf-5.md` **C1**
*Art. 2 : autorité parentale conjointe (clause positive)*

- **source** — `PDFDocument` **5** — 20150813 MJ projet consentement (`20150813_MJ_projet_consentement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > > Voir verbatim art. 2 ci-dessus. Pertinent §30 : la consultation conjointe est posée comme principe.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Art. 2 : autorité parentale conjointe (clause positive)
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **7** — Réponse finale à l'offre d'une progression vers une garde partagée (`20150903_MJ_reponse_a_reponse_du_projet_de_consentement.PDF`)

#### V143 · `piece_pdf-7.md` **C4**
*Les messages de P-5 sont annexés dès le 3 septembre 2015*

- **source** — `PDFDocument` **7** — Réponse finale à l'offre d'une progression vers une garde partagée (`20150903_MJ_reponse_a_reponse_du_projet_de_consentement.PDF`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Analyse : les iMessages produits comme P-5 dans la Requête de nov. 2015 étaient déjà annexés à cette lettre du 3 sept. 2015. Établit la provenance et la date d'usage des messages dans la négociation, antérieure à la Requête.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Les messages de P-5 sont annexés dès le 3 septembre 2015
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **12** — Revenus technicien laboratoire_agent service a la clientele 2024 (`Guichet-Emplois_Information_sur_le_marché_du_travail.pdf`)

#### V151 · `piece_pdf-12.md` **C1**
*les salaires invoqués sont des données 2024, BORNE SUPÉRIEURE de la réalité 2019*

- **source** — `PDFDocument` **12** — Revenus technicien laboratoire_agent service a la clientele 2024 (`Guichet-Emplois_Information_sur_le_marché_du_travail.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le jugement et les salaires en débat sont de 2019 ; les données Guichet-Emplois sont de 2024. Les emplois peu spécialisés ont subi une inflation majeure (2023 seule : +6,5 % ; cumul 2019-2024 ≈ +18 %). Les chiffres 2024 (≈ 38-39 k) surestiment donc le 2019 : l'équivalent 2019 des emplois suggérés ≈ 30 410 $. → Le « 35-42 k » employé jusqu'ici est une borne supérieure ; la réalité 2019 est plus basse.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — les salaires invoqués sont des données 2024, BORNE SUPÉRIEURE de la réalité 2019
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V152 · `piece_pdf-12.md` **C2**
*les emplois suggérés (2019 ≈ 30 k) < le revenu déclaré (46 743 $) < l'imputé (65 k)*

- **source** — `PDFDocument` **12** — Revenus technicien laboratoire_agent service a la clientele 2024 (`Guichet-Emplois_Information_sur_le_marché_du_travail.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > En 2019, les emplois suggérés par la partie adverse valaient ≈ 30 410 $ — inférieurs au revenu déclaré par le défendeur (46 743 $) et très loin du 65 k imputé (qui, indexé, vaudrait 82 904 $ en 2024). → Accepter ces emplois aurait abaissé sa base ; et ils n'appuient en rien une capacité de 65 k.

---
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — les emplois suggérés (2019 ≈ 30 k) < le revenu déclaré (46 743 $) < l'imputé (65 k)
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **13** — Jugement sur le fond (perte emplois) (`jugement.pdf`)

#### V155 · `piece_pdf-13.md` **C3**
*Capacité de gain imputée + arrérages*

- **source** — `PDFDocument` **13** — Jugement sur le fond (perte emplois) (`jugement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > - 650 $/mois maintenus « compte tenu de la situation financière » + arrérages ≈ 5 500 $ : c'est le jugement « perte d'emplois » que LP cherchait à « finaliser » en 2020. Utile au contexte financier/contrainte.
- **position_anchor** — « compte tenu de la situation financière »
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Capacité de gain imputée + arrérages
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V156 · `piece_pdf-13.md` **C4**
*P-2 déposée APRÈS la clôture de la preuve de Monsieur (asymétrie procédurale)*

- **source** — `PDFDocument` **13** — Jugement sur le fond (perte emplois) (`jugement.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > La liasse P-2 (« plusieurs recherches d'emploi offertes à Monsieur ») — la pièce même qu'invoque le §7 de la Dénonciation 2023 (« plus de quatre cents offres… disponibles ») — est déposée à 10 h 38:50, pendant le témoignage d'Élise interrogée par Me Ayoub, soit après que la preuve de Monsieur fut close (≈ 10 h 29). Le défendeur, qui se représentait seul, n'a « pas de question » (10 h 45:50) et n'a jamais eu l'occasion de contester le contenu de P-2 ni les salaires réels des emplois qu'elle liste. → Le « il a été mis en preuve » du §7 s'appuie sur une pièce entrée sans contradiction possible. Soutient faits 231-233.

---
- **position_anchor** — « plusieurs recherches d'emploi offertes à Monsieur »
- **page_number** — ⚠️ à préciser
- **quote_location_details** — P-2 déposée APRÈS la clôture de la preuve de Monsieur (asymétrie procédurale)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **14** — Jugement sur la garde des enfants (`Jugement_1.pdf`)

#### V157 · `piece_pdf-14.md` **C1**
*Frais de garde inclus dans la base ; frais particuliers = 0 $ ; médical = 48 % sur pièces*

- **source** — `PDFDocument` **14** — Jugement sur la garde des enfants (`Jugement_1.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > La pension de base (820 $) inclut les frais de garde (jugement, parenthèse). Les frais particuliers (l. 405) sont à 0 $. Le médical/santé est traité hors pension : père 48 % sur pièces justificatives. → Pertinent §6.6 / §6.7.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Frais de garde inclus dans la base ; frais particuliers = 0 $ ; médical = 48 % sur pièces
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V158 · `piece_pdf-14.md` **C2**
*La majoration (820 $ vs 764,87 $) compense la mère pour les accès limités du père*

- **source** — `PDFDocument` **14** — Jugement sur la garde des enfants (`Jugement_1.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le supplément (~55 $/mois) est accordé « pour tenir compte des accès limités exercés par le père et des inconvénients que cela entraîne pour la mère » (partie 7). → La pension indemnise déjà la mère de la charge asymétrique (calibre §6.7). À relier : le père réclamait plus d'accès (axes A/C/M) — la « limitation » n'était pas sa préférence.
- **position_anchor** — « pour tenir compte des accès limités exercés par le père et des inconvénients que cela entraîne pour la mère »
- **page_number** — ⚠️ à préciser
- **quote_location_details** — La majoration (820 $ vs 764,87 $) compense la mère pour les accès limités du père
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V159 · `piece_pdf-14.md` **C3**
*Autorité parentale exclusive de fait (mère signe seule)*

- **source** — `PDFDocument` **14** — Jugement sur la garde des enfants (`Jugement_1.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le jugement permet à la mère de signer seule santé/éducation/passeport/voyage et de voyager sans le consentement du père. → Pertinent §30-31 (autorité) et §42/§64 (voyage). Jugement par défaut — n'adjuge rien au fond (bouclier anti-bootstrap).

---
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Autorité parentale exclusive de fait (mère signe seule)
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **15** — Jugement Intérimaire (`20191021_Jugement_Intérimaire.pdf`)

#### V160 · `piece_pdf-15.md` **C1**
*Substitution de procureure : Ferreira → Me Ayoub*

- **source** — `PDFDocument` **15** — Jugement Intérimaire (`20191021_Jugement_Intérimaire.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > La procureure inscrite Adelia Ferreira (rédactrice de la Requête de 2015) est biffée ; Me Marie-Josée Ayoub (sœur de la demanderesse) la remplace et plaide en personne. Le défendeur se représente seul.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Substitution de procureure : Ferreira → Me Ayoub
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V161 · `piece_pdf-15.md` **C2**
*Le père sans revenu (contexte perte d'emploi)*

- **source** — `PDFDocument` **15** — Jugement Intérimaire (`20191021_Jugement_Intérimaire.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le tribunal retient que « Monsieur n'a aucun revenu » ; suspension de la pension et des arrérages, levée des saisies — mesures favorables au père dans l'attente de la documentation. Contexte : recherche d'emploi 2018-2019, emploi éventuel à Bucarest.
- **position_anchor** — « Monsieur n'a aucun revenu »
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Le père sans revenu (contexte perte d'emploi)
- **contrôle** — ✅ retrouvé dans la source
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V162 · `piece_pdf-15.md` **C3**
*Report au 21 octobre 2019 (date de la suite / du fond)*

- **source** — `PDFDocument` **15** — Jugement Intérimaire (`20191021_Jugement_Intérimaire.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le dossier est reporté au 21 octobre 2019 — date à laquelle la déclaration assermentée (§6.3, etc.) est signée (faits_par6-3_2019.md) et où le défendeur envoie son courriel de contestation B-12 (piece_thread-121_email-486.md).
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Report au 21 octobre 2019 (date de la suite / du fond)
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V163 · `piece_pdf-15.md` **C4**
*Rétablissement des communications demandé par le juge (⚠️ hors PV)*

- **source** — `PDFDocument` **15** — Jugement Intérimaire (`20191021_Jugement_Intérimaire.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Selon le déroulement de l'audition, le juge a demandé le rétablissement de la communication entre les parties (rompue depuis le 26 sept. 2016 — piece_thread-5_email-5.md), ce qui a été fait. Cette demande n'est pas transcrite au PV ; elle figurerait à l'enregistrement de l'audition (disponible au besoin). → À confirmer par l'enregistrement avant d'en faire un fait plaidable ; sert d'endpoint à la période de cessation (26 sept. 2016 → 27 sept. 2019).

---
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Rétablissement des communications demandé par le juge (⚠️ hors PV)
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **16** — Formulaire de pension alimentaire Jugement sur le fond (`formulaire_pension_alimentaire_3.pdf`)

#### V164 · `piece_pdf-16.md` **C1**
*En 2019, Me Ayoub porte les frais particuliers (sports) à la ligne 405 = 2 900 $*

- **source** — `PDFDocument` **16** — Formulaire de pension alimentaire Jugement sur le fond (`formulaire_pension_alimentaire_3.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Contrairement au formulaire de 2016 (l. 405 = 0 $), le formulaire de 2019 — rédigé par Me Ayoub — ajoute les activités physiques des enfants comme frais particuliers (2 900 $). → C'est l'objet même de la modification : faire reconnaître des frais non portés en 2016. Pertinent §6.6/6.7 : confirme que les frais particuliers n'étaient pas au calcul de 2016 (cohérent avec §6.6) et que la voie normale pour les ajouter est… la modification de 2019.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — 8
- **quote_location_details** — En 2019, Me Ayoub porte les frais particuliers (sports) à la ligne 405 = 2 900 $
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V165 · `piece_pdf-16.md` **C2**
*Autorat de Me Ayoub (scienter 2019)*

- **source** — `PDFDocument` **16** — Formulaire de pension alimentaire Jugement sur le fond (`formulaire_pension_alimentaire_3.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le formulaire de 2019 est préparé pour Me Ayoub. Au moment de le produire (et de rédiger la DA), elle dispose du jugement de 2016 et de ses termes (frais de garde inclus dans la base ; médical 48 % sur pièces). → Base du scienter de Me Ayoub pour §6.6/6.7 : connaissance du régime de 2016, non autorat du formulaire de 2016.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — 8
- **quote_location_details** — Autorat de Me Ayoub (scienter 2019)
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V166 · `piece_pdf-16.md` **C3**
*le père y est imputé à son revenu 2018 (ligne 200 = 64 028,34 $), sa ligne 203 (a.-e.) laissée vide*

- **source** — `PDFDocument` **16** — Formulaire de pension alimentaire Jugement sur le fond (`formulaire_pension_alimentaire_3.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Au formulaire de la mère, la ligne 200 (salaire brut) du père porte 64 028,34 $ — soit exactement son revenu total 2018 (déclaration 2018, fait 221). La ligne 203 (assurance-emploi) du père est vide, alors qu'il percevait de l'a.-e. en 2019. Le formulaire présente donc le père comme s'il gagnait encore son revenu d'emploi 2018, tandis que son propre formulaire (piece_pdf-82.md) déclare pour 2019 un salaire brut de 0 $ (survie : a.-e. 7 658 $ + retrait REER 35 000 $). → Fonde faits 227-230 ; c'est le cœur du litige d'imputation.

---
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — 8
- **quote_location_details** — le père y est imputé à son revenu 2018 (ligne 200 = 64 028,34 $), sa ligne 203 (a.-e.) laissée vide
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **35** — Avis de cotisation 2018 (`avis_de_cotisation_2018.pdf`)

#### V174 · `piece_pdf-35.md` **C1**
*le « 64 028 » est un revenu COMPOSITE, pas un salaire*

- **source** — `PDFDocument` **35** — Avis de cotisation 2018 (`avis_de_cotisation_2018.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le revenu total 2018 (64 028,34 $) se compose de : emploi 47 520,51 $ + A-E 12 034 $ + REER 4 089,60 $ + autres 384,23 $. Les ~16 508 $ d'A-E + REER sont non récurrents (chômage + liquidation d'épargne).
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — 2
- **quote_location_details** — le « 64 028 » est un revenu COMPOSITE, pas un salaire
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V175 · `piece_pdf-35.md` **C2**
*le vrai revenu d'EMPLOI 2018 = 47 520,51 $ (et l'emploi a pris fin le 29 juin 2018)*

- **source** — `PDFDocument` **35** — Avis de cotisation 2018 (`avis_de_cotisation_2018.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > La capacité de gain d'emploi démontrée en 2018 est 47 520,51 $ (ligne 101), non 64 028 $ — et provient d'un emploi (BNC) terminé le 29 juin 2018.

---
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — 2
- **quote_location_details** — le vrai revenu d'EMPLOI 2018 = 47 520,51 $ (et l'emploi a pris fin le 29 juin 2018)
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **72** — Permis de travail (`20200304_Work_authorization_-_Mr._David_Louis_Philippe.pdf`)

#### V177 · `piece_pdf-72.md` **C1**
*le père a OBTENU le permis de travail : il avait tout fait*

- **source** — `PDFDocument` **72** — Permis de travail (`20200304_Work_authorization_-_Mr._David_Louis_Philippe.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le défendeur n'a pas seulement trouvé l'emploi (Allianz, offre 19 août 2019) — il a obtenu le permis de travail roumain (4 mars 2020), poste permanent. → Il a accompli toutes les démarches pour travailler. Incompatible avec « choix de ne pas travailler » (§8).

---
- **position_anchor** — « choix de ne pas travailler »
- **page_number** — ⚠️ à préciser
- **quote_location_details** — le père a OBTENU le permis de travail : il avait tout fait
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **82** — formulaire pension alimentaire père (`test.pdf`)

#### V182 · `piece_pdf-82.md` **C1**
*salaire brut du père = 0 (aucun revenu d'emploi en 2019)*

- **source** — `PDFDocument` **82** — formulaire pension alimentaire père (`test.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Le père, dans son propre formulaire déposé au tribunal, déclare un salaire brut de 0 $ : il n'a aucun revenu d'emploi en 2019 (sans emploi du 29 juin 2018 à août 2019 — chronologie_emploi_2018-2023.md).
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — salaire brut du père = 0 (aucun revenu d'emploi en 2019)
- **contrôle** — ➖ la source n'a pas de transcription en base
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V183 · `piece_pdf-82.md` **C2**
*le revenu = assurance-emploi + REER (survie)*

- **source** — `PDFDocument` **82** — formulaire pension alimentaire père (`test.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > Total ≈ 42 658 $ = A-E (7 658 $) + autres revenus 35 000 $ (retrait REER, per la chronologie). Revenu de survie, non un revenu d'emploi qu'on aurait refusé. → Retire à §8 (« choix de ne pas travailler ») sa prémisse.

---
- **position_anchor** — « choix de ne pas travailler »
- **page_number** — ⚠️ à préciser
- **quote_location_details** — le revenu = assurance-emploi + REER (survie)
- **contrôle** — ➖ la source n'a pas de transcription en base
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **83** — La Presse - Lois 9 parjet imigration annulé (`Dossiers_dimmigration_annulés.pdf`)

#### V184 · `piece_pdf-83.md` **C1**
*la cause externe du projet de départ à l'étranger*

- **source** — `PDFDocument` **83** — La Presse - Lois 9 parjet imigration annulé (`Dossiers_dimmigration_annulés.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > L'annulation des ~18 000 CSQ (PL9, 7 févr. 2019) est le fait public qui sous-tend le §18 de la DA-2019 (Me Ayoub) : « sa décision d'aller travailler à Bucarest est le résultat de la décision du Gouvernement […] de réduire les quotas d'immigration, de sorte que la demande d'immigration de la conjointe […] rejetée ». → La demande de CSQ de la conjointe du défendeur figure parmi les dossiers annulés ; sans CSQ, le projet de vie au Québec s'effondre, d'où le projet de relocalisation à l'étranger (Bucarest / Allianz).

---
- **position_anchor** — « sa décision d'aller travailler à Bucarest est le résultat de la décision du Gouvernement […] de réduire les quotas d'immigration, de sorte que la demande d'immigration de la conjointe […] rejetée »
- **page_number** — ⚠️ à préciser
- **quote_location_details** — la cause externe du projet de départ à l'étranger
- **contrôle** — ➖ la source n'a pas de transcription en base
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **84** — Demande d'immigration Silvia (`20160613_demande_de_Certificat_de_sélection_du_Québec.pdf`)

#### V185 · `piece_pdf-84.md` **C1**
*c'est cette demande de CSQ qui a été annulée par le PL9 de Legault*

- **source** — `PDFDocument` **84** — Demande d'immigration Silvia (`20160613_demande_de_Certificat_de_sélection_du_Québec.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > La conjointe du défendeur a une demande de CSQ pendante depuis le 13 juin 2016 (programme régulier des travailleurs qualifiés, établissement à Montréal). C'est cette demande qui figure parmi les ~18 000 dossiers annulés le 7 février 2019 par le projet de loi 9 du gouvernement Legault (piece_pdf-83.md). → Sans CSQ, la conjointe ne peut s'établir au Québec : c'est la cause externe du projet de relocalisation à l'étranger (Bucarest) invoquée par Me Ayoub elle-même à la DA-2019 §18.

---
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — c'est cette demande de CSQ qui a été annulée par le PL9 de Legault
- **contrôle** — ➖ la source n'a pas de transcription en base
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **85** — indice indexation rrq 2016 - 2026 (`Historique_indexation_rrq.pdf`)

#### V186 · `piece_pdf-85.md` **C1**
*proxy officiel pour actualiser/déflater un salaire 2019 ↔ 2024*

- **source** — `PDFDocument` **85** — indice indexation rrq 2016 - 2026 (`Historique_indexation_rrq.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > La pension alimentaire est indexée au 1ᵉʳ janvier selon l'indice des rentes (C.c.Q.). La colonne 1 (indice des rentes) fournit donc le proxy légitime pour ramener à 2019 les salaires Guichet-Emplois de 2024 (et inversement) — calcul fait dans piece_pdf-12.md.

---
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — proxy officiel pour actualiser/déflater un salaire 2019 ↔ 2024
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **91** — Soccer St-Lambert date début et fin de session (`Soccer_enfants_4-8_ans__A.S._Saint-Lambert.pdf`)

#### V187 · `piece_pdf-91.md` **C1**
*Programme des enfants de quatre à huit ans*

- **source** — `PDFDocument` **91** — Soccer St-Lambert date début et fin de session (`Soccer_enfants_4-8_ans__A.S._Saint-Lambert.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > La première page décrit le « CDC 4 à 8 ans » et précise que, depuis 2020, les activités des joueurs et joueuses de quatre à douze ans sont regroupées au Centre de développement du club. Pour les quatre à huit ans, les matchs sont inclus dans les séances d'entraînement.

Cette mention « depuis 2020 » confirme que le nom et la structure administrative actuels ne doivent pas être projetés tels quels sur 2013.
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Programme des enfants de quatre à huit ans
- **contrôle** — ⚠️ **non retrouvé dans la source** — texte à ajuster ou ancre à fournir
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PDFDocument` **95** — Relevé de compte pension alimentaire (`document-2.pdf`)

#### V189 · `piece_releve_pension_rq_2026.md` **C1**
*Sommaire des sommes dues (au 21 janvier 2026)*

- **source** — `PDFDocument` **95** — Relevé de compte pension alimentaire (`document-2.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > | Description | À payer ($) | Payée ($) | Solde ($) |
|---|---:|---:|---:|
| Solde précédent | | | 49 279,00 |
| Pension alimentaire — périodes précédentes | 48 389,26 | 131,24 | 48 258,02 |
| Pension alimentaire — pendant la période | 6 269,92 | 261,75 | 6 008,17 |
| Sûreté demandée | 783,74 | 0,00 | 783,74 |
| Frais demandés | 109,56 | 0,00 | 109,56 |
| Total des sommes dues | | | 55 159,49 |

- Arrérages de pension seuls : 48 258,02 + 6 008,17 = 54 266,19 $.
- Revenu Québec a versé 572,57 $ au créancier « à titre d'avance » (le percepteur avance au créancier même sans paiement du débiteur).
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Sommaire des sommes dues (au 21 janvier 2026)
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V190 · `piece_releve_pension_rq_2026.md` **C2**
*Sommes payées par le débiteur (uniquement des saisies, 2025)*

- **source** — `PDFDocument` **95** — Relevé de compte pension alimentaire (`document-2.pdf`)
- **cible** — `pdf_manager.Quote`
- **quote_text** — 
  > | Type | Prise d'effet | Montant ($) |
|---|---|---:|
| Saisie d'impôt fédéral | 2025-06-25 | 87,25 |
| Saisie du crédit d'impôt pour solidarité | 2025-07-04 | 65,62 |
| Saisie d'impôt fédéral | 2025-09-23 | 87,25 |
| Saisie du crédit d'impôt pour solidarité | 2025-10-03 | 65,62 |
| Saisie d'impôt fédéral | 2025-12-16 | 87,25 |
| Total payé (période) | | 392,99 |

---
- **position_anchor** — ⚠️ **à choisir dans la source**
- **page_number** — ⚠️ à préciser
- **quote_location_details** — Sommes payées par le débiteur (uniquement des saisies, 2025)
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


---

## 3. Objets — `ChatSequence` / `PhotoDocument` (27)

Ces sources n'ont pas de modèle `Quote`, mais elles n'en ont pas besoin : une `ChatSequence` est un titre plus une sélection de messages, un `PhotoDocument` un titre plus une sélection de photos. La citation s'y crée en **découpant plus fin**, pas en ajoutant une ligne d'un autre type.


### `ChatSequence` **1** — Premiere discussion pension (30 messages)

#### V001 · `piece_chatsequence-1.md` **C1**
*Élise impose son revenu 2014 (année de congé maladie) contre le revenu prévisible*

- **source** — `ChatSequence` **1** — Premiere discussion pension (30 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > LP : « j'ai fait calculer la pension » — Élise : « tu as pris quel montant pour moi ? » — LP : « 95k »
> Élise : « car j'ai à peine fait 75 l'an passé… et cette année je ne ferai pas 95 non plus »
> LP : « c'est calculé sur le salaire normal que tu t'attends à recevoir »
> Élise : « Voici ce que j'ai fait l'an dernier 74914,39 et c'est ce que tu dois utiliser »
> Élise : « ok je vais lui envoyer mon T4… car même cette année, pas retour à temps complet avant avril »
> Élise : « ma sœur a bien confirmé et c'est sur le T4 »
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `ChatSequence` **3** — Etats de la relation avant la séparation (126 messages)

#### V002 · `piece_chatsequence-3.md` **C1**
*Solidarité financière et projet familial (3-4 nov. 2014)*

- **source** — `ChatSequence` **3** — Etats de la relation avant la séparation (126 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise : « est ce que je peux t'emprunter 1000$ et te le donner en 4 paiements de 250$? » — LP : « je peux te donner 800 jeudi ».
>
> Élise : « les voyages… le temps consacrés à nous 4… c'est assez important » et « c'est la première fois que tu investis dans un voyage ça me fait plaisir que tu le fasses ».

→ Les reproches financiers présents dans le même échange ne sont pas occultés. La portée n'est pas de démontrer l'harmonie : elle est d'établir qu'une relation financière et une projection familiale demeuraient possibles et effectivement exercées.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V003 · `piece_chatsequence-3.md` **C2**
*Coordination ménagère (habit de neige de Nicolas, 28 nov. 2014)*

- **source** — `ChatSequence` **3** — Etats de la relation avant la séparation (126 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise : « as tu acheté lhabit de neige a nico » — LP : « as tu l lien je vais l'achetr la »
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V004 · `piece_chatsequence-3.md` **C3**
*Urgence médicale de Nicolas — le défendeur s'organise (3 déc. 2014)*

- **source** — `ChatSequence` **3** — Etats de la relation avant la séparation (126 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise : « urgence — 13h30 — nicolas david » — LP : « ma mere va me faire un lift elle part a 12h » — Élise : « il faut vraiment juste que tu arrives avant 12h30 car ils commencent le processus dodo »

→ le défendeur organise son déplacement (lift de sa mère) pour arriver au RV médical avant le dodo.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V005 · `piece_chatsequence-3.md` **C4**
*Gestion des antibiotiques et de la fièvre de Nicolas (16 déc. 2014)*

- **source** — `ChatSequence` **3** — Etats de la relation avant la séparation (126 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise : « as tu été cherché ses antibio » — LP : « je vais y aller sa fievre a baisser et il est en feu »

→ Malgré un désaccord sur le moment des doses, les parties coordonnent concrètement les soins et le défendeur va chercher la médication.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V006 · `piece_chatsequence-3.md` **C5**
*Confidence personnelle et soutien (métastases de la mère d'Élise, 14 janv. 2015)*

- **source** — `ChatSequence` **3** — Etats de la relation avant la séparation (126 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise : « Ma mère a plusieurs métastases dans son foie… » — LP : « Je suis désolé Elise »

→ Cinq semaines avant le départ, le canal de confiance personnelle et de soutien demeure accessible.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V007 · `piece_chatsequence-3.md` **C6**
*Transition matérielle et nouvelle coopération financière : offre Accord D (2 fév. 2015)*

- **source** — `ChatSequence` **3** — Etats de la relation avant la séparation (126 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise : « Tu prévois quitter quand? » / « Et tu prévoies emmener quoi avec toi? » — LP : « je prevoit amener le lit et le four, laveuse secheuse » / « le matelas » / « je veux pas changer trop la maiso » — Élise : « Je trouverais une façon de te payer les divans » — LP : « c est pas pressé » / « si tu veux je peux prendre un accord D pour un matelas et le pouel, four » / « je te l'offre » — Élise : « Non ça va merci »

→ À la question d'Élise sur ce qu'il emporte, le défendeur répond par une liste limitée et « je veux pas changer trop la maiso », puis offre spontanément de contracter une nouvelle obligation de crédit au bénéfice de la demanderesse. Le refus de l'offre par Élise n'efface pas le fait qu'une coopération financière additionnelle demeurait possible et était proposée au moment du départ.

(Correction : version antérieure de C5 n'avait extrait que la fin — l'offre Accord D — omettant la question d'Élise et la réponse « je veux pas changer trop la maiso ». Complété depuis ChatSequence pk=3, base.)
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V008 · `piece_chatsequence-3.md` **C7**
*Soutien proposé pour l'après-départ (3 fév. 2015)*

- **source** — `ChatSequence` **3** — Etats de la relation avant la séparation (126 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise : « je vais être seule la nuit avec eux si ils sont malades » — LP : « tu m'apple, j'airai chez vous, je vais etre a coté »

→ Le défendeur offre un soutien de proximité après son départ. La réponse sceptique d'Élise (« tu dis ça maintenant… attends d'avoir une cocotte ») témoigne d'une tension, mais confirme que la dimension discutée est la continuité future de cette aide.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V009 · `piece_chatsequence-3.md` **C8**
*Projection familiale après l'annonce du départ (13 fév. 2015)*

- **source** — `ChatSequence` **3** — Etats de la relation avant la séparation (126 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise : « Le film joue a 4h15, on pourrait y aller les 4 […] et manger au scores après » — LP : « on devrait faire une journee famille par mois qu'en penses tu? » — Élise : « oui pour la journée familiale » et « on ira à la cabane à sucre en mars ».

→ Dix jours avant le départ physique et après son annonce, les parties projettent des activités familiales au-delà de la cessation prévue de la cohabitation.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `ChatSequence` **4** — La suprise du départ (10 messages)

#### V010 · `piece_chatsequence-4.md` **C1**
*Échéancier décidé sans discussion préalable*

- **source** — `ChatSequence` **4** — La suprise du départ (10 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise (2 fév. 2015) : « Tu prévois quitter quand? »
>
> Élise (3 fév. 2015) : « tu as décidé de quand tu partais et la date » · « tu ne m'en as même pas parlé ».
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V011 · `piece_chatsequence-4.md` **C2**
*Absence de temps pour prévoir la conséquence*

- **source** — `ChatSequence` **4** — La suprise du départ (10 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise (3 fév. 2015) : « si j'avais pu prendre le temps de prévoir » · « je ne serais pas stressée comme ca » · « mais tu as décidé de partir vite » · « je suis fucking stressée » · « tu n'y a pas vraiment pensé à ce que cela me ferait ».
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `ChatSequence` **5** — discussion du pret de 9000$ (19 messages)

#### V012 · `piece_chatsequence-5.md` **C1**
*Le solde du prêt de 9 000 $ (remboursé par crédit de loyer)*

- **source** — `ChatSequence` **5** — discussion du pret de 9000$ (19 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise : « 7507=5250 » · « 9000-5250 » · « 3750 » · « c'est ça? » — LP : « 750 /mois 7 mois c est bon ok? » — Élise : « oui » · « je vais demander a mon pere de me donner le 3700 »

→ le prêt de 9 000 $ était remboursable par crédit de loyer (750 $/mois sur ~12 mois). Le départ a écourté l'année à ~7 mois (5 250 $ crédités), laissant un solde de 3 750 $. Le calcul établit le solde — il ne révise pas l'entente.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `ChatSequence` **6** — Discussion sur le financement d'Élise (21 messages)

#### V013 · `piece_chatsequence-6.md` **C1**
*Endettement de la demanderesse et taux d'intérêt (3 fév. 2015)*

- **source** — `ChatSequence` **6** — Discussion sur le financement d'Élise (21 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise : « je paie vraiment 1200 par mois d'intéret… juste d'intéret et taxe » · « j'ai 400k$ de pret » · « et j'ai des taux à 10% » · « à 8% » · « et à 2,5% » · « j'ai 320 à 2,5 » · « 20 à 5 » · « 30 à 10 » · « 30 entre 4 et 20 »

Décomposition (verbatim) : 400 000 $ de dette — 320 k à 2,5 %, 20 k à 5 %, 30 k à 10 %, 30 k entre 4 et 20 %.

→ Au moment où le défendeur consent un prêt de 9 000 $ sans intérêt ni formalisme, la demanderesse porte elle-même 400 000 $ de dette à des taux de 2,5 % à 20 %. Le contraste établit le degré de confiance/solidarité financière, incompatible avec une relation « invivable ».

> Note de correction : l'analyse `argument paragraphes 4 5 6.md` indiquait « taux entre 4 % et 20 % » — exact pour la tranche de 30 k, mais le gros (320 k) est à 2,5 %. Plaider la décomposition complète ci-dessus, plus précise.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `ChatSequence` **8** — Voyage Cuba 2013 (6 messages)

#### V014 · `piece_chatsequence-8.md` **C1**
*Dynamique familiale positive — « nous 4 » (4 nov. 2014)*

- **source** — `ChatSequence` **8** — Voyage Cuba 2013 (6 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise : « le temps consacrés à nous 4… c'est assez important c'est vraiment dommage » · « c'est la première fois que tu investis dans un voyage ça me fait plaisir que tu le fasses »

→ la référence à « nous 4 » (les deux parents et les deux enfants) et le plaisir exprimé en novembre 2014 sont incompatibles avec une relation « très difficile » structurelle depuis 2009.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `ChatSequence` **9** — Admission du pret et de l'arrangement (1 messages)

#### V015 · `piece_chatsequence-9.md` **C1**
*La demanderesse confirme la nature du prêt de 9 000 $ (crédit de loyer)*

- **source** — `ChatSequence` **9** — Admission du pret et de l'arrangement (1 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise (4 nov. 2014) : « je ne peux pas financièrement supporter toutes les dépenses d'opération sous prétexte que je te dois de l'argent… ce n'étais pas notre entente, le 9000 était du loyer »

→ la demanderesse reconnaît elle-même que le prêt de 9 000 $ était un arrangement de loyer (remboursable par crédit, sans intérêt en preuve).
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `ChatSequence` **10** — Pret additionel de 100 junior (5 messages)

#### V016 · `piece_chatsequence-10.md` **C1**
*La demanderesse emprunte 1 000 $ au défendeur (nov. 2014)*

- **source** — `ChatSequence` **10** — Pret additionel de 100 junior (5 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > Élise (3 nov. 2014) : « est ce que je peux t'emprunter 1000$ et te le donner en 4 paiements de 250$? Je n'Ai pas d'Autres options en ce moment… car je dois payer ce que je dois à junior »
> Élise (4 nov. 2014) : « est ce que aussi tu pourrais regarder pour le 1000$? Junior me court après… » — LP : « je peux te donner 800 jeudi »

→ trois mois après le prêt de 9 000 $, la demanderesse sollicite un emprunt additionnel auprès du défendeur — niveau de confiance financière incompatible avec une relation hostile/invivable.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `ChatSequence` **11** — Journé familiale (3 messages)

#### V017 · `piece_chatsequence-11.md` **C1**
*Projet de tradition familiale mensuelle (13 fév. 2015)*

- **source** — `ChatSequence` **11** — Journé familiale (3 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > > LP : « on devrait faire une journee famille par mois qu'en penses tu? » — Élise : « oui pour la journée familiale » · « on ira à la cabane à sucre en mars »
> (En amont, même séquence : Élise propose d'aller au cinéma « les 4 » et de manger au restaurant après — voir séq. 3 C7 / le fil du 13 fév.)

→ dix jours avant la séparation, les parties planifient des activités familiales mensuelles récurrentes. On ne planifie pas une tradition familiale avec un conjoint dont on affirme ensuite, sous serment, que la vie commune était « devenue impossible » (§4) ou « très difficile depuis la naissance » (§5).
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `ChatSequence` **12** — Activité enfants (38 messages)

#### V018 · `piece_chatsequence-12.md` **C1**
*Les parents discutent d'activités organisées par sessions*

- **source** — `ChatSequence` **12** — Activité enfants (38 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > Les activités nommées dans l'échange comprennent la natation, la gymnastique, la danse, le cheerleading et le ski.

LP demande notamment :

> « 3X par annes right »

Puis, au sujet de la gymnastique, Élise répond :

> « non y a 3 sessions aussi »

Ces messages documentent que les activités sont comprises par les parents comme des engagements cycliques, répartis en plusieurs sessions dans l'année, et non comme des événements isolés.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V019 · `piece_chatsequence-12.md` **C2**
*Discussion parentale sur la participation de Nicolas*

- **source** — `ChatSequence` **12** — Activité enfants (38 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > LP demande :

> « Nicolas fait de la gym? »

Élise répond :

> « en janvier oui »
>
> « a 2 ans »

LP exprime ensuite une réserve :

> « il trop jeune »

Élise répond qu'elle ne partage pas cette appréciation, mais indique qu'elle ne s'obstinera pas. L'échange établit donc :

1. que LP connaît et vérifie les activités prévues pour Nicolas;
2. qu'il s'intéresse au moment où l'enfant commencera;
3. qu'il formule une opinion fondée sur son âge;
4. qu'Élise répond à cette opinion dans le cadre d'une discussion parentale.

La séquence ne permet pas de déterminer si l'inscription future de Nicolas à la gymnastique a finalement été réalisée.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V020 · `piece_chatsequence-12.md` **C3**
*Adaptation du programme d'activités*

- **source** — `ChatSequence` **12** — Activité enfants (38 messages)
- **cible** — `ChatSequence` — nouvelle séquence restreinte aux messages cités
- **contenu cité** — 
  > Élise écrit :

> « cheerleading ce sera le ski en janvier »

Ce message documente une substitution planifiée entre deux activités et montre que le programme des enfants est discuté dans le temps, en fonction des prochaines sessions.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Email` **295** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16

#### V049 · `piece_photo-4558.md` **C2**
*LP a épuisé la totalité de son congé exclusif (5 sem.) et en a même ajouté 2*

- **source** — `Email` **295** — « Re: Visite », "Élise " <elise.ayoub@gmail.com>, 2016-09-16
- **cible** — `PhotoDocument` — description/transcription du fragment
- **contenu cité** — 
  > > Paternité (non partageables) : max. 5 — accordées à LP : 5 ; versées : 5. Modification 2010/07/31 : « Ajout de 2 semaines de Paternité ».

Analyse : LP a pris 100 % des semaines auxquelles il avait droit à titre exclusif, et a activement demandé l'ajout de 2 semaines. C'est l'inverse d'un désengagement : il a maximisé sa présence dans les limites du congé qui lui restait accessible (les 32 partageables étant déjà attribuées à la mère).

Contextes d'usage :
- §14-17 (faits_par14-17_2015.md Axe 3, glissement causal) : l'inégalité de temps de soins durant la petite enfance d'Alexia découle de l'allocation du congé (32-0), non du désengagement — réfute directement l'énoncé d'Élise « ta participation n'a jamais été de 50 %, même quand Alexia était bébé pendant les 13 mois » (Email id=295, thread-6).
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Photo` **4551**

#### V198 · `piece_photo-4551.md` **C1**
*Écrement est une PSYCHOLOGUE (consultée par la demanderesse), non une médiatrice*

- **source** — `Photo` **4551**
- **cible** — `PhotoDocument` — description/transcription du fragment
- **contenu cité** — 
  > > Signature : « Claudia Écrement, Psy.D., Psychologue, Co-Propriétaire, Clinique de psychologie St-Lambert. »

Analyse : Écrement est psychologue. Les §§28 et 29 décrivent cette même intervention. La qualification de « médiation » ne correspond ni à sa signature professionnelle ni à sa description expresse de l'intervention.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V199 · `piece_photo-4551.md` **C2**
*Le seul refus : ne pas rencontrer Écrement « concernant la garde », à la demande du père*

- **source** — `Photo` **4551**
- **cible** — `PhotoDocument` — description/transcription du fragment
- **contenu cité** — 
  > > « Je ne rencontrerai pas le père concernant la garde des enfants finalement, à sa demande. »

Analyse : il s'agit du refus documenté que les §§28 et 29 présentent ensemble. Le §29 en identifie l'intervenante et la portée ciblée; le §28 le requalifie en refus de « séances de médiation ».
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V200 · `piece_photo-4551.md` **C3**
*Coopération : le père permet à Écrement de continuer à voir les enfants*

- **source** — `Photo` **4551**
- **cible** — `PhotoDocument` — description/transcription du fragment
- **contenu cité** — 
  > > « Il me permets toutefois de continuer à voir vos enfants si nécessaire. »

Analyse : le défendeur autorise la poursuite des services aux enfants. Son refus porte sur une rencontre le concernant au sujet de la garde. Cette coopération limitée est documentée par la pièce de la demanderesse elle-même.

Contextes d'usage :
- §28-29 (faits_par28-29_2015.md) : événement unique; §29 concédé dans son contenu complet; fausse requalification au §28; coopération ciblée documentée (C3).
- §26 : contredit le « de consentement entre les parties » (le père a refusé de rencontrer Écrement sur la garde → non consenti).
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `Photo` **4558**

#### V201 · `piece_photo-4558.md` **C1**
*Le congé parental PARTAGEABLE a été attribué 32-0 (Élise-LP)*

- **source** — `Photo` **4558**
- **cible** — `PhotoDocument` — description/transcription du fragment
- **contenu cité** — 
  > > Prestations parentales (partageables) : max. 32 semaines — accordées au demandeur (LP) : 0 ; accordées à l'autre parent (Élise) : 32 ; versées à LP : 0.

Analyse : les 32 semaines de congé parental partageables — la portion qui pouvait revenir au père — ont été attribuées en totalité à la mère. LP n'en a reçu aucune. La présence quasi exclusive de la mère auprès d'Alexia durant la petite enfance résulte donc de l'allocation du congé, non d'un choix du père de ne pas s'impliquer. Contrainte objective et documentée par un registre gouvernemental.
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


### `PhotoDocument` **17** — Déclaration revenus 2019 (1 photos)

#### V202 · `piece_photodoc-17.md` **C1**
*les DEUX chiffres litigieux sortent de CETTE déclaration : 112 569,08 = revenu total (l. 199) ; 99 271,79 = revenu NET (l. 275)*

- **source** — `PhotoDocument` **17** — Déclaration revenus 2019 (1 photos)
- **cible** — `PhotoDocument` — description/transcription du fragment
- **contenu cité** — 
  > - 112 569,08 $ = revenu total (ligne 199). C'est le montant que le père a inscrit pour la mère à la ligne 200 « Salaire brut » de son formulaire (piece_pdf-82.md / piece_photodoc-18.md).
- 99 271,79 $ = revenu NET (ligne 275), soit le revenu total moins 13 297,29 $ de déductions (dont RPA 12 118,29 $ + déduction pour travailleur 1 150 $ + REER 29 $). C'est le montant qu'Élise a inscrit pour elle-même à la ligne 200 « Salaire brut » de son formulaire (piece_pdf-16.md).
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V203 · `piece_photodoc-17.md` **C2**
*le formulaire de pension demande le revenu, PAS le revenu net*

- **source** — `PhotoDocument` **17** — Déclaration revenus 2019 (1 photos)
- **cible** — `PhotoDocument` — description/transcription du fragment
- **contenu cité** — 
  > La Partie 2 du formulaire Annexe I (a.3) demande d'« indiquer les revenus […] conformément à la déclaration fiscale » — c'est-à-dire le revenu total (l. 199). Les déductions (base, cotisations syndicales/professionnelles) se retranchent séparément à la Partie 3. En portant son revenu net (l. 275) à la ligne 200, Élise sous-déclare son revenu de 13 297,29 $ et retranche deux fois ses déductions (une première fois en amont via le net, une seconde fois à la Partie 3 : cotisations syndicales 1 055,32 $ + professionnelles 1 015,18 $).

---
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter


---

## 4. Source à trancher (2)

Le fichier couvre plusieurs sources et le texte cité n'a pas pu être rattaché à l'une d'elles avec certitude.

#### V204 · `piece_thread-16_ecrement_2015.md` **C2**
*Écrement travaille avec / pour la mère [id=174, id=177]*

- **source** — ⚠️ **source à trancher**
- **cible** — à déterminer
- **contenu** — 
  > J'ai vu la mère des enfants seule à seule cette semaine.
- **attribution retirée du texte** — id=174
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter

#### V205 · `piece_thread-16_ecrement_2015.md` **C4**
*Refus ciblé (la garde) + soutien des services aux enfants [id=180, id=178]*

- **source** — ⚠️ **source à trancher**
- **cible** — à déterminer
- **contenu** — 
  > je souhaites annuler mon rendez vous du 19. Je suis bien heureux que mes enfants aient pu profiter de vos services.
- **attribution retirée du texte** — id=180
- `[ ]` créer &nbsp; `[ ]` corriger &nbsp; `[ ]` écarter
