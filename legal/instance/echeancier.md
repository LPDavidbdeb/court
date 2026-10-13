# Échéancier — source unique

> **Règle.** Aucune date ne se calcule ailleurs que dans ce fichier. Si une date
> apparaît dans un courriel, une lettre adverse ou une conversation, elle est
> vérifiée ici avant d'être tenue pour vraie — y compris quand c'est une
> avocate qui l'annonce.

Dernière mise à jour : **7 octobre 2026** — **Me Marie-Josée Ayoub est désormais
représentée** par Timmons Séguin Tremblay, contentieux du **Fonds d'assurance
responsabilité professionnelle du Barreau du Québec** (substitution signifiée ce
jour). Ils annoncent un **projet de protocole** et **réclament les pièces**.
Élise Marie Ayoub demeure non représentée. **Le demandeur réécrit sa demande**
avant de communiquer — paragraphes et cotes renumérotés, texte entièrement
réécrit, fond inchangé (`communication_pieces.md` § 10). Prochaine échéance :
**protocole, 1er novembre** — c'est là que s'inscrivent le calendrier de
l'amendement et les délais de l'art. 207.

## 1. ✅ Le verrou est franchi — signification faite le 17 septembre 2026

Pièce : `PDFDocument` **id=101** — « Preuve signification huissier », Darveau et
Associé, huissiers de justice (Luc Darveau, permis # 189). Transcription
intégrale dans le champ `ai_analysis`.

| Destinataire | Date et heure | Lieu | Mode |
|---|---|---|---|
| **Élise Marie Ayoub** | 17 sept. 2026, **8 h 10** | 245 av. Macaulay, Saint-Lambert | **au destinataire personnellement à son domicile** (art. 116 C.p.c., 1er al.) — mains propres |
| **Me Marie-Josée Ayoub** | 17 sept. 2026, **8 h 40** | 1091 rue Gendron, Longueuil | **sous pli cacheté, fixé à la porte du domicile** (art. 116, 1er al. cité) |

Ce qui a été signifié : la demande introductive d'instance, la **liste** des
pièces et l'**avis d'assignation**.

| | |
|---|---|
| Dépôt au greffe | 24 juillet 2026 |
| **Signification** | **17 septembre 2026** |
| Cible prudentielle (ancre assermentation) | 19 septembre 2026 — **respectée** |
| Falaise art. 2892 (ancre connaissance) | 23 septembre 2026 — **respectée** |

**✅ L'interruption de prescription est acquise. C'est le verrou n° 1 du recours,
et il est franchi.**

### Le procès-verbal visant Me Ayoub — analyse recalibrée (17 sept.)

Le procès-verbal 32994-1-2-1 certifie **de façon disjonctive** : « attendu qu'il
n'y a personne pour recevoir ladite signification **ou s'il y a quelqu'un il
refuse d'ouvrir les portes afin de l'éviter ».

**⚠️ D'abord, dissiper une fausse condition : l'art. 116 ne compte pas les
tentatives.** Il pose une cascade de **modes** assortie d'une condition
d'impossibilité — en mains propres, *si ce n'est pas possible* à une personne
apte au domicile, *si le document ne peut être remis ainsi* sous pli cacheté
dans un endroit approprié. Le cran 3 s'ouvre par **l'impossibilité des deux
premiers**, constatée le 17 sept. à 8 h 40 — pas par un nombre de visites. Les
« 2 tentatives » convenues avec l'huissier étaient un arrangement **pratique**,
jamais un seuil légal. La route du 16 sept. **corrobore** la diligence ; elle ne
fonde pas la validité.

**Ensuite, la disjonction n'est pas davantage un défaut.** Les deux branches mènent au même
constat : **personne n'a reçu le document** — donc la remise en mains propres a
échoué et la remise à une personne apte aussi. La condition d'ouverture du mode
résiduel est remplie **quelle que soit la branche vraie**. Ce que l'ambiguïté
coûte, c'est une **meilleure** qualification : si quelqu'un était présent et a
refusé, cela pourrait valoir **refus de recevoir**, donc signification à
personne. On perd une promotion, pas l'acte.

**Trois raisons de tenir la signification pour solide :**

1. Le procès-verbal est un **acte authentique** : contester que l'huissier a
   apposé le pli cacheté à la porte exigerait une **inscription de faux**.
2. La cascade est satisfaite dans les deux branches (ci-dessus).
3. ✅ **La purge a eu lieu.** Me Ayoub a répondu le **29 septembre** : elle
   conteste, et **ne formule aucune objection à la signification**. Sa
   comparution couvre toute irrégularité du mode employé le 17 septembre à
   8 h 40. **Le point faible de la signification est refermé** — non par un
   argument, mais par son propre acte.

**Ce qui reste à faire — assurance, pas réparation :**

- [ ] **Procès-verbal complémentaire** de Me Darveau : ce qu'il a constaté le
      17 sept. à 8 h 40, et la qualification des routes du 16 sept. (14 h 47 et
      15 h 28). ⬇️ **Priorité retombée au 29 sept.** : la comparution sans
      objection de Me Ayoub purge l'irrégularité que ce PV devait corroborer.
      Reste une assurance peu coûteuse contre un revirement, plus une urgence.
      → `sortants/2026-09-17_huissier_demande-pv-complementaire.md`
- [x] **Preuve de signification déposée au greffe le lundi 21 septembre
      2026** (Palais de justice de Longueuil, dossier 505-17-016235-261). Elle
      est donc au dossier avant l'échéance du 2 octobre : la condition
      préalable à toute démarche fondée sur le défaut de répondre est remplie.
- [ ] Geler la pièce 101 (procès-verbaux + facture) dans `legal/depots/`, sur
      le modèle de `2026-07-24_initial/` — empreinte SHA-256 et README. **Pas
      fait** : `legal/depots/` ne contient toujours que l'archive du dépôt.
      Aucune échéance propre, mais c'est la seule pièce qui établit
      l'interruption de prescription.
- [ ] Acquitter le **solde de 25,30 $** de la facture 358300.

~~**Écarté (décision LP, 17 sept.)** : seconde signification à l'étude de
Me Ayoub.~~ **Sans objet depuis le 29 septembre** : elle a comparu. *(Pour
mémoire : l'adresse d'étude que le dossier tenait pour périmée est en fait
active — elle l'élit elle-même comme adresse de notification, 425 rue
Saint-Sulpice, Montréal. La décision de ne pas y signifier reposait sur une
incertitude réelle au 17 septembre et n'a rien coûté.)*

## 2. Délais déclenchés par la signification du 17 septembre 2026

Source : l'avis d'assignation signifié (art. 145 et s. C.p.c.).

| Événement | Délai | **Échéance** |
|---|---|---|
| ~~**Réponse à l'assignation** par chaque défenderesse~~ | ~~15 j~~ | ✅ **reçues des deux le 29 septembre 2026** |
| **Protocole de l'instance** déposé au greffe | 45 j | **dimanche 1er novembre 2026** — reporté au premier jour ouvrable suivant s'il y a lieu |
| Conférence de gestion possible | 20 j du dépôt du protocole | à défaut, **protocole présumé accepté** |

> ⚠️ **Le protocole est aussi notre obligation.** Il s'établit « en
> coopération » ; leur silence ne suspend rien. À défaut d'entente, déposer
> notre propre proposition avant l'échéance, avec la trace des démarches. Voir
> [`protocole_instance.md`](protocole_instance.md).

> ✅ **La voie du défaut est fermée.** Les deux défenderesses ont répondu le
> 29 septembre. Plus rien ne dépend du 2 octobre.

## 3. Délais qui courent déjà

| Règle | Objet | Échéance | Sanction |
|---|---|---|---|
| ~~Art. 2892 C.c.Q.~~ | ~~signification~~ | ~~23 sept. 2026~~ | ✅ **satisfait le 17 sept. 2026** |
| **Art. 133 al. 2 C.p.c.** | ⚠️ **le consentement d'Élise est requis** pour lui notifier par un moyen technologique — elle n'est pas représentée. Demandé dans la lettre du `sortants/` | avec la lettre | une notification par courriel sans son consentement serait attaquable |
| **Art. 147 al. 3 C.p.c.** | 🔴 **informer TOUTES les parties des réponses reçues et du nom de leurs avocats** — deux défenderesses assignées, les deux ont répondu le 29 sept. | **court depuis le 29 sept.** | manquement du demandeur, matière à leur art. 51-54 |
| Art. 145 al. 1 C.p.c. | **communication des pièces** aux défenderesses, « dans les plus brefs délais » | dès la signification | reproche de manque de coopération, matière à leur art. 51-54 |
| ~~Art. 107 C.p.c.~~ | ~~notification dans les 3 mois du dépôt~~ | ~~24 oct. 2026~~ | ✅ **satisfait le 17 sept. 2026** |

**La communication des pièces est l'obligation la plus immédiate et la plus
facile à nous reprocher** : le bordereau compte plus de 107 pièces. À organiser
dès la signification faite, pas après la réponse.

## 4. Où en sommes-nous — et le parcours d'ici l'audition

**Position au 29 septembre 2026 : J+12 de la signification.** Les deux
défenderesses ont répondu **le même jour**, à 42 minutes d'intervalle, trois
jours avant l'échéance. Le dossier est **contesté par les deux**, chacune se
représentant elle-même. La prochaine échéance est le **protocole de l'instance,
1er novembre**.

### 4.1 L'étape franchie — les deux réponses à l'assignation

**Les deux défenderesses ont répondu le 29 septembre 2026**, séparément, par
courriel, sous bordereau invoquant l'art. 134 C.p.c. Leurs actes sont au dossier,
horodatés et empreintés.

| Défenderesse | Reçue | Position | Représentation | Adresse élue |
|---|---|---|---|---|
| **Élise Marie Ayoub** | 13 h 45 (v1) et **13 h 52 (v2)** | **conteste** + coopérera au protocole | **seule** | 245, rue Macaulay, Saint-Lambert |
| **Me Marie-Josée Ayoub** | **14 h 27** | **conteste** + coopérera au protocole | seule *(à cette date — **remplacée le 5 oct.**, voir ci-dessous)* | 425, rue Saint-Sulpice *(à cette date)* |

Fiches : [`entrants/2026-09-29_elise_reponse-assignation.md`](entrants/2026-09-29_elise_reponse-assignation.md)
et [`entrants/2026-09-29_ayoub_reponse-assignation.md`](entrants/2026-09-29_ayoub_reponse-assignation.md).

**Les §§ 2 et 3 des deux actes sont identiques mot pour mot** : intention de
contester, engagement de coopérer à l'établissement du protocole, réserve de
tous droits. Seul le § 1 diffère, et seulement par la mention des coordonnées
professionnelles.

#### 🔴 Mise à jour du 7 octobre — Me Ayoub est représentée

| Défenderesse | Représentation au 7 oct. | Tout lui est adressé |
|---|---|---|
| **Élise Marie Ayoub** | **non représentée** — inchangé | elle-même, 245 rue Macaulay · `elise.ayoub@gmail.com` |
| **Me Marie-Josée Ayoub** | 🔴 **représentée** depuis le 5 oct. — avis de substitution (art. 194 C.p.c.) signifié par huissier le 7 oct. | **Me Patricia Timmons, Timmons Séguin Tremblay**, 445 boul. Saint-Laurent, b. 300, Montréal H2Y 3T8 · `patricia.timmons@farpbq.ca` |

Timmons Séguin Tremblay est le **contentieux du Fonds d'assurance responsabilité
professionnelle du Barreau du Québec**, et leur lettre précise qu'ils
représentent **uniquement** Me Marie-Josée Ayoub.

⚠️ **Plus rien ne va directement à Me Ayoub.** Ni son étude, ni son domicile, ni
`mjayoub@ayoubavocats.ca`.

⚠️ **La prise en charge par un assureur n'est aucune admission** — ni de
couverture, ni de la nature professionnelle des actes reprochés. Les documents ne
disent rien de la position du Fonds. Ne jamais l'écrire ni le plaider. Analyse :
[`analyses/2026-10-07_substitution-farpbq-et-demandes-timmons.md`](analyses/2026-10-07_substitution-farpbq-et-demandes-timmons.md).

#### Ce que ces deux réponses règlent

| Question ouverte hier | Réglée comment |
|---|---|
| Branche procédurale | **Contestation** pour les deux → protocole au 1er nov. ; la communication des pièces s'engage pleinement |
| Voie du défaut | **Fermée.** Plus rien ne dépend du 2 octobre |
| Destinataires | **Chacune pour elle-même**, aux adresses ci-dessus. Aucune ne représente l'autre |
| Conflit d'intérêt (punitifs divergents) | **Ne se pose plus en pratique** : aucune ne prétend occuper pour l'autre |
| ✅ Irrégularité de la signification du 17 sept. à 8 h 40 | **Purgée.** Me Ayoub comparaît **sans formuler d'objection à la signification**. Le seul point faible de l'acte est refermé par son propre geste |
| Moyens préliminaires | **Aucun n'est annoncé** dans les deux actes. Ils se dénoncent au protocole — l'attente de `pieges.md` § A.1 et A.2 reste entière |

#### ⚠️ Ce qui reste ouvert, et qui n'est pas dans les actes

- **Le dépôt au greffe.** Les deux ont *notifié* au demandeur. La notification ne
  vaut pas dépôt. → vérifier au **plumitif** que les deux RÉPONSES y sont.
- **La v1 d'Élise**, qui déclarait qu'elle était représentée par Me Marie-Josée
  Ayoub avant d'être remplacée sept minutes plus tard. **Rien à écrire là-dessus**
  — valeur latente seulement :
  [`analyses/2026-09-29_reponse-elise-et-representation-retractee.md`](analyses/2026-09-29_reponse-elise-et-representation-retractee.md).

### 4.2 Le protocole de l'instance (1er novembre → lundi 2 novembre)

Le premier vrai champ de bataille, et celui qu'un non-avocat perd sans s'en
apercevoir : positions arrêtées dans
[`protocole_instance.md`](protocole_instance.md). Il se dépose **même sans
entente**, avec la trace écrite des démarches de coopération.

🔴 **Changement du 7 octobre : ce sont eux qui tiennent la plume.** Timmons
Séguin Tremblay annonce un projet « où nous aurons complété notre partie afin
que vous puissiez compléter la vôtre ».

**Le piège est entier dans cette formule.** Elle présente le protocole comme un
formulaire à deux colonnes. Ce n'en est pas un : il fixe la forme de la défense,
les interrogatoires préalables, le calendrier et le sort des moyens
préliminaires — et **à défaut de conférence de gestion dans les 20 jours de son
dépôt, il est présumé accepté**. Un document arrivant à moitié rempli exerce une
pression de défaut : chaque rubrique déjà remplie se présente comme acquise.

**Règle de travail** : quand leur projet arrive, il se lit **contre la liste de
`protocole_instance.md`, rubrique par rubrique** — jamais dans l'ordre où il
arrive, et jamais en remplissant les cases laissées en blanc. Les trois positions
qui ne se négocient pas : défense **écrite**, interrogatoires **réciproques et
plafonnés**, et **refus que la prescription soit tranchée sur un dossier nu**
avant communication des pièces.

### 4.3 Ce qui vient après — ⚠️ voir la carte, pas ce tableau

🔴 **Les projections qui figuraient ici étaient périmées et fausses** (« ~21
novembre », « ~21 mai 2027 », « audition 2027-2028 »). Elles avaient été
calculées avant la lecture des art. 83, 152, 173 et 177 au Code, et ce fichier
porte pourtant la règle « aucune date ne se calcule ailleurs ». Deux fichiers
divergents, dont l'un se dit source unique, est pire que pas de projection.

➜ **La succession complète des étapes, leurs délais lus au Code, et les
scénarios de dates vivent désormais dans
[`carte_de_l_instance.md`](carte_de_l_instance.md).** Ce § n'en retient que ce
qui gouverne.

| Ce qui gouverne | Source | Date |
|---|---|---|
| **Protocole ou proposition de protocole déposé** | 148, 149, **152** | 🔵 **lundi 2 novembre 2026** |
| Mise en état + demande d'inscription — **délai de rigueur** | 173 | 6 mois de l'acceptation ; **17 mars 2027** si le protocole est manqué |

⚠️ **Tout le reste est scénario.** Les dates d'acceptation, de mise en état et
d'instruction dépendent de dates de dépôt qui n'existent pas encore. Aucune ne
se cite comme acquise.

#### 🔴 Les deux points où une inaction éteint l'action

Le dossier en compte deux. Le premier est connu depuis juillet. **Le second a
été identifié le 13 octobre 2026** et n'était nulle part.

| | Chaîne |
|---|---|
| **1. Prescription** | dépôt tardif ou signification hors des 60 j → pas d'interruption (2892 C.c.Q.) |
| **2. Désistement présumé** | défaut de demander l'inscription dans le délai de rigueur → **désistement présumé** (177 C.p.c.) → **« L'interruption n'a pas lieu s'il y a […] désistement »** (**2894 C.c.Q.**) → le recours retombe sous une prescription expirée depuis juillet 2026 |

**La seconde chaîne reconduit à la première.** Elle ne coûte pas du temps : elle
défait rétroactivement le verrou franchi le 17 septembre. ⚠️ Et le délai de grâce
de trois mois de l'art. 2895 C.c.Q. vise le **rejet** de la demande, **pas le
désistement** — à vérifier avant de compter dessus.

**Première comparution réelle.** Les moyens préliminaires s'annoncent au
protocole (art. 148, 1°) et se plaident à une date fixée en gestion :
irrecevabilité pour prescription (`pieges.md` § A.1, *quasi certain*) et rejet
pour abus (§ A.2, *très probable*). **C'est là que le dossier se gagne ou se
perd**, pas à l'audition au fond.

### 4.4 Ce qui est en retard maintenant

| Obligation | État |
|---|---|
| **Communication des pièces** (art. 145 al. 1, « dans les plus brefs délais ») — 107+ pièces ; seule la **liste** a été signifiée le 17 sept. | 🔴 **Réclamée par écrit le 5 octobre.** ⏳ Court depuis le 17 septembre. **Le demandeur réorganise et renumérote** : le délai doit être rendu **consenti** (offre écrite + choix laissé à l'adverse) puis **inscrit au protocole** — `communication_pieces.md` § 10.3. Le manquement le plus facile à nous reprocher et le plus directement utile à leur art. 51-54 (`pieges.md` § C.1). Destinataires, modalités et ordre arrêtés dans [`communication_pieces.md`](communication_pieces.md) ; lettre de modalités en projet au `sortants/`. |
| Procès-verbal **complémentaire** de Me Darveau | ⬇️ **Priorité retombée** : la comparution sans objection de Me Ayoub purge ce que ce PV devait corroborer. Assurance résiduelle, plus une urgence |
| Gel de la pièce 101 dans `legal/depots/` | ⏳ non fait |
| Solde de 25,30 $ — facture 358300 | ⏳ |

---

## 5. Journal des modifications de l'échéancier

| Date | Modification | Cause |
|---|---|---|
| 2026-09-16 | Création. Falaise 2892 corrigée de 19 à 23 sept. | Le point de départ des 60 j est l'expiration de la prescription, pas le dépôt. |
| 2026-09-17 | **Signification faite aux deux défenderesses.** Art. 2892 et art. 107 satisfaits. Délais de réponse (2 oct.) et de protocole (1er nov.) figés. | Procès-verbaux de Me Luc Darveau, `PDFDocument` id=101. |
| 2026-09-28 | Preuve de signification **déposée au greffe le 21 sept.** Ajout du § 4 : position à J+11, scénarios du 2 octobre, parcours jusqu'à l'audition, retards en cours. | Apport du demandeur, 28 sept. 2026. |
| 2026-09-28 | § 4.1 : ajout du bloc **« aucune comparution le 2 octobre »**, avec le verbatim de l'avis d'assignation signifié et la vérification du plumitif à faire ce jour-là. | Question du demandeur sur une éventuelle présence au palais le 2 oct. |
| 2026-09-28 | Création de [`communication_pieces.md`](communication_pieces.md) : destinataires (les **deux parties séparément**, non représentées à ce jour), pas de dépôt au greffe, ordre de communication. | Question du demandeur sur le destinataire des 107 pièces. |
| 2026-10-13 | 🔴 **§ 4.3 purgé.** Les projections (~21 nov., ~21 mai 2027, « 2027-2028 ») étaient fausses et contredisaient la carte, dans le fichier qui se déclare source unique des dates. Remplacées par ce qui gouverne, le reste renvoyé à `carte_de_l_instance.md`. **Ajout de la seconde chaîne d'extinction** : art. 177 C.p.c. → art. 2894 C.c.Q. | Relecture critique apportée par le demandeur, 13 oct. |
| 2026-10-13 | **Lettre à Élise rédigée** (`sortants/2026-10-13_…`), alignée sur celle à Timmons. ⚠️ Une différence de fond : **art. 133 al. 2 C.p.c.** — la notification par moyen technologique à une partie **non représentée** exige **son consentement** ; il lui est donc demandé expressément. Échéance de réponse portée au **27 octobre** pour ne pas presser une partie non représentée. L'ancienne lettre du 28 sept. est marquée **supersédée**. | Lecture du Code, 13 oct. |
| 2026-10-07 | 🔴 **Obligation de l'art. 147 al. 3 C.p.c. relevée** (texte lu au Code) : le demandeur doit informer **toutes les parties** des réponses reçues et du nom de leurs avocats. Elle court depuis le 29 septembre et n'était pas remplie. Portée dans les deux lettres du `sortants/`. | Lecture du Code à la demande du demandeur, 7 oct. |
| 2026-10-07 | **Réécriture intégrale de la demande décidée par le demandeur** : paragraphes renumérotés **et réécrits**, cotes renumérotées, pièces additionnelles ; fond inchangé. Deux balayages de concordance obligatoires et **préalable bloquant** : fixer lequel des 5 candidats du dépôt fait référence (47 paragraphes sur 179 diffèrent entre le `.md` et l'imprimé). Méthode, garde-fous de prescription et concordance sur `model:pk` → `communication_pieces.md` § 10 ; inscription au protocole → `protocole_instance.md` § 8. Le demandeur **n'a pas de téléphone** (§ 11) ; sa situation financière **ne se divulgue pas**. | Apport du demandeur, 7 oct. 2026. |
| 2026-10-07 | **Me Ayoub est représentée** : Timmons Séguin Tremblay (contentieux du Fonds d'assurance du Barreau) substitués à Ayoub Avocats Inc., avis signifié par huissier. Destinataire changé (§ 4.1) ; **le projet de protocole viendra d'eux** (§ 4.2) ; **les pièces sont réclamées** (§ 4.4). Élise reste non représentée. | `entrants/2026-10-07_timmons_substitution-et-demande-pieces.md` |
| 2026-09-29 | **Réponse de Me Marie-Josée Ayoub reçue** (14 h 27). Les DEUX défenderesses contestent et se représentent seules. § 4.1 réécrit ; voie du défaut fermée (§ 2) ; **purge de la signification acquise** (§ 1) et priorité du PV complémentaire **retombée** (§ 4.4) ; adresse de Me Ayoub = son **étude**, 425 rue Saint-Sulpice, Montréal. | `entrants/2026-09-29_ayoub_reponse-assignation.md` |
| 2026-09-29 | **Réponse d'Élise Marie Ayoub reçue** (29 sept., courriel) : conteste, **se représente seule** → branche contestation réalisée à son égard. **Me Ayoub n'a pas répondu** (échéance 2 oct.). Ajout de l'état des deux branches au § 4.1 ; priorité du PV complémentaire relevée au § 4.4. | `entrants/2026-09-29_elise_reponse-assignation.md` ; analyse du 29 sept. |
| 2026-09-28 | **§ 4 réécrit — la réponse du 2 oct. est un point de bifurcation, pas seulement une adresse.** L'avis rattache le protocole à la seule branche « contester » : dans deux des trois branches (règlement/médiation, défaut), l'envoi des pièces aux défenderesses n'est pas l'acte suivant — au défaut, la preuve va au **tribunal**. Séquence corrigée (§ 6) : **lettre seule maintenant, pièces après le 2 octobre.** | Objection du demandeur : attendre la réponse, ou son absence, avant d'envoyer les pièces. |
| 2026-09-28 | § 4 b (devenu § 4.6) : « convenues » **est** une obligation bilatérale, avec chemin d'escalade lettre → protocole (1er nov.) → conférence de gestion. Le silence n'équivaut pas à consentement, il épuise le devoir de coopération. Clause d'accommodement ajoutée à la lettre. | Objection du demandeur : la convention implique une communication. |
| 2026-09-28 | § 2 de `communication_pieces.md` : **ni impression, ni huissier** — distinction signification / communication, et décompte des cotes dont la métadonnée porte le fait (67 sur 106). | Question du demandeur sur l'impression et l'envoi par huissier. |
| 2026-09-28 | **Révision du support et de la séquence** : le numérique est retenu parce que la métadonnée porte la preuve (EXIF, en-têtes), pas seulement pour le volume → §§ 3 et 7 de `communication_pieces.md`. **Aucune raison d'attendre leur réponse** (§ 4) ; la lettre et le lot 1 partent **ensemble** (§ 6), et non l'une puis l'autre. | Apport du demandeur sur la valeur probante des métadonnées. |
