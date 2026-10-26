# Architecture C — modèle transversal et revue de cohérence

**C-TRANS-2026-10-21-R1 — 21 octobre 2026.** Mandat documentaire :
[source exacte](references/MANDAT_COHERENCE_TRANSVERSALE_2026-10-21.md).
La source reçue s’arrête après « Pour chaque exigence transversale importante,
indique : ». La matrice ci-dessous fournit la chaîne et les limites demandées
aux §§4–6 du mandat, sans lui attribuer une liste de colonnes absente.

**Conclusion : les décisions A–E sont maintenant explicitées dans les contrats
transversaux, les stories et les compléments de spécification. La cohérence
horizontale complète des use cases reste à démontrer : plusieurs séquences,
ERD et classes locaux n’existent pas encore.** Aucun statut de validation
ou d’approbation de dossier n’est déduit de ce travail. Aucun développement,
schéma, migration, accès à la base, commit, push ou fusion n’est effectué.

Cette note définit les trois projections communes de TRANS-02 et consigne
la revue; la [matrice existante §13](MATRICE_COUVERTURE_V2_C.md#13-cohérence-transversale--actes-révisions-de-preuve-et-histoire)
porte la couverture, le [backlog §15](BACKLOG_ARCHITECTURE_C.md#15-fondations-transversales--r8-trans)
porte les dépendances et le [registre](registre_validation.md) garde seul les
statuts. L’[avenant](AVENANT_ARCHITECTURE_C.md) et les [décisions consolidées](DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md)
restent les autorités D/CF. Aucun registre ou backlog parallèle n’est créé.

## 1. Trois vues à lire ensemble

| Vue | Source | SVG | PNG | Périmètre |
|---|---|---|---|---|
| État VersionActe | [PlantUML](modele_global/etat_version_acte.puml) | [SVG](modele_global/etat_version_acte.svg) | [PNG](modele_global/etat_version_acte.png) | UC01A/01B/11/19; une instance passe de BROUILLON à FIGEE |
| État des révisions de preuve | [PlantUML](modele_global/etat_revision_preuve.puml) | [SVG](modele_global/etat_revision_preuve.svg) | [PNG](modele_global/etat_revision_preuve.png) | UC03/04/07/11; une révision, distincte de l’identité Preuve |
| ERD transversal C | [PlantUML](modele_global/erd_transversal_c.puml) | [SVG](modele_global/erd_transversal_c.svg) | [PNG](modele_global/erd_transversal_c.png) | Cause/Acte/VersionActe, Preuve/révisions, sélections, cotation et gel |

Ces vues sont **cibles conceptuelles proposées**, non un relevé ORM ni des
migrations. Cause est réutilisée; les occurrences et sources s’appuient sur
les modèles existants. Acte, VersionActe, RevisionPreuve et les associations
ne prescrivent ici ni tables nouvelles, ni clés composites physiques.
Les contraintes effectives devront être montrées dans les ERD locaux.
Le [modèle transversal de cotation](MODELE_TRANSVERSAL_COTATION.md) conserve
son périmètre et son autorité spécialisés. Son ERD est une projection des
éléments documentaires résolus par les sélections, y compris une sélection
de branche; il n’impose pas une seconde sélection indépendante des nœuds.

## 2. Invariants essentiels

1. **Contexte.** Cause → 0..N Acte; Acte → 1..N VersionActe dès création
   valide; chaque version possède son Document PRODUCED propre. La cause
   d’origine d’une source n’est pas remplacée par la cause d’usage.
2. **État d’acte.** BROUILLON est modifiable sous contrôle de révision;
   FIGEE ne redevient jamais BROUILLON. Une modification produit une autre
   identité de VersionActe, avec filiation et nouveaux textes privés PRODUCED.
   R06 reste sur le parcours et le nombre de brouillons actifs, pas sur
   l’existence de plusieurs versions d’un même Acte.
3. **Identité probatoire.** Preuve est l’identité durable de l’arbre;
   RevisionPreuve est son état exact, avec arbre simple complet et nœuds
   propres. Un nœud appartient à une seule révision; parent/enfant dans la
   même révision, sans cycle; seuls les groupes ont des enfants.
4. **Usage.** Une UP valide désigne une occurrence, sa VersionActe et UNE
   révision exacte de Preuve. Ses sélections visent uniquement des nœuds de
   cette révision. La même révision peut servir plusieurs VersionActe.
   Aucun pointeur « dernière révision » dans un état historique.
5. **Modification isolée.** Une révision engagée dans un gel est immuable.
   Pour la modifier, copier l’arbre entier sous la même identité Preuve,
   conserver la filiation de révision et la carte des nœuds, puis repointer
   les seuls usages choisis d’une version modifiable. Même règle de
   détachement si une modification de brouillon affecterait des usages non
   ciblés. Ne pas copier fictivement les Email/PDF originaux.
6. **Clôture historique.** Le gel conserve révisions exactes, nœuds, chemins
   sélectionnés, états sources/citations utilisés, textes, examens, liens,
   renvois pertinents, cotes/sous-cotes, résultat et livrables. Les liens
   externes CF2 désignent une version cible figée et ses occurrences;
   ses fondements sont retrouvés par ses UP et révisions exactes. Une
   prémisse externe mutable doit être figée ou reprise explicitement avant
   le strict selon CF2. Un renvoi pertinent absent ou ambigu est signalé.
   Aucun renvoi entre preuves ni moteur d’inférence n’est ajouté à D01.
7. **Cotation.** À une révision calculée donnée : un document retenu, une
   cote principale; citation identifiée avec parent vérifié, sous-cote dans
   cette cote. Document sans citation : une cote, zéro sous-cote. Répétition
   d’usage et composition ne multiplient pas la cote principale du document.
   Bordereau/ResultatVersion communs; R04 notation/ordre encore à préciser.
8. **Gel atomique.** Recontrôler les entrées et protéger les relations lues
   avant finalisation. Aucun FIGEE publié incomplet; un candidat orphelin
   après panne est distinct du contenu figé. Hashes seuls insuffisants.
   La conservation immuable des décisions ExamenEditorial en L1-A ne doit
   pas attendre L5; elle ne verrouille pas les brouillons entiers.
9. **Deux concordances.** UC12 compare les paragraphes; UC17 compare les
   documents/cotes et citations/sous-cotes, sur l’union des états retenus.
   Elles partagent l’identification explicite du couple historique et les
   références conservées; aucun rapprochement par numéro/cote seuls.
10. **Juillet.** Référent : acte papier déposé le 24 juillet 2026 à 15 h 19;
    sources d’impression et `cotes.lock.json` dans l’archive intouchable
    `legal/depots/2026-07-24_initial/`, ancrée à `1f0af56`. Ne pas inventer
    une VersionActe, une révision de preuve ou un examen d’époque à partir
    du présent. Utiliser les captures disponibles avec provenance; marquer
    les lacunes. Pour les futures versions instrumentées, conserver et
    restituer les fondements exacts; l’absence passée reste une absence.
11. **Événements.** Notification, communication, dépôt sont des événements
    attestés, multiples et distincts du gel; ils ne changent pas le contenu.
    Pas de chaîne d’états exclusive FIGEE → DEPOSEE → COMMUNIQUEE.
12. **Mono-utilisateur.** Un seul utilisateur humain; rédacteur, relecteur,
    lecteur sont ses points de vue. Pas d’affectation d’équipe, quorum,
    approbation collaborative ou rôles nouveaux. Les onglets, tâches,
    doubles soumissions et reprises exigent toujours verrous, contrôle
    d’entrées et idempotence. Les validations B/PO sont le processus du
    projet, pas une fonctionnalité collaborative à ajouter à l’application.

## 3. Écarts constatés et corrections minimales

Les versions antérieures exactes sont [préservées](historique/2026-10-21_avant_coherence_transversale/README.md).
Les lignes localisent la source de l’écart et la conséquence, puis distinguent
la correction documentaire réalisée de la revalidation encore requise.

| ID / exigence | Localisation et risque avant correction | Correction minimale apportée / qualification | Revalidation nécessaire |
|---|---|---|---|
| CT-01 / A | D12, CF1; story01, plan01A/01B; aucun état transversal ni ERD Cause/Acte/versions : contexte possible mais cardinalités et non-retour de FIGEE non démontrés | États + ERD communs, critères TRV01A/01B, activité01. Mise en cohérence de la décision A; pas d’arbitrage sur la hiérarchie | Quatre vues 01A/01B/11, R06 pour parcours actif; L1-A puis L5/L6 |
| CT-02 / B | D01/D08/D12, INV12; stories03/04/07/11 : « Preuve entière verrouillée / copie » sans identité de révision. Risque de bloquer tout l’arbre logique ou d’utiliser implicitement sa dernière version | Distinguer Preuve/RevisionPreuve; UP → révision exacte, copie entière de révision; critères TRV03/04/07/11. Application de B; traduction physique proposée, non approuvée | Quatre vues 03/04/05P/07/11, cible UP/Noeud dans ERD/classes; L2/L5/L6 |
| CT-03 / B | CF2 et activité06 gardaient la version de prémisse sans expliciter le chemin vers ses révisions probatoires. Une copie partielle pouvait perdre le contexte historique externe | Conserver LienRedactionnel, version/occurrences cibles exactes et fondements via leurs UP. Pas de graphe inter-preuves ajouté; pas d’inférence. TRV06/11 | Vues 06/07/11, refus de prémisse externe mutable, stabilité du renvoi; L1-B, L2, L5/L6 |
| CT-04 / C | Cotation correctement définie dans UC08/09/16/17, mais pas reliée à une révision exacte de preuve dans une vue commune. Risque de calculer un résultat depuis un arbre courant modifié | ERD commun + rattachement des quatre compléments COT à TRV04/11. Principe inchangé; R04 reste technique | ERD/classes/séquences 04/08/09/10/16/17/18A, entrée commune ResultatVersion; L2 à L6 |
| CT-05 / D | Story12 générique E01, UC17 documentaire; couple juillet → modifiée et preuve exacte non tracés ensemble. Risque de livrer une seule concordance ou de fabriquer l’histoire manquante | UC12 parent, UC17 complément et critères TRV12/17 : deux sorties distinctes, même couple attesté, lacunes visibles. Application de D, aucun import historique prescrit | Quatre vues 12 complet / 17 / 18B, cartes N:M/archives; C0-B pour paragraphes, L6 pour ensemble |
| CT-06 / E | Acteurs génériques et R06 « branches » pouvaient laisser supposer plusieurs utilisateurs | Un humain, points de vue fonctionnels; branches éventuelles = variantes personnelles. Conservation de la concurrence technique. TRV01A-AC02 | Classes/responsabilités et scénarios de concurrence des UC touchés; R06 non résolu par cette clarification |
| CT-07 / méthode | Plan/registre contiennent des constats anciens « aucun approuvé / mandat à obtenir ». Risque de lire un journal daté comme état courant ou de transférer une approbation C0-A à C cible | Distinguer état courant, journaux historiques et revue C0-A référencée. Aucun changement des dossiers ou manifestes approuvés | Registre courant; aucune réouverture de C0-A par cette revue. B01 demeure régi par sa revue séparée |
| CT-08 / méthode | Séquences/classes/ERD locaux manquants pour les UC principaux; compilation des vues globales ne prouve pas ces correspondances | Cartographier ce qui est vérifiable et ce qui reste absent (§4), rattacher aux tickets UML existants | Les quadruplets et leur revue sémantique restent requis; pas de validation B complète accordée |

**Arbitrages :** A–E sont les exigences du mandat; aucune nouvelle décision
fonctionnelle nécessaire pour ces corrections. Les choix de stockage et de
contrainte sont des propositions techniques à justifier dans les dossiers.
R04 demeure notation/ordonnancement des sous-cotes; R06 demeure parcours et
brouillons actifs (plusieurs versions historiques sont déjà acquises).
R01/R02/R03/R05/R07/R08 gardent leurs seuls périmètres de l’avenant; ils ne
rouvrent ni cote du document ni zéro sous-cote sans citation. Aucun nouveau
use case, ticket ou processus de gouvernance n’est nécessaire.

## 4. Contrôle horizontal réellement possible

| Comparaison | Constat documentaire réalisé | Limite / suite opposable |
|---|---|---|
| État VersionActe ↔ ERD transversal ↔ activité01/11 | FIGEE irréversible; nouveau brouillon avec nouvelle identité; contenu figé unique, événements externes séparés | Séquences/classes/ERD locaux 01A/01B/11 encore absents; conformité d’exécution non démontrée |
| État RevisionPreuve ↔ ERD ↔ activités03/04/07/11 | UP vise une révision; nœud de cette révision; même révision réutilisable; copie entière seulement avant modification isolée | Contraintes physiques et verrouillage entre gel/repointage à détailler et éprouver en L2/L5 |
| Cotation ↔ UC08/09/16/17 ↔ ERD C-COT et C-TRANS | Même dépendance version/document/cote et citation/parent/sous-cote. C-COT montre les éléments résolus, C-TRANS les nœuds qui y conduisent | Les quatre dossiers COT n’ont pas leurs quadruplets; R04 ouvert; pas d’affirmation de cohérence locale complète |
| Séquences ↔ responsabilités de classes | Matrice d’opérations à respecter ci-dessous; les projections C0-A sont d’un autre périmètre et n’introduisent aucun Preuve implicite | Impossible de valider des séquences/classes cibles absentes. À contrôler opération par opération lors de leur production |
| Gel ↔ concordances paragraphes et pièces | Révisions, textes, numéros, identités, sources, cotes, sous-cotes et usages conservés explicitement; juillet traité comme référence attestée distincte | Les captures disponibles ne suffisent pas forcément à toutes les correspondances; lacunes affichées, aucun résultat de concordance réelle calculé ici |
| ERD locaux ↔ transversal | Les ERD C0-A approuvés protègent occurrences/Statement/correspondances; le transversal les replace dans une future version, sans changer leur contrat | Les relations Acte/RevisionPreuve/Cotation n’existent pas dans ces ERD locaux limités. Leur absence n’est pas une contradiction; aucun transfert d’approbation |

Responsabilités à vérifier dans les futures séquences/classes (noms d’opérations
indicatifs, **pas des API implantées**). Chaque opération doit avoir un
propriétaire identifié dans la vue de classes, des entrées révisées, un refus
atomique et les écritures exactes indiquées dans sa séquence :

| Opération logique | Responsable cible | Contrat d’entrée/sortie / UC |
|---|---|---|
| Créer Acte/VersionActe et document propre | act_manager; primitives neutres document_manager | Cause, origine éventuelle, révision contrôlée → nouvelle identité; 01A/01B |
| Créer/modifier/détacher une révision | proof_manager | Preuve, révision exacte, usages explicitement choisis → nouvelle révision complète si nécessaire et carte des nœuds; 03/07 |
| Choisir les appuis d’une occurrence | proof_manager; orchestration de reprise | VersionActe modifiable, occurrence, révision et sélections compatibles → UP; 04/05P/07 |
| Résoudre documents, citations et cotes | autorité ResultatVersion / bordereau; adaptateurs sources | mêmes entrées versionnées → résultat commun et chemins d’usage; 08/09/10/16/18A |
| Finaliser le gel | act_manager, orchestration et protections des gestionnaires | candidat stable + stockage garanti + clôture pertinente → contenu immuable; 11 |
| Comparer deux états historiques | lecteur éditorial neutre / lecteur documentaire | couple attesté → paragraphes (12), documents/cotes/citations (17); aucune écriture des états comparés |
| Consigner un événement effectif | service d’événements de l’acte | version et livrables identifiés, faits attestés → événement séparé; 19 |

La reprise et le gel orchestrent les gestionnaires; document_manager n’importe
pas proof_manager. Un lecteur E01/UC12 peut fonctionner sans Preuve ni L2.
Les décisions ExamenEditorial restent conservées même si leur application
courante devient invalide ou si une occurrence autorisée est supprimée.
Leur immutabilité L1-A/C0-B et la fermeture globale d’un gel L5 sont distinctes.

## 5. Vérification et limites

Les scénarios **TRV:T01–T13** sont définis dans la matrice existante §13,
rattachés aux critères et lots. Ils sont **NON EXECUTES**; ils complètent,
sans remplacer, les 38 NR/CF3, les 91 critères V2, les suites COT et A/E01.
Les activités A0 révisées ne sont pas les quatre vues contractuelles locales.
Les résultats effectivement obtenus pour les sources, rendus, liens et
conservation des fichiers sont consignés au §6 après vérification.
Aucun test applicatif, aucune requête ORM et aucun test sur PostgreSQL réel
ou jetable ne fait partie de cette livraison documentaire.

### Correspondances des vues locales C0-A disponibles

Lecture documentaire des sources, sans modification ni nouvelle approbation :

| Séquence existante | Classe / responsabilité correspondante | Portée constatée |
|---|---|---|
| UC13 SEQ-EDIT/AVANT/COPIE/ASSOC/APRES et FRESH | produced_views.ajax_edit_node → concordance.detacher_pour_edition; création Statement, LibraryNode, VersionTexte.capter; lecteurs etat_courant | Isolement d’une occurrence et fraîcheur sur son Statement porté; aucune révision Preuve ni gel global ajouté |
| UC14 SEQ14-SERVICE/GARDE/ARCH/REL/DELETE | concordance.supprimer_occurrence; protection.verifier_suppression_noeud/archivabilite/archiver_noeud; NoeudArchive et ExtremiteCorrespondance | Archive avant retrait, frontière atomique, aucune purge de Statement/VersionTexte; aucune preuve nouvelle de conformité du code concurrent |
| UC15 SEQ15-PAIR/VALID/DIAG/RESULT/STRICT | concordance.appuis_dorigine; LectureAppuis/DiagnosticAppui/ErreurContexteLecture; export_concordance et contrôles EX | Couple/type qualifiés, appuis et anomalies conservés, strict après collecte; lecture historique distincte d’appui courant |

Ces correspondances sémantiques confirment des responsabilités compatibles
dans les profils locaux disponibles; elles ne constituent ni une comparaison
automatique de signatures ni une nouvelle validation des dossiers.
Les légendes historiques « proposé » présentes dans les vues conservées
ne supplantent pas les décisions d’approbation inscrites au registre.

## 6. Résultats effectivement obtenus

Contrôles documentaires du 21 octobre 2026, sur les fichiers présents dans
le dépôt de travail; aucun résultat applicatif ajouté à ceux des lots.
[Empreintes des vues](modele_global/manifest_transversal_c_2026-10-21.json),
[relevé des contrôles](modele_global/controles_transversal_c_2026-10-21.json).

- **10 sources PlantUML** : trois nouvelles vues transversales et sept
  activités révisées, compilées en SVG avec PlantUML **1.2026.8 / 149874a**,
  sortie finale **0**. Conversion des dix SVG en PNG par `rsvg-convert`,
  sortie **0**. Inspection visuelle des dix PNG; les boucles d’état
  initialement superposées ont été remplacées par des transitions internes
  lisibles avant livraison. Les trois modèles sont proposés, pas approuvés.
- **91 lignes de critères V2** et **38 lignes NR/CF3** exactement conservées,
  comparées aux copies antérieures. **44 tickets** et **22 statuts de
  dossiers** inchangés. Treize critères TRV définis dans les UC existants et
  treize scénarios TRV planifiés, sans exécution fonctionnelle.
- **32 copies historiques** conformes à leurs empreintes; **207 fichiers**
  existants des périmètres protégés inchangés, y compris les trois dossiers
  C0-A approuvés, leurs archives, les sous-cas citations et les modèles
  globaux antérieurs. Les **cinq manifestes actifs** concordent encore avec
  leurs fichiers (26, 29, 29, 26 et 29 entrées selon le dossier).
- Liens locaux nouveaux vérifiés; absence de cible manquante. Les copies
  historiques gardent leurs anciens chemins relatifs d’origine et ne sont
  pas publiées comme documents actifs.
- **456 fichiers Python** identiques au relevé de début de mandat; contrôle
  complémentaire des **670 fichiers du socle** du relevé documentaire
  précédent : aucune différence. Aucun fichier applicatif ou migration
  modifié. Aucun import Django, test PostgreSQL, accès réel ou opération Git
  de publication dans ce travail.

Commandes de rendu réellement employées, avec les dix chemins explicites :
`plantuml -tsvg -failfast2 <sources.puml>` puis, pour chaque source compilée,
`rsvg-convert --background-color=white -o <rendu.png> <rendu.svg>`.
Le contrôle des empreintes a comparé les SHA-256 aux copies préservées et
aux cinq manifestes existants; les identifiants/critères ont été comparés
sans renumérotation. Le relevé JSON décrit chaque contrôle et ses écarts.
Ce relevé technique n’est ni un registre d’approbation ni un banc de tests
métier. Les scénarios TRV/COT restent **NON EXECUTES**.

## 7. Suite limitée et points à décider

La clarification documentaire ferme les écarts d’identité et de révision
CT-01–CT-06 au niveau des contrats. Restent à justifier dans les dossiers
locaux les contraintes physiques, la clôture des références et les séquences
atomiques; CT-08 demeure une limite explicite, pas une conformité acquise.
Les corrections actuelles n’exigent pas de nouveau use case ni de lot.
R04 notation/ordre et R06 parcours actifs restent à préciser dans leur
périmètre; les autres réserves de l’avenant restent celles des chemins concernés.

La suite de conception utile est de compléter les vues locales des fondations
01A/05E de L1-A, avec le contrat transversal applicable approuvé, puis celles
de 03/04/05P pour L2 selon le plan. Cela ne doit pas retarder la clôture de
C0-A, examinée séparément. Aucun développement, ouverture de lot suivant ou
modification de l’environnement A n’est proposé comme déjà autorisé.

