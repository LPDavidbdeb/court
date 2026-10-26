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
de livraison et d’intégration. C0-A n’est pas atterri et aucun dossier à quatre
vues n’est encore déclaré validé, approuvé ou prêt au développement.

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
son applicabilité au socle actualisé doit être revérifiée avant intégration
(TRANS-01 du backlog). Les 209 tests du rapport ont été obtenus sur une copie
isolée au socle P6; ils ne valent pas validation du HEAD courant.
