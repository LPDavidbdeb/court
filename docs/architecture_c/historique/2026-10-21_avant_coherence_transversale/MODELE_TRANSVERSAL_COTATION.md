# Cotation du document et sous-cotation des citations

**C-COT-2026-10-21-R1 — décision fonctionnelle du Product Owner intégrée à D05.**
[Décision source](references/DECISION_PO_COTATION_DOCUMENT_CITATIONS_2026-10-21.md).
Le principe est décidé. L’ERD ci-dessous est sa traduction conceptuelle;
il ne constitue ni un schéma physique approuvé ni une autorisation de développement.

[ERD SVG](modele_global/cotation_document_citations.svg) ·
[Source PlantUML](modele_global/cotation_document_citations.puml) ·
[PNG](modele_global/cotation_document_citations.png).

![Cotation versionnée des documents et citations](modele_global/cotation_document_citations.png)

## 1. Identités et associations fonctionnelles

| Objet ou relation | Contrat décidé |
|---|---|
| Document source | Identité intrinsèque `(modèle qualifié, PK)`, indépendante du titre, de la cote et de la version; état utilisé conservé séparément |
| Citation | Identité propre `(modèle qualifié, PK)`; document parent identifié et vérifié, par exemple EmailQuote → Email ou PDFQuote → PDFDocument |
| `(VersionActe, DocumentSource) → cote` | Une cote principale par document retenu dans le bordereau de cette version; plusieurs citations/usages du document ne lui créent pas plusieurs cotes principales |
| `(VersionActe, Citation, DocumentSource) → sous-cote` | Sous-cote de la citation sous la cote principale de son document parent, dans la même version; aucune cote principale autonome de citation |
| Version, occurrence, utilisation → sélection | L’utilisation appartient au contexte rédactionnel de la version et conserve ses sélections de documents ou de citations; une sélection de citation conserve aussi son document parent |
| Gel et concordance | Conserver les états et associations exacts, puis comparer les identités de document et de citation entre versions; afficher séparément les variations de cote, sous-cote, sélection et composition |

`DocumentSource` est ici un **rôle conceptuel** applicable aux documents
probatoires. Ce nom ne désigne pas l’énumération actuelle
`document_manager.DocumentSource` (PRODUCED/REPRODUCED), ni une nouvelle table
à créer. Les boîtes de l’ERD représentent des responsabilités et associations;
les dépendances fonctionnelles ci-dessus ne prescrivent aucune clé primaire
composite, nouvelle GFK ou migration.
La projection porte sur les documents et citations; les autres éléments
probatoires et contenants, notamment Photo→Event de CF4, gardent leurs contrats.

Une sous-cotation ne peut désigner une citation d’un autre document, d’une
autre version ou d’un type seulement supposé d’après une PK numérique.
Une référence active est résolue depuis le bordereau du ResultatVersion de
la version utilisatrice. Numéro de paragraphe, rang de segment dans une
composition et sous-cote restent distincts.

## 2. Production et conservation

Le classement CHRONO_VERSION porte sur les documents retenus pour la
production. Le bordereau fournit ensuite leurs cotes principales et les
sous-cotes des citations sélectionnées. L’interface, les renvois, l’acte,
le cahier et les fichiers consomment ce même résultat; aucun exportateur ne
recote les citations séparément.

Un document explicitement retenu **sans citation** conserve une cote principale
et possède zéro sous-cote. Ce cas découle déjà de la sélection d’une source
entière (D02/INV02, avenant §3) et de D05; il n’est pas un nouvel arbitrage.
Le simple classement analytique ne suffit toujours pas à retenir un document
pour la production; cette frontière reste celle des usages/sélections et de R05.

La composition d’une pièce ou d’une liasse décrit les matières et leur ordre.
Elle ne transforme pas ses citations en documents cotés autonomes. Plusieurs
compositions utilisant un document restent distinctes comme compositions,
tout en référençant son unique cote principale dans la version. Un fichier
assemblé ne reçoit pas une nouvelle cote principale par le seul effet du rendu.
R01/R02 conservent leurs questions de continuité/composition; ils ne rouvrent
pas l’identité de l’objet recevant la cote principale.

Le gel conserve les identités et états utilisés des documents et citations,
les liens de provenance, les cotes et sous-cotes, le profil d’allocation et
les cartes occurrence → utilisation → sélection. La relecture utilise ces
captures; aucune mutation du travail courant ne les reconstitue ni ne les
réécrit. Les associations et lacunes historiques de juillet restent intactes.

La concordance relie le même document par son identité malgré une recotation,
et la même citation par son identité et son parent malgré une nouvelle
sous-cote. Un même libellé dans deux versions n’établit aucune identité.
Un changement de composition est signalé séparément, même sans changement
de libellé; les décisions N:M sur les assemblages restent explicites.

## 3. Précisions résiduelles réellement nécessaires

| Sujet | État et travail restant |
|---|---|
| Objet de la cote principale et lien des sous-cotes | **Décidé**, aucun arbitrage ouvert |
| Document retenu sans citation | **Déjà déterminé** : cote principale, aucune sous-cote; aucune citation fictive à créer |
| Ordre des segments d’une citation composée et insertions au même point | Ordre explicite déjà requis par D10/UC08; il ne décide pas l’ordre de sous-cotation du bordereau |
| Ordonnancement des citations sous chaque document | Profil technique à préciser par type : repères source, égalités, rangs absents et stabilité après ajout/retrait. D04 recommande l’ordre source des fragments d’acte; cette recommandation ne définit pas à elle seule le classement de toutes les EmailQuote/PDFQuote |
| Notation et espace d’unicité des sous-cotes | R04 réduit à ces modalités : notation, qualification par cote parente/version, conflits et diagnostics. Aucun choix « citation cotée seule » à soumettre |
| Traduction physique et gel | À justifier dans les dossiers ERD/séquences : contraintes d’appartenance, conservation des états, droits et transactions; aucune nouvelle table imposée par ce complément |

Les autres réserves existantes (dates de composites, production analytique,
stockage, etc.) gardent leur périmètre. Elles ne sont pas réouvertes ni
transformées en préalables nouveaux au principe décidé.

## 4. Acceptations documentaires à reprendre dans les lots

Tous les scénarios suivants sont **NON EXECUTES**; ce sont des attentes de
conception, sans système automatisé de traçabilité supplémentaire.

| Scénario | Résultat attendu | UC / lots |
|---|---|---|
| COT:T01 | Deux citations distinctes d’un document et plusieurs usages : une cote principale, deux sous-cotes; tous les usages conservés, aucune sous-cote supplémentaire pour répéter la même citation | 08/09/16; L3-A/B, L4 |
| COT:T02 | Nouvelle version recotant le document et changeant la sous-cote d’une citation conservée : les deux identités et leur provenance permettent le rapprochement; la version figée conserve ses associations | 09/17/11; L3-A, L5/L6 |
| COT:T03 | PK identique entre modèles ou libellé identique entre versions : aucun rapprochement sur cette seule égalité | 16/17; L3-A/L6 |
| COT:T04 | Citation rattachée à un autre document, mauvaise version d’utilisation ou référence à une citation comme cote principale : refus du résultat strict concerné, sans rattachement corrigé implicitement | 08/09/16; L3-A/B, L4 |
| COT:T05 | Document entier retenu sans citation : cote principale et zéro sous-cote. Une source seulement classée dans une preuve ne devient pas produite par ce fait | 09/16; L2/L3-A |
| COT:T06 | Après gel, changement du travail courant : relecture des documents, citations, cotes, sous-cotes et usages depuis les captures; aucune validation historique inventée | 11/17; L5/L6 |
| COT:T07 | Ordre de composition différent de l’ordre de repérage source : conserver les deux responsabilités; une règle d’allocation manquante produit un diagnostic sans remettre le principe en arbitrage | 08/09/16; L3-A/B, L4 |

Les compléments des [UC08](use_cases/UC-C-08/specification.md),
[UC09](use_cases/UC-C-09/specification.md), [UC16](use_cases/UC-C-16/specification.md)
et [UC17](use_cases/UC-C-17/specification.md) intègrent ce contrat. Leurs dossiers
à quatre vues restent à compléter et à approuver. Aucun statut de développement
prêt n’en découle. Les dossiers et preuves C0-A déjà approuvés restent inchangés.

## 5. Vérification de ce complément documentaire

Le 21 octobre 2026 : quatre sources concernées (ERD transversal, vue d’ensemble,
activités US08/09) compilées en SVG avec PlantUML 1.2026.8, code 0; PNG sur fond
blanc générés avec rsvg-convert et quatre rendus inspectés par B. Les 57 nouveaux
liens locaux contrôlés sont valides. Les 91 exigences littérales V2, 38 scénarios
NR/CF3 et 44 tickets sont conservés. Les cinq manifestes actifs et les dossiers
C0-A approuvés sont inchangés et cohérents; 670 fichiers applicatifs inchangés.
Aucun test applicatif ou accès à une base exécuté pour ce complément.
