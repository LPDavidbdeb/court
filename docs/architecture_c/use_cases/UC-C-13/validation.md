# UC-C-13 — Validation documentaire du sous-cas C0A_ISOLER

**C0A-UML-R2-ST — 20 octobre 2026.** Conception et revue documentaire : B.
Socle lu : `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`.
Modèle global : G-C0A-R2-ST. [Périmètre exact](specification.md),
[traçabilité](tracabilite.md), [invariants métier et analyse](../../INVARIANTS_STATEMENT_REPRODUCED_PRODUCED.md).
L’attestation R1 est conservée dans [l’archive](../../historique/2026-10-20_avant_invariants_statement_R2/corpus/use_cases/UC-C-13/validation.md)
et **ne vaut pas validation de cette révision**.

## 1. Contrôle technique T

PlantUML 1.2026.8 / 149874a, Graphviz 12.2.1. Commande exécutée, code **0** :

```sh
plantuml -charset UTF-8 -tsvg docs/architecture_c/use_cases/UC-C-13/*.puml docs/architecture_c/modele_global/*.puml
```

Après deux corrections de libellés, recompilation de `UC-C-13/class.puml` et
`modele_global/classes_consolidees.puml`, code 0. Les six SVG ont été rendus
avec `rsvg-convert --background-color=white -o <nom>.png <nom>.svg`, code 0.
B a ouvert les six PNG et contrôlé lisibilité, accents, branches de refus,
absence de collision et de troncature; les deux classes ont été réinspectées
après correction. Les SVG permettent le zoom sur les ERD/classes larges.
Les huit vues locales 14/15 sont inchangées : leur contrôle T R1 n’est pas
présenté comme une nouvelle exécution.

| Vue locale | Résultat | SHA-256 source | SHA-256 SVG |
|---|---|---|---|
| [activity](activity.svg) | Compilation 0, PNG inspecté B | `8221478dad8f8d36afff843d26490bd8c2c22d3841de05ca6a41627c91743076` | `20585577762e97b6acf64974ff503fd26ebcf40c8e6c828b63aad7a3286cc2a1` |
| [sequence](sequence.svg) | Compilation 0, PNG inspecté B | `918433483a3f5bafb5b65a9f586c07762ae89e3aea787eebe0b83f4c921d7645` | `354f2d285dfc4f2301ef4df3a25eeb4eb1167a635d23f8e4a341d6339c758e3c` |
| [erd](erd.svg) | Compilation 0, PNG inspecté B | `8ee1901c2e6778ba9ae1b7c4db95c9a5dfc838937e295bca7499b9b8e49b4309` | `2d96221198feee36fc17a9082181bf91fbfc600a580c18cbab09b91144d22880` |
| [class](class.svg) | Compilation 0, PNG inspecté B | `92e5c59a0ed1e835b179bd8dc9fab67d5563e251895996c5fc119f0871052bad` | `8688981d79a69249811f2f7aca54c07c1357c6217e6033ce827e2de5528a5c79` |

Sources/rendus/style et documents contractuels sont identifiés dans le
[manifeste](manifest_sha256.json). Les [preuves communes](../../lots/C0-A/VALIDATION_UML_C0A.json)
distinguent compilation actuelle et contrôles historiques. Les inclusions
sont locales; aucune source distante n’a été chargée.

## 2. Contrôle fonctionnel F

- AC02 décrit le détachement de l’origine REPRODUCED; AC03 définit les
  conditions du chemin direct futur et son absence d’activation dans ce profil.
- La comparaison littérale R1/R2 confirme que les six autres critères restent
  identiques. Le texte identique et `item` seul ne créent pas de Statement.
- Le sous-cas a ses quatre vues, critères et scénarios propres. Les éléments
  ACT / SEQ / ERD / CLS sont reliés dans la traçabilité; ST:T01–ST:T12 indiquent
  résultats attendus, lots et **NON EXECUTE** pour tous les essais applicatifs.
- ST04 global, provenance durable, édition directe d’un privé attesté et
  fraîcheur du contexte sémantique de `item` sont des suites explicites; ils
  ne sont pas donnés comme des garanties du sous-cas C0A_ISOLER.

Aucun test Django, HTTP, SQL ou de concurrence PostgreSQL n’est exécuté dans
ce mandat. Les 209 succès historiques P6 restent des résultats historiques.
L’entrelacement T1/T2 est une démonstration par lecture des chemins existants,
pas un résultat expérimental. Aucune base réelle n’a été consultée ou modifiée.

## 3. Revue architecturale A1–A8 renouvelée

| Contrôle | Résultat documentaire et limite |
|---|---|
| A1 | Activité et séquence concordent : refus REPRODUCED/référent, texte égal, premier texte, copie neuve sur différence, rollback. Aucune branche privée en place dans le profil. |
| A2 | Vue HTTP et module concordance portent mutation/captures; protection contrôle la mutabilité; les modèles de décision calculent la fraîcheur. Les modules sont distingués des modèles Django. |
| A3 | Schéma actuel inchangé, GFK typée et captures présentes dans ERD. Les deux métadonnées d’origine/propriétaire sont notées comme proposition L1-A absente, pas comme champs livrés. |
| A4 | Ne pas écrire l’ancien Statement préserve les autres usages même si un rattachement interdit survient. Les gardes de captures utiles restent applicatives; aucune fermeture universelle bulk/SQL n’est prétendue. |
| A5 | Copie de texte et partage d’identité distincts; filiation E01 ne donne pas droit à partager un privé. Anciennes décisions conservées, pas de reconfirmation ni de provenance reconstruite. |
| A6 | Captures/objet neuf/repointage/item dans une seule opération atomique; échec tardif annule l’ensemble. Aucun fichier ou gel de version ajouté. Les éditions concurrentes d’une même occurrence ne sont pas sérialisées par ce profil. |
| A7 | ST01–ST05 guident la cible; protections historiques prioritaires même pour PRODUCED. Identité d’occurrence, cotes historiques et HERITE/PHRASE conservés. La portée locale de C0-A est explicite. |
| A8 | Impacts UC02/07/14/15 et lots assignés. `item` sémantique reste L1-A/C0-B. C0A-ST-01 signale la branche du patch à corriger après autorisation; C0A-REV-01 reste distincte dans UC15. |

Aucun arbitrage bloquant n’est identifié pour **concevoir ce seul profil**.
L’activation du chemin direct et la validation du contrat complet de
propriété nécessiteront la solution et les preuves L1-A. La proposition
technique de copie systématique demeure soumise à la décision utilisateur.

## 4. Attestation B et état antérieur à la décision utilisateur

**VALIDE_ARCHITECTURE — B, 20 octobre 2026 — exclusivement pour le sous-cas
`UC-C-13::C0A_ISOLER`, version C0A-UML-R2-ST**, fichiers du manifeste.
Cette nouvelle attestation T/F/A ne valide ni UC13 complet, ni ST04 sur toutes
les écritures, ni le patch actuel, ni le lot C0-A entier.

**Approbation utilisateur : AUCUNE.** Version exacte proposée : C0A-UML-R2-ST,
sous-cas C0A_ISOLER, avec la copie neuve sur chaque différence réelle de texte
et les exclusions ci-dessus. Aucun passage APPROUVE_UTILISATEUR ou
PRET_DEVELOPPEMENT, aucune autorisation d’implantation déduite de la décision
métier déjà acquise ST01–ST05.

## 5. Contrôle ultérieur et journal

Le patch reste inchangé. Un futur mandat A devra couvrir explicitement
C0A-ST-01, ses fichiers et contre-épreuves, sur copie Git indépendante et
PostgreSQL jetable sans écriture réelle; les dossiers 14/15, leur approbation
et C0A-REV-01 restent nécessaires au lot entier. Un élargissement de fichiers
ne peut être absorbé tacitement. Conformité après implantation : NON EVALUEE.

| Date | Version / action | Effet |
|---|---|---|
| 2026-10-20 | R1, ancien dossier | Attestation antérieure conservée; aucune approbation utilisateur obtenue. |
| 2026-10-20 | R2-ST, mandat utilisateur sur les invariants | AC02/03 seuls reformulés; quatre vues révisées; nouvelle attestation B pour C0A_ISOLER uniquement; dossier à approuver. |


## 6. Décision utilisateur du 20 octobre 2026 — état courant

**APPROUVE_UTILISATEUR pour UC-C-13::C0A_ISOLER, C0A-UML-R2-ST seulement.**
Source exacte : [mandat reçu](../../references/MANDAT_APPROBATION_UC13_VALIDATION_C0A_2026-10-20.md).
Référence : [PR #30](https://github.com/LPDavidbdeb/court/pull/30), fusion
`cd584c307fcc31096dd93daae6a8fc26ab949eaf`, modèle global G-C0A-R2-ST.
Empreinte du manifeste approuvé :
`367846c13385444b673a2a21e4c57599812c33118a74d917a7064ccd4fdfaa3d`.
[Copie contractuelle immuable](../../versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md)
et [périmètre structuré de la décision](approbation.json).

L’approbation exclut L1-A permanent, modification directe privée, UC14/15,
patch actuel, développement, fusion et migration. Les mentions AUCUNE ci-dessus
sont conservées comme état historique précédent. La décision ne transfère pas
son approbation à un futur modèle global ou à un autre sous-cas.

Les douze fichiers .puml/.svg/.png UC13 restent identiques au manifeste d’origine.
Les modifications de suivi n’affectent aucun critère, branche ou responsabilité.
Aucune nouvelle exécution applicative. **PRET_DEVELOPPEMENT : NON**.

| Date | Décision | Périmètre et résultat |
|---|---|---|
| 2026-10-20 | Approbation utilisateur expresse, mandat SHA-256 997a88cc5392c753f21d0b2cba2005263df63e10947ba29f02c60ff5147ee094 | UC13::C0A_ISOLER R2-ST au manifeste du commit cd584c3; pas d’autorisation d’implantation. |
