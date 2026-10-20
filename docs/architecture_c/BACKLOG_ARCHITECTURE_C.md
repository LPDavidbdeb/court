# Backlog de l’architecture C

**Version BLC-2026-10-20-R4-APPROB — 20 octobre 2026.** Structure R1 acceptée comme
référence provisoire de pilotage par le [mandat de revue](references/MANDAT_REVUE_COUVERTURE_C0A_2026-10-20.md),
sans validation implicite de complétude ni autorisation de développement.
La [copie exacte R1](historique/2026-10-20_avant_revue_backlog_R2/BACKLOG_ARCHITECTURE_C.md)
est conservée; les changements R2 sont expliqués au §9 et R3-ST au §10.

**Version approuvée : UML-13 C0A-UML-R2-ST, sous-cas C0A_ISOLER seulement (20 octobre 2026, cd584c3 / PR #30).**
Les propositions R1 mentionnées au journal §9 sont historiques. Le patch reste
inchangé; C0A-ST-01 et C0A-REV-01 sont distincts. Aucun ticket ou lot nouveau.

Objectif : livrer progressivement la rédaction versionnée, les utilisations de
preuves, les citations, les bordereaux CHRONO_VERSION et leur conservation.
Ce backlog ordonne le travail restant; il ne lance aucun développement.

Il contient **44 tickets** : 4 préparations transversales, 8 décisions ou études
résiduelles, 22 dossiers de use cases et 10 livraisons de lots. Les tickets UML
préparent les lots : ils ne sont pas des fonctionnalités supplémentaires.

## 1. Références, état de départ et règles de suivi

| Question | Document faisant autorité |
|---|---|
| Décisions D/CF et périmètre des lots | [Décisions consolidées](DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md), notamment §§7.1 et 10.5 |
| Identités, compositions, production et réserves R01–R08 | [Avenant](AVENANT_ARCHITECTURE_C.md) |
| Exigences et scénarios V2 | [Matrice de couverture](MATRICE_COUVERTURE_V2_C.md) |
| Dépendances et vagues des 22 use cases | [Plan UML](PLAN_MODELISATION_UML.md) |
| Contenu des dossiers, validation et approbation | [Protocole UML](PROTOCOLE_VALIDATION_UML.md) et [gabarit](use_cases/MODELE_DOSSIER.md) |
| Statut courant de chaque dossier | [Registre de validation](registre_validation.md) |
| Autorisation, intégration et avancement réel des lots | [Processus de changement](../PROCESSUS_CHANGEMENT.md), notamment §§5–6 |

Le présent fichier porte les priorités et les travaux à faire. Il ne crée pas
un deuxième registre de validation ou journal des lots. Une clôture renvoie
toujours à la preuve et à la transition inscrites dans le document compétent.

**État initial :** C0-A dispose d’un [rapport](lots/C0-A/RAPPORT_EXECUTION_C0A.md)
et d’un [patch](lots/C0-A/C0A_DIFF_COMPLET.patch), mais n’est pas atterri selon le
journal des lots. Les 209 tests, dont 31 nouveaux, sont les résultats rapportés
sur sa copie isolée. À l’initialisation R1, les 22 dossiers cibles étaient à constituer : 9
`A_SPECIFIER` et 13 `A_MODELISER`, aucun approuvé ou prêt au développement.
Ces constats décrivent l’initialisation R1, sans réexécution des tests. La
revue R2 produit les dossiers 13/14/15 : 13 validé B et à approuver, 14/15 en
revue; aucun dossier approuvé utilisateur ou prêt au développement. Le
registre reste l’autorité courante.

**Évolution de A constatée pendant la préparation :** le HEAD local lu est
`515666eb8c6e7fdcdd265f9187c9c37b769b0fed`. Le
[plan du régime des citations §12.6](../modele_preuve/PLAN_REGIME_CITATIONS.md#126-le-déploiement-réel-de-létape-2-20-octobre-12-h-54--12-h-57)
rapporte le déploiement réel de l’étape 2 et l’avance locale à `91f1ee8` avant
ce commit documentaire. C’est un résultat rapporté par A, sans vérification du
serveur dans ce travail. Les relevés P6 restent historiques et le rapport de
consolidation antérieur garde son constat daté. TRANS-01 a établi la
compatibilité statique sur `515666e`; ce socle est proposé au futur mandat,
sans autorisation d’application du patch. Voir le [rapport R2](RAPPORT_REVUE_COUVERTURE_ET_C0A.md).

La référence initiale de C0-A demeure
`212a7feee81aef46a5b43d36e8eeafe0f8870064` (P6). Aucun changement de cible,
application du patch, commit, push, fusion, migration ou accès à la base réelle
n’est effectué par la production de ce backlog.

Les identifiants ci-dessous sont stables. Au départ, les préparations et
dossiers sont **à préparer**, les décisions sont **à résoudre**, C0-A est
**à revoir puis à intégrer sous mandat**, et les neuf autres lots sont
**non autorisés**. Une tâche peut être documentée sans être ouverte à
l’implantation. Au point R2 : TRANS-01 est livré pour la vérification statique,
TRANS-02 pour le modèle initial C0-A et TRANS-04 pour sa traçabilité fine;
leurs extensions restent ouvertes. UML-13 est soumis à approbation, UML-14/15
restent en revue. C0A-REV-01 bloque la conformité du patch; aucun lot n’est
déclaré terminé et toutes les décisions DEC-R restent ouvertes.

## 2. Ordre proposé et portes de passage

| Priorité | Travail à préparer | Résultat attendu |
|---|---|---|
| **P0 — immédiat** | TRANS-01, premier périmètre TRANS-02 et TRANS-04; UML-13/14/15; revue LOT-C0-A | Dossier de revue concret de C0-A, puis mandat d’intégration si approuvé |
| **P1 — fondations** | DEC-R06; UML-01A/05E, puis UML-12/02/06 | Préparer L1-A, C0-B et L1-B sans introduire Preuve dans E01 |
| **P2 — preuves et sources** | DEC-R01–R05; TRANS-03; UML-03/04/05P/07/08/16 | Stabiliser sélections, reprise, identités, compositions et interfaces des sources |
| **P3 — production et gel** | DEC-R08; UML-09/10/18A/11; DEC-R07 pour la promesse supplémentaire | Un résultat documentaire commun et un gel éprouvé face aux pannes |
| **P4 — historique et intégration** | UML-01B/17/18B/19 et LOT-L6 | Nouvelle version, concordances, restitution et communications sans altération historique |

Ces priorités ordonnent le backlog; les vagues P0–P7 du plan UML restent des
vagues de conception. Les décisions P2/P3 peuvent être préparées pendant la
revue de C0-A. Elles ne sont pas des préalables à ses corrections indépendantes.

Pour tout développement : **spécification → quatre vues → validation B →
approbation utilisateur de la version exacte → dépendances satisfaites →
mandat écrit du lot**. Un lot non atterri bloque l’exécution du suivant.

Ordre de livraison recommandé : **C0-A → L1-A → C0-B → L1-B → L2 → L3-A →
L3-B → L4 → L5 → L6**. Il applique la règle d’atterrissage aux dépendances
techniques du registre. L3-B conditionne la capacité PHRASE; un autre ordre
pour des rendus sans PHRASE demanderait un périmètre explicitement approuvé.

**Précision R2 :** les contrats futurs de 10/11/17/18A/18B cités par un lot
antérieur sont des interfaces de conception, pas des fonctionnalités devant
déjà être implantées. Le [rapport §4](RAPPORT_REVUE_COUVERTURE_ET_C0A.md#4-d--trois-graphes-sans-cycle-dexécution)
sépare conception/exécution/validation pour les dix lots et établit l’absence
de cycle d’exécution. Il n’exige pas le use case futur complet pour définir
une interface nécessaire au lot précédent.

## 3. Préparations transversales

Porteurs : B pour la conception et les revues; utilisateur pour les arbitrages,
approbations et autorisations; A pour l’implantation, les corrections et les
tests applicatifs, ainsi que ses références et contrats.
Ces rôles ne constituent ni une sollicitation envoyée à A ni une délégation.

| Ticket | Priorité et dépendances | Travail et livrable | Critères d’acceptation |
|---|---|---|---|
| **TRANS-01** | P0; sans dépendance | Établir le socle de revue C0-A et le contrat fournisseur A. Produire un relevé daté des SHA, différences depuis P6, migrations et capacités HERITE/PHRASE; proposer la référence d’intégration à autoriser. | P6 distingué du HEAD et du déploiement rapporté; patch C0-A comparé aux changements intervenus sans l’appliquer au principal; interfaces, conflits et retour arrière identifiés. Si de nouveaux relevés observés sont nécessaires, les extraire du code nommé en environnement documentaire isolé et conserver explicitement ceux de P6. Aucun contrôle du pilote ou ressource de A modifié. |
| **TRANS-02** | P0 puis enrichissement; TRANS-01 pour l’existant | Produire `modele_global/erd_consolide.puml` et `classes_consolidees.puml`, leurs SVG et le relevé des changements. Première version circonscrite à C0-A; extensions au fil des dossiers. | Existant/proposé/modifié distingués; classes de services séparées des tables; cardinalités, propriété et suppression explicites. Chaque dossier référence une version du modèle global. Les réserves futures restent visibles sans bloquer le périmètre C0-A indépendant. Compilation, contrôle visuel et revue consignés. |
| **TRANS-03** | P2; TRANS-01; contrats D07/CF4 | Vérifier les capacités des sources pour L3-A/B : actes et originaux, fragments complets, Photo→Event, Email/PDF, PHRASE. Produire une matrice source/capacité/preuve/limite. | Contenant vérifié et sélection de photos explicites; texte d’acte certifiable depuis l’original; certification PHRASE effective consommée via A. Les doubles sont identifiés. Les capacités non vérifiées restent indisponibles au strict réel; D07/CF4 ne sont pas déclarées levées sans preuve. Lecture des sources réelles seulement dans un mandat adapté. |
| **TRANS-04** | P0 puis suivi; matrice et registres existants | Tenir les liens exigences → critères → vues → tests → lots et préparer les dossiers de revue/intégration. | Les 38 NR/CF3 sont conservés avec leur affectation; suites E01/A et nouveaux scénarios référencés sans collision. Résultat NON EXECUTE tant qu’aucune exécution ne l’atteste. Chaque rapport futur précise commandes, SHA, base dédiée, résultats et limites. Une preuve ancienne reste datée. |

TRANS-01 ne doit pas attendre un nouveau déploiement de A par principe : il
vérifie les capacités désormais rapportées et leurs références. La récupération
de C et la compatibilité du patch restent à démontrer séparément.

## 4. Décisions et études résiduelles

**D05 CHRONO_VERSION est décidée.** Aucun ticket ne propose de revenir à une
permanence globale des nouvelles cotes. Les associations de juillet demeurent
intactes; P-107 reste la prochaine cote du registre historique, sans devenir
le compteur universel des nouvelles versions.

Pour DEC-R01–R07, B prépare la recommandation et ses exemples; l’utilisateur
tranche les choix fonctionnels. Pour DEC-R08, B justifie d’abord la solution
technique et ses contre-épreuves; son adoption passe par le dossier UML et
l’autorisation du lot. Les recommandations ci-dessous ne sont pas approuvées
par leur inscription au backlog.

| Ticket | Priorité | Question à fermer et recommandation de départ | Sortie vérifiable et chemins concernés |
|---|---|---|---|
| **DEC-R01** | P2 | Continuité d’une pièce lorsque sa composition change : conserver l’identité logique uniquement par décision explicite, avec une nouvelle composition immuable; comparer l’option nouvelle pièce + filiation. | Décision illustrée par `[A,B]→[A,C]`, retrait/réintroduction et scission/fusion; aucune identité déduite de la cote. UML-16/17; variantes de 09/18A/18B. |
| **DEC-R02** | P2; coordonner R01 | Déduplication et compositions simultanées : recommander une composition active par identité logique dans une version, sans fusion automatique d’identités distinctes. | Répétition d’un usage dédupliquée avec tous ses chemins; composites partageant A encore distincts; compositions identiques d’identités distinctes seulement candidates à rapprochement. UML-16/09/17/18A. |
| **DEC-R03** | P2 | Date des composites, dates imprécises et départage : choisir une règle métier traçable sans date d’import de substitution. | Exemples datés/atemporels/à dater, précision conservée, égalités déterministes et refus strict défini; D06 préservée. UML-09/16 et adaptateurs concernés. |
| **DEC-R04** | P2 | Notation des sous-cotes, liasses et fragments : distinguer occurrence source complète, numéro imprimé, sous-cote et cote de version. | Exemples de fragments non contigus, ordre source et réutilisation dans plusieurs composites; notation et références approuvées. UML-08/09/16/18A. L’unité D04 n’est pas rouverte. |
| **DEC-R05** | P2 | Usages analytiques et usages destinés à la production : recommander un choix enregistré, diagnostiqué et indépendant du filtre d’affichage. | Une pièce commune reste produite si un usage retenu l’exige; exclusions explicites; retrait du dernier usage traité. UML-04/16/09; EPIC-V2:T03/T04, C-UML:N16. |
| **DEC-R06** | P1 | Parcours de rédaction et nombre de brouillons actifs : identifier explicitement les branches si plusieurs brouillons sont admis. | Exemples de création et modification concurrentes, propriété des versions et absence d’écrasement; périmètre MVP nommé. UML-01A/01B; C-UML:N12. |
| **DEC-R07** | P3 | Promesse de régénération supplémentaire : distinguer restitution obligatoire des octets conservés et nouvelle génération à environnement maîtrisé. | Niveau de promesse, paramètres et limites documentés; la restitution historique ne dépend jamais d’un recalcul. UML-18B; n’empêche pas la conservation de base. |
| **DEC-R08** | P3; anticiper avant 18A | Backend, droits et récupération du gel : justifier staging durable, fichiers protégés avant finalisation canonique, verrous/recontrôle et reprise idempotente. | Matrice ORM/bulk/SQL/stockage, fenêtres de panne et récupération; aucun état partiel publié; pas de promesse d’atomicité des fichiers déduite d’une transaction SQL. UML-11, contrat de 18A/18B et activation réelle de 19; C-UML:N07–N09. |

Une réserve ne bloque que les chemins qu’elle affecte. Pour livrer un périmètre
partiel, il faut un sous-cas nommé, ses critères, quatre vues et une approbation
explicite; masquer le chemin indécis ne rend pas le use case complet prêt.

## 5. Backlog des user stories et dossiers UML

Chaque ligne est un ticket de dossier, avec une valeur utilisateur et un
résultat d’acceptation distinct. Les dépendances ci-dessous complètent l’ordre
de lecture; le [plan](PLAN_MODELISATION_UML.md#2-inventaire-dépendances-et-ordre-recommandé)
conserve la liste détaillée, y compris les variantes conditionnelles.

**Acceptation commune des 22 tickets UML :**

1. Écrire la spécification et les critères identifiés dans `use_cases/<UC-ID>/`.
2. Fournir activité, séquence, ERD cible et classes : quatre sources `.puml`,
   leurs SVG, compilation et contrôle visuel tracés. Réexaminer les anciennes
   activités; les diagrammes observés P6 ne remplacent pas les vues cibles.
3. Relier chaque critère aux éléments précis des vues, aux scénarios et aux
   lots. Traiter nominal, refus, concurrence, annulation et postconditions.
4. Consigner la revue B technique, fonctionnelle et architecturale, les
   réserves résolues, puis l’approbation utilisateur de la version exacte.
   Mettre le registre à jour avec ses preuves. Toute modification invalidant
   l’approbation retourne à la revue selon le protocole.

Les scénarios dans les colonnes suivantes sont **à préparer et à exécuter lors
des lots autorisés**, pas des résultats acquis. Le minimum prévu est de
88 vues finales; aucun nouveau diagramme n’est produit par ce backlog.

| Ticket / use case | Priorité; lot(s) | User story et résultat d’acceptation particulier | Dépendances essentielles / tests repères |
|---|---|---|---|
| **UML-13 — UC-C-13** | P0; C0-A | Éditer une rédaction PRODUCED en préservant les sources REPRODUCED et la propriété privée. Sous-cas C0A_ISOLER R2-ST approuvé au commit cd584c3 : tout texte différent reçoit un objet neuf; aucune écriture sur l’ancien Statement, pas de schéma nouveau. | TRANS-01/02; NR01/03/11, TR02; fraîcheur sur le Statement effectivement porté, y compris substitution par un autre Statement au même texte. |
| **UML-14 — UC-C-14** | P0; C0-A | Supprimer un bloc autorisé en conservant les captures disponibles; un élément protégé fait refuser toute l’opération. | Contrat de capture UML-13; NR01/11 et partie C0-A de NR12; suppression avec décision incompatible refusée, absence d’effets partiels HTTP. Le journal complet reste hors C0-A. |
| **UML-15 — UC-C-15** | P0; C0-A | Consulter les appuis de la bonne origine documentaire, sans récupérer ceux d’un autre couple partageant un Statement. | TRANS-01/02; NR07, noyau typé de CF3-26; lecteurs/export/archive, types vérifiés et couple explicite, sans anticiper `nature`. |
| **UML-01A — UC-C-01A** | P1; L1-A | Créer un acte ou une analyse interne et sa première version de travail, avec un Document propre et un contexte explicite, sans dépôt fictif. | UML-13/14/15; DEC-R06; VF01/VF08, CF3-01/02/23, C-UML:N12. |
| **UML-05E — UC-C-05E** | P1; L1-A | Examiner la filiation entre occurrences et conserver les décisions successives dans un journal immuable, distinct de leur validité courante. | UML-13/14/15; Correspondance existante; IM01–IM08, CF3-20, NR10/12. Écritures directes/bulk/SQL, concurrence et suppressions couvertes. |
| **UML-12 — UC-C-12** | P1; C0-B/L6 | Consulter la filiation et les décisions éditoriales/probatoires E01, puis savoir quoi réexaminer avant un nouvel export strict. Aucun examen passé inventé. | UML-05E, 13/14/15; NR04–NR10/NR12, TR01–TR06, EX01–EX07. Aucune dépendance obligatoire à Preuve. |
| **UML-02 — UC-C-02** | P1; L1-B | Structurer une rédaction récursive et garder une numérotation cohérente calculée sur le Document entier avant filtrage. | UML-01A, primitives 05E, 13/14; C:T01–T05/T22, NR02, CF3-21; LEGACY/STORED et repères historiques conservés. |
| **UML-06 — UC-C-06** | P1; L1-B; contrôles L5 | Déclarer un renvoi ou une dépendance entre occurrences, suivre les modifications et résoudre les cibles sans inférence automatique. | UML-01A/02/05E; contrat d’état des versions; VF05–VF11, CF3-14–18/21; cycles, cibles absentes et prémisses externes traités. |
| **UML-03 — UC-C-03** | P2; L2 | Organiser une preuve réutilisable en arbre, y compris un appui atomique, sans y déplacer la rédaction ni créer un moteur de raisonnement. | UML-01A/02/13; C:T06/T07/T17/T21, VF13, CF3-08/24; seules les branches de groupe ont des enfants. |
| **UML-04 — UC-C-04** | P2; L2/L3-A | Choisir exactement les éléments utilisés par une cible et leur portée, indépendamment des autres utilisations de la même preuve. | UML-03/02; DEC-R05, CF4 selon type; C:T08/T12/T21, VF03/VF14, CF3-07/08/12/24, EPIC-V2:T03. |
| **UML-05P — UC-C-05P** | P2; L2 | Décider les appuis des utilisations C sans transformer un examen éditorial ou une parenté en validation probatoire. | UML-05E/04/12; NR03/06/12, TR01–TR06, C:T08/T12. Les appuis historiques E01 sont portés par 12 et C0-B. |
| **UML-07 — UC-C-07** | P2; L2; intégration L6 | Reprendre un sous-arbre avec réserves et contexte, décider les usages/prémisses/liens repris et annuler sans copie partielle. | UML-02/03/04/05E/05P/06/12; 08 si insertions, contrat 11 si source figée; CF3-01–CF3-26, VF02–VF05/VF08. Source intacte et carte N:M explicite. |
| **UML-08 — UC-C-08** | P2; L3-B/L4 | Composer une citation fidèle avec omissions/emphases explicites, l’insérer dans la bonne version de texte et réancrer après modification. | UML-02/04; TRANS-01/03, fournisseur A; D07, DEC-R04 selon chemin; C:T09–T11/T18/T19, C:N01/N03–N05, CF3-10/11/26, A:T2.1–T2.9. |
| **UML-16 — UC-C-16** | P2; L3-A; composants L4 | Définir une pièce simple ou composite, conserver sa composition ordonnée et la réutiliser sans fusionner des pièces sur leur source commune. | UML-04; DEC-R01–R05, D04/D07/CF4; EPIC-V2:T03/T10, C-UML:N03–N06/N10/N16; US-C-16, critères AC01–AC08 du plan. |
| **UML-09 — UC-C-09** | P3; L3-A | Obtenir le bordereau et les cotes de la version à partir des seuls usages retenus; insertion ou retrait recalcule le brouillon, jamais l’histoire. | UML-04/16; D06, DEC-R02/03/04 et R05 via la sélection; EPIC-V2:T01–T06/T09/T13/T14, NR08, CF3-24. |
| **UML-10 — UC-C-10** | P3; L3/L4 | Produire texte, références et bordereau depuis une même révision de ResultatVersion, ou recevoir les diagnostics empêchant le strict. | UML-08/09/05P/12; sources vérifiées; EX01–EX07 applicables, TR06, C:T14/T18/T19, EPIC-V2:T02/T13. |
| **UML-18A — UC-C-18A** | P3; L3/L4 | Préparer fichiers, cahier et manifeste ordonnés d’une version, sans les présenter comme gelés ou transmis. | UML-16/09/10; contrat de stockage candidat coordonné à DEC-R08; EPIC-V2:T11/T13, C-UML:N07/N08/N10; critères US-C-18 pertinents. |
| **UML-11 — UC-C-11** | P3; L5 | Finaliser un état cohérent et immuable de la version, de ses cotes, décisions et fichiers, avec reprise sûre après panne. | UML-05E/05P/06/09/10/18A; DEC-R08; EPIC-V2:T07/T11/T12/T14, CF3-16–19/25, IM05/07, C-UML:N07–N09. |
| **UML-01B — UC-C-01B** | P4; L5/L6 | Ouvrir une version amendée depuis un état figé sans modifier les objets ou livrables de la version précédente. | UML-01A/11; DEC-R06; EPIC-V2:T07/T12, CF3-16/18, C-UML:N12. |
| **UML-17 — UC-C-17** | P4; L6; contrats L3-A | Comparer les pièces de deux versions figées : ajouts, retraits, recotations et changements de composition, avec scissions/fusions et ambiguïtés visibles. | UML-16/09/11; DEC-R01/02; EPIC-V2:T08/T09/T10/T14, C-UML:N02/N04/N06/N11; US-C-17, AC01–AC08. |
| **UML-18B — UC-C-18B** | P4; L5/L6 | Retrouver les fichiers historiques conservés avec leur manifeste et leurs empreintes, sans recalcul à partir des relations vivantes. | UML-11/18A; DEC-R07 pour la seule promesse supplémentaire; EPIC-V2:T12/T13/T14, C-UML:N09/N11; critères US-C-18 pertinents. |
| **UML-19 — UC-C-19** | P4; L6 | Consigner plusieurs dépôts ou communications attestés, distincts du gel, avec les seules informations connues et les preuves disponibles. | UML-11/18B; C-UML:T19-01–T19-06, C-UML:N11; US-C-19, AC01–AC06. Un dépôt papier n’acquiert pas une identité de fichier fictive. |

Pour les stories nouvelles, les critères exhaustifs restent dans le
[plan §5](PLAN_MODELISATION_UML.md#5-quatre-stories-complémentaires-proposées), sans
création d’un deuxième jeu de critères dans le backlog.

## 6. Backlog de livraison par lot

Les tickets suivants préparent les futurs mandats. **LOT-C0-A reprend une
livraison isolée existante**; les autres lots ne sont pas ouverts. Les quatre
vues approuvées de tous les use cases touchés et un mandat écrit sont des
préalables communs, y compris pour un sous-lot indépendant.

Les compléments [COV-A à F de la matrice](MATRICE_COUVERTURE_V2_C.md#9-compléments-de-couverture-du-mandat-de-revue-r2)
sont rattachés aux tickets existants : raisonnement à 02/03/04/05P/06/07,
constat d’absence à 03/04/05P, régimes à 03/04/08 et L3-B, recherche à 03,
relais de diagnostics à 04/08/10/18A, anomalies mixtes à 15 et LOT-C0-A.
Leur définition fait autorité dans la matrice; aucune nouvelle story n’est créée.

| Ticket | Priorité; préalables | Périmètre et résultat d’acceptation | Tests et limites de livraison |
|---|---|---|---|
| **LOT-C0-A** | P0; TRANS-01/02/04, UML-13/14/15 approuvés; mandat de revue/intégration | Revoir indépendamment le patch existant, sa conformité aux dossiers et son applicabilité au socle proposé. Rejouer les contre-épreuves en copie Git indépendante et PostgreSQL jetable. Soumettre diff complet, résultats et limites avant intégration autorisée. | NR01/03/07/11, variantes même texte/autre Statement, édition/suppression HTTP et rollback; suites E01 et régime P6, puis fournisseur actuel si socle autorisé. Aucun schéma nouveau, `nature`, journal complet ou gel global réputé livré. Un dépassement des fichiers autorisés est signalé et justifié avant écriture. |
| **LOT-L1-A** | P1; C0-A atterri; UML-01A/05E, DEC-R06; mandat futur | Contexte neutre Acte/VersionActe/analyse, qualification persistante des relations, archive typée et ExamenEditorial immuable. Ajout contrôlé, droits, intégrité et concurrence protègent les décisions. | NR10, CF3-20, IM01–IM08; migration et retour uniquement sur base jetable autorisée. Aucun ancien manifeste inventé; pas d’accès à Preuve; pas de modification des migrations de A. Un périmètre journal seul exigerait un sous-cas approuvé. |
| **LOT-C0-B** | P1; L1-A atterri; UML-12 | Adopter les contrats renforcés dans E01 : lecteurs nature/couple, historique conservé, état courant et admissibilité au strict distincts; réexamen explicite des confirmations sans manifeste. | NR04–NR10/NR12, CF3-19, TR01–TR06, EX01–EX07; aucun réexamen passé fabriqué, aucun appui courant importé de l’histoire. **Ne dépend pas de L2.** |
| **LOT-L1-B** | P1; L1-A disponible et C0-B atterri dans l’ordre proposé; UML-02/06 et primitives rédactionnelles de 07 approuvées | Structure récursive, rôles/présentations, index commun, liens déclarés et copie neutre avec carte N:M, réserves/prémisses décidées. | C:T01–T05/T22, VF06/07/09/10, NR02, CF3-03/04/05/13/14/15/21. Pas d’UP ajoutée par la copie neutre. La reprise probatoire complète attend L2/L6. |
| **LOT-L2** | P2; L1-A/B et C0-B atterris; UML-03/04/05P/07; DEC-R05 pour chemins concernés | Arbres de preuves, utilisations et sélections, appuis de groupe et preuve atomique; détachement d’une preuve partagée avant modification; orchestration explicite et atomique des reprises. | C:T06–T08/T12/T17/T20/T21, VF02/03/05/11–14, CF3-01/02/06–09/12/22/23. Aucun héritage automatique d’appuis; pas de résultat officiel ou de CF3 complet annoncé sans rendus et gel ultérieurs. |
| **LOT-L3-A** | P2/P3; L2 atterri; TRANS-03, UML-16/09, contrats pertinents de 04/10/17/18A; DEC-R01–R05 selon chemins | Adaptateurs, provenance, contenants/fragments, dates et certifications vérifiées; identités/compositions exactes; ResultatVersion et bordereau CHRONO_VERSION communs. | C:N01/N02/N07/N09/N10/N14, VF14, CF3-24; EPIC-V2:T01–T06/T09/T10/T14, C-UML:N03–N06/N15/N16. L’affectation de cote est une responsabilité explicite, distincte de l’identité. Aucune cote de juillet modifiée. |
| **LOT-L3-B** | P2; L3-A atterri dans l’ordre proposé; TRANS-01/03, UML-08 et interface A approuvée | Consommer le fournisseur PHRASE versionné : bornes, trois empreintes et certification effective. Préserver l’isolation HERITE et la navigation contextuelle. | A:T2.1–T2.9, C:T14/T19, C:N03/N04/N14, CF3-26; mutations invalidantes refusées. Ne crée pas à nouveau les services ni les migrations de A. Un double conforme ne certifie aucune source réelle. |
| **LOT-L4** | P3; L3-A/B atterris dans l’ordre proposé; UML-08/10/18A et portion rendu de 16; DEC-R04 selon chemin, contrat candidat R08 | Citations composites, insertions ancrées, éditeur/clean/PDF, cahier et manifeste utilisent la même révision de ResultatVersion. Fichiers candidats ordonnés et identifiés. | C:T09–T15/T18/T22, C:N04/N05, VF04, CF3-10/11/24, EPIC-V2:T02/T11/T13. Réancrage après modification; aucune publication partielle ni transmission implicite. Le gel global reste L5. |
| **LOT-L5** | P3/P4; L1–L4 atterris; UML-11, périmètres 18B/01B et contrôles de 06 approuvés; DEC-R08 | Contenu canonique et fichiers protégés, gardes globales ORM/bulk/SQL/stockage, finalisation avec recontrôle, récupération idempotente; propriété destination de la filiation et isolation des versions. | C:T16/T20, C:N06/N08/N11–N14, VF08, CF3-16–19/25, IM05/07, EPIC-V2:T07/T11/T12/T14, C-UML:N07–N09. Pannes et mutations interdites réellement éprouvées. Aucun gel réel automatique. |
| **LOT-L6** | P4; L1–L5 atterris; UML-01B/07/12/17/18B/19 pour le périmètre intégré; référence A autorisée et récupération vérifiée | Intégration complète : reprises, nouvelle version, concordances éditoriales et documentaires distinctes, restitution historique et événements attestés. Démonstration de bout en bout et récupération C. | Revalidation des 38 NR/CF3, E01/A, C:T01–T22/C:N01–N14, VF01–VF14, IM/TR, EPIC-V2:T01–T14, C-UML:N01–N16/T19-01–06. Juillet et ses fichiers intacts; activation réelle et déploiement exigent leur propre mandat. |

La livraison L3-A inclut les nouveaux contrats de pièces/cotation introduits
par l’avenant; elle ne transforme pas la formulation historique « affectation
officielle séparée » en un onzième lot implicite. Le mandat fixera les fichiers,
capacités et réserves effectivement levées avant toute implantation.

**Définition commune de « lot fait » :** les six conditions du processus
doivent être attestées, sans en remplacer une par un succès isolé :

1. Rapport durable dans `docs/architecture_c/lots/<LOT>/`.
2. Tests affectés réussis sur le socle principal autorisé, avec base de test dédiée.
3. Diff fusionné dans la branche d’intégration, puis dans `main`, sous autorisation.
4. ERD observé régénéré si le schéma change, avec le nouveau SHA.
5. Limites restantes affectées nommément à un lot ultérieur.
6. Journal des lots mis à jour avec les preuves.

## 7. Tests conservés et traçabilité de livraison

Les attentes et contre-épreuves des **38 scénarios** restent intégralement
dans le [registre consolidé §8.1](DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md#81-les-38-scénarios-du-dernier-addendum).
Le tableau suivant en reprend uniquement la responsabilité principale. Les
revalidations intermédiaires détaillées du registre restent obligatoires;
L6 revalide l’ensemble. Aucune des 38 lignes n’est marquée exécutée ici.

| Ticket de livraison | Scénarios sous responsabilité principale |
|---|---|
| LOT-C0-A | NR01, NR03, NR07, NR11 |
| LOT-L1-A | NR10, CF3-20 |
| LOT-C0-B | NR04, NR05, NR06, NR08, NR09, NR12, CF3-19 |
| LOT-L1-B | NR02, CF3-03, CF3-04, CF3-05, CF3-13, CF3-14, CF3-15, CF3-21 |
| LOT-L2 | CF3-01, CF3-02, CF3-06, CF3-07, CF3-08, CF3-09, CF3-12, CF3-22, CF3-23 |
| LOT-L3-A | CF3-24 |
| LOT-L3-B | CF3-26 |
| LOT-L4 | CF3-10, CF3-11 |
| LOT-L5 | CF3-16, CF3-17, CF3-18, CF3-25 |
| LOT-L6 | Revalidation des 38; aucun scénario historique remplacé |

Les scénarios complets NR12, CF3-19 et CF3-25 ne sont pas réputés livrés par
les captures et refus conservateurs de C0-A. Leur acceptation attend C0-B/L5
et leurs revalidations.

Compléments obligatoires, sans renumérotation des suites anciennes :

| Famille | Affectation et finalité |
|---|---|
| E01:T01–T29; régime A applicable au SHA | C0-A puis tous les lots affectant ces comportements, revalidation finale L6 |
| C:T01–T22; C:N01–N14; VF01–VF14 | Lots du registre §7.1 et tickets UML ci-dessus; revalidation L6 |
| IM01–IM08; TR01–TR06; diagnostics EX01–EX07 | L1-A, C0-B, contrôles des utilisations et gel; EX désigne des diagnostics à éprouver, pas une nouvelle suite indépendante |
| EPIC-V2:T01–T06 | L3-A : chronologie, insertions/retraits, pièce commune, départage et datation |
| EPIC-V2:T07/T11/T12 | L4 pour préparation, L5 pour gel et panne; L6 pour nouvelle version et restitution complète |
| EPIC-V2:T08/T09/T10 | L3-A pour identités/compositions; L6 pour concordances entre versions figées |
| EPIC-V2:T13/T14 | L3-A/L4/L5 puis L6 : résultat commun et conservation de juillet |
| C-UML:N01/N13/N14 | Tous les dossiers : porte UML, approbation devenue périmée, relevé observé non substituable à la cible |
| C-UML:N02–N06/N10/N15/N16 | L3-A/L4 puis L6 : identités, compositions, cotes contextualisées, dates et usages produits |
| C-UML:N07–N09 | L4 pour préparation, L5 pour protections/pannes, L6 pour récupération et restitution |
| C-UML:N11 | L5/L6 : histoire de juillet, lacunes assumées et dépôt papier |
| C-UML:N12 | L1-A, L5/L6 : concurrence des brouillons et nouvelles versions |
| C-UML:T19-01–T19-06 | L6 : gel sans envoi, informations attestées, empreintes, événements multiples, papier et correction non destructive |

## 8. Travaux indépendants de la bascule et première suite proposée

La conception des dossiers peut avancer sans attendre une autre intervention
réelle de A : contexte/journal neutres, structure/numérotation, organisation de
preuves, sélection, liens, rendus candidats et protocole de stockage. Les
futurs développements de ces parties peuvent employer des données synthétiques
et des doubles, après approbation UML, mandat et atterrissage du lot précédent.
Cette indépendance technique n’ouvre pas plusieurs lots en parallèle.

La connexion au fournisseur PHRASE exige son contrat/version vérifiés; un rendu
strict réel exige les sources/certifications effectivement valables. La bascule
désormais rapportée ne prouve ni la compatibilité de C ni sa récupérabilité.
Les migrations de A, le pilote, ses contrôles et son retour arrière restent hors
des futurs mandats C sauf autorisation explicite distincte. Les changements C
doivent être isolés, avec leurs migrations futures propres et un plan de
récupération qui conserve l’histoire; le retour arrière de A ne vaut pas pour C.

**Suite concrète recommandée au point R2 :**

1. Prendre acte des livraisons documentaires TRANS-01/02/04 et examiner la
   proposition de socle `515666e`, sans l’assimiler à un mandat d’application.
2. Approbation **UML-13 C0A-UML-R2-ST, sous-cas C0A_ISOLER** reçue; clôturer les revues
   **UML-14 et UML-15**, puis soumettre leurs versions précises à approbation.
3. Après approbation des dossiers, préparer le mandat A de correction et
   validation isolée de **LOT-C0-A** : C0A-REV-01, fichiers exacts, copie Git
   indépendante, PostgreSQL jetable, tests, interdictions et récupération.
4. Après autorisation seulement, A corrige et exécute les tests; B révise la
   conformité. L’intégration et sa destination restent une autorisation
   distincte, puis exigent les six conditions d’atterrissage.
5. Ouvrir ensuite la demande d’autorisation de **L1-A**, avec DEC-R06 et les
   dossiers requis résolus. Aucun passage automatique à L1-A.

Le dossier **UC-C-13** est donc livré pour approbation; le premier lot à
terminer et intégrer reste **C0-A**, avec la correction et les preuves encore
manquantes. Les décisions R01–R08 ne justifient pas de repousser cette clôture
indépendante.

## 9. Journal R1 → R2 et travail suivant

- **Aucun ticket ajouté ou retiré : 44 tickets, 22 use cases, dix lots.**
- R1 est acceptée comme structure provisoire; sa complétude n’est pas présumée.
- TRANS-01 documente les cinq commits depuis P6, les fichiers disjoints, le
  contrôle du patch réussi et la proposition de validation sur `515666e`.
  La destination Git reste à autoriser, sans convergence main/epic décidée.
- TRANS-02 livre les deux modèles G-C0A-R1. Les 12 vues locales de 13/14/15
  sont produites; 13 est validé B documentaire, 14/15 restent en revue.
- TRANS-04 livre les trois tables de traçabilité C0-A; le suivi des autres
  dossiers reste à effectuer. Aucun test applicatif n’est ajouté aux résultats
  historiques P6 par cette livraison documentaire.
- Précision des dépendances : contrats, exécution et validation sont séparés.
  Les interfaces des futurs UC17/18/11 n’exigent pas leur implantation avant
  L3-A/L4. Le graphe d’exécution des dix lots est acyclique.
- Compléments ciblés dans les tickets existants : protocole de constat
  d’absence, consultation qualifiée HERITE, recherche de sources, retour aux
  diagnostics et test transversal du raisonnement. Leur approbation reste
  celle des dossiers; DEC-R01–R08 ne sont pas clos.
- LOT-C0-A / UML-15 : **C0A-REV-01** confirmé, perte des appuis valides en
  présence d’une anomalie locale. Critères AC03/AC06 et test COV:T-F01 à
  réaliser par A après autorisation du périmètre; patch conservé inchangé.

**Prochaine décision proposée au point R2 (remplacée au §10) :** approuver UC-C-13 C0A-UML-R1 dans son
périmètre de conception, examiner les dossiers 14/15 puis autoriser à A la
correction et la validation isolées de C0-A sur le socle exact proposé.
L’intégration demeure une autorisation ultérieure; le lot n’est pas atterri.

## 10. Révision Statement R3-ST

Référence : [invariants ST-R1](INVARIANTS_STATEMENT_REPRODUCED_PRODUCED.md).
Les 44 tickets et 22 use cases sont conservés. Changements ciblés :

- UML-13 : version **C0A-UML-R2-ST**, validation B limitée au sous-cas nommé
  `C0A_ISOLER`, à approuver. AC02/AC03 reformulés, six critères inchangés.
  L’écriture directe d’un privé attesté reste hors activation C0-A.
- LOT-C0-A : le profil de copie sur changement réel diffère du patch conservé,
  notamment de sa branche de modification en place. Écart **C0A-ST-01**, à
  corriger uniquement après autorisation; pas de fermeture implicite des
  rattachements privés par les huit fichiers. **C0A-REV-01 reste ouverte.**
- LOT-L1-A : provenance/propriété durables proposées sur Statement existant,
  attribution contrôlée et fermeture des créations/rattachements/repointages,
  y compris source_type, ORM/bulk/SQL autorisés. Pas de nouvelle entité imposée.
  Audit des anciens objets sans origine déduite de leur usage actuel.
- UML-02/07 et L1-B/L2 : copier un texte PRODUCED crée un nouvel objet même
  identique; réutiliser une source REPRODUCED exige sa provenance attestée.
  Les références probatoires réutilisables restent distinctes des Statement privés.
- UML-14 : conservation d’un propriétaire retiré sans rendre son Statement
  réutilisable; contraintes persistantes à examiner avec L1-A/C0-B.
- UML-15 : lecture historique par couple/type maintenue; aucune autorisation de
  nouveau partage déduite des anciennes associations. Cas mixte C0A-REV-01 distinct.
- `item` sémantique : contexte d’examen en L1-A/C0-B et UC02/05E/12, non garanti
  par la seule fraîcheur textuelle de C0-A. Scénarios ST:T01–ST:T12 dans UC13.

La structure R1 reste acceptée provisoirement; R3-ST ne transforme aucune
proposition technique en décision utilisateur. Le premier lot à clore reste
C0-A, sans dépendance circulaire vers la persistance future de L1-A : le profil
proposé n’utilise pas cette persistance pour décider d’écrire dans l’ancien objet.


## 11. Approbation UC13 enregistrée, sans ouverture de lot

[Décision du 20 octobre 2026](use_cases/UC-C-13/approbation.json) :
UML-13 / UC13::C0A_ISOLER → APPROUVE_UTILISATEUR, version R2-ST, PR #30,
fusion cd584c3, manifeste original archivé avec les 24 fichiers contractuels.
Aucun changement des quatre vues approuvées, aucun ticket ni lot nouveau.
Les propositions « à approuver » des journaux antérieurs sont historiques.
UML-14/15, C0A-ST-01 et C0A-REV-01 restent à traiter. LOT-C0-A n’est pas prêt;
aucun mandat de code ou autorisation de fusion applicative n’est émis.
