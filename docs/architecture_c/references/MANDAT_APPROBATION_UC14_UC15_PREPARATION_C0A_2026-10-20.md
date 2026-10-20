# Agent B — Approbation d'UC-C-14 et UC-C-15 et préparation de l'implantation C0-A

## 1. Décisions du Product Owner

Nous avons examiné les spécifications et les quatre diagrammes UML de chacun des dossiers UC-C-14 et UC-C-15 publiés dans la PR #31.

Nous approuvons expressément les deux conceptions suivantes.

### UC-C-14 — C0A-UML-R2-HIST

**APPROUVÉ UTILISATEUR**, avec les décisions C14-D1 et C14-D2.

Nous approuvons :

- La suppression atomique des occurrences autorisées.
- La conservation des `Statement`, des `VersionTexte` et des informations historiques nécessaires.
- L'absence de purge automatique des contenus dans C0-A.
- Le refus de supprimer un bloc comportant une occurrence protégée ou un contenu qui ne peut pas être archivé fidèlement.
- Le refus global du bloc plutôt qu'une suppression partielle présentant un risque de perte d'information.

Nous acceptons que la suppression des occurrences contenant des citations reste limitée dans ce profil. Cette restriction devra toutefois être réexaminée si elle entrave la rédaction de la demande judiciaire.

### UC-C-15 — C0A-UML-R2-DIAG

**APPROUVÉ UTILISATEUR**, avec la décision C15-D1.

Nous approuvons :

- La conservation de tous les appuis valides d'un couple documentaire, même lorsqu'une autre origine est invalide.
- La production de diagnostics individualisés pour les anomalies locales.
- La distinction entre anomalies locales, erreurs globales et exceptions techniques.
- Le refus de considérer une lecture incomplète comme admissible au mode strict.
- Le maintien cumulatif des contrôles EX01–EX07, dont EX04 enrichi par les diagnostics.

Les résultats de consultation ne constituent pas de nouvelles confirmations et ne modifient pas les décisions historiques.

## 2. Périmètre exact de l'approbation

Les approbations portent exclusivement sur les versions présentées dans la PR #31, au commit `30724df7ec5cbd1aba8ef25d59b5c3a162d20dab`, avec leurs sources PlantUML, rendus, spécifications et manifestes.

UC-C-13::C0A_ISOLER R2-ST demeure approuvé dans sa version antérieure.

Les propositions suivantes restent distinctes et ne sont pas approuvées pour implantation :

- UC02::RENOMMER_CITATION — CIT-D1/D2.
- UC12::DIAGNOSTIQUER_EXAMEN — CIT-D3/D4.
- Le mécanisme permanent de provenance et de propriété L1-A.
- Les autres fonctionnalités non couvertes par les trois profils approuvés.

Nous maintenons la décision de créer les citations `PHRASE` progressivement, selon les besoins. Aucune conversion générale des citations `HERITE` n'est demandée.

## 3. Enregistrement et publication

Tu es mandaté pour :

1. Enregistrer les approbations d'UC-C-14 et UC-C-15 dans le registre et leurs dossiers de validation.
2. Conserver les versions exactes approuvées, leurs sources PlantUML, leurs rendus et leurs empreintes.
3. Maintenir le statut EN_REVUE des sous-cas UC02 et UC12 non approuvés.
4. Vérifier que la PR #31 demeure strictement documentaire.
5. Finaliser puis fusionner la PR #31 dans `main`, après vérification de son contenu et de l'intégrité des versions approuvées.

Aucune modification fonctionnelle des diagrammes approuvés n'est autorisée dans cette opération. Toute modification significative exigerait une nouvelle soumission au Product Owner.

## 4. Préparer le mandat d'implantation pour l'Agent A

Nous souhaitons maintenant accélérer le développement.

Prépare un mandat technique unique et limité à C0-A, fondé directement sur les trois dossiers UML approuvés :

- UC-C-13::C0A_ISOLER — R2-ST.
- UC-C-14 — R2-HIST.
- UC-C-15 — R2-DIAG.

Le mandat doit identifier les écarts à corriger dans le patch conservé, notamment :

- `C0A-ST-01` : suppression de la branche de modification directe des `Statement`.
- `C0A-14-01` : conservation des contenus et restrictions d'archivage.
- `C0A-REV-01` : conservation des appuis valides malgré les anomalies d'autres origines.

L'Agent A devra développer à partir des diagrammes et critères approuvés, et non simplement adapter le patch jusqu'à ce que ses anciens tests réussissent.

Les tests indispensables doivent couvrir les comportements nouveaux, les refus, la conservation historique et l'atomicité.

Le développement et les essais devront d'abord s'effectuer sur une copie Git indépendante et une base PostgreSQL jetable. Aucune intervention sur la base réelle ni sur le serveur de production n'est autorisée.

**Soumets-nous ce mandat avant de demander à l'Agent A de commencer l'implantation.**

## 5. Proportionnalité du processus

Nous réaffirmons que notre objectif principal est la production de la demande judiciaire dans un délai raisonnable.

Nous conservons les quatre vues UML et leur validation, mais nous ne souhaitons pas ajouter de système de traçabilité automatisée entre chaque élément UML et les tests.

Le processus doit rester proportionné :

- Les diagrammes UML approuvés guident le développement.
- Les critères d'acceptation définissent les résultats attendus.
- Les tests vérifient les comportements essentiels.
- Les contradictions architecturales significatives sont renvoyées à l'Agent B.
- Les changements fonctionnels nécessitent notre approbation.

Nous ne voulons pas transformer la gouvernance UML en chantier logiciel autonome.

## 6. Prochaine livraison attendue

Après publication des approbations, transmets-nous :

1. La référence Git contenant les dossiers approuvés.
2. La confirmation que les versions UML approuvées sont préservées.
3. Le mandat technique proposé pour l'Agent A.
4. Les seuls obstacles réellement bloquants au démarrage de C0-A.

Ne lance pas un nouveau cycle général de documentation ou de révision architecturale.

**Notre décision est prise : UC-C-13, UC-C-14 et UC-C-15 sont approuvés dans leurs périmètres respectifs. La priorité est maintenant leur implantation, sous le contrôle des modèles UML validés.**