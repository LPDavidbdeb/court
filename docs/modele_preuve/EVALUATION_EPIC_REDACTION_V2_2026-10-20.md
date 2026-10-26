# Évaluation de l’Epic « Rédaction d’actes judiciaires » — proposition V2

**Date :** 20 octobre 2026.  
**Objet :** évaluer la proposition transmise et la comparer aux diagrammes existants.  
**Statut :** avis documentaire; aucune nouvelle approbation architecturale ni autorisation de développement.

## 1. Avis

**La proposition constitue un bon cahier fonctionnel pour la production documentaire. Elle peut compléter l’architecture C, mais ne doit pas la remplacer telle quelle.**

Ses points forts sont la séparation source/pièce/cote, la sélection des seules pièces produites, le résultat commun aux sorties, la conservation complète des versions et la distinction entre gel et communication. Elle rend aussi beaucoup plus explicite la concordance documentaire entre versions.

Quatre points demandent une décision avant de figer les contrats concernés :

1. **D05 :** la proposition choisit une recotation par version, encore non approuvée.
2. **Démonstration :** préciser son articulation avec les utilisations de preuve déjà retenues dans C.
3. **Pièce simple ou composite :** définir son identité et celle de ses compositions successives, y compris les sélections de passages.
4. **Socle Git :** tenir compte des travaux E01 et P6 absents de la référence `main` examinée.

Il n’est pas nécessaire de recommencer l’analyse générale ni de créer une troisième architecture. Je recommande de conserver C, de lui rattacher les douze stories de V2 et d’isoler ces décisions.

## 2. Documents et références comparés

| Ensemble | Ce qu’il représente | Portée de la comparaison |
|---|---|---|
| Proposition V2 transmise | Cahier fonctionnel, référence `main` à `34bc98ac9132b1` | Exigences proposées, développement explicitement non autorisé |
| [Diagrammes historiques 01–05](diagrammes/README.md) | Proposition du 16 octobre, chaîne Démonstration/Poignée | Contexte historique; ils ne constituent pas le contrat C actuel |
| [User stories de l’architecture C](diagrammes/user_stories_architecture_c/README.md) | Cible C et parcours C0-A isolés | Contrats architecturaux approuvés avec leurs réserves; lots ultérieurs à autoriser |
| [ERD du système](diagrammes/erd_etat_actuel/README.md) | Modèles Django au commit P6 `212a7feee81aef46a5b43d36e8eeafe0f8870064` | État déclaré du code à cette référence, sans inspection de la base réelle |

Le mandat utilisateur d’approbation de C reste la référence pour les décisions : D05 demeure en arbitrage; D07 et CF4 sont conditionnelles; C0-A ne réalise ni le journal immuable de L1-A, ni l’adoption C0-B, ni le gel global de L5.

La liste des travaux du §8 de V2 est évaluée comme une proposition de préalables. Elle ne constitue pas une instruction d’implémenter ces travaux dans le présent mandat.

## 3. Écart de socle : `main` et l’ERD ne décrivent pas la même révision

La vérification locale des objets Git confirme :

- référence de V2 : `34bc98ac9132b1fee12b0946a8a93b19a5a1d702`, fusion du 13 octobre 2026;
- référence de l’ERD et du socle P6 : `212a7feee81aef46a5b43d36e8eeafe0f8870064`;
- ancêtre commun : `7b260819e56686b773a56f2abea7fd0355392952`;
- historique divergent : un commit propre à la référence `main` examinée et 26 propres à P6, selon `git rev-list --left-right --count`.

**La référence `main` de V2 ne contient pas plusieurs structures pourtant présentes dans notre ERD.** Il s’agit d’un écart entre branches, pas d’une preuve de suppression dans la base ou d’un état certifié de GitHub aujourd’hui.

| Présent dans P6, absent de la référence `main` de V2 | Conséquence |
|---|---|
| `Cause`, `EtatCause`, `LienCause` | Le contexte judiciaire neutre ne doit pas être redessiné en ignorant ces travaux |
| `ReferentHistorique`, `InstantaneReferent`, `InstantaneNoeud`, `VersionTexte` | Réutiliser les responsabilités historiques et de capture disponibles, sans les confondre avec le futur gel complet |
| `Correspondance`, `ExtremiteCorrespondance`, `NoeudArchive` | Préserver la concordance rédactionnelle et les archives E01 |
| `ConfirmationAppui`, `AncrageCitation` | Étendre les examens et références existants plutôt que repartir d’un système supposé dépourvu de ces fonctions |
| `Document.numbering_mode`, `LibraryNode.paragraph_number` | Maintenir les contrats de numérotation E01 et les repères imprimés |
| `Document.cause_origine`, `Email.cause_origine`, `Document.notes` | Conserver les métadonnées et la distinction origine/utilisation |
| `Quote.regime` dans les deux applications de citations | Préserver la séparation HERITE/PHRASE et les travaux de l’Agent A |

L’ERD reste exact pour P6; il ne faut pas le renommer « ERD de main ». Il ne contient pas encore les futures tables de C et ne prouve pas les garanties comportementales d’immutabilité.

Deux réutilisations doivent particulièrement être encadrées :

- [`ProducedExhibit`](../../case_manager/models.py) est une représentation temporaire reconstruite. Son nom ne suffit pas à en faire la future identité immuable d’une `PieceProduite`.
- [`Transmission` et `FichierTransmis`](../../case_manager/models.py) fournissent déjà destinataire, date, noms et empreintes, mais ne sont pas rattachés à une `VersionActe`. Ils couvrent une partie d’US-12, pas son contrat complet.

Le service de cotation existant est également un point de départ, pas une implémentation conforme à réutiliser sans adaptation : il parcourt le registre de juillet et possède notamment un repli sur `created_at`. V2 et D06 demandent le périmètre effectif d’une version et des dates métier vérifiées.

La comparaison de branches demandée au §8 de V2 est donc justifiée. Elle doit préparer une intégration ultérieure, sans modifier la cible P6 validée, le pilote de A ni ses conditions de retour arrière.

## 4. Correspondance des douze user stories

Les numéros `US-xx` ci-dessous appartiennent à V2; les `US-C-xx` appartiennent aux diagrammes C. Une correspondance signifie une proximité de contrat, pas une fonction déjà implémentée.

| Story V2 | Diagrammes C correspondants | Évaluation et complément nécessaire |
|---|---|---|
| **US-01 — Actes et versions** | [US-C-01](diagrammes/user_stories_architecture_c/01_contexte_versionne.puml), [US-C-11](diagrammes/user_stories_architecture_c/11_gel_conservation.puml) | Compatible. « Un seul brouillon actif par parcours » est une nouvelle contrainte : définir le parcours et les branches. Conserver les analyses internes autonomes. |
| **US-02 — Rédaction structurée** | [US-C-02](diagrammes/user_stories_architecture_c/02_structure_numerotation.puml), [US-C-13/14](diagrammes/user_stories_architecture_c/README.md#us-c-13--modifier-une-occurrence-partagée--c0-a) | Compatible. Expliciter le détachement des textes partagés, la fraîcheur sur le Statement réellement porté, les refus atomiques et la numérotation historique conservée. |
| **US-03 — Démonstrations et preuves** | [US-C-03](diagrammes/user_stories_architecture_c/03_organiser_preuve.puml), [US-C-04](diagrammes/user_stories_architecture_c/04_selection_effective.puml), [US-C-05](diagrammes/user_stories_architecture_c/05_rattachement_examen.puml) | Plusieurs appuis sont compatibles. La Démonstration doit être définie sans recréer une autorité concurrente pour les propositions et conclusions. |
| **US-04 — Pièces à produire** | US-C-03/04, [US-C-09](diagrammes/user_stories_architecture_c/09_bordereau_cotation.puml) | Bonne séparation entre classement et utilisation. Compléter l’identité des assemblages et le passage explicite de l’utilisation analytique à la production. |
| **US-05 — Cotation dynamique** | US-C-09 | **Écart décisif : D05 non arbitrée.** Le diagramme conserve cette réserve; V2 propose de la lever dans le sens CHRONO_VERSION. |
| **US-06 — Références dans le texte** | [US-C-08](diagrammes/user_stories_architecture_c/08_citation_composite.puml), [US-C-10](diagrammes/user_stories_architecture_c/10_rendu_strict.puml) | Compatible pour les références actives qualifiées par version. Maintenir les cotes littérales historiques, les ancrages et le réancrage après modification. Une référence de pièce ne remplace pas une citation textuelle certifiée. |
| **US-07 — Gel** | US-C-11 | Très bonne convergence. AC08 rend explicite la cohérence entre base et stockage; ajouter les fenêtres de panne, reprises et protections contre les mutations directes. |
| **US-08 — Concordance des pièces** | US-C-09/11 et [US-C-12](diagrammes/user_stories_architecture_c/12_concordance_historique.puml), partiellement | **Complément substantiel aux diagrammes.** US-C-12 traite surtout la filiation éditoriale et ses examens. Il manque un parcours dédié couvrant toutes les pièces, cotes et compositions de deux versions. |
| **US-09 — Bordereau** | US-C-09/10 | Compatible avec le résultat commun et la sélection effective. Les cotes nouvelles et sous-cotes actives restent soumises à D05. |
| **US-10 — Exportation** | US-C-10/11 | Compatible. Le manifeste ordonné de fichiers par pièce mérite d’être rendu plus visible. Distinguer restitution des fichiers conservés et nouvelle génération avec un moteur actuel. |
| **US-11 — Version amendée** | US-C-01/11, [US-C-07](diagrammes/user_stories_architecture_c/07_reprise_partielle.puml) | Compatible pour le nouveau brouillon; recotation conditionnelle à D05. La copie complète d’une version ne remplace pas la reprise partielle CF3 avec décisions de contexte. |
| **US-12 — Dépôt et communication** | US-C-01/11/12 | Bonne convergence. Mérite un parcours dédié pour plusieurs communications d’une même version, leurs preuves et les modalités papier. |

## 5. Arbitrages et précisions ciblées

### 5.1 D05 : la proposition choisit une politique, elle ne l’approuve pas

INV-04, US-05, US-11 et l’exemple V1/V2 sont cohérents entre eux : une même pièce change de cote et une même cote désigne des pièces différentes selon la version.

Ce choix est techniquement cohérent si la cote est **locale à un bordereau/version**. Il diffère de la permanence globale actuellement approuvée dans la [méthodologie, §3.3](../../legal/METHODOLOGIE_POST_DEPOT.md). Préserver uniquement les associations de juillet ne règle pas, à lui seul, la portée de cette règle pour les versions futures.

**Recommandation :** si le recalcul intégral est bien l’objectif retenu, approuver explicitement CHRONO_VERSION pour les nouvelles versions désignées, avec :

- identité permanente de la pièce distincte de son libellé;
- référence active qualifiée par le bordereau/version;
- distinction visible entre référence active et citation historique littérale;
- conservation des associations, paramètres et artefacts de chaque version figée;
- concordance documentaire exportable, y compris les changements de composition;
- aucune réécriture du registre, du verrou ou des archives de juillet.

Sinon, conserver les cotes permanentes et dissocier leur valeur de l’ordre chronologique de présentation. L’exemple de V2 et les critères de recotation devront alors être adaptés. La remise de cette proposition pour évaluation ne tranche pas D05.

### 5.2 Démonstration : conserver une seule autorité sur le raisonnement

V2 autorise plusieurs démonstrations par paragraphe : elle ne réintroduit donc pas la limite 0..1 du [schéma historique](diagrammes/02_schema_nouveau_pont.puml).

Elle remet toutefois au premier plan une chaîne Démonstration → Preuve. Dans C, les propositions, conclusions et réserves restent dans la rédaction; les preuves organisent les sources; les `UtilisationPreuve` et leurs sélections portent les rattachements.

**Recommandation :** interpréter d’abord « démonstration » comme une organisation rédactionnelle et une présentation des usages de preuve. Un regroupement de plusieurs usages est envisageable sans imposer d’emblée une nouvelle table. Le §5 de V2 laisse justement cette liberté.

Si une démonstration doit avoir sa propre identité, son texte de raisonnement et sa réutilisation indépendants de la rédaction, le besoin est une évolution de D01/D02/D12 à décider expressément. Il faut alors désigner l’autorité du texte, ses règles d’édition et de gel, plutôt que dupliquer les conclusions dans `Preuve`.

### 5.3 Pièces composites : distinguer identité, composition et fichier

INV-02 signale lui-même le contrat restant à définir. Le couple modèle/PK identifie une source; il ne définit pas à lui seul une pièce composée de plusieurs sources ou passages.

Il faut au minimum distinguer les responsabilités suivantes, sans imposer leur traduction en tables :

| Responsabilité | Contrat nécessaire |
|---|---|
| Identité de source | Modèle qualifié par application et PK; une clé de ContentType locale n’est pas une identité portable suffisante |
| Identité de pièce | Identité stable de l’unité produite, indépendante de sa cote |
| Composition versionnée | Composantes ordonnées, identités et états sources, passages retenus, contenants et paramètres de composition |
| Artefact | Octets effectivement produits, nom, format et empreinte, reliés à la composition et à la version |

Exemple : une liasse `[A, B]` devenant `[A, C]` ne peut être déclarée inchangée parce qu’elle conserve son nom ou sa cote. Une famille de pièce peut conserver une filiation, mais sa composition exacte a changé. Il faut choisir si le produit reçoit une nouvelle identité ou une nouvelle révision immuable, puis qualifier la concordance en conséquence. Ordre modifié, scission et fusion demandent également un traitement explicite.

Pour un passage d’acte, D04 conserve l’occurrence source complète comme unité de fragment. Une sélection de passages peut être une composition de ces unités. Si V2 veut faire d’une découpe arbitraire une nouvelle unité cotée autonome, elle élargit le contrat et exige une décision, particulièrement pour les recouvrements et la déduplication.

Une citation composite dans un paragraphe et une pièce composite dans un dossier de production sont deux objets différents. Le diagramme US-C-08 ne couvre pas, à lui seul, l’identité des liasses de V2.

La date de classement d’une pièce composite doit aussi être définie : première composante, dernière composante ou date propre vérifiée ne sont pas équivalentes. Conserver D06 : précision et provenance explicites, sans repli silencieux sur la date d’import; une date requise non établie bloque le strict concerné.

### 5.4 Analyse, sélection et production : rendre la frontière explicite

US-04 AC06 est utile. Il ne faut toutefois pas qu’un simple filtre d’affichage retire implicitement une pièce du dossier.

La chaîne recommandée reste : **sources classées → sélections effectives des usages → unités documentaires retenues pour la production**. Les sources seulement classées restent hors production. Un usage analytique doit être identifié comme tel; sa transformation en appui plaidé doit déclencher les contrôles pertinents.

Conserver les chemins d’usage : supprimer l’un de deux usages ne retire pas leur pièce commune; une branche non sélectionnée n’entre pas dans le résultat. L’appui d’un regroupement n’est pas automatiquement celui de ses enfants. La dérogation éventuelle permettant de conserver un appui plaidé sans produire sa pièce doit être explicite et diagnostiquée.

### 5.5 Gel et restitution : préciser le résultat observable

US-07 AC08 est une exigence utile. Une transaction PostgreSQL ne suffit pas à rendre atomiques toutes les écritures du stockage de fichiers.

Le protocole de L5 doit garantir qu’une version n’est visible comme finalisée qu’avec tous ses objets et fichiers vérifiés, que les reprises après panne sont idempotentes et que le nettoyage ne détruit aucun livrable déjà finalisé. Les contre-épreuves doivent couvrir les pannes avant et après finalisation, ainsi qu’une modification concurrente.

Les empreintes détectent une altération; elles ne l’interdisent pas. Les protections du journal d’examens dès L1-A restent distinctes des protections de tout l’agrégat gelé en L5, avec vérifications ORM, bulk, SQL et stockage.

Pour US-10 AC10, je recommande que la restitution historique serve les fichiers effectivement conservés. Une régénération avec une autre version de moteur, de police ou de bibliothèque peut produire d’autres octets : elle doit rester un dérivé identifié, sans remplacer silencieusement l’artefact historique.

### 5.6 Brouillons et communications

US-01 AC04 doit définir « parcours de rédaction ». Une seule version active par acte et plusieurs branches actives explicitement identifiées sont deux règles différentes. La création concurrente de brouillons doit respecter la règle choisie.

US-12 AC05/06 est à conserver : geler ne signifie pas déposer ou envoyer. Le dépôt de juillet est un acte papier; les fichiers conservés sont une source d’impression. Une importation historique conserve les preuves et lacunes disponibles et ne fabrique ni démonstrations déposées, ni examens, ni identité numérique parfaite avec le papier.

## 6. Contrats C à conserver comme exigences transversales

V2 ne les contredit pas nécessairement, mais son adoption comme cahier unique les ferait perdre sans rattachement explicite :

- **CF1 :** analyses internes autonomes, gelables sans transmission; origine d’une source distincte de la cause d’utilisation.
- **D01/D02/D11 :** cibles proposition ou regroupement, usages multiples avec sélections explicites, appui simple sous le même contrat, sans héritage automatique.
- **CF2 :** renvois et dépendances déclarés, cycles contrôlés, sans inférence automatique ni import implicite des appuis.
- **CF3 :** reprise partielle avec réserves, prémisses externes, contexte, occurrences nouvelles et cartes N:M décidés explicitement.
- **CF3-D1/D2 :** filiation qualifiée par nature et couple documentaire, examens éditoriaux distincts des confirmations d’appui, décisions conservées; aucun ancien manifeste inventé. Une décision historique compatible aujourd’hui ne suffit pas automatiquement au nouvel export strict.
- **D03/D09 et C0-A :** structure neutre, numérotation contextuelle et historique préservée, détachement avant édition, fraîcheur sur le Statement réel, archives utiles et refus atomiques.
- **D04/D07/D10/CF4 :** fragment source complet, fidélité sur original, ancrages et citations exactes; contenants Photo→Event vérifiés et certification PHRASE dépendante des capacités réellement livrées par A.
- **D08 :** conservation canonique complète et protection des objets et fichiers; une modification de preuve engagée dans un gel passe par la copie entière prévue dans C.

Ces contrats peuvent être référencés par une courte annexe de traçabilité. Il n’est pas nécessaire de recopier toute la conception.

## 7. Évolution recommandée des diagrammes

| Diagramme | Évolution utile après décisions |
|---|---|
| US-C-01 | Ajouter la règle choisie pour le brouillon actif et les branches |
| US-C-03/04/05 | Clarifier le sens de Démonstration et le passage usage analytique → production, en conservant les autorités C |
| US-C-09 | Brancher la politique D05 effectivement approuvée; montrer pièce, composition, date et cotation de version |
| **Nouveau parcours dédié** | Concordance documentaire exhaustive : union des deux bordereaux, identités, ajouts/retraits/recotations, compositions modifiées, scissions/fusions et ambiguïtés |
| US-C-10/11 | Détailler le manifeste de fichiers, les fenêtres de panne, la reprise et la restitution historique |
| **Nouveau parcours dédié** | Dépôts et communications multiples, preuves disponibles et modalités papier |
| ERD P6 | Conserver le relevé observé; produire ultérieurement un schéma cible séparé et un nouveau relevé après intégration réelle |

Le nouveau parcours documentaire ne remplace pas US-C-12 : **la concordance des pièces et des cotes, la filiation éditoriale et l’examen des appuis répondent à des questions distinctes**.

Les anciens diagrammes 01–05 restent historiques. Leur copie du chemin, leur chaîne Démonstration/Poignée et leur association gel/dépôt ne doivent pas redevenir les contrats C par simple réemploi graphique. Leur recotation dessinée n’était pas une approbation de D05.

## 8. Tests : apports de V2 et rattachement aux lots

Les quatorze scénarios sont pertinents comme tests de bout en bout minimaux. Les nommer **`EPIC-V2:T01` à `EPIC-V2:T14`** éviterait la collision avec les identifiants de tests antérieurs. **Aucun n’a été exécuté dans cette évaluation.**

| Scénarios V2 | Lots concernés | Condition ou complément |
|---|---|---|
| T01/02/04 — Ajouts, retrait final, recotation et renvois | L3-A, L4, L6 | Attentes de recotation soumises à D05 |
| T03 — Dernier usage ou usage restant | L2, L3-A, L6 | Compter les usages effectifs, pas les seules occurrences classées dans une preuve |
| T05/06 — Égalités et dates particulières | L3-A, L6 | D06; ajouter la date des composites, les précisions et les corrections de date entre versions |
| T07 — Intégrité de V1 après modification de V2 | L1/L2, L5, L6 | Textes, preuves partagées, sélections, décisions, fichiers et paramètres |
| T08/09/10 — Concordance et composition | L3-A, L6 | Identité/composition préalablement décidées; D05 pour les changements de cote; scissions, fusions et ordre modifié |
| T11 — Échec après préparation des fichiers | L5, L6 | Plusieurs fenêtres de panne, reprise et concurrence; pas seulement une exception avant le commit |
| T12 — Restitution historique | L5, L6 | Lire les associations et fichiers conservés; ne pas reconstruire l’histoire depuis les sources actuelles |
| T13 — Cohérence des sorties | L3/L4, L6 | Même ResultatVersion; conserver aussi les contrôles de citations et les littéraux historiques |
| T14 — Préservation de juillet | C0-A/C0-B pour leurs protections, L5/L6 pour l’ensemble | Ne pas présenter le test global comme déjà satisfait par C0-A |

Les 38 scénarios NR01–NR12 et CF3-01–CF3-26, les contrôles IM/TR et les non-régressions E01/A restent nécessaires. V2 ne s’y substitue pas.

Contre-épreuves particulièrement utiles à garder visibles : substitution du Statement par un autre de texte identique; collision de PK entre types; suppression refusée sans effet partiel; examen ancien sans manifeste; modification SQL/bulk d’un examen ou objet gelé; dérive de certification; deux finalisations concurrentes; brouillons concurrents; référence à une pièce d’une autre version; absence de fichier original ou de preuve d’identité avec le papier.

## 9. Décision et suite recommandées

**À retenir dès maintenant comme compléments proposés à C :** les douze stories comme organisation du besoin, la distinction source/pièce/cote, le résultat commun, la concordance documentaire exhaustive, les manifestes de composition/fichiers et les communications distinctes du gel. Leur adoption reste une décision du demandeur.

**À trancher :** D05; le rôle de Démonstration; l’identité et la révision des pièces composites; la portée des sélections de passages; la règle du brouillon actif. La définition du périmètre analytique/produit et la date des composites peuvent être précisées dans les contrats de services correspondants.

**Préalable d’intégration :** établir une référence autorisée tenant compte de P6, de l’évolution des citations par A et du résultat de la revue C0-A. La référence `main` de V2 est insuffisante, seule, pour conserver tous ces acquis. Cette évaluation ne change aucune cible ni condition de retour arrière.

**Progression possible sans attendre toute la cotation :** après revue de C0-A et mandat séparé, L1-A demeure le prochain lot du plan accepté; structures neutres, filiation qualifiée et journal d’examens peuvent avancer isolément. La préparation des structures, sélections, adaptateurs non PHRASE et rendus avec doubles peut suivre les dépendances du plan, sans attendre la bascule réelle de A. L’activation PHRASE, la cotation officielle et l’intégration réelle gardent leurs propres préalables et autorisations.

Il n’y a donc pas lieu de rouvrir l’ensemble de la conception. Il faut compléter la traçabilité de V2 vers C et décider ces points circonscrits avant les lots qui en dépendent.

## 10. Vérifications effectivement réalisées

- Lecture de la proposition V2, des diagrammes historiques, des parcours C pertinents, du relevé ERD, des décisions consolidées et des règles de continuité applicables.
- Inspection locale en lecture seule des deux commits, de leur ancêtre commun, de leurs historiques et des différences de modèles et migrations.
- Comparaison statique par AST des déclarations de champs des fichiers `models.py` aux deux références; consultation des services de numérotation, cotation, concordance, références et production concernés.
- Empreinte SHA-256 de la proposition reçue : `4649e11ec5d721ec1e3596d930de729ddd39ad664b373da0cdafe561593a0da1`.

Cette vérification ne consulte ni la base réelle ni le serveur, ne certifie pas les migrations appliquées et ne lance aucun test applicatif. Les résultats C0-A cités par les diagrammes restent ceux du rapport isolé antérieur, sans réexécution ici. Seule cette note est ajoutée; aucun diagramme ou document antérieur n’est remplacé, aucun code ni migration n’est modifié, aucun commit ou push n’est effectué.
