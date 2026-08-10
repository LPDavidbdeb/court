# Chevauchement des citations et contexte d'usage

Généré par `docs/purge_quotes/analyse_chevauchements.py`. Lecture seule.

Objet : séparer les **blocs simples** (un passage atomique) des **compositions** (un passage qui en contient d'autres, ou qui recolle des fragments non contigus). Une composition réintroduit sa prémisse comme citation distincte : c'est la perte de rigueur à corriger avant de reconstruire.

## 1. Répartition

| Classe | Courriels | PDF |
|---|---|---|
| COMPOSITION | 13 | 19 |
| COMPOSITION (et incluse ailleurs) | 2 | 5 |
| bloc simple, repris dans une composition | 16 | 25 |
| CHEVAUCHEMENT PARTIEL | 2 | 0 |
| DOUBLON | 14 | 4 |
| bloc simple isole | 134 | 50 |
| *non localisable dans la source* | 31 | — |
| **total** | **211** | **103** |

Citations engagées dans au moins une relation de recouvrement : **47** courriels, **53** PDF.

---

## 2. Détail par source

Chaque groupe ci-dessous rassemble les citations d'une même source qui se recouvrent. `⊃` = contient, `⊂` = incluse dans, `≈` = chevauchement partiel, `=` = identique. La colonne *usage* indique le nombre de fichiers `.md` qui reprennent la citation et les trames qui la citent.

### Courriels

#### email-6 — Re: Visite — 2016-09-16 

- **eq-159** — bloc simple, repris dans une composition — 73 car. [0:73] — usage : 2 fichier(s) .md, trames —
    - ≈ eq-56 37 car. (51%)
    - ≈ eq-114 37 car. (51%)
    - ≈ eq-122 37 car. (51%)
    - ⊂ eq-197 73/224 car.
    - > tu n'en as pas assez de répéter ça? je ne t'ai jamais traiter d'incapable
- **eq-197** — COMPOSITION — 224 car. [0:224] — usage : 2 fichier(s) .md, trames [50]
    - ⊃ eq-56 188/224 car.
    - ⊃ eq-114 187/224 car.
    - ⊃ eq-122 135/224 car.
    - ⊃ eq-159 73/224 car.
    - > tu n'en as pas assez de répéter ça? je ne t'ai jamais traiter d'incapable je t'ai parlé de leur lien d'attachement, je ne t'ai jamais accusé de rien d
- **eq-56** — COMPOSITION (et incluse ailleurs) — 188 car. [36:224] — usage : 2 fichier(s) .md, trames [55]
    - ≈ eq-159 37 car. (51%)
    - ⊃ eq-122 135/188 car.
    - = eq-114 
    - ⊂ eq-197 188/224 car.
    - > je ne t'ai jamais traiter d'incapable je t'ai parlé de leur lien d'attachement, je ne t'ai jamais accusé de rien depuis que tu es parti je ne comprend
- **eq-114** — COMPOSITION (et incluse ailleurs) — 187 car. [36:223] — usage : 2 fichier(s) .md, trames [56]
    - ≈ eq-159 37 car. (51%)
    - ⊃ eq-122 135/187 car.
    - = eq-56 
    - ⊂ eq-197 187/224 car.
    - > je ne t'ai jamais traiter d'incapable je t'ai parlé de leur lien d'attachement, je ne t'ai jamais accusé de rien depuis que tu es parti je ne comprend
- **eq-122** — bloc simple, repris dans une composition — 135 car. [36:171] — usage : 0 fichier(s) .md, trames —
    - ≈ eq-159 37 car. (51%)
    - ⊂ eq-56 135/188 car.
    - ⊂ eq-114 135/187 car.
    - ⊂ eq-197 135/224 car.
    - > [...] je ne t'ai jamais traiter d'incapable je t'ai parlé de leur lien d'attachement, je ne t'ai jamais accusé de rien depuis que tu es parti [...]

#### email-8 — Re: Visite — 2016-09-16 

- **eq-53** — bloc simple, repris dans une composition — 182 car. [380:562] — usage : 3 fichier(s) .md, trames [8, 50]
    - ⊂ eq-110 182/255 car.
    - > peu importe mes accusations du passé tu as decide de ne pas t'en occupe 50% du temps, tu aurais pu decide de te foutre de moi et ce que je te disais e
- **eq-110** — COMPOSITION — 255 car. [380:635] — usage : 2 fichier(s) .md, trames [50, 55]
    - ⊃ eq-53 182/255 car.
    - > peu importe mes accusations du passé tu as decide de ne pas t'en occupe 50% du temps, tu aurais pu decide de te foutre de moi et ce que je te disais e

#### email-10 — Re: Visite — 2016-09-16 

- **eq-102** — COMPOSITION — 573 car. [45:618] — usage : 1 fichier(s) .md, trames —
    - ⊃ eq-106 268/573 car.
    - > ils t'aiment, tu as fais un deuil mais ils ne sont pas morts et sont toujours présents, tu es leur père et ils vont toujours vouloir que tu le sois. m
- **eq-106** — bloc simple, repris dans une composition — 268 car. [269:537] — usage : 1 fichier(s) .md, trames [55, 56]
    - ⊂ eq-102 268/573 car.
    - > c'est dommage que tu les punissent ainsi, ils n'auraient jamais du être le prix de ta déception. ils ne devraient pas être une conséquence, ni une pun

#### email-11 — Assurancesq — 2016-08-03 

- **eq-145** — DOUBLON — 169 car. [0:169] — usage : 0 fichier(s) .md, trames —
    - = eq-198 
    - > bonjour peux tu stp me dire si je dois te donner une copie des reçus ou une copie de mon relevé d'assurances pour que tu puisses réclamer la différenc
- **eq-198** — DOUBLON — 169 car. [0:169] — usage : 0 fichier(s) .md, trames [68]
    - = eq-145 
    - > bonjour peux tu stp me dire si je dois te donner une copie des reçus ou une copie de mon relevé d'assurances pour que tu puisses réclamer la différenc

#### email-21 — (sans objet) — 2015-08-03 

- **eq-31** — DOUBLON — 48 car. [0:48] — usage : 0 fichier(s) .md, trames [3]
    - = eq-194 
    - > bonjour, nicolas est malade je reste a la maison
- **eq-194** — DOUBLON — 48 car. [0:48] — usage : 0 fichier(s) .md, trames [50, 67]
    - = eq-31 
    - > bonjour, nicolas est malade je reste a la maison

#### email-27 — vendredi le 19 dec — 2014-12-19 

- **eq-30** — COMPOSITION — 341 car. [0:341] — usage : 0 fichier(s) .md, trames [3]
    - ⊃ eq-195 187/341 car.
    - > bon après-midi, de toute évidence je ne rentre pas aujord hui, je viens de me lever, je suis désolé de ne pas t'avoir avertis avant! aucun des enfants
- **eq-195** — bloc simple, repris dans une composition — 187 car. [133:320] — usage : 1 fichier(s) .md, trames [67]
    - ⊂ eq-30 187/341 car.
    - > aucun des enfants ni moi avons dormis la nuit dernière, c est au tour de ma fille d'être malade, je serai au bureau lundi, élise ma conjointe va prend

#### email-42 — absence — 2012-09-10 

- **eq-25** — COMPOSITION — 225 car. [0:225] — usage : 0 fichier(s) .md, trames [3]
    - ⊃ eq-190 133/225 car.
    - > bon matin karl, je ne retrerai pas travailler aujourd hui, je vais rester a la maison avec ma petite qui es malade et qui ne dors pas s'il y a quelque
- **eq-190** — bloc simple, repris dans une composition — 133 car. [0:133] — usage : 0 fichier(s) .md, trames [67]
    - ⊂ eq-25 133/225 car.
    - > bon matin karl, je ne retrerai pas travailler aujourd hui, je vais rester a la maison avec ma petite qui es malade et qui ne dors pas

#### email-55 — (sans objet) — 2011-09-06 

- **eq-20** — COMPOSITION — 146 car. [0:146] — usage : 0 fichier(s) .md, trames [3, 31]
    - ⊃ eq-188 136/146 car.
    - > good morning, i have to stay home today with my daugter because she is sick, i will be reacheble all day at my house number 450-550-2998 thank you
- **eq-188** — bloc simple, repris dans une composition — 136 car. [0:136] — usage : 0 fichier(s) .md, trames [67]
    - ⊂ eq-20 136/146 car.
    - > good morning, i have to stay home today with my daugter because she is sick, i will be reacheble all day at my house number 450-550-2998

#### email-61 — Reunion demain — 2011-05-25 

- **eq-152** — DOUBLON — 104 car. [0:104] — usage : 1 fichier(s) .md, trames [5]
    - = eq-186 
    - > salut demain je dois aller chez le pediatre pour les vaccins de ma fille. on doir la remettre a vendredi
- **eq-186** — DOUBLON — 104 car. [0:104] — usage : 1 fichier(s) .md, trames [67]
    - = eq-152 
    - > salut demain je dois aller chez le pediatre pour les vaccins de ma fille. on doir la remettre a vendredi

#### email-86 — demain — 2010-10-14 

- **eq-35** — COMPOSITION — 133 car. [0:133] — usage : 0 fichier(s) .md, trames [24]
    - ⊃ eq-138 118/133 car.
    - > salut, peux tu arriver vers 7hre - 7h15 demain, j'ai une entrevue chez hydro qubec a 8h30 et je dois prendre le train de 7h30 merci !
- **eq-138** — bloc simple, repris dans une composition — 118 car. [7:125] — usage : 1 fichier(s) .md, trames —
    - ⊂ eq-35 118/133 car.
    - > peux tu arriver vers 7hre - 7h15 demain, j'ai une entrevue chez hydro qubec a 8h30 et je dois prendre le train de 7h30

#### email-90 — cours de natation — 2010-05-15 

- **eq-38** — DOUBLON — 45 car. [0:45] — usage : 1 fichier(s) .md, trames [11, 66]
    - = eq-136 
    - > c'est à quelle heure et quel jour ses cours -
- **eq-136** — DOUBLON — 45 car. [0:45] — usage : 1 fichier(s) .md, trames —
    - = eq-38 
    - > c'est à quelle heure et quel jour ses cours -

#### email-91 — Re: cours de natation — 2010-05-15 

- **eq-1** — DOUBLON — 21 car. [0:21] — usage : texte trop court, trames [11, 66]
    - = eq-137 
    - > c est dimanche a 9hre
- **eq-137** — DOUBLON — 21 car. [0:21] — usage : texte trop court, trames —
    - = eq-1 
    - > c est dimanche a 9hre

#### email-106 — Re: Samedi — 2011-02-02 

- **eq-80** — CHEVAUCHEMENT PARTIEL — 73 car. [0:73] — usage : 1 fichier(s) .md, trames [30]
    - ≈ eq-206 67 car. (92%)
    - > salut les demenageurs n etait pas libre samedi amors je demenage dimanche
- **eq-206** — CHEVAUCHEMENT PARTIEL — 122 car. [6:128] — usage : 1 fichier(s) .md, trames [30]
    - ≈ eq-80 67 car. (92%)
    - > les demenageurs n etait pas libre samedi amors je demenage dimanche j imagine que samedi soir je vais finaliser les boites

#### email-116 — Re: ce soir — 2011-03-15 

- **eq-42** — COMPOSITION — 158 car. [0:158] — usage : 0 fichier(s) .md, trames [5, 31, 64]
    - ⊃ eq-61 99/158 car.
    - > salut ce soir elise ne va pas a son premier cour de danse je sais pas a quelle heure elle va partit je t'appel si c est pas trops tard sinon on se voi
- **eq-61** — bloc simple, repris dans une composition — 99 car. [0:99] — usage : 0 fichier(s) .md, trames [31]
    - ⊂ eq-42 99/158 car.
    - > salut ce soir elise ne va pas a son premier cour de danse je sais pas a quelle heure elle va partit

#### email-267 — Re: Visite — 2016-09-16 

- **eq-118** — COMPOSITION — 212 car. [0:212] — usage : 6 fichier(s) .md, trames [9]
    - ⊃ eq-91 89/212 car.
    - > je sais que c'est ce que tu m'as demandé et moi je t'ai demandé autre chose. aujourd'hui tu n'as pas de garde partagée et je n'ai pas ce que je t'ai d
- **eq-91** — bloc simple, repris dans une composition — 89 car. [122:211] — usage : 12 fichier(s) .md, trames [35, 55]
    - ⊂ eq-118 89/212 car.
    - > je n'ai pas ce que je t'ai demandé non plus, une garde avec visites multiples par semaine

#### email-275 — Re: Visite — 2016-09-16 

- **eq-215** — COMPOSITION — 100 car. [37:137] — usage : 3 fichier(s) .md, trames —
    - ⊃ eq-55 73/100 car.
    - > je penses que tu as tords, je penses que je m'en occupais 50% du temps a toutes fins pratique... 46%
- **eq-55** — bloc simple, repris dans une composition — 73 car. [64:137] — usage : 5 fichier(s) .md, trames [50]
    - ⊂ eq-215 73/100 car.
    - > je penses que je m'en occupais 50% du temps a toutes fins pratique... 46%

#### email-296 — Re: Visite — 2016-09-16 

- **eq-52** — DOUBLON — 253 car. [42:295] — usage : 1 fichier(s) .md, trames —
    - = eq-109 
    - > n'assumes pas ce que j'aurais été en mesure d'accepter. si je ne m'étais pas occupé de mes enfants je ne me serais jamais mise dans une position d'exi
- **eq-109** — DOUBLON — 253 car. [42:295] — usage : 0 fichier(s) .md, trames [55]
    - = eq-52 
    - > [...] n'assumes pas ce que j'aurais été en mesure d'accepter. si je ne m'étais pas occupé de mes enfants je ne me serais jamais mise dans une position

#### email-299 — Re: Visite — 2016-09-16 

- **eq-101** — DOUBLON — 137 car. [0:137] — usage : 1 fichier(s) .md, trames [55]
    - = eq-105 
    - > louis philippe, stp, les journées ne se reprennent pas. le temps passe vite et les enfants t'aiment beaucoup et je sais que tu les aimes.
- **eq-105** — DOUBLON — 137 car. [0:137] — usage : 1 fichier(s) .md, trames —
    - = eq-101 
    - > louis philippe, stp, les journées ne se reprennent pas. le temps passe vite et les enfants t'aiment beaucoup et je sais que tu les aimes.

#### email-305 — Re: Visite — 2016-09-16 

- **eq-100** — COMPOSITION — 291 car. [0:291] — usage : 2 fichier(s) .md, trames [55, 56]
    - ⊃ eq-104 227/291 car.
    - ⊃ eq-121 121/291 car.
    - > lp les enfants veulent te voir et je ne peux m'être trompée car je n'ai pas décidé de la situation actuelle, je n'étais simplement pas d,accord avec e
- **eq-121** — bloc simple, repris dans une composition — 121 car. [34:155] — usage : 2 fichier(s) .md, trames —
    - ≈ eq-104 91 car. (75%)
    - ⊂ eq-100 121/291 car.
    - > je ne peux m'être trompée car je n'ai pas décidé de la situation actuelle, je n'étais simplement pas d,accord avec et toi
- **eq-104** — bloc simple, repris dans une composition — 227 car. [64:291] — usage : 2 fichier(s) .md, trames [55]
    - ≈ eq-121 91 car. (75%)
    - ⊂ eq-100 227/291 car.
    - > je n'ai pas décidé de la situation actuelle, je n'étais simplement pas d,accord avec et toi et je paie le prix aujourd'hui de ça, car c'est comme ça q

#### email-306 — Re: Visite — 2016-09-16 

- **eq-111** — COMPOSITION — 256 car. [37:293] — usage : 1 fichier(s) .md, trames —
    - ⊃ eq-216 86/256 car.
    - > je n'ai pas dit que tu passais ton temps à te saouler mais je ne pense pas que j'aille tort de dire que non tu ne t'en occupais pas 50% du temps. je n
- **eq-216** — bloc simple, repris dans une composition — 86 car. [96:182] — usage : 8 fichier(s) .md, trames —
    - ⊂ eq-111 86/256 car.
    - > je ne pense pas que j'aille tort de dire que non tu ne t'en occupais pas 50% du temps.

#### email-349 — Re: — 2013-06-30 

- **eq-15** — COMPOSITION — 308 car. [0:308] — usage : 0 fichier(s) .md, trames [2, 8]
    - ⊃ eq-50 73/308 car.
    - ⊃ eq-63 73/308 car.
    - > elise les 2 chemins ne mene pas au meme resultat avec alexia, pas du tout. tout ce que je veux c est de pouvoir aller passer des fds au chalet avec. j
- **eq-50** — bloc simple, repris dans une composition — 73 car. [75:148] — usage : 1 fichier(s) .md, trames [26]
    - = eq-63 
    - ⊂ eq-15 73/308 car.
    - > tout ce que je veux c est de pouvoir aller passer des fds au chalet avec.
- **eq-63** — bloc simple, repris dans une composition — 73 car. [75:148] — usage : 1 fichier(s) .md, trames [8, 19, 34, 48, 52]
    - = eq-50 
    - ⊂ eq-15 73/308 car.
    - > tout ce que je veux c est de pouvoir aller passer des fds au chalet avec.

### PDF

#### pdf-1 — Courriel suggérant de faire une plainte pour violence conjugale

- **pq-1** (p. 1) — bloc simple, repris dans une composition — 71 car. — usage : 3 fichier(s) .md, trames —
    - ⊂ pq-25 71/793 car.
    - ⊂ pq-26 71/890 car.
    - ⊂ pq-57 71/77 car.
    - > je t'écris comme si tu étais une cliente à laquelle je donnais conseil.
- **pq-2** (p. 1) — bloc simple, repris dans une composition — 49 car. — usage : 8 fichier(s) .md, trames —
    - ⊂ pq-17 49/310 car.
    - ⊂ pq-22 49/144 car.
    - ⊂ pq-25 49/793 car.
    - ⊂ pq-26 49/890 car.
    - ⊂ pq-55 49/284 car.
    - ⊂ pq-59 49/144 car.
    - > si j'étais ton avocate le plan serait le suivant:
- **pq-3** (p. 1) — bloc simple, repris dans une composition — 80 car. — usage : 29 fichier(s) .md, trames —
    - = pq-24 
    - = pq-51 
    - ⊂ pq-25 80/793 car.
    - ⊂ pq-56 80/183 car.
    - ⊂ pq-63 80/92 car.
    - > tu veux avoir la garde et lui puisse voir les enfants plusieurs fois par semaine
- **pq-4** (p. 1) — bloc simple, repris dans une composition — 94 car. — usage : 14 fichier(s) .md, trames —
    - ⊂ pq-17 94/310 car.
    - ⊂ pq-22 94/144 car.
    - ⊂ pq-25 94/793 car.
    - ⊂ pq-26 94/890 car.
    - ⊂ pq-55 94/284 car.
    - ⊂ pq-59 94/144 car.
    - > faire une requête pour garde exclusive d'urgence, et usage exclusif de la résidence familiale.
- **pq-5** (p. 1) — COMPOSITION — 397 car. — usage : 0 fichier(s) .md, trames —
    - ⊃ pq-54 215/397 car.
    - > faire une requête pour garde exclusive d'urgence, et usage exclusif de la résidence familiale ... on accorde des droits d'accès sans coucher au père e
- **pq-6** (p. 1) — bloc simple, repris dans une composition — 58 car. — usage : 17 fichier(s) .md, trames [7, 48, 49, 70, 72, 76]
    - ⊂ pq-25 58/793 car.
    - ⊂ pq-26 58/890 car.
    - ⊂ pq-34 58/224 car.
    - ⊂ pq-58 58/180 car.
    - > alexia vie dans la violence conjugale depuis sa naissance.
- **pq-7** (p. 1) — bloc simple, repris dans une composition — 110 car. — usage : 12 fichier(s) .md, trames [7, 48, 49, 70, 72]
    - ⊂ pq-25 110/793 car.
    - ⊂ pq-26 110/890 car.
    - ⊂ pq-34 110/224 car.
    - ⊂ pq-58 110/180 car.
    - > tout intervenant de la dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.
- **pq-8** (p. 1) — bloc simple, repris dans une composition — 177 car. — usage : 6 fichier(s) .md, trames [70]
    - = pq-53 
    - ⊂ pq-26 177/890 car.
    - ⊂ pq-64 177/189 car.
    - > le meilleur moment pour lui envoyer la procédure est jeudi pour qu'on aille à la cour vendredi avant son départ. une pierre deux coups. la procédure e
- **pq-9** (p. 1) — COMPOSITION — 430 car. — usage : 2 fichier(s) .md, trames [70, 71, 72, 76]
    - ⊃ pq-18 106/430 car.
    - > on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser et on l'oblige également à payer 50% des charges afférentes à la maiso
- **pq-17** (p. 1) — COMPOSITION — 310 car. — usage : 0 fichier(s) .md, trames [21]
    - ⊃ pq-2 49/310 car.
    - ⊃ pq-4 94/310 car.
    - ⊃ pq-22 144/310 car.
    - ⊃ pq-59 144/310 car.
    - > je t'écris comme si tu étais une cliente à laquelle je donnais conseil (...) si j'étais ton avocate le plan serait le suivant: faire une requête pour 
- **pq-18** (p. 1) — bloc simple, repris dans une composition — 106 car. — usage : 2 fichier(s) .md, trames [32]
    - ⊂ pq-9 106/430 car.
    - > lp s'il réside temporairement chez ses parents peut s'acquitter facilement de ses obligations financières.
- **pq-22** (p. 1) — COMPOSITION (et incluse ailleurs) — 144 car. — usage : 4 fichier(s) .md, trames —
    - ⊃ pq-2 49/144 car.
    - ⊃ pq-4 94/144 car.
    - = pq-59 
    - ⊂ pq-17 144/310 car.
    - ⊂ pq-25 144/793 car.
    - ⊂ pq-26 144/890 car.
    - ⊂ pq-55 144/284 car.
    - > si j'étais ton avocate le plan serait le suivant: faire une requête pour garde exclusive d'urgence, et usage exclusif de la résidence familiale.
- **pq-24** (p. 1) — bloc simple, repris dans une composition — 80 car. — usage : 29 fichier(s) .md, trames [35]
    - = pq-3 
    - = pq-51 
    - ⊂ pq-25 80/793 car.
    - ⊂ pq-56 80/183 car.
    - ⊂ pq-63 80/92 car.
    - > tu veux avoir la garde et lui puisse voir les enfants plusieurs fois par semaine
- **pq-25** (p. 1) — COMPOSITION — 793 car. — usage : 0 fichier(s) .md, trames [6, 34, 36, 52]
    - ⊃ pq-1 71/793 car.
    - ⊃ pq-2 49/793 car.
    - ⊃ pq-3 80/793 car.
    - ⊃ pq-4 94/793 car.
    - ⊃ pq-6 58/793 car.
    - ⊃ pq-7 110/793 car.
    - ⊃ pq-22 144/793 car.
    - ⊃ pq-24 80/793 car.
    - ⊃ pq-51 80/793 car.
    - ⊃ pq-57 77/793 car.
    - ⊃ pq-59 144/793 car.
    - ⊃ pq-61 91/793 car.
    - > je t'écris comme si tu étais une cliente à laquelle je donnais conseil. [...] alexia vie dans la violence conjugale depuis sa naissance. tout interven
- **pq-26** (p. 1) — COMPOSITION — 890 car. — usage : 0 fichier(s) .md, trames [39]
    - ⊃ pq-1 71/890 car.
    - ⊃ pq-2 49/890 car.
    - ⊃ pq-4 94/890 car.
    - ⊃ pq-6 58/890 car.
    - ⊃ pq-7 110/890 car.
    - ⊃ pq-8 177/890 car.
    - ⊃ pq-22 144/890 car.
    - ⊃ pq-53 177/890 car.
    - ⊃ pq-54 215/890 car.
    - ⊃ pq-57 77/890 car.
    - ⊃ pq-59 144/890 car.
    - ⊃ pq-61 91/890 car.
    - ⊃ pq-62 227/890 car.
    - ⊃ pq-64 189/890 car.
    - > je t'écris comme si tu étais une cliente à laquelle je donnais conseil. [...] alexia vie dans la violence conjugale depuis sa naissance. tout interven
- **pq-34** (p. 1) — COMPOSITION — 224 car. — usage : 0 fichier(s) .md, trames [48]
    - ⊃ pq-6 58/224 car.
    - ⊃ pq-7 110/224 car.
    - ⊃ pq-69 48/224 car.
    - > [...] alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la dpj pourra arriver à la conclusion que sa sécurité et son déve
- **pq-51** (p. 1) — bloc simple, repris dans une composition — 80 car. — usage : 29 fichier(s) .md, trames [50, 55, 70]
    - = pq-3 
    - = pq-24 
    - ⊂ pq-25 80/793 car.
    - ⊂ pq-56 80/183 car.
    - ⊂ pq-63 80/92 car.
    - > tu veux avoir la garde et lui puisse voir les enfants plusieurs fois par semaine
- **pq-52** (p. 1) — bloc simple, repris dans une composition — 138 car. — usage : 6 fichier(s) .md, trames [50, 55]
    - ⊂ pq-88 138/160 car.
    - > toutes procédures peut être amendée, rectifié et qu'une entente peut intervenir entre les parents à tout moment, même la veille du procès.
- **pq-53** (p. 1) — bloc simple, repris dans une composition — 177 car. — usage : 6 fichier(s) .md, trames [55]
    - = pq-8 
    - ⊂ pq-26 177/890 car.
    - ⊂ pq-64 177/189 car.
    - > le meilleur moment pour lui envoyer la procédure est jeudi pour qu'on aille à la cour vendredi avant son départ. une pierre deux coups. la procédure e
- **pq-54** (p. 1) — bloc simple, repris dans une composition — 215 car. — usage : 14 fichier(s) .md, trames [50, 55, 70, 71, 76]
    - ⊂ pq-5 215/397 car.
    - ⊂ pq-26 215/890 car.
    - ⊂ pq-62 215/227 car.
    - > pendant toute cette procédure les enfants sont avec toi. donc, cela créé un précédant, c'est à dire une routine s'instaure entre toi et les enfants et
- **pq-55** (p. 1) — COMPOSITION — 284 car. — usage : 0 fichier(s) .md, trames [55]
    - ⊃ pq-2 49/284 car.
    - ⊃ pq-4 94/284 car.
    - ⊃ pq-22 144/284 car.
    - ⊃ pq-59 144/284 car.
    - > [...] si j'étais ton avocate le plan serait le suivant: faire une requête pour garde exclusive d'urgence, et usage exclusif de la résidence familiale.
- **pq-56** (p. 1) — COMPOSITION — 183 car. — usage : 3 fichier(s) .md, trames [9]
    - ⊃ pq-3 80/183 car.
    - ⊃ pq-24 80/183 car.
    - ⊃ pq-51 80/183 car.
    - > tu veux avoir la garde et lui puisse voir les enfants plusieurs fois par semaine, ce n'est ce qu'il veut. il veut avoir une coupure avec toi et avoir 
- **pq-57** (p. 1) — COMPOSITION (et incluse ailleurs) — 77 car. — usage : 0 fichier(s) .md, trames [56, 62]
    - ⊃ pq-1 71/77 car.
    - ⊂ pq-25 77/793 car.
    - ⊂ pq-26 77/890 car.
    - > je t'écris comme si tu étais une cliente à laquelle je donnais conseil. [...]
- **pq-58** (p. 1) — COMPOSITION — 180 car. — usage : 0 fichier(s) .md, trames [56, 62]
    - ⊃ pq-6 58/180 car.
    - ⊃ pq-7 110/180 car.
    - > [...] alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la dpj pourra arriver à la conclusion que sa sécurité et son déve
- **pq-59** (p. 1) — COMPOSITION (et incluse ailleurs) — 144 car. — usage : 4 fichier(s) .md, trames [56, 62]
    - ⊃ pq-2 49/144 car.
    - ⊃ pq-4 94/144 car.
    - = pq-22 
    - ⊂ pq-17 144/310 car.
    - ⊂ pq-25 144/793 car.
    - ⊂ pq-26 144/890 car.
    - ⊂ pq-55 144/284 car.
    - > si j'étais ton avocate le plan serait le suivant: faire une requête pour garde exclusive d'urgence, et usage exclusif de la résidence familiale.
- **pq-60** (p. 1) — bloc simple, repris dans une composition — 118 car. — usage : 8 fichier(s) .md, trames [56, 62]
    - ⊂ pq-68 118/198 car.
    - > lors de cette procédure d'urgence le juge en question n'entend pas de témoin c'est seulement les avocats qui plaident.
- **pq-61** (p. 1) — bloc simple, repris dans une composition — 91 car. — usage : 0 fichier(s) .md, trames [56, 62]
    - ⊂ pq-25 91/793 car.
    - ⊂ pq-26 91/890 car.
    - > [...] on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser [...]
- **pq-62** (p. 1) — COMPOSITION (et incluse ailleurs) — 227 car. — usage : 0 fichier(s) .md, trames [56, 62, 70]
    - ⊃ pq-54 215/227 car.
    - ⊂ pq-26 227/890 car.
    - > [...] pendant toute cette procédure les enfants sont avec toi. donc, cela créé un précédant, c'est à dire une routine s'instaure entre toi et les enfa
- **pq-63** (p. 1) — COMPOSITION — 92 car. — usage : 0 fichier(s) .md, trames [56, 62]
    - ⊃ pq-3 80/92 car.
    - ⊃ pq-24 80/92 car.
    - ⊃ pq-51 80/92 car.
    - > [...] tu veux avoir la garde et lui puisse voir les enfants plusieurs fois par semaine [...]
- **pq-64** (p. 1) — COMPOSITION (et incluse ailleurs) — 189 car. — usage : 0 fichier(s) .md, trames [56, 62]
    - ⊃ pq-8 177/189 car.
    - ⊃ pq-53 177/189 car.
    - ⊂ pq-26 189/890 car.
    - > [...] le meilleur moment pour lui envoyer la procédure est jeudi pour qu'on aille à la cour vendredi avant son départ. une pierre deux coups. la procé
- **pq-68** (p. 1) — COMPOSITION — 198 car. — usage : 3 fichier(s) .md, trames [62]
    - ⊃ pq-60 118/198 car.
    - > en urgence on appelle cela une ordonnance de sauvegarde. lors de cette procédure d'urgence le juge en question n'entend pas de témoin c'est seulement 
- **pq-69** (p. 1) — bloc simple, repris dans une composition — 48 car. — usage : 0 fichier(s) .md, trames [62, 70, 71, 72]
    - ⊂ pq-34 48/224 car.
    - > [...] tu dois le faire sortir de la maison [...]
- **pq-88** (p. 1) — COMPOSITION — 160 car. — usage : 5 fichier(s) .md, trames [62]
    - ⊃ pq-52 138/160 car.
    - > dis toi également que toutes procédures peut être amendée, rectifié et qu'une entente peut intervenir entre les parents à tout moment, même la veille 

#### pdf-3 — Réponse à l'offre de garde partagée

- **pq-10** (p. 2) — bloc simple, repris dans une composition — 202 car. — usage : 0 fichier(s) .md, trames [9, 38, 55, 56, 71, 72, 73, 76]
    - ⊂ pq-27 202/222 car.
    - > il y a contre-indication à l'établissement de la garde parlagée des deux (2) enfants mineurs vu leur jeune âge et qu'il n'est pas dans leur intérêt de
- **pq-27** (p. 2) — COMPOSITION — 222 car. — usage : 0 fichier(s) .md, trames [34, 39, 42, 49, 71, 72, 73, 76]
    - ⊃ pq-10 202/222 car.
    - > nous considérons qu'il y a contre-indication à l'établissement de la garde parlagée des deux (2) enfants mineurs vu leur jeune âge et qu'il n'est pas 

#### pdf-5 — 20150813 MJ projet consentement

- **pq-33** (p. 3) — COMPOSITION — 1069 car. — usage : 0 fichier(s) .md, trames [34, 47, 49, 50, 52, 55]
    - ⊃ pq-93 225/1069 car.
    - > les parties conviennent également à l'accroissement progressif des droits d'accès du demandeur auprès de ses enfants de la façon suivante: a) b) c) d)
- **pq-93** (p. 3) — bloc simple, repris dans une composition — 225 car. — usage : 0 fichier(s) .md, trames [50]
    - ⊂ pq-33 225/1069 car.
    - > à partir du 26 août 2018 : semaine 1 de vendredi après la garderie et/ou garderie, jusqu'au mardi 8h00 directement à l'école et/ou la garderie; semain

#### pdf-6 — 20150902 FP réponse projet consentement

- **pq-14** (p. 2) — bloc simple, repris dans une composition — 277 car. — usage : 0 fichier(s) .md, trames —
    - = pq-67 
    - ⊂ pq-28 277/539 car.
    - > en ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client 
- **pq-28** (p. 2) — COMPOSITION — 539 car. — usage : 0 fichier(s) .md, trames [34, 40]
    - ⊃ pq-14 277/539 car.
    - ⊃ pq-66 154/539 car.
    - ⊃ pq-67 277/539 car.
    - > notre client est tout à fait disposé à établir une progression dans les droits d'accès auprès des enfants. cependant, il souhaite ajouter un sous-para
- **pq-66** (p. 2) — bloc simple, repris dans une composition — 154 car. — usage : 0 fichier(s) .md, trames [56]
    - ⊂ pq-28 154/539 car.
    - > cependant, il souhaite ajouter un sous-paragraphe " e) " afin de prévoir qu'à compter du 7 février 2016 l'horaire de garde sera en alternance 2-2-3/2-
- **pq-67** (p. 2) — bloc simple, repris dans une composition — 277 car. — usage : 0 fichier(s) .md, trames [56]
    - = pq-14 
    - ⊂ pq-28 277/539 car.
    - > en ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client 

#### pdf-8 — Commission spéciale sur les droits des enfants et la protection de la 

- **pq-70** (p. 2) — DOUBLON — 114 car. — usage : 0 fichier(s) .md, trames [62]
    - = pq-72 
    - > le barreau du québec remercie les membres de son comité consultatif en droit de la jeunesse : me marie-josée ayoub
- **pq-72** (p. 2) — DOUBLON — 114 car. — usage : 0 fichier(s) .md, trames [48, 55]
    - = pq-70 
    - > le barreau du québec remercie les membres de son comité consultatif en droit de la jeunesse : me marie-josée ayoub

#### pdf-11 — Étude de la valeur marchande à des fins de partage

- **pq-16** (p. 1) — bloc simple, repris dans une composition — 72 car. — usage : 0 fichier(s) .md, trames [20]
    - ⊂ pq-23 72/212 car.
    - > étude de la valeur marchande en date des présentes à des fins de partage
- **pq-23** (p. 1) — COMPOSITION — 212 car. — usage : 0 fichier(s) .md, trames [33]
    - ⊃ pq-16 72/212 car.
    - > requérant(e): monsieur louis-philippe david lieux: 245, avenue macaulay saint-lambert, qc fins du rapport: étude de la valeur marchande en date des pr

#### pdf-13 — Jugement sur le fond (perte emplois)

- **pq-74** (p. 2) — COMPOSITION — 306 car. — usage : 0 fichier(s) .md, trames [62]
    - ⊃ pq-82 88/306 car.
    - > 10h13:11 témoignage de m. david - questions du tribunal. objection de me ayoub (un jugement a été prononcé en 2016 sur ces sujets) ; le tribunal prend
- **pq-75** (p. 2) — DOUBLON — 76 car. — usage : 0 fichier(s) .md, trames [62]
    - = pq-83 
    - > 10h38:50 p-2 en liasse : plusieurs recherches d'emploi offertes à monsieur ;
- **pq-82** (p. 2) — bloc simple, repris dans une composition — 88 car. — usage : 0 fichier(s) .md, trames [62]
    - ⊂ pq-74 88/306 car.
    - > 10h17:04 le tribunal informe monsieur de ne pas parler de ce qui s'est passé avant 2016.
- **pq-83** (p. 2) — DOUBLON — 76 car. — usage : 0 fichier(s) .md, trames [62]
    - = pq-75 
    - > 10h38:50 p-2 en liasse : plusieurs recherches d'emploi offertes à monsieur ;
- **pq-76** (p. 3) — COMPOSITION — 882 car. — usage : 0 fichier(s) .md, trames —
    - ⊃ pq-84 247/882 car.
    - > attendu que les parties, après le début de l'audition, se sont entendues à ce qu'un jugement soit rendu avec les conclusions suivantes : ordonne à mon
- **pq-84** (p. 3) — bloc simple, repris dans une composition — 247 car. — usage : 0 fichier(s) .md, trames [62]
    - ⊂ pq-76 247/882 car.
    - > attendu que les parties, après le début de l'audition, se sont entendues à ce qu'un jugement soit rendu avec les conclusions suivantes : ordonne à mon

#### pdf-57 — Facture Pistorio 2011-05-31

- **pq-41** (p. 1) — bloc simple, repris dans une composition — 175 car. — usage : 0 fichier(s) .md, trames —
    - ⊂ pq-42 175/255 car.
    - > | | séance du 03 mai 2011 | 80,00 | 80,00 | | | séance du 17 mai 2011 | 80,00 | 80,00 | | | séance du 24 mai 2011 | 80,00 | 80,00 | | | séance du 31 m
- **pq-42** (p. 1) — COMPOSITION — 255 car. — usage : 0 fichier(s) .md, trames [30]
    - ⊃ pq-41 175/255 car.
    - > | quantité | description | prix unit. | montant | | :--- | :--- | :--- | :--- | | | séance du 03 mai 2011 | 80,00 | 80,00 | | | séance du 17 mai 2011 

---

## 3. Citations non localisables dans leur source

Leur texte ne se retrouve pas (ou pas entièrement) dans le corps stocké : recomposition manuelle, bloc cité, message transféré, ou corps vide. Elles échappent à l'analyse d'intervalles et doivent être tranchées à l'œil.

- **eq-5** (email-34) — aucun segment retrouve dans le corps (texte recompose)
    - > > bonne fête lp!! et puis ton party vendredi? c'était cool? salut eve, oui on a eu bien du plaisir, y'avais bcoup d'enfants, de rire et de joie.
- **eq-9** (email-359) — aucun segment retrouve dans le corps (texte recompose)
    - > hi doug, we are preparing for our vacation in cape cod from august 10-17 at the house on 22 glenwood drive west yarmouth, properties no 320. i just wa
- **eq-21** (email-53) — aucun segment retrouve dans le corps (texte recompose)
    - > good morning my daugther is sick and i ll be staying at home today with her, thanks, lp
- **eq-22** (email-51) — aucun segment retrouve dans le corps (texte recompose)
    - > hi i have to stay home again today my mother in law can t come in. you ll bebable tomreach me at home, thanks
- **eq-32** (email-89) — aucun segment retrouve dans le corps (texte recompose)
    - > tu m'as demandé si je pouvais changer mes vendredis pour les lundis pour octobre - le 4 pas de problème - le 11 c'est congé - le 18 c'est ok et leb 25
- **eq-54** (email-7) — aucun segment retrouve dans le corps (texte recompose)
    - > j'étais tout le temps à la maison. tu vas honnêtement venir me dire que pendant tout ce temps passer a la maison j'etais assis dans le divan a écouter
- **eq-68** (email-49) — 1 segment(s) sur 2 introuvable(s)
    - > je t'envoie trois possibilités de maisons à cape cod - je m'attends à ce qu'élise ne soit pas d'accord. [...] si ça marche pas cette année, ce sera pl
- **eq-86** (email-394) — aucun segment retrouve dans le corps (texte recompose)
    - > c'est certain que je suis libre, alexia est présentement malade, mais très certainement elle serra rétablie dimanche
- **eq-90** (email-402) — aucun segment retrouve dans le corps (texte recompose)
    - > puisqu'il n'est pas dans l'intérêt des enfants de modifier une routine établie depuis plus deux mois, nous garderons les droits d'acces tels qu'ils so
- **eq-92** (email-26) — aucun segment retrouve dans le corps (texte recompose)
    - > je sais qu'il ne veut pas entrer dans une dynamique de confrontation mais il pourrait bénéficier d'informations.
- **eq-93** (email-343) — aucun segment retrouve dans le corps (texte recompose)
    - > moi j y vais pas j ai pas ete invité et en fait je savais pas qu elle le faisias baptiser.... bonjour, demain le 19 juillet à 14:00 je ferais baptiser
- **eq-127** (email-456) — aucun segment retrouve dans le corps (texte recompose)
    - > ... suite au constat que vous ne répondez malheureusement pas aux attentes de votre poste.
- **eq-146** (email-266) — citation trop courte pour etre localisee
    - > les 2
- **eq-167** (email-364) — citation trop courte pour etre localisee
    - > oui
- **eq-169** (email-141) — aucun segment retrouve dans le corps (texte recompose)
    - > hum, je penses que nous allons etre loins, mais pourquoi pas
- **eq-170** (email-355) — aucun segment retrouve dans le corps (texte recompose)
    - > direction loisirs, culture et vie communautaire 600, avenue oak, saint-lambert
- **eq-173** (email-350) — corps du courriel vide en base
    - > c'est le prix pour nous 4 c'est tentant non c'est nouveau et un 5 étoiles
- **eq-178** (email-69) — aucun segment retrouve dans le corps (texte recompose)
    - > bon matin catherine je dois rester avec ma petite aujourd'hui. j'imagine qu'il y a des journees prevues pour ca a la banque. sinon je vais prendre une
- **eq-180** (email-64) — aucun segment retrouve dans le corps (texte recompose)
    - > good morning i won't be coming in today i have to stay with my daughter. she is sick and must go to the doctor.
- **eq-182** (email-59) — aucun segment retrouve dans le corps (texte recompose)
    - > j'ai essayer de convaincre ma copine que tu avais plus besoins de moi que ma fille mais en vains je resterai donc a la maison avec elle, si jamais il 
- **eq-183** (email-53) — aucun segment retrouve dans le corps (texte recompose)
    - > good morning my daughter is sick and i'll be staying at home today with her
- **eq-184** (email-51) — aucun segment retrouve dans le corps (texte recompose)
    - > hi i have to stay home again today my mother in law can't come in.
- **eq-185** (email-47) — aucun segment retrouve dans le corps (texte recompose)
    - > je restes a la maison avec ma fille aujourd'hui. si danilo a des questions, je suis disponible 450 550 2998
- **eq-187** (email-56) — aucun segment retrouve dans le corps (texte recompose)
    - > salut catherine je dois rester avec ma fille cet avant midi je rentrerai au travail cet apres midi
- **eq-189** (email-45) — aucun segment retrouve dans le corps (texte recompose)
    - > salut, ma fille a la gastro je dois rester a la maison je serrai disponible au 450 550 2998
- **eq-191** (email-41) — aucun segment retrouve dans le corps (texte recompose)
    - > bon matin karl, je vais etre au fravail lundi. la sittuation se stabilise, mais nous ne dormons que quelques heures par nuit depuis une semaine et je 
- **eq-192** (email-40) — aucun segment retrouve dans le corps (texte recompose)
    - > salut karl, je vais rester a la maison aujourd hui pour aider ma conjointe avec le bebe, elle ne se sent pas tres bien et ma belle mere n est pas disp
- **eq-193** (email-30) — aucun segment retrouve dans le corps (texte recompose)
    - > salut karl, je vais à la clinique ce matin avec mon gars et en fonction de ce qu ils me disent, je vais rester ici ou rentrer travailler!
- **eq-196** (email-28) — aucun segment retrouve dans le corps (texte recompose)
    - > salut voici le papier du medicine, je vais manquer le cmoc et le dîner d'équipe, mais je suis malade et en plus je dois m occuper de mon gars
- **eq-199** (email-266) — citation trop courte pour etre localisee
    - > les 2
- **eq-208** (email-404) — aucun segment retrouve dans le corps (texte recompose)
    - > dernière chose, est il possible dans l entente que je demande de ne plus avoir a donner mon consentement pour que les enfants partent a l étranger. je
