# UC-C-15 — Lire les appuis valides de la bonne origine

**C0A-UML-R1 — 20 octobre 2026 — C0-A — EN_REVUE.** Auteur : B; implantation
future : A. Approbation utilisateur : **AUCUNE**. Socle proposé `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`;
modèle global [G-C0A-R1](../../modele_global/README.md).

Comme lecteur, retrouver les appuis d’origine du couple documentaire demandé,
avec les anomalies visibles, sans les confondre avec les appuis actuellement
retenus. Sources : US-C-15, NR07, CF3-26 noyau typé, mandat de revue §5.
Lecture sans mutation; `nature` et archives typées futures restent hors C0-A.

**Cible de correction proposée, différente du patch conservé** : C0A-REV-01.
Les quatre vues montrent le contrat attendu; elles ne déclarent pas cette
correction déjà implantée. Les variantes d’anomalies et le contrat de retour
doivent être approuvés avant mandat de correction à A.

| AC | Critère observable |
|---|---|
| AC01 | Restreindre les correspondances au Document cible de l’occurrence et au Document source demandé. Un autre couple partageant le Statement n’apporte aucun appui. |
| AC02 | Lire AppuiDepotJuillet uniquement après vérification du Document de l’antécédent, du ContentType Statement et de son objet réel. Un groupe structurel sans contenu ne produit aucun appui. |
| AC03 | Dans un couple comportant antécédents valides et invalides, restituer tous les appuis valides et les anomalies locales identifiables, dans les deux ordres. Ne jamais deviner le type d’une archive ou assimiler object_id à Statement.pk. |
| AC04 | Qualifier les résultats VERSION SOURCE; ne créer ni ConfirmationAppui, ni nouvel examen, ni reprise automatique de validation. Cotes citées et historiques restent inchangées. |
| AC05 | Une cible étrangère au couple, ou plusieurs origines sans source explicitement demandée, entraîne une erreur globale avant lecture. Cette erreur se distingue d’une anomalie locale d’antécédent. |
| AC06 | L’export conserve les appuis valides et affiche les diagnostics; il ne les remplace pas tous par une liste vide sur la première anomalie. Une lecture partielle n’est pas présentée comme une validation stricte complète. Les diagnostics EX existants sont conservés, sans inventer EX08. |

Nominal : valider le couple → charger ses groupes → parcourir chaque extrémité
SOURCE → contrôler Document/type/objet → ajouter les appuis valides ou une
anomalie locale → restituer les deux informations. Proposition de résultat
en mémoire `LectureAppuis(appuis_valides, anomalies)` : pas de nouvelle table.
Le détail de l’API peut être adapté par A dans le périmètre approuvé, à
condition de préserver ces postconditions et ses consommateurs.

Une anomalie comporte au minimum groupe/extrémité/motif et distingue archive
non attestée, absence, mauvais Document et type incompatible. Un groupe
structurel vide est un cas normal, pas une fausse preuve d’absence.

Erreurs globales : contexte de requête invalide ou ambigu → refus explicite,
sans appui d’un autre couple. Anomalie locale : conserver les autres résultats
et signaler l’incomplétude; toute admissibilité stricte dépend encore des
contrôles E01 applicables, jamais du seul succès de cette lecture.

Le patch actuel lève ValueError pour chaque anomalie locale, et `_ligne`
efface alors `origines`; il ne satisfait donc pas AC03/AC06. Voir la
[contre-épreuve](../../lots/C0-A/CONTRE_EPREUVE_LECTEUR_SANS_BASE.json).
L’export devient consultable avec résultats partiels qualifiés; lever une
anomalie bloquante pour un nouveau strict requiert une correction des données
ou l’examen prévu, pas une validation implicite.

Dépendance de conception : contrat des archives disponibles de 14, données
E01 existantes. Exécution future : C0-A après approbation/mandat, indépendamment
de L1-A et de Preuve. Tests Django/SQL sur `515666e` encore non exécutés.

Vues : [activité](activity.svg) ([source](activity.puml)),
[séquence](sequence.svg) ([source](sequence.puml)),
[ERD](erd.svg) ([source](erd.puml)),
[classes](class.svg) ([source](class.puml)).
[Traçabilité](tracabilite.md) · [Validation](validation.md).
