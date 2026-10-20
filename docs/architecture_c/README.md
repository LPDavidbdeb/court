# Architecture C — corpus de décision et dossiers UML

Les rapports initiaux ont été rapatriés dans le dépôt le **20 octobre 2026** depuis
`/private/tmp/court-agent-b-validation-c-20261019/` et
`/private/tmp/court-agent-b-c0a-20261019-bmr16wwh/artifacts/`, où ils étaient
exposés à la purge du système. Le registre et le processus ont ensuite été
révisés explicitement sous **C-UML-2026-10-20-R1**; leurs états antérieurs exacts
sont conservés dans [l’historique](historique/2026-10-20_avant_consolidation/README.md).

**Décision actuelle : D05 CHRONO_VERSION.** Les nouvelles versions recotent les
pièces retenues; chaque état figé garde ses associations historiques. La
permanence de juillet demeure entière. Les détails résiduels R01–R08 ne sont
pas automatiquement approuvés.

**Porte obligatoire : quatre vues UML par use case, validation B puis
approbation utilisateur, avant toute implantation.** Le lot demeure l’unité
de livraison et d’intégration. C0-A n’est pas atterri. UC-C-13 possède quatre
vues **C0A-UML-R2-ST, approuvées utilisateur pour le seul sous-cas C0A_ISOLER** le 20 octobre 2026 (cd584c3 / PR #30); UC-C-14 et 15
restent en revue. Aucun dossier n’est prêt au développement. [Décision UC13 et exclusions](use_cases/UC-C-13/approbation.json).

## Révision des invariants Statement

Le [contrat ST-R1 et son analyse du code](INVARIANTS_STATEMENT_REPRODUCED_PRODUCED.md)
conservent la décision utilisateur : seule une origine REPRODUCED attestée
permet la réutilisation d’un Statement; les contenus PRODUCED sont privés.
Les usages actuels ne prouvent pas l’origine et le rattachement générique
permet encore un partage privé interdit. Le profil UC13 proposé crée donc
un objet neuf sur tout changement réel de texte, sans écrire sur l’ancien.
La propriété persistante et la fermeture de tous les rattachements relèvent
de L1-A; l’effet sémantique de `item` reste à spécifier dans L1-A/C0-B.

Le [dossier approuvé pour C0A_ISOLER](use_cases/UC-C-13/specification.md), sa
[validation bornée](use_cases/UC-C-13/validation.md) et ses empreintes remplacent
la proposition R1. **Le patch n’est pas modifié : C0A-ST-01 signale son écart
au profil proposé; C0A-REV-01 reste ouverte séparément dans UC15.** L’historique
précédent est [conservé avec empreintes](historique/2026-10-20_avant_invariants_statement_R2/README.md).

## Revue de couverture et préparation de C0-A

Le [rapport de revue](RAPPORT_REVUE_COUVERTURE_ET_C0A.md) répond aux six questions
de couverture et établit TRANS-01. Le [backlog R3-ST](BACKLOG_ARCHITECTURE_C.md)
conserve 44 tickets et 22 use cases; la matrice ajoute neuf critères ciblés
sans nouvelle story. Les étapes de conception, exécution et validation des
lots sont distinguées.

Le [modèle global G-C0A-R2-ST](modele_global/README.md) et les dossiers
[UC-C-13](use_cases/UC-C-13/specification.md),
[UC-C-14](use_cases/UC-C-14/specification.md),
[UC-C-15](use_cases/UC-C-15/specification.md) fournissent 14 vues PlantUML
compilées, leurs SVG, PNG de contrôle, critères et traçabilité. La révision ST
a régénéré les quatre vues 13 et les deux globales; les huit vues 14/15 restent
celles de R1. L’attestation B de 13 porte uniquement sur C0A_ISOLER;
aucune approbation utilisateur n’est déduite.

**Le patch C0-A passe le contrôle statique sur `515666e`, mais C0A-REV-01
reste à corriger sous autorisation : une anomalie locale peut effacer les
appuis valides de la lecture.** Le patch est conservé inchangé et les tests
applicatifs sur le nouveau socle ne sont pas exécutés. L’intégration reste
à mandater après correction et revue.

## Livraison de consolidation

| Livrable | Autorité et contenu |
|---|---|
| [A — Avenant](AVENANT_ARCHITECTURE_C.md) | Nouveaux contrats de pièces/compositions, D05, concordance et production; réserves à trancher |
| [B — Couverture V2/C](MATRICE_COUVERTURE_V2_C.md) | 8 invariants, 91 critères, 14 scénarios V2, scénarios complémentaires et conservation des tests antérieurs |
| [C — Plan UML](PLAN_MODELISATION_UML.md) | 22 use cases et leurs quatre vues, disponibilités/manques, dépendances et ordre |
| [D — Protocole](PROTOCOLE_VALIDATION_UML.md) | Contrôle préalable opposable, transitions, approbation et conformité |
| [E — Rapport](RAPPORT_CONSOLIDATION_ET_VALIDATION.md) | Références Git vérifiées, impacts, risques, limites et premier passage proposé |

Le [registre de validation](registre_validation.md) porte le statut courant de
chaque dossier. Le [gabarit](use_cases/MODELE_DOSSIER.md) prépare les dossiers;
les [sources reçues](references/README.md) conservent le mandat et V2.

Le [backlog opérationnel](BACKLOG_ARCHITECTURE_C.md) ordonne les décisions
résiduelles, les 22 dossiers UML et les 10 livraisons de lots. Il précise les
préalables, critères d’acceptation et tests, en commençant par la revue et
l’atterrissage de C0-A; il n’autorise aucun développement supplémentaire.

## Registre et rapports antérieurs

Le registre actif porte les statuts D/CF; l’avenant définit les contrats
complémentaires. Les deux analyses fonctionnelles antérieures restent des
sources de conception, sans supplanter D05 décidée ni constituer une validation
des nouveaux dossiers UML.

| Fichier | Contenu |
|---|---|
| [`DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md`](DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md) | registre actif D01–D12, CF1–CF4, CF3-D1–D6 révisé; plan des lots (§ 7.1); périmètre historique du premier mandat (§ 10.5) |
| [`VALIDATION_FONCTIONNELLE_ARCHITECTURE_C.md`](VALIDATION_FONCTIONNELLE_ARCHITECTURE_C.md) | validation fonctionnelle de la cible |
| [`CF3_COMPATIBILITE_CONCORDANCES_E01.md`](CF3_COMPATIBILITE_CONCORDANCES_E01.md) | compatibilité de la reprise partielle avec les concordances E01 |
| [`lots/C0-A/`](lots/C0-A/) | livraison du lot C0-A : rapport, diff complet, vérifications |

Lectures associées : [`../PROCESSUS_CHANGEMENT.md`](../PROCESSUS_CHANGEMENT.md)
pour la façon dont un lot est mandaté puis intégré,
[`../modele_preuve/diagrammes/user_stories_architecture_c/`](../modele_preuve/diagrammes/user_stories_architecture_c/)
pour les parcours, et
[`../modele_preuve/diagrammes/erd_etat_actuel/`](../modele_preuve/diagrammes/erd_etat_actuel/)
pour l'état du schéma au SHA `212a7fe`.

Les diagrammes de [classes observées](../modele_preuve/diagrammes/classes_etat_actuel/README.md)
complètent l’ERD P6. Les anciennes activités de C et ces relevés observés ne
remplacent pas les quatre vues cibles par use case. L’[évaluation V2 antérieure](../modele_preuve/EVALUATION_EPIC_REDACTION_V2_2026-10-20.md)
précède la décision D05 du nouveau mandat; ses mentions d’un arbitrage de
principe restent historiques.

Le lot C0-A **n'est pas intégré** : son diff existe en fichier `.patch` et
son contrôle d’application statique sur `515666e` réussit (TRANS-01). Sa
conformité fonctionnelle et C0A-REV-01 restent à traiter avant intégration. Les 209 tests du rapport ont été obtenus sur une copie
isolée au socle P6; ils ne valent pas validation du HEAD courant.


## Approbation reçue et version conservée

[Décision utilisateur du 20 octobre 2026](use_cases/UC-C-13/approbation.json),
PR #30 et fusion cd584c3 : C0A_ISOLER C0A-UML-R2-ST seulement.
La [copie exacte du manifeste et de ses 24 fichiers](versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md)
préserve l’état approuvé. Les autres dossiers et évolutions globales n’héritent
pas de cette approbation; aucun mandat d’implantation n’est émis.
