# Matrice de couverture — Epic rédaction V2 → architecture C

**C-UML-2026-10-20-R1 — Livrable B.** Source : [V2 conservée](references/EPIC_REDACTION_V2_SOURCE.md). Décisions : [avenant](AVENANT_ARCHITECTURE_C.md). Les libellés des 91 critères sont repris de la source pour permettre un contrôle exhaustif.

## 1. Sens des qualifications

- **COUVERT** : contrat C existant suffisant, ou principe désormais explicitement décidé par le mandat; aucune nouvelle autorité nécessaire. Cela ne signifie ni implémenté ni dossier UML validé.
- **A_COMPLETER** : préciser un contrat ou une story existante.
- **NOUVEAU** : nouveau use case/parcours documentaire, avec réutilisation des fondations C.
- **A_ARBITRER** : option fonctionnelle ou contractuelle non tranchée; R01–R08 de l’avenant.
- **INCOMPATIBLE** : contradiction à résoudre, sans autorisation de l’implanter. Aucune exigence littérale de V2 n’est classée ainsi après la décision D05 et l’interprétation conceptuelle de Démonstration; les interprétations incompatibles sont isolées au §7.

Les colonnes de tests désignent des **scénarios planifiés**, non exécutés dans cette intervention. Les UC renvoient au [plan](PLAN_MODELISATION_UML.md). La traçabilité fine `AC → éléments précis des quatre vues → test` sera obligatoire dans chaque dossier; elle n’est pas prétendue terminée ici, puisque les vues cibles manquent.

## 2. Les huit invariants de V2

| ID | Exigence | Qualification | Contrat C / complément | Use cases | Scénarios à rattacher |
|---|---|---|---|---|---|
| V2:INV-01 | Identité permanente des sources | COUVERT | INV01, D12; modèle qualifié + PK, état source distinct | 03/04/16 | CF3-08/26; C-UML:N03 |
| V2:INV-02 | Source distincte de la pièce produite, simple ou composite | A_COMPLETER | Avenant §3; R01/R02/R04; pas de tables imposées | 16 | EPIC-V2:T03/T10; C-UML:N03–N06 |
| V2:INV-03 | Chaîne de justification et réutilisation | A_COMPLETER | D01/D02/D12; regroupement rédactionnel sans entité de raisonnement concurrente | 02/03/04/05P | C:T06–T08/T21; CF3-12 |
| V2:INV-04 | Cotation chronologique intégrale par version | COUVERT | D05 décidée; modalités restantes R03/R04 ne réouvrent pas le principe | 09 | EPIC-V2:T01–T06/T09; C-UML:N15 |
| V2:INV-05 | Conservation complète et immuable du contenu figé | COUVERT | D08, CF3-D5; compléments de protocole R08 | 11 | CF3-16–19/25; EPIC-V2:T07/T11/T12 |
| V2:INV-06 | Concordance des pièces entre versions | NOUVEAU | UC-C-17, identité/composition depuis les captures | 17 | EPIC-V2:T08/T09/T10/T14 |
| V2:INV-07 | Conservation de juillet | COUVERT | Référent/lock E01, exception explicite D05 pour le futur seulement | 12/15/17 | NR01/07/08; EPIC-V2:T14; C-UML:N11/N15 |
| V2:INV-08 | Une autorité de production | COUVERT | ResultatVersion; avenant §5 précise manifeste/fichiers | 09/10/18A | EX07; EPIC-V2:T13; C-UML:N07/N10 |

## 3. Les 91 critères d’acceptation

### V2 US-01 — Gestion des actes et de leurs versions

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-01.AC01** | Un dossier contient plusieurs actes. | COUVERT | US-C-01/11; CF1/D12; Contrat existant conservé; quatre vues à produire/réexaminer. | 01A/01B | VF01/VF08; CF3-01/02/16/18/23; C-UML:N12 |
| **V2:US-01.AC02** | Chaque acte possède une identité permanente. | COUVERT | US-C-01/11; CF1/D12; Contrat existant conservé; quatre vues à produire/réexaminer. | 01A/01B | VF01/VF08; CF3-01/02/16/18/23; C-UML:N12 |
| **V2:US-01.AC03** | Chaque acte peut posséder plusieurs versions. | COUVERT | US-C-01/11; CF1/D12; Contrat existant conservé; quatre vues à produire/réexaminer. | 01A/01B | VF01/VF08; CF3-01/02/16/18/23; C-UML:N12 |
| **V2:US-01.AC04** | Une seule version de travail active est permise par parcours de rédaction, sauf gestion explicite de branches. | A_ARBITRER | US-C-01/11; CF1/D12; R06 : définir parcours/branche et création concurrente de brouillons. | 01A/01B | VF01/VF08; CF3-01/02/16/18/23; C-UML:N12 |
| **V2:US-01.AC05** | Une version de travail peut être créée à partir d'une version figée. | COUVERT | US-C-01/11; CF1/D12; Contrat existant conservé; quatre vues à produire/réexaminer. | 01A/01B | VF01/VF08; CF3-01/02/16/18/23; C-UML:N12 |
| **V2:US-01.AC06** | Chaque version connaît son acte, son état et son antécédent. | COUVERT | US-C-01/11; CF1/D12; Contrat existant conservé; quatre vues à produire/réexaminer. | 01A/01B | VF01/VF08; CF3-01/02/16/18/23; C-UML:N12 |
| **V2:US-01.AC07** | Une version figée n'est plus modifiable. | COUVERT | US-C-01/11; CF1/D12; Contrat existant conservé; quatre vues à produire/réexaminer. | 01A/01B | VF01/VF08; CF3-01/02/16/18/23; C-UML:N12 |

### V2 US-02 — Rédaction structurée des faits

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-02.AC01** | Les paragraphes peuvent être créés, modifiés, déplacés et retirés. | COUVERT | US-C-02/13/14; D03/CF3-D4; Contrat existant conservé; quatre vues à produire/réexaminer. | 02/13/14 | C:T01–T05/T22; NR01/02/03/11; TR02 |
| **V2:US-02.AC02** | Chaque occurrence possède une identité stable indépendante de son numéro affiché. | COUVERT | US-C-02/13/14; D03/CF3-D4; Contrat existant conservé; quatre vues à produire/réexaminer. | 02/13/14 | C:T01–T05/T22; NR01/02/03/11; TR02 |
| **V2:US-02.AC03** | La numérotation est calculée selon l'ordre documentaire. | COUVERT | US-C-02/13/14; D03/CF3-D4; Contrat existant conservé; quatre vues à produire/réexaminer. | 02/13/14 | C:T01–T05/T22; NR01/02/03/11; TR02 |
| **V2:US-02.AC04** | Un même contenu réutilisable peut apparaître dans différents contextes sans imposer un numéro unique. | COUVERT | US-C-02/13/14; D03/CF3-D4; Contrat existant conservé; quatre vues à produire/réexaminer. | 02/13/14 | C:T01–T05/T22; NR01/02/03/11; TR02 |
| **V2:US-02.AC05** | Les opérations de rédaction préservent les liens de justification. | COUVERT | US-C-02/13/14; D03/CF3-D4; Contrat existant conservé; quatre vues à produire/réexaminer. | 02/13/14 | C:T01–T05/T22; NR01/02/03/11; TR02 |
| **V2:US-02.AC06** | Les paragraphes d'une version figée sont conservés avec leur texte et leur position historique. | COUVERT | US-C-02/13/14; D03/CF3-D4; Contrat existant conservé; quatre vues à produire/réexaminer. | 02/13/14 | C:T01–T05/T22; NR01/02/03/11; TR02 |

### V2 US-03 — Construction des démonstrations et preuves

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-03.AC01** | Un paragraphe peut être soutenu par plusieurs démonstrations. | A_COMPLETER | US-C-03/04/05; D01/D02/D11/D12; Le regroupement rédactionnel reste une projection/organisation des usages; aucune Démonstration autonome imposée. | 03/04/05P | C:T06–T08/T12/T17/T21; VF03/VF13; IM/TR |
| **V2:US-03.AC02** | Une démonstration peut utiliser plusieurs preuves. | A_COMPLETER | US-C-03/04/05; D01/D02/D11/D12; Plusieurs preuves par regroupement via plusieurs UP, chacune avec ses sélections; pas de double autorité. | 03/04/05P | C:T06–T08/T12/T17/T21; VF03/VF13; IM/TR |
| **V2:US-03.AC03** | Une preuve peut organiser plusieurs éléments probatoires. | COUVERT | US-C-03/04/05; D01/D02/D11/D12; Contrat existant conservé; quatre vues à produire/réexaminer. | 03/04/05P | C:T06–T08/T12/T17/T21; VF03/VF13; IM/TR |
| **V2:US-03.AC04** | Un élément peut être réutilisé sans duplication de sa source. | COUVERT | US-C-03/04/05; D01/D02/D11/D12; Contrat existant conservé; quatre vues à produire/réexaminer. | 03/04/05P | C:T06–T08/T12/T17/T21; VF03/VF13; IM/TR |
| **V2:US-03.AC05** | Les rôles probatoires et les limites d'un appui peuvent être conservés. | COUVERT | US-C-03/04/05; D01/D02/D11/D12; Contrat existant conservé; quatre vues à produire/réexaminer. | 03/04/05P | C:T06–T08/T12/T17/T21; VF03/VF13; IM/TR |
| **V2:US-03.AC06** | L'application distingue la justification interne du texte destiné à être plaidé. | COUVERT | US-C-03/04/05; D01/D02/D11/D12; Contrat existant conservé; quatre vues à produire/réexaminer. | 03/04/05P | C:T06–T08/T12/T17/T21; VF03/VF13; IM/TR |
| **V2:US-03.AC07** | Une version figée conserve l'état des démonstrations et des preuves qu'elle mobilise. | COUVERT | US-C-03/04/05; D01/D02/D11/D12; Contrat existant conservé; quatre vues à produire/réexaminer. | 03/04/05P | C:T06–T08/T12/T17/T21; VF03/VF13; IM/TR |

### V2 US-04 — Détermination des pièces à produire

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-04.AC01** | Le système détermine les sources impliquées dans les utilisations probatoires de la version. | COUVERT | US-C-03/04/09; INV02/CF4; Contrat existant conservé; quatre vues à produire/réexaminer. | 04/16 | CF3-07/08/12/24; VF14; EPIC-V2:T03; C-UML:N03/N16 |
| **V2:US-04.AC02** | Les règles de production identifient les unités documentaires correspondantes. | A_ARBITRER | US-C-03/04/09; INV02/CF4; R01/R02/R04 : unité produite, continuité logique, compositions et fragments. | 04/16 | CF3-07/08/12/24; VF14; EPIC-V2:T03; C-UML:N03/N16 |
| **V2:US-04.AC03** | Une utilisation répétée ne crée pas automatiquement plusieurs copies d'une même pièce. | A_COMPLETER | US-C-03/04/09; INV02/CF4; Conserver les chemins des usages et distinguer la déduplication de pièce de celle des composantes. | 04/16 | CF3-07/08/12/24; VF14; EPIC-V2:T03; C-UML:N03/N16 |
| **V2:US-04.AC04** | Les citations et passages restent reliés à leurs sources. | COUVERT | US-C-03/04/09; INV02/CF4; Contrat existant conservé; quatre vues à produire/réexaminer. | 04/16 | CF3-07/08/12/24; VF14; EPIC-V2:T03; C-UML:N03/N16 |
| **V2:US-04.AC05** | Les liasses et assemblages conservent leurs composantes et leur ordre. | NOUVEAU | US-C-03/04/09; INV02/CF4; US-C-16 : manifeste de composition ordonné; choix R01/R02. | 04/16 | CF3-07/08/12/24; VF14; EPIC-V2:T03; C-UML:N03/N16 |
| **V2:US-04.AC06** | L'utilisateur peut distinguer les preuves exploitées à des fins analytiques de celles destinées à la production. | A_ARBITRER | US-C-03/04/09; INV02/CF4; R05 : choix analytique/production enregistré; jamais un filtre d’affichage. | 04/16 | CF3-07/08/12/24; VF14; EPIC-V2:T03; C-UML:N03/N16 |
| **V2:US-04.AC07** | Une pièce sans utilisation pertinente n'est pas ajoutée automatiquement au bordereau. | COUVERT | US-C-03/04/09; INV02/CF4; Contrat existant conservé; quatre vues à produire/réexaminer. | 04/16 | CF3-07/08/12/24; VF14; EPIC-V2:T03; C-UML:N03/N16 |

### V2 US-05 — Cotation chronologique dynamique

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-05.AC01** | Le périmètre de calcul est l'ensemble des pièces retenues pour la version. | COUVERT | US-C-09; D05 décidée/D06; Contrat existant conservé; quatre vues à produire/réexaminer. | 09 | EPIC-V2:T01–T06/T09/T13/T14; NR08; C-UML:N02/N10 |
| **V2:US-05.AC02** | L'ordre chronologique est déterminé par une règle unique. | A_COMPLETER | US-C-09; D05 décidée/D06; D06 pour les sources simples; R03 pour la date des composites et le profil exact. | 09 | EPIC-V2:T01–T06/T09/T13/T14; NR08; C-UML:N02/N10 |
| **V2:US-05.AC03** | Les dates manquantes, incertaines ou atemporelles reçoivent un traitement explicite. | COUVERT | US-C-09; D05 décidée/D06; Contrat existant conservé; quatre vues à produire/réexaminer. | 09 | EPIC-V2:T01–T06/T09/T13/T14; NR08; C-UML:N02/N10 |
| **V2:US-05.AC04** | Les égalités de date sont départagées de manière déterministe. | A_COMPLETER | US-C-09; D05 décidée/D06; Départage déterministe conservé; R03 pour une clé stable des compositions. | 09 | EPIC-V2:T01–T06/T09/T13/T14; NR08; C-UML:N02/N10 |
| **V2:US-05.AC05** | L'insertion d'une pièce recalcule les cotes concernées. | COUVERT | US-C-09; D05 décidée/D06; Contrat existant conservé; quatre vues à produire/réexaminer. | 09 | EPIC-V2:T01–T06/T09/T13/T14; NR08; C-UML:N02/N10 |
| **V2:US-05.AC06** | Le retrait d'une pièce provoque le recalcul. | COUVERT | US-C-09; D05 décidée/D06; Contrat existant conservé; quatre vues à produire/réexaminer. | 09 | EPIC-V2:T01–T06/T09/T13/T14; NR08; C-UML:N02/N10 |
| **V2:US-05.AC07** | Le recalcul ne modifie jamais les associations d'une version figée. | COUVERT | US-C-09; D05 décidée/D06; Contrat existant conservé; quatre vues à produire/réexaminer. | 09 | EPIC-V2:T01–T06/T09/T13/T14; NR08; C-UML:N02/N10 |
| **V2:US-05.AC08** | Les règles de classement sont identiques pour l'interface, le bordereau et l'exportation. | COUVERT | US-C-09; D05 décidée/D06; Contrat existant conservé; quatre vues à produire/réexaminer. | 09 | EPIC-V2:T01–T06/T09/T13/T14; NR08; C-UML:N02/N10 |
| **V2:US-05.AC09** | Les filtres d'affichage ne modifient pas la cotation de référence. | COUVERT | US-C-09; D05 décidée/D06; Contrat existant conservé; quatre vues à produire/réexaminer. | 09 | EPIC-V2:T01–T06/T09/T13/T14; NR08; C-UML:N02/N10 |

### V2 US-06 — Référencement automatique dans le texte

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-06.AC01** | Les références internes désignent une identité stable. | COUVERT | US-C-08/10; D10 et AncrageCitation E01; Contrat existant conservé; quatre vues à produire/réexaminer. | 08/09/10 | C:T09–T11/T18/T19; CF3-10/11/24; EPIC-V2:T02/T13; TR05 |
| **V2:US-06.AC02** | La cote affichée est obtenue à partir de la cotation de la version. | COUVERT | US-C-08/10; D10 et AncrageCitation E01; Contrat existant conservé; quatre vues à produire/réexaminer. | 08/09/10 | C:T09–T11/T18/T19; CF3-10/11/24; EPIC-V2:T02/T13; TR05 |
| **V2:US-06.AC03** | Toute recotation actualise les références du brouillon. | COUVERT | US-C-08/10; D10 et AncrageCitation E01; Contrat existant conservé; quatre vues à produire/réexaminer. | 08/09/10 | C:T09–T11/T18/T19; CF3-10/11/24; EPIC-V2:T02/T13; TR05 |
| **V2:US-06.AC04** | Les références aux sous-cotes et aux liasses sont prises en charge. | A_ARBITRER | US-C-08/10; D10 et AncrageCitation E01; R04 : règles de sous-cote et de liasse; identité/numéro source conservés séparément. | 08/09/10 | C:T09–T11/T18/T19; CF3-10/11/24; EPIC-V2:T02/T13; TR05 |
| **V2:US-06.AC05** | Une référence non résolue est détectée. | COUVERT | US-C-08/10; D10 et AncrageCitation E01; Contrat existant conservé; quatre vues à produire/réexaminer. | 08/09/10 | C:T09–T11/T18/T19; CF3-10/11/24; EPIC-V2:T02/T13; TR05 |
| **V2:US-06.AC06** | Aucune référence périmée ne peut subsister silencieusement dans une exportation validée. | COUVERT | US-C-08/10; D10 et AncrageCitation E01; Contrat existant conservé; quatre vues à produire/réexaminer. | 08/09/10 | C:T09–T11/T18/T19; CF3-10/11/24; EPIC-V2:T02/T13; TR05 |
| **V2:US-06.AC07** | Les références figées sont restituées selon leur version historique. | COUVERT | US-C-08/10; D10 et AncrageCitation E01; Contrat existant conservé; quatre vues à produire/réexaminer. | 08/09/10 | C:T09–T11/T18/T19; CF3-10/11/24; EPIC-V2:T02/T13; TR05 |

### V2 US-07 — Gel d'une version et de son dossier probatoire

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-07.AC01** | Le texte et sa structure sont conservés. | COUVERT | US-C-11; D08/CF3-D5; Contrat existant conservé; quatre vues à produire/réexaminer. | 11 | C:T16/T20; CF3-16–19/25; IM05/07; EPIC-V2:T07/T11/T12; C-UML:N07–N09 |
| **V2:US-07.AC02** | Les démonstrations, preuves et utilisations sont conservées dans leur état de version. | COUVERT | US-C-11; D08/CF3-D5; Contrat existant conservé; quatre vues à produire/réexaminer. | 11 | C:T16/T20; CF3-16–19/25; IM05/07; EPIC-V2:T07/T11/T12; C-UML:N07–N09 |
| **V2:US-07.AC03** | Le bordereau et les associations pièce–cote sont enregistrés. | COUVERT | US-C-11; D08/CF3-D5; Contrat existant conservé; quatre vues à produire/réexaminer. | 11 | C:T16/T20; CF3-16–19/25; IM05/07; EPIC-V2:T07/T11/T12; C-UML:N07–N09 |
| **V2:US-07.AC04** | Les paramètres chronologiques ayant déterminé l'ordre sont conservés. | COUVERT | US-C-11; D08/CF3-D5; Contrat existant conservé; quatre vues à produire/réexaminer. | 11 | C:T16/T20; CF3-16–19/25; IM05/07; EPIC-V2:T07/T11/T12; C-UML:N07–N09 |
| **V2:US-07.AC05** | Les fichiers produits sont vérifiables par des empreintes d'intégrité. | COUVERT | US-C-11; D08/CF3-D5; Contrat existant conservé; quatre vues à produire/réexaminer. | 11 | C:T16/T20; CF3-16–19/25; IM05/07; EPIC-V2:T07/T11/T12; C-UML:N07–N09 |
| **V2:US-07.AC06** | Une erreur de validation empêche la finalisation. | COUVERT | US-C-11; D08/CF3-D5; Contrat existant conservé; quatre vues à produire/réexaminer. | 11 | C:T16/T20; CF3-16–19/25; IM05/07; EPIC-V2:T07/T11/T12; C-UML:N07–N09 |
| **V2:US-07.AC07** | Le système ne publie jamais un dossier partiellement finalisé. | COUVERT | US-C-11; D08/CF3-D5; Contrat existant conservé; quatre vues à produire/réexaminer. | 11 | C:T16/T20; CF3-16–19/25; IM05/07; EPIC-V2:T07/T11/T12; C-UML:N07–N09 |
| **V2:US-07.AC08** | Le gel logique en base et la publication des fichiers suivent un protocole garantissant la cohérence, y compris en cas d'échec. | A_COMPLETER | US-C-11; D08/CF3-D5; Protocole base + stockage de l’avenant §6, choix R08, pannes et reprise idempotente. | 11 | C:T16/T20; CF3-16–19/25; IM05/07; EPIC-V2:T07/T11/T12; C-UML:N07–N09 |
| **V2:US-07.AC09** | Une fois figée, la version ne peut être modifiée rétroactivement. | COUVERT | US-C-11; D08/CF3-D5; Contrat existant conservé; quatre vues à produire/réexaminer. | 11 | C:T16/T20; CF3-16–19/25; IM05/07; EPIC-V2:T07/T11/T12; C-UML:N07–N09 |

### V2 US-08 — Concordance exhaustive entre versions

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-08.AC01** | La concordance compare deux versions explicitement identifiées. | NOUVEAU | US-C-09/11/12, couverture documentaire partielle; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 17 | EPIC-V2:T08/T09/T10/T14; C-UML:N02/N04/N06/N11 |
| **V2:US-08.AC02** | Elle couvre toutes les pièces des deux versions. | NOUVEAU | US-C-09/11/12, couverture documentaire partielle; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 17 | EPIC-V2:T08/T09/T10/T14; C-UML:N02/N04/N06/N11 |
| **V2:US-08.AC03** | Elle distingue les pièces conservées, ajoutées et retirées. | NOUVEAU | US-C-09/11/12, couverture documentaire partielle; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 17 | EPIC-V2:T08/T09/T10/T14; C-UML:N02/N04/N06/N11 |
| **V2:US-08.AC04** | Elle identifie les changements de cote. | NOUVEAU | US-C-09/11/12, couverture documentaire partielle; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 17 | EPIC-V2:T08/T09/T10/T14; C-UML:N02/N04/N06/N11 |
| **V2:US-08.AC05** | Elle reconnaît qu'une même cote peut désigner deux pièces différentes dans deux versions. | NOUVEAU | US-C-09/11/12, couverture documentaire partielle; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 17 | EPIC-V2:T08/T09/T10/T14; C-UML:N02/N04/N06/N11 |
| **V2:US-08.AC06** | Elle traite les sous-cotes, les liasses et les changements de composition. | A_ARBITRER | US-C-09/11/12, couverture documentaire partielle; R01/R02/R04 : comparaison exacte des compositions et carte des sous-cotes. | 17 | EPIC-V2:T08/T09/T10/T14; C-UML:N02/N04/N06/N11 |
| **V2:US-08.AC07** | Les correspondances non univoques sont signalées. | NOUVEAU | US-C-09/11/12, couverture documentaire partielle; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 17 | EPIC-V2:T08/T09/T10/T14; C-UML:N02/N04/N06/N11 |
| **V2:US-08.AC08** | La concordance repose sur les états historiques figés. | NOUVEAU | US-C-09/11/12, couverture documentaire partielle; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 17 | EPIC-V2:T08/T09/T10/T14; C-UML:N02/N04/N06/N11 |
| **V2:US-08.AC09** | Elle peut être consultée et exportée. | NOUVEAU | US-C-09/11/12, couverture documentaire partielle; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 17 | EPIC-V2:T08/T09/T10/T14; C-UML:N02/N04/N06/N11 |
| **V2:US-08.AC10** | Le système peut retrouver l'historique des cotes d'une pièce à travers toutes les versions où elle apparaît. | NOUVEAU | US-C-09/11/12, couverture documentaire partielle; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 17 | EPIC-V2:T08/T09/T10/T14; C-UML:N02/N04/N06/N11 |

### V2 US-09 — Génération du bordereau

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-09.AC01** | Le bordereau ne nécessite aucune ressaisie manuelle des cotes. | COUVERT | US-C-09/10; ResultatVersion; Contrat existant conservé; quatre vues à produire/réexaminer. | 09 | EPIC-V2:T01–T06/T13; CF3-24; NR08 |
| **V2:US-09.AC02** | Il contient exactement les pièces retenues pour la production. | COUVERT | US-C-09/10; ResultatVersion; Contrat existant conservé; quatre vues à produire/réexaminer. | 09 | EPIC-V2:T01–T06/T13; CF3-24; NR08 |
| **V2:US-09.AC03** | Son ordre et ses cotes correspondent au calcul de référence. | COUVERT | US-C-09/10; ResultatVersion; Contrat existant conservé; quatre vues à produire/réexaminer. | 09 | EPIC-V2:T01–T06/T13; CF3-24; NR08 |
| **V2:US-09.AC04** | Les descriptions sont reliées aux identités des pièces. | A_COMPLETER | US-C-09/10; ResultatVersion; Descriptions rattachées aux identités et états de pièce, pas seulement à la source. | 09 | EPIC-V2:T01–T06/T13; CF3-24; NR08 |
| **V2:US-09.AC05** | Les liasses et sous-cotes sont correctement représentées. | A_ARBITRER | US-C-09/10; ResultatVersion; R04 : représentation des liasses/sous-cotes. | 09 | EPIC-V2:T01–T06/T13; CF3-24; NR08 |
| **V2:US-09.AC06** | Le bordereau d'une version figée peut être restitué à l'identique. | COUVERT | US-C-09/10; ResultatVersion; Contrat existant conservé; quatre vues à produire/réexaminer. | 09 | EPIC-V2:T01–T06/T13; CF3-24; NR08 |

### V2 US-10 — Production et exportation des pièces

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-10.AC01** | L'exportation utilise la cotation de la version sélectionnée. | COUVERT | US-C-10/11, livrables et restitution; Contrat existant conservé; quatre vues à produire/réexaminer. | 18A/18B | EPIC-V2:T11/T12/T13; C-UML:N07/N08/N09/N10 |
| **V2:US-10.AC02** | Chaque pièce possède un fichier ou un ensemble de fichiers explicitement représenté dans le manifeste. | NOUVEAU | US-C-10/11, livrables et restitution; US-C-18 : liste ordonnée explicite des fichiers par pièce et par composition. | 18A/18B | EPIC-V2:T11/T12/T13; C-UML:N07/N08/N09/N10 |
| **V2:US-10.AC03** | Les noms des fichiers reflètent les cotes. | A_COMPLETER | US-C-10/11, livrables et restitution; Nom local à la version et cote issue du résultat commun; pas de collision historique. | 18A/18B | EPIC-V2:T11/T12/T13; C-UML:N07/N08/N09/N10 |
| **V2:US-10.AC04** | Toutes les composantes d'une pièce composite sont conservées. | NOUVEAU | US-C-10/11, livrables et restitution; Composition intégrale du dossier, ordre et correspondance avec chaque artefact. | 18A/18B | EPIC-V2:T11/T12/T13; C-UML:N07/N08/N09/N10 |
| **V2:US-10.AC05** | Le dossier comprend le bordereau correspondant. | COUVERT | US-C-10/11, livrables et restitution; Contrat existant conservé; quatre vues à produire/réexaminer. | 18A/18B | EPIC-V2:T11/T12/T13; C-UML:N07/N08/N09/N10 |
| **V2:US-10.AC06** | Le dossier comprend un manifeste des identités, cotes et empreintes. | A_COMPLETER | US-C-10/11, livrables et restitution; Manifeste de production : version/résultat/pièces/compositions/fichiers et empreintes. | 18A/18B | EPIC-V2:T11/T12/T13; C-UML:N07/N08/N09/N10 |
| **V2:US-10.AC07** | Les fichiers sources originaux ne sont jamais modifiés. | COUVERT | US-C-10/11, livrables et restitution; Contrat existant conservé; quatre vues à produire/réexaminer. | 18A/18B | EPIC-V2:T11/T12/T13; C-UML:N07/N08/N09/N10 |
| **V2:US-10.AC08** | Une exportation historique ne recalcule pas les cotes. | COUVERT | US-C-10/11, livrables et restitution; Contrat existant conservé; quatre vues à produire/réexaminer. | 18A/18B | EPIC-V2:T11/T12/T13; C-UML:N07/N08/N09/N10 |
| **V2:US-10.AC09** | Les erreurs de rendu ou de correspondance sont détectées. | COUVERT | US-C-10/11, livrables et restitution; Contrat existant conservé; quatre vues à produire/réexaminer. | 18A/18B | EPIC-V2:T11/T12/T13; C-UML:N07/N08/N09/N10 |
| **V2:US-10.AC10** | L'exportation d'une version figée est reproductible et vérifiable. | A_ARBITRER | US-C-10/11, livrables et restitution; R07 : restitution des octets conservés obligatoire; promesse de régénération à préciser. | 18A/18B | EPIC-V2:T11/T12/T13; C-UML:N07/N08/N09/N10 |

### V2 US-11 — Création d'une version amendée

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-11.AC01** | L'utilisateur peut créer une nouvelle version de travail depuis une version figée. | COUVERT | US-C-01/07/11; CF3; Contrat existant conservé; quatre vues à produire/réexaminer. | 01B/07/11/17 | EPIC-V2:T07/T08/T12/T14; CF3-01–26 |
| **V2:US-11.AC02** | Il peut ajouter ou retirer des paragraphes, démonstrations, preuves et pièces. | COUVERT | US-C-01/07/11; CF3; Contrat existant conservé; quatre vues à produire/réexaminer. | 01B/07/11/17 | EPIC-V2:T07/T08/T12/T14; CF3-01–26 |
| **V2:US-11.AC03** | Le bordereau est intégralement recalculé. | COUVERT | US-C-01/07/11; CF3; Contrat existant conservé; quatre vues à produire/réexaminer. | 01B/07/11/17 | EPIC-V2:T07/T08/T12/T14; CF3-01–26 |
| **V2:US-11.AC04** | Les renvois aux pièces sont actualisés. | COUVERT | US-C-01/07/11; CF3; Contrat existant conservé; quatre vues à produire/réexaminer. | 01B/07/11/17 | EPIC-V2:T07/T08/T12/T14; CF3-01–26 |
| **V2:US-11.AC05** | La version précédente reste intacte. | COUVERT | US-C-01/07/11; CF3; Contrat existant conservé; quatre vues à produire/réexaminer. | 01B/07/11/17 | EPIC-V2:T07/T08/T12/T14; CF3-01–26 |
| **V2:US-11.AC06** | La nouvelle version conserve une référence à son antécédent. | COUVERT | US-C-01/07/11; CF3; Contrat existant conservé; quatre vues à produire/réexaminer. | 01B/07/11/17 | EPIC-V2:T07/T08/T12/T14; CF3-01–26 |
| **V2:US-11.AC07** | Le gel produit une concordance avec les versions pertinentes. | A_COMPLETER | US-C-01/07/11; CF3; Ajouter la concordance documentaire UC-C-17 à la filiation déjà prévue. | 01B/07/11/17 | EPIC-V2:T07/T08/T12/T14; CF3-01–26 |

### V2 US-12 — Historique de dépôt et de communication

| Critère source | Exigence exacte | Qualification | Couverture et action | UC-C | Scénarios |
|---|---|---|---|---|---|
| **V2:US-12.AC01** | Une communication désigne une version identifiée. | A_COMPLETER | US-C-01/11/12; modèles Transmission/FichierTransmis existants; Relier l’événement à la version figée sans prétendre que Transmission le fait déjà. | 19 | C-UML:T19-01–T19-06; C-UML:N11 |
| **V2:US-12.AC02** | Les dates, destinataires et modalités de communication sont conservés. | NOUVEAU | US-C-01/11/12; modèles Transmission/FichierTransmis existants; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 19 | C-UML:T19-01–T19-06; C-UML:N11 |
| **V2:US-12.AC03** | Les fichiers transmis sont identifiés par leur nom et leur empreinte. | NOUVEAU | US-C-01/11/12; modèles Transmission/FichierTransmis existants; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 19 | C-UML:T19-01–T19-06; C-UML:N11 |
| **V2:US-12.AC04** | Une même version peut faire l'objet de plusieurs communications. | NOUVEAU | US-C-01/11/12; modèles Transmission/FichierTransmis existants; Nouveau parcours US-C-19; réutiliser les données existantes sans inventer son rattachement à VersionActe. | 19 | C-UML:T19-01–T19-06; C-UML:N11 |
| **V2:US-12.AC05** | Les événements de dépôt et de communication sont distincts du gel. | COUVERT | US-C-01/11/12; modèles Transmission/FichierTransmis existants; CF1 et US-C-11 distinguent déjà gel volontaire et événement réel. | 19 | C-UML:T19-01–T19-06; C-UML:N11 |
| **V2:US-12.AC06** | Les communications papier peuvent être documentées sans supposer automatiquement une identité parfaite avec un fichier numérique. | COUVERT | US-C-01/11/12; modèles Transmission/FichierTransmis existants; US-C-12 conserve la nature papier et les lacunes historiques; UC-C-19 l’étend aux événements. | 19 | C-UML:T19-01–T19-06; C-UML:N11 |

**Décompte des 91 critères :** A_ARBITRER : 7, A_COMPLETER : 11, COUVERT : 58, NOUVEAU : 15. Ce décompte mesure les contrats, pas les fonctionnalités livrées.

## 4. Contraintes, concepts et préalables également couverts

Les identifiants COMPAT/PRE ci-dessous sont des repères de cette matrice, sans renumérotation des critères V2.

| Source | Exigence | Qualification | Traitement / preuve documentaire |
|---|---|---|---|
| V2:§1 | Intégrer rédaction, preuve et production, conserver la collecte | COUVERT | D12 et chaîne C conservés; aucun remplacement des applications sources |
| V2:§4.EX-01 | V1 A=P-1/B=P-2/C=P-3; V2 D=P-1/A=P-2/C=P-3 avec B retirée | COUVERT | D05 décidée; EPIC-V2:T01/T04/T08/T09, jamais rapprochement sur P-1 seul |
| V2:§5.Acte/VersionActe | Identité d’acte et états versionnés | COUVERT | UC-C-01A/01B/11; R06 reste sur le parcours, pas sur le besoin d’identité |
| V2:§5.Occurrence | Position/contenu dans la version | COUVERT | LibraryNode/Statement, D03 et C0-A; pas un numéro global de Statement |
| V2:§5.Demonstration/Preuve | Justification et réutilisation | A_COMPLETER | Regroupement rédactionnel et UP; pas de nouveau raisonnement autonome |
| V2:§5.Utilisation | Relation entre rédaction et appuis | COUVERT | D01/D02, UC-C-04/05P |
| V2:§5.PieceProduite | Identité d’unité produite | A_ARBITRER | Contrat de l’avenant §3, R01/R02; UC-C-16 |
| V2:§5.CotationVersion | Association historique pièce/cote | A_COMPLETER | D05 + composition exacte; pas de table imposée avant ERD justifié |
| V2:§5.ArtefactVersion | Fichiers, manifeste, empreintes | A_COMPLETER | UC-C-18A/18B, D08; R07/R08 |
| V2:§5.Communication | Historique d’événements | NOUVEAU | UC-C-19, sans confondre gel et envoi |
| V2:§5.Non-prescription | Réutiliser les responsabilités sans prescrire neuf tables | COUVERT | ERD observé + futur ERD cible; justifier toute persistance autonome |
| V2:COMPAT-01 | Sources et PK conservées | COUVERT | INV01/INV14; aucune migration ou conversion dans ce mandat |
| V2:COMPAT-02 | Relations de preuve conservées | COUVERT | Ancien pont lu comme existant, aucune copie/rupture silencieuse |
| V2:COMPAT-03 | Documents reproduits et produits | COUVERT | C0-A, D12; protections et provenance séparées |
| V2:COMPAT-04 | Archives historiques | COUVERT | D08/CF3-D4; aucun fichier de l’archive légale modifié |
| V2:COMPAT-05 | Associations pièce–cote historiques | COUVERT | D05/lock; EPIC-V2:T14 et C-UML:N15 |
| V2:COMPAT-06 | Réutiliser les moteurs compatibles | A_COMPLETER | Dossier de classes/contrats et contrôle de conformité, sans déclaration de conformité par nom |
| V2:COMPAT-07 | Contrôles et audits opérationnels | COUVERT | E01 EX01–EX07 et oracles A conservés |
| V2:COMPAT-08 | Reconstruction interdite sur cible figée | COUVERT | D08 et garde globale L5; C-UML:N09 |
| V2:PRE-01 | Inventaire réutilisable | COUVERT | ERD/classes P6 et analyse de références dans le rapport |
| V2:PRE-02 | Diff main/travaux non intégrés | COUVERT | Lecture Git locale + ls-remote; références exactes du rapport, sans fusion |
| V2:PRE-03 | Identité simple/composite | A_ARBITRER | Définition minimale §3 de l’avenant; décision R01/R02 avant UML final du chemin concerné |
| V2:PRE-04 | Contrat de classement unique | A_COMPLETER | D05/D06 et ResultatVersion; R03/R04 pour les détails manquants |
| V2:PRE-05 | Conservation des versions/artefacts | A_COMPLETER | D08 + manifeste et protocole base/stockage, UC-C-11/18 |
| V2:PRE-06 | Stratégie de migration additive | A_COMPLETER | Voir rapport : nouveaux schémas futurs, migrations A intactes, plan/retour testés seulement après mandat |
| V2:PRE-07 | Risques suppression/mutation/désynchronisation | COUVERT | CF3/IM/TR, contre-épreuves complémentaires et analyse d’impact |
| V2:PRE-08 | Décomposition dépendances/tests | COUVERT | 22 dossiers dans le plan et porte obligatoire du protocole |

## 5. Les quatorze scénarios V2, conservés sans renumérotation

| ID | Scénario source | UC-C | Lots / conditions | Statut d’exécution ici |
|---|---|---|---|---|
| EPIC-V2:T01 | Ajout chronologique avant toutes les pièces existantes. | 09/16 | L3-A/L4/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T02 | Ajout entre deux pièces et mise à jour des renvois. | 08/09/10 | L3-A/L4/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T03 | Retrait d'une pièce utilisée plusieurs fois, avec conservation tant qu'une utilisation demeure. | 04/16 | L3-A/L4/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T04 | Retrait définitif d'une pièce et recalcul complet. | 09/16 | L3-A/L4/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T05 | Insertion de deux pièces de même date, avec ordre déterministe. | 09 | L3-A/L4/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T06 | Pièce sans date, date incertaine et pièce atemporelle. | 09/16 | L3-A/L4/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T07 | Gel V1, modification du brouillon V2 et vérification de l'intégrité de V1. | 01B/11 | L5/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T08 | Concordance V1–V2 couvrant ajouts, retraits et recotations. | 17 | L3-A/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T09 | Même cote, pièces différentes selon les versions. | 09/17 | L3-A/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T10 | Pièce composite ou liasse dont les composantes changent. | 16/17 | L3-A/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T11 | Échec du gel après préparation des fichiers, sans publication partielle. | 11/18A | L5/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T12 | Réexportation d'une version historique sans recalcul. | 11/18B | L5/L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T13 | Correspondance exacte entre renvois dans l'acte, bordereau, fichiers et manifeste. | 09/10/18A/18B | L3–L6; contrats R applicables à résoudre | NON EXECUTE |
| EPIC-V2:T14 | Préservation intégrale des associations du dépôt du 24 juillet 2026. | 12/15/17/18B | E01 + L5/L6; contrats R applicables à résoudre | NON EXECUTE |

## 6. Nouveaux scénarios négatifs à ajouter

Chaque scénario ci-dessous complète les suites antérieures. Tous sont **NON EXECUTES** dans cette intervention.

| ID | Attendu / contre-épreuve | UC-C |
|---|---|---|
| C-UML:N01 | Refuser l’ouverture du développement si une des quatre vues, sa validation B ou l’approbation utilisateur manque, même si PlantUML compile. | Tous |
| C-UML:N02 | Deux P-1 de versions différentes restent deux désignations contextualisées; une référence active sans contexte ne choisit pas arbitrairement une pièce. | 09/10/17 |
| C-UML:N03 | Même titre, cote ou source partagée ne fusionne pas deux pièces; deux compositions égales d’identités différentes restent des candidats explicites. | 16/17 |
| C-UML:N04 | [A,B]→[A,C] n’est jamais inchangé; V1 garde B et sa composition/cote/artefacts. La continuité logique suit seulement R01 approuvée. | 16/17/11 |
| C-UML:N05 | [A,B]→[B,A] conserve l’ordre dans les manifestes et signale sa modification; pas de tri/déduplication silencieux. | 16/18A |
| C-UML:N06 | Scission/fusion et candidats multiples : carte N:M et décision explicites; aucune équivalence automatique à partir d’un composant commun. | 17 |
| C-UML:N07 | Une modification concurrente entre calcul et gel refuse le résultat périmé; aucun mélange ancien/nouveau dans acte, bordereau et fichiers. | 09/10/11/18A |
| C-UML:N08 | Pannes avant/après stockage durable, avant/après commit et reprises répétées : aucun gel partiel visible ni remplacement du résultat finalisé. | 11/18A |
| C-UML:N09 | UPDATE/bulk/SQL, suppression/cascade ou mutation du stockage sur le périmètre figé : refus ou protection éprouvée selon les droits; hashes seuls insuffisants. | 05E/11/18B |
| C-UML:N10 | Correction de date ou état source/composition rend le brouillon périmé et recalcule selon la politique; l’état historique reste intact. | 09/16/18A |
| C-UML:N11 | Import de juillet et événement papier : aucune composition numérique, date d’examen ou identité fichier/papier inventée pour remplir une lacune. | 12/17/18B/19 |
| C-UML:N12 | Deux créations concurrentes de brouillons respectent la règle R06 approuvée; refus atomique sans branche implicite. | 01A/01B |
| C-UML:N13 | Modification d’un contrat ou dossier approuvé : impact, nouvelle version et nouvelle décision; l’ancienne approbation ne suit pas automatiquement. | Tous |
| C-UML:N14 | Une vue de classe/ERD P6 ou une activité ancienne ne vaut pas quadruplet cible approuvé; une inclusion globale non contextualisée est rejetée. | Tous |
| C-UML:N15 | Nouvelle version CHRONO_VERSION peut recoter sans modifier lock/registre/artefacts de juillet; ne pas réintroduire P-107 comme compteur global. | 09/17 |
| C-UML:N16 | Supprimer un usage analytique ou de production ne retire pas implicitement une pièce encore produite ailleurs; un filtre visuel ne change pas le périmètre de cotation. | 04/16/09 |

### Scénarios complémentaires de communication

Ces six scénarios sont nouveaux et **NON EXECUTES**; ils donnent des contrôles propres à UC-C-19, au-delà de la seule contre-épreuve historique C-UML:N11.

| ID | Critères V2 | Attendu observable |
|---|---|---|
| C-UML:T19-01 | US-12.AC01/AC05 | Geler une version sans créer d’événement; enregistrer ensuite un événement sur la version explicitement choisie, sans mutation du gel |
| C-UML:T19-02 | US-12.AC02 | Conserver les dates, destinataires, modalités et preuves effectivement renseignés; une information manquante reste déclarée manquante |
| C-UML:T19-03 | US-12.AC03 | Relier les fichiers envoyés à leurs noms et empreintes; une divergence par rapport au livrable annoncé est refusée ou explicitement diagnostiquée, jamais certifiée à tort |
| C-UML:T19-04 | US-12.AC04/AC05 | Deux communications d’une même version restent deux événements, sans duplication ni réécriture du contenu figé; le dépôt ne crée pas automatiquement un envoi |
| C-UML:T19-05 | US-12.AC06 | Relever une communication papier avec sa preuve disponible et l’incertitude éventuelle de correspondance numérique, sans inventer un fichier transmis |
| C-UML:T19-06 | US-12.AC01–AC06 | Corriger un relevé d’événement par une trace explicite conservant l’ancien constat; refus/conflit tardif sans perte ni événement partiellement enregistré |

## 7. Incompatibilités identifiées et traitement

| Point | Diagnostic | Résolution documentaire / réserve |
|---|---|---|
| Permanence globale pour toute nouvelle version | Incompatible avec D05 désormais décidée | Supplantée pour les nouvelles versions CHRONO_VERSION; permanence des associations historiques maintenue |
| Processus local « Classe : jamais » et séquence seulement sur atomicité | Incompatible avec le mandat §§4–5 | Processus révisé : quatre vues toujours obligatoires par UC; états en complément |
| Démonstration portant son propre raisonnement et ses validations | Interprétation incompatible avec C, mais non imposée par V2 §5 | Non introduite; regroupement rédactionnel par occurrences/usages, D01/D02/D12 conservés |
| Produit recalculé utilisé comme capture historique | Incompatible avec D08 | ProducedExhibit reste une projection temporaire; contenu et artefacts figés font autorité |
| Transaction SQL assimilée à une publication atomique des fichiers | Incompatible avec le mandat §3.5 | Protocole recommandé de l’avenant §6; R08 et contre-épreuves à résoudre avant gel |
| ERD/classes observés confondus avec la cible | Incompatible avec le nouveau contrôle préalable | Références P6 conservées; vues contextuelles cibles à produire |

## 8. Conservation des 38 scénarios NR/CF3 et des autres suites

Le tableau complet et ses contre-épreuves restent inchangés dans le [registre §8.1](DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md#81-les-38-scénarios-du-dernier-addendum). Aucun ancien ID n’est supprimé, réaffecté ou déclaré exécuté dans cette intervention.

| Groupe / IDs conservés | Affectation aux dossiers |
|---|---|
| NR01, NR02, NR03, NR04, NR05, NR06, NR07, NR08, NR09, NR10, NR11, NR12 | 13/14/15 pour leurs seuls contrôles C0-A; 02/05E/05P/07/09/12, puis 11/17 et L6 pour leurs garanties complètes |
| CF3-01, CF3-02, CF3-03, CF3-04, CF3-05, CF3-06, CF3-07, CF3-08, CF3-09, CF3-10, CF3-11, CF3-12, CF3-13 | 01A/02/03/04/05P/07/08/12 selon la couverture initiale, contexte et sélections |
| CF3-14, CF3-15, CF3-16, CF3-17, CF3-18, CF3-19, CF3-20, CF3-21, CF3-22, CF3-23, CF3-24, CF3-25, CF3-26 | 05E/06/07/08/09/11/12/16; source/citation, filiation, gel et revalidation L6 |
| IM01–IM08, TR01–TR06 | 05E/05P/11/12; garanties locales du journal distinctes du gel global |
| E01:T01–T29, C:T01–T22, C:N01–N14, VF01–VF14 | Réutilisation dans les dossiers concernés; aucun changement d’attentes pour normaliser une régression |
| A : invariants P6, T2.1–T2.9 et T-pont | 08/10/11 et intégration L3-B/L6; résultats rapportés sur branche/clone distincts d’une nouvelle exécution ou d’un déploiement |
