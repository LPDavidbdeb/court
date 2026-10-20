# Citations dans C0-A — intitulés, examens et appuis d’origine

**CIT-C0A-2026-10-20-R1 — analyse et propositions documentaires.**
[Mandat](references/MANDAT_APPROBATION_UC13_VALIDATION_C0A_2026-10-20.md).
Code lu : `515666e` (application inchangée dans le HEAD de travail `94f3bc4`).
Le [constat A, B.3/B.4 conservé avec sa provenance](references/OBSERVATIONS_A_CITATIONS_2026-10-20.md)
est confronté aux sources et au patch; aucune base ou interface réelle testée.
Les quatre vues UC13 approuvées au commit cd584c3 restent inchangées.

## 1. Attribution fonctionnelle

| Sujet | Responsable | Dossier / effet sur les lots |
|---|---|---|
| Changer le texte d’une occurrence Statement | UC13::C0A_ISOLER | Approuvé R2-ST, sans écriture sur l’ancien objet; pas de mutation d’une Quote. |
| Changer seulement l’intitulé d’une occurrence portant une citation | UC02::RENOMMER_CITATION | [Quatre vues proposées](use_cases/UC-C-02/RENOMMER_CITATION/specification.md); responsabilité rédactionnelle. Une action distincte évite de changer le contrat UC13. Extension éventuelle C0-A à autoriser séparément, sinon L1-B. |
| Diagnostiquer fraîcheur et possibilité d’un nouvel examen | UC12::DIAGNOSTIQUER_EXAMEN | [Quatre vues et états](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/specification.md); lecture seule proposée. Le nouvel examen lui-même appartient à UC05E puis UC12, après L1-A/C0-B et l’adaptateur concerné. |
| Supprimer une occurrence et conserver son histoire | UC14 | [Contrat R2-HIST](use_cases/UC-C-14/specification.md); pas de purge automatique de contenu dans le profil proposé. |
| Retrouver les appuis historiques | UC15 | [Contrat R2-DIAG](use_cases/UC-C-15/specification.md); conserve résultats valides et diagnostics, ne reconfirme rien. |
| Ancrer/certifier une citation | Fournisseur de A, puis UC08 / L3-B | HERITE et PHRASE distincts; aucune modification de ses modèles, migrations, contrôles ou données. |

UC02 et UC12 restent les deux tickets existants; aucun nouveau use case, lot
ou ticket n’est créé. Leurs sous-cas ont chacun les quatre vues pour rendre
les propositions examinables. Leur présence ne les intègre pas automatiquement
au périmètre de code de C0-A.

## 2. Intitulé d’une occurrence-citation

### Constat vérifié par lecture

Dans le code principal, `ajax_edit_node` sauve item puis, pour un objet sans
attribut text, crée un Statement et repointe le nœud. Quote porte quote_text,
pas text : un renommage peut donc remplacer son association par un Statement.
Le patch évite ce repointage mais refuse toutes ces demandes avant de sauver
item. Ce 403 protège le contenu mais **n’est pas une règle fonctionnelle approuvée**.
L’interface actuelle peut masquer le refus (HTML 403 interprété comme JSON);
les gabarits n’offrent pas directement l’édition d’une citation. Ces constats
sont statiques, pas des essais navigateur ou HTTP.

### Proposition CIT-D1 — action rédactionnelle distincte

Recommander une action explicite `RENOMMER_OCCURRENCE`, avec seulement item,
identité de la cible et jeton d’état attendu. Elle relève d’UC02, pas du chemin
d’édition de texte UC13. Sur PRODUCED non protégé, une citation identifiée
par (app_label, modèle, PK, régime) peut recevoir un intitulé purement
rédactionnel sans sauver Quote, sa source, ses bornes ou sa certification.
Un champ text/quote_text ou une demande de repointage dans cette action est
refusé; un champ vide n’est pas une consigne implicite de convertir la citation.

Le résolveur proposé choisit explicitement le gestionnaire du régime déclaré :
HERITE via objects, PHRASE via phrase_objects. Un objet filtré par objects n’est
pas déclaré absent sans vérifier le régime attendu; aucune recherche par PK
seule ni substitution par derived_from. La lecture PHRASE n’active pas son
rendu dans les parcours historiques et ne modifie aucun contrôle de A.
Une certification PHRASE ineffective n’interdit pas en soi un renommage sans
incidence sur le contenu; elle reste diagnostiquée pour l’admissibilité probatoire.

### Proposition CIT-D2 — frontière du renommage C0-A

Comparer genre et index de numérotation du Document entier avant/après, sur
le résolveur commun. Un passage C-… / item vide peut changer rôle et numéro.
**Cette comparaison ne prouve pas, à elle seule, l’absence de changement de
sens ou de portée d’examen.** Dans le sous-cas conservateur proposé :

- Refuser toute mutation sur REPRODUCED ou occurrence historiquement protégée.
- Autoriser seulement un intitulé explicitement demandé comme présentation,
  genre et numérotation inchangés, sans décision/relation/ancrage ou contexte
  d’examen potentiellement affecté dans le bloc ou ses dépendances connues.
- Si le changement est sémantique, si un examen dépend de ce contexte, ou si
  cette dépendance n’est pas déterminable : refuser avec motif explicite.
  L1-A/C0-B devront conserver le contexte examiné; L1-B porte l’évolution
  sémantique explicite. Aucun ancien examen de contexte n’est fabriqué.

Un futur endpoint/action distinct et son affichage des erreurs nécessiteraient
notamment route, formulaire et interface au-delà des huit fichiers du patch :
**dépassement de périmètre signalé avant toute implantation**, non autorisé ici.
CIT-D1/D2 restent à approuver : accepter ce renommage limité, ou conserver le
refus actuel de tout renommage citation jusqu’à L1-B. La recommandation est
le renommage limité; aucune des deux options n’est considérée acquise.

## 3. Une concordance citation peut-elle être reconfirmée ?

### Constat précis

`Correspondance.etat_courant()` ne modifie pas etat stocké. Le patch compare
les ensembles de (Statement, empreinte) des deux rôles et renvoie faux pour
une extrémité Quote, indépendamment de son régime ou de sa certification.
`confirmer_traitement()` ne capture que Statement; il ignore Quote, et
**efface puis remplace** les M2M et les champs de décision. Le réappeler
pour une citation ne rend donc pas son examen représentable; le réappeler
pour un Statement ne préserve pas un journal complet des décisions antérieures.
La lecture du code confirme le défaut structurel; aucun nombre de concordances
réelles touchées n’est déduit et aucun parcours de reconfirmation n’est testé.

### Proposition CIT-D3 — qualifier au lieu de promettre une reconfirmation

La lecture doit exposer séparément, dans un résultat en mémoire :

1. La décision enregistrée et sa date, inchangées.
2. Sa fraîcheur dans le périmètre contrôlé : courant limité, périmé,
   ou non attestable faute de capture/manifeste approprié.
3. L’admissibilité de l’objet au contrat d’examen : Statement vérifié,
   type non pris en charge (Quote dans le contrat E01 actuel), objet absent
   ou couple incohérent.
4. La disponibilité d’un nouvel examen et son motif d’indisponibilité.

Une citation hors du contrat Statement n’est pas une preuve globalement
invalide. Une PHRASE effectivement certifiée n’est pas, pour autant, un examen
éditorial E01 valide. HERITE ne reçoit aucune certification PHRASE fictive.
Le code de compatibilité A_REEXAMINER peut être maintenu pour l’API existante,
mais le libellé doit expliquer le type hors contrat et ne pas proposer une
boucle de reconfirmation vouée à échouer. Une structure vide n’est pas
un examen textuel confirmé par défaut. La composition complète des occurrences
et le contexte item restent à L1-A/C0-B.

### Proposition CIT-D4 — sortie possible après les préalables réels

Pour un objet admissible devenu périmé : nouvel examen humain du contenu et
du contexte présents, après disponibilité du journal UC05E/L1-A, puis ajout
d’une nouvelle décision; l’ancienne reste historique. Pas de remplacement
de l’ancienne M2M tenu pour un journal append-only.
Pour Quote : il faut en plus un manifeste typé et l’adaptateur de régime
vérifié (L3-B selon la source), incluant identité complète, texte, origine,
bornes/empreintes pertinentes et statut du fournisseur. Une source absente
ou un couple incohérent doit d’abord être rétabli par une opération autorisée;
aucune reconfirmation ne répare ces défauts à elle seule.

C0-A peut proposer le diagnostic en lecture seule. **Aucune nouvelle voie de
reconfirmation conservant tout l’historique n’est annoncée comme réalisable
sans L1-A/C0-B.** L’activation de confirmations nouvelles avec l’ancienne fonction
écrasante est à exclure du futur mandat C0-A; sa garde éventuelle doit être
mandatée, pas déclarée déjà en place. CIT-D3/D4 sont à approuver comme contrat
de lecture et plan de résolution; elles n’autorisent aucun schéma ou service.

## 4. Conservation lors d’une suppression — recommandations UC14

**C14-D1 :** supprimer les occurrences autorisées, conserver les Statement et
leurs captures; désactiver la purge automatique de contenu dans C0-A. Le
modèle ne prouve ni l’origine durable ni l’utilité historique par un simple
compteur d’usages. Un objet devenu orphelin ne devient pas réutilisable.
Le traitement d’une purge administrative relève d’un mandat ultérieur avec
provenance/propriété L1-A et protections utiles, sans promesse de récupération
après destruction. Le patch conservé fait encore une purge conditionnelle :
écart C0A-14-01, pas une correction déjà exécutée.

**C14-D2 :** dans C0-A, refuser le bloc s’il contient un contenu non Statement,
une GFK incohérente ou un objet manquant : l’archive actuelle ne porte pas le
type générique et ne capture pas quote_text. Une citation ne doit pas être
archivée en faux Statement ou remplacée silencieusement par du texte vide.
L’alternative d’une archive partielle est rejetée pour ce profil, car elle
perdrait l’identité/contenu requis; l’archive typée L1-A/C0-B permettra de revoir
ces refus. Une structure sans type ni objet reste archivable comme structure.
L’ancien test de suppression d’Event avec PK homonyme est conservé comme
résultat historique; il faudra tester le nouveau refus sans effets, sans
renommer silencieusement ce test dans le patch.

Ces choix conservateurs sont explicitement soumis avec UC14. Ils ne sont pas
déduits de l’approbation de UC13 et ne prétendent pas imposer ST04 globalement.

## 5. C0A-REV-01 et consultation stricte — UC15

Une anomalie locale ajoute un DiagnosticAppui à LectureAppuis sans interrompre
les autres origines du même couple. Une erreur globale de contexte interrompt
la lecture avec un résultat d’erreur distinct. Une panne de stockage ou erreur
logicielle n’est pas absorbée en diagnostic métier : l’opération échoue et
aucun résultat partiel n’est qualifié complet.

Le constructeur actuel calcule déjà les EX après les lignes, mais les anomalies
locales réduites à une note ne constituent pas un contrôle structuré de leur
résolution. La cible conserve et transmet ces anomalies à EX04.
L’export collecte les résultats de toutes les lignes **avant** son verdict
strict. Les anomalies de résolution d’appuis alimentent EX04 (sources/références
non résolues); pas de EX08 inventé. Incomplétude → strict_possible faux,
même avec des appuis valides visibles. Lecture complète ne suffit pas : les
sept contrôles EX01–EX07 restent cumulatifs. Ni note libre ni liste vide ne
remplace le diagnostic structuré. Aucune confirmation nouvelle créée.

## 6. Décisions à examiner et limites

| Décision proposée | Recommandation | Périmètre d’approbation attendu |
|---|---|---|
| C14-D1 / C14-D2 | Conserver le contenu et refuser les archives insuffisantes | UC14 R2-HIST, quatre vues complètes; validation B du contrat conservateur, approbation utilisateur absente. |
| C15-D1 | Résultat partiel qualifié, erreur globale distincte et strict bloqué par incomplétude | UC15 R2-DIAG, quatre vues complètes; validation B, approbation utilisateur absente; C0A-REV-01 ouverte dans le code. |
| CIT-D1 / CIT-D2 | Renommage limité par action distincte; refus des changements de contexte non conservables | Sous-cas UC02 en revue, arbitrage utilisateur encore nécessaire; aucune extension C0-A automatique. |
| CIT-D3 / CIT-D4 | Diagnostic explicite; nouvel examen seulement avec conservation et type pris en charge | Sous-cas UC12 en revue, états et futur parcours dessinés; journal/adaptateurs non livrés. |

Les 38 scénarios NR/CF3 et les résultats existants sont conservés; tous les
nouveaux scénarios sont NON EXECUTES. Aucun code, patch, migration, base,
serveur, pilote ou contrôle de A modifié. La présente livraison n’émet pas
de mandat d’implantation et ne fusionne pas le nouveau dossier de conception.
