# Mémoire de continuité — projet `court`

Dernière mise à jour : 2 août 2026

## Objet du projet

Application Django servant à organiser, analyser et produire le dossier d’un litige familial. Elle regroupe notamment les courriels, documents/PDF, photos, vidéos, événements, conversations Google Chat, protagonistes et arguments. Le répertoire `legal/` contient le travail de préparation procédurale et de preuve.

## Situation procédurale actuelle

- La demande/requête introductive et le bordereau de preuve ont été **déposés le 24 juillet 2026 à 15 h 19** au Palais de justice de **Longueuil**, sous le **n° de dossier 505-17-016235-261**. Droit de greffe de 616,00 $, reçu 0585314-0035. Le dépôt est archivé sous `legal/depots/2026-07-24_initial/` (incluant `preuve_de_depot.pdf`), ancré au commit `1f0af56`.
- **Une copie imprimée** de la demande et du bordereau a été remise au comptoir : **aucun fichier n’a été transmis**. L’acte déposé est un document papier détenu par le greffe; les fichiers conservés sont la source d’impression, non l’acte lui-même. Lequel des cinq candidats du 24 juillet a été imprimé reste à établir.
- L’acte se signe « Daté du 21 juillet 2026 », porte `2026-07-21` dans son nom de fichier et laisse « N° : ______________ » en blanc. Aucun des trois ne reflète la réalité : le dépôt est du **24 juillet** et le dossier est le **505-17-016235-261**. La version amendée doit porter le numéro, de même que le bordereau, les pièces assemblées et le cahier.
- La requête **n’a pas encore été notifiée/signifiée** aux autres parties.
- Selon l’information reçue par le demandeur, la requête peut encore être modifiée malgré son dépôt. Le travail en cours peut donc préparer une version amendée avant notification.
- Le dépôt initial demeure un jalon à préserver : ne pas écraser ni présenter une version subséquente comme si elle avait été celle déposée le 24 juillet.

### Prescription — deux ancres concurrentes, aucune marge

Le dépôt du 24 juillet 2026 se situe **entre** les deux dates d’expiration possibles du délai de 3 ans (art. 2925 C.c.Q.) sur la dénonciation de 2023 (P-40) :

| Ancre | Expiration | Dépôt du 24 juillet |
|---|---|---|
| Assermentation du 21 juillet 2023 | 21 juillet 2026 | **3 jours en retard** |
| Connaissance acquise le 25 juillet 2023 (P-105) | 25 juillet 2026 | 1 jour avant |

Le chef fondé sur P-40 repose donc **entièrement** sur l’ancre de la connaissance, plaidée au §234 de la demande déposée. Le corpus antérieur (`legal/these_prescription.md`, `legal/plan_de_travail.md`, les fichiers `ponts_*_consolides.md`) retenait la date conservatrice du 21 juillet 2026 et rappelait qu’elle ne devait pas être traitée comme acquise sans avis juridique. **Cette réserve demeure entière et n’est pas levée par le dépôt.**

### Deux délais de notification — c’est le plus court qui gouverne

- **Art. 2892 C.c.Q.** — le dépôt n’interrompt la prescription que si la demande est signifiée **au plus tard dans les 60 jours suivant l’expiration du délai de prescription**. Sanction : l’interruption est perdue rétroactivement, donc le recours est prescrit. Sous l’ancre conservatrice (21 juillet 2026) : **19 septembre 2026**. Sous l’ancre plaidée (25 juillet 2026) : 23 septembre 2026.
- **Art. 107 C.p.c.** — notification dans les trois mois du dépôt, soit le 24 octobre 2026. Sanction distincte (péremption).

**Échéance de travail retenue : 19 septembre 2026**, la plus courte. Travailler vers octobre ferait perdre en septembre exactement ce que le dépôt du 24 juillet servait à sauver. Le texte des deux articles et leur application au dossier doivent être validés auprès d’un professionnel du droit ou du greffe.

### Amender n’est pas neutre au regard de la prescription

L’interruption produite par le dépôt couvre la cause d’action déposée. Un fait ou un chef **nouveau** ajouté à la version amendée après le 25 juillet 2026 n’en bénéficie pas nécessairement. Toute modification doit donc être qualifiée : reformulation d’une cause déjà plaidée (protégée) ou cause nouvelle (exposée). La modification d’un acte est par ailleurs encadrée par l’art. 206 C.p.c.

## Règles de travail pour la suite

1. Conserver une trace explicite de la **version déposée** et de la date de dépôt.
2. Produire les corrections sous forme de **version amendée / prête à notifier**, avec une liste claire des changements.
3. Distinguer les preuves déjà au bordereau de celles ajoutées ou réorganisées après le dépôt.
4. Ne pas modifier silencieusement les fichiers déposés; créer une copie versionnée lorsque le contenu procédural change.
5. Avant notification, vérifier le document final, ses annexes/bordereaux, le numéro de dossier et les exigences du greffe applicables.

## État du dépôt et de la preuve dans le dépôt Git

- Le répertoire `legal/` comprend les faits, axes, pièces, bordereaux, annexe et fichiers de génération du dépôt.
- `legal/expose/README.md` décrit la méthode de traçabilité des sources, des pièces et des cotes.
- À la date de cette note, l’arbre Git contient plusieurs modifications locales, principalement dans `legal/`, ainsi que des pièces nouvellement générées ou en préparation. Elles ne doivent pas être présumées déposées ou signifiées sans vérification explicite.

## Directive d’interprétation — plan de 2013 et exécution en 2015

La distinction suivante doit être conservée dans tout travail relatif à P-2,
P-8, P-9, P-16, P-18 ou P-19 :

- selon le demandeur, le **véhicule procédural immédiat** annoncé dans P-2 —
  requête d’urgence en juin 2013 et éviction judiciaire du père — n’a pas été
  exécuté sous cette forme;
- le **dessein fonctionnel** documenté dans P-2 ne vise pas seulement un
  résultat de garde. La préférence maternelle est fixée avant l'examen de
  l'intérêt des enfants; la sortie du père, la garde maternelle de fait et
  l'installation d'une routine doivent ensuite fournir au Tribunal une base
  décisionnelle construite permettant de présenter cette préférence comme
  commandée par la stabilité. La tromperie alléguée vise donc le processus
  décisionnel du Tribunal, non le père;
- le départ du père le 23 février 2015, que le demandeur qualifie de
  volontaire, a satisfait autrement le préalable de sa sortie. P-19 établit le
  départ, sa date et le logement à proximité, mais non sa qualification de
  volontaire. Il n’est pas allégué que ce départ a été causé ou orchestré par
  P-2 ou par les défenderesses;
- P-8 montre Élise transmettant à Me Ayoub les textos du père sous l'objet
  « Voici quand il me confirme qu'il me donne la garde »; P-9 invoque ensuite,
  contre la garde partagée, la « routine établie depuis plus deux mois » et met
  Élise en copie; P-16 propose de modifier cette routine tout en maintenant une
  progression sous le partage égal; P-18 refuse la destination partagée comme
  « prématurée », sans critère de franchissement centré sur les enfants;
- ces positions de négociation soutiennent l'inférence que les motifs opposés
  en 2015 étaient insincères et servaient à maintenir la destination
  maternelle. Elles sont invoquées comme preuve du concert et de sa continuité,
  non comme un crime autonome ni comme une tromperie du père, lequel connaissait
  la réalité vécue et maintenait une position contraire;
- le départ rend sans objet l’utilisation des allégations de violence pour
  obtenir l’éviction, mais non leur pertinence éventuelle pour la sécurité des
  enfants. Leur disparition du corpus P-9, P-16 à P-19, malgré les nuitées
  offertes sans pont explicatif, est analysée comme un indice
  d’instrumentalité, non comme une preuve autonome de fausseté;
- P-19, rédigée par Me Ferreira et affirmée sous serment par Élise, constitue la
  **réalisation judiciaire alléguée** du mécanisme : elle ajoute au motif
  situationnel récent de P-9 une marginalité paternelle historique (§§ 15-17),
  affirme une garde maternelle convenue et demande sa consécration. La fausseté
  consciente, le caractère volontaire, l'intention de tromper et la fonction
  judiciaire doivent être établis séparément pour chaque énoncé contesté.

La formule de référence est **« exécution fonctionnelle différée et adaptée du
plan »**. Ne pas revenir à « inexécution du plan ». Analyse détaillée :
`legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/01_inexecution_plan_cohabitation.md`.

## Directive d’interprétation — cohérence prédictive et motifs exprimés

La synthèse des dix analyses transmises le 27 juillet 2026 est consignée dans
`legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/10_synthese_coherence_predictive_P2_P9_P16_P18_P19.md`.

La formule qui gouverne cette ligne d’analyse est **« cohérence prédictive du
plan malgré l’incohérence du motif exprimé »** :

- P-2 juxtapose une qualification de violence et de compromission extrêmement
  grave, un régime initial avec accès sans coucher et une préférence maternelle
  simultanée pour des contacts paternels plus étendus qu’une fin de semaine sur
  deux, mais sans partage égal. La borne d’une fin de semaine sur deux implique
  normalement au moins une nuitée; ne pas présenter les nuitées comme seulement
  éventuelles. P-2 ne fixe toutefois ni horaire précis ni plafond arithmétique;
- P-2 annonce le mécanisme père sorti → garde maternelle de fait → routine →
  résistance au changement. Environ 22,5 mois plus tard, P-9 oppose précisément
  cette routine au partage égal tout en offrant des modifications avec trois
  nuitées sur quatorze. P-9 permet une distinction de degré, mais ne la formule
  pas;
- P-16 est un projet non signé. S’il avait été signé, sa première phase aurait
  fait passer immédiatement le régime décrit de zéro nuitée à trois nuitées sur
  quatorze, dont un bloc de deux nuits consécutives, sans palier préalable
  d’acclimatation. La progression subséquente est réelle — trois, quatre, cinq,
  puis six nuitées, jusqu’à quatre nuits consécutives — mais aucune étape
  automatique ne mène au 2-2-3;
- P-17 propose le 2-2-3 pour le 7 février 2016. P-18 le qualifie de
  « prématuré » sans fournir de critère centré sur l’acclimatation des enfants,
  de condition d’évaluation ou d’échéance à laquelle il deviendrait approprié;
- il est inexact d’écrire qu’aucun changement n’est documenté entre 2013 et
  2015 : la séparation, le vieillissement des enfants et des consultations
  psychologiques le sont. La proposition exacte est qu’**aucun document examiné
  n’articule une cessation ou une réévaluation du risque allégué permettant de
  relier les restrictions de 2013 aux nuitées proposées en 2015**;
- P-19 déplace la justification vers une disponibilité paternelle historiquement
  limitée tout en maintenant la demande de garde maternelle et le refus du
  partage. La différence de motif est directe; la substitution et l’insincérité
  sont des inférences. La fausseté du portrait historique exige une preuve
  indépendante.

La chaîne P-2 → P-8 → P-9 → P-16 → P-18 → P-19 soutient cumulativement :

1. le dessein de substitution directement exprimé dans P-2;
2. une forte inférence de concert tacite entre Élise et Me Ayoub, fondée sur la
   communication directe du plan, leurs échanges opérationnels et les positions
   prises par Me Ayoub au nom de sa cliente;
3. l'insincérité des motifs employés pendant les négociations de 2015;
4. la réalisation judiciaire alléguée du mécanisme dans P-19.

Cette chaîne n'établit pas un concert avec Me Ferreira et ne dispense pas de
démontrer séparément les éléments de chaque parjure allégué dans P-19. Les
tensions dépendantes ne doivent pas être additionnées mécaniquement : leur
force vient de leur convergence structurée et de la capacité prédictive de P-2.

### Verrou anti-régression — objections déjà répondues

La mémoire gouvernante est :
`legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/11_memoire_argumentative_verrouillee_continuite_P2_P19.md`.

Sans élément nouveau précisément identifié, ne plus présenter comme
réfutations de la continuité fonctionnelle :

- la non-utilisation de la procédure urgente de 2013 : le départ a rendu le
  véhicule d’éviction caduc tout en satisfaisant son préalable matériel;
- la cohabitation jusqu’en février 2015 : elle constitue une période de
  dormance avant la séparation, non l’abandon du mécanisme;
- l’origine indépendante ou volontaire du départ : elle interdit d’en
  attribuer l’orchestration à P-2, mais ne rompt pas l’utilisation ultérieure de
  ses effets;
- la réalité de la garde maternelle de fait ou de la routine : P-19 place le
  refus maternel du partage dès la rupture avant cette garde de fait, puis P-9
  oppose la routine au partage;
- l’étiquette de « compromis » appliquée à P-16 : elle ne fournit aucun critère
  centré sur l’enfant expliquant les frontières retenues;
- la rédaction de P-19 par une autre avocate : elle limite l’attribution
  personnelle à cette rédactrice, non la continuité de la position assermentée
  d’Élise.

La conformité de la séquence au mécanisme expressément planifié dans P-2 est
documentairement démontrable. Seules la relecture matérielle de P-2 et la
mémoire consciente de son texte exact demeurent inconnues; elles sont inutiles.
Le concert tacite entre Élise et Me Ayoub repose indépendamment sur P-2
directement communiqué à Élise, P-8 transmis par Élise à Me Ayoub, puis P-9,
P-16 et P-18 pris par Me Ayoub au nom de sa cliente. Il ne doit pas être
confondu avec l'existence, non établie, d'un concert avec Me Ferreira.

## Directive d’interprétation — origine et fonction de la reconfiguration familiale

La mémoire de travail gouvernante est :
`legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/12_memoire_reconfiguration_familiale_statu_quo.md`.

P-2 ne propose pas seulement un résultat juridique. Il décrit un moyen de
modifier la base à partir de laquelle le Tribunal décidera : faire sortir le
père, maintenir les enfants auprès de la mère, laisser cette configuration
devenir une routine, puis compter sur l'hésitation des juges à la modifier. Le
besoin de cette reconfiguration naît de l'écart entre le régime déjà recherché
pour la mère et les faits relatifs aux enfants qui auraient normalement dû
déterminer le régime.

P-2 constitue ainsi une preuve directe du dessein de substitution de la base
décisionnelle. La séquence de 2015 en constitue l'exécution fonctionnelle
différée et adaptée alléguée : prospective par la routine dans le plan de 2013,
puis rétrospective par le portrait historique soumis sous serment en 2015.

### Verrou anti-répétition — objections relatives à la reconfiguration

La mémoire gouvernante des objections déjà examinées est :
`legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/13_verrou_objections_reconfiguration_interet_enfants.md`.

Sans élément nouveau précisément identifié, ne plus présenter comme objections
intactes :

- que des allégations de violence vraies suffiraient à expliquer l’ensemble du
  plan : elles pourraient justifier une mesure protectrice correspondante, mais
  n’expliquent pas la préférence durable simultanée pour des accès paternels
  fréquents et plus étendus qu’une fin de semaine sur deux;
- que le maintien des liens affectifs expliquerait cette préférence malgré la
  compromission alléguée : la sécurité et le développement doivent d’abord être
  assurés, et aucun mécanisme de supervision, d’évaluation ou de progression
  fondé sur le risque n’est documenté;
- que le risque aurait été exclusivement lié à la cohabitation : P-2 prévoit
  des accès sans coucher après la relocalisation et P-4 étend le registre de
  préoccupation à l’enfant;
- que l’absence d’un statu quo maternel était l’obstacle fondamental : le point
  gouvernant est l’écart entre le régime déjà recherché pour la mère et les
  faits relatifs aux enfants qui devaient déterminer les modalités conformes à
  leur intérêt;
- que la routine serait nécessairement indépendante du refus du partage :
  P-19 place ce refus dès la rupture et P-9 invoque ensuite la routine qui en
  résulte.

Les limites restantes sont plus étroites : la chaîne n'établit ni
l'inexistence universelle de tout incident de violence, ni l'orchestration du
départ, ni la participation de Me Ferreira au concert entre les deux sœurs, ni
les éléments de chacun des parjures allégués dans P-19. Ces limites ne
diminuent ni la preuve du dessein exprimé dans P-2, ni la forte inférence de
concert Élise–Me Ayoub, ni la concordance fonctionnelle des actes.

## Directive d'interprétation — concert, cible et base décisionnelle

Le verrou gouvernant est :
`legal/dossier_plaidoirie/06_verrou_concert_substitution_base_decisionnelle_tribunal.md`.

Il faut désormais distinguer sans les confondre :

- **le dessein** : P-2 fixe la préférence maternelle, décrit le véhicule de
  reconfiguration et explique l'utilité judiciaire future de la routine;
- **le concert** : les communications et les actes complémentaires de 2015
  soutiennent fortement un concert tacite entre Élise et Me Ayoub. Une
  acceptation expresse de P-2, sa relecture ou la mémoire de son texte exact ne
  sont pas nécessaires;
- **le départ** : il demeure volontaire et indépendant des défenderesses; il
  fournit seulement le préalable matériel que la procédure devait initialement
  produire;
- **les négociations** : leur insincérité alléguée documente la destination et
  le concert, mais n'est pas présentée comme un crime autonome ni comme une
  fraude ayant trompé le père;
- **la cible** : la tromperie alléguée vise la base factuelle fournie au
  Tribunal, qui devait appliquer l'article 33 C.c.Q.;
- **la réalisation judiciaire** : P-19 est l'acte sous serment d'Élise, rédigé
  par Me Ferreira, qui fournit la base historique et consensuelle alléguée. La
  participation personnelle de Me Ayoub à sa rédaction n'est pas établie et
  n'est pas requise pour le concert antérieur entre les deux sœurs;
- **l'étape suivante** : chaque énoncé de P-19 qualifié de parjure doit encore
  être éprouvé quant à sa déclaration exacte, sa fausseté objective, la
  connaissance personnelle d'Élise, son caractère volontaire, l'intention de
  tromper le Tribunal et sa fonction dans les conclusions recherchées; pour
  toute qualification pénale, la corroboration exigée par l'article 133 C.cr.
  doit aussi être vérifiée.

Sans nouvelle source, erreur de cote, d'attribution ou de transcription, ne pas
rouvrir le bloc général au motif abstrait que Me Ayoub n'aurait pas relu P-2,
que le départ n'aurait pas été orchestré, que P-16 n'aurait pas été appliqué,
que le 2-2-3 n'aurait pas été optimal, que Me Ferreira a rédigé P-19 ou que le
père n'a pas été trompé. Les questions d'admissibilité, de causalité et de
qualification juridique demeurent des modules distincts.

## Audit automatisé de la chaîne des pièces

La commande suivante valide en lecture seule les fiches `legal/piece*.md`, le
registre technique `legal/bordereau_pieces.md`, le bordereau procédural
`legal/bordereau_bloc_depot.md`, les objets PostgreSQL, les fichiers originaux,
les renderers et l’assemblage `pieces_pdf/` :

```bash
python manage.py audit_piece_files
```

Options utiles :

```bash
# Échec de la commande si une erreur bloquante est constatée
python manage.py audit_piece_files --strict

# Rapports détaillés JSON et CSV
python manage.py audit_piece_files --output-dir /tmp/audit-piece-chain
```

L’audit distingue trois seuils : `source_ready`, `render_ready` et
`communication_ready`. Un placeholder, une cote manquante, une divergence de
source ou un PDF invalide bloque `communication_ready`.

### État constaté le 27 juillet 2026, après régénération complète

- Le registre technique et le bordereau de dépôt contiennent tous deux les
  cotes P-1 à P-106.
- Les 22 groupes de sous-cotes indexés dans le bordereau de dépôt concordent
  avec leur source technique.
- **L’assemblage contient les 106 cotes, 1 425 pages, aucun placeholder,
  aucune erreur de rendu.** P-106 est assemblée.
- P-19, P-40 et P-42 (actes de la partie adverse) et P-58 à P-64
  (conversations) sont désormais rendus depuis la base plutôt que laissés en
  placeholder — voir `legal/METHODOLOGIE_POST_DEPOT.md` §9.2 sur les deux
  régimes d’origine.
- Restent 9 erreurs de niveau `source`, qui bloquent les trois seuils : six
  divergences de liaison (P-22, P-27, P-92, P-98, P-100, P-106) et trois
  fiches sans identité résoluble. Le détail est au §9 de la méthodologie.

## Méthodologie postérieure au dépôt

La méthodologie approuvée est consignée dans
`legal/METHODOLOGIE_POST_DEPOT.md`.

Elle fixe notamment :

- la conservation immuable du dépôt initial;
- la séparation de la demande amendée;
- le verrouillage des cotes P-1 à P-106;
- la concordance entre versions;
- les identifiants stables des faits;
- le journal des changements;
- les barrières `source_ready`, `render_ready` et `communication_ready`.

La forme définitive de la section « Exposé des faits » demeure expressément
ouverte. Plusieurs variantes doivent pouvoir être expérimentées sans qu’un plan
chronologique, thématique, juridique ou hybride soit présumé choisi.
