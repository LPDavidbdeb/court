# Mandat — Approbation de la conception UC14 R3-CONC et préparation de sa vérification

**Source : message explicite de l'utilisateur, reçu le 23 octobre 2026.**
Le texte du mandat est conservé ci-dessous. La décision courante est portée
par le [registre officiel](../registre_validation.md); l'enregistrement de
ce mandat ne modifie aucun fichier du dossier R3-CONC approuvé.

## 1. Décision de l'utilisateur

J'approuve formellement la conception **UC14 R3-CONC**, telle que publiée dans le dépôt :

- Branche : `docs/uc14-r3-conc-20261023`
- Commit : `b0adf1136c55c38a830d3a1cd1a4332741bf297d`
- Dossier : `docs/architecture_c/use_cases/UC-C-14/revisions/R3-CONC/`

Cette approbation fait suite au verdict `VALIDE_ARCHITECTURE` documenté dans `validation.md` et `revue_B.md`.

Elle autorise uniquement une correction applicative isolée conforme à la conception R3-CONC, dans les cinq fichiers explicitement mentionnés dans `analyse_coherence.md`, section 6.

Elle n'autorise ni intégration, ni fusion, ni migration, ni déploiement.

## 2. Enregistrer l'approbation

Mettre à jour le registre officiel :

`docs/architecture_c/registre_validation.md`

Enregistrer :

- L'identifiant `UC14 R3-CONC`.
- Le commit documentaire approuvé.
- La date d'approbation.
- Le statut `APPROUVE_UTILISATEUR`.
- Le périmètre exact de l'autorisation corrective.
- La persistance du blocage d'intégration C0-A.
- L'absence de résultats applicatifs R3-CONC à cette étape.

Conserver intégralement les versions UML R2 antérieurement approuvées, leurs empreintes et leurs historiques.

Ne pas modifier le contenu des diagrammes R3-CONC approuvés.

Si une correction documentaire devient indispensable, créer une révision distincte et en expliquer la nécessité.

## 3. Préparer la vérification de conformité

À partir des documents R3-CONC existants, préparer une grille de revue applicable à tout candidat correctif présenté ultérieurement.

La grille doit être directement fondée sur :

- `specification.md`
- `analyse_coherence.md`
- `plan_tests.md`
- `tracabilite.md`
- Les sept diagrammes PlantUML.
- Le rapport `REVUE_INDEPENDANTE_B01.md`.

Elle doit permettre de vérifier :

1. La fidélité de l'implantation aux diagrammes.
2. L'acquisition réelle et la durée des verrous.
3. Le contrôle exact de l'état avant suppression.
4. La fidélité des archives produites.
5. Les opérations concurrentes d'édition HTTP et de sauvegarde ORM.
6. L'absence de réinsertion après suppression.
7. L'atomicité et les rollbacks.
8. La protection des parents Treebeard.
9. Les tests discriminants sur l'ancienne et la nouvelle version.
10. La non-régression UC13, UC14 et UC15.

Distinguer strictement les exigences définies, les garanties démontrées par des tests et les garanties non encore vérifiées.

## 4. Règles pour la future revue applicative

Lorsqu'un candidat correctif identifié sera soumis à examen, sa conformité devra être évaluée indépendamment à partir du code, des résultats exécutés et des contrats R3-CONC approuvés.

La réussite de la suite générale ne pourra pas remplacer les contre-épreuves ciblées.

Les résultats devront établir notamment :

- Que l'ancien candidat échoue aux contre-épreuves discriminantes.
- Que le candidat corrigé les réussit.
- Que les résultats ne proviennent pas de timeouts artificiels.
- Que les archives correspondent aux états effectivement supprimés.
- Que les refus et annulations sont atomiques.
- Que le périmètre autorisé est respecté.

Aucune conclusion de conformité applicative ne doit être prononcée avant l'examen d'un candidat et de résultats réels.

Si aucun candidat corrigé n'est actuellement disponible, préparer uniquement le protocole de revue et conserver le statut « vérification applicative en attente ».

## 5. Réserve maintenue

Le problème d'orphelin tardif, déjà identifié dans les revues C0-A, demeure distinct de la correction R3-CONC.

Ne pas présenter ce problème comme corrigé ou testé.

Ne pas élargir la portée d'UC14 à la voie d'ajout UC02.

## 6. Livrables du présent mandat

Produire :

1. Le registre de validation actualisé.
2. Une attestation de l'approbation utilisateur et de sa portée.
3. Une grille de contrôle de conformité des futures implantations.
4. Une vérification de l'intégrité des versions de conception approuvées.
5. Un bref rapport distinguant clairement les éléments approuvés, les éléments encore non exécutés et les autorisations restant interdites.

Ne modifier aucun code applicatif ni la base de données réelle.

**Résultat attendu :** la conception R3-CONC est officiellement approuvée, le périmètre d'implantation est délimité et les conditions de validation du futur candidat sont définies, sans déclarer prématurément C0-A conforme.
