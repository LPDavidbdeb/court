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

- Une demande introductive et un bordereau de preuve ont été déposés le
  **24 juillet 2026**.
- La demande n’a pas encore été notifiée/signifiée aux autres parties.
- Le demandeur a été informé qu’il pouvait modifier la demande après son dépôt.
- Le dépôt initial doit être conservé comme un jalon historique distinct.
- La version destinée à la notification sera une version modifiée, dont les
  différences avec la version déposée devront être retraçables.
- La date exacte apparaissant sur la preuve de dépôt doit servir au calcul du
  délai de notification; elle ne doit pas être déduite du seul nom des fichiers.
  L’acte se signe « Daté du 21 juillet 2026 » et les fichiers portent
  `2026-07-21` : ni l’un ni l’autre ne correspond à la date réelle du dépôt.

### 2.1 Échéance gouvernante

Deux délais courent en parallèle et **c’est le plus court qui gouverne** :

| Règle | Objet | Sanction | Échéance |
|---|---|---|---|
| Art. 2892 C.c.Q. | signification dans les 60 jours de l’expiration de la prescription | interruption perdue rétroactivement → recours prescrit | **19 septembre 2026** (ancre conservatrice) |
| Art. 107 C.p.c. | notification dans les 3 mois du dépôt | péremption | 24 octobre 2026 |

Toute planification du travail postérieur au dépôt se règle sur le
**19 septembre 2026**. Les deux textes et leur application au dossier doivent
être validés auprès d’un professionnel du droit ou du greffe.

Le dépôt du 24 juillet se situe entre les deux ancres de prescription possibles
sur P-40 : trois jours après le 21 juillet 2026 (assermentation), un jour avant
le 25 juillet 2026 (connaissance, plaidée au §234). L’analyse est consignée dans
`PROJECT_CONTEXT.md`; la réserve du corpus sur la date du 21 juillet n’est pas
levée par le dépôt.

### 2.2 Effet de l’amendement sur la prescription

L’interruption produite par le dépôt couvre la cause d’action déposée. Un fait
ou un chef **nouveau** ajouté après le 25 juillet 2026 n’en bénéficie pas
nécessairement. Règle de travail : tout ajout à la version amendée doit se
rattacher à un fait ou à un chef déjà allégué au dépôt, ou être expressément
signalé comme cause nouvelle et son exposition à la prescription évaluée.

## 3. Principes approuvés

### 3.1 Préserver le dépôt initial

Les documents effectivement déposés ne doivent plus être utilisés comme fichiers
de travail ni être écrasés par une version ultérieure.

L’archive de référence est constituée :

```text
legal/depots/2026-07-24_initial/
├── README.md            état établi / état non établi
├── cotes.lock.json      identité figée des 106 cotes
├── SHA256SUMS           empreintes des candidats
└── candidats/           les 5 fichiers produits le 24 juillet + sources .md
```

Elle est ancrée au commit `1f0af56` (« etat au dépot »), qui capture l’arbre
complet à la date du dépôt.

Deux éléments restent à verser : la **preuve de dépôt du greffe** et
l’**identification du fichier exactement transmis**. Il ne faut pas présumer
que l’état courant d’un fichier portant « DEPOT » dans son nom correspond
exactement au fichier déposé — cinq candidats ont été produits le même jour
entre 13 h 57 et 14 h 29. Tant que ce point n’est pas tranché, aucune
comparaison ancien/nouveau n’est fiable.

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
- **effet sur la prescription** : reformulation d’une cause déjà déposée, ou
  cause nouvelle exposée au délai (§2.2);
- **visibilité en contradiction** : le changement retire-t-il ou atténue-t-il
  une concession, une limite probatoire ou une admission figurant au dépôt (§6.1);
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

### 6.1 Le diff sera lisible par la partie adverse

Les défenderesses n’ont pas reçu la version déposée, mais celle-ci est au
dossier de la cour et leur est accessible. L’écart entre la version déposée et
la version notifiée est donc un document adverse potentiel.

La demande déposée contient des concessions délibérées et calibrées — notamment
le §22-A (asymétrie quantitative reconnue, trente-deux semaines de prestations
parentales) et le §234 (reconnaissance qu’une caractérisation sous l’art. 2929
C.c.Q. serait opposable). Retirer ou atténuer une telle concession n’est pas un
choix rédactionnel neutre : c’est un instrument de contre-interrogatoire offert
à la partie adverse. La table de concordance doit rendre ces cas visibles.

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

⚠️ **Ce que l’audit ne fait pas.** `audit_piece_files` contrôle la cohérence
*interne à l’instant t* (fiches ↔ bordereaux ↔ PostgreSQL ↔ PDF assemblés). Il
ne mesure aucune **dérive par rapport au dépôt** : il ne peut donc pas, en
l’état, vérifier qu’une cote n’a pas changé de source depuis le 24 juillet. Cette
vérification suppose une comparaison avec
`legal/depots/2026-07-24_initial/cotes.lock.json`, qui existe désormais mais
n’est pas encore outillée. Tant qu’un mode de comparaison au verrou n’est pas
implémenté, la règle du §3.3 demeure déclarative et doit être vérifiée à la main.

Des validations complémentaires devront couvrir la demande amendée :

- toute cote citée existe dans le registre;
- aucune cote P-1 à P-106 n’a changé de source (comparaison au verrou);
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

## 9. État de l’assemblage

Régénération complète le 27 juillet 2026 (`sync_pieces_pdf`) :

- Le registre technique et le bordereau procédural contiennent P-1 à P-106.
- Les 22 groupes de sous-cotes indexés concordent.
- **L’assemblage contient les 106 cotes, 1 425 pages, aucun placeholder,
  aucune erreur de rendu.** P-106 est désormais assemblée.
- Il ne reste **aucune erreur de niveau `render` ni `communication`**.

Restent 9 erreurs, toutes au niveau `source`, qui bloquent `source_ready` et
donc, en cascade, les deux seuils suivants :

- **6 divergences de liaison** entre le bordereau et les fiches d’appui —
  P-22, P-27, P-92, P-98, P-100 et P-106. La cote et le bordereau désignent
  une source que la fiche `piece_*.md` ne confirme pas. À trancher fiche par
  fiche : c’est l’identité documentaire d’une cote qui est en jeu (§3.3).
- **3 fiches sans identité résoluble** : `piece_courriel_philemon_2023-07-25.md`,
  `piece_emails_petite_enfance_2010.md`, `piece_pension_nonmodif_jan2019.md`.

Six autres fiches non rattachées à une cote demeurent en avertissement
(jurisprudence, règlement, tableau récapitulatif, pièces financières 2018-2019).

### 9.1 Trois placeholders portent la demande déposée

Les placeholders ne sont pas un retard d’assemblage indifférent : trois d’entre
eux sont les actes mêmes dont la demande fait déclarer le contenu faux.

| Cote | Pièce | Citations dans l’acte déposé |
|---|---|---|
| P-19 | Requête assermentée du 19 nov. 2015 | 29 |
| P-42 | Déclaration assermentée du 21 oct. 2019 | 19 |
| P-40 | Dénonciation du 21 juil. 2023 — **ancre de prescription du §234** | 17 |

Le bordereau déposé déclare par ailleurs communiquer « les pièces P-1 à P-106 »,
dont P-106 qui n’est pas assemblée.

### 9.2 Origine des pièces — ce qui peut être généré et ce qui ne le peut pas

Deux régimes distincts, à ne jamais confondre.

**a) Les actes incriminés — l’original s’impose.** P-19, P-40 et P-42 sont les
actes de la partie adverse dont la demande fait déclarer le contenu faux ou
trompeur. Leur **libellé exact est le fait opérant** : c’est lui qu’on oppose,
et l’argument de connaissance repose précisément sur les mots employés plutôt
que sur d’autres. Une reproduction régénérée à partir de la base serait la
**transcription faite par celui-là même qui allègue le mensonge** — la partie
adverse n’aurait qu’à contester la fidélité du rendu pour déplacer le débat de
son acte vers la version du demandeur. La règle de la meilleure preuve
(art. 2860 C.c.Q.) commande l’original ou une copie qui en tient légalement
lieu.

**Ces originaux sont en main** : `media/evidence_files/`, liés par
`Document.file_source` (documents 1, 2 et 3), numérisations de 16, 5 et 4 pages,
sans couche texte. Le statut de placeholder était un **défaut de câblage de
l’assemblage**, non une absence de preuve. Une copie certifiée conforme du
greffe reste souhaitable pour ces trois-là, vu leur position centrale.

**Version de travail rendue depuis le modèle.** Sur décision du demandeur, qui
assume le risque de non-conformité, ces trois pièces sont rendues à partir du
modèle documentaire par `case_manager.exhibit_renderers.document`. La
numérotation des paragraphes y est calculée au rendu, comme dans la vue HTML.
Ce rendu porte une mention de provenance en page de garde et **ne remplace pas
l’original** pour la communication.

**b) Les documents propres du demandeur — la génération est légitime.** P-58 à
P-64 sont des `ChatSequence`, courriels ou messages dont le demandeur est
détenteur : la base **est** le dépôt du document technologique, et le rendu PDF
n’est qu’un changement de support. Ce qui est exigé n’est pas une provenance
tierce mais la **documentation de l’intégrité** du transfert — métadonnées,
horodatage, identifiants conservés et procédé de génération reproductible.

`case_manager.exhibit_renderers.chat_sequence` la fournit : transcription
intégrale en ordre chronologique, horodatage et expéditeur (nom + adresse) sur
chaque message, et une **annexe** donnant pour chaque message son identifiant
Google Chat et son horodatage d’origine tels qu’exportés, de sorte que chaque
ligne soit vérifiable contre l’export source. Lorsqu’une séquence ne retient
les propos que d’un seul participant, le rendu le signale — une conversation
amputée de l’autre voix s’expose au reproche de décontextualisation. C’est le
cas de P-58, P-60, P-61 et P-63.

**Aucune altération silencieuse.** Les polices Base-14 du PDF détruisent
« œ » sans avertir. Les rendus vérifient donc chaque caractère par
aller-retour écriture/relecture et basculent au besoin sur une police Unicode
intégrée. Ce qu’aucune police ne rend — un émoji, par exemple — est remplacé
par le marqueur visible `[U+XXXX]`, et la substitution est documentée dans la
pièce elle-même.

Règle de travail : ne jamais générer une pièce à partir du modèle lorsque la
pièce est un acte d’une autre partie, et particulièrement lorsque son contenu
est lui-même contesté.

## 10. Prochaine décision méthodologique attendue

La prochaine décision ne consiste pas à choisir immédiatement le plan définitif
des faits. Elle consiste à déterminer quelles variantes seront expérimentées,
avec quel échantillon représentatif et selon quels critères de comparaison.

Cette expérimentation doit tenir dans le rétroplanning commandé par le
**19 septembre 2026** (§2.1) : gel de l’architecture, puis gel du texte, puis
signification. Une recherche de forme à durée indéterminée est incompatible avec
le délai de l’art. 2892 C.c.Q.

Une bonne expérience initiale peut porter sur un seul bloc — par exemple une
allégation de 2015 — rédigé selon deux ou trois architectures. Le choix final
sera fait après comparaison, puis appliqué au reste de la section.
