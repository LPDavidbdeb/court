# Agent B — Addendum de conception du pont probatoire après la Note 02

Date : 19 octobre 2026. Statut : **proposition soumise à décision, sans autorisation d'implémentation**.

Ce document produit les neuf livrables demandés dans le mandat « Agent B — Production des neuf livrables de conception du pont probatoire ». Il conserve le plan antérieur et les documents de l'Agent A. Les architectures A/B/C de cet addendum concernent la représentation des utilisations; elles ne sont pas les anciennes options « preuve obligatoire / élément direct ».

**Recommandation : C, avec une utilisation explicite par preuve et par cible rédactionnelle, des sélections multiples et des supports projetés dans l'éditeur.** Les regroupements peuvent recevoir des utilisations. Le stockage de nœuds SUPPORT physiques demeure une option supplémentaire à approuver. La sélection, la composition affichée et l'insertion rédactionnelle ont des identités distinctes.

## 0. Périmètre, preuves de lecture et différences proposées

### 0.1 Sources et portée de la vérification

Lectures statiques sur la branche **epic/E01-numerotation-concordance**, commit **14f7533**. L'arbre de travail était propre au début de l'étude. Aucun serveur, shell Django, accès à la base, migration, test applicatif, répétition P6, fusion, commit ou push n'a été exécuté. Seul cet addendum est rédigé.

Sources de conception :

- [CONCEPTION_PREUVE.md](CONCEPTION_PREUVE.md), notamment §§ 1, 3, 4, 7 et 17.
- [ARCHITECTURE_CAUSES.md](ARCHITECTURE_CAUSES.md), notamment §§ 2–4.
- [PLAN_REGIME_CITATIONS.md](PLAN_REGIME_CITATIONS.md), contrat de l'étape 2 et état documenté au § 10.4.
- [PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md) et [méthodologie approuvée](../../legal/METHODOLOGIE_POST_DEPOT.md).
- Note consolidée du 19 octobre, fournie dans /Users/Louis-Philippe/Downloads/NOTE_02_OBSERVATIONS_EXEMPLE_CITATION_COMPOSITE.md. SHA-256 : 03ed46068ef67cdeb86c1839e35ee8d32c4beda1474d807bb3ddb914f7cda44a.
- Mandat joint, attachment 4d87f97d-f556-4e8a-9f55-c6ba8df014e0/Pasted text.txt. SHA-256 : 7f7a2a5a4ef96ffc2b41a39fa8d33dedb734315926a705fc0ac8b4e291c22f69.

Le fichier nommé PLAN_AGENT_B_PONT_PROBATOIRE.md n'a pas été retrouvé dans le dépôt ni dans la recherche par nom sous Downloads. La comparaison avec le plan initial repose sur la proposition antérieure de cette conversation et sa restitution au § 6.1 de la Note 02. Aucun fichier original n'est remplacé.

Les identités N.*, S.*, UP.*, PR.* ci-dessous sont des **identifiants de conception**, pas des PK inventées. Les dates, qualifications et extraits des exemples sont des entrées de conception communiquées, sans vérification contre les originaux. L'étude ne réévalue pas la thèse juridique.

### 0.2 Exigences confirmées, invariants et choix proposés

| Catégorie | Contenu |
|---|---|
| Fonctionnel confirmé | Organiser la rédaction récursive; utiliser une ou plusieurs preuves, entièrement ou partiellement; réutiliser les sources; restituer les passages; calculer un bordereau commun depuis les usages; conserver les versions communiquées. |
| Invariants | Source documentaire stable par modèle qualifié + PK; occurrence source explicite; aucune mutation d'une version gelée; aucune certification supposée; aucune justification déduite automatiquement des descendants; même résultat de résolution pour références, bordereau et livrables. |
| Proposition nouvelle | Profil de rédaction récursive, rôles indépendants de la profondeur, utilisations attachables aux groupes, compteur commun aux paragraphes principaux, composition multi-passages. |
| Choix à approuver | Architecture C; preuve obligatoire même atomique; cardinalités; présence physique des supports; sous-cotation des paragraphes; politique de cotation par version; mesures du premier gel réel. |

### 0.3 Différences avec la proposition antérieure

| Proposition antérieure | Révision proposée | Motif |
|---|---|---|
| 0..1 Demonstration par occurrence de paragraphe | 0..N UtilisationPreuve par occurrence STATEMENT ou REGROUPEMENT; une preuve par utilisation | Deux appuis distincts et appuis de groupe sans démonstration partagée ambiguë. |
| Demonstration contient des Poignee | UtilisationPreuve contient des SelectionPreuve | Conserver les responsabilités utiles; retirer l'enveloppe sans fonction supplémentaire démontrée. |
| Structure rédactionnelle peu spécifiée | Typage et présentation explicites des LibraryNode, récursion indépendante de la profondeur | U1 contient des paragraphes à D=4, D=6 et D=7. |
| InsertionRendu orientée vers un passage | CompositionCitation + segments ordonnés + insertions indépendantes | Neuf paragraphes non contigus; répétition d'une citation sans duplication documentaire. |
| Appui collectif surtout traité comme plusieurs feuilles | Appui explicite à une conclusion ou à un groupe, avec portée déclarée | Une union technique ne décrit pas l'intention de l'auteur. |
| Bordereau gelé en tables séparées envisagées | Un contenu gelé canonique contenant aussi le bordereau; index éventuels dérivés | Éviter deux autorités concurrentes pour les cotes historiques. |
| DAG ou copie minimale du chemin possibles à terme | Arbres simples et copie entière des arbres modifiés | Les nouveaux cas n'imposent toujours pas de renvoi récursif interne. |

## 1. Livrable 1 — Reconstruction de U1 et U2

### 1.1 Conventions et catalogue documentaire

Chaque N.* désigne une occurrence LibraryNode. Un N.* de type STATEMENT porte un S.* par la relation de contenu existante. Un regroupement porte un titre facultatif mais aucun Statement implicite. UP.* est une utilisation rattachée à un N.*; SEL.* sélectionne des nœuds d'un PR.*. Les supports affichés dans les arbres ci-dessous sont la projection de ces UP.*, sauf décision contraire.

| Alias documentaire | Source à résoudre avant emploi réel | Unité documentaire / fragment |
|---|---|---|
| DOC.NOV15 | Acte du 19 novembre 2015; document 1 selon la documentation du projet, sans contrôle en base dans cette étude | Document / occurrence LibraryNode source vérifiée |
| EMAIL.JUIN13 | Courriel du 11 juin 2013 | Email / Quote PHRASE future, ou Email entier pour une observation d'absence |
| EMAIL.JUIN30 | Communication du 30 juin 2013 | Source exacte et PHRASE à identifier |
| PROJET.AOUT15 | Projet du 13 août 2015 | Type réel à confirmer; aucune assimilation automatique à un Document plutôt qu'un PDF |
| COMM.JAN16 | Communication du 11 janvier 2016 | Source exacte et passages à identifier |
| COMM.SEPT16 | Échange du 16 septembre 2016 | Messages individuels à distinguer; une citation renvoie à son message précis |
| OFFRE.AVR20 / LETTRE.AVR27 | Proposition du 20 avril et lettre du 27 avril 2015 | Sources et passages à identifier |
| OFFRE.SEPT02 | Proposition du 2 septembre 2015 | Une identité de passage commune aux deux insertions de U2 |
| PARENT.* | Courriels, événements, photos et autres éléments des routines invoquées | Chaque élément et contenant explicites; aucune source créée pour combler un manque |

Le numéro imprimé « 14 » ne suffit pas à résoudre une occurrence : il peut être répété. L'adaptateur doit recevoir sa PK réelle après identification dans le bon Document. Un Statement seul, une date seule ou le premier résultat d'une requête ne conviennent pas.

### 1.2 Arbre rédactionnel complet au niveau des segments communiqués

Les plages R01..R24 désignent **chacune** un LibraryNode et un Statement distincts. Elles abrègent le dessin, pas le nombre d'occurrences. Les rattachements de sources proposés sont détaillés ensuite.

~~~text
N.DOC                                  REGROUPEMENT, racine D=1
├─ N.U1                                REGROUPEMENT, UNITE_CONTESTATION D=2
│  ├─ N.U1.OBS                         REGROUPEMENT, OBSERVATION D=3
│  │  ├─ N.U1.O1 → S.U1.O1             STATEMENT, PARAGRAPHE D=4
│  │  │    ↳ UP.U1.O1.NOV → PR.NOV / neuf occurrences
│  │  ├─ N.U1.O2 → S.U1.O2             STATEMENT, PARAGRAPHE D=4
│  │  │    ↳ UP.U1.O2.NOV → PR.NOV / sélection collective explicite
│  │  └─ N.U1.O3 → S.U1.O3             STATEMENT, PARAGRAPHE D=4
│  │       ↳ UP.U1.O3.NOV → PR.NOV / passages caractérisés, à arrêter
│  └─ N.U1.REF                         REGROUPEMENT, REFUTATION D=3
│     ├─ N.U1.A                        REGROUPEMENT D=4; texte non reçu
│     │                                aucun Statement, aucune preuve inventée
│     ├─ N.U1.B                        REGROUPEMENT D=4
│     │  ├─ N.U1.B1                    REGROUPEMENT D=5
│     │  │  ├─ .OBJECTIF               REGROUPEMENT D=6 → R01..R03 D=7
│     │  │  ├─ .PLAN                   REGROUPEMENT D=6 → R04..R05 D=7
│     │  │  ├─ .THESE_SILENCE          REGROUPEMENT D=6 → R06..R10 D=7
│     │  │  ├─ .MOTIF                  REGROUPEMENT D=6 → R11..R13 D=7
│     │  │  ├─ .ROTATION               REGROUPEMENT D=6 → R14..R17 D=7
│     │  │  ├─ .CONTRADICTION          REGROUPEMENT D=6 → R18..R20 D=7
│     │  │  └─ .OFFRE_AOUT             REGROUPEMENT D=6 → R21..R24 D=7
│     │  └─ N.U1.B2                    REGROUPEMENT D=5
│     │     ├─ .GRIEF                  REGROUPEMENT D=6 → R01..R09 D=7
│     │     │    R08 : sous-item a) non fourni; aucune citation suppléée
│     │     └─ .REMEDE                 REGROUPEMENT D=6 → R10..R13 D=7
│     └─ N.U1.C                        REGROUPEMENT D=4
│        ├─ .TEMPS                     REGROUPEMENT D=5 → R01..R08 D=6
│        ├─ .ROLES                     REGROUPEMENT D=5 → R09..R13 D=6
│        └─ .CONFIRMATION              REGROUPEMENT D=5 → R14..R16 D=6
└─ N.U2                                REGROUPEMENT, UNITE_CONTESTATION D=2
   ├─ N.U2.OBS                         REGROUPEMENT, OBSERVATION D=3
   │    ↳ UP.U2.OBS.NOV → PR.NOV / §§ 14..17
   │    aucun dixième paragraphe ajouté aux neuf communiqués
   └─ N.U2.REF                         REGROUPEMENT, REFUTATION D=3
      ├─ N.U2.MOMENT                   REGROUPEMENT D=4 → R01..R07 D=5
      └─ N.U2.MOTIF                    REGROUPEMENT D=4 → R08..R09 D=5
~~~

Exemple d'identité développée : N.U1.B1.R20 porte S.U1.B1.R20; il est enfant de N.U1.B1.CONTRADICTION. UP.U1.B1.R20.COMPARE est une relation distincte de ce contenu et du PR.* qu'elle utilise. Un déplacement du paragraphe conserve son identité; sa copie dans une autre VersionActe reçoit un nouveau N.* avec correspondance explicite.

L'observation composée est N.U1.OBS avec ses trois énoncés. N.U1 est l'unité qui réunit observation et réfutation. La note ne fournit pas le texte intégral de chaque R.* : le rapport reconstruit exactement leurs emplacements et identités, **pas une transcription prétendument complète de leurs contenus**. Le texte ancien de [25_presentation_argument_complet.md](../../legal/redaction_v2/25_presentation_argument_complet.md) n'est pas utilisé pour remplir la branche A absente des nouveaux exemples.

### 1.3 Arbres de preuve et sélections

~~~text
PR.NOV
└─ PN.NOV.ROOT                         GROUPE
   ├─ PN.NOV.4..7                      quatre ELEMENT → occurrences source 4,5,6,7
   └─ PN.NOV.14..18                    cinq ELEMENT → occurrences source 14..18

PR.JUIN13
└─ PN.J13.ROOT                         GROUPE
   ├─ PN.J13.ENTIER                    ELEMENT → EMAIL.JUIN13 entier
   ├─ PN.J13.OBJECTIF                  GROUPE → PHRASE à identifier
   └─ PN.J13.PLAN                      GROUPE → PHRASE à identifier

PR.COMPARAISON
└─ PN.COMP.ROOT                        GROUPE
   ├─ PN.COMP.J13                      ELEMENT(S) → passages de juin 2013
   └─ PN.COMP.NOV                      ELEMENT(S) → occurrences de novembre 2015

PR.NEGOCIATIONS / PR.COMM2016 / PR.PARENTAL
└─ groupes et feuilles documentaires explicitement identifiés
   une feuille par élément utilisé; aucun renvoi interne à un autre PR.*
~~~

Les feuilles de PR.COMPARAISON peuvent référencer les mêmes objets source que PR.NOV et PR.JUIN13. Ce sont de nouvelles **occurrences d'organisation**, sans copie des sources et sans DAG. Une autre possibilité, retenue dans le schéma minimal, consiste à attacher deux UP.* à la même conclusion plutôt qu'à créer PR.COMPARAISON.

| Cible rédactionnelle | Utilisations proposées et sélections | Statut / limite |
|---|---|---|
| U1.O1 | PR.NOV : les neuf feuilles; une composition d'affichage de neuf passages | Décrit existence/contenu de la déclaration. |
| U1.O2 | PR.NOV : sélection explicitement décidée des passages thématiques | Pas d'héritage automatique depuis O1. |
| U1.O3 | PR.NOV : passages invoqués pour le fondement commun | Portée interprétative rédigée; sélection à confirmer. |
| B1.R01..R05 | Passages de EMAIL.JUIN13; communication de septembre selon le paragraphe réellement concerné | La note donne des segments; les rattachements phrase par phrase restent à confirmer sur les textes. |
| B1.R08 | PR.JUIN13 : PN.J13.ENTIER | Usage ABSENCE_DOCUMENTAIRE; référence au courriel entier, sans prétendre prouver automatiquement l'absence. |
| B1.R06..R10, hors R08 | Passages de DOC.NOV15 et de EMAIL.JUIN13 selon les propositions | Aucune ventilation inventée des passages non fournis. |
| B1.R11..R13 | Passages de EMAIL.JUIN30 | Identités et certification à obtenir. |
| B1.R14..R20 | Deux UP.* explicites vers les sélections de juin/novembre; possibilité d'appui à .CONTRADICTION | Comparaison attribuée à l'auteur. |
| B1.R21..R24 | PROJET.AOUT15, passages des modalités invoquées | Type source et passages à confirmer. |
| B2.R01..R09 | COMM.JAN16, COMM.SEPT16 et sources d'audience effectivement identifiées | « contre les protestations » n'est pas confirmé par la seule citation; R08.a reste manquant. |
| B2.R10..R13 | OFFRE.AVR20, LETTRE.AVR27, PROJET.AOUT15, propositions réellement invoquées | Sélections explicites, sans importer tout le corpus des négociations. |
| C.R02..R08 | Aucun UP.* obligatoire | Cadre analytique; pas de fausse pièce ni de fausse certification. |
| C.R09..R13 | Sélections propres aux responsabilités alléguées, notamment C.R11 | Les fréquences précises restent à étayer; aucune source fictive. |
| C.R14..R16 | UP.* distincts sur les messages pertinents de COMM.SEPT16 | Même pièce/fragment que B2 quand l'identité est réellement la même; fonctions d'utilisation distinctes. |
| U2.OBS | PR.NOV : quatre feuilles des §§ 14..17 | Support attaché au groupe, portée « objet documentaire contesté ». |
| U2.R01..R07 | DOC.NOV15, OFFRE.AVR20, LETTRE.AVR27, OFFRE.SEPT02 selon le texte de chacun | U2.R05 et U2.R07 affichent le même passage de septembre, via deux insertions. |
| U2.R08..R09 | Sélections des motifs dans DOC.NOV15 et LETTRE.AVR27 | Le système conserve la confrontation, sans conclure à une incompatibilité logique. |

Une case « à confirmer » est une donnée manquante, pas une autorisation de sélectionner arbitrairement toute une preuve. Les corpus utilisables et leurs parcours sont identifiés; le gel réel attendra la résolution des sources, du texte absent et des certifications requises.

## 2. Livrable 2 — Comparaison A / B / C et schéma concret

### 2.1 Socle commun aux trois variantes

Les variantes partagent : Acte/VersionActe, Document/LibraryNode/Statement, Preuve/NoeudPreuve, les adaptateurs documentaires, les compositions/insertions et le contenu gelé. Aucune ne dépend en exécution de case_manager ou argument_manager.

| Variante | Modèles propres et cardinalités | Sélection et autorité | Coût et gel |
|---|---|---|---|
| A | Demonstration : version FK, cible LibraryNode FK, portée; au plus une par cible. Poignee : démonstration FK, NoeudPreuve FK, rang, portée. 0..1 démonstration par cible; 1..N poignées par démonstration valide; plusieurs preuves possibles. | La démonstration possède l'utilisation; chaque poignée sélectionne un sous-arbre. Extension aux cibles REGROUPEMENT indispensable. SUPPORT peut être une projection. | Bonne continuité avec l'ancien plan. Deux poignées vers une même preuve peuvent être deux sélections ou deux usages : convention à fixer. Copie des démonstrations/poignées par version. Un SUPPORT persistant crée une contrainte de synchronisation supplémentaire. |
| B | LibraryNode de type SUPPORT obligatoire, enfant direct de la cible. SupportNoeud : OneToOne vers ce nœud, preuve FK, portée. SelectionSupport : FK SupportNoeud + FK NoeudPreuve + rang. 0..N enfants SUPPORT par cible; une preuve par support; 1..N sélections. | L'occurrence SUPPORT, ses métadonnées OneToOne et ses sélections constituent ensemble l'utilisation. La cible est son parent réel, non un deuxième champ libre. | Utilisation visible dans l'arbre, mais tout déplacement, suppression, copie Treebeard et filtrage devient opération probatoire. Le gel doit protéger l'arbre documentaire et les tables de sélection conjointement. Le support ne se réduit pas à une GFK vers Preuve. |
| C | UtilisationPreuve : version FK, cible LibraryNode FK, preuve FK, portée, rang. SelectionPreuve : FK utilisation + FK NoeudPreuve + rang. 0..N usages par cible; une preuve par usage; 1..N sélections. SUPPORT projeté par défaut; lien physique facultatif unique. | UtilisationPreuve est la seule autorité du rattachement et des sélections. Les insertions y renvoient. L'éditeur peut présenter chaque usage comme un enfant technique sans le stocker dans LibraryNode. | Même coût de sélection que B, mais l'arbre reste déplaçable sans recréer les usages. La copie versionnelle copie les usages; la preuve est partagée puis copiée entièrement si modifiée. Un nœud physique facultatif ajoute un contrôle, sans ajouter une seconde autorité. |

Dans A, imposer un champ « preuve » sur Demonstration changerait son sens en une utilisation par preuve et rapprocherait A de C. Dans B, une table SupportNoeud n'est pas un doublon si elle ne fait que porter les champs d'un SUPPORT obligatoire; elle le devient si une seconde table d'utilisation conserve les mêmes sélections. Le nombre de tables ne suffit donc pas à départager les variantes.

**Choix recommandé : C avec supports projetés.** Il satisfait les opérations demandées et conserve l'indépendance des rives. Si l'enregistrement physique des supports devient une exigence, C peut l'accueillir; B reste possible si l'on accepte que leur identité et leur cible dépendent de leur place matérielle dans l'arbre.

### 2.2 Modèles proposés pour C

Sauf mention contraire : PK technique stable; FK en PROTECT pour les références probatoires et historiques. La suppression d'un brouillon passe par un service qui retire ses dépendances dans un ordre explicite. Les noms de champs ci-dessous constituent une spécification, pas du code existant.

| Modèle / emplacement | Champs et relations essentiels | Contraintes, édition et identité |
|---|---|---|
| Cause, existant | Numéro, métadonnées et historique existants | Réutilisation sans nouvelle table de cause. Origine d'une source distincte de la cause de son utilisation. |
| Acte, couche neutre act_manager proposée | cause FK; nature; titre; créé_le | Identité durable; pas de FK vers proof_manager. |
| VersionActe, act_manager | acte FK; numéro; document OneToOne; issue_de FK nullable; état BROUILLON/GELEE; revision; profil et versions d'algorithmes; gelée_le | Unique(acte, numéro); une version possède son document de rédaction. Égalité cause de l'acte / origine du document produit vérifiée, sans l'imposer aux sources adverses. |
| Document, extension neutre | profil_structure, défaut LEGACY; verrouille_le nullable | Aucun reclassement des documents existants. Le verrou local protège texte/structure sans importer le pont; ReferentHistorique reste indépendant. |
| LibraryNode, extension neutre | nature_structurelle LEGACY/REGROUPEMENT/STATEMENT/SUPPORT; role_editorial; presentation TRANSPARENT/TITRE/PARAGRAPHE/SOUS_ITEM/TECHNIQUE | Profil récursif : STATEMENT vise un Statement; regroupement sans contenu; SUPPORT sans contenu, technique, feuille. Nature, rôle et présentation ne se déduisent pas de depth. |
| Statement / VersionTexte, existants à protéger | Contenu et version textuelle existants | Édition d'un contenu partagé par détachement; VersionTexte devient append-only dans le contrat neutre proposé. Pas de confirmation héritée automatiquement d'un ancien texte. |
| Preuve, proof_manager | titre facultatif; issue_de FK nullable; revision; verrouillee_le nullable | Une racine; arbre réutilisable. Tout arbre engagé dans un gel est verrouillé entier. |
| NoeudPreuve, proof_manager, MP_Node | preuve FK; nature GROUPE/ELEMENT/CONTEXTE; libellé/rôle/note facultatifs; element_type FK ContentType PROTECT + element_id; contenant_type/id facultatifs | Chemin Treebeard pour parent et ordre, sans deuxième champ parent. ELEMENT : cible autorisée existante. CONTEXTE : note interne non cotable, jamais un verbatim probatoire. Groupes seuls parents; aucun renvoi récursif. |
| UtilisationPreuve, proof_manager | version FK; cible FK LibraryNode; preuve FK; rang; portée facultative; objet_usage DOCUMENTAIRE/COMPARAISON/ABSENCE_DOCUMENTAIRE; noeud_support FK unique nullable | Cible dans le document de la version, de type STATEMENT ou REGROUPEMENT. Unique(version, cible, rang). Plusieurs usages de la même preuve possibles avec portées distinctes. |
| SelectionPreuve, proof_manager | utilisation FK; noeud_preuve FK; rang | Unique(utilisation, noeud_preuve) et Unique(utilisation, rang); nœud dans la preuve de l'utilisation. Racine, groupe ou feuille autorisés. |
| CompositionCitation, proof_manager | version FK; format SIMPLE/BLOC_DOCUMENTAIRE/REFERENCES; politique_ordre SOURCE/EXPLICITE | Objet d'affichage indépendant de son nombre d'insertions; aucune cote ni copie manuelle du verbatim. |
| SegmentCitation, proof_manager | composition FK; rang; element_type/id; contenant_type/id si nécessaire; emphases structurées avec empreinte du texte ciblé | Unique(composition, rang). Texte lu par adaptateur. Les omissions entre passages se calculent depuis la structure source; pas de faux texte source dans un champ libre. |
| InsertionRendu, proof_manager | version FK; cible STATEMENT FK LibraryNode; version_texte FK VersionTexte; start/end; ordre_local; composition FK nullable; mode; utilisations M2M | start=end pour insertion, start<end pour remplacement; bornes Python du texte rédactionnel. Une composition obligatoire si l'affichage choisit des passages; références de tous les usages possibles sans composition. |
| CertificationPassageActe, proof_manager | occurrence_source FK LibraryNode; texte_sha256; numero_source; structure_sha256; fichier_source_sha256; localisation_scan; vérificateur; vérifié_le | Enregistrement append-only de conformité d'un passage reproduit. Ne certifie pas la vérité de l'allégation. Aucune assimilation à Quote PHRASE. |
| ContenuVersionFige, act_manager | version OneToOne; schema_version; document JSON; usages_et_preuves JSON; rendu JSON; bordereau JSON; manifeste JSON; empreinte globale; créé_le | Un seul contenu canonique par version; tous ses composants sont immuables et leur schéma est validé. La couche neutre conserve des valeurs sérialisées, sans FK vers les modèles du pont. |
| LivrableVersion, act_manager | contenu_fige FK; nature; URI immuable; taille; SHA-256; profil de génération | Livrables en ajout seul; fichiers jamais remplacés sous la même URI. Échec du stockage : pas de gel déclaré terminé. |
| Transmission, act_manager | contenu_fige FK; date; destinataire/canal; livrables transmis; preuve de remise | Ajout seul; une nouvelle transmission ne modifie pas le contenu. Ce modèle ne réalise aucun envoi dans cette étude. |
| CorrespondanceHistorique, proof_manager | bordereaux source/cible identifiés par version et empreinte; entrées/identités concernées; relation EGALITE/CONTIENT/EQUIVALENCE_VALIDEE; justification; validateur/date | Pour les exceptions et transformations d'unité. L'égalité exacte par identité se calcule sans ligne supplémentaire. Relations 1:N et N:1 possibles, sans fusion automatique des sources. |

Le bordereau gelé est un composant typé de ContenuVersionFige, et **non une deuxième table autonome faisant autorité**. Chaque entrée y porte pièce/fragment/composant historique, identité qualifiée, parent éventuel, cote, rang, date et provenance, ancrage, libellés et chemins d'utilisation. Des index SQL dérivés pourront être ajoutés pour la recherche, avec l'empreinte du contenu dont ils proviennent.

### 2.3 Contraintes locales et contraintes relationnelles

| Niveau | Garanties à porter |
|---|---|
| Contraintes SQL locales | Unicités de rang et d'identité; FK PROTECT; paires type/id complètes ou vides; bornes non négatives et start<=end; cohérence nature/contenu du nouveau profil. |
| Services transactionnels | Cible/document/version cohérents; sélection dans la bonne preuve; portée d'insertion compatible; détachement avant édition partagée; copie et remappage cohérents. |
| Contrôles relationnels en base avant usage réel | Gardes de gel sur INSERT/UPDATE/DELETE; contrôles différés de cible/version, parent des supports physiques éventuels et appartenance des sélections. Ils couvrent aussi les opérations de masse et les changements du parent ou du document référencé. |
| Lecture stricte | Existence des cibles génériques; classe autorisée; certification effective; empreintes, dates et positions; cohérence du manifeste. Un contrôle d'écriture ne dispense pas de vérifier à la lecture. |

Une CheckConstraint ne peut pas, à elle seule, vérifier qu'une sélection appartient à la preuve de son utilisation. Les signaux save/pre_save existants ne protègent pas QuerySet.update ou tous les déplacements Treebeard. Le premier gel réel exige donc les gardes relationnelles et d'immutabilité, avec leurs tests de contournement. La conception ne les présente pas comme déjà disponibles.

La cohérence locale nature/contenu vérifie la présence ou l'absence des champs génériques; vérifier que le ContentType correspond réellement à Statement relève du registre de types et des contrôles relationnels. Les champs existants Statement.is_true/is_falsifiable ne fournissent aucune validation au nouveau pont : leur valeur ne décide ni l'admissibilité d'un support ni la vérité d'une conclusion.

### 2.4 Conséquences de migration, uniquement proposées

1. Ajouter les métadonnées neutres avec défaut LEGACY et verrou non posé; vérifier que les sorties existantes restent identiques.
2. Créer les nouvelles applications/tables après arbitrage; aucune conversion automatique de TrameNarrative ou ConfirmationAppui.
3. Activer le profil récursif seulement sur un Document de travail explicitement choisi ou neuf.
4. Reprendre les textes et rattachements par correspondance d'occurrences contrôlée; ne pas déduire les nouvelles sélections des anciennes cotes en prose.
5. Réaliser séparément l'import historique de juillet, après contrôle du verrou; ne pas renuméroter le doc 9.

Le passage ultérieur de A à C est possible en regroupant les poignées d'une démonstration par preuve et portée, mais ne serait pas une simple opération de renommage : identité des usages, insertions et instantanés seraient à remapper. Choisir avant de créer les tables évite ce coût.

## 3. Livrable 3 — Structure et numérotation démontrées

### 3.1 Constats sur la branche lue

| Constat vérifié | Référence | Conséquence |
|---|---|---|
| LibraryNode est MP_Node, avec document, GFK de contenu, item, paragraph_number et is_evidence | [models.py](../../document_manager/models.py), lignes 176–226 | Occurrence réutilisable; aucun type fonctionnel par nœud aujourd'hui. |
| Niveau est unique par schéma et profondeur | même fichier, lignes 308–327 | Deux frères de rôles éditoriaux distincts ne peuvent pas être distingués par le seul Niveau. |
| numeroter saute racine et nœuds sans content_type; le rôle vient de niveaux[depth] | [numerotation.py](../../document_manager/numerotation.py), lignes 161–190 | Un groupe transparent n'est pas un paragraphe; un SUPPORT avec GFK ne sera pas automatiquement ignoré. |
| Les compteurs DOCUMENT sont indexés par profondeur | même fichier, lignes 199–209 | D=4 puis D=7 ne partagent pas un compteur, même si les deux niveaux sont PARAGRAPHE. |
| Le régime sans schéma dépend de D=2,3,4; les niveaux suivants sont libres | même fichier, lignes 136–158 | Le repli actuel ne satisfait pas le nouveau profil. |
| resoudre distingue AUTO/STORED, conserve les numéros lus, signale ceux manquants | même fichier, lignes 276–307 | Conserver ce contrat pour les sources et le dépôt; pas de recalcul historique. |
| La vue clean filtre is_evidence avant de construire son arbre; sa table de types est explicite | [produced_views.py](../../document_manager/views/produced_views.py), lignes 18–106 et 199–205 | SUPPORT inconnu peut disparaître; ses insertions ne doivent pas disparaître avec lui. Le nouveau rendu doit composer avant de masquer les nœuds techniques. |
| Les vues produites importent les anciennes trames et chargent Quote.objects | même fichier, lignes 12–16 et 35–64 | Pas de branchement direct du nouveau pont dans ces consommateurs hérités. |
| schema_views enrichit les cotes présentes dans le texte, via case_manager | [schema_views.py](../../document_manager/views/schema_views.py), lignes 25–93 | Ne fournit pas les nouvelles références dynamiques; risque de traiter un P-2 historique comme une référence active si les deux flux sont mélangés. |

La profondeur variable est possible dans le stockage actuel; sa capacité physique reste celle du chemin Treebeard. Aucun maximum métier fixe à D=5 n'est proposé; les limites de stockage doivent être diagnostiquées, jamais masquées.

### 3.2 Trois dimensions explicites

| Dimension | Exemple sur U1 | Effet |
|---|---|---|
| Nature structurelle | N.U1.REF=REGROUPEMENT; N.U1.B1.R20=STATEMENT | Validation du contenu et des enfants autorisés. |
| Rôle éditorial | REFUTATION, OBSERVATION, CONCLUSION, CADRE_ANALYTIQUE ou autre valeur déclarée | Navigation et contrôles éditoriaux; aucun calcul de vérité ou de certification. |
| Présentation | TITRE, PARAGRAPHE, SOUS_ITEM, TRANSPARENT, TECHNIQUE | Impression et compteurs. Un STATEMENT analytique peut être PARAGRAPHE sans support. |

Un regroupement portant un chapeau rédigé contient un enfant STATEMENT : le titre du groupe ne devient pas silencieusement une proposition. Le profil récursif utilise ces dimensions; les documents LEGACY continuent d'utiliser SchemaNiveaux. Il faut un seul résolveur public, avec stratégie explicite par profil, et pas un compteur différent dans chaque vue.

### 3.3 Algorithme de présentation du profil récursif

1. Lire le document entier en ordre de chemin, sans filtrer les supports ou les sections.
2. Valider types et relations. Fixer un compteur de paragraphes principaux unique au document.
3. Pour PARAGRAPHE, incrémenter ce compteur, quelle que soit la profondeur.
4. Pour SOUS_ITEM, utiliser un compteur propre au paragraphe principal propriétaire, retrouvé explicitement par son ascendance rédactionnelle; le sous-item reçoit par exemple 2.a pour l'index et a) à l'impression. Refuser un sous-item sans paragraphe propriétaire.
5. TITRE possède une série de titres distincte, si le profil en demande une. TRANSPARENT et TECHNIQUE n'incrémentent aucun compteur.
6. Construire l'index complet occurrence → numéro/présentation. Composer les citations, puis appliquer les filtres d'affichage.
7. Sur une version gelée, lire l'index gelé. Sur un document source STORED, lire paragraph_number selon le résolveur historique et refuser un numéro requis mais absent.

Un déplacement change le rang imprimé d'un brouillon, pas l'identité de l'occurrence ni ses usages. Un filtre de lecture ne change jamais les rangs.

### 3.4 Correspondance de numérotation des deux unités

| Occurrences principales | Profondeur | Numéros imprimés proposés |
|---|---:|---|
| U1.O1, O2, O3 | 4 | 1, 2, 3 |
| U1.B1.R01..R24 | 7 | 4..27 |
| U1.B2.R01..R13 | 7 | 28..40 |
| U1.C.R01..R16 | 6 | 41..56 |
| U2.R01..R09 | 5 | 57..65 |
| A non reçu, groupes, supports, citations insérées | variables | Aucun numéro de paragraphe principal |

Contrôles de raccord : B1.R20=23; B2.R08=35; C.R16=56; U2.R05=61; U2.R07=63. La note fournit 3+24+13+16+9=65 paragraphes principaux. Le sous-item manquant de B2.R08 n'en ajoute aucun. Des sous-items de O2 peuvent détailler ses trois thèmes sans changer le compteur principal.

### 3.5 Exemple effectivement présenté et numéroté dans cet addendum

Rendu de référence de conception, constitué d'un **extrait** de ces paragraphes. Les ellipses entre paragraphes rédactionnels signalent les paragraphes non reproduits dans cet extrait; elles ne sont pas un nouveau contenu d'acte. Ce rendu est écrit ici, sans exécution d'un renderer applicatif ni validation des citations.

~~~text
UNITÉ 1 — Observation contestée

1. Le 19 novembre 2015, la défenderesse Élise Ayoub a affirmé
   solennellement ce qui suit :

   4. La continuation de la vie commune étant devenue impossible,
      le défendeur a quitté la résidence commune le 23 février 2015
      pour se loger dans un appartement à proximité;
   5. En effet, depuis la naissance d'Alexia, la relation entre les
      parties était très difficile;
   6. En effet, le défendeur ne s'impliquait que minimalement dans
      les soins d'Alexia, laissant toute la responsabilité à la
      demanderesse, ce qui causait de grandes frictions dans le couple;
   7. En 2011, suite à une infidélité du défendeur, les parties ont
      vécu séparées pendant un (1) an et ont été en thérapie. A ce
      moment il est ressorti que le défendeur avait de la difficulté
      à assumer son rôle de père et s'investir;

   [Paragraphes 8 à 13 non reproduits — indication éditoriale.]

   14. Dès la rupture, le défendeur voulait instaurer une garde
       partagée, que la demanderesse a refusé puisque contraire
       à l'intérêt des enfants;
   15. En effet, les enfants sont jeunes et de plus, le défendeur
       était rarement disponible pour prendre soins d'eux;
   16. C'est la demanderesse qui s'occupait des enfants, qui allait
       aux activités, etc......;
   17. Le défendeur aidait lorsque la demanderesse n'était pas disponible;
   18. Les parties ont donc convenu que la demanderesse aurait la garde
       des enfants, le tout tel qu'il appert des échanges des messages
       textes datés du 21 avril 2015, produits en liasse au soutien
       des présentes sous la pièce P-2.

   [Référence active au document source et à ses passages :
    à résoudre dans le bordereau de la version.]

2. Ensemble, ces neuf paragraphes expliquent :
   a) la séparation des parties;
   b) le refus de la garde partagée;
   c) l'entente alléguée sur le régime de garde.

3. Le tout repose sur l'implication minimale historique du demandeur
   dans les soins des enfants, sur sa difficulté à assumer son rôle
   de père et sur son indisponibilité.

Réfutation — B1 — La contradiction
[Paragraphes rédactionnels 4 à 22 non reproduits dans cet extrait.]

23. On ne crée pas ce qui existe déjà.

[Paragraphes rédactionnels 24 à 55 non reproduits dans cet extrait.]

Réfutation — C — Confirmation du rôle
56. [Texte de C.R16; citation du message de septembre composée ici.]

UNITÉ 2 — Réfutation
57. [Texte communiqué de U2.R01.]
[Paragraphes rédactionnels 58 à 60 non reproduits dans cet extrait.]
61. [Texte de U2.R05; première insertion du passage de septembre.]
62. [Texte de U2.R06.]
63. [Texte de U2.R07; deuxième insertion du même passage.]
64. [Texte de U2.R08.]
65. [Texte de U2.R09.]
~~~

Le texte des neuf passages ci-dessus est repris du matériau rédactionnel communiqué, également présent aux lignes 37–45 du fichier 25; les retours de ligne sont de présentation. Il n'est pas certifié par cette reprise. Les crochets ne remplacent pas des textes source manquants et ne seraient pas admis dans un livrable réel. Les numéros 4,5,…,18 à l'intérieur du bloc sont ceux du document historique; ils ne font pas avancer le compteur rédactionnel 1,2,3,… Le P-2 du § 18 demeure littéral.

## 4. Livrable 4 — Contrat d'utilisation d'une preuve

### 4.1 Sens précis et sélection

Une UtilisationPreuve signifie : **dans cette VersionActe, l'auteur rattache à cette occurrence rédactionnelle les éléments sélectionnés de cette preuve, selon cette portée**. Elle ne signifie ni démonstration valide, ni vérité, ni admission.

~~~text
VersionActe 1 ── N UtilisationPreuve N ── 1 Preuve
                        │
                        ├── 1 cible LibraryNode de sa version
                        └── 1..N SelectionPreuve ── 1 NoeudPreuve
~~~

- Sélectionner la racine mobilise toutes les feuilles de cette preuve.
- Sélectionner un groupe mobilise ses feuilles descendantes.
- Sélectionner plusieurs feuilles ou branches mobilise leur union.
- L'union déduplique les éléments pour le calcul documentaire et conserve tous les parcours utilisation/sélection/feuille pour la traçabilité.
- Des sélections chevauchantes, par exemple racine et feuille déjà descendante, ne doublent pas l'appui ni la cote. Un diagnostic de redondance peut les proposer à la simplification.
- Une utilisation valide a au moins une sélection contenant un élément documentaire. Le retrait de sa dernière sélection supprime l'utilisation dans la même transaction, ou laisse un brouillon explicitement invalide; il ne produit pas silencieusement un appui vide « valide ».
- La preuve atomique contient une racine et une feuille. Sa création peut être automatique, sans demander de données argumentatives supplémentaires.

L'objet CONTEXTE ne permet pas de contourner la certification en y copiant un extrait. Il est interne et non cotable. Un fait rédactionnel de contexte imprimé est un Statement; une source documentaire invoquée reste une feuille ELEMENT.

La création normale d'une feuille Quote du nouveau pont exige le régime PHRASE cible; une HERITE n'est pas admise sous prétexte qu'elle ne serait pas encore sélectionnée. Une PHRASE peut rester à certifier dans une preuve en préparation, mais tout usage sélectionné doit satisfaire la certification effective avant un rendu strict. Les gardes de lecture refusent aussi une HERITE introduite par contournement.

### 4.2 Appuis de groupe et conclusions collectives

**Recommandation : autoriser les deux cibles, groupe et Statement.**

1. Une conclusion rédigée reçoit ses propres utilisations. Deux UP.* vers deux preuves suffisent à déclarer une confrontation documentaire, sans arête logique entre propositions.
2. Un groupe peut recevoir un usage avec portée explicite, par exemple « objet documentaire contesté » pour U2.OBS ou « corpus comparé par cette section ». Cet usage alimente le bordereau, même si le groupe n'a pas de texte numéroté.
3. Les enfants ne reçoivent pas automatiquement ce support; ils peuvent le retrouver pour la navigation. Une référence insérée dans un enfant doit désigner explicitement cet usage de groupe.
4. Aucun usage vers un autre Statement n'est introduit comme substitut à la source : le raisonnement reste dans le texte. Les éventuelles références rédactionnelles entre paragraphes sont distinctes et ne génèrent pas de pièces.

L'ensemble des feuilles des usages de tous les groupes et Statements inclus dans la version constitue le périmètre du bordereau. Une simple collection de sources visibles en navigation ne constitue pas un usage.

### 4.3 Réutilisation et opérations autorisées

| Opération proposée | Contrat et résultat |
|---|---|
| ajouter_appui_atomique(version, cible, élément) | Résoudre/admettre l'élément, créer preuve + feuille + utilisation + sélection atomiquement; retourner leurs identités. |
| utiliser_preuve(version, cible, preuve, sélections) | Valider la cible, l'appartenance des sélections et la portée; créer une nouvelle utilisation, sans copier la source. |
| modifier_selection(utilisation, sélections, revision_attendue) | Brouillon uniquement; nouvelle révision de la version et invalidation du calcul/affichage antérieurs. |
| retirer_utilisation(utilisation) | Retirer aussi ou invalider ses liens d'insertion; ne supprimer ni preuve partagée ni source. |
| deplacer_occurrence(noeud, parent, rang) | Même document/version; conserver ses utilisations et insertions; recalculer les numéros. Déplacement inter-version refusé : effectuer une copie remappée. |
| modifier_preuve(preuve, perimetre_utilisations) | Si verrouillée ou partagée, copier l'arbre entier et repointer seulement le périmètre explicitement choisi. Aucune propagation implicite aux autres brouillons. |

Un support projeté est identifié par UP.pk dans l'éditeur, jamais par un faux PK de LibraryNode. Si les supports physiques sont approuvés, le lien unique UtilisationPreuve.noeud_support et l'égalité parent du support=cible sont vérifiés à la transaction. Un SUPPORT physique sans utilisation ou pointant vers une autre version est invalide.

## 5. Livrable 5 — Contrat du rendu documentaire

### 5.1 Trois objets et une règle de cohérence

| Objet | Question traitée | Exemple |
|---|---|---|
| UtilisationPreuve + SelectionPreuve | Quels éléments l'auteur mobilise-t-il? | Les neuf occurrences de DOC.NOV15 pour O1. |
| CompositionCitation + SegmentCitation | Quels passages sont affichés, dans quel ordre et sous quelle forme? | Un bloc avec les neuf paragraphes, leurs numéros historiques et une omission explicite. |
| InsertionRendu | À quel endroit du texte rédactionnel cet affichage intervient-il? | Après « ce qui suit : » de O1, ou à deux endroits différents de U2. |

Une insertion désigne explicitement les utilisations qui l'autorisent, toutes dans la même version. Il s'agit d'usages de sa cible ou d'un regroupement ancêtre explicitement choisi; une utilisation d'une section sans ce rapport ne peut être empruntée silencieusement. La composition peut être réutilisée par plusieurs insertions de la même version.

Chaque passage affiché doit correspondre, par identité documentaire et identité de fragment, à une feuille effectivement sélectionnée par ces usages. Une référence au document parent d'un fragment sélectionné est autorisée sans créer un nouvel usage. Utiliser un courriel entier pour une observation d'absence ne suffit pas à afficher une PHRASE arbitraire non sélectionnée : son ajout est explicite.

La composition peut afficher seulement certains appuis, par exemple « notamment ». Les autres appuis effectivement utilisés restent au bordereau. À l'inverse, un élément simplement présent ailleurs dans la preuve n'apparaît ni dans les références actives ni dans le bordereau.

### 5.2 Résolution et formes d'affichage

| Forme | Données requises | Règles |
|---|---|---|
| Citation simple de courriel/PDF | Quote PHRASE, source, bornes et certification effective | Lire le verbatim certifié; aucune restitution depuis une saisie manuelle du paragraphe. |
| Bloc documentaire composite | Liste de LibraryNode source du même Document, ordre SOURCE | Conserver les numéros, séparations et ordre source. Émettre une indication éditoriale pour les passages sautés. Ne pas concaténer comme un passage continu. |
| Composition comparative de plusieurs sources | Segments avec provenance propre, ordre EXPLICITE | Séparer et identifier chaque source; cet ordre d'affichage ne change pas l'ordre des sous-cotes. |
| Référence seule | Usages explicitement liés ou segments choisis | Résoudre cote documentaire et sous-cotes dans le résultat de cette version, sans lire une cote globale. |
| Même citation répétée | Une composition et plusieurs insertions, ou compositions équivalentes | Deux affichages, même identité de fragment et même sous-cote dans une version. |

Pour U1.O1 : la composition COMP.U1.NOV possède neuf segments référant aux occurrences 4,5,6,7,14,15,16,17,18. INS.U1.O1 la place après l'introduction. Pour U2 : COMP.SEPT02 contient le passage source commun; INS.U2.R05 et INS.U2.R07 le placent dans deux textes et versions textuelles distincts. L'identité de la composition ne détermine jamais la cote.

L'ordre SOURCE est obligatoire pour la reproduction d'un ensemble présenté comme les passages d'un acte. Une comparaison peut avoir un ordre éditorial explicite avec des blocs séparés. Changer cet ordre ne réordonne ni les fragments du bordereau ni les paragraphes historiques.

Un segment PHRASE restitue le quote_text certifié entier. La composition n'en découpe pas une portion pour fabriquer une citation plus courte; elle peut sélectionner plusieurs PHRASE complètes et indiquer leurs séparations. Les emphases modifient seulement la présentation.

Les liens de passage PHRASE doivent utiliser une nouvelle route contextuelle du pont, validant version, identité et droits d'accès, ou ouvrir l'original documentaire. Les anciennes fiches Quote sont volontairement filtrées et doivent continuer à rendre 404 pour une PHRASE : réutiliser leur get_absolute_url comme seul lien de passage casserait T14. La nouvelle route lit le passage sélectionné, ou sa capture historique pour une version gelée; elle n'élargit pas la visibilité des routes héritées.

### 5.3 Fidélité des paragraphes reproduits

L'adaptateur d'acte restitue :

- le Document et l'occurrence source exacts;
- le texte complet du paragraphe selon sa structure vérifiée;
- son numéro conservé, distinct de item et de son rang de sélection;
- son rang canonique dans la source, calculé sur la structure complète;
- les empreintes du texte, du numéro, de la structure pertinente et du fichier original;
- la conformité au scan et sa trace, selon la politique de CertificationPassageActe proposée.

Si le paragraphe a été scindé en nœuds de travail, il faut établir sa correspondance avec le paragraphe réel : ne pas concaténer automatiquement parent et descendants, au risque de doubler du texte. Une occurrence source ambiguë ou incomplète bloque le rendu strict.

Les numéros 4–7 puis 14–18 décrivent les passages originaux. La mention « paragraphes 8 à 13 non reproduits » n'est possible qu'après examen de la structure source; le moteur ne déduit pas une plage numérique en supposant que tous les numéros existent. Un saut ou une répétition de numéros imprimés reste une propriété de la source.

### 5.4 Texte historique, emphases et sécurité

Le flux de rendu distingue les segments SOURCE_LITERAL, REFERENCE_ACTIVE et ANNOTATION_EDITORIALE. Une chaîne P-2 contenue dans SOURCE_LITERAL est reproduite telle quelle, sans passage dans le remplaceur de cotes actives. La référence actuelle est un autre objet, lié au bordereau de la version.

Les emphases sont des plages start/end dans le **verbatim affiché**, avec son empreinte et un style autorisé. Elles ne modifient pas Quote.quote_text ou Statement.text source. Pour un scan corrigé, les positions d'emphase portent sur le texte humain certifié; elles ne sont pas les coordonnées de l'OCR. Une empreinte périmée invalide l'emphase. Une mention « emphase ajoutée » est éditoriale.

Tout texte source est échappé. Le moteur construit les éléments de mise en forme autorisés; il n'injecte pas le HTML brut d'une source ni d'une analyse. Le rendu du nouveau pont ne réutilise pas globalement enrichir/RE_COTE de schema_views.

### 5.5 Placement et réécriture

Les coordonnées d'InsertionRendu portent sur VersionTexte.texte de la cible rédactionnelle, en indices Python, début inclusif et fin exclusive. Le contrat accepte 0<=start<=end<=longueur. Les insertions d'un même texte sont appliquées selon leurs positions sur le texte original, sans décaler les suivantes; les insertions au même point ont un ordre_local unique.

VersionTexte.statement doit être exactement le Statement porté par la cible et son empreinte doit correspondre au texte courant du brouillon. Une égalité de texte avec le Statement d'une autre occurrence ne suffit pas à autoriser ce rattachement. Pour le premier profil, un groupe sans Statement peut porter un usage et des accès de navigation, mais aucune insertion dans son titre libre : un affichage dans la prose se place dans un Statement désigné. Le support de U2.OBS n'invente donc ni introduction ni dixième paragraphe imprimé.

Les remplacements qui se chevauchent, ou une insertion ambiguë à l'intérieur d'un remplacement, sont refusés dans le premier profil. Une composition peut être placée en bloc après un paragraphe via une insertion en fin de texte.

Après réécriture :

1. détacher le Statement si nécessaire;
2. capter la nouvelle VersionTexte;
3. conserver les anciennes insertions comme état historique ou les marquer périmées dans le brouillon;
4. demander/recalculer un rattachement explicite, puis le valider;
5. ne jamais rechercher une chaîne semblable et déplacer silencieusement l'insertion.

Déplacer un paragraphe entier sans modifier son texte conserve ses ancrages. L'état certifié d'une citation source ne certifie pas la pertinence de son emplacement dans une nouvelle rédaction.

## 6. Livrable 6 — Bordereau central, sous-cotes et histoire

### 6.1 Contrat central

Une seule chaîne de calcul produit un **ResultatVersion**, utilisé par l'éditeur, la prévisualisation, le rendu propre, les exports et le gel. Sa partie calcul documentaire est pure sur des valeurs résolues; la collecte depuis l'ORM et les adaptateurs reste une couche d'entrée du même service.

~~~text
resoudre_version(version, profil, strict)
  → identité/révision d'entrée + empreinte de dépendances
  → index des numéros rédactionnels
  → usages et feuilles effectives avec tous leurs parcours
  → pièces et fragments dédupliqués, datés, ordonnés et cotés
  → compositions, références et diagnostics
~~~

Une vue filtrée pour la navigation ne change pas le périmètre de la version. Pour produire un acte réellement amputé d'une section et de ses usages, il faut une version ou un périmètre de production explicitement défini, puis un calcul cohérent de cet ensemble. Masquer les supports techniques dans une vue propre ne retire aucun usage.

### 6.2 Valeur minimale retournée par chaque adaptateur

| Champ | Contrat |
|---|---|
| element_key | Modèle qualifié + PK de l'élément; pour un acte, occurrence LibraryNode source. Aucun ContentType numérique dans une identité exportée. |
| piece_key | Modèle qualifié + PK de l'unité documentaire cotable. |
| fragment_key | Identité canonique du passage dans cette pièce, ou absent pour la pièce entière. |
| position_source | Tuple ordonnable dans la structure complète de la source. |
| date_documentaire | Valeur, précision, champ d'origine, convention de fuseau, statut DATEE/A_DATER/ATEMPORELLE. |
| provenance | Cause d'origine si connue, titre, auteur/date, contenant et localisation; la cause d'utilisation reste distincte. |
| contenu_restituable | Texte ou structure depuis le modèle source, avec son régime de fidélité. |
| verification | État de certification effectif et preuves associées, ou régime de vérification propre au type. |
| empreintes / liens | Hash des composants pertinents, accès au fichier/document et passage; diagnostics explicites. |

Le GFK est un mécanisme d'accès, pas une politique d'acceptation. Un registre fermé d'adaptateurs reconnaît les types admis. Un Statement nu est refusé lorsqu'une occurrence dans un acte est nécessaire. Un lien générique vers une Quote n'est jamais réputé PHRASE parce qu'il se résout.

### 6.3 Identité, contenant, dates et positions par type

| Type d'élément | Pièce cotable | Fragment et ordre | Datation / contrôles |
|---|---|---|---|
| Quote PHRASE de courriel | Email individuel | (piece_key, PHRASE, start, end); ordre start puis end | date_sent; pas saved_at comme substitut silencieux. Corps canonique défini par le contrat cible. |
| Quote PHRASE de PDF | PDFDocument | Même principe; bornes absolues dans transcription, avec repères de page conservés | document_date; pas uploaded_at. Les pages sont un localisateur, pas un remplacement des bornes canoniques. |
| Paragraphe d'acte | Document reproduit finalisé | (piece_key, PARAGRAPHE_ENTIER, source_library_node_pk); ordre canonique de la structure source, puis PK si égalité technique | document_original_date vérifiée; le défaut automatique à la création n'est pas une preuve de date. |
| Email entier | Email | Aucun fragment | date_sent; utilisé notamment pour le constat d'absence dans le message entier. |
| PDF/Document entier | Objet documentaire lui-même | Aucun fragment | Date métier vérifiée; trace de l'original. |
| Event | Event comme pièce composée lorsque ce contenant est choisi | Éléments du contenant dans l'ordre du rendu; photos actuellement datetime_original puis PK | Event.date. Composition et fichiers doivent être fixés; pas de conversion locale abusive des heures EXIF. |
| Photo d'un PhotoDocument | PhotoDocument explicitement désigné | Photo comme fragment; ordre de page du contenant, actuellement PK | Date documentaire selon politique validée. Ne pas réordonner les pages par EXIF. |
| Photo autonome | Photo si cette unité est choisie explicitement | Pièce entière, ou fragment futur défini séparément | Date EXIF/XMP fiable selon sa convention; repli système non admis sans justification. |
| ChatMessage | ChatSequence explicitement désignée | Message : ordre timestamp puis PK dans la séquence | Date de la séquence issue des messages vérifiés; pas de date de création technique. |
| CONTEXTE interne | Aucune | Aucun | Ne génère ni cote ni citation probatoire. |

Un message ou une photo peut appartenir à plusieurs contenants M2M. L'adaptateur exige alors le contenant choisi et vérifie l'appartenance. Il ne prend pas le premier. Deux contenants distincts ne sont pas fusionnés parce qu'ils partagent un élément. Les sources structurées qui ne disposent pas encore d'un contrat fiable de date/contenant/rendu sont diagnostiquées comme non admissibles au profil strict, sans bloquer la conception des autres types.

Les précédences métier existantes sont réutilisables, mais les replis de get_exhibit_date ne le sont pas sans contrôle : Email revient sur saved_at; PDF sur uploaded_at; Document sur created_at; PhotoDocument sur created_at. Le service ancien de cotation lit toute la table BordereauDepotJuillet; il ne peut pas calculer les seuls usages du nouveau pont.

### 6.4 Algorithme et décisions de tri

1. Vérifier la version, son document, son profil et les révisions dépendantes.
2. Parcourir tous les usages inclus, portés par les Statements **et les groupes**.
3. Développer les sélections en feuilles; conserver (cible, usage, sélection, feuille, chemin).
4. Résoudre chaque ELEMENT par son adaptateur; ne pas exploiter les sources de feuilles non sélectionnées pour le bordereau.
5. Refuser les diagnostics bloquants : source absente, mauvais contenant, occurrence ambiguë, régime ou certification invalide, date requise absente, position non déterminable.
6. Dédupliquer les pièces par piece_key. Une sélection de fragment inscrit sa pièce entière; un usage du document entier et d'un fragment ne doublent pas cette pièce.
7. Trier les pièces datées par date documentaire normalisée selon la politique du profil, puis modèle qualifié et PK. Une date au jour est acceptable; la convention de position dans cette journée doit être explicite et ne prétend pas établir une heure. Départage des égalités indépendant de l'ordre des requêtes.
8. Affecter P-1, P-2,… dans le profil CHRONO_VERSION proposé. Les atemporelles explicitement qualifiées suivent les pièces datées, triées par identité. Une pièce simplement à dater bloque le profil strict; l'aperçu de travail affiche un diagnostic et des rangs provisoires clairement identifiés.
9. Pour chaque pièce, dédupliquer les fragments par fragment_key, conserver les identités d'élément correspondantes et tous les parcours d'utilisation, puis trier par position_source.
10. Affecter P-n.1, P-n.2,… aux fragments sélectionnés; aucune sous-cote pour une utilisation du document entier seul.
11. Valider les compositions et insertions contre ces sélections. Résoudre leurs références depuis cette table uniquement.
12. Retourner l'ensemble, les diagnostics et une empreinte des entrées/profils. Les sorties ne recalculent pas les cotes séparément.

Les dates sans heure suivent une convention de tri déclarée, par exemple début de journée locale, avec précision JOUR conservée dans le résultat. Les dates partielles plus vagues exigent une politique explicite avant un gel strict. Pour les heures vraies, normaliser les fuseaux; pour les heures d'appareil historiquement étiquetées UTC mais contenant une heure au mur, suivre le contrat du fournisseur sans leur appliquer localtime. Cette particularité est documentée dans [events/models.py](../../events/models.py), lignes 29–37.

Le plancher historique de l'an 2000 est une règle de détection des sentinelles de l'ancien dossier, pas une interdiction universelle des sources antérieures à 2000. L'adaptateur doit distinguer une sentinelle d'une vraie date ancienne.

### 6.5 Égalités, doublons et chevauchements

| Situation | Politique proposée |
|---|---|
| Même élément source utilisé plusieurs fois | Une pièce et un fragment; tous les chemins et affichages restent distincts. |
| Deux feuilles vers la même occurrence source | Déduplication documentaire; aucune fusion de leurs rôles d'organisation. |
| Deux PHRASE aux mêmes bornes et même source | L'unicité cible de l'Agent A doit l'empêcher. Si l'adaptateur en reçoit néanmoins deux : diagnostic d'intégrité, pas de choix arbitraire par PK. |
| Même texte à deux positions de la source | Deux fragments distincts; le texte n'est pas une identité. |
| PHRASE partiellement chevauchantes | Refus strict dans le premier profil jusqu'à arbitrage; pas de fusion automatique ni troncature de phrase. |
| Même numéro imprimé porté par deux occurrences d'acte | Deux fragments par PK distinctes, ordre source conservé et localisation non ambiguë; le numéro seul ne déduplique rien. |
| Texte d'un même ancrage discordant | Refus et vérification; ne pas retenir « le plus récent ». |
| Pièces de même date | Départage modèle qualifié/PK déterministe, sans leur attribuer une priorité probatoire. |

### 6.6 Sous-cotation des paragraphes d'actes : proposition à décider

**Proposition D04 : un paragraphe source complet identifié par son occurrence constitue un fragment; sa sous-cote séquentielle dépend de sa position dans l'ensemble des fragments utilisés de sa pièce.**

Pour le sous-ensemble limité au document de novembre, sélection 4,5,6,7,14,15,16,17,18 :

| Paragraphe historique | Sous-cote, si la pièce a reçu P-n |
|---:|---|
| 4 / 5 / 6 / 7 | P-n.1 / P-n.2 / P-n.3 / P-n.4 |
| 14 / 15 / 16 / 17 / 18 | P-n.5 / P-n.6 / P-n.7 / P-n.8 / P-n.9 |

U2 réutilise 14–17 : aucune nouvelle entrée de pièce ou de fragment. Une citation composite des neuf passages ne reçoit pas une dixième sous-cote. Le rendu conserve à la fois « § 14 » comme numéro source et sa sous-cote active P-n.5. Il ne traite pas .14 comme synonyme automatique du § 14.

Alternatives à arbitrer : simple cote documentaire accompagnée de « §§ 4–7 et 14–18 », sans sous-cotes pour ces occurrences; ou unité de fragment regroupant une plage. La première s'écarte du contrat général de sous-cotation des éléments; la seconde rend l'identité dépendante de la composition et complique les recouvrements U1/U2. La recommandation est donc l'occurrence complète, sans lui appliquer PHRASE. Une subdivision future d'un paragraphe demande un contrat distinct.

### 6.7 Juillet 2026 : conservation et concordance

**Contradiction documentaire précise :** la méthodologie approuvée § 3.3 impose P-1..P-106 permanents et P-107 pour une nouvelle pièce. CONCEPTION_PREUVE § 4, lignes 501–510, décrit leur remplacement dans les versions futures par un classement chronologique, et le mandat précédent demande le recalcul par version. Ces deux politiques ne peuvent pas gouverner simultanément la même nouvelle version sans règle de portée.

**Arbitrage proposé D05 :**

- JUILLET_2026_HISTORIQUE : associations et libellés inchangés, cotes qualifiées par ce bordereau; aucune réaffectation de l'archive.
- CHRONO_VERSION : pour une version nouvelle explicitement soumise à cette politique, rangs recalculés depuis ses usages, cotes toujours qualifiées par version.
- Référence interne = identité documentaire; référence procédurale affichée = (version de bordereau, cote).
- Si D05 n'est pas approuvée, aucune mise en production du profil CHRONO_VERSION; l'étude peut continuer à le simuler. Aucune modification de la méthodologie n'est faite ici.

Le dépôt du 24 juillet à 15 h 19 était **papier**. Le doc 9 et l'archive restent des référents historiques; un arbre nouveau ne sera pas présenté comme remis au greffe.

Import ultérieur, extérieur à la nouvelle application :

1. Lire la colonne **cote** non nulle de BordereauDepotJuillet; exclure cote_pont et les lignes postérieures à cote nulle.
2. Comparer au cotes.lock.json gelé; conserver l'empreinte, les libellés originaux et les identités qualifiées. Les 268 lignes/106 racines et 66 ajouts sont les effectifs **documentés**, non un comptage réalisé aujourd'hui.
3. Conserver le sens historique des groupes/composants. Une entrée P-43.7 peut être un document d'une liasse, pas la septième phrase d'une pièce moderne.
4. Traiter explicitement les équivalences Photo/PhotoDocument et les contenus de liasses/fils. Les quatre équivalences décrites par E01 sont une trace documentaire, pas une dispense de contrôle lors de l'import.
5. Écrire un contenu historique distinct, sans inventer des usages du nouveau pont en juillet. Garder les champs inconnus comme tels.

La concordance normale joint les identités exactes et donne conservée, ajoutée ou non utilisée dans la version suivante. Un ancien fil peut correspondre à plusieurs courriels; une liasse à plusieurs pièces; une photo à un contenant validé. Ces cas demandent une relation explicite CONTIENT/EQUIVALENCE_VALIDEE, avec son fondement historique, et ne se déduisent pas de la seule appartenance M2M actuelle.

Une cote racine historique peut donc avoir N correspondants nouveaux. Un composant non réutilisé reste visible comme historique/non utilisé; la concordance ne le supprime pas. Une identité ancienne non résolue bloque l'affirmation d'une concordance complète.

## 7. Livrable 7 — Versionnement, gel et démonstrations

### 7.1 Ce qui évolue et ce qui reste stable

| Objet | Brouillon | Après gel |
|---|---|---|
| Source documentaire | État final; aucun versionnement créé par l'acte | Même identité et original; contrôle d'intégrité. |
| Statement rédactionnel | Réécriture avec détachement si partagé | Texte et occurrence verrouillés; texte capturé dans le contenu gelé. |
| Structure / usages / sélections / compositions | Éditables par services, avec révisions | Immuables; copiés et remappés dans une nouvelle version pour changer. |
| Preuve réutilisée | Modification en place seulement si privée, non verrouillée et dans le périmètre demandé | Arbre entier verrouillé; modification par copie entière avec issue_de. |
| Citation/transcription dérivée | Contrat de correction et certification propre au fournisseur | Texte utilisé et preuve de certification capturés; aucune résolution vivante ne remplace le rendu historique. |
| Cotes / bordereau | Calculés | Valeurs conservées dans le contenu canonique; pas de recalcul courant. |
| Transmission | Sans effet sur les brouillons | Événement ajouté au même contenu figé; aucune remise à zéro du gel. |

La PK d'une source ne suffit pas à garantir le contenu d'une représentation dérivée encore corrigeable. La capture des passages effectivement utilisés au gel conserve une **représentation de l'acte**, sans créer de nouvelle version de l'Email, du PDF ou de la photo.

### 7.2 Contenu canonique du gel

ContenuVersionFige contient un document structuré, validé par un numéro de schéma :

~~~text
identité : cause, acte, version, instant, profil et algorithmes
document :
  occurrences, parent/ordre, type/rôle/présentation
  Statement et VersionTexte, textes exacts, empreintes
  index complet des numéros et sous-items, titres et valeurs d'en-tête
usages_et_preuves :
  cibles, usages, sélections
  arbres entiers utilisés : nœuds/ordre/rôles/références source
  feuilles effectives et tous les parcours d'utilisation
rendu :
  compositions/segments/emphases/insertions/ancrages
  passages résolus effectivement utilisés, provenance et traces de certification
bordereau :
  pièces et fragments, identités, dates/précisions, positions, cotes
  références de concordance historique validées
manifeste :
  empreintes des composants et originaux
  versions des adaptateurs, moteur, gabarits, styles et ressources
  liste des livrables avec taille et empreinte
~~~

L'arbre entier est conservé comme organisation; les feuilles non sélectionnées n'entrent pas au bordereau et n'exigent pas une certification de citation pour cet usage. Leur présence ne force pas la capture du texte de toutes les sources non utilisées.

Les textes dérivés et les numéros source nécessaires au rendu sont capturés. Un simple hash sans texte ne permettrait pas de reconstruire une citation dont la transcription a changé. Les livrables exacts sont archivés avec leurs octets; une régénération future peut préserver le contenu sans reproduire tous les octets d'un PDF si l'environnement diffère. Seul le fichier archivé et son hash attestent les octets transmis.

La sérialisation canonique fixe l'UTF-8, les clés d'objet triées et les formats de dates/identités; elle conserve l'ordre sémantique des listes, notamment paragraphes, segments et fragments. L'empreinte globale est calculée sur le contenu et le manifeste sans inclure son propre champ d'empreinte. Les fichiers ne doivent pas introduire une dépendance circulaire en contenant une empreinte qui dépend de leurs propres octets.

### 7.3 Protocole de gel proposé

1. Préparer un ResultatVersion strict et ses livrables candidats dans un stockage temporaire isolé. Rien n'est encore déclaré gelé.
2. Ouvrir une transaction de finalisation. Verrouiller selon un ordre commun aux services : document/version concernés, puis preuves par PK croissante; stabiliser les représentations dérivées lues. Toute opération qui les modifie doit respecter ces verrous ou une garde relationnelle équivalente.
3. Vérifier à nouveau révisions et empreintes de toutes les entrées, sources et certifications. Si elles diffèrent du résultat préparé, refuser et recalculer; ne pas geler le mélange de deux états.
4. Valider l'ensemble des contraintes, y compris insertions, dates, certification, appartenance des usages et statut des éléments sources.
5. Déposer les livrables sous des URI nouvelles et immuables; vérifier leur lecture et leurs empreintes. Une panne de stockage fait échouer la finalisation. Les éventuels fichiers orphelins ne valent pas gel.
6. Créer l'unique ContenuVersionFige et ses LivrableVersion; poser le verrou neutre du Document, les verrous des Preuve entières et l'état GELEE de VersionActe dans cette transaction.
7. Après succès, servir le contenu et les fichiers conservés. Enregistrer séparément chaque transmission externe.

La transaction SQL ne rend pas le système de fichiers transactionnel. L'ordre ci-dessus permet un fichier candidat orphelin en cas d'échec, mais interdit une version gelée pointant vers un fichier incomplet. La suppression des orphelins est une opération de maintenance séparée.

Les sources finales doivent disposer d'une protection locale contre les modifications/destructions et d'un stockage d'originaux non remplaçable; les hashes apportent la détection, pas une interdiction physique. Les représentations corrigibles doivent être stabilisées pendant la lecture/capture. Ces protections sont un prérequis du premier gel réel, pas une propriété actuelle démontrée des modèles.

La finalisation est idempotente : une nouvelle demande sur la même version déjà gelée retourne son contenu existant si elle vise le même ensemble; elle ne le remplace jamais. Un contenu différent exige une nouvelle VersionActe. Unicité et verrouillage interdisent deux gels concurrents divergents.

### 7.4 Copier une version et modifier une preuve partagée

cloner_version crée :

- un nouveau Document et de nouveaux LibraryNode, avec table ancien→nouveau;
- des usages, sélections, compositions et insertions propres à la nouvelle version;
- les mêmes sources et, initialement, les mêmes preuves et Statements;
- des références remappées vers les nouvelles occurrences et nouveaux usages; les VersionTexte peuvent être partagées si le Statement et son texte restent identiques;
- une filiation explicite de VersionActe et une correspondance des occurrences, sans réécrire la version source.

Avant toute réécriture d'un Statement partagé, le service neutre le détache. Une VersionTexte utilisée ne se réécrit ni ne se supprime. Le code actuel fournit un précédent de détachement dans [concordance.py](../../document_manager/concordance.py), lignes 164–205; il ne suffit pas à lui seul au gel complet proposé.

Si PR.DANSE est partagée par V1 gelée et deux brouillons V2/V3, modifier la danse pour V2 crée PR.DANSE.B issue_de PR.DANSE. La copie entière fournit une correspondance de tous les NoeudPreuve. Seuls les usages de V2 explicitement concernés sont repointés; leurs sélections sont remappées sur les nœuds copiés. V1 et V3 restent sur PR.DANSE. Les segments de composition gardent leurs identités source; leur appartenance aux nouvelles sélections est revalidée.

Une sélection de racine suit le contenu courant d'une preuve privée de brouillon. Dès qu'une preuve est partagée, toute réorganisation susceptible de modifier les feuilles sélectionnées par d'autres usages passe par la copie et le repointage explicites. Aucun copy-on-write de chemin minimal n'est nécessaire.

### 7.5 Démonstration chiffrée de deux versions

Données **synthétiques**, indépendantes des pièces réelles; politique CHRONO_VERSION supposée approuvée pour cette démonstration :

| Pièce | Date | Fragments et positions |
|---|---|---|
| X = email_manager.email:EX | 10 janvier | Q.X.A [100,150), Q.X.B [300,350) |
| Y = pdf_manager.pdfdocument:EY | 20 janvier | Aucun fragment dans cet exemple |
| Z = email_manager.email:EZ | 5 janvier | Aucun fragment |

V1 utilise X.A, X.B et Y. Les paragraphes peuvent afficher X.B avant X.A :

| Version | Bordereau et sous-cotes |
|---|---|
| V1 gelée | X=P-1; X.A=P-1.1; X.B=P-1.2; Y=P-2 |
| V2 copie de V1, ajout de Z et retrait du dernier usage de X.A | Z=P-1; X=P-2; X.B=P-2.1; Y=P-3; X.A absent |
| V1 relue après ces changements | Exactement X=P-1, X.A=P-1.1, X.B=P-1.2, Y=P-2 et mêmes fichiers archivés |

Correspondance par identité : X P-1→P-2; Y P-2→P-3; Z ajoutée; X.B P-1.2→P-2.1; X.A historique non utilisée dans V2. La nouvelle P-1 n'est pas une réaffectation de **V1/P-1**, qui reste X. Cette distinction exige D05; elle n'est pas appliquée au dépôt réel par l'étude.

Déplacer ensuite les paragraphes de V2 modifie leurs numéros rédactionnels, sans changer l'ordre X.A/X.B dans leur source. Réorganiser une copie de PR.* dans V2 n'altère aucun composant du ContenuVersionFige de V1. Ni X, ni Y, ni Z n'ont été copiés ou versionnés.

### 7.6 Intégrité contre les contournements

Les protections existantes de document_manager visent notamment ReferentHistorique et les documents reproduits. Elles ne couvrent pas actuellement tout l'agrégat VersionActe ni toutes les écritures de masse. Le nouveau verrou neutre et les gardes doivent vérifier aussi l'ancien rattachement d'une ligne : changer d'abord document_id ou preuve_id ne doit pas permettre de sortir une ligne gelée de son périmètre.

Les tables gelées et événements sont append-only pour le rôle applicatif; les triggers doivent refuser les mutations par update/bulk/delete, y compris la suppression de la ligne de protection. Les fournisseurs documentaires gardent leurs protections propres, sans importer proof_manager. Le pont vérifie encore la fidélité à la lecture.

La corruption hors des chemins autorisés n'entraîne jamais un nouveau rendu vivant d'une version historique. Le système sert son artefact conservé et signale le contrôle d'intégrité défaillant. Une empreinte n'est pas une signature contre un administrateur pouvant tout réécrire; signature externe ou stockage à rétention renforcée sont des décisions d'exploitation distinctes.

## 8. Livrable 8 — Matrice Exigence → Modèle → Service → Contrôle → Test

### 8.1 Services de référence proposés

| Identifiant | Service et responsabilité |
|---|---|
| S1 | valider_structure / déplacer / numéroter : rives neutres et profil récursif. |
| S2 | utiliser_preuve / modifier_selection / retirer_utilisation : relations et sélections effectives. |
| S3 | resoudre_element : adaptateurs, provenance, dates, fidélité et certification. |
| S4 | resoudre_version : calcul unique du bordereau et des références. |
| S5 | composer / ancrer / rendre : compositions, insertions et sorties depuis ResultatVersion. |
| S6 | cloner_version / copier_preuve_et_repointer : isolation des copies et remappages. |
| S7 | preparer_livrables / geler_version / lire_version_gelee : conservation et intégrité. |
| S8 | importer_historique / comparer_bordereaux : import externe ponctuel et concordance. |

Tous les tests ci-dessous sont **spécifiés, non exécutés**. Leur future exécution doit utiliser une base de test isolée ou des adaptateurs de test, jamais la base réelle. Les scénarios PHRASE peuvent être éprouvés sur des objets de test conformes au contrat cible avant toute citation PHRASE réelle.

### 8.2 Couverture T01–T22

| ID / exigence | Modèle | Service | Contrôle | Test positif et négatif pertinent |
|---|---|---|---|---|
| T01 — Deux unités D=2 indépendantes | LibraryNode typé, VersionActe | S1/S2 | Même Document; sous-arbres identifiés | Créer U1/U2 avec leurs branches; déplacer U1 sans rattacher les usages d'U2. Refuser un enfant dont document diffère du parent. Dépend D01/D03. |
| T02 — Rôles différents à profondeur égale | nature_structurelle + role_editorial | S1 | Typage indépendant du titre et de l'ordre | Permuter/renommer OBS et REF : rôles inchangés. Refuser qu'un renommage libre décide du type. Dépend D03. |
| T03 — Regroupements récursifs | LibraryNode / profil | S1 | Parenté valide, profondeur non sémantique | Imbriquer B/B1/mouvements; Statement reste Statement à D=7. Détecter dépassement de capacité du stockage; ne pas classer selon depth. Dépend D03. |
| T04 — Numérotation D=4/D=7 | Index de présentation | S1/S5 | Un compteur principal par document | O1,O2,O3,R01 → 1,2,3,4; insertion d'un groupe/support ne change pas la suite. Un filtre d'écran conserve les numéros. Dépend D03. |
| T05 — Proposition conceptuelle sans support | Statement et 0 utilisation | S1/S4 | Aucun support obligatoire universel | C.R02 sans UP valide; pas de pièce fabriquée. Un avis éditorial éventuel ne devient pas une erreur structurelle. |
| T06 — Deux supports d'une proposition | Deux UtilisationPreuve et sélections | S2/S4 | 0..N usages, même cible/version | Deux preuves correctement sélectionnées; sources communes dédupliquées. Refuser une sélection de la mauvaise preuve. Dépend D01. |
| T07 — Sélection d'une branche | SelectionPreuve / NoeudPreuve | S2/S4 | Développement du sous-arbre choisi seulement | Trois branches; une sélectionnée : seules ses pièces entrent. Sélection racine+feuille ne double rien. Refuser sélection vide valide. |
| T08 — Appui collectif explicite | UtilisationPreuve cible groupe ou conclusion | S2/S4 | Aucune justification par héritage implicite | Deux UP sur conclusion, puis usage propre sur groupe : périmètres explicites. Ajouter une source dans un autre descendant ne l'ajoute pas à la conclusion. Dépend D01/D02. |
| T09 — §§ 4–7 et 14–18 | CompositionCitation, SegmentCitation, occurrences source | S3/S5 | Ordre source, numéros conservés, omission | Neuf segments fidèles, séparation avant 14, un seul document. Refuser occurrence ambiguë, numéro requis manquant ou faux ordre SOURCE. Sous-cotes selon D04. |
| T10 — P-2 historique | Segment SOURCE_LITERAL et référence active distincte | S5 | Aucun remplacement de cote dans verbatim | Modifier la cote active : le P-2 interne reste identique et lien distinct. Détecter tout passage de ce segment dans un remplaceur global de cotes. |
| T11 — Citation de septembre en deux endroits | Une composition, deux InsertionRendu | S4/S5 | Deux ancrages, un fragment | INS.R05/INS.R07 affichent même texte et sous-cote. Retirer un affichage ne retire pas le fragment encore utilisé; retirer tous les usages le retire. |
| T12 — Source réutilisée B2/C | Utilisations distinctes, identité source commune | S2/S4 | Déduplication par pièce/fragment | Deux fonctions d'utilisation et une pièce; chemins tous conservés. Deux messages différents d'un échange ne sont pas fusionnés parce qu'ils ont la même date. |
| T13 — Absence dans un courriel entier | Usage ABSENCE_DOCUMENTAIRE, feuille Email entier | S2/S3 | Source entière et portée explicite | Usage entier consultable; pas de vérité calculée. Un seul extrait PHRASE ne satisfait pas le contrôle de portée pour une observation déclarée sur le courriel entier. |
| T14 — Retour à la source | Identités et localisateurs des adaptateurs | S3/S5/S7 | Document/passage exacts et droits d'accès | Depuis référence active, ouvrir le bon original et passage via la route contextuelle. La fiche Quote héritée continue de refuser PHRASE. Source absente ou empreinte différente : diagnostic, pas de première occurrence de remplacement. |
| T15 — Éditeur/clean/PDF cohérents | ResultatVersion, insertions, index de présentation | S4/S5 | Même résultat, supports non numérotés | Comparer pièces/références et numéros entre sorties; aucune perte d'insertion quand SUPPORT est masqué. Dépend D02/D03; moteur futur requis. |
| T16 — Copier et modifier sélection | VersionActe, copies d'usages, ContenuVersionFige | S6/S7 | Remappage et isolation | V2 retire X.A : V1 garde tous ses hashes/cotes/textes. Refuser une insertion de V2 pointant un usage de V1. Dépend D05/D08. |
| T17 — Preuve partagée entre brouillons | Preuve.issue_de et carte des nœuds | S6 | Périmètre de repointage explicite | Modifier pour V2 crée une copie; V3 inchangée. Refuser la modification en place de la preuve partagée/verrouillée; tester remappage branche et feuille. |
| T18 — Ancrage périmé | InsertionRendu + VersionTexte | S5/S6 | Empreinte et rattachement au Statement | Réécrire avant l'insertion : diagnostic et gel refusé jusqu'au réancrage. Aucun placement à l'ancienne position même si celle-ci reste dans les bornes. |
| T19 — HERITE dans un flux PHRASE | Quote, adaptateur et contrat de certification | S3/S5 | Régime explicite, certification effective | PHRASE de test valide acceptée; HERITE injectée par GFK ou all_objects refusée dans le nouveau flux. Champs cibles absents : capacité indisponible, jamais certification supposée. Dépend Agent A étape 2, sans PHRASE réelle requise pour les tests isolés. |
| T20 — Support orphelin ou inter-version | UtilisationPreuve; SUPPORT physique si choisi | S1/S2/S7 | FK, appartenance relationnelle, gardes différées | C projetée : projection absente si usage supprimé. C/B physique : orphelin refusé. Forger un mauvais document par update/bulk est refusé; mutation d'une cible existante également contrôlée. Dépend D02/D08. |
| T21 — Même source dans deux groupes de preuve | Deux NoeudPreuve, une identité documentaire | S2/S4 | Déduplication sans perte des chemins | Deux feuilles sélectionnées vers même fragment donnent une sous-cote et deux parcours. Ne pas fusionner les nœuds d'organisation. |
| T22 — Nouvelle section entre paragraphes | LibraryNode, index, usages et insertions | S1/S5/S6 | Association par PK, pas par numéro imprimé | Ajouter un Statement principal entre 2 et 3 : les suivants avancent d'un rang; groupes/supports seuls n'incrémentent rien. Les usages restent sur les mêmes occurrences; V1 gelée reste inchangée. Dépend D03/D08. |

### 8.3 Scénarios négatifs complémentaires

| ID | Action à éprouver sur données de test | Résultat exigé |
|---|---|---|
| N01 | Supprimer/rendre introuvable une cible GFK sélectionnée | Diagnostic bloquant; aucune pièce fantôme ni référence de remplacement. |
| N02 | Donner au fournisseur une date d'import seulement, ou une sentinelle | A_DATER; gel strict refusé. Une vraie date antérieure à 2000 reste admissible. |
| N03 | Corrompre par update les bornes, le texte ou les empreintes d'une PHRASE, y compris scan corrigé | Certification effective fausse; refus immédiat de nouveau rendu strict; pas d'attente de l'audit. |
| N04 | Donner deux ancrages PHRASE chevauchants ou identiques avec contenus discordants | Diagnostic selon § 6.5; aucune fusion/troncature implicite. Dépend D10. |
| N05 | Injecter HTML/script dans une source ou une annotation | Texte échappé, styles autorisés seulement, aucune exécution ni HTML brut injecté. |
| N06 | Modifier/supprimer/ajouter une ligne dans un agrégat gelé, y compris changer d'abord sa version ou son parent | Refus par gardes en base et services; empreinte du contenu conservé inchangée. |
| N07 | Modifier les photos/messages d'un contenant finalisé, ou choisir un contenant ambigu | Refus ou diagnostic d'intégrité; jamais un changement silencieux des pièces/rangs. |
| N08 | Modifier un schéma ou gabarit après gel | Le rendu historique lit l'index/contenu gelés et les livrables conservés; aucune renumérotation. |
| N09 | Importer cote_pont, une ligne à cote nulle ou une correspondance liasse non vérifiée comme juillet | Import rejeté ou marqué incomplet; archive/doc 9 inchangés. |
| N10 | Même date pour deux pièces, même timestamp pour deux messages | Ordres déterministes jusqu'à l'identité, indépendants de l'ordre SQL. |
| N11 | Éditer une sélection ou une preuve pendant la préparation du gel | Un état cohérent gèle ou la finalisation refuse; jamais un mélange. Tester les deux ordres d'acquisition des verrous. |
| N12 | Échec de stockage ou de transaction pendant le gel | Aucune version déclarée gelée avec un livrable absent; au plus fichiers candidats orphelins identifiés. |
| N13 | Modifier un Statement partagé par une autre version, sans détacher | Refus; édition par détachement préserve le texte source et invalide les insertions de la cible réécrite. |
| N14 | Remplacer un fichier original sous sa même référence | Détection d'empreinte et refus du nouveau rendu strict; artefact historique conservé et signalement d'intégrité. |

### 8.4 Critères d'acceptation des démonstrations

- U1/U2 : 65 occurrences principales identifiées, avec A et R08.a explicitement incomplets, sans faux contenu.
- Numérotation : index commun aux profondeurs 4/5/6/7 et aux surfaces de rendu; sources STORED inchangées.
- Bordereau : égalité exacte entre pièces issues des usages et pièces du résultat; aucune inclusion par simple présence dans une preuve.
- Rendu : neuf paragraphes distincts, omission explicitée, P-2 littéral intact, deux insertions pour un seul fragment commun.
- Conservation : comparaison avant/après des contenus gelés et hashes des livrables, pas seulement vérification que les PK existent encore.
- Intégration : aucune nouvelle dépendance d'exécution aux deux anciens ponts, aucune PHRASE observable par leurs consommateurs.

## 9. Livrable 9 — Recommandation, responsabilités, décisions et réalisation

### 9.1 Répartition des responsabilités

| Périmètre | Réutilisable / à construire | Limites |
|---|---|---|
| cause_manager existant | Cause, cause_origine, liens et historique | Pas d'inférence de provenance depuis un usage ou un bordereau. |
| document_manager existant | Document, occurrence LibraryNode, Statement, VersionTexte, distinction AUTO/STORED, détachement et protections historiques | Pas encore le profil récursif, les numéros communs aux profondeurs ni le gel complet d'une VersionActe. |
| Extensions document_manager | Typage par nœud; rôle; présentation; profil récursif; verrou documentaire neutre; stratégies du résolveur commun; contrôle des VersionTexte protégées | Aucun import de proof_manager; anciens profils inchangés par défaut. |
| Nouveau proof_manager | Preuve, NoeudPreuve, utilisations/sélections, compositions/insertions, adaptateurs, bordereau calculé, certification des passages d'actes, concordance d'exceptions | Pas d'import de case_manager/argument_manager; aucune source copiée ou versionnée par l'acte. |
| Nouvelle couche neutre act_manager proposée | Acte, VersionActe, contenu gelé canonique, livrables et transmissions | Ne connaît pas les modèles internes du pont; conserve leurs valeurs sérialisées. |
| Rives documentaires | Dates métier, provenance, texte canonique, originaux, état de finalisation/protection locale et fidélité des représentations | Les méthodes actuelles avec replis techniques ne suffisent pas toutes au profil strict. |
| Outil d'import extérieur | Lecture ponctuelle du registre juillet et du verrou | Aucune dépendance durable au registre ancien. |
| Orchestration du nouveau pont | Assemble présentation neutre, résolution probatoire et rendu; fournit ResultatVersion aux sorties | La rive n'importe pas cette orchestration pour fonctionner. |

La frontière proposée est :

~~~mermaid
flowchart LR
    PM["proof_manager : usages, preuves, bordereau, rendu"] --> DM["document_manager : documents et présentation"]
    PM --> AM["act_manager : actes, versions et contenu gelé"]
    PM --> SOURCES["Rives : courriels, PDF, photos, événements, chat"]
    AM --> DM
    AM --> CAUSE["cause_manager"]
    DM --> CAUSE
    IMP["Import historique ponctuel, extérieur"] --> OLD["case_manager historique"]
    IMP --> PM
~~~

Ce graphe décrit les dépendances du nouveau périmètre. Les imports anciens déjà présents dans certaines vues de document_manager sont constatés au § 3.1, sans être corrigés par cette étude. La nouvelle stratégie neutre doit pouvoir être appelée sans ces vues.

### 9.2 État du contrat de l'Agent A et compatibilité

| Niveau | État établi pour cette étude | Conséquence |
|---|---|---|
| Code de la branche lue | Quote courriel/PDF sans champ regime ni champs de certification cible; quote_text demeure éditable; positions courantes issues de recherche tolérante | Ne pas brancher le nouveau pont sur ce code en prétendant disposer de PHRASE certifiées. |
| Travail de l'étape 1 conservé en branche | Les objets Git 5fa62ed, b45808c et 11214d1 existent; le plan § 10.4 les décrit comme état validé sur clone, non poussé à la date de ce relevé | Distinction entre travail disponible en branche et déploiement réel. Cette étude ne vérifie pas une publication distante et n'effectue aucune fusion. |
| Situation la plus récente fournie par le mandat | Pilote P6 prêt pour autorisation; répétition sur sauvegarde fraîche et bascule réelle non autorisées | Aucun P6 exécuté; aucune attente de bascule pour concevoir. |
| Contrat cible étape 2 | PHRASE avec bornes, trois empreintes, certification effective et derived_from | Capacité future; aucune PHRASE réelle réputée disponible. |
| Futur pont | T-pont refuse toute certification ineffective | Contrôle dans l'adaptateur et avant chaque nouveau rendu strict/gel, même si un GFK ou gestionnaire de base a permis de charger l'objet. |

Le contrat cible doit être consommé tel que documenté :

~~~text
source canonique :
  Email.body_plain_text
  PDFDocument.transcription, en-tête retiré, repères de page conservés

bornes : indices Python [start, end)

valid_anchor =
  bornes dans le texte
  ET hash(source) = source_text_sha256
  ET hash(source[start:end]) = anchored_text_sha256
  ET hash(quote_text) = certified_text_sha256
  ET (corrected_on_scan OU source[start:end] = quote_text)

effective_certification = certified ET valid_anchor
~~~

Le pont ne réutilise pas les coordonnées repliées de position_in_source comme bornes certifiées. Il charge les PHRASE par le gestionnaire cible et valide le régime; un GFK peut utiliser le gestionnaire de base, donc la validation reste obligatoire. Il ne change pas Quote.objects de l'ancien système et n'ajoute pas de nouveau modèle au registre de types admis de ses formulaires.

**Compatibilités et points d'intégration à conserver :**

- Les trois gestionnaires de l'étape 1 et l'isolation des consommateurs hérités sont compatibles avec la nouvelle architecture.
- Les fiches héritées de Quote ne sont pas des routes de consultation PHRASE pour le nouveau pont; sa route contextuelle est un ajout autonome, pas une modification du filtre de l'Agent A.
- Le fallback actuel du corps vide vers le sujet dans Quote.source_text n'est pas le contrat PHRASE cible : un courriel sans corps ne reçoit pas un ancrage dans son sujet par commodité.
- L'étape 1 seule ne fournit ni bornes ni certification; aucune traduction « HERITE devient PHRASE » n'est implicite.
- Les passages d'actes reproduits nécessitent leur propre vérification; le contrat de Quote ne la fournit pas.
- Les protections de finalisation des sources, des représentations utilisées et du gel ne sont pas toutes réalisées par le plan de l'Agent A. Le pont les exige avant son premier gel réel; il n'adresse aucune demande de modification à l'Agent A dans ce mandat.
- La certification source est appréciée au moment du nouveau rendu. Une version déjà gelée conserve sa trace et ses livrables; une corruption ultérieure déclenche un diagnostic d'intégrité sans réécrire son histoire.

### 9.3 Décisions explicites à prendre

| Décision | Question au décideur | Recommandation et effet |
|---|---|---|
| D01 — Architecture et cardinalité | Approuves-tu C, avec 0..N utilisations par cible et une preuve par utilisation, en remplacement de l'enveloppe Demonstration proposée? | Oui. Maintenir les sélections multiples; pas de Demonstration supplémentaire sans responsabilité propre. |
| D02 — Groupes et supports | Approuves-tu des supports sur les groupes, et leur projection dans l'éditeur sans LibraryNode SUPPORT persistant par défaut? | Oui aux appuis de groupe explicites et à la projection. Stockage physique seulement si une opération exige cette identité arborescente. |
| D03 — Structure et numérotation | Approuves-tu les trois dimensions indépendantes et un compteur de paragraphes principaux commun à toutes profondeurs du nouveau profil? | Oui, profil limité aux documents de rédaction choisis; conserver LEGACY et STORED. |
| D04 — Sous-cotes d'actes | Un paragraphe source complet identifié par LibraryNode reçoit-il une sous-cote séquentielle selon sa position source? | Oui; numéro historique conservé en plus. Ni la composition ni chaque phrase du paragraphe ne crée une nouvelle unité. |
| D05 — Portée des cotes | Approuves-tu la séparation JUILLET_2026_HISTORIQUE / CHRONO_VERSION, avec cotes toujours qualifiées par version? | Oui pour satisfaire le recalcul demandé, avec évolution explicite de la règle méthodologique applicable aux versions futures; aucun changement de juillet. |
| D06 — Dates et ambiguïtés | Approuves-tu le refus strict des dates insuffisantes, les atemporelles explicites et les conventions de tri à précision déclarée? | Oui; aperçu provisoire autorisé avec diagnostic visible, aucun repli technique silencieux au gel. |
| D07 — Fidélité des actes reproduits | Approuves-tu une vérification explicite par occurrence/scan, distincte de PHRASE, pour leur nouveau rendu strict? | Oui; source/numéros/structure contrôlés et trace capturée. |
| D08 — Gel | Approuves-tu un contenu canonique structuré unique, les livrables immuables et les gardes relationnelles en base avant tout gel réel? | Oui; les instantanés et hashes seuls ne sont pas une protection d'écriture. |
| D09 — Forme des unités | La paire Observation/Réfutation est-elle une convention de départ ou une contrainte de tous les documents? | Convention/profil facultatif au départ. Ne pas imposer cette architecture narrative à tous les actes. |
| D10 — Chevauchements | Approuves-tu le refus initial des PHRASE chevauchantes ambiguës et des remplacements rédactionnels qui se recouvrent? | Oui; résoudre ou expliciter un profil ultérieur, sans fusion/troncature automatique. |
| D11 — Appui simple | Maintient-on le passage uniforme par Preuve, avec preuve atomique automatique pour une citation? | Oui recommandé; toujours une décision de conception à valider, distincte de A/B/C de cet addendum. |
| D12 — Découpage des modules | Approuves-tu act_manager comme couche neutre et le report du DAG, des renvois récursifs et de la copie minimale de chemin? | Oui; les cas actuels sont couverts par arbres simples, réutilisation des sources et copie entière. |

Ces questions ne présument aucune validation tacite. D01–D04/D11 structurent le schéma; D05/D06/D07/D08 conditionnent un résultat réel fiable; D09/D10/D12 fixent le périmètre et les profils.

### 9.4 Ordre de réalisation proposé

Les lots ci-dessous sont un plan, pas une autorisation. Leur numérotation est indépendante du pilote P6 de l'Agent A.

| Lot | Dépendances | Livraison vérifiable et critère de sortie |
|---|---|---|
| L0 — Décisions | Arbitrages D01–D12 | Contrats et profils approuvés; aucune politique contradictoire silencieuse. Sources et textes manquants listés séparément de l'implémentation. |
| L1 — Présentation neutre | D03/D09; branche cible fixée | Typage, récursion, index commun et sortie de référence de 65 paragraphes; tests T01–T05/T22 et non-régression des documents historiques/LEGACY. |
| L2 — Usages et sélection | D01/D02/D11; L1 | Preuve atomique/organisée, appuis de groupes, sélection partielle, réutilisation et copie entière; T06–T08/T17/T20/T21 sur base isolée. |
| L3 — Adaptateurs et bordereau | D04/D06/D07; contrats source | Un seul ResultatVersion; pièces et fragments exacts, datation et diagnostics; tests de tri/déduplication. PHRASE éprouvée avec doubles de contrat puis contre l'étape 2 disponible en environnement isolé. |
| L4 — Compositions et insertions | L1–L3; D10 | Rendu simple/composite, omissions, répétitions, liens, emphases et ancrages; T09–T15/T18/T19, sans prétendre que des PHRASE réelles existent. |
| L5 — Conservation complète | D08; protections locales et stockage prêts; L1–L4 | Gel atomiquement cohérent, gardes bulk/SQL, clone/remappage, fichiers archivés, transmissions; T16/N06/N08/N11–N14. Aucun premier gel réel avant réussite. |
| L6 — Reprise historique et usage réel | D05; contrôle archive/registre; L5 | Import ponctuel validé, concordance 1:N et exceptions explicites; N09 et relecture du dépôt intact. Validation séparée avant toute opération sur base réelle. |
| Ultérieur | Besoin concret nouveau | DAG, renvois entre sous-nœuds, propagation automatique ou copie minimale de chemin. Pas de dépendance des lots précédents envers ces fonctions. |

### 9.5 Risques d'intégration principaux

| Risque | Mesure proposée |
|---|---|
| Anciennes vues filtrent/chargent les objets selon leurs propres types et régimes | Nouvelle orchestration explicite; adaptateurs et résultat commun; aucune insertion de PHRASE dans les chemins hérités. |
| Extension de numérotation affecte les sources historiques | Profil par défaut LEGACY, stratégie STORED conservée, tests sur les sorties existantes avant activation du nouveau profil. |
| GFK sans intégrité native vers l'objet cible | Registre de types fermé, validation d'existence/appartenance, protection locale des sources et refus strict à la lecture. |
| Supports physiques créent deux autorités | Projection par défaut; si stockés, lien unique et parent=cible contrôlé, jamais deux jeux de sélections. |
| Éditions de masse ou mouvements Treebeard contournent les signaux | Gardes relationnelles et d'immutabilité en base, vérifiant ancien et nouveau périmètre; tests de contournement dédiés. |
| Correction de transcription invalide une citation | Contrat Agent A et captures de rendu au gel; aucune source réécrite pour « réparer » un ancien livrable. |
| Fichiers/ressources de rendu remplacés | URI immuables, hashes, sauvegarde et archivage des livrables; manifeste de gabarits/ressources. |
| Source ou texte d'exemple manquant | Diagnostic explicite; ne pas remplacer par un extrait de travail présenté comme original vérifié. |
| Confusion entre cote de juillet et cote nouvelle | Qualification par bordereau/version, concordance explicite, D05 avant production. |

Le choix proposé conserve les opérations du rédacteur au centre : écrire et organiser les propositions, choisir leurs appuis, placer les citations, produire un bordereau cohérent puis conserver l'ensemble communiqué. Les mécanismes d'inférence restent hors périmètre; les invariants documentaires, de sélection et d'histoire sont explicitement couverts.
