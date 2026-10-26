# Avenant à l’architecture C — rédaction V2 et CHRONO_VERSION

**Version documentaire : C-COT-2026-10-21-R1. Livrable A actualisé.**

Complément fonctionnel décidé par le Product Owner : [cote du document / sous-cotes des citations](references/DECISION_PO_COTATION_DOCUMENT_CITATIONS_2026-10-21.md), [traduction ERD](MODELE_TRANSVERSAL_COTATION.md). Les modalités antérieures sont relues avec cette décision, sans autorisation de développement.

Autorité : [mandat utilisateur](references/MANDAT_CONSOLIDATION_UML_2026-10-20.md), notamment §§2–5 et 9–10. La décision de principe D05 et les quatre vues UML obligatoires viennent de ce mandat. Les modalités recommandées ci-dessous restent soumises à l’approbation de leur dossier de conception. Aucun développement n’est autorisé par cet avenant.

## 1. Analyse d’impact et décisions intégrées

| Sujet | État consolidé | Effet |
|---|---|---|
| D05 | **APPROUVÉE UTILISATEUR pour le principe CHRONO_VERSION** | Chaque version cote les documents sources retenus et sous-cote leurs citations; identités et associations exactes conservées au gel |
| Autorités C | Conservées | Cible rédactionnelle → UtilisationPreuve → SelectionPreuve → élément → source; 0..N usages par cible, une révision exacte de Preuve et des sélections explicites par usage |
| Démonstration autonome | Non introduite | Aucun second arbre de conclusions ou moteur de validation; un regroupement rédactionnel utilise les occurrences et usages existants |
| Pièces produites | Contrat complété, modalités résiduelles signalées | Séparer identité de source, identité logique de pièce, composition exacte, cote locale et capture historique |
| Concordance documentaire | Exigence intégrée | Complément distinct de la filiation rédactionnelle et des examens d’appui |
| Production et gel | Exigences renforcées | Un ResultatVersion, manifestes de composition/fichiers et protocole base + stockage |
| Gouvernance UML | **Obligatoire par mandat** | Quatre vues par use case, validation B, puis approbation utilisateur et préalables avant implantation |
| Unité de livraison | Lot maintenu | Les dossiers de use cases sont des préalables au mandat du lot, pas une autorisation de lancer le lot suivant |

Les statuts antérieurs de D01–D12 et CF sont relus avec l’approbation utilisateur déjà donnée, puis avec ce nouveau mandat. D07 et CF4 restent conditionnelles aux sources. La révision du [registre](DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md) indique les effets nouveaux; son état antérieur est conservé en historique. Les [sources V2](references/EPIC_REDACTION_V2_SOURCE.md) sont intégrées par traçabilité, sans epic concurrent.

## 2. D05 : domaine d’application et invariants

### 2.1 Règle décidée

Pour une version de travail `v`, soit `P(v)` l’ensemble des documents sources effectivement retenus pour sa production, après résolution des usages, citations et compositions. Le classement approuvé pour le profil de `v` produit une suite déterministe. La cote principale de chaque document est locale à `v`, sans devenir son identité intrinsèque. Chaque citation conserve sa propre identité et son document parent; sa sous-cote est rattachée à la cote de ce document dans `v`. Aucune citation ne reçoit une cote principale autonome.

Insertion, retrait, remplacement ou correction d’une donnée pertinente au classement impose une nouvelle évaluation du résultat de travail. Les filtres d’interface ne modifient pas `P(v)`. Le numéro d’un paragraphe et la cote d’une pièce demeurent deux responsabilités séparées.

Le gel conserve les associations **(version, document source, cote)** et **(version, citation, document parent, sous-cote)**, leurs états/compositions exacts, paramètres et liens occurrence → utilisation → sélection. Ces dépendances fonctionnelles ne prescrivent pas de clés primaires physiques. Il n’existe aucune mise à jour ultérieure de ce tuple dans cette version. Une nouvelle version peut réutiliser la pièce et lui attribuer une autre cote.

Une référence active désigne la version utilisatrice, l’identité du document et, si elle vise une citation, l’identité propre de celle-ci et son parent. Le libellé est résolu depuis son ResultatVersion. Un libellé `P-1` isolé de son contexte ne permet pas une résolution entre versions. Un fichier nommé d’après sa cote est également rattaché à une version dans son manifeste et son espace de publication.

### 2.2 Histoire de juillet et portée de l’exception

Le mandat modifie explicitement la portée de la permanence globale pour les **nouveaux bordereaux CHRONO_VERSION**. Il ne réaffecte aucune association du dépôt de juillet, ne reconstruit aucun examen ancien et ne transforme pas l’ancien registre en table de travail.

La consigne historique « prochaine cote P-107 » conserve sa fonction pour le registre historique; elle ne devient pas le compteur de toutes les nouvelles versions. Les anciens textes méthodologiques sont lus avec cette exception explicite, sans modifier les archives. Une nouvelle version peut porter `P-1` pour une autre pièce, à condition que les deux contextes soient identifiés et que la concordance les distingue.

L’import historique conserve les associations documentées, leur provenance et leurs lacunes. Il n’exige pas une composition numérique entièrement connue pour inventer une identité avec l’acte papier. Une lacune demeure un diagnostic; la réexportation ne fabrique pas les fichiers ou validations absents.

### 2.3 Dates, égalités, fragments et sous-cotes

D06 reste applicable : dates métier vérifiées, précision et provenance explicites; pas de date d’import utilisée silencieusement. Le premier profil déjà recommandé distingue jour seul et instant fiable, conserve le fuseau de comparaison et départage de façon déterministe. `A_DATER` n’est pas une pièce atemporelle; une donnée requise non établie bloque le strict concerné.

Pour les pièces composites, le choix de la date de classement et le dernier départage demandent R03 ci-dessous. Aucun choix automatique « première date », « dernière date » ou date de création technique n’est ajouté ici. Une correction de date peut recoter un brouillon; elle ne modifie pas les paramètres historiques figés.

D04 conserve l’occurrence source complète d’un acte comme unité de fragment. Numéro imprimé, identité du fragment, ordre de composante et sous-cote sont distincts. Le principe cote principale du document / sous-cote de ses citations est décidé. R04 porte seulement sur notation et ordre technique par type. L’ordre des segments dans une composition ne détermine pas à lui seul l’ordre de sous-cotation du bordereau.

## 3. Pièce produite et composition documentaire

### 3.1 Définitions formelles

Une **source** est un objet probatoire original identifié par un modèle qualifié (`application.modèle`) et sa clé primaire. Cette identité ne garantit pas à elle seule l’immutabilité de son texte ou de son fichier : l’état utilisé doit aussi être conservé et vérifié.

Un **élément probatoire** est l’objet ou passage référencé par une feuille de preuve. Son utilisation désigne ses sélections, sa portée et la cible rédactionnelle. Plusieurs utilisations peuvent mobiliser le même élément sans dupliquer la source.

Une **pièce produite** décrit une unité ou composition documentaire retenue par les usages de production. Son identité logique, son titre et son fichier restent distincts de la cote. La cote principale est cependant portée par le **document source**, identifié par modèle qualifié + PK, et les citations sélectionnées ont leurs propres sous-cotes. Source entière, extraits et assemblages conservent leurs compositions sans créer de cote principale autonome pour les citations.

Une **composition exacte** décrit ce que cette unité réunit dans un état donné. Son manifeste comporte :

- identités et états sources conservés; original ou reproduction utilisé, empreintes et certification pertinente;
- liste **ordonnée** des composantes et identifiants de fragments; bornes et conventions de repérage lorsque nécessaires;
- contenants explicites et appartenance vérifiée, notamment Photo→Event;
- choix de sélection et transformations documentaires significatives, avec limites et provenance;
- version du format de manifeste et empreinte canonique, indépendante de la cote et du nom de fichier.

L’empreinte de composition n’inclut pas une cote recalculable : sinon une recotation ferait artificiellement changer la matière documentaire. Les octets rendus, leur empreinte et la recette de rendu sont conservés dans les artefacts. Deux rendus de mise en page différente ne prouvent pas nécessairement un changement de composition; inversement, un même nom de fichier ne prouve aucune égalité.

L’**identité logique** permet la réutilisation et la filiation. L’**identité de composition** permet la comparaison exacte. Les deux doivent pouvoir être conservées ensemble au gel. R01 détermine la politique de continuité logique lors d’un remplacement de composantes; ce n’est pas décidé par le hash.

### 3.2 Déduplication et production

Les règles minimales suivantes découlent de C et du mandat :

1. Plusieurs chemins d’usage ou citations du même document ne créent pas plusieurs cotes principales dans une version; tous les chemins restent traçables.
2. Ni titre égal, ni cote égale, ni texte semblable, ni PK numérique sans modèle ne permettent une fusion.
3. Un document apparaissant dans deux compositions différentes ne fusionne pas ces compositions; sa cote principale de version est commune à leurs usages.
4. Deux compositions exactement égales mais portées par des identités logiques distinctes sont des candidates à rapprochement, pas une autorisation de réaffecter leurs identités.
5. La répétition d’une composante dans une liasse ne doit pas être supprimée silencieusement. Son intention et sa représentation doivent être décidées.

Le même document conserve une cote principale unique dans une version. R02 porte sur la représentation de compositions/assemblages, pas sur un droit de multiplier cette cote ou de coter les citations seules. La contrainte de représentation d’une identité logique de composition plusieurs fois relève de R02. La recommandation est une seule composition active par identité logique dans une version, avec distinction explicite lorsqu’une autre unité de production est voulue. Cette recommandation n’est pas marquée approuvée.

Le simple classement d’un élément dans Preuve ne produit aucune pièce. Les utilisations analytiques et les utilisations destinées à la production doivent être distinguables dans le contexte de version. Le passage de l’analyse à un appui plaidé ne contourne pas les vérifications de portée, de source et de production. R05 précise la représentation et les éventuelles exclusions explicites; aucun filtre visuel ne vaut exclusion.

Un document entier retenu sans citation reçoit sa cote principale et aucune sous-cote. Cela découle de la sélection de source entière déjà admise et de D05; aucune citation fictive ni nouvel arbitrage n’est nécessaire. Un document seulement classé analytiquement reste soumis à la sélection de production R05.

### 3.3 Cas obligatoire `[A, B]` → `[A, C]`

Les deux compositions sont différentes, même si le titre et la cote sont inchangés. L’ancien état `[A, B]` reste accessible depuis sa version figée; le nouveau manifeste conserve `[A, C]` avec cet ordre et ses états sources.

Deux politiques restent à arbitrer en R01 :

- **recommandation :** continuité logique explicitement déclarée de la pièce, avec nouvelle composition immuable; concordance `COMPOSITION_MODIFIEE`;
- autre possibilité : nouvelle identité logique de pièce, avec une filiation documentaire explicite vers l’ancienne.

Dans les deux cas, le résultat ne peut être `INCHANGEE` et ne peut être inféré du titre ou de `P-n`. Une éventuelle recotation est un autre changement, cumulable avec le changement de composition. Remplacer `[A, B]` par `[B, A]` change également l’ordre documentaire, sauf règle d’équivalence expressément approuvée pour le type concerné.

### 3.4 Persistance minimale et responsabilités

Les noms `IdentitePiece`, `CompositionPiece`, `CotationVersion` et `ManifesteProduction` désignent ici des responsabilités de données. **Ils ne prescrivent pas quatre nouvelles tables Django.** Une composition immuable peut être conservée dans le contenu canonique de version; une persistance autonome se justifie seulement si son cycle de vie et sa réutilisation l’exigent.

L’ERD cible devra choisir, justifier et contraindre leur traduction. Le minimum est de conserver des identifiants stables, les compositions exactes et les associations historiques consultables. Une contrainte d’unicité (version, cote), l’appartenance à la bonne version, les composantes ordonnées et la protection des données figées doivent être représentées, à l’endroit où elles sont effectivement garanties.

`ProducedExhibit`, table recalculée, ne devient pas un journal historique par changement de nom. Les identités génériques existantes ne sont pas des FK SQL vers toutes les sources. Les consommateurs E01 et les fichiers du dépôt ne sont pas réécrits pour adopter ces structures.

## 4. Concordance documentaire

### 4.1 Entrées et autorité

La comparaison porte sur **deux versions identifiées et leurs états figés**, y compris identités intrinsèques des documents et citations, parents documentaires, compositions, cotes, sous-cotes et utilisations. Son périmètre est l’union des deux bordereaux, et non leur seule intersection. Elle n’interroge pas les sélections ou textes actuels pour reconstituer l’histoire.

Les responsabilités restent séparées :

| Question | Autorité |
|---|---|
| De quelles occurrences rédactionnelles provient cette rédaction ? | Correspondance qualifiée + ExtremiteCorrespondance |
| Quelle transformation a été examinée, pour quels textes ? | ExamenEditorial conservé, distinct de l’appui probatoire |
| Quelles pièces et compositions changent entre deux versions ? | Concordance documentaire des états de production figés |
| Ce passage est-il appuyé pour cette portée ? | Utilisations/sélections et décisions d’appui correspondantes |

Une nouvelle table de concordance n’est pas imposée pour les rapprochements déterministes calculables depuis ces captures. Une décision humaine résolvant une ambiguïté, une scission ou une fusion doit toutefois être conservée avec ses versions, extrémités, motif et auteur, sans devenir une seconde filiation rédactionnelle.

### 4.2 Résultats et ambiguïtés

Les résultats exposent les identités des deux côtés, anciennes/nouvelles cotes et compositions, traitements, raisons et diagnostics. Conservation, ajout et retrait décrivent la présence; recotation et modification de composition décrivent des différences cumulables. Une scission ou une fusion porte une carte N:M explicite et ne résulte pas du seul partage d’une source.

Un même document reste retrouvable par son identité malgré recotation; une même citation par son identité et son parent malgré changement de sous-cote. Une même cote ou sous-cote pour des objets différents n’est jamais une correspondance. Une même identité logique avec composition modifiée n’est jamais une identité documentaire exacte. Les candidats ambigus restent visibles; leur résolution n’est ni devinée par similarité de titre, ni fabriquée à partir de l’état courant.

Les rapprochements vers juillet conservent les associations attestées et les exceptions documentaires déjà contrôlées (`CONTIENT`, `EQUIVALENCE_VALIDEE` et leur provenance). Une lacune historique ne disparaît pas parce que la nouvelle pièce est bien connue. L’export présente le contexte des cotes des deux versions et les éventuelles réserves.

UC-C-17 porte ce nouveau parcours; UC-C-12 conserve la concordance rédactionnelle et la transition des décisions E01.

## 5. ResultatVersion et production

### 5.1 Une autorité de résultat

Le ResultatVersion représente une révision cohérente des entrées : occurrence et Statement réel, textes, sélections, sources/certifications, pièces/compositions, dates/précisions, profil de cotation des documents et sous-cotation des citations, références, examens et diagnostics. Il fournit l’acte, les références actives, le bordereau, les noms des pièces, le cahier et le manifeste. Aucun exportateur ne réattribue sa propre cote.

Un jeton de révision ou une empreinte des entrées permet de refuser un résultat périmé. Les écritures concurrentes et les mises à jour entre deux rendus ne doivent pas assembler deux cotations. La stratégie de verrouillage/lecture cohérente devra être montrée par les séquences; aucun algorithme existant n’est déclaré conforme sans adaptation.

Les références historiques littérales restent intactes. Une modification de texte ou de rattachement impose le contrôle des ancrages; remplacer globalement `P-n` dans Statement.text est interdit. Les contrôles EX01–EX07 applicables restent cumulatifs et qualifiés par profil : une analyse interne ne devient pas un faux référent E01 pour contourner ses préconditions.

### 5.2 Manifestes et fichiers

Le dossier de production conserve : identifiants de version/résultat, profil et paramètres de classement, entrées du bordereau, pièces et compositions, fichiers ordonnés par pièce, noms, formats, tailles, empreintes, rôle de chaque fichier, liens vers cahier et acte, version du moteur et ressources nécessaires. Une pièce peut produire plusieurs fichiers; la correspondance est explicite.

Les originaux restent indépendants. Le contenant d’une source, la composition d’une pièce et l’assemblage d’un cahier ne sont pas trois noms pour le même objet. Le manifeste permet de remonter de chaque fichier à la pièce, sa composition et la version concernées.

La restitution historique sert les livrables effectivement conservés sans recalcul des cotes. Une nouvelle génération avec un moteur actuel est un dérivé identifié; elle ne remplace pas silencieusement les octets historiques. Le niveau de reproductibilité attendu est R07, sans remettre en cause cette conservation obligatoire.

## 6. Gel, publication et communication

### 6.1 Garanties de gel

D08, les protections d’examens dès L1-A et le gel global L5 restent distincts. Une transaction SQL n’assure pas, à elle seule, la cohérence du stockage.

Protocole technique **recommandé à modéliser et à éprouver en L5**, sans le présenter comme réalisé :

1. Préparer un ensemble candidat non publié depuis une révision identifiée; produire et vérifier tous ses fichiers.
2. Placer les fichiers dans un stockage durable adressable par identifiants stables, prêt à être rendu immuable. Une opération encore nécessaire après le commit ne doit pas pouvoir laisser un livrable final introuvable.
3. Acquérir les verrous nécessaires en base, recontrôler entrées, examens, sources et version, puis vérifier la présence et les garanties de conservation des fichiers candidats.
4. Enregistrer le contenu canonique, les associations documents/citations/cotes/sous-cotes/utilisations et son manifeste, et finaliser la version dans la transaction. L’interface ne considère publiés que les ensembles finalisés et complets.
5. En cas d’échec avant commit : aucun gel publié; candidats orphelins identifiables, nettoyage uniquement après contrôle d’absence de références. Après commit : les fichiers référencés doivent déjà être disponibles et protégés. Une reprise retrouve le résultat finalisé ou refuse une divergence; elle n’en écrase pas un autre.

Ce protocole ne remplace pas la preuve du backend de stockage. R08 porte le choix concret et la récupération. Les séquences devront couvrir crash avant/après préparation durable, conflit sous verrou, échec du commit, interruption après commit et reprise répétée. Les protections doivent résister aux chemins ORM/bulk/SQL et aux mutations du stockage dans le modèle de droits retenu.

### 6.2 États et événements

Préparation et gel décrivent l’état du contenu. Dépôt et communication sont des événements attestés portant sur ce contenu, ses livrables et les preuves disponibles. Une version peut être figée sans envoi, puis communiquée plusieurs fois, et déposée à un moment distinct. Il ne faut pas imposer une chaîne exclusive `FIGEE → DEPOSEE → COMMUNIQUEE` qui perdrait ces combinaisons.

UC-C-19 enregistre modalités, dates, destinataires, livrables ou support papier et preuve disponible. Le gel n’invente pas l’événement. Un événement postérieur ne modifie ni les textes ni le manifeste figé; une erreur de relevé se corrige par trace explicite, pas par une réécriture de l’histoire.

## 7. Dépendances et arbitrages résiduels

Les réserves ci-dessous distinguent les **arbitrages fonctionnels à soumettre
à l’utilisateur** des modalités techniques à spécifier et vérifier par B dans
les dossiers. R08 relève d’abord de cette seconde catégorie : B doit proposer
un backend et ses preuves, puis soumettre le dossier complet à approbation.
Aucune réserve n’est résolue silencieusement par le code :

| ID | Question et recommandation B | Use cases bloqués | Travaux indépendants |
|---|---|---|---|
| R01 | Continuité d’identité lors d’un changement de composition. Préférence : identité logique maintenue seulement sur décision explicite, nouvelle composition immuable; autre choix : nouvelle identité + filiation | 16, 17; variantes composites de 09/18 | Édition E01, contexte, journal, organisation des sources |
| R02 | Plusieurs compositions d’une même identité dans une version et déduplication exacte. Préférence : une composition active par identité logique; pas de fusion automatique des identités distinctes | 16, 09, 17, 18 composites | Usages et sélections sans cotation finale |
| R03 | Date des composites, traitement des dates plus vagues qu’un jour et dernier départage. Conserver D06 pour les types déjà définis | 09/16 sur types concernés | Adaptateurs aux dates vérifiées, fondations neutres |
| R04 | Principe **décidé** : cote du document / sous-cotes des citations. Modalités techniques restantes : notation, ordre par type, égalités/rangs absents et représentation des liasses/fragments | 08/09/16/17/18 pour les seules modalités applicables | Identités, provenance et cas du document retenu sans citation déjà fixés; ne pas rouvrir le principe |
| R05 | Représentation des usages analytiques/produits et exceptions explicites à la production. Préférence : choix enregistré et diagnostiqué, indépendant de l’affichage | 04/16/09 pour le nouveau périmètre | Classement de preuves; contexte d’analyse autonome |
| R06 | Définition du « parcours de rédaction » et unicité des brouillons actifs. Préférence MVP : branche explicitement identifiée si plusieurs brouillons sont permis | 01A/01B | Journal E01, revue C0-A |
| R07 | Reproductibilité de génération : restitution des octets conservés obligatoire; niveau supplémentaire de régénération à déterminer | 18B pour la promesse supplémentaire | Préparation et conservation des fichiers |
| R08 | Backend immuable, droits, durable staging et récupération. Recommandation technique au §6, à choisir et éprouver | 11, activation réelle de 18/19 | Conception, rendus candidats et tests de panne synthétiques autorisés séparément |

Les libellés numériques renvoient aux UC-C correspondants, y compris leurs sous-cas. Une réserve ne bloque que les chemins qu’elle affecte; elle ne permet pas de déclarer le use case entier prêt si un critère obligatoire reste indéterminé. Tout périmètre partiel doit devenir un sous-cas nommé, doté des quatre vues et approuvé explicitement.

Le fournisseur PHRASE existe désormais sur la branche locale A `b695e4683ed68bbc82e50cd68f712b3d5c5206d5` : voir le [rapport de références](RAPPORT_CONSOLIDATION_ET_VALIDATION.md). Cela ne change pas P6, ne prouve pas le déploiement et ne lève pas D07/CF4. Son contrat, ses deux migrations 0010 et ses tests rapportés doivent être pris en compte avant le dossier UC-C-08/L3-B; C ne les réimplémente pas.

## 8. Acceptation et gouvernance

Les 38 scénarios NR/CF3 sont conservés. Les scénarios V2 gardent leurs numéros sous le préfixe `EPIC-V2:T01` à `EPIC-V2:T14`. Les contre-épreuves nouvelles `C-UML:N01` à `C-UML:N16` sont définies dans la [matrice](MATRICE_COUVERTURE_V2_C.md). Ce sont des scénarios à exécuter ultérieurement, pas des résultats de tests.

Pour chaque use case, les quatre vues et leur traçabilité sont obligatoires selon le [protocole](PROTOCOLE_VALIDATION_UML.md). Les états observés P6 restent séparés des modèles cibles, et les services proposés sont signalés comme tels. Aucune validation antérieure d’une activité ou d’un patch isolé ne vaut approbation du nouveau dossier à quatre vues.

## 9. Clarification Statement ST-R1

Le [mandat reçu](references/MANDAT_INVARIANTS_STATEMENT_2026-10-20.md) décide
ST01–ST05 : seules les origines REPRODUCED attestées autorisent la réutilisation
d’identité. La reprise d’un contenu PRODUCED crée un Statement propre à la
nouvelle occurrence; la filiation ne dépend pas du partage de PK. Les anciens
rapports permettant ce partage à texte égal sont historiques sur ce point.

Les [invariants et leur analyse](INVARIANTS_STATEMENT_REPRODUCED_PRODUCED.md)
précisent les lacunes du modèle, le risque de rattachement concurrent, la
solution minimale L1-A et le profil C0-A proposé sans schéma. La modification
directe privée reste conditionnelle à une propriété fiable et à la fermeture
des rattachements, hors activation C0-A proposée. La question de item est
séparée. Aucun R01–R08, schéma, nouveau lot ou développement n’est approuvé ici.

## 10. Identités et révisions transversales — C-TRANS-R1

[Décision fonctionnelle A–E](references/MANDAT_COHERENCE_TRANSVERSALE_2026-10-21.md),
[modèles et invariants](MODELE_TRANSVERSAL_C.md) : une Cause contient plusieurs
Acte et un Acte plusieurs VersionActe. Version figée modifiée → autre version
BROUILLON; gel distinct des événements. Preuve est une identité durable;
RevisionPreuve en est l’arbre complet à un état exact, avec ses propres nœuds.
UP vise cette révision et ses sélections y appartiennent. Modifier une révision
protégée, ou affectant des usages non choisis, exige une nouvelle révision entière
sous la même Preuve; les références et textes historiques restent inchangés.

Les entrées de ResultatVersion (§5.1) incluent donc les **identités exactes de
révision**, leurs chemins de sélection, les états sources/citations et les
liens pertinents; le gel (§6.1) conserve et protège ces associations. Un renvoi
CF2 externe garde sa version/occurrence cible exacte et retrouve ses révisions
via ses usages. Aucun renvoi entre preuves ou moteur d’inférence n’est ajouté.
DocumentSource demeure un rôle intrinsèque distinct de son état capturé et
indépendant des cotes. La projection C-COT est inchangée sur ce point.

Deux concordances juillet → demande modifiée : UC12 paragraphes, UC17 pièces
et cotes, avec les seules captures attestées. Aucune reconstruction d’un arbre,
examen ou VersionActe historique manquant. Application mono-utilisateur : les
acteurs sont des points de vue du même humain. La concurrence technique reste
traitée. R06 concerne les parcours/variantes personnels, sans workflow d’équipe;
la pluralité des versions d’un acte ne clôt pas le nombre de brouillons actifs.

Il s’agit de corrections de cohérence et de propositions de traduction dans
les modèles; les dossiers locaux restent à compléter et à approuver. L1-A
connaît le contrat d’identité sans implanter proof_manager; L2 implante les
révisions; L5 ferme le gel global, L6 prouve les deux concordances. Détails
au backlog §15; aucune dépendance d’exécution inverse L1-A → L5.
