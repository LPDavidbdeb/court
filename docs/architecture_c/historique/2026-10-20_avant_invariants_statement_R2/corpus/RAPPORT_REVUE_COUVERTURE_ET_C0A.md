# Revue de couverture du backlog et préparation de C0-A

**RC-C0A-2026-10-20-R1 — mandat de revue du 20 octobre 2026.**

Le backlog couvre les principales capacités de C, mais **sa complétude n’est
pas encore démontrée pour le constat d’absence, la recherche de sources et
l’exposition explicite des garanties des citations héritées**. Ces manques
se corrigent dans les use cases existants. Aucun nouveau ticket ni nouvelle
story n’est nécessaire : BLC-R2 conserve 44 tickets et 22 use cases.

**C0-A est compatible textuellement avec `515666e`, mais son patch présente
une anomalie fonctionnelle confirmée, C0A-REV-01.** Il n’est pas prêt à intégrer.
UC-C-13 est soumis à approbation dans sa version C0A-UML-R1, après validation
documentaire B; UC-C-14 et 15 sont préparés et restent en revue. Aucun résultat
Django/PostgreSQL n’est réexécuté sur le nouveau socle.

## 1. Sources et sens du diagnostic

Références actives : [décisions](DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md),
[avenant](AVENANT_ARCHITECTURE_C.md), [matrice](MATRICE_COUVERTURE_V2_C.md),
[plan](PLAN_MODELISATION_UML.md), [protocole](PROTOCOLE_VALIDATION_UML.md),
[registre](registre_validation.md). Sources détaillées confrontées :
[validation fonctionnelle initiale](VALIDATION_FONCTIONNELLE_ARCHITECTURE_C.md)
§§A.3/B/C.2 et VF05–VF13, [conception initiale](../modele_preuve/CONCEPTION_PREUVE.md)
§§10/11/15/16/17, [stories initiales](../modele_preuve/diagrammes/user_stories_architecture_c/README.md),
V2 conservée, rapport/patch C0-A et code du socle nommé. Les anciennes options
de raisonnement de la conception initiale ne supplantent pas D12/CF2.

« Entièrement couverte » désigne une capacité représentable et spécifiée dans
les contrats, sans attester son implantation. « Partiellement couverte »
signale un critère ou un raccord manquant. « Absente » signifie aucun support
identifié. « Indécidable » désigne un choix encore non approuvé. Les résultats
de tests historiques restent attribués à leur environnement d’origine.

| Question | Diagnostic | Preuve et reste à traiter |
|---|---|---|
| A — Raisonnement composé | **Entièrement couverte au niveau contractuel** | D01/D02/D03/D11/D12 et CF2/CF3; validation initiale B et C.2, VF05/VF11–VF13. Ajouter une contre-épreuve transversale ciblée, sans nouveau modèle. |
| B — Allégation d’absence | **Partiellement couverte** | L’intention existe dans la conception §10 et l’arbre §11; portée/limites sont prévues, mais aucun AC ne rend obligatoire un périmètre d’examen vérifiable. Complément COV-B-AC01/02. |
| C — HERITE / PHRASE | **Partiellement couverte** | Le fournisseur et l’isolation sont explicites; le traitement visible des HERITE dans la consultation C n’est pas assez spécifié. Strict PHRASE décidé par INV14/§9.1; proposition de consultation qualifiée à approuver. |
| D — Dépendances | **Partiellement couverte dans R1; clarifiée dans R2** | Le graphe d’exécution est acyclique; des contrats de 17/18/11 figuraient comme préalables sans qualifier leur nature. Tableau §4 et contrôle topologique conservé. |
| E — Parcours complet | **Partiellement couverte** | Recherche/retour au contexte de rédaction et relais des diagnostics insuffisamment explicites. Le reste réutilise les contrats présents; tableau §5. |
| F — Socle et intégration | **Compatibilité statique établie; autorité finale indécidable sans décision utilisateur** | Aucun chevauchement de fichiers, `git apply --check` réussi. Anomalie du lecteur indépendante de A; nouvelle validation dynamique et destination de promotion à autoriser. |

Les critères complémentaires et leurs scénarios sont définis une seule fois
dans la [matrice §9](MATRICE_COUVERTURE_V2_C.md#9-compléments-de-couverture-du-mandat-de-revue-r2).
Ils sont proposés pour approbation, sans clôture présumée des DEC-R01–R08.

## 2. A/B — Raisonnement composé et constat d’absence

Pour le cas danse, créer quatre occurrences rédactionnelles distinctes :

| Proposition de l’exemple | Représentation et appuis | Limite à préserver |
|---|---|---|
| P1 : participation aux cours certains soirs | Statement dans LibraryNode; UP1 avec les seuls éléments de calendrier/communication retenus pour cette portée | Les périodes et jours non établis restent qualifiés. |
| P2 : ces cours nécessitaient une absence du domicile | Autre occurrence; appuis propres UP2 si choisis; lien déclaré vers P1 et réserves explicites | P1 n’attribue aucun appui automatiquement à P2. |
| P3 : pendant certaines absences, le père prenait les enfants en charge | Occurrence et UP3 propres, éléments de prise en charge et témoignages/limites rédigés dans leur contexte | Absence de la mère et prise en charge du père sont deux propositions distinctes. |
| P4 : contribution à une participation régulière aux responsabilités | Conclusion intermédiaire ou générale dans la rédaction; dépendances déclarées vers P1/P2/P3; UP4 uniquement si un appui direct est expressément choisi | Le lien de dépendance ne certifie pas la conclusion et n’importe pas les sélections des prémisses. |

02 organise propositions, prémisses, conclusions et réserves; 03 organise les
éléments sourcés; 04 sélectionne; 05P porte portée et décision d’appui; 06
enregistre RENVOI/DEPENDANCE_DECLAREE sans moteur d’inférence. 07 reprend le
bloc avec contexte et décisions explicites. Une conclusion peut avoir zéro
UP et des dépendances déclarées : cela n’en fait pas une conclusion
automatiquement confirmée. Réécriture et copie déclenchent les contrôles de
fraîcheur pertinents. Cette construction est déjà montrée dans la validation
initiale, notamment B.1–B.3 et C.2; COV:T-A01 la vérifie transversalement.

Pour une allégation négative, la liste vide d’appuis ou `SANS_APPUI` ne constitue
pas un constat documentaire d’absence. Complément minimal proposé : conserver
avec la portée de l’usage un **protocole d’examen** contenant les identités et
états du corpus, pages/sections examinées, question recherchée, méthode utile,
auteur/date et limites. L’UP sélectionne les documents/passages réellement
examinés et leur contexte consultable, sans fausse citation représentant un
texte absent. Le protocole est une valeur du contexte d’examen, pas une
nouvelle source ni une entité Démonstration. Sa persistance exacte sera
justifiée dans l’ERD de 04/05P, et capturée au gel de 11.

Exemple synthétique : « Le document D, état H, pages 1–16 relues dans leur
ensemble, ne contient pas l’allégation X selon la question Q ». Une recherche
plein texte sur OCR incomplet ne justifie pas ce constat exhaustif; le champ
de conclusion doit alors exprimer cette limite. Changer H impose réexamen pour
un nouvel usage, sans effacer l’ancien constat. L’absence documentaire ne
devient jamais une preuve générale d’inexistence du fait. Ce complément relève
de L2, des capacités sources de L3-A et de sa conservation en L5.

## 3. C — Usage des 394 HERITE et de PHRASE

Le mandat atteste 268 HERITE Email, 126 HERITE PDF et une PHRASE certifiée.
Le code de `515666e` confirme les gestionnaires `objects` filtré HERITE,
`phrase_objects` filtré PHRASE, `all_objects` sans filtre, ainsi que les bornes,
trois empreintes, `effective_certification` et `derived_from`. Ces nombres ne
sont pas recomptés sur la base réelle par B.

| Usage envisagé | HERITE | PHRASE |
|---|---|---|
| Identité et usages historiques | Préserver `(modèle qualifié, PK, régime)`, texte disponible et rattachements existants | Identité distincte, antécédent conservé s’il existe |
| Consultation / organisation analytique C, proposition | Référence historique explicitement qualifiée; source et contexte ouvrables; ancrage/certification absents affichés comme tels | Afficher le résultat effectif des contrôles, y compris une invalidation |
| Nouveau verbatim strict C | **Non admissible comme citation certifiée sous le contrat actuel**; le simple maintien des anciens usages n’accorde pas cette garantie | Seulement si régime PHRASE, bornes, trois empreintes et certification effective valides au moment du rendu |
| Restitution d’un ancien livrable conservé | Restituer les octets et garanties historiques, sans les présenter comme une nouvelle certification | Même règle de restitution; distinguer l’état conservé et la disponibilité courante du fournisseur |

Les **394 peuvent donc rester identifiables et consultables**, et servir de
repères pour retrouver leurs sources dans le parcours analytique proposé.
Cela n’autorise pas l’utilisation automatique des 394 verbatims dans le strict
du second pont. Pour citer à nouveau un passage : obtenir chez A une PHRASE
valablement certifiée, ou sélectionner la source originale via un autre
adaptateur vérifié pour un usage différent qui n’attribue pas une certification
PHRASE au vieux verbatim. Aucun traitement en masse ou conversion n’est mandaté.

`derived_from` exprime une filiation, pas une certification rétroactive.
Une GFK et `all_objects` ne dispensent jamais du contrôle de régime/capacité.
L3-B consomme A; il ne modifie ni ses gestionnaires ni ses migrations. La
politique de présentation analytique des HERITE, ajout ciblé à 03/04/08, est
soumise à l’utilisateur (COV-C-AC01/02); le refus du strict non certifié reste
l’invariant actuel, et ne rouvre pas le régime A.

## 4. D — Trois graphes, sans cycle d’exécution

| Lot consommateur | Dépendances d’exécution livrées | Contrats à définir avant sa conception/implantation | Validation ultérieure |
|---|---|---|---|
| C0-A | Socle A proposé `515666e`, après mandat adapté | 13/14/15, pas de nouveau schéma | Rejouer E01 et régime A actuel; C0A-REV-01 |
| L1-A | C0-A atterri | 01A/05E; R06; droits/examens | Transition complète en C0-B; gel global en L5 |
| C0-B | L1-A atterri | 12, diagnostics et transition | Appuis C en L2; non-régression finale L6 |
| L1-B | L1-A; C0-B avant exécution dans l’ordre retenu | 02/06 et copie neutre de 07; état de version | Reprise probatoire L2, contrôle des dépendances au gel L5 |
| L2 | L1-A/B, C0-B | 03/04/05P/07; RefSource; portions citation/gel utiles à une reprise | Sélections rendues L3/L4; copie depuis gel L5/L6 |
| L3-A | L2 | 16/09; interfaces 10/17/18A : identité/composition, résultat, comparaison et manifeste; pas leurs services complets | Concordance figée 17 en L6; fichiers 18A en L4; gel 11 en L5 |
| L3-B | L3-A et fournisseur A versionné | 08 : régime, ancrage, certification et navigation | Rendu intégré L4 et revalidation L6 |
| L4 | L3-A; L3-B pour PHRASE, également prédécesseur dans l’ordre proposé | 08/10/18A; interface de candidat, reprise et finalisation 11; R08 sur ce contrat | Gel effectif et pannes finales L5; restitution complète L6 |
| L5 | L1–L4 pour le périmètre gelé | 11; lecture historique 18B et clone 01B définis sans attendre leurs parcours complets; R08 | Parcours 01B/17/18B/19 et récupération intégrée L6 |
| L6 | L1–L5, capacités sources réelles et référence autorisée | Parcours d’intégration et récupération C | Toutes les suites intégrées et conditions d’atterrissage |

Le contrôle topologique du graphe d’exécution confirme un ordre possible :
`C0-A, L1-A, C0-B, L1-B, L2, L3-A, L3-B, L4, L5, L6`.
Les références de L3-A à 17/18A ou de L4 à 11 sont des dépendances de **contrat**,
pas une exigence d’implanter L6/L5 avant L3-A/L4. La préparation du fichier
candidat ne dépend pas de la finalisation du gel, tandis que le gel consomme
le candidat. Aucun arc d’exécution L6→L3-A ou L5→L4 n’est introduit.

Un contrat partagé doit être nommé/versionné et examiné dans les dossiers
touchés; il ne nécessite pas l’implantation ou l’approbation présumée du use
case futur entier. Les quatre vues du use case effectivement implanté restent
obligatoires. Les reprises partielles doivent nommer leur périmètre de contrat
sans prétendre livrer toutes les variantes CF3 avant les lots intégrés.

## 5. E — Parcours transversal et passages de relais

| Étape / responsable | Données reçues → produites | Choix laissé à l’utilisateur / diagnostic |
|---|---|---|
| 1. 01A : contexte | Cause et nature d’analyse/acte → Acte/VersionActe + Document de travail | Choisir contexte et branche selon R06; aucun dépôt fictif |
| 2. 02, édition 13 | Document/occurrence → propositions et structure numérotée | Rédiger, ordonner, expliciter prémisses/conclusions/réserves |
| 3. 03, sources L3-A/B | Contexte de rédaction + requête de recherche → candidats RefSource qualifiés et aperçu/contexte | **Complément manquant R1 : sélecteur intégré et retour au point de rédaction**, COV-E-AC01; ne pas demander une PK brute via script |
| 4. 03/04 | RefSource choisi + Preuve organisée → UP et SelectionPreuve sur la cible | Choisir les éléments, la portée et le contenant; aucun héritage automatique |
| 5. 05P/06 | Texte actuel + sélections + limites → examen d’appui et liens déclarés | Examiner réellement l’appui; choisir le traitement des réserves/constats négatifs; pas de vérité déduite |
| 6. 08 | Sélections/capacités fournisseur + VersionTexte → composition et insertion ancrées | Choisir segments, omissions et emphases; refuser une garantie indisponible |
| 7. 04/16 | Usages de la version + choix analytique/production → identités/compositions retenues | Choix explicite R05 et R01/R02/R04; un filtre de vue n’exclut pas une pièce |
| 8. 09 | Pièces retenues, dates vérifiées, profil → ResultatVersion et cotes CHRONO_VERSION | Résoudre A_DATER et ambiguïtés; aucune ressaisie de cote |
| 9. 10/18A | Même révision ResultatVersion → texte, bordereau, cahier, fichiers candidats, manifeste | Lire les diagnostics et revenir au point concerné; aucun transport manuel entre générateurs, COV-E-AC02 |
| 10. 11 | Candidat cohérent + fournisseurs recontrôlés → contenu et fichiers figés | Décider de figer; gel distinct d’une communication; refus/panne sans publication partielle |
| 11. 01B/07/12/17/18B | État figé → nouveau brouillon, filiation, concordance de pièces et restitution de l’ancien | Choisir les reprises et examiner les changements; aucun appui reconduit automatiquement |

Après les ajouts ciblés, aucune étape n’exige une nouvelle story. La recherche
réutilise les catalogues disponibles via une interface explicite de 03; aucun
nouveau moteur de recherche sémantique universel n’est prescrit. En L2, le
sélecteur traite les sources disponibles et les références qualifiées; les
adaptateurs de production de L3-A/B complètent ensuite leurs capacités, sans
créer un cycle d’exécution. Les choix de fond et examens humains restent des
opérations prévues, pas des ressaisies techniques cachées.

## 6. F / TRANS-01 — Compatibilité, socle et destination proposés

Constats en lecture seule, détaillés dans les
[preuves JSON](lots/C0-A/PREUVES_REVUE_DOCUMENTAIRE.json) :

- P6 `212a7feee81aef46a5b43d36e8eeafe0f8870064` est ancêtre de
  `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`; cinq commits les séparent.
- Le diff P6→515 touche 14 fichiers : fournisseur/commandes/tests de régime,
  modèles/admin Email/PDF, deux migrations 0010, plan de A et scripts de A.
  Le patch C0-A touche huit autres fichiers; intersection vide. Ces huit
  fichiers sont identiques octet pour octet aux blobs P6.
- `git apply --check docs/architecture_c/lots/C0-A/C0A_DIFF_COMPLET.patch`
  réussit, code retour 0. Le patch n’est pas appliqué. Ses huit sources
  reconstruites **en mémoire** passent l’analyse syntaxique et correspondent
  aux huit empreintes Git du diff; aucun module Django n’est importé.
- Les services C0-A filtrent le type Statement et le couple documentaire;
  ils n’appellent pas les nouveaux services PHRASE. Les nouvelles GFK et
  capacités de A exigent toutefois les contre-épreuves de régime/type et la
  non-régression sur `515666e`, pas seulement sur P6.

**Socle technique recommandé pour les prochaines validations : `515666e`
complet ci-dessus**, dans une copie indépendante avec configuration synthétique
et PostgreSQL jetable, en conservant P6 comme référence du diff d’origine.
Le mandat actuel autorise cette proposition et sa vérification statique; il
n’autorise ni développement ni application du patch. La référence de départ
du futur mandat doit être explicitement approuvée.

**Destination proposée, sans création :** branche de lot
`review/c0a-515666e`, puis branche d’intégration C dédiée
`integration/architecture-c` issue du même socle, toutes deux à autoriser.
Ne pas déplacer `integration/quote-regime-step1` ni P6. La branche réellement
déployée demeure `epic/E01-numerotation-concordance`. L’utilisateur doit fixer
la promotion autorisée vers cette branche et l’application de la condition
de fusion finale dans `main` du processus. Aucune convergence main/epic n’est
décidée ici; tant que ce circuit n’est pas autorisé et accompli, C0-A ne peut
être déclaré atterri. Ce point de gouvernance ne change pas le graphe métier.

## 7. C0A-REV-01 et conditions de passage

Le lecteur du patch lève `ValueError` dès qu’une extrémité est absente,
archivée, du mauvais Document ou de type incorrect. Dans `_ligne`, le catch
fixe alors `origines=[]`. Les appuis valides déjà parcourus ou restant à lire
sont perdus pour cette lecture. Les tests du patch couvrent le filtrage entre
deux origines, une anomalie seule et une archive seule, **pas le mélange valide
et invalide d’un même couple**.

La [contre-épreuve sans base](lots/C0-A/CONTRE_EPREUVE_LECTEUR_SANS_BASE.json)
exécute la fonction exacte reconstruite en mémoire avec des doubles : valide
seul → P-5; valide puis mauvais type, ordre inverse ou valide puis archive →
exception. Le remplacement par liste vide est établi par lecture du catch
export; il ne s’agit pas d’un test HTTP/ORM/PostgreSQL.

Correction proposée dans [UC-C-15](use_cases/UC-C-15/specification.md) : séparer
erreur globale de couple et anomalies locales; conserver les appuis valides et
les diagnostics identifiables. L’export ne doit pas effacer les premiers en
affichant les seconds. Une lecture incomplète ne vaut pas validation stricte.
Périmètre de correction à soumettre à A **après autorisation** :
`document_manager/concordance.py`, `document_manager/export_concordance.py`,
`case_manager/test_e01_cotes_concordance.py`; tout autre fichier serait justifié
avant modification. **Le patch conservé est inchangé.**

Conditions pour demander l’intégration : approbation de 13, fin de revue puis
approbation de 14/15 et du contrat des anomalies, mandat de correction A avec
fichiers autorisés et socle `515666e`, correction de C0A-REV-01, tests actuels
et nouveaux cas mixtes sur PostgreSQL jetable, revue de conformité indépendante,
plan de récupération C préservant A, destination Git et étapes de promotion
explicitement décidées, puis six preuves d’atterrissage du processus.

## 8. Livrables et contrôles de cette intervention

- Matrice révisée avec critères complémentaires localisés; 91 libellés V2 et
  38 scénarios NR/CF3 conservés.
- [Backlog R2](BACKLOG_ARCHITECTURE_C.md), toujours 44 tickets; changements
  expliqués dans son journal, aucun DEC-R clos sans décision.
- [Modèle global G-C0A-R1](modele_global/README.md) : ERD et classes, périmètre
  C0-A seulement. Les relevés observés P6 restent intacts.
- Dossiers [13](use_cases/UC-C-13/specification.md),
  [14](use_cases/UC-C-14/specification.md),
  [15](use_cases/UC-C-15/specification.md), chacun avec quatre vues, critères,
  traçabilité et validation distincte. Seul 13 reçoit l’attestation B complète
  à ce stade; aucune approbation utilisateur n’est présumée.
- TRANS-04 : traçabilité fine C0-A dans ces dossiers, conservation de la
  couverture globale et des scénarios dans la matrice; les autres dossiers
  n’acquièrent aucune validation par cette intervention.

Les sources sont compilées avec PlantUML 1.2026.8, rendues en SVG et contrôlées
visuellement via leurs PNG conservés. Les commandes, empreintes et limites
figurent dans les validations de dossiers. Les contrôles statiques et la
contre-épreuve en mémoire sont distingués des tests applicatifs **NON EXECUTES**.

L’intégration n’est donc pas à autoriser en l’état. **UC-C-13 peut être soumis
à approbation de conception**, sans lui attribuer les garanties de L1-A, C0-B
ou L5, ni approuver le patch entier par extension.

Les [contrôles finaux de livraison documentaire](lots/C0-A/CONTROLES_LIVRAISON_DOCUMENTAIRE.json)
vérifient notamment les 91 libellés V2, les 38 affectations NR/CF3, les 44
tickets, les 22 UC, les manifestes et les liens locaux. Les empreintes de
670 fichiers suivis hors `docs/` et `legal/` sont identiques au relevé de
départ, et le patch C0-A garde son empreinte. Les copies antérieures sont
vérifiées octet pour octet; le README d’origine porte le nom distinct
`README_ARCHITECTURE_C.md` dans l’archive pour laisser place à son index.
