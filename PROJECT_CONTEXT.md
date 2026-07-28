# Mémoire de continuité — projet `court`

Dernière mise à jour : 27 juillet 2026

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
P-9, P-16 ou P-19 :

- selon le demandeur, le **véhicule procédural immédiat** annoncé dans P-2 —
  requête d’urgence en juin 2013 et éviction judiciaire du père — n’a pas été
  exécuté sous cette forme;
- le **plan fonctionnel** visait la garde exclusive par la sortie du père, la
  garde maternelle de fait, l’installation d’une routine et l’utilisation de
  cette routine pour résister à un changement;
- le départ du père le 23 février 2015, que le demandeur qualifie de
  volontaire, a satisfait autrement le préalable de sa sortie. P-19 établit le
  départ, sa date et le logement à proximité, mais non sa qualification de
  volontaire. Il n’est pas allégué que ce départ a été causé ou orchestré par
  P-2 ou par les défenderesses;
- P-9 invoque ensuite, contre la garde partagée, la « routine établie depuis
  plus deux mois »; P-16 maintient la garde maternelle avec une progression
  sous le partage égal; P-19 demande la consécration judiciaire de la garde;
- le départ rend sans objet l’utilisation des allégations de violence pour
  obtenir l’éviction, mais non leur pertinence éventuelle pour la sécurité des
  enfants. Leur disparition du corpus P-9, P-16 à P-19, malgré les nuitées
  offertes sans pont explicatif, est analysée comme un indice
  d’instrumentalité, non comme une preuve autonome de fausseté;
- P-19 ajoute au motif situationnel récent de P-9 une marginalité paternelle
  historique (§§15-17). La comparaison établit directement la différence entre
  les motifs exprimés; leur qualification comme substitution destinée à
  justifier le même refus constitue une inférence. La non-conformité du portrait
  historique à la vie réellement vécue doit être démontrée par la preuve
  indépendante.

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

La chaîne P-2 → P-9 → P-16 → P-18 → P-19 constitue un **indice sérieux
d’instrumentalité** et soutient cumulativement une **inférence sérieuse
d’insincérité**. Elle ne prouve pas, à elle seule, la fausseté des allégations
de violence, une fausseté consciente de chaque position ou un concert
frauduleux. Les tensions dépendantes ne doivent pas être additionnées
mécaniquement : leur force vient de leur convergence structurée et de la
capacité prédictive de P-2.

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
une correspondance documentaire objectivement démontrable. Ce qui demeure
inférentiel est la proposition plus étroite selon laquelle les acteurs auraient
matériellement rouvert P-2, s’en seraient explicitement souvenus ou se seraient
concertés pour l’exécuter. Cette preuve subjective n’est pas nécessaire à la
thèse de l’**exécution fonctionnelle différée et adaptée**.

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
