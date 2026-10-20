# UC-C-12::DIAGNOSTIQUER_EXAMEN — Décision historique et état courant

**CIT-UML-R1 — 20 octobre 2026 — EN_REVUE; aucune approbation.**
Lecture seule proposée; quatre vues et états, sans activation de reconfirmation.
G-C0A-R3-CIT, socle lu 515666e. [Analyse CIT-D3/D4](../../../ANALYSE_CIBLEE_CITATIONS_C0A.md).
Propriétaire de la consultation : UC12; écriture d’un nouvel examen : UC05E.
Diagnostic limité candidat C0-A à mandater; journal/examens L1-A/C0-B, adaptateurs
citations L3-B selon source. Pas de validation de tout UC12 ni de code ici.

| AC | Critère proposé |
|---|---|
| AC01 | Restituer etat/traitement/motif/date enregistrés sans écriture et sans les confondre avec validité actuelle. L’absence de décision reste à établir. |
| AC02 | Comparer les occurrences actuelles avec leurs captures dans le périmètre réellement disponible : Document, type, identité et contenu. Divergence vérifiable : périmé. Composition/contexte non capturés : limite/non attesté explicite, jamais preuve reconstruite. |
| AC03 | Exposer séparément admissibilité au contrat d’examen : Statement vérifié, type non pris en charge, objet absent ou couple incohérent. Quote hors contrat E01 n’est pas une preuve globalement invalide; certification PHRASE ne suffit pas à confirmer une concordance. |
| AC04 | Exposer reexamen_possible et son motif. Ne pas proposer de reconfirmation répétée lorsque le type n’est pas représentable ou le journal conservant les décisions n’est pas disponible; aucun appel à la fonction écrasante dans ce sous-cas. |
| AC05 | Un futur nouvel examen, hors activation de ce profil, relit contenu/contexte et ajoute une décision après journal immuable UC05E disponible. Citation : manifeste typé et adaptateur de régime vérifié requis en plus. Échec ou conflit annule l’ajout, ancienne décision intacte; aucune validation rétroactive. |
| AC06 | Afficher transitions et motifs : à établir; courant limité; périmé; non attesté/type hors contrat. Un objet absent/couple incohérent exige d’abord correction autorisée. A_REEXAMINER de compatibilité n’efface pas ces causes ni l’historique. |

Le patch calcule A_REEXAMINER pour toute extrémité non Statement. La fonction
confirmer_traitement ignore Quote puis remplace les M2M/champs : aucun cycle
fiable de reconfirmation ne peut être promis sur cette base. Les transitions
futures dessinées sont conditionnelles et **hors** sous-cas de lecture C0-A.
Le journal ExamenEditorial dans l’ERD est PROPOSE L1-A; aucune table ajoutée.

CIT-D3/D4 restent à approuver. Les diagnostics peuvent rendre la situation
compréhensible immédiatement après implantation autorisée; la sortie par un
nouvel examen attend les capacités réelles, sans dépendance circulaire C0-A.
Tous les scénarios sont NON EXECUTES. Les règles de A restent intactes.

[Activité](activity.svg) · [Séquence](sequence.svg) · [ERD](erd.svg) · [Classes](class.svg)
· [États de la lecture et transition future](states.svg).
Sources .puml correspondantes; [traçabilité](tracabilite.md), [validation](validation.md).
