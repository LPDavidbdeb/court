# Inventaire et plan de modélisation UML de C

**Plan actualisé R2 — 20 octobre 2026; contrats C-UML-2026-10-20-R1 — Livrable C.**

Révision de couverture : modèles G-C0A-R1 et dossiers 13/14/15 produits;
validation B de 13, revues de 14/15 en cours. Les autres dossiers ne sont
pas produits par cette révision. [Rapport de revue](RAPPORT_REVUE_COUVERTURE_ET_C0A.md).

Le [mandat](references/MANDAT_CONSOLIDATION_UML_2026-10-20.md) impose quatre vues avant toute implantation. La revue R2 produit celles de 13/14/15 seulement; aucune production globale des 88 vues n’est déclarée. L’[avenant](AVENANT_ARCHITECTURE_C.md) consolide les contrats; le [protocole](PROTOCOLE_VALIDATION_UML.md) fixe le contrôle; le [registre](registre_validation.md) porte les statuts courants.

## 1. Organisation durable et frontières

Le corpus déjà rapatrié est conservé sous `docs/architecture_c/`. Il n’est pas dupliqué sous `docs/modele_preuve/architecture_c/`. Les anciens diagrammes restent à leurs emplacements, sans déplacement ni suppression.

```text
docs/architecture_c/
  DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md
  AVENANT_ARCHITECTURE_C.md
  MATRICE_COUVERTURE_V2_C.md
  PLAN_MODELISATION_UML.md
  PROTOCOLE_VALIDATION_UML.md
  RAPPORT_CONSOLIDATION_ET_VALIDATION.md
  registre_validation.md
  references/                    sources reçues, sans modification
  historique/                    états antérieurs explicitement non normatifs
  use_cases/
    MODELE_DOSSIER.md
    UC-C-xx/                     13/14/15 produits; autres dossiers à constituer
  modele_global/                 G-C0A-R1 produit, limité à C0-A
  lots/C0-A/                    rapport et patch déjà conservés
```

`use_cases/UC-C-xx/` contiendra `specification.md`, `activity.puml`, `sequence.puml`, `erd.puml`, `class.puml`, les SVG, `validation.md` et `tracabilite.md`. Les dossiers manquants ne sont pas créés comme coquilles vides. Les [deux vues globales G-C0A-R1](modele_global/README.md) et les dossiers 13/14/15 sont désormais produits, bornés à C0-A : ce sont des cibles, distinctes des relevés P6 existants.

Les 15 stories initiales deviennent 17 dossiers de use cases : 01 se sépare en création initiale 01A et nouvelle version issue du gel 01B; 05 se sépare en examen éditorial neutre 05E et décision d’appui 05P. Quatre stories nouvelles 16–19 ajoutent cinq dossiers, car préparation 18A et restitution 18B ont des dépendances différentes. Total : **22 use cases identifiés**, sans renuméroter les stories historiques.

## 2. Inventaire, dépendances et ordre recommandé

Dans les dépendances, `13` signifie UC-C-13; les niveaux P0–P7 sont des vagues de conception. Ils ne constituent pas une autorisation de lot ni un ordre d’implantation automatique. Les statuts ci-dessous sont le constat initial de cette livraison; leur autorité courante est le registre.

| Use case | Comportement / stories | Lot(s) | Dépendances et réserves | Ordre | Statut initial |
|---|---|---|---|---|---|
| **UC-C-01A** | Créer le contexte et une première version de travail; US-C-01; V2:US-01 | L1-A | 13/14/15; R06 | P1 | `A_SPECIFIER` |
| **UC-C-01B** | Ouvrir une version amendée depuis un état figé; US-C-01/11; V2:US-11 | L5/L6 | 01A, 11; R06 | P7 | `A_SPECIFIER` |
| **UC-C-02** | Structurer et numéroter la rédaction; US-C-02; V2:US-02 | L1-B | 01A; primitives 05E; 13/14 | P2 | `A_MODELISER` |
| **UC-C-03** | Organiser une preuve réutilisable; US-C-03; V2:US-03 | L2 | 01A, 02; 13 | P3 | `A_MODELISER` |
| **UC-C-04** | Sélectionner les éléments par utilisation; US-C-04; V2:US-04 | L2/L3-A | 03, 02; R05; CF4 selon type | P3 | `A_SPECIFIER` |
| **UC-C-05E** | Examiner la filiation dans un journal immuable; US-C-05; V2:US-02/03 | L1-A | 13/14/15; Correspondance E01 existante | P1 | `A_MODELISER` |
| **UC-C-05P** | Décider les appuis des utilisations C et leur portée; US-C-05; V2:US-03 | L2 | 05E, 04, 12; appuis E01 traités par 12 | P3 | `A_MODELISER` |
| **UC-C-06** | Déclarer les renvois et dépendances rédactionnels; US-C-06; V2:US-03 | L1-B; contrôles de gel L5 | 01A, 02, 05E; contrat d’état de version | P2 | `A_MODELISER` |
| **UC-C-07** | Reprendre un sous-arbre avec contexte et usages décidés; US-C-07; V2:US-11 | L2; intégration L6 | 02, 03, 04, 05E/05P, 06, 12; 08 si insertions; contrat 11 si source figée | P4 | `A_MODELISER` |
| **UC-C-08** | Composer et insérer une citation fidèle; US-C-08; V2:US-06 | L3-B/L4 | 02, 04; fournisseur A versionné; D07; R04 pour sous-cotes | P4 | `A_SPECIFIER` |
| **UC-C-09** | Calculer la cotation et le bordereau CHRONO_VERSION; US-C-09; V2:US-05/09 | L3-A | 04, 16; D06; R02/R03/R04 | P5 | `A_SPECIFIER` |
| **UC-C-10** | Rendre depuis un ResultatVersion strict cohérent; US-C-10; V2:US-06/09/10 | L3/L4 | 08/09, 05P, 12; profils de sources vérifiés | P5 | `A_MODELISER` |
| **UC-C-11** | Finaliser le gel cohérent et conserver le contenu; US-C-11; V2:US-07 | L5 | 05E, 05P, 06, 09, 10, 18A; R08 | P6 | `A_SPECIFIER` |
| **UC-C-12** | Consulter la filiation et adopter les décisions éditoriales/probatoires E01; US-C-12; V2:US-02/11 partiel | C0-B/L6 | 05E; 13/14/15; pas de dépendance obligatoire à Preuve | P2 | `A_MODELISER` |
| **UC-C-13** | Modifier une occurrence partagée sans altérer les autres; US-C-13; V2:US-02 | C0-A | P6; dossier à quatre vues et revue du patch existant | P0 | `A_MODELISER` |
| **UC-C-14** | Supprimer un bloc autorisé en préservant les traces; US-C-14; V2:US-02 | C0-A | P6; 13 pour le contrat de capture; pas de nouveau schéma | P0 | `A_MODELISER` |
| **UC-C-15** | Lire les appuis de la bonne origine documentaire; US-C-15; V2:US-02 partiel | C0-A | P6; types et couple; pas de champ nature anticipé | P0 | `A_MODELISER` |
| **UC-C-16** | Définir et réutiliser les pièces et leurs compositions; US-C-16 nouvelle; V2:US-04 | L3-A; composants L4 | 04; R01–R05; D04/D07/CF4 selon type | P4 | `A_SPECIFIER` |
| **UC-C-17** | Comparer les pièces et cotes de deux versions figées; US-C-17 nouvelle; V2:US-08 | L6; contrats L3-A | 16, 09, 11; R01/R02; états historiques disponibles | P7 | `A_SPECIFIER` |
| **UC-C-18A** | Préparer le dossier de production et son manifeste; US-C-18 nouvelle; V2:US-10 | L3/L4 | 16, 09, 10; contrat stockage candidat; pas de finalisation implicite | P5 | `A_MODELISER` |
| **UC-C-18B** | Restituer les livrables historiques conservés; US-C-18 nouvelle; V2:US-10 | L5/L6 | 11, 18A; R07; lecture seule des objets figés | P7 | `A_SPECIFIER` |
| **UC-C-19** | Consigner dépôts et communications attestés; US-C-19 nouvelle; V2:US-12 | L6 | 11, 18B; preuves numériques ou papier identifiées | P7 | `A_MODELISER` |

## 3. Les quatre vues par dossier : disponibles et manquantes

**A0** désigne une activité initiale réellement disponible, à réexaminer et contextualiser dans le nouveau dossier. **S**, **E** et **C** désignent respectivement la séquence, l’ERD cible et les classes cibles. Un ERD ou diagramme de classes observé P6 ne compte pas comme vue cible du use case. Au constat initial, aucun quadruplet cible n’était complet. Au point R2, 13/14/15 ont leurs quatre vues compilées; 13 est validé B et 14/15 restent en revue. Le registre porte les transitions courantes.

| Use case | Activité de départ | Séquence | ERD cible | Classes cibles | Tests à rattacher sans les déclarer exécutés |
|---|---|---|---|---|---|
| UC-C-01A | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/01_contexte_versionne.puml) | À produire | À produire | À produire | VF01/VF08; CF3-01/02/23; C-UML:N12 |
| UC-C-01B | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/01_contexte_versionne.puml) | À produire | À produire | À produire | EPIC-V2:T07/T12; CF3-16/18; C-UML:N12 |
| UC-C-02 | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/02_structure_numerotation.puml) | À produire | À produire | À produire | C:T01–T05/T22; NR02; CF3-21 |
| UC-C-03 | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/03_organiser_preuve.puml) | À produire | À produire | À produire | C:T06/T07/T17/T21; VF13; CF3-08/24 |
| UC-C-04 | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/04_selection_effective.puml) | À produire | À produire | À produire | C:T08/T12/T21; VF03/VF14; CF3-07/08/12/24; EPIC-V2:T03 |
| UC-C-05E | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/05_rattachement_examen.puml) | À produire | À produire | À produire | IM01–IM08; CF3-20; NR06/12; TR03 |
| UC-C-05P | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/05_rattachement_examen.puml) | À produire | À produire | À produire | NR03/06/12; TR01–TR06; C:T08/T12 |
| UC-C-06 | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/06_liens_redactionnels.puml) | À produire | À produire | À produire | VF05–VF11; CF3-12/14–18/21 |
| UC-C-07 | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/07_reprise_partielle.puml) | À produire | À produire | À produire | CF3-01–CF3-26; VF02–VF05/VF08; NR04/11/12 |
| UC-C-08 | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/08_citation_composite.puml) | À produire | À produire | À produire | C:T09–T11/T18/T19; C:N01/N03–N05; VF04; CF3-10/11/26; A:T2.1–T2.9 |
| UC-C-09 | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/09_bordereau_cotation.puml) | À produire | À produire | À produire | EPIC-V2:T01–T06/T09/T13/T14; NR08; CF3-24 |
| UC-C-10 | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/10_rendu_strict.puml) | À produire | À produire | À produire | EX01–EX07 applicables; TR06; C:T14/T18/T19; EPIC-V2:T02/T13 |
| UC-C-11 | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/11_gel_conservation.puml) | À produire | À produire | À produire | EPIC-V2:T07/T11/T12/T14; CF3-16–19/25; IM05/07; C-UML:N07–N09 |
| UC-C-12 | [A0 à revoir](../modele_preuve/diagrammes/user_stories_architecture_c/12_concordance_historique.puml) | À produire | À produire | À produire | NR04–NR10/NR12; TR01–TR06; IM06; EX01–EX07 |
| UC-C-13 | [Produite R1](use_cases/UC-C-13/activity.svg) | [Produite R1](use_cases/UC-C-13/sequence.svg) | [Produite R1](use_cases/UC-C-13/erd.svg) | [Produite R1](use_cases/UC-C-13/class.svg) | NR01/03/11; TR02; classes C0AEditionEtConservation/C0AFraicheurEtPerimetre |
| UC-C-14 | [Produite R1](use_cases/UC-C-14/activity.svg) | [Produite R1](use_cases/UC-C-14/sequence.svg) | [Produite R1](use_cases/UC-C-14/erd.svg) | [Produite R1](use_cases/UC-C-14/class.svg) | NR01/11/12 dans le périmètre C0-A; suppression avec décision refusée; rollback HTTP |
| UC-C-15 | [Produite R1](use_cases/UC-C-15/activity.svg) | [Produite R1](use_cases/UC-C-15/sequence.svg) | [Produite R1](use_cases/UC-C-15/erd.svg) | [Produite R1](use_cases/UC-C-15/class.svg) | NR07; CF3-26 noyau typé; cinq tests lecteur/export/type/archive du rapport C0-A |
| UC-C-16 | À produire | À produire | À produire | À produire | EPIC-V2:T03/T10; C-UML:N03–N06/N10/N16; CF3-24 |
| UC-C-17 | À produire | À produire | À produire | À produire | EPIC-V2:T08/T09/T10/T14; C-UML:N02/N04/N06/N11 |
| UC-C-18A | À produire | À produire | À produire | À produire | EPIC-V2:T11/T13; C-UML:N07/N08/N10; contrôles fichiers absents/ordres divergents |
| UC-C-18B | À produire | À produire | À produire | À produire | EPIC-V2:T12/T13/T14; C-UML:N09/N11; fichiers conservés sans recalcul |
| UC-C-19 | À produire | À produire | À produire | À produire | C-UML:T19-01–T19-06; C-UML:N11; gel sans envoi, envois multiples, papier incertain |

Pour les 22 dossiers : **88 vues contractuelles finales** seront nécessaires au minimum. Les 15 activités sources donnent des bases à 17 dossiers; cinq activités sont nouvelles. Initialement, il restait donc 71 vues à créer et 17 activités à réexaminer, sans compter les séquences supplémentaires de panne/concurrence ni les deux modèles globaux. Ce décompte était celui de l’initialisation R1. Au point R2, 12 vues locales sont produites pour 13/14/15 et les deux vues globales existent. Les 19 autres dossiers demandent encore 76 vues finales (62 nouvelles et 14 activités à réexaminer). Leur validation n’est pas acquise.

Références observées réutilisables : [ERD P6](../modele_preuve/diagrammes/erd_etat_actuel/README.md), [classes P6](../modele_preuve/diagrammes/classes_etat_actuel/README.md), [registre des 38 scénarios](DECISIONS_ARCHITECTURE_C_CONSOLIDEES.md#81-les-38-scénarios-du-dernier-addendum). Les classes P6 ont été produites après `30ce0ac`; elles ne sont pas prétendues présentes dans ce commit documentaire.

## 4. Ordre et acceptation des vagues de conception

- **P0 — UC-C-13/14/15.** Concevoir les quatre vues de chacun à partir du périmètre réel C0-A, examiner le patch, traiter les refus et l’atomicité. Le premier dossier à soumettre est UC-C-13. Le lot C0-A entier ne passe pas la porte tant que ses trois dossiers ne la satisfont pas. L’essai isolé antérieur ne reçoit aucune validation rétroactive.
- **P1 — 01A et 05E.** Contexte neutre et journal d’examens, sans dépendance à Preuve. Trancher R06 pour le périmètre de création; couvrir les attaques ORM/bulk/SQL et les rôles. C’est le socle conceptuel de L1-A, pas un mandat de l’exécuter avant l’atterrissage de C0-A.
- **P2 — 12, 02 et 06.** Adoption E01, numérotation et liens. Préserver LEGACY/STORED et la distinction confirmation éditoriale/appui. La partie 12 porte également la transition et les confirmations d’appui E01, sans dépendre de la future organisation des preuves. UC-C-05P ne porte que les appuis des utilisations C en L2 : il ne crée donc pas une dépendance circulaire C0-B → L2 → C0-B.
- **P3 — 03, 04 et 05P.** Organisation, usages/sélections et décisions d’appui. Traiter R05; les groupes n’héritent pas leurs appuis aux enfants. Les primitives communes ne déclarent pas CF3 complet.
- **P4 — 07, 08 et 16.** Reprise complète, citations et compositions. Trancher R01–R05 selon le chemin; inspecter l’interface PHRASE de A sans modifier ses ressources. Le contrat de lecture d’un état figé et de refus d’une destination figée peut être spécifié avant l’activation réelle du gel; sa preuve d’intégration reste L5/L6.
- **P5 — 09, 10 et 18A.** Cotation, strict et préparation des fichiers. Aucun exporteur n’a sa propre cotation. Les candidats ne sont pas présentés comme finalisés. Les décisions de date et de sous-cotation nécessaires sont préalables aux vues finales concernées.
- **P6 — 11.** Choisir et éprouver le protocole base/stockage R08 sur les vues de concurrence et de panne; aucun premier gel réel avant ses protections. Le contrat des fichiers candidats vient de 18A, ce qui évite le cycle préparation↔gel.
- **P7 — 01B, 17, 18B et 19.** Nouveaux brouillons depuis gel, concordance documentaire exhaustive, restitution historique et communications. Toutes les lectures historiques reposent sur des captures; les événements restent distincts du gel. Résoudre R07 avant une promesse de régénération supplémentaire.

Un use case peut être conçu avant la livraison de ses dépendances; il ne devient prêt au développement que dans le périmètre approuvé et avec les préalables du protocole satisfaits. La disponibilité de données d’essai ne prouve pas la disponibilité d’une source réelle. Les travaux de conception peuvent avancer sans la bascule réelle de A; l’exécution d’un lot reste interdite tant que le précédent n’est pas atterri.

## 5. Quatre stories complémentaires proposées

Ces critères fixent le besoin à rattacher à V2 et au mandat; les options R01–R08 restent ouvertes. Ils ne constituent pas une approbation de dossier UML.

### US-C-16 — Composer les pièces produites

En tant que rédacteur, je veux définir les unités documentaires produites depuis mes usages afin de conserver leur identité et leur composition indépendamment des cotes.

- **AC01** : distinguer identités de source et de pièce, composition exacte et cote de version.
- **AC02** : conserver composantes ordonnées, états sources, contenants et passages autorisés.
- **AC03** : répéter un usage ne duplique pas sa pièce; les chemins d’usage sont conservés.
- **AC04** : un titre, une cote ou une source partagée ne fusionne pas des identités distinctes.
- **AC05** : `[A,B]→[A,C]` et `[A,B]→[B,A]` révèlent la modification de composition, sans modifier V1.
- **AC06** : distinguer usages analytiques et production sans effet d’un filtre d’affichage.
- **AC07** : préserver les unités D04 et la provenance des fragments/sous-cotes selon la politique approuvée.
- **AC08** : une composition manquante, source ambiguë ou règle R non décidée refuse le chemin strict concerné.

### US-C-17 — Comparer les pièces entre versions

En tant que lecteur, je veux retrouver les pièces, leurs compositions et cotes de deux versions afin de comprendre leurs différences sans dépendre du travail actuel.

- **AC01** : nommer les deux versions et couvrir l’union des bordereaux.
- **AC02** : distinguer conservation, ajout, retrait, recotation et modification de composition; changements cumulables.
- **AC03** : ne jamais rapprocher deux pièces sur la seule cote ou le seul titre.
- **AC04** : conserver les cartes N:M explicites des scissions/fusions et les motifs des décisions.
- **AC05** : rendre visibles les candidats non univoques sans équivalence fabriquée.
- **AC06** : calculer depuis les états figés, même après mutation/suppression autorisée du travail courant.
- **AC07** : conserver les associations et lacunes attestées de juillet; aucune validation rétroactive.
- **AC08** : permettre consultation/export et historique multi-version avec contexte des libellés.

### US-C-18 — Produire puis restituer le dossier documentaire

En tant que rédacteur, je veux préparer un dossier cohérent puis restituer les fichiers conservés d’une version afin que texte, pièces, bordereau et cahier concordent.

- **AC01** : préparation 18A et restitution 18B utilisent une version et un résultat identifiés.
- **AC02** : conserver un ou plusieurs fichiers ordonnés par pièce, avec noms, formats, tailles et empreintes.
- **AC03** : inclure acte, bordereau, cahier/assemblages et manifeste cohérents avec le même ResultatVersion.
- **AC04** : ne jamais modifier les originaux pour produire les dérivés.
- **AC05** : refuser fichier absent, mélange de révisions, rendu en défaut ou correspondance de pièce ambiguë.
- **AC06** : les candidats préparés ne sont pas une version figée ni un envoi.
- **AC07** : une panne et sa reprise ne publient pas un ensemble partiellement finalisé; coordination avec UC-C-11.
- **AC08** : restituer les octets conservés d’une version figée sans recalcul de cotes.
- **AC09** : une régénération éventuelle est un dérivé tracé, selon R07, sans remplacement silencieux.
- **AC10** : l’accès historique conserve version, pièce, composition et contexte de cote pour chaque fichier.

### US-C-19 — Consigner les communications et dépôts

En tant que rédacteur, je veux relier chaque événement réel à la version et au support concernés afin de conserver ce qui a été transmis ou déposé.

- **AC01** : identifier la version, la nature d’événement et sa preuve disponible.
- **AC02** : conserver date, destinataires et modalités sans inventer de fait manquant.
- **AC03** : identifier les fichiers transmis par leurs noms/empreintes lorsqu’ils existent.
- **AC04** : permettre plusieurs événements sur une même version sans réécrire son contenu.
- **AC05** : un gel sans communication n’en crée aucune; dépôt et communication ne sont pas des états exclusifs obligatoirement successifs.
- **AC06** : documenter le papier et ses incertitudes sans lui attribuer automatiquement l’identité exacte d’un fichier.

## 6. Premier passage possible et limite de la présente intervention

Ces dossiers et la première version globale sont produits. La prochaine étape est l’approbation de 13, la clôture des revues de 14/15, puis leur approbation et un mandat A de correction/validation isolée du patch. Les arbitrages des composites ne bloquent pas ces corrections sans schéma. L’atterrissage C0-A reste un mandat distinct et exige les conditions du processus.

Le premier **nouveau** lot candidat demeure L1-A après cet atterrissage et les dossiers correspondants. UC-C-13 est validé B documentaire; aucun dossier n’est approuvé utilisateur ou prêt au développement et aucun ordre de mission de code n’est transmis à A.


## 7. Clarifications de couverture R2

Les compléments normatifs proposés sont centralisés dans la [matrice §9](MATRICE_COUVERTURE_V2_C.md#9-compléments-de-couverture-du-mandat-de-revue-r2) : constat d’absence dans 03/04/05P, consultation des régimes dans 03/04/08, recherche/retour dans 03 et parcours transversal, anomalie mixte dans 15. Aucune story ou UC supplémentaire.

Les dépendances de la table §2 distinguent désormais explicitement leur portée : un contrat de futur UC11/17/18A/18B nécessaire à 07/09/10/16 est une interface à définir et examiner, pas son implantation complète préalable. Le [rapport §4](RAPPORT_REVUE_COUVERTURE_ET_C0A.md#4-d--trois-graphes-sans-cycle-dexécution) fournit les arcs d’exécution des dix lots et leur contrôle acyclique. Les quatre vues des comportements implantés et les mandats restent obligatoires.
