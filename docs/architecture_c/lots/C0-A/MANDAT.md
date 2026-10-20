# C0-A — Mandat technique proposé à l’Agent A

**20 octobre 2026 — PROJET À APPROUVER AVANT DÉMARRAGE.**
Ce document propose une seule reprise bornée de C0-A, jusqu’à livraison pour
revue indépendante. L’approbation des conceptions est acquise; l’autorisation
d’exécuter ce mandat reste à donner. Aucune consigne de démarrage n’a été
adressée à A. La fusion documentaire de la PR #31 n’intègre pas le code C0-A.

## 1. Contrats à réaliser

| Profil approuvé | Référence Git immuable | Dossier contractuel conservé |
|---|---|---|
| UC-C-13::C0A_ISOLER, **C0A-UML-R2-ST** | PR #30, `cd584c307fcc31096dd93daae6a8fc26ab949eaf` | [Quatre vues, spécification et manifeste](../../versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md) |
| UC-C-14, **C0A-UML-R2-HIST**, C14-D1/D2 | PR #31, `30724df7ec5cbd1aba8ef25d59b5c3a162d20dab` | [Quatre vues, spécification et manifeste](../../versions_approuvees/UC-C-14_C0A-UML-R2-HIST/README.md) |
| UC-C-15, **C0A-UML-R2-DIAG**, C15-D1 | PR #31, `30724df7ec5cbd1aba8ef25d59b5c3a162d20dab` | [Quatre vues, spécification et manifeste](../../versions_approuvees/UC-C-15_C0A-UML-R2-DIAG/README.md) |

Empreintes SHA-256 des manifestes originaux, respectivement :

- UC13 : `367846c13385444b673a2a21e4c57599812c33118a74d917a7064ccd4fdfaa3d`.
- UC14 : `2c5ba44a30d63d6533f7d983a03a969f06f428ef54950b64109b13cf97d4ae1b`.
- UC15 : `eb3a3785690191bef386d1ab42547064d5b5c5bcbdbc3a6019cfe8c76e89c742`.

Les [approbations](../../registre_validation.md) sont limitées à ces profils.
Les modèles globaux servent de contexte; les extensions citations de G-R3
ne sont pas approuvées par transfert. Les critères et diagrammes approuvés
guident le développement. Les anciens tests du patch ne constituent pas des
oracles lorsque leur attente contredit ces contrats.

## 2. Socle et isolation proposés

**SHA de départ proposé à approbation avec ce mandat :
`515666eb8c6e7fdcdd265f9187c9c37b769b0fed`.** Ce socle intègre les évolutions
du régime des citations déjà étudiées. P6
`212a7feee81aef46a5b43d36e8eeafe0f8870064` reste la référence historique du
patch; aucune cible ou référence de A n’est déplacée.

A préparera une copie Git complète et indépendante, avec son propre `.git`,
sans worktree, partage d’index, alternates ou objets liés aux ressources de A.
Branche locale proposée : `review/c0a-515666e`. Relever son SHA initial et
vérifier l’absence de changements avant exécution. Les documents contractuels
ci-dessus seront consultés aux références immuables, même s’ils ne sont pas
présents dans l’arbre applicatif de départ. Ne pas fusionner `main` ou toute
la branche E01 pour obtenir la documentation.

Les essais utilisent exclusivement une instance/base PostgreSQL jetable,
initialement vide, et des fixtures synthétiques. Configurer explicitement
l’hôte, le port, le rôle et les noms de base de travail/test. Le rôle ne doit
donner aucun accès en écriture à la base réelle. Employer des paramètres de
test synthétiques, des médias temporaires et des services externes neutralisés;
ne charger aucun `.env` réel, identifiant de production, sauvegarde ou dump réel.
Vérifier la destination effective avant toute migration ou test. Les migrations
existantes peuvent s’exécuter uniquement sur cette base jetable.

La préparation de l’environnement et les fichiers de configuration temporaires
restent dans la copie isolée/hors des sources suivies. A n’utilise, n’arrête et
ne nettoie aucune ressource appartenant à une autre intervention. Le rapport
conserve les paramètres non secrets prouvant l’isolation et les commandes de
création/arrêt de ses seules ressources. Si l’isolation n’est pas vérifiable,
ne pas lancer les commandes Django.

## 3. Fichiers applicatifs modifiables

La reprise reste dans les huit fichiers du périmètre initial :

| Fichier | Modification permise |
|---|---|
| `document_manager/views/produced_views.py` | Voies existantes `ajax_edit_node` et `ajax_delete_node`, validation, protections, appel des services et traitement transactionnel des erreurs |
| `document_manager/protection.py` | Précontrôle du bloc, archivabilité, captures/détachement, archivage et retrait atomiques; conservation de tous les contenus |
| `document_manager/models.py` | Méthodes Python concernées de fraîcheur et gardes de suppression; aucun changement de champ ou de schéma |
| `case_manager/models.py` | Méthodes concernées de `ConfirmationAppui` : fraîcheur calculée depuis l’occurrence réellement persistée et gardes locales nécessaires |
| `document_manager/concordance.py` | Lecture des appuis par couple/type, résultat et diagnostics en mémoire, erreurs globales distinctes |
| `document_manager/export_concordance.py` | Conservation des appuis/diagnostics, transmission à EX04 et calcul strict cumulatif existant |
| `document_manager/test_e01_numerotation.py` | Tests de comportement, HTTP, conservation et atomicité des profils UC13/14 |
| `case_manager/test_e01_cotes_concordance.py` | Tests de fraîcheur, lecture mixte, diagnostics et export UC13/15 |

Le rapport d’exécution et le diff de cette reprise sont livrés dans
`docs/architecture_c/lots/C0-A/`, sans remplacer le rapport ni le patch
historiques : `RAPPORT_REPRISE_C0A.md` et `C0A_REPRISE_DIFF_COMPLET.patch`.
Une modification nécessaire hors de cette liste doit être signalée avec son
motif, son chemin et son impact **avant exécution**, pour autorisation.

Interdictions : nouveau champ, schéma ou migration; nouvelle application,
route, interface ou fonctionnalité; changement de politique des cotes;
modification des diagrammes approuvés, des archives gelées ou des documents
sources. Ne modifier ni `core/quote_regime.py`, ni les fournisseurs Email/PDF,
ni les pilotes, contrôles, scripts ou migrations de A. Aucune conversion
générale HERITE → PHRASE. Les citations PHRASE restent créées au besoin.
Aucun commit, push, merge, déploiement, accès réel, intervention sur serveur,
sauvegarde ou branche protégée n’est inclus dans cette reprise proposée.

## 4. Corrections attendues dans ce seul lot

Le [patch historique](C0A_DIFF_COMPLET.patch), SHA-256
`d10781a1c815e2b41d0c14ea39e8a51e8d2803bcb6c313fd4d22dec95b827a27`,
reste une référence conservée. A peut en reprendre les parties conformes dans
sa copie isolée après approbation du mandat; il ne doit ni le publier tel quel
ni écraser l’original. Trois écarts sont à fermer par le comportement livré :

**C0A-ST-01 — UC13.** Pour tout changement réel de texte sur une occurrence
PRODUCED éditable, capturer l’avant, créer un Statement neuf, repointer cette
seule occurrence et capturer l’après. Supprimer la branche d’écriture du texte
en place, même si un seul usage est observé ou si l’ancien objet paraît privé.
Texte égal : ni nouveau Statement, ni capture additionnelle; `item` peut être
modifié séparément dans la même opération atomique si autorisé. Une occurrence
sans type ni objet peut recevoir son premier texte. Autre type, objet absent
ou clé incohérente : refus. REPRODUCED et référents historiques restent protégés,
y compris pour `item`. Captures, nouvel objet, association et `item` sont annulés
ensemble en cas d’échec tardif.

À la consultation de ConfirmationAppui, recharger l’occurrence réellement
persistée : autre Statement, même à texte égal, ou autre empreinte impose
`A_REEXAMINER`, y compris pour SANS_APPUI. La Correspondance compare Document
et couples Statement/empreinte des deux rôles. Ne pas réécrire les décisions
stockées ni inventer une capture d’examen manquante. L’identité complète des
compositions et le contexte sémantique de `item` restent hors de ce lot.

**C0A-14-01 — UC14.** Précontrôler le bloc entier, cible et descendants,
avant la première écriture. Une occurrence protégée, une cascade détruisant
une décision/ancrage ou un contenu non archivable fait refuser tout le bloc.
Seuls les Statement réels vérifiés et les structures sans type ni objet sont
archivables. Refuser Quote HERITE/PHRASE, Event, objet disparu ou GFK partielle;
ne jamais lire une PK homonyme comme Statement ou produire une archive de
citation au texte vide. Cette restriction acceptée sera signalée si elle
entrave effectivement la rédaction, sans élargissement silencieux.

Capturer Document, ancien ID, position, item, numéro, texte/empreinte disponibles
et motif; distinguer Statement vide et structure. Repointage des extrémités
vers l’archive, puis retrait des seuls nœuds du bas vers le haut. Conserver
tous les Statement et VersionTexte, même sans occurrence, ainsi que décisions
et captures disponibles. Aucune purge automatique ni appel indirect à un
collecteur; `statements_supprimes` reste vide. Garder les refus ORM locaux
sur capture utilisée, archive liée et Document nécessaire. Le service possède
sa transaction, y compris sous celle de la vue : rollback avant interception
HTTP, refus métier 403 lisible et exception technique 500, jamais de succès
partiel. Ne pas ajouter un chantier frontend pour réaliser cette réponse.

**C0A-REV-01 — UC15.** Vérifier le couple documentaire réel et la sélection
de source avant lecture. Une cible étrangère, un Document inexistant ou une
source ambiguë est une erreur globale. Pour chaque origine du bon couple,
vérifier Document, ContentType et objet réel. Une structure pure ne produit
aucun appui et n’entraîne aucune exploration implicite des descendants.
Archive non typée, absence, incohérence ou type non pris en charge produisent
des diagnostics locaux individualisés; poursuivre la lecture et conserver
tous les appuis valides, quel que soit l’ordre. Garder les identités de
correspondance, extrémité, occurrence et appui, et la qualification VERSION SOURCE;
ne pas dédoublonner des filiations distinctes par cote/Statement seul.

Retourner `LectureAppuis(appuis_valides, anomalies, lecture_complete)` en
mémoire. Les exceptions techniques inattendues se propagent; ne pas convertir
une panne en succès vide. L’export conserve les deux listes et collecte les
diagnostics avant son verdict : EX04 reçoit les défauts structurés de résolution;
anomalie non résolue ou lecture incomplète interdit le strict. EX01–EX07 restent
cumulatifs, sans EX08 ni validation fondée sur `lecture_complete` seul.
La lecture ne crée aucun examen, confirmation, capture ou nouveau partage.
Une liste vide ne vaut pas SANS_APPUI. Une Quote hors contrat Statement reçoit
un diagnostic de type, indépendamment de sa certification.

## 5. Essais indispensables et acceptation

**Ces essais sont à exécuter par A après autorisation; aucun n’est présenté
comme exécuté par la publication du présent mandat.** Commencer par relever
les suites découvertes et exécuter la référence sur le SHA de départ, avec
PostgreSQL jetable. Les 209 tests du rapport initial sont un résultat historique
sur P6, pas un nombre de succès à atteindre sur le nouveau socle.

| Ensemble | Preuve de comportement exigée |
|---|---|
| UC13 — ST:T01–T08, AC01–AC08 | POST réel partagé et privé apparent : nouvel objet seulement sur texte différent; ancien texte et autres occurrences inchangés; texte égal/item seul et premier texte; refus REPRODUCED/référent/autre type/GFK incohérente; fraîcheur identité + empreinte, y compris même texte/autre Statement et instance déjà chargée; anciennes décisions/captures consultables |
| UC13 — atomicité et intercalage | Injecter un échec après création, repointage puis sauvegarde de `item` : aucun objet/capture/repointage partiel. Avec deux connexions PostgreSQL, rattacher une autre occurrence à l’ancien Statement entre contrôle et édition : son texte ne change pas. Ce test ne prouve pas la fermeture globale des rattachements |
| UC14 — C14:T01–T07 et T10 | Bloc mixte avec un seul membre protégé ou non archivable : refus entier sans archive. Couvrir cascades de décision/ancrage, PK homonymes, citations des deux régimes, objet absent, clé partielle, structure et Statement vide. Après retrait admissible, comparer champs d’archive, extrémités, décisions, tous les contenus/captures; vérifier les gardes ORM locales |
| UC14 — C14:T08–T09 | Échecs après seconde archive, repointage et premier retrait : égalité des états métier avant/après, HTTP sans succès trompeur. Éprouver un conflit concurrent sur copie jetable et consigner son résultat/sa limite, sans prétendre livrer un verrou universel |
| UC15 — C15:T01–T08 et T11–T12 | Deux couples avec Statement commun, source ambiguë, structure pure et types homonymes. Origines valides + chaque anomalie, deux ordres et permutations multiples : ensemble valide conservé et chaque diagnostic identifiable. Zéro mutation historique. Panne technique propagée; vide distinct d’un examen SANS_APPUI |
| UC15 — C15:T09–T10 | Export mixte conserve appuis et diagnostics, EX04 et strict refusés. Lecture complète avec un autre EX insatisfait : strict encore refusé. Un ensemble satisfaisant tous les contrôles conserve le comportement strict attendu |
| Non-régression | Suites E01 existantes, numérotation/cotes, concordance et protections; suites disponibles du régime des citations, dont `core.test_regime_citations_etape2`, et contrôles de P6 pertinents sur le socle choisi. Réutiliser les contrôles existants sans modifier leurs oracles ni les ressources de A |

Exécuter les tests ciblés HTTP/ORM sur PostgreSQL puis l’ensemble de la suite
applicative du socle autorisé avec la configuration synthétique. Relever les
commandes exactes, nombre découvert/exécuté, succès, échecs et exclusions avec
motifs. Un pilote de lecture ou un test avec doubles ne remplace pas les
contre-épreuves POST et transactionnelles ci-dessus. Ne pas normaliser une
régression en réécrivant son attente; si un ancien test attend la purge ou une
écriture en place désormais interdite, expliquer son remplacement par le
critère approuvé. Les autres attentes de sécurité restent opposables.

Les 38 scénarios NR/CF3 antérieurs sont conservés avec leur affectation aux
lots; leurs garanties futures ne sont pas exigées comme déjà réalisées par
C0-A. ST:T09–T12 et les scénarios CIT-I/CIT-E ne deviennent pas des fonctions
à implanter dans ce mandat. Les tables documentaires existantes suffisent :
**aucun outil de traçabilité automatisée élément UML → test n’est demandé**.

## 6. Livraison, revue et limites

Livrer le diff complet des huit fichiers, le rapport de reprise, les commandes
et résultats réellement obtenus, le SHA de départ, les preuves d’isolation,
les problèmes découverts et les limites restantes. Le diff doit pouvoir être
appliqué et revu indépendamment; les originaux historiques restent inchangés.
B examinera la conformité aux trois dossiers approuvés et aux acceptations
ci-dessus. Une contradiction architecturale significative revient à B;
un changement fonctionnel ou de périmètre demande l’approbation utilisateur.
Il n’y a pas de nouveau cycle général UML si le contrat est respecté.

Restent **L1-A/C0-B** : provenance/propriété persistantes, fermeture de toutes
les voies de rattachement, journal immuable et manifeste complet d’examen,
contexte sémantique de `item`, archives typées et nouveaux examens. Restent
**L5** : gel et protections globales SQL/bulk. Les sous-cas UC02/UC12 de citations
demeurent EN_REVUE; aucun renommage ou réexamen nouveau n’est implanté ici.
La conservation locale et l’atomicité ne valent pas immutabilité globale.

Après revue, la promotion du code vers une branche d’intégration puis `main`
sera autorisée séparément, avec essais sur base dédiée selon le processus.
La divergence entre le socle applicatif E01 et `main` sera traitée à cette
étape : elle ne bloque pas les corrections isolées. Aucun déploiement ni
changement des conditions de retour arrière de A n’en découle. C0-A n’est
pas « atterri » à la livraison d’un patch ou à une fusion de documentation.
Ne pas ouvrir automatiquement L1-A ou un autre lot.

**Seule décision encore nécessaire pour démarrer : approuver ce mandat,
notamment le SHA `515666e`, les huit fichiers, l’environnement jetable et la
livraison pour revue sans commit/push/merge applicatif.** Aucun arbitrage
CIT-D1–D4, mécanisme L1-A ou nouveau diagramme n’est un préalable à ce périmètre.
L’isolation vérifiée et la disponibilité du SHA sont des préalables techniques
à contrôler par A avant les essais, pas des décisions métier à rouvrir.
