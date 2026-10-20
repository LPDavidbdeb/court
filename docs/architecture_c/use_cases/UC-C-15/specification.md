# UC-C-15 — Consulter les appuis historiques avec leurs diagnostics

**C0A-UML-R2-DIAG — 20 octobre 2026 — profil C0-A approuvé, contexte G-C0A-R3-CIT.**
Approbation utilisateur : **APPROUVE_UTILISATEUR**, au commit 30724df / PR #31; [décision et manifeste original](approbation.json). Socle lu 515666e. Aucun code, schéma,
patch ou examen nouveau réalisé. Sources : NR07, CF3-26, COV-F-AC01,
[mandat](../../references/MANDAT_APPROBATION_UC13_VALIDATION_C0A_2026-10-20.md).
**C0A-REV-01 reste ouverte dans le patch**; les quatre vues définissent sa correction.

Acteur : lecteur; déclencheur : consultation/export du couple documentaire.
Une lecture d’origine ne vaut ni sélection d’appui courant ni reconfirmation.

| AC | Critère observable |
|---|---|
| AC01 | Vérifier occurrence cible et couple documentaire; restreindre les correspondances au Document cible réel et au Document source demandé. Cible étrangère, Document inexistant ou origines multiples sans choix explicite : erreur globale, aucune lecture d’un autre couple. L’appel historique sans source ne reste possible qu’en l’absence d’ambiguïté. |
| AC02 | Pour chaque extrémité SOURCE du couple, vérifier Document, clé générique complète, ContentType Statement et objet réel avant de lire AppuiDepotJuillet. Un nœud structurel sans type ni objet ne produit aucun appui et n’entraîne aucune exploration implicite de ses descendants. |
| AC03 | Une archive non typée, absence, mauvais Document, type non pris en charge ou objet manquant ajoute un diagnostic local identifiable sans abandonner les autres origines. Dans tous les ordres, préserver chaque appui valide du même couple; jamais déduire le type d’une archive ou d’une PK homonyme. |
| AC04 | Retourner LectureAppuis en mémoire : appuis_valides, anomalies et lecture_complete. Chaque résultat garde correspondance/extrémité/occurrence/appui et qualification VERSION SOURCE. Ne pas fusionner par seul Statement ou cote des origines distinctes. Aucune décision, capture ou confirmation créée. |
| AC05 | Distinguer erreur globale de contexte et anomalie locale. Une panne de stockage ou exception inattendue fait échouer la lecture; ne pas la convertir en résultat complet vide. Aucun résultat d’erreur globale ou technique n’est admissible au strict. |
| AC06 | L’export conserve appuis et diagnostics dans les lignes, collecte les diagnostics avant son verdict et les transmet au contrôle EX04 existant de résolution des sources. Anomalie non résolue ou lecture incomplète : strict_possible faux. Lecture complète seule : aucun strict acquis; EX01–EX07 restent cumulatifs. Aucun EX08 inventé. |
| AC07 | Une absence de lien ou une liste d’appuis vide ne décide ni retrait, ni ajout, ni absence d’appui confirmée. Une citation hors du contrat Statement reçoit un diagnostic de type, indépendamment de sa certification; elle n’est pas déclarée globalement invalide et ne devient pas automatiquement un appui retenu. |

## Résultat proposé, sans table nouvelle

`LectureAppuis(appuis_valides, anomalies, lecture_complete)` est un résultat
non persistant. Chaque DiagnosticAppui porte code, message, correspondance,
extrémité et identités documentaires; occurrence et archive si disponibles.
Codes locaux proposés : ORIGINE_ARCHIVEE_NON_ATTESTEE, ORIGINE_ABSENTE,
DOCUMENT_SOURCE_INCOHERENT, CLE_GENERIQUE_INCOHERENTE, TYPE_NON_PRIS_EN_CHARGE,
OBJET_INTROUVABLE. Le gestionnaire du type exact est vérifié avant l’objet;
une Quote, y compris PHRASE certifiée, n’est jamais lue comme un Statement.

Une structure vide vérifiée ne crée pas d’anomalie. Zéro origine déclarée
peut donner une lecture vide, mais ne satisfait pas par lui-même les autres
contrôles de concordance. Des anomalies sans aucun appui donnent une lecture
incomplète, distincte d’une lecture complète sans appui.
L’erreur globale est un résultat d’échec séparé (motif explicite), pas un
LectureAppuis partiellement « validé ». Une exception inattendue est propagée.

## Export et limites

Les appuis restent visibles en consultation qualifiée même si une autre
extrémité est invalide. La construction de l’export conserve cette information,
puis enrichit les motifs EX04 et calcule le strict cumulatif; une note libre
n’est pas un contrôle. Le patch actuel lève ValueError pour l’anomalie locale
et l’export remplace alors toutes les origines par une liste vide : AC03/06
ne sont pas satisfaits. Le [constat antérieur](../../lots/C0-A/CONTRE_EPREUVE_LECTEUR_SANS_BASE.json)
est conservé, sans être présenté comme un essai de la correction.

La fraîcheur/reconfirmation relève de UC12/05E. La possibilité de consulter
une ancienne association incompatible ne l’autorise pas comme nouveau partage.
Les archives typées et nature restent L1-A/C0-B; aucune origine ou ancien examen
n’est fabriqué. Les diagnostics de citation n’altèrent aucun régime HERITE/PHRASE.

**C15-D1 approuvé le 20 octobre 2026 :** résultat partiel qualifié, erreur globale distincte,
export bloqué au strict si incomplétude. Aucune réserve technique bloquante
identifiée pour ce contrat documentaire; aucune conformité applicative attestée.
[Vues](activity.svg) : [activité source](activity.puml), [séquence](sequence.svg)
([source](sequence.puml)), [ERD](erd.svg) ([source](erd.puml)),
[classes](class.svg) ([source](class.puml)).
[Traçabilité](tracabilite.md) · [Validation B](validation.md) · [Empreintes](manifest_sha256.json).
Version R1 au [commit cd584c3](https://github.com/LPDavidbdeb/court/tree/cd584c307fcc31096dd93daae6a8fc26ab949eaf/docs/architecture_c/use_cases/UC-C-15).

Suivi administratif de l’approbation uniquement : critères AC et quatre vues
inchangés. La [spécification présentée exactement au Product Owner](../../versions_approuvees/UC-C-15_C0A-UML-R2-DIAG/use_cases/UC-C-15/specification.md)
est préservée avec le manifeste original. Le [mandat C0-A](../../lots/C0-A/MANDAT.md)
reste un projet à approuver avant toute implantation.
