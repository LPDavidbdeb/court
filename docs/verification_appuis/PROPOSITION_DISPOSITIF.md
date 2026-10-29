# Relations entre les paragraphes et les pièces de la demande déposée — proposition de dispositif

> **Statut : proposition révisée, 29 oct. 2026, à examiner par LP.** Elle
> intègre la précision de LP : obtenir une image du dépôt, examiner les pièces
> une à une, puis relire l'ensemble. La décision de **persister en base**
> (option B) est conservée. Cette révision ne vaut ni spécification approuvée
> ni mandat de lot. L'état des sources et la décision initiale sont consignés
> dans le [plan préparatoire](../../legal/amendements/01_avant_notification/plan_verification_appuis.md).
> Le présent document porte la proposition de dispositif mise à jour.

## 1. L'objectif

**Produire une image durable, vérifiable et révisable des relations entre les
paragraphes de la demande déposée le 24 juillet 2026 et les pièces qui leur
sont associées dans cet acte.**

La question gouvernante est :

> Existe-t-il une relation entre ce paragraphe, tel qu'il a été déposé, et
> cette pièce qui lui est associée ? Quel passage ou élément permet de la
> constater, et quelle est la portée de cette relation ?

L'examen part du texte et des références effectivement présents au dépôt.
Lorsqu'un paragraphe rapporte une déclaration, on observe si elle a été faite,
par qui et dans quels termes. La vérité objective de ce qu'affirme cette
déclaration demeure une question distincte de cet examen documentaire.

**Hypothèse de travail : une pièce citée peut avoir une contribution propre et
repérable, même si elle ne porte pas seule tout le sens de la démonstration.**
L'examen cherche cette contribution sans la présumer acquise. Une relation
limitée à une date, une déclaration, un échange ou un élément de contexte est
consignée avec cette portée.

L'appréciation cumulative vient **après** la réunion et l'examen individuel de
l'ensemble des pièces du périmètre annoncé (§ 5).

## 2. Trois couches, deux temps de lecture

```text
CONSTAT DU DÉPÔT — référence historique préservée
  document 9 : représentation en base, 287 énoncés recensés
  BordereauDepotJuillet : 268 lignes cotées recensées
  AppuiDepotJuillet : 515 liens « ce paragraphe cite cette pièce »
        │
        ▼
OBSERVATIONS INDIVIDUELLES — nouvelles, proposées puis validées
  paragraphe × pièce déjà associée
  élément observé + localisation + relation repérée + portée et limites
        │
        ▼  après examen de l'ensemble
RELECTURE GLOBALE — nouvelle, proposée puis validée
  articulation des contributions documentées et contexte plus large
```

Ces nombres sont ceux du relevé du 29 octobre. Leur ancrage reste à réaliser
en phase 0. Le document 9 est un instrument de travail contrôlé contre la
source d'impression identifiée. **L'acte déposé est le papier remis au greffe.**

Le constat conserve ses paragraphes, ses références et ses cotes. Les couches
nouvelles s'y rattachent sans modifier les liens existants ni en ajouter au
nom de ce qui aurait dû être cité. Les ajouts postérieurs au dépôt, notamment
les lignes sans cote de juillet, restent hors de cet inventaire historique.

## 3. L'unité d'examen et la grille proposée

**L'unité principale est le couple paragraphe déposé × pièce associée**, porté
par `AppuiDepotJuillet`. Chaque lien existant doit recevoir un examen explicite.
La forme du renvoi est conservée : sous-cote nommée ou membre d'une liasse
citée dans son ensemble.

Un paragraphe peut contenir plusieurs propositions. Des extraits littéraux
peuvent préciser la portion à laquelle une pièce se rapporte. Le paragraphe
complet reste visible, avec son numéro imprimé, ses attributions et ses
réserves. Le découpage sert à localiser la relation ; il ne remplace pas le
paragraphe et n'impose pas un verdict pour chaque combinaison fragment–pièce.

Les anciens libellés « appuie / en partie / n'appuie pas / contredit » sont
remplacés, dans cette proposition, par une grille de **relation documentaire** :

| Résultat proposé | Sens |
|---|---|
| **Relation repérée** | Un ou plusieurs éléments de la pièce se rapportent au paragraphe. Les éléments concernés, la nature de la relation et sa portée sont décrits. |
| **Aucune relation repérée** | L'examen effectué n'a pas permis d'identifier de relation. Le périmètre lu et la raison sont consignés. |
| **Indéterminé** | La lecture ou l'identification disponible ne permet pas encore de se prononcer. L'obstacle et le travail restant sont consignés. |

Une relation peut porter, par exemple, sur une déclaration, une date, une
identité, un échange, un contenu visuel ou un élément de contexte. Plusieurs
natures peuvent coexister. La description doit expliquer le rapport avec le
texte précis du paragraphe ; une simple proximité de thème ne suffit pas à
tenir lieu d'explication.

Une différence de date, de citation ou d'attribution entre les deux textes est
relevée précisément, même si une relation est repérée. Cette observation ne
devient pas automatiquement une conclusion sur la vérité du fait.

Le **résultat** reste distinct de l'**avancement** : non examiné, proposé,
validé ou rejeté. Un élément non examiné n'a pas de résultat. Un paragraphe
sans pièce citée est signalé à l'inventaire, sans lui inventer un lien ni une
observation « aucune relation repérée ».

## 4. Les informations à conserver

La persistance en base reste la destination. Le nombre de modèles, leurs noms
et leurs cardinalités seront fixés dans la spécification et les vues UML.
Les informations attendues sont les suivantes :

| Ensemble | Informations nécessaires |
|---|---|
| **Ancrage du constat** | Texte conservé, identifiants des paragraphes et de leurs occurrences, ordre, numéros imprimés, liens existants, cotes et identités des sources ; empreintes et provenance de l'instantané. |
| **Fragments de lecture, lorsqu'utilisés** | Identifiant stable, extrait littéral et bornes dans le texte conservé, contexte, auteur et validation du découpage ; historique des révisions. |
| **Observation individuelle** | Lien exact `AppuiDepotJuillet`, paragraphe ou fragments visés, résultat, élément observé, localisation, nature de la relation, portée, limites ou différences constatées, périmètre examiné. |
| **Support examiné** | Identité du fichier ou des fichiers, empreintes, qualification du support et méthode de lecture. Pour une pièce composée, manifeste ordonné des fichiers effectivement examinés. |
| **Validation et historique** | Auteur et date de proposition, auteur et date de validation ou de rejet, motif, référence à l'observation remplacée ; conservation des versions antérieures. |
| **Relecture globale** | Périmètre exact, pièces réunies, versions des observations utilisées, articulation proposée, limites, auteur, date, validation et historique. |

Pour un texte, l'élément observé est un passage reproduit au mot et localisé
dans la pièce. Pour une photographie, il est une description de ce qui est
visible, localisée dans le fichier, avec les métadonnées utiles. La
qualification du support est conservée, notamment lorsqu'il s'agit d'un dérivé
en base. Pour « aucune relation repérée », le relevé du périmètre examiné et la
motivation remplacent le passage inexistant.

Les observations validées et les découpages qui les fondent sont conservés
sans écrasement. Une correction crée une nouvelle version. Un remplacement
proposé n'écarte pas la dernière observation validée encore applicable ; il
reste signalé comme en attente. Un changement de texte, de fragment, de lien
ou de support rend les observations concernées à revoir, avec leur histoire
intacte. Les garanties de conservation devront être spécifiées et éprouvées
dans le lot ; le champ `remplace` et les empreintes ne les réalisent pas seuls.

## 5. Le fonctionnement

### Premier temps — examen individuel, par séries de travail

1. **Ancrer et contrôler.** Conserver l'instantané du constat hors de l'archive
   gelée de juillet. Avant chaque série, contrôler textes, ordre, numéros,
   liens et sources contre cet instantané. Un écart est signalé et résolu
   explicitement avant de poursuivre les examens concernés.
2. **Présenter le paragraphe et toutes ses références.** Employer le numéro
   imprimé. Identifier les fragments utiles en conservant le contexte ; LP
   valide les découpages utilisés.
3. **Lire chaque pièce séparément.** Lire le support source approprié :
   `.eml`, scan, fichier ou données source documentées. Les fiches
   `piece_*.md` et les transcriptions dérivées servent à se repérer. Pour les
   actes adverses P-19, P-40 et P-42, le libellé est vérifié sur le scan.
4. **Proposer l'observation.** Consigner ce qui est observé, où, la relation
   avec le paragraphe et sa portée propre. La pièce n'a pas à porter seule
   toute la démonstration pour que sa contribution soit relevée.
5. **Valider et enregistrer.** LP valide, corrige ou rejette. Les résultats
   retenus sont validés ; les examens manquants, en attente, rejetés ou devenus
   périmés restent visibles dans l'avancement.

Ordre proposé : paragraphes sur la prescription (§ 234-236), puis ceux qui
invoquent P-19, P-40 et P-42, puis le préjudice (§ 200-217), puis le reste dans
l'ordre de l'acte. Les séries de lecture sont distinctes des lots de
changement du système.

### Second temps — relecture globale

Le périmètre de la relecture est annoncé avant sa préparation. Pour la
synthèse de l'image du dépôt, il comprend **l'ensemble des pièces associées
aux paragraphes de la demande**. Toutes doivent être réunies, examinées
individuellement et leurs observations validées et encore applicables avant
de conclure cette appréciation cumulative. Les paragraphes sans référence
restent visibles dans l'image complète de l'acte.

La relecture permet alors d'apprécier comment les contributions se complètent,
se répondent ou présentent des différences, dans leur contexte plus large.
Elle cite les observations et les passages utilisés ; elle conserve la
distinction entre constat individuel et interprétation d'ensemble. LP la
valide séparément. Une modification d'une observation utilisée impose de
revoir la synthèse concernée.

Une pièce manquante ou un examen indéterminé est un reste à traiter, et non
une absence de relation acquise. Une série achevée ou un pilote ne vaut pas
relecture globale de l'ensemble du dépôt.

## 6. Les quatre rapports

| Rapport | Contenu |
|---|---|
| **Image du dépôt, paragraphe par paragraphe** | Texte et numéro imprimé, références telles que citées, éléments observés dans chaque pièce, relations documentaires et portée, validations et limites. Export possible des mêmes données. |
| **Couverture et travail restant** | Tous les liens attendus, leur avancement, les résultats validés, les supports manquants ou illisibles, les révisions en attente et les paragraphes sans référence. Les dénominateurs restent visibles. |
| **Relecture globale** | Périmètre, état de réunion et d'examen des pièces, puis appréciation cumulative lorsqu'elle peut être réalisée. Avant ce seuil, le rapport indique ce qui reste à examiner. |
| **Dérive et historique** | Écarts au constat ancré, supports modifiés ou indisponibles, observations et synthèses à revoir, versions remplacées et motifs des révisions. |

Les premiers rapports sont régénérables pendant les passes. Le rapport global
ne présente une synthèse validée qu'après le second temps du § 5. Chaque
rapport distingue résultats courants, historique et éléments en attente.

## 7. Le plan de réalisation

| Phase | Contenu | Condition |
|---|---|---|
| **0 — ancrage et premiers examens, hors modification de l'application** | Conserver l'instantané du constat ; dresser la liste de travail ; définir un fichier d'attente au format versionné ; commencer les observations individuelles, notamment sur les paragraphes de prescription. Un pilote vérifie que la grille décrit aussi une contribution limitée ou contextuelle. | Sources identifiées et ancrées avant de retenir les observations. Le fichier d'attente anticipe l'import sans prétendre figer le schéma des futures tables. |
| **1 — le lot de persistance** | Proposition → spécification → quatre vues UML par use case touché (activité, séquence, ERD cible, classes) → revue B → approbation de LP de la version précise → mandat écrit → implémentation et tests en copie isolée → intégration selon les six conditions du processus ; import contrôlé du fichier d'attente dans le périmètre autorisé. | Implantation après C0-A atterri, sauf dérogation expresse de LP. La conception documentaire peut avancer. Le schéma couvre les observations, leur validation, leur histoire et la relecture globale. |
| **2 — les passes individuelles** | Examiner tous les liens paragraphe–pièce, par séries, et faire valider les observations. Suivre l'exhaustivité et les restes à traiter. | Dès la phase 0 dans le fichier d'attente ; dans la base après livraison autorisée. L'import conserve les auteurs, dates et validations réellement obtenues, sans doublons ni validation inventée. |
| **3 — la relecture globale et l'image complète** | Après réunion et examen de l'ensemble, proposer puis faire valider l'appréciation du contexte plus large ; produire l'image complète du dépôt et son export. | Ensemble des pièces du périmètre réuni, observations individuelles validées et courantes ; aucun manque absorbé silencieusement dans la synthèse. |

**Échéance de travail :** rendre ces résultats disponibles avant la rédaction
finale de la demande modifiée, dont la cible proposée est le **1er février
2027**. Son statut procédural et les autres dates se lisent dans
l'[échéancier](../../legal/instance/echeancier.md). Cet exercice ne conditionne
pas la communication des pièces prévue le **6 novembre 2026**.

## 8. Portée des résultats et règles de conservation

Le livrable de ce dispositif est **l'image expliquée du dépôt existant**.
Ses résultats pourront ensuite éclairer la préparation de la demande modifiée,
les interrogatoires et la concordance avec une autre version. Les décisions
de réécriture, de scission, d'ajout ou de retrait relèvent d'un travail
ultérieur, tracé séparément.

Dans cet exercice :

- le document 9, les associations du bordereau de juillet et les liens
  existants restent préservés ; aucune nouvelle référence ne leur est ajoutée
  au titre du dépôt initial ;
- l'archive `legal/depots/2026-07-24_initial/` reste en lecture seule ;
- chaque cote conserve son identité historique, y compris lorsqu'une pièce
  est retirée d'une version ultérieure ;
- une relation limitée est décrite avec sa contribution propre ; elle n'est
  pas assimilée à une absence de relation faute de porter toute la démonstration ;
- constater une déclaration conserve son auteur et ses termes, sans adopter
  automatiquement comme vrais les faits qu'elle rapporte ;
- les observations individuelles restent distinctes de la relecture globale,
  et les propositions distinctes des validations ;
- les empreintes sont accompagnées des textes et supports conservés ou de
  leurs références de conservation vérifiables ; les versions examinées et
  l'historique restent accessibles.
