# Mémoire méthodologique — travail postérieur au dépôt

Dernière mise à jour : 27 juillet 2026

## 1. Statut de cette mémoire

La présente méthodologie est **approuvée** comme cadre de travail pour la suite
du projet.

Elle fixe les règles de conservation du dépôt, de gestion des cotes, de
traçabilité et de validation. Elle ne fixe toutefois **pas** la forme finale de
la section « Exposé des faits ».

Le demandeur souhaite expérimenter plusieurs façons d’organiser et de rédiger
les faits avant de choisir une architecture définitive. Aucun plan narratif
particulier — chronologique, thématique, centré sur les actes reprochés ou
hybride — ne doit donc être présenté comme une décision acquise.

## 2. Situation procédurale de référence

- Une demande introductive et un bordereau de preuve ont été déposés avant
  l’échéance de prescription du 25 juillet 2026.
- La demande n’a pas encore été notifiée/signifiée aux autres parties.
- Le demandeur a été informé qu’il pouvait modifier la demande après son dépôt.
- Le dépôt initial doit être conservé comme un jalon historique distinct.
- La version destinée à la notification sera une version modifiée, dont les
  différences avec la version déposée devront être retraçables.
- La date exacte apparaissant sur la preuve de dépôt doit servir au calcul du
  délai de notification; elle ne doit pas être déduite du seul nom des fichiers.

## 3. Principes approuvés

### 3.1 Préserver le dépôt initial

Les documents effectivement déposés ne doivent plus être utilisés comme fichiers
de travail ni être écrasés par une version ultérieure.

Une archive de référence doit réunir, lorsque les originaux exacts auront été
confirmés :

```text
legal/depots/2026-07-25_initial/
├── demande_deposee.pdf
├── demande_deposee.docx
├── bordereau_depose.pdf
├── preuve_de_depot.pdf
├── cotes.lock.json
└── SHA256SUMS
```

La constitution de cette archive exige d’identifier les fichiers réellement
transmis au greffe. Il ne faut pas présumer que l’état courant d’un fichier
portant « DEPOT » dans son nom correspond exactement au fichier déposé.

### 3.2 Travailler dans une version amendée séparée

Le travail postérieur au dépôt doit vivre dans un espace distinct :

```text
legal/amendements/01_avant_notification/
├── demande_amendee.md
├── faits_experimentaux/
├── concordance_ancien_nouveau.csv
├── journal_modifications.md
├── bordereau_amende.md
└── rapports_audit/
```

Cette structure est une cible méthodologique. Sa création matérielle peut être
faite progressivement, une fois les fichiers exacts du dépôt identifiés.

### 3.3 Verrouiller l’identité des cotes

Les cotes P-1 à P-106 sont des identifiants procéduraux permanents.

Règles :

1. Une cote conserve toujours la même source documentaire.
2. Une cote retirée du récit ne peut pas être réutilisée pour une autre pièce.
3. Une nouvelle pièce reçoit P-107 ou la prochaine cote disponible après les
   cotes déjà attribuées.
4. Une pièce existante conserve la même cote dans la demande, le bordereau,
   les PDF normalisés et le cahier.
5. Une modification de description ne modifie pas l’identité documentaire et
   doit être inscrite au journal des changements.
6. Une pièce qui n’est plus invoquée doit être marquée comme telle; sa cote
   ne doit pas disparaître ou être réaffectée silencieusement.

Le registre technique `legal/bordereau_pieces.md` relie les cotes aux sources
de la base. Le bordereau procédural `legal/bordereau_bloc_depot.md` représente
la présentation destinée au dépôt ou à la communication. Les deux documents
ont des fonctions différentes et doivent demeurer concordants.

### 3.4 Maintenir une concordance entre les versions

Toute refonte substantielle doit produire une table de concordance :

| Élément déposé | Élément amendé | Traitement | Motif | Cotes touchées |
|---|---|---|---|---|
| § ou bloc initial | identifiant de travail | conservé, fusionné, scindé, reformulé ou retiré | justification courte | P-n |

Cette concordance permet de démontrer que la version amendée demeure reliée à
la demande initiale et d’identifier clairement les changements.

### 3.5 Utiliser des identifiants de faits stables

Pendant les expérimentations, les faits devraient recevoir des identifiants
internes indépendants de leur numéro final, par exemple :

```markdown
<!-- FACT_ID: F15-009-A -->
```

Le même fait peut ainsi être déplacé, fusionné ou testé dans plusieurs plans
sans perdre sa source ni son historique. La numérotation procédurale continue
sera générée seulement lorsque la version retenue sera assemblée.

## 4. Statut particulier de la section « Exposé des faits »

### 4.1 Décision actuelle

La section des faits doit être entièrement retravaillée, car sa version actuelle
n’est pas jugée satisfaisante.

Toutefois, **aucune architecture définitive n’est choisie**.

Les formes suivantes peuvent être explorées :

- chronologie stricte;
- organisation par acte procédural contesté;
- organisation par élément de responsabilité;
- organisation thématique;
- architecture hybride;
- version courte centrée sur les faits essentiels;
- version plus développée comportant davantage de contexte.

Cette liste n’est pas limitative et ne constitue pas une préférence arrêtée.

### 4.2 Règle d’expérimentation

Les variantes doivent être conservées séparément et comparées selon des critères
communs. Une expérience ne doit pas écraser une autre variante ni être intégrée
à la demande amendée principale avant une décision explicite.

Exemple :

```text
faits_experimentaux/
├── variante_A_chronologique.md
├── variante_B_actes_reproches.md
├── variante_C_elements_responsabilite.md
├── variante_D_hybride.md
└── comparaison_variantes.md
```

### 4.3 Invariants applicables à toutes les variantes

Même si la forme demeure ouverte, chaque variante doit :

- préserver les mêmes identifiants de faits;
- préserver les mêmes cotes pour les mêmes sources;
- distinguer fait, preuve et qualification juridique;
- permettre de retracer chaque proposition vers une ou plusieurs pièces;
- distinguer fait essentiel, contexte et corroboration;
- identifier les faits reposant uniquement sur la connaissance personnelle;
- conserver les concessions et limites probatoires;
- éviter de transformer une inférence en fait établi;
- permettre une comparaison avec la version déposée;
- demeurer compatible avec une numérotation finale continue.

### 4.4 Grille de comparaison des variantes

Chaque variante pourra être évaluée selon :

1. clarté de la théorie du dossier;
2. compréhension par un lecteur qui ne connaît pas l’historique;
3. concision;
4. séparation entre faits et argumentation;
5. visibilité des actes précis reprochés;
6. continuité de la chronologie;
7. facilité de rattachement aux éléments juridiques;
8. densité et pertinence des renvois aux pièces;
9. risque de répétition;
10. capacité de résister au retrait d’un fait ou d’une pièce;
11. facilité de comparaison avec la demande déposée;
12. lisibilité générale de l’acte.

Une architecture ne sera retenue qu’après comparaison explicite.

## 5. Couches documentaires à conserver

La chaîne conceptuelle demeure :

```text
objet Django/PostgreSQL + original
→ fiche piece_*.md
→ axe thématique
→ faits organisés par allégation
→ analyse
→ pont procédural
→ variante expérimentale de l’exposé
→ demande amendée retenue
→ bordereau et pièces assemblées
```

Les fiches `piece_*.md` sont des représentations de travail dérivées. Elles ne
remplacent pas les originaux conservés par l’application Django et ses espaces
de stockage.

## 6. Journal des changements

Le journal de l’amendement doit au minimum noter :

- date du changement;
- fichier ou bloc touché;
- nature du changement;
- faits concernés;
- cotes concernées;
- effet éventuel sur les conclusions;
- caractère purement rédactionnel ou substantiel;
- auteur ou outil ayant effectué le changement;
- validation exécutée après le changement.

Il doit être possible de distinguer :

1. correction linguistique;
2. déplacement sans changement de sens;
3. fusion ou scission de faits;
4. reformulation substantielle;
5. ajout d’un fait;
6. retrait d’un fait;
7. ajout ou retrait d’une pièce;
8. modification d’une conclusion.

## 7. Barrières de validation

Avant toute version destinée à la notification ou à la communication :

```bash
python manage.py audit_piece_files --strict
```

L’audit doit notamment confirmer :

- concordance entre les deux bordereaux;
- stabilité de l’identité des cotes;
- existence des objets PostgreSQL;
- disponibilité des originaux nécessaires;
- cohérence entre les fiches `piece_*.md` et les sources;
- présence d’un renderer utilisable;
- absence de placeholder;
- concordance entre le bordereau et `pieces_pdf/manifest.json`;
- présence et lisibilité de tous les PDF P-n;
- concordance de l’ordre des sous-cotes.

Des validations complémentaires devront couvrir la demande amendée :

- toute cote citée existe dans le registre;
- aucune cote P-1 à P-106 n’a changé de source;
- toute nouvelle cote est ajoutée après les cotes existantes;
- chaque fait essentiel possède une provenance identifiable;
- la concordance ancien/nouveau est complète;
- les paragraphes finaux sont numérotés consécutivement;
- le bordereau, les pièces assemblées et le cahier correspondent à la même
  version de la demande.

## 8. Seuils de préparation

Trois seuils distincts sont utilisés :

1. `source_ready` : identités et sources cohérentes;
2. `render_ready` : sources matériellement transformables en PDF;
3. `communication_ready` : bordereaux, PDF et assemblage complets, concordants
   et sans placeholder.

Une version ne doit pas être qualifiée de prête à communiquer tant que
`communication_ready` est faux.

## 9. État constaté au moment de l’adoption de cette méthode

- Le registre technique et le bordereau procédural contiennent P-1 à P-106.
- Les 22 groupes de sous-cotes indexés concordent.
- L’assemblage existant contient 105 cotes et ne contient pas encore P-106.
- P-19, P-40, P-42 et P-58 à P-64 sont actuellement des placeholders.
- Des divergences de liaison demeurent notamment pour P-22, P-27, P-92, P-98,
  P-100 et P-106.
- L’assemblage courant n’est pas prêt à communiquer.

## 10. Prochaine décision méthodologique attendue

La prochaine décision ne consiste pas à choisir immédiatement le plan définitif
des faits. Elle consiste à déterminer quelles variantes seront expérimentées,
avec quel échantillon représentatif et selon quels critères de comparaison.

Une bonne expérience initiale peut porter sur un seul bloc — par exemple une
allégation de 2015 — rédigé selon deux ou trois architectures. Le choix final
sera fait après comparaison, puis appliqué au reste de la section.
