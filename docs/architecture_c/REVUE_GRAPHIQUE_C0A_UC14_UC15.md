# Revue graphique C0-A — UC14, UC15 et comportements liés aux citations

**Suivi du 20 octobre 2026 — UC14 et UC15 APPROUVE_UTILISATEUR au commit 30724df / PR #31.**
[Décision source](references/MANDAT_APPROBATION_UC14_UC15_PREPARATION_C0A_2026-10-20.md) ·
[UC14 exact conservé](versions_approuvees/UC-C-14_C0A-UML-R2-HIST/README.md) ·
[UC15 exact conservé](versions_approuvees/UC-C-15_C0A-UML-R2-DIAG/README.md).
L’approbation UC13::C0A_ISOLER C0A-UML-R2-ST est enregistrée séparément
(commit af52eef), au manifeste de la PR #30 / cd584c3.
[Décision et exclusions](use_cases/UC-C-13/approbation.json) ·
[Version approuvée préservée](versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md).
Ses quatre sources et huit rendus sont inchangés. Aucun lot prêt au développement.

| Dossier | Version / revue B | Décision utilisateur |
|---|---|---|
| [UC14 — suppression](use_cases/UC-C-14/specification.md) | R2-HIST, VALIDE_ARCHITECTURE pour l’option conservatrice C14-D1/D2 | [APPROUVE_UTILISATEUR, C14-D1/D2](use_cases/UC-C-14/approbation.json) |
| [UC15 — appuis d’origine](use_cases/UC-C-15/specification.md) | R2-DIAG, VALIDE_ARCHITECTURE pour le contrat C15-D1 | [APPROUVE_UTILISATEUR, C15-D1](use_cases/UC-C-15/approbation.json) |
| [UC02::RENOMMER_CITATION](use_cases/UC-C-02/RENOMMER_CITATION/specification.md) | CIT-UML-R1, EN_REVUE; quatre vues | CIT-D1/D2 ouverts |
| [UC12::DIAGNOSTIQUER_EXAMEN](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/specification.md) | CIT-UML-R1, EN_REVUE; quatre vues + états | CIT-D3/D4 ouverts |
| [Modèle consolidé C0-A](modele_global/README.md) | G-C0A-R3-CIT proposé; deux vues | Aucune approbation transférée de G-R2 |

Les diagrammes ci-dessous sont les artefacts centraux. Ouvrir les SVG pour
zoomer sur les grands schémas. Les sources PlantUML, SVG et PNG sont conservés.
Les 38 anciens scénarios NR/CF3 et 38 nouveaux scénarios C14/C15/CIT restent
planifiés; aucun essai applicatif nouveau n’est exécuté dans ce mandat.

## A. UC14 — suppression sans perte

**C14-D1 approuvé :** supprimer les occurrences, conserver tous les Statement
et VersionTexte; pas de purge automatique C0-A.
**C14-D2 approuvé :** refuser tout le bloc contenant un contenu non Statement,
un objet disparu ou une GFK incohérente, faute d’archive typée fidèle.
Les protections historiques et décisions/ancrages non archivables font
également refuser tout le bloc. Le rollback inclut archives et repointages.

[Spécification](use_cases/UC-C-14/specification.md) ·
[Traçabilité](use_cases/UC-C-14/tracabilite.md) ·
[Attestation B](use_cases/UC-C-14/validation.md) ·
[Manifeste](use_cases/UC-C-14/manifest_sha256.json) ·
[Comparer les vues R1 conservées](historique/2026-10-20_avant_invariants_statement_R2/corpus/use_cases/UC-C-14/specification.md).

### UC14 — Activité

[SVG](use_cases/UC-C-14/activity.svg) · [PlantUML](use_cases/UC-C-14/activity.puml) · [PNG](use_cases/UC-C-14/activity.png)

![UC14 Activité](use_cases/UC-C-14/activity.png)

### UC14 — Séquence

[SVG](use_cases/UC-C-14/sequence.svg) · [PlantUML](use_cases/UC-C-14/sequence.puml) · [PNG](use_cases/UC-C-14/sequence.png)

![UC14 Séquence](use_cases/UC-C-14/sequence.png)

### UC14 — ERD

[SVG](use_cases/UC-C-14/erd.svg) · [PlantUML](use_cases/UC-C-14/erd.puml) · [PNG](use_cases/UC-C-14/erd.png)

![UC14 ERD](use_cases/UC-C-14/erd.png)

### UC14 — Classes et responsabilités

[SVG](use_cases/UC-C-14/class.svg) · [PlantUML](use_cases/UC-C-14/class.puml) · [PNG](use_cases/UC-C-14/class.png)

![UC14 Classes et responsabilités](use_cases/UC-C-14/class.png)

## B. UC15 — appuis conservés, anomalies et strict distincts

**C15-D1 approuvé :** toute origine valide du bon couple reste visible; une
anomalie locale ajoute un diagnostic sans effacer les autres appuis. Une
erreur de contexte ou une panne fait échouer la lecture. Les anomalies de
résolution alimentent EX04 et bloquent le strict, même si des appuis valides
restent consultables. Les sept EX restent cumulatifs.

[Spécification](use_cases/UC-C-15/specification.md) ·
[Traçabilité](use_cases/UC-C-15/tracabilite.md) ·
[Attestation B](use_cases/UC-C-15/validation.md) ·
[Manifeste](use_cases/UC-C-15/manifest_sha256.json) ·
[Comparer R1](historique/2026-10-20_avant_invariants_statement_R2/corpus/use_cases/UC-C-15/specification.md).
**C0A-REV-01 reste ouverte dans le patch**; aucune correction testée ou implantée.

### UC15 — Activité

[SVG](use_cases/UC-C-15/activity.svg) · [PlantUML](use_cases/UC-C-15/activity.puml) · [PNG](use_cases/UC-C-15/activity.png)

![UC15 Activité](use_cases/UC-C-15/activity.png)

### UC15 — Séquence

[SVG](use_cases/UC-C-15/sequence.svg) · [PlantUML](use_cases/UC-C-15/sequence.puml) · [PNG](use_cases/UC-C-15/sequence.png)

![UC15 Séquence](use_cases/UC-C-15/sequence.png)

### UC15 — ERD

[SVG](use_cases/UC-C-15/erd.svg) · [PlantUML](use_cases/UC-C-15/erd.puml) · [PNG](use_cases/UC-C-15/erd.png)

![UC15 ERD](use_cases/UC-C-15/erd.png)

### UC15 — Classes et responsabilités

[SVG](use_cases/UC-C-15/class.svg) · [PlantUML](use_cases/UC-C-15/class.puml) · [PNG](use_cases/UC-C-15/class.png)

![UC15 Classes et responsabilités](use_cases/UC-C-15/class.png)

## C. Citations — deux responsabilités proposées

[Analyse ciblée et arbitrages](ANALYSE_CIBLEE_CITATIONS_C0A.md).
Le renommage de l’occurrence relève d’UC02, par une action distincte du profil
UC13 approuvé. Recommandation CIT-D1/D2 : item seul, source intacte, refus de
toute incidence de rôle/numéro ou de contexte d’examen non conservable.
Le refus HTTP 403 actuel n’est pas pris pour une décision approuvée.

La consultation de l’examen relève d’UC12, son nouvel ajout d’UC05E.
Recommandation CIT-D3/D4 : distinguer décision, fraîcheur, capture absente,
type hors contrat et possibilité réelle de nouvel examen. Le chemin futur
attend le journal immuable et le type/adaptateur nécessaires; pas de boucle
de reconfirmation par une fonction qui écrase l’ancien état.

### UC02 — intitulé de citation

[Spécification](use_cases/UC-C-02/RENOMMER_CITATION/specification.md) · [Traçabilité](use_cases/UC-C-02/RENOMMER_CITATION/tracabilite.md) · [Revue B et réserves](use_cases/UC-C-02/RENOMMER_CITATION/validation.md).

| Vue | Rendu | Source |
|---|---|---|
| Activité | [SVG](use_cases/UC-C-02/RENOMMER_CITATION/activity.svg) · [PNG](use_cases/UC-C-02/RENOMMER_CITATION/activity.png) | [PlantUML](use_cases/UC-C-02/RENOMMER_CITATION/activity.puml) |
| Séquence | [SVG](use_cases/UC-C-02/RENOMMER_CITATION/sequence.svg) · [PNG](use_cases/UC-C-02/RENOMMER_CITATION/sequence.png) | [PlantUML](use_cases/UC-C-02/RENOMMER_CITATION/sequence.puml) |
| ERD | [SVG](use_cases/UC-C-02/RENOMMER_CITATION/erd.svg) · [PNG](use_cases/UC-C-02/RENOMMER_CITATION/erd.png) | [PlantUML](use_cases/UC-C-02/RENOMMER_CITATION/erd.puml) |
| Classes et responsabilités | [SVG](use_cases/UC-C-02/RENOMMER_CITATION/class.svg) · [PNG](use_cases/UC-C-02/RENOMMER_CITATION/class.png) | [PlantUML](use_cases/UC-C-02/RENOMMER_CITATION/class.puml) |

![UC02 — intitulé de citation — activité](use_cases/UC-C-02/RENOMMER_CITATION/activity.png)

### UC12 — diagnostic de l’examen

[Spécification](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/specification.md) · [Traçabilité](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/tracabilite.md) · [Revue B et réserves](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/validation.md).

| Vue | Rendu | Source |
|---|---|---|
| Activité | [SVG](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/activity.svg) · [PNG](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/activity.png) | [PlantUML](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/activity.puml) |
| Séquence | [SVG](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/sequence.svg) · [PNG](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/sequence.png) | [PlantUML](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/sequence.puml) |
| ERD | [SVG](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/erd.svg) · [PNG](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/erd.png) | [PlantUML](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/erd.puml) |
| Classes et responsabilités | [SVG](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/class.svg) · [PNG](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/class.png) | [PlantUML](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/class.puml) |

![UC12 — diagnostic de l’examen — activité](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/activity.png)

### États de lecture et nouvel examen futur

[SVG](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/states.svg) ·
[PlantUML](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/states.puml) ·
[PNG](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/states.png).

![UC12 — états et préalables du nouvel examen](use_cases/UC-C-12/DIAGNOSTIQUER_EXAMEN/states.png)

## D. Modèle consolidé proposé

G-C0A-R3-CIT ajoute les types Quote à la projection et distingue les services
rédactionnels, diagnostics et résultats non persistants. Le schéma est inchangé.
Le modèle G-R2 déjà approuvé avec UC13 est conservé séparément.

[ERD SVG](modele_global/erd_consolide.svg) · [PlantUML](modele_global/erd_consolide.puml) · [PNG](modele_global/erd_consolide.png).

![ERD global proposé](modele_global/erd_consolide.png)

[Classes SVG](modele_global/classes_consolidees.svg) · [PlantUML](modele_global/classes_consolidees.puml) · [PNG](modele_global/classes_consolidees.png).

![Classes globales proposées](modele_global/classes_consolidees.png)

## Décisions enregistrées et prochaine étape

UC14 R2-HIST (C14-D1/D2) et UC15 R2-DIAG (C15-D1) sont approuvés à la version
exacte présentée dans la PR #31, commit 30724df. UC13 conserve son approbation
antérieure. Sources et rendus ci-dessus inchangés; copies originales préservées.
Les sous-cas UC02/12 et CIT-D1–D4 restent EN_REVUE, hors implantation C0-A.
Le global G-R3 ne reçoit aucune approbation générale par transfert.

Le [mandat technique proposé à A](lots/C0-A/MANDAT.md) vise uniquement les trois
profils approuvés et les écarts C0A-ST-01 / C0A-14-01 / C0A-REV-01.
Il doit être approuvé avant de demander le démarrage; aucun nouvel examen
citation, mécanisme L1-A ou cycle général de documentation n’est requis.
La fusion documentaire de la PR #31 est autorisée par le mandat utilisateur;
aucun code, migration, base réelle ou ressource de A n’est modifié.
[Registre courant](registre_validation.md) · [Backlog](BACKLOG_ARCHITECTURE_C.md).
