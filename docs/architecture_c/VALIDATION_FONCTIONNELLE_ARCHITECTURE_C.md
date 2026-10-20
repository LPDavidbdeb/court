# Agent B — Validation fonctionnelle de C par combinaison des deux arbres

19 octobre 2026 — **Étude de conception, sans autorisation d'implémentation.**

## Périmètre et résultat

La combinaison proposée suffit pour organiser les affirmations, les raisonnements et les réserves dans le document, puis leur rattacher les éléments documentaires explicitement choisis. Les cas danse, garderie et synthèse ne nécessitent pas de recopier les conclusions dans Preuve.

Deux compléments sont nécessaires pour satisfaire tout le nouveau mandat : admettre une analyse interne comme contexte de rédaction versionné, et représenter les dépendances déclarées entre propositions. Deux contrats opératoires doivent également être précisés : la reprise partielle entre documents et la sélection de photographies dans un événement composé. Un seul nouveau type de relation est recommandé, LienRedactionnel; aucun arbre documentaire parallèle ni lien entre arbres de preuve n'est nécessaire.

Le verdict porte sur la **suffisance de la conception**. Aucun de ces comportements n'est présenté comme une fonctionnalité déjà exécutée dans l'application.

### Sources et état de référence

- [Addendum de C conservé au commit 06fe44c](https://github.com/LPDavidbdeb/court/blob/06fe44c1a7e8582792f9d1fcfcba8155046168ee/docs/modele_preuve/ADDENDUM_AGENT_B_NOTE_02_PONT_PROBATOIRE.md), notamment §§ 2.2, 4, 5, 7 et 8.2.
- [CONCEPTION_PREUVE, état 14f7533](https://github.com/LPDavidbdeb/court/blob/14f7533650d2a28832698b2222ced1df1cd89bb1/docs/modele_preuve/CONCEPTION_PREUVE.md), §§ 10–12 et 16. Les anciens arbres à propositions sont relus comme des cas d'usage, pas comme des prescriptions du nouveau modèle.
- [Référence du thème danse](https://github.com/LPDavidbdeb/court/blob/14f7533650d2a28832698b2222ced1df1cd89bb1/legal/implication_parentale_recurrence/01_cours_danse_mere.md), notamment théorie, sessions, conclusion et limites.
- [Référence du thème garderie](https://github.com/LPDavidbdeb/court/blob/14f7533650d2a28832698b2222ced1df1cd89bb1/legal/implication_parentale_recurrence/02_garderie.md).
- [Architecture des causes et des versions](https://github.com/LPDavidbdeb/court/blob/14f7533650d2a28832698b2222ced1df1cd89bb1/docs/modele_preuve/ARCHITECTURE_CAUSES.md), § 3.
- [Correspondance et extrémités existantes](https://github.com/LPDavidbdeb/court/blob/14f7533650d2a28832698b2222ced1df1cd89bb1/document_manager/models.py#L552), et contrats de LibraryNode, Statement et VersionTexte du même module.
- Note 02 consolidée du 19 octobre, revue pour les scénarios T01–T22; mémoire de continuité et méthodologie post-dépôt lues.
- Mandat joint, attachment 398ec23f-fc5c-4108-a453-4e6086efa632. SHA-256 : c83848ac549657e777f764700ffdfadd9cc68ca94bdd5da9c45d306058315701.

À l'ouverture de cette étude : E01=14f7533650d2a28832698b2222ced1df1cd89bb1; intégration=212a7feee81aef46a5b43d36e8eeafe0f8870064; branche documentaire=06fe44c1a7e8582792f9d1fcfcba8155046168ee. Répertoire principal propre. Le rapport est produit sous /private/tmp, sans checkout, commit, push, fusion, accès PostgreSQL ou intervention sur le serveur.

Les identifiants N.*, S*, UP.*, PN.* et Q* ci-dessous sont des identifiants de conception. Les PK de sources mentionnées proviennent de la documentation lue; aucune vérification des objets en base ni des originaux n'a été effectuée. Q100 signifie une ou plusieurs PHRASE futures à délimiter et certifier dans Email 100; aucune nouvelle Quote réelle ni borne n'est inventée.

Pour le parcours de réutilisation, Q347 désigne le même fragment PHRASE futur relatif à l'adaptation d'horaire dans Email 347. Si plusieurs phrases complètes sont nécessaires, elles auront des identités de fragments distinctes sous le même courriel; leur répétition ne créera toujours qu'une pièce documentaire.

## A. Matrice de couverture et parcours fonctionnels

### A.1 Sens des statuts

- **Couvert** : les objets et contrats déjà proposés dans C suffisent; aucune extension nouvelle n'est nécessaire pour ce comportement.
- **Couvert sous condition** : le parcours nécessite un arbitrage, un complément de contrat identifié ici ou une capacité technique déjà prévue mais indisponible.
- **Non couvert** : C actuelle ne possède pas la relation ou le contexte exigé; le texte peut en parler, mais le comportement explicite demandé n'est pas enregistré.

Les couvertures ne constituent ni validation factuelle des conclusions ni succès de tests applicatifs.

### A.2 U1/U2 — seuls les points restant conditionnels ou incomplets

La revue porte sur les 22 scénarios T01–T22. La séparation des deux arbres ne révèle pas de nouvelle lacune structurelle pour leurs autres comportements. En particulier, l'appui collectif de T08 est déjà représenté par des utilisations propres à la conclusion ou au groupe; il n'exige pas de recopier une conclusion dans Preuve.

| Scénarios / comportement | Objets de C et parcours concret | Création, modification, copie et réutilisation | Résultat observable et réserve | Statut |
|---|---|---|---|---|
| T04/T15/T22 : paragraphes à profondeurs variables, sorties cohérentes | LibraryNode typé; index de numérotation commun; ResultatVersion | Créer les groupes sans compteur; déplacer/insérer un paragraphe conserve sa PK; copier crée une nouvelle occurrence et recalcule les numéros | Suite continue, supports invisibles non numérotés. Le résolveur actuel par profondeur ne suffit pas; la stratégie neutre de L1 reste à réaliser | Couvert sous condition déjà prévue |
| T09 : neuf paragraphes d'acte et leurs sous-cotes | Occurrences source, CompositionCitation, SegmentCitation | Sélectionner 4–7 et 14–18; composer en ordre source; réutiliser les mêmes occurrences dans U2 | Numéros historiques et omission conservés. La granularité de sous-cotation et la vérification des passages d'actes restent à approuver | Couvert sous condition D04/D07 du premier addendum |
| T14/T19 : citation consultable et fidèle | Adaptateurs, PHRASE et route contextuelle du pont | Charger par régime; refuser une certification ineffective; ne pas élargir les anciennes fiches Quote | Lien vers le passage correct, anciennes routes toujours isolées. Aucune PHRASE certifiée réelle n'est présumée disponible | Couvert sous condition du contrat cible de l'Agent A |
| T16/T17/T20 : isolation, gel et intégrité | VersionActe, copie entière de Preuve, usages propres, contenu gelé | Copier/remapper; modifier seulement le périmètre choisi; protéger les états gelés et les écritures de masse | Ancien bordereau et autres brouillons inchangés. Les gardes, le stockage et le protocole de gel restent des réalisations futures | Couvert sous condition déjà prévue |
| T16 et sous-cotation : nouvelle version avec pièces ajoutées/retirées | Bordereau central qualifié par version | Recalculer seulement la version de travail; conserver le bordereau gelé et la concordance | La politique chronologique future doit être articulée explicitement avec les cotes permanentes historiques | Couvert sous condition D05 |

Les manques de contenu de U1 — branche A non reçue et sous-item B2.R08.a vide — restent des manques d'entrée. Aucun nouveau modèle ne peut les compléter. Les autres sélections exactes et certifications attendront leurs sources; elles ne sont pas déduites d'une simple capacité de stockage.

### A.3 Danse — couverture des six comportements demandés

La représentation détaillée et les sélections sont données en B. Les libellés D, I, T et R sont ici des annotations de lecture : déclaration documentaire, inférence de l'auteur, témoignage à mobiliser, réserve. Ce ne sont pas de nouveaux champs obligatoires.

| Comportement | Objets et parcours | Opérations sur le cycle de vie | Résultat observable | Statut |
|---|---|---|---|---|
| B1 — Organisation en sessions | S1 dans N.DANSE; UP.D1 sélectionne PDF 59 et calendrier PhotoDocument 4 | Créer l'énoncé et ses deux appuis; réviser le texte par détachement; reprendre le bloc et ses usages | Le texte distingue continuité mentionnée dans la biographie et structure illustrée par le calendrier récent | Couvert |
| B2 — Créneaux par session | S2 et sous-items par session; UP.D2 sélectionne les communications/occurrences correspondantes | Ajouter ou réviser une session sans modifier les autres; copier ses appuis seulement si cette session est reprise | Mardi/mercredi ou lundi sont associés à leurs sessions. Le jour d'une session n'est pas transporté automatiquement à une autre | Couvert |
| B3 — Absences récurrentes | S1+S2, raisonnement rédigé et réserve dans S2 | Écrire l'extension proposée par l'auteur; réviser les prémisses et leur texte; réutiliser les pièces choisies | La récurrence est exposée comme raisonnement; aucune liste fictive de présences à chaque cours n'est générée | Couvert |
| B4 — Communications/calendrier | Preuve documentaire organisée; usages distincts pour S1/S2/S3 | Sélectionner les feuilles pertinentes; modifier un arbre partagé par copie; conserver les mêmes sources | Une source reste unique au bordereau de la version malgré plusieurs utilisations | Couvert |
| B5 — Limites et exceptions | Sous-items Statement R.D et T.D liés rédactionnellement à S2/S3 | Créer, afficher et copier avec le bloc; signaler une reprise qui les omet | Calendrier 2025–2026 distinct des dates historiques; présence de Johanne distincte de responsabilité; absence de visite distincte de présence de la mère | Couvert |
| B6 — Conclusion sur les soins | S3; UP.D3 propres à la conclusion; texte T.D sur le mode normal et l'authentification | Sélection explicite; reformulation avec réexamen; copie des usages sans nouveau document source | Absence de la mère et prise en charge par le père restent deux propositions distinctes; l'une ne certifie pas l'autre | Couvert |

### A.4 Garderie et synthèse

| Comportement | Objets et parcours | Création/modification/copie/réutilisation | Résultat observable | Statut |
|---|---|---|---|---|
| C1 — Trajets et coordination documentés | S4; UP.G4 vers Q54/Q369/Q29/Q371 | Créer les occurrences textuelles; sélectionner les passages; copier et remapper les usages | Distinguer trajet annoncé, trajet rapporté et relais; ne pas transformer chaque message en trajet personnellement accompli | Couvert |
| C2 — Articulation horaires/soins | S5; UP.G5 vers la preuve garderie et UP.D5 vers Q347 de la preuve danse | Réutiliser la même feuille Q347 dans un autre thème; modifier les portées d'utilisation indépendamment | Même Email 347, mêmes fragments, rôles différents; aucune cote supplémentaire par thème | Couvert |
| C3 — Mode général et responsabilités | S5/S6; témoignage et réserves dans leurs sous-items; UP.G6 explicites | Rédiger le mode allégué, ses limites et la conclusion; reprendre leur bloc complet | Les points documentaires corroborent le mode décrit; ils ne deviennent pas un registre exhaustif ni un partage de 50 % | Couvert |
| C4 — Photographies pertinentes d'un événement composé | Feuilles Photo avec contenant Event 214 explicite; UP.PH4 | Sélectionner les photos du trajet; conserver l'événement source entier; exclure de la sélection celles étrangères au trajet | Les photos de 9 h 32 ne prolongent pas le trajet décrit jusqu'à 8 h 36. Le contrat Photo-dans-Event doit être explicité | Couvert sous condition CF4 |
| D1 — Conclusion générale dans le même document | S7, deux UP propres et prose réunissant S3/S6 | Créer S7; reprendre les sélections pertinentes; modifier ses usages sans changer S3/S6 | Une conclusion et des appuis explicites sont visibles, sans autre affirmation dans Preuve | Couvert |
| D2 — Dépendance déclarée S7→S3 et S7→S6 | Aucune relation correspondante dans C actuelle | La prose permet de l'écrire; partager des preuves ne permet pas d'enregistrer/interroger cette déclaration | Pas de liste fiable des dépendances ni de contrôle de proposition modifiée à partir des seuls usages | Non couvert; CF2 recommandé |
| D3 — Analyse autonome puis demande | Document de travail existant, puis contexte versionné et reprise partielle | Écrire dans Document; rattacher les UP exige un contexte; transférer une sélection de paragraphes avec cartes de correspondance | Analyse initiale indépendante, nouvelle rédaction avec nouveaux usages et nouveaux numéros | Couvert sous conditions CF1/CF3 |

## B. Démonstration des deux arbres combinés

### B.1 Arbre documentaire : propositions et raisonnement

V.ANALYSE est un contexte de rédaction interne proposé en CF1. Les références S1..S7 identifient des propositions, pas leurs numéros définitifs ni des PK.

~~~text
Document PRODUCED de V.ANALYSE
└─ N.RACINE                                        REGROUPEMENT
   ├─ N.DANSE                                      REGROUPEMENT
   │  ├─ N.S1 → Statement S1                       PARAGRAPHE
   │  │    Structure en sessions et continuité alléguée.
   │  │    D : ce que le calendrier/la biographie indiquent.
   │  │    I : portée attribuée par l'auteur à leur combinaison.
   │  ├─ N.S2 → Statement S2                       PARAGRAPHE
   │  │  ├─ N.S2.H2010 → Statement                 SOUS_ITEM
   │  │  │    Cours suivi pendant cette session; jour et bornes non documentés.
   │  │  ├─ N.S2.A2010 → Statement                 SOUS_ITEM
   │  │  │    Créneaux de l'automne 2010, d'après les communications.
   │  │  ├─ N.S2.H2011 → Statement                 SOUS_ITEM
   │  │  ├─ N.S2.H2012 → Statement                 SOUS_ITEM
   │  │  ├─ N.S2.A2013 → Statement                 SOUS_ITEM
   │  │  │    Document seul : visite; avec règle testimoniale de LP : lundi.
   │  │  ├─ N.S2.H2014 → Statement                 SOUS_ITEM
   │  │  │    Occurrences du lundi; contexte des photographies exposé.
   │  │  └─ N.S2.LIMITES → Statement               SOUS_ITEM
   │  │       R : créneau propre à la session; bornes historiques non inventées.
   │  └─ N.S3 → Statement S3                       PARAGRAPHE, CONCLUSION
   │     │  I : pendant ces absences, le père était normalement responsable
   │     │      des soins, selon le raisonnement et le témoignage exposés.
   │     ├─ N.S3.T → Statement T.D                 SOUS_ITEM
   │     │    T : rôle, soins et mode familial normal à porter par témoignage;
   │     │        contexte des photographies à authentifier.
   │     └─ N.S3.R → Statement R.D                 SOUS_ITEM
   │          R : normalement seul; visites et aides occasionnelles;
   │              aucune équivalence automatique absence/prise en charge.
   ├─ N.GARDERIE                                   REGROUPEMENT
   │  ├─ N.S4 → Statement S4                       PARAGRAPHE
   │  │    D : coordination, trajets annoncés/rapportés et relais documentés.
   │  │    Sous-items : exemples datés et portée de chaque source,
   │  │    dont N.S4.PHOTOS → Statement             SOUS_ITEM.
   │  ├─ N.S5 → Statement S5                       PARAGRAPHE
   │  │    I/T : mode matin/soir décrit par l'auteur et adaptation aux horaires.
   │  │    R : Q347 ne nomme pas la garderie; les lieux manquants exigent contexte.
   │  └─ N.S6 → Statement S6                       PARAGRAPHE, CONCLUSION
   │     │  I : ces tâches appartenaient à ses responsabilités répétées,
   │     │      selon les éléments et le mode général exposés.
   │     └─ N.S6.R → Statement R.G                 SOUS_ITEM
   │          R : pas d'alternance parfaite; relais; soins ordinaires et
   │              trajet médical d'exception restent distingués.
   └─ N.SYNTHESE                                   REGROUPEMENT
      └─ N.S7 → Statement S7                       PARAGRAPHE, CONCLUSION GENERALE
         │  I : les responsabilités décrites couvrent plusieurs catégories,
         │      et l'auteur en tire une synthèse de participation parentale.
         └─ N.S7.R → Statement R.SYN               SOUS_ITEM
              R : cette synthèse n'est ni un calcul de temps ni une validation
                  automatique des inférences.
~~~

Le profil de numérotation de C peut imprimer S1..S7 en 1..7, malgré les profondeurs et les sous-items. Les étiquettes D/I/T/R restent du contenu ou une présentation éditoriale. Le parent et les enfants maintiennent le raisonnement et ses limites ensemble.

Le statut « conclusion principale close » de la référence danse est conservé comme appréciation de l'auteur. Les besoins de témoignage et d'authentification mentionnés ici décrivent les fondements exposés dans cette référence; ils ne rouvrent pas son appréciation générale et ne deviennent pas des conditions nouvelles inventées par le logiciel.

### B.2 Arbres probatoires : sources et regroupements

~~~text
PR.DANSE_SOURCES
└─ PN.D.ROOT
   ├─ PN.D.CADRES
   │  ├─ PN.D.BIO59        → passage de PDFDocument 59
   │  └─ PN.D.CAL4         → PhotoDocument 4, calendrier entier
   ├─ PN.D.COMMUNICATIONS
   │  ├─ PN.D.A2010        → Q81, Q80, Q100
   │  ├─ PN.D.H2011        → Q114, Q116
   │  ├─ PN.D.H2012        → Q347
   │  └─ PN.D.A2013        → Q498, Q499
   ├─ PN.D.PHOTOGRAPHIES
   │  └─ E19, E46, E52, E274, E278 → événements documentaires correspondants
   └─ PN.D.COMM2016        → Q305, Q7, Q306, non sélectionnés par simple présence

PR.GARDERIE_SOURCES
└─ PN.G.ROOT
   ├─ PN.G.COMMUNICATIONS  → Q54, Q369, Q29, Q371
   ├─ PN.G.PHOTOGRAPHIES
   │  ├─ E213             → Event 213
   │  └─ GROUPE.E214
   │     └─ PH214.TRACE[*] → Photo choisie, contenant Event 214 explicite
   └─ PN.G.EXCEPTIONS
      └─ messages pertinents de l'urgence médicale du 3 décembre 2014,
         avec leur ChatSequence vérifiée, seulement si explicitement utilisés
~~~

Un groupe de preuve organise les éléments par support, période ou dossier; il ne contient pas un deuxième Statement « le père était normalement responsable ». Les qualifications et le raisonnement figurent dans N.S3/N.S6.

Les événements et calendriers restent des unités documentaires structurées. La borne exacte de chaque PHRASE et les PK de photos pertinentes doivent être obtenues des sources avant usage réel. Les subdivisions ci-dessus ne créent aucune nouvelle pièce.

### B.3 Relations et sélections concrètes

Une ligne UP représente une UtilisationPreuve; chaque élément de la sélection devient une SelectionPreuve, ou une branche explicitement choisie. Le recours à plusieurs preuves implique plusieurs UP sur la même cible.

| Usage | Cible | Preuve | Sélection explicite | Portée |
|---|---|---|---|---|
| UP.D1 | N.S1 | PR.DANSE_SOURCES | BIO59, CAL4 | Continuité mentionnée et structure des cours. |
| UP.D2 | N.S2 | PR.DANSE_SOURCES | Q100, Q114, Q116, Q347, Q498, Q499, E19, E274, E278 | Exemples de sessions; le texte indique le fondement différent de chaque jour proposé. |
| UP.D3 | N.S3 | PR.DANSE_SOURCES | BIO59, CAL4, Q347, E46, E52, E274, E278 | Corpus documentaire choisi pour la conclusion intermédiaire; le témoignage reste exprimé dans T.D. |
| UP.G4 | N.S4 | PR.GARDERIE_SOURCES | Q54, Q369, Q29, Q371 | Coordination, annonce, récit d'un retour et relais. |
| UP.PH4 | N.S4.PHOTOS | PR.GARDERIE_SOURCES | E213 et PH214.TRACE[*] | Photos pertinentes seulement; rôle/destination à authentifier. |
| UP.G5 | N.S5 | PR.GARDERIE_SOURCES | Q54, Q369 | Articulation annoncée des responsabilités et horaires. |
| UP.D5 | N.S5 | PR.DANSE_SOURCES | Q347 | Même passage que dans la danse, utilisé comme pont logistique; ne prouve pas textuellement un trajet de garderie. |
| UP.G6 | N.S6 | PR.GARDERIE_SOURCES | Q54, Q369, Q29, Q371 | Éléments documentaires choisis pour la conclusion garderie. |
| UP.D7 | N.S7 | PR.DANSE_SOURCES | Q347, E46, E52 | Sous-ensemble documentaire expressément réutilisé dans la synthèse. |
| UP.G7 | N.S7 | PR.GARDERIE_SOURCES | Q54, Q29 | Deux catégories d'occurrences choisies pour la synthèse. |

Les usages sur N.S2 ne justifient pas silencieusement chacun de ses sous-items. N.S2 est un Statement : son utilisation n'autorise pas à elle seule une citation dans un autre Statement enfant. Celui-ci reçoit son propre UP; une autre possibilité est d'attacher l'appui destiné à être partagé à un véritable REGROUPEMENT ancêtre et de le désigner explicitement depuis l'insertion, selon le contrat de C. Les portées particulières peuvent ainsi être précisées sans changer le modèle.

Les conclusions S3 et S6 ont des utilisations propres; S7 possède les siennes. Aucune des trois ne dépend, pour son rattachement documentaire, d'une union automatique des sources de ses descendants. Les références de raisonnement S7→S3/S6 seront des LienRedactionnel distincts, examinés en C.2.

### B.4 Résultat vérifiable du parcours

1. Dans le document combiné, Q347 figure dans UP.D2, UP.D3, UP.D5 et UP.D7 : plusieurs utilisations, une identité de passage, un Email 347 au bordereau de cette version.
2. Le même élément n'a pas besoin d'être ajouté dans PR.GARDERIE_SOURCES : N.S5 utilise directement la sélection utile de PR.DANSE_SOURCES. Aucun renvoi Preuve→Preuve n'est requis.
3. Q305/Q7/Q306 n'entrent pas au bordereau par leur seule présence dans PR.DANSE_SOURCES. Les ajouter exige un usage sélectionné.
4. Copier S7 seul dans une demande, avec seulement ses liens de dépendance vers une analyse externe, n'importe aucune pièce automatiquement.
5. Copier explicitement UP.D7 et UP.G7 dans cette demande ajoute exactement cinq unités documentaires : Email 347, Events 46 et 52, Emails 54 et 29. Les références et sous-cotes sont résolues dans la demande, jamais reprises depuis l'analyse.
6. Modifier PR.DANSE_SOURCES pour cette demande passe par la copie entière et le repointage des seuls usages choisis si la preuve est partagée. L'analyse initiale conserve son organisation.

Ces résultats sont déduits des sélections énumérées, sans exécution de service ni certification de leurs sources. La validité de l'inférence S7 reste celle que l'auteur soutient dans le texte.

### B.5 Fidélité des exemples et limites à conserver

- Le calendrier récent illustre une structure; il ne fournit pas les dates historiques de toutes les sessions.
- La biographie, les communications et les événements ont des fonctions différentes. Les récitals d'Alexia ne deviennent pas des marqueurs du jour de danse de la mère.
- Pour l'automne 2013, Q498/Q499 documentent une visite. Le lien avec la danse est présenté avec la règle testimoniale du demandeur; le texte ne devient pas un courriel nommant explicitement la danse.
- L'absence de visite de Johanne ne devient pas la présence de la mère. Une visite ou un spectacle n'atteste pas automatiquement les soins accomplis par le père.
- Les photographies des routines et le texte de l'Email 347 corroborent des éléments distincts; le mode normal et certaines attributions reposent aussi sur le témoignage exposé.
- L'Email 54 ne nomme pas le lieu; l'Email 369 annonce une organisation et ne constitue pas à lui seul le compte rendu d'un trajet accompli. L'Email 29 rapporte le trajet de la veille : date de communication et date du fait sont distinctes.
- L'Email 371 documente un relais; il n'établit pas que le père a personnellement effectué ce trajet.
- L'urgence médicale ne devient pas une occurrence ordinaire de répartition matin/soir.
- Les objets Email 48 et Email 347 sont décrits comme un doublon dans la documentation. La réutilisation présentée ici choisit 347 partout. C déduplique une identité stable; elle ne fusionne pas automatiquement deux PK représentant le même message physique. Ce point de qualité des sources n'appelle pas un second mécanisme de cotation.

## C. Les trois questions particulières

### C.1 Analyse autonome avant la demande

#### Comparaison des solutions

| Solution | Ce qu'elle permet | Difficulté concrète | Évaluation |
|---|---|---|---|
| Document de travail seul, avec les modèles documentaires existants | Texte, occurrences, sections et contenu analytique avant toute demande | UtilisationPreuve.version est obligatoire dans C : aucun usage valide ne peut être rattaché à ce Document sans contexte VersionActe | Suffisant pour rédiger; insuffisant pour tout le scénario d'analyse appuyée |
| Généraliser le conteneur proposé à la rédaction interne | Acte.nature=ANALYSE_INTERNE, VersionActe interne, Document PRODUCED existant; mêmes UP/sélections/compositions/gel | Élargir explicitement le contrat d'Acte, aujourd'hui décrit pour les actes au tribunal et communications entre parties | **Recommandé, CF1** : même architecture, aucune nouvelle table documentaire |
| Rattacher les UP directement au Document ou introduire un ContexteRedaction indépendant | Analyse avec usages sans conteneur Acte | Déplacer la responsabilité versionnelle; redéfinir copies, gel, transmissions et rattachements; ou maintenir deux contextes concurrents | Non nécessaire pour ce scénario; coût supérieur |

Rendre VersionActe nullable sur UP, ou inventer une demande procédurale pour héberger l'analyse, affaiblirait les invariants. La recommandation utilise un document de travail identifiable comme analyse interne, sans présumer un dépôt, une transmission ou une qualification judiciaire.

#### Contrat minimal CF1

1. Acte demeure l'identité durable du document de rédaction; sa nature peut être ANALYSE_INTERNE. L'interface l'appelle « analyse », sans présenter ce document comme une demande.
2. VersionActe conserve une correspondance OneToOne avec son Document PRODUCED et les mêmes invariants d'utilisation. Un Document existant peut être rattaché à ce contexte sans être dupliqué.
3. Plusieurs analyses peuvent réutiliser la même Preuve. Une Preuve reste également constructible avant tout Document ou usage.
4. Une analyse interne peut être gelée volontairement pour être référencée, même sans transmission externe. Le gel ne crée aucun événement de dépôt ni de transmission fictif.
5. Le bordereau de l'analyse est une vue de ses usages, qualifiée comme travail interne. Ses cotes ne sont pas copiées dans une demande.
6. L'analyse et la demande ont des identités et des versions distinctes. Le passage de l'une à l'autre est une reprise éditoriale, pas une transformation silencieuse de l'analyse en demande.

Le scénario examiné peut utiliser la cause déjà identifiée du dossier. Il ne nécessite pas de créer une cause judiciaire fictive. Un besoin futur d'analyse sans cause connue requerrait un contrat de contexte approprié; il n'est pas ajouté aux modèles sous couvert de ce mandat.

#### Identités et reprise partielle : CF3

Le service proposé reprendre_sous_arbre(source, destination, plan_de_reprise) complète les opérations de C. Le plan est une valeur de commande explicitant :

- les occurrences à reprendre, avec leurs descendants rédactionnels utiles;
- le mode conservé/reformulé de chaque texte;
- les usages et sélections repris, et leur portée;
- les réserves ou témoignages inclus dans le bloc;
- les compositions et insertions concernées;
- le devenir des liens rédactionnels : remappés, maintenus comme références externes ou retirés explicitement.

Parcours « analyse danse → demande » :

1. Créer de nouveaux LibraryNode dans le Document de la demande, avec une carte ancien→nouveau. Les occurrences de l'analyse ne sont ni déplacées ni supprimées.
2. Conserver éventuellement le même Statement si le texte est identique, avec détachement obligatoire avant une réécriture ultérieure. Une reformulation reçoit un Statement et une VersionTexte propres.
3. Copier les UP sur les nouvelles cibles et le contexte destination; recopier les sélections vers les mêmes nœuds de preuve. Les sources ne changent pas. Un usage d'un groupe ancêtre non repris doit être choisi explicitement pour une cible destination; il n'est pas hérité par défaut.
4. Copier les compositions nécessaires dans la version destination. Une insertion n'est conservée comme valide que si son Statement/version textuelle et son texte restent compatibles; après reformulation, elle est à réancrer.
5. Recalculer numéros et cotes dans la destination. Les numéros de l'analyse sont des repères d'origine, pas les nouveaux numéros procéduraux.
6. Remapper les liens dont les deux extrémités sont reprises. Pour une cible non reprise, conserver une référence externe explicite ou choisir de la reprendre; ne jamais fabriquer un renvoi interne vers un numéro semblable.
7. Garder la filiation éditoriale. Correspondance et ExtremiteCorrespondance offrent déjà les relations N:M entre Documents et occurrences. Élargir leur contrat de « versions d'un même acte » à la reprise entre documents de rédaction permet de les réutiliser sans nouvelle table de filiation. Leurs services hérités ne sont pas réemployés sans revue de leurs présupposés.

La reprise doit conserver les limites du bloc par défaut. Une omission délibérée de réserve est une décision éditoriale visible; elle ne réemploie pas une confirmation de texte inchangé. Les modifications de la demande n'atteignent pas l'analyse, et inversement. Une analyse gelée conserve ses textes, liens, usages et numéros; une nouvelle version porte ses changements.

### C.2 Reprise de contenu, réutilisation des sources et dépendance déclarée

| Opération | C actuelle | Autorité et résultat |
|---|---|---|
| Reprendre/reformuler S3 dans un autre endroit | Les occurrences, Statements, versions textuelles et opérations de copie fournissent les primitives; reprise partielle à préciser par CF3 | Nouveau texte ou nouvelle occurrence; filiation éditoriale. Aucune dépendance logique n'est déduite de la seule copie. |
| Réutiliser les éléments de S3 pour S7 | Oui : créer des UP sur S7 avec les mêmes preuves et sélections choisies | UP/SelectionPreuve font autorité. Aucune copie de source, aucune nouvelle cote pour la même identité dans une version. |
| Déclarer « S7 dépend de S3 et S6 » | Le texte peut l'exprimer; C ne possède pas de relation dédiée | Partager une pièce ou être enfant du même groupe ne permet pas de retrouver cette déclaration de manière fiable. **CF2 nécessaire** pour l'enregistrer et la suivre. |

#### Pourquoi les relations existantes ne remplacent pas CF2

- LibraryNode.parent exprime l'organisation; il ne distingue pas « développé dans la même section » de « prémisse explicitement invoquée ».
- UP vise des éléments documentaires organisés dans Preuve. Lui faire viser un Statement de l'analyse transformerait ce raisonnement en pseudo-pièce et mélangerait les deux autorités.
- Correspondance exprime une transformation éditoriale : reprise, reformulation, scission ou fusion. « S7 dépend de S3 » n'est pas une transformation de S3 en S7.
- Un texte « voir § 3 » reste rédigeable, mais ne fournit ni identité stable de cible ni détection fiable d'un changement de proposition.

#### Relation minimale CF2 : LienRedactionnel

Une relation neutre de document_manager, sans FK vers Preuve ni import du pont :

| Champ / relation proposé | Fonction |
|---|---|
| source → LibraryNode, FK PROTECT | Occurrence portant le renvoi ou la conclusion dépendante. |
| cible → LibraryNode, FK PROTECT | Occurrence visée, dans le même Document ou un autre. |
| nature = RENVOI ou DEPENDANCE_DECLAREE | Navigation et référence rédactionnelle, ou prémisse expressément déclarée par l'auteur. |
| texte_source_examine → VersionTexte, nullable pour RENVOI | Texte précis de la conclusion lors de la déclaration de dépendance. |
| texte_cible_examine → VersionTexte, nullable pour RENVOI | Texte précis de la proposition invoquée. |
| créé_le; motif facultatif | Trace de la déclaration, sans calcul de validité. |

Unicité (source, cible, nature). Pour DEPENDANCE_DECLAREE, les deux extrémités portent un Statement rédactionnel et leurs VersionTexte sont obligatoires et cohérentes avec ces occurrences. Source et cible ne sont pas le même LibraryNode. Cibler le Statement seul serait ambigu s'il est réutilisé dans plusieurs documents ou à plusieurs endroits.

Pour le premier périmètre, les renvois de propositions concernent les occurrences rédactionnelles porteuses de Statement. Les références à des paragraphes d'actes sources conservent le chemin documentaire de C. Les liens vers des groupes sans proposition ne sont pas nécessaires à l'exemple S3/S6/S7.

Le statut « à revoir » se calcule par comparaison des textes examinés avec ceux des occurrences courantes; il ne demande pas un second champ de degré probatoire. Il faut également vérifier que chaque VersionTexte examinée appartient au Statement actuellement porté par son occurrence : est_courante sur l'ancien Statement ne suffit pas après un détachement. Changer l'une des propositions ne change pas automatiquement l'autre et ne déclare pas son raisonnement faux : la déclaration de dépendance requiert une revue de l'auteur.

#### Exemple de navigation et rendu

~~~text
Lien L73 : source N.S7, cible N.S3, nature DEPENDANCE_DECLAREE
Lien L76 : source N.S7, cible N.S6, nature DEPENDANCE_DECLAREE

Après le paragraphe S7 :
« Dépendances déclarées par l'auteur : § 3 et § 6. »

Dans l'éditeur de S3 :
« Cette proposition est invoquée par S7. »
~~~

Les numéros viennent de l'index des occurrences, jamais d'une chaîne stockée « § 3 ». Déplacer S3 à un autre rang actualise le renvoi de brouillon. Un lien entre documents ajoute le titre et le contexte de version de la cible.

Une projection après le paragraphe suffit à cet exemple. Il n'est pas nécessaire de détourner InsertionRendu, dont le contrat concerne les citations probatoires. Un placement arbitraire de renvois à l'intérieur de phrases n'est pas demandé et n'est pas ajouté à ce périmètre.

#### Modification, copie et historique

- Si S3 ou S7 change de texte, L73 devient « à revoir »; les usages documentaires de S7 restent des relations distinctes. Revoir L73 ne recalcule pas automatiquement les appuis de S7.
- Si S3 et S7 sont copiés ensemble, le nouveau lien vise leurs nouvelles occurrences. Si S7 seul est repris, L73 ne vise pas un nouveau S3 imaginaire : le plan conserve la cible externe ou en prévoit une reprise.
- Une version gelée capture ses liens, les textes examinés, identités, numéros résolus et contexte de cible. Le contenu gelé ajoute un composant liens_redactionnels; cette extension ne modifie aucun ancien contenu déjà conservé.
- La filiation des reprises, avec ses Correspondance, extrémités et textes examinés, est également capturée dans le contenu gelé. Il s'agit d'une évolution explicite de son schéma, sans seconde autorité historique.
- Pour une dépendance entre deux propositions du même Document, le gel les conserve ensemble.
- Pour une DEPENDANCE_DECLAREE vers un autre Document, le gel strict recommandé exige une version cible gelée et le texte correspondant. Une analyse interne peut être gelée à cette fin sans être déposée. L'alternative est de reprendre les prémisses pertinentes dans le document destination.
- En brouillon, une dépendance vers un autre brouillon est possible, avec contrôle des textes et signalement de changements; elle ne suffit pas à autoriser le gel strict.
- Un simple RENVOI externe ne transporte pas le dossier d'appuis de la cible. Le gel peut conserver son repère et le texte observé même si cette cible n'était pas gelée, à condition de l'indiquer comme capture de référence. Il ne présente pas le document cible entier comme figé. L'accès historique ouvre ce repère conservé, avec un accès distinct à l'état courant.

Cette politique rend consultable la raison déclarée de S7 sans importer les pièces de S3/S6. S7 doit sélectionner ses appuis documentaires par des UP propres s'il les mobilise directement.

#### Cycles : contrôle structurel proposé

Recommandation à approuver : autoriser les renvois de navigation réciproques, interdire les cycles de DEPENDANCE_DECLAREE dans le premier profil. Cette convention ne valide aucune inférence.

Avant d'ajouter A→B, vérifier qu'il n'existe pas de chemin B→A formé de dépendances déclarées, y compris entre documents. Le contrôle porte sur les occurrences, pas sur les Statement partagés. Le même texte utilisé deux fois ne constitue pas à lui seul un cycle.

Pour éviter une réactivation implicite de cycle lors d'une réécriture, le contrôle topologique inclut les liens de dépendance conservés mais « à revoir ». L'auteur peut retirer ou réviser un lien dans un brouillon; aucun lien d'une version gelée n'est réécrit.

Les ajouts et changements de cible doivent être sérialisés par un verrou transactionnel commun aux modifications de ce graphe; une vérification sans sérialisation permettrait à A→B et B→A d'être acceptés simultanément. Les écritures de masse doivent subir le même contrôle relationnel avant usage réel.

Il existe ainsi un petit graphe de **déclarations rédactionnelles**. Il ne relie pas des arbres Preuve, ne déroule pas leurs feuilles et ne calcule ni vérité, ni force probante, ni cotes.

### C.3 Témoignages, réserves et degrés d'établissement

| Comportement demandé | A — Rédaction et présentation | B — Structuration ou traitement requis par ce mandat |
|---|---|---|
| Dire qu'un fait doit être établi par témoignage | Statement T.D/T.G, par exemple sous-item de la proposition; préciser le témoin et ce qu'il doit porter dans le texte | Aucun modèle de fausse source. Le mandat ne demande pas une gestion automatisée des témoins ou des audiences. |
| Exposer une réserve ou exception | Statement enfant ou contenu de la proposition; conservation dans la reprise du bloc | Le rôle éditorial déjà proposé peut aider la navigation. Aucun second statut probatoire obligatoire. |
| Présenter une conclusion hypothétique, partielle ou suffisamment établie selon l'auteur | Formulation explicite dans Statement; variantes de rédaction possibles | Aucun calcul de degré demandé. Statement.is_true ne constitue pas cette appréciation et ne la valide pas. |
| Exposer prémisses et raisonnement | Sous-arbres documentaires, paragraphes et conclusions | Le lien CF2 n'est ajouté que pour la déclaration explicite de dépendance et son suivi, effectivement demandés. |
| Distinguer fait documentaire et inférence | Texte et présentation séparés, avec références documentaires des propositions pertinentes | Le logiciel doit préserver cette distinction de rendu; il ne classe pas automatiquement une phrase à partir de la présence d'une pièce. |

Une proposition peut donc être correctement rédigée et conservée sans UP. Un témoignage futur n'engendre ni feuille ELEMENT fictive, ni certificat PHRASE, ni cote. Un témoignage effectivement reçu et matérialisé pourra avoir son traitement documentaire propre, mais ce comportement supplémentaire n'est pas spécifié ici.

La possibilité de rechercher automatiquement « toutes les affirmations encore à établir par témoignage », d'établir des filtres de degré ou de bloquer un export selon un degré prédéfini exigerait des conventions structurées. Ces opérations ne sont pas demandées dans ce mandat; aucun champ ni test n'est ajouté pour elles.

## D. Lacunes constatées, adaptations et autorités

### D.1 Lacunes et conséquences sur L1/L2

| Condition / scénario qui échoue | Pourquoi C actuelle ne suffit pas complètement | Options comparées | Adaptation recommandée | Effet L1 / L2 |
|---|---|---|---|---|
| CF1 — Document analytique seul recevant des UP | FK VersionActe obligatoire, périmètre d'Acte décrit jusqu'ici pour documents procéduraux/communications | Laisser UP sans version; nouveau contexte parallèle; élargir les catégories du conteneur existant | Analyse interne dans le même conteneur versionné, sans nouvelle table documentaire | L1 : présentation neutre inchangée. Avant les premières UP persistées de L2 : contexte interne valide et aucun dépôt fictif. |
| CF2 — Enregistrer et suivre S7→S3/S6 | Ni parenté, ni sources partagées, ni Correspondance ne portent cette sémantique | Renvoi littéral; graphe dans Preuve; relation éditoriale entre occurrences | LienRedactionnel neutre; deux natures; références textuelles examinées; projection et politique historique/cycles explicites | L1 : contrat d'identité, renvois dynamiques, relation neutre et contrôles après approbation. L2 : usages restent distincts; aucun déroulement automatique de dépendances. |
| CF3 — Reprise de quelques paragraphes/groupes avec leurs appuis | Le clonage complet décrit dans C ne fixe pas le traitement des appuis d'ancêtres, liens externes et insertions d'une reprise partielle | Copier tout le Document; copier seulement le texte; reprise ciblée avec plan et remappage | Nouveau contrat de service; réemploi de Correspondance avec portée éditoriale élargie; pas de table de copie parallèle | L1 : carte d'occurrences/textes et devenir des liens. L2 : reprise atomique des UP/sélections choisies. Gel complet reste L5. |
| CF4 — Retenir des photos d'Event 214 sans prolonger le trajet | Sélectionner Event entier n'isole pas ses photos pertinentes; la table des adaptateurs de C explicite surtout PhotoDocument pour une Photo contenue | Modifier la source; créer un faux document filtré; sélectionner Photo avec contenant Event | Expliciter l'adaptateur Photo→Event à partir des champs de contenant déjà prévus | L1 : aucun modèle nouveau. L2 : autoriser/valider cette feuille et son contenant dans le contrat; résolution/rendu détaillés relèvent de L3/L4. |

CF3 et CF4 sont des précisions de services/adaptateurs dans les primitives de C, pas de nouveaux domaines de données. CF2 ajoute une relation parce qu'une opération précise échoue autrement. CF1 élargit le contrat du conteneur existant plutôt que de dupliquer la rédaction.

### D.2 Détail de CF4 : sélection et contenant

Une feuille PH214.x référence une Photo existante et indique Event 214 comme contenant. Son adaptateur vérifie l'appartenance, résout la pièce Event 214 et donne à la photo une identité de fragment et une position dans le contenant. Il n'utilise pas la date de saisie comme date de la pièce.

Le bordereau conserve Event 214 comme unité documentaire entière; les fragments et le rendu probatoire identifient seulement les photos invoquées. La présence d'autres photos dans le contenant ne prolonge pas automatiquement la période attribuée au trajet dans le texte. Le rendu ne doit pas présenter l'ensemble du contenant comme une sélection intégralement utilisée.

Si l'auteur choisit Event 214 entier, le système ne nettoie pas ses photos en silence. Il faut changer explicitement la sélection vers les photos pertinentes. Les plages de temps décrites dans le texte restent attribuées à l'auteur et aux photographies sélectionnées; aucune correction de source n'est autorisée par cette étude.

### D.3 Une seule autorité par responsabilité

| Information | Autorité | Projections ou références permises | Duplication à éviter |
|---|---|---|---|
| Proposition, conclusion, règle de témoignage, réserve | Statement dans son occurrence rédactionnelle | Renvoi par occurrence; copie éditoriale tracée dans un autre document | Même conclusion maintenue comme texte concurrent dans un nœud de preuve. |
| Contenu, identité et provenance de la pièce | Modèle documentaire source et original; adaptateur pour la lecture | Feuilles référentes; captures de rendu au gel | Copier le courriel ou créer une pièce parce qu'il sert un deuxième thème. |
| Organisation des éléments | Preuve/NoeudPreuve | Vues par thème, dates ou source | Reproduire tout le plan argumentatif du document dans l'arbre de preuve. |
| Choix d'appui documentaire | UP/SelectionPreuve | Supports projetés, listes et bordereau | Seconde relation d'appui implicite par parenté ou par lien de dépendance. |
| Dépendance déclarée entre propositions | LienRedactionnel de nature DEPENDANCE_DECLAREE | Renvois et liste des propositions qui l'invoquent | Interpréter la simple réutilisation d'une pièce comme une dépendance. |
| Origine d'un texte repris | Correspondance éditoriale et carte d'occurrences | Historique de reprise et confirmation du traitement | Utiliser cette filiation comme une preuve ou comme une dépendance logique. |
| Affichage des passages et emplacement | CompositionCitation/segments et InsertionRendu | Plusieurs affichages de la même source | Verbatim retapé et modifiable dans chaque paragraphe. |
| Cotes courantes et historiques | Résultat central par version; contenu gelé pour l'histoire | Références actives; concordance par identité | Cotes de travail copiées en dur ou moteurs indépendants par thème. |
| Appréciation du degré par l'auteur | Formulation rédactionnelle | Rôle éditorial facultatif, présentation claire | Champ de vérité déduit de l'existence d'une citation certifiée. |

Le libellé d'un groupe de preuve peut faciliter le repérage. Il n'est pas une seconde proposition évaluée. Une remarque technique de source, par exemple un ancrage invalide, reste un diagnostic du fournisseur; une réserve sur la portée d'un raisonnement est rédactionnelle.

## E. Tests d'acceptation complémentaires

Ces tests complètent T01–T22 pour les comportements nouveaux du mandat. Ils sont spécifiés pour une exécution future isolée; aucun test applicatif, scénario sur sauvegarde réelle ou accès à PostgreSQL n'est effectué ici.

| Test | Scénario et contrôle positif | Contre-épreuve / résultat interdit |
|---|---|---|
| VF01 — Analyse interne | Créer le contexte interne d'un Document PRODUCED puis UP et sélections; constater zéro dépôt/transmission fictif | Un Document sans contexte ne peut recevoir une UP dont la version est inventée ou nulle. CF1. |
| VF02 — Reprise partielle indépendante | Copier S3 et ses sous-items utiles vers la demande, avec nouveaux N/UP et mêmes sources; modifier la copie | Analyse inchangée, détachement du texte partagé; aucun nouveau document source ou numéro conservé de force. CF3. |
| VF03 — Appui d'un ancêtre non repris | Reprendre un enfant; proposer explicitement le support du groupe source et sa portée dans la destination | Aucun héritage silencieux du support de l'ancien parent; annulation si la destination n'est pas choisie. CF3. |
| VF04 — Réécriture et insertions reprises | Reprendre un passage à l'identique, puis une variante reformulée | Première insertion remappée valide; seconde à réancrer si le texte change, même si l'ancien offset reste dans les bornes. CF3. |
| VF05 — Trois opérations distinctes | Copier le texte de S3; sélectionner ses sources pour S7; créer séparément L73 | Aucune opération ne crée automatiquement les deux autres; les trois autorités restent distinctes. CF2/CF3. |
| VF06 — Renvoi et déplacement | L73 vise N.S3; insérer un paragraphe avant lui et ouvrir son lien | Le numéro actif change, la cible reste N.S3; aucune recherche par ancien numéro ou par texte semblable. CF2. |
| VF07 — Texte de prémisse modifié | Modifier S3, puis S7, y compris par détachement vers un nouveau Statement; comparer les textes examinés et leur appartenance aux occurrences | Liens à revoir même si l'ancienne VersionTexte est toujours courante sur l'ancien Statement; aucun degré ou raisonnement validé automatiquement. CF2. |
| VF08 — Référence interdocuments et gel | Lier S7 à une analyse gelée V1; geler la demande; créer V2 de l'analyse et modifier S3 | Le renvoi historique garde V1, son texte et son numéro. Une dépendance vers une analyse encore mutable bloque le gel strict ou exige une reprise interne explicite. CF1/CF2. |
| VF09 — Cycles et occurrences | S7→S3 et S7→S6 acceptés; un chemin de retour vers S7 refusé; renvois de navigation réciproques autorisés | Pas de faux cycle parce que deux occurrences partagent un Statement; pas de cycle masqué par un lien « à revoir ». CF2. |
| VF10 — Concurrence des dépendances | Deux transactions proposent A→B et B→A; contrôle sous le verrou commun | Au plus une création réussit; une écriture de masse ne contourne pas ce contrôle. CF2. |
| VF11 — Dépendance sans import de pièces | Demande contenant S7 et liens externes seuls : aucune pièce importée; ajouter explicitement UP.D7/UP.G7 : cinq pièces attendues | Les autres sources de l'analyse externe restent absentes. Aucune union transitive des usages via L73/L76. |
| VF12 — Témoignage et réserves | Rédiger une prémisse testimoniale et une réserve sans support, puis reprendre le bloc | Zéro pièce/certification fictive; texte et limites conservés; aucune extension automatique d'une absence à une prise en charge. |
| VF13 — Même passage dans plusieurs fonctions | Q347 utilisé pour créneau, coordination et synthèse dans une même version | Une seule pièce et une seule identité de fragment; plusieurs parcours conservés; modifier une portée ne modifie pas les autres. |
| VF14 — Photo dans Event | Données de test : deux photos pertinentes et une étrangère au trajet dans le même Event; sélectionner les deux premières | Pièce Event unique, fragments sélectionnés exacts; troisième photo non invoquée; contenant et source inchangés. Sélectionner l'événement entier ne le filtre pas automatiquement. CF4. |

Les tests de fidélité PHRASE, de numérotation multidepth, de certification et de gel global déjà spécifiés restent applicables. Les cas présents n'ajoutent aucun test de moteur d'inférence, de classement automatique des degrés, de planning des témoins ou de décompte de toutes les occurrences historiques : ces fonctionnalités ne sont pas demandées.

## F. Recommandation et décisions nécessaires

### F.1 Adaptations à approuver avant de figer L1/L2

1. **CF1 : contexte interne** — admettre ANALYSE_INTERNE dans le conteneur versionné proposé et le gel volontaire sans transmission.
2. **CF2 : liens rédactionnels** — approuver LienRedactionnel entre occurrences, ses deux natures, le suivi des textes examinés, la projection des renvois, la règle de cible externe gelée pour une dépendance historique stricte et la politique de cycles.
3. **CF3 : reprise ciblée** — approuver le service de copie partielle avec sélection explicite des appuis et élargissement du contrat de Correspondance éditoriale, sans créer une seconde filiation.
4. **CF4 : photos contenues** — expliciter le contrat Photo→Event avec contenant et sélection de fragments, sans nouveau modèle.

Les arbitrages D01–D12 du premier addendum restent des propositions. Ce rapport ne les valide pas tacitement. Les conditions déjà connues sur numérotation, fidélité, PHRASE, cotation historique et gel réel continuent de s'appliquer; le travail de l'Agent A n'est ni modifié ni présumé basculé.

### F.2 Justification fonctionnelle du verdict

- Les parcours S1..S7 montrent où vivent les propositions, les conclusions intermédiaires et la synthèse, et quelles sélections documentaires les appuient.
- Q347 sert plusieurs fonctions sans nouvelle source ni nouvelle cote; des usages distincts suffisent.
- Les règles et réserves restent dans le document. L'arbre probatoire n'a pas à reproduire les conclusions ou à calculer leur degré.
- L'analyse interne peut utiliser exactement les mêmes primitives versionnelles que la demande, après l'élargissement de contrat identifié.
- La reprise partielle possède un parcours de conservation défini; elle ne se réduit pas à copier du texte.
- Une relation supplémentaire est justifiée pour une demande nouvelle précise : déclarer et suivre S7→S3/S6. Cette relation ne développe aucune preuve et ne valide pas l'inférence.
- Le traitement de l'Event 214 montre la précision d'adaptateur encore nécessaire pour sélectionner les éléments pertinents d'un contenant, sans corriger sa source.

Ces compléments permettent de planifier L1/L2 après décision, sans architecture concurrente. Ils ne constituent pas une autorisation de les implémenter. Le fonctionnement réel restera à vérifier par les tests isolés spécifiés.

**C SUFFISANTE SOUS CONDITIONS — ADAPTATIONS MINIMALES À APPROUVER**
