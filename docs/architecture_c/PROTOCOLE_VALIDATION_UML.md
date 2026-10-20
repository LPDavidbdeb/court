# Protocole de validation UML préalable à l’implantation

**C-UML-2026-10-20-R1 — Livrable D.**

Exigence opposable issue du [mandat utilisateur, §§4–8](references/MANDAT_CONSOLIDATION_UML_2026-10-20.md). Ce document formalise son application; les détails des dossiers seront soumis à l’utilisateur. **Aucun use case n’est autorisé à être implanté par la seule adoption de ce protocole.**

## 1. Deux unités complémentaires

Le **use case** est l’unité de conception et d’approbation fonctionnelle. Le **lot** reste l’unité de mandat, d’exécution et d’intégration selon [PROCESSUS_CHANGEMENT](../PROCESSUS_CHANGEMENT.md).

Avant la première écriture applicative d’un lot : chaque use case touché possède un dossier approuvé, ses dépendances du périmètre autorisé sont satisfaites, et un mandat écrit du lot fixe le SHA, les fichiers modifiables, les données d’essai, les interdictions et les acceptations. Si un changement affecte un autre use case, son impact est réexaminé avant de poursuivre.

Un service partagé ne sert pas à contourner cette règle. Ses comportements doivent appartenir à un ou plusieurs use cases approuvés. Une livraison partielle doit nommer un sous-cas avec ses propres critères et quatre vues; elle n’hérite pas de l’approbation d’un cas plus large. Les cas séparés 01A/01B, 05E/05P et 18A/18B évitent les dépendances circulaires entre fondations, appuis, préparation, gel et restitution.

## 2. Dossier versionné obligatoire

Emplacement : `docs/architecture_c/use_cases/<UC-ID>/`. Le [gabarit](use_cases/MODELE_DOSSIER.md) définit le contenu attendu :

```text
specification.md
activity.puml        activity.svg
sequence.puml       sequence.svg
erd.puml            erd.svg
class.puml          class.svg
tracabilite.md
validation.md
```

Une séquence complexe peut ajouter `sequence_panne.puml`, `sequence_concurrence.puml`, etc., chacune compilée et rendue. Les PNG restent utiles selon le processus du dépôt; le SVG est obligatoire pour chaque vue contractuelle. Les quatre fichiers racines sont identifiables dans le dossier même s’ils incluent des fragments locaux partagés. Une inclusion vers la vue globale entière ne remplace pas la vue contextualisée.

Chaque dossier porte version, date, SHA du socle observé, version des contrats et du modèle global cible, dépendances, auteur, réviseur, périmètre synthétique/réel et liste des questions ouvertes. Les sources/rendus et leurs empreintes identifient exactement la version examinée. Une référence à « dernière version » ne permet pas d’approuver un contenu mobile.

## 3. Contenu contractuel des quatre vues

| Vue | Minimum à vérifier |
|---|---|
| Activité | Déclencheur, préconditions, acteurs et responsabilités, chemin nominal, variantes, vérifications, refus, erreurs, annulation, résultats et postconditions |
| Séquence | Interfaces, services/composants, agrégats, lectures/écritures, appels et réponses, validations, frontières de transaction, verrous, stockage si concerné, erreurs et retour à un état cohérent |
| ERD | Entités réellement persistantes, IDs, attributs nécessaires, relations/cardinalités, unicité/intégrité, suppression, versionnement et immutabilité; existant/proposé/à modifier distingués |
| Classes | Responsabilités et invariants, attributs utiles, opérations, interfaces, modèles Django, services de lecture/métier, rendus, stockage, dépendances et héritage/composition justifiés; pas une copie de l’ERD |

Les noms proposés ne sont pas présentés comme des classes existantes. Un module de fonctions reste un module ou composant explicitement stéréotypé, pas une classe Python fictivement constatée. Un concept de composition ne devient pas une table sans nécessité de persistance autonome démontrée.

L’ERD cible local doit correspondre à une version du modèle global cible. Le relevé ORM P6 documente l’existant; il ne remplace pas cet ERD cible. Un modèle global consolidé peut circonscrire une première version validée à C0-A/fondations et signaler les zones futures non arbitrées. Les lacunes ne peuvent toucher les données ou contraintes du use case déclaré valide.

Les diagrammes d’états sont un **complément** recommandé pour les cycles de vie, pas un substitut à l’une des quatre vues. Préparation/gel et événements de communication/dépôt doivent rester distingués.

## 4. Contrôle technique T

Pour **chaque** source, le registre de validation indique : chemin, empreinte, version PlantUML, commande exacte, date, code de sortie, rendu et contrôle visuel.

1. Compiler la syntaxe et générer le SVG, avec les inclusions locales versionnées.
2. Ouvrir le rendu : vérifier textes, caractères, taille lisible, absence de troncature, collisions gênantes et chemins d’erreur visibles.
3. Contrôler les liens, inclusions et références vers les autres vues et le modèle global.
4. Corriger puis régénérer les vues touchées. Une ancienne image sans source correspondante n’est pas une preuve.

Exemple de commandes depuis le dossier, à adapter au périmètre réellement présent :

```sh
plantuml -charset UTF-8 -checkonly '*.puml'
plantuml -charset UTF-8 -tsvg '*.puml'
```

Une compilation réussie vaut seulement contrôle T. Elle ne démontre ni l’exigence, ni la cohérence architecturale, ni un test applicatif. Une vue illisible ou non compilable n’est jamais techniquement validée.

## 5. Contrôle fonctionnel F

Chaque critère d’acceptation possède un identifiant local stable et une ligne dans `tracabilite.md` :

**Exigence → critère → éléments précis des quatre vues → scénario → résultat attendu.**

Les éléments sont identifiés dans les sources : par exemple `AC02`, `ACT-refus-source-gelee`, message `SEQ-07`, relation `ERD-version-piece`, invariant `CLS-fraicheur`. Une simple mention du nom de fichier ou du use case n’établit pas une couverture.

Chaque critère doit pointer vers les vues pertinentes; si une vue ne porte pas de donnée nouvelle pour ce critère, la justification est écrite. Le dossier reste composé de quatre vues. Les préconditions, refus et postconditions des vues doivent correspondre aux critères approuvés, sans élargissement silencieux.

Les scénarios existants gardent leurs espaces de noms : `E01:Txx`, `C:Txx`, `C:Nxx`, `VFxx`, `NRxx`, `CF3-xx`, `IMxx`, `TRxx`, `EPIC-V2:Txx`. Un nouveau scénario reçoit un ID distinct. Un scénario non exécuté est marqué **NON EXECUTE**, même s’il est couvert par une conception.

Des contre-épreuves sont obligatoires pour autorisation/refus, suppression, mutation historique, concurrence, opération irréversible et promesse d’annulation. Elles décrivent aussi ce qui doit rester inchangé après le refus.

## 6. Contrôle architectural A

La revue B vérifie au minimum :

| Contrôle | Vérification croisée |
|---|---|
| A1 | Chaque activité exigeant une interaction possède une séquence réalisable |
| A2 | Chaque message métier a un responsable et une opération dans la vue de classes/composants |
| A3 | Chaque donnée persistée ou lue correspond à une entité/attribut de l’ERD, sans table implicite |
| A4 | Les séquences respectent les contraintes d’appartenance, unicité, suppression, fraîcheur et immutabilité de l’ERD |
| A5 | Les autorités rédaction, appui, filiation, composition, cotation et rendu ne sont pas dupliquées |
| A6 | Préparation, état figé et événements restent cohérents; les écritures SQL et stockage ont des frontières réalistes |
| A7 | D05 et les invariants C/CF, notamment source, sélection, occurrence réelle, archives et HERITE/PHRASE, sont respectés |
| A8 | Les autres use cases et contrats de services restent compatibles; les effets sur les refus et données historiques sont analysés |

Toute contradiction possède une entrée : description, sources, impact, responsable de résolution et preuve de correction. Une question bloquante du périmètre empêche le statut `VALIDE_ARCHITECTURE`. Un avis B peut constater les parties conformes et la réserve restante sans valider le dossier entier.

## 7. États et preuves de décision

`A_MODElISER` du mandat est normalisé **`A_MODELISER`** : même état, casse harmonisée.

| Statut | Conditions d’entrée / sortie |
|---|---|
| `A_SPECIFIER` | Critères, contrats, périmètre ou arbitrages incomplets; définir ou décider avant modélisation finale |
| `A_MODELISER` | Périmètre spécifiable et critères identifiés; au moins une vue requise manque ou doit être revue |
| `EN_REVUE` | Quatre vues du périmètre présentes et dossier de preuve proposé; revue T/F/A et scénarios en cours |
| `CORRECTIONS_REQUISES` | Lacune ou contradiction constatée en revue; révision et recontrôles affectés nécessaires |
| `VALIDE_ARCHITECTURE` | T/F/A et traçabilité réussis, aucune question bloquante du périmètre; attestation B datée et versionnée |
| `APPROUVE_UTILISATEUR` | Décision explicite de l’utilisateur sur cette version précise, avec date, référence et réserves; aucune auto-approbation par B |
| `PRET_DEVELOPPEMENT` | Approbation conservée, dépendances livrées selon le périmètre, conditions d’essai et mandat du lot autorisés; contrôles d’intégration applicables satisfaits |

Une approbation de principe de D05 ou d’un contrat n’est pas l’approbation de tous les dossiers qui l’utilisent. La validation de B n’est pas une autorisation de code. Un refus/suspension utilisateur est consigné comme décision avec motif; aucune transition vers développement n’en résulte. Aucun délai écoulé ne vaut approbation.

Les dépendances sont distinguées : contrat nécessaire à la conception; structure/API nécessaire au développement; source/capacité réelle nécessaire à l’activation. Une autorisation sur doubles ou données synthétiques doit être explicite et bornée. Elle ne permet pas de déclarer le chemin réel disponible. Un lot non atterri bloque le suivant selon le processus; la conception documentaire peut se poursuivre.

Le [registre de validation](registre_validation.md) est l’index courant des statuts. Chaque ligne renvoie au dossier/version et à sa preuve B/utilisateur. L’historique des décisions reste dans `validation.md`; les anciens éléments ne sont pas effacés lors d’une correction.

## 8. Analyse d’impact et revalidation

Tout changement du comportement, des critères, des données, des séquences, des responsabilités ou d’une décision approuvée ouvre une analyse d’impact :

1. Identifier dossiers, vues, scénarios, lots et contrats de fournisseurs affectés.
2. Versionner la révision; conserver l’état approuvé et ses empreintes dans Git ou dans une archive explicitement historique si aucun commit ne le conserve encore.
3. Refaire les contrôles T/F/A et la traçabilité affectés; élargir aux autres cas dépendants si l’invariant partagé change.
4. Revenir à `A_SPECIFIER` ou `CORRECTIONS_REQUISES` selon la cause; ne pas conserver un statut prêt pour une nouvelle version non examinée.
5. Obtenir une nouvelle décision utilisateur pour tout contrat ou périmètre d’implantation modifié. Une simple régénération identique des images n’invente pas une nouvelle décision fonctionnelle.

Un constat de divergence du code pendant le développement suit cette même procédure. L’Agent A suspend le changement dépendant, documente la divergence et sollicite une correction ou une évolution de conception; il ne tranche pas une ambiguïté par le seul code.

## 9. Passage à l’Agent A et conformité après développement

Séquence obligatoire : spécification → quatre vues → validation B → approbation utilisateur → contrôle des préalables/mandat de lot → implantation isolée → revue de conformité → intégration mandatée.

Le mandat d’implémentation remis à A référence les versions approuvées, fichiers permis, interdictions, SHA, environnement jetable, tests et modalités de livraison. Sa préparation opérationnelle n’est engagée qu’après approbation des dossiers concernés. Le présent travail définit le gabarit et le plan; il n’émet pas ce mandat.

Après développement : comparer routes et services réellement actifs aux séquences, comportements aux activités, schéma/migrations aux ERD, responsabilités aux classes et tests aux critères. Fournir diff et preuves d’exécution sur environnement identifié. Un succès isolé ne prouve pas le déploiement.

Le lot n’est « fait » qu’après les six conditions d’atterrissage du processus : rapport dans le dépôt, tests sur le socle principal autorisé et sa base de test, fusion intégration puis main, ERD observé actualisé si schéma modifié, limites réaffectées et journal à jour. Aucune commande de ces étapes n’est autorisée par le protocole seul.

## 10. Situation de la présente livraison

**Constat historique de la consolidation initiale C-UML-R1.** La revue
ultérieure C0A-UML-R1 valide B le seul dossier 13 et prépare 14/15 en revue;
aucune approbation utilisateur ou autorisation de développement n’en résulte.
Les états courants font autorité dans le [registre](registre_validation.md);
les règles du présent protocole sont inchangées.

Cette intervention fournit l’impact, l’avenant, la couverture, le plan et le contrôle obligatoire. **Elle ne produit ni ne valide les quatre vues cibles de tous les use cases.** Les activités préexistantes sont des bases; les ERD/classes P6 sont des références observées. Le registre ne contient donc encore aucun `VALIDE_ARCHITECTURE`, `APPROUVE_UTILISATEUR` ou `PRET_DEVELOPPEMENT` au titre de ce protocole.


**Actualisation documentaire ST-R1 :** l’attestation UC13 R1 précitée est
historique; la nouvelle validation C0A-UML-R2-ST porte seulement sur le sous-cas
C0A_ISOLER. La propriété globale et le chemin privé direct restent à traiter.
Voir le [registre courant](registre_validation.md) et l’[analyse ST-R1](INVARIANTS_STATEMENT_REPRODUCED_PRODUCED.md).
Les règles du protocole ne changent pas; aucune approbation utilisateur ajoutée.
