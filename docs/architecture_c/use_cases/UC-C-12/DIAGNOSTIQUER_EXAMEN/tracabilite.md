# UC12::DIAGNOSTIQUER_EXAMEN — Traçabilité CIT-UML-R1

CIT-D3/D4 ouverts. Scénarios **NON EXECUTES**. Le diagramme d’états complète
les quatre vues; les branches de nouvel examen sont futures et non activées.

| Source | AC | Activité | Séquence | ERD | Classes / états | Scénario attendu |
|---|---|---|---|---|---|---|
| Décision historique conservée | AC01 | ACT12-DEC/AET | SEQ12-DEC | Correspondance.etat/traitement/motif/decide_le | CLS12-DEC; état A | CIT-E01 : lecture sans écriture, décision absente reste à établir. |
| Occurrence réelle / NR03/TR02 | AC02 | ACT12-FRESH/PERIME/LIMITE/MANQUE | SEQ12-FRESH/MANQUE | ERD12-CAP/LIMITE | CLS12-FRESH; états C/P | CIT-E02/E03 : autre identité ou texte → périmé; composition/contexte non capturés restent limite explicite. |
| Admissibilité distincte | AC03 | ACT12-TYPE/INADM/HORS | SEQ12-TYPE | Statement vs Quote et FK/captures distinctes | CLS12-TYPE; états H/I | CIT-E04/E05 : Quote certifiée hors contrat E01; objet absent/couple faux à rétablir, pas simple périmption. |
| Nouvel examen réalisable | AC04 | ACT12-RESULT/NOW | SEQ12-RESULT et note fonction écrasante | ERD12-FUTUR absent de C0-A | CLS12-CAPACITE; transitions N gardées | CIT-E06 : reconfirmation indisponible et motif exact, aucun appel de confirmation dans le diagnostic. |
| Journal immuable, pas de passé inventé | AC05 | ACT12-FUTUR légende | SEQ12-FUTUR/APPEND | J proposé L1-A, manifeste typé futur | CLS12-APPEND; N/NC/échec | CIT-E07 : après capacités livrées, ajout d’un examen conservant l’ancien; conflit annule le nouvel ajout. |
| États/motifs exploitables | AC06 | ACT12-RESULT | SEQ12-RESULT | DTO non persistant, limites explicites | QualificationLecture; states.puml | CIT-E08 : affichage distinct courant limité/périmé/hors contrat/absent; A_REEXAMINER n’est pas une promesse de reconfirmation. |

| ID | Résultat attendu | Lot / exécution |
|---|---|---|
| CIT-E01 | Relire décision stockée/absence sans mutation ni capture rétroactive. | Diagnostic candidat C0-A à mandater; NON EXECUTE |
| CIT-E02 | Nouveau Statement même texte puis même identité texte changé : divergence détectée, ancienne décision/capture intacte. | C0-A limité puis C0-B; NON EXECUTE |
| CIT-E03 | Capture totalement absente, composition d’occurrences ou item hors manifeste : limite signalée, jamais examen complet reconstruit depuis les données présentes. | Diagnostic C0-A, manifeste L1-A/C0-B; NON EXECUTE |
| CIT-E04 | Quote Email/PDF × HERITE/PHRASE, certifiée ou non : type hors contrat E01 distingué de l’admissibilité fournisseur et de la péremption d’un examen. | Diagnostic, adaptateurs L3-B; NON EXECUTE |
| CIT-E05 | Source absente ou mauvais Document : nouvel examen indisponible tant que la source n’est pas rétablie par voie autorisée. | Diagnostic puis correction mandatée; NON EXECUTE |
| CIT-E06 | Journal/adaptateur indisponible : motif visible, aucun appel de confirmer_traitement ni boucle de reconfirmation. | C0-A / futurs préalables; NON EXECUTE |
| CIT-E07 | Nouvel examen après journal et type admissible livrés : ajout, ancien conservé; conflit/échec sans écriture partielle ni état artificiellement forcé. | UC05E/L1-A/C0-B et L3-B selon type; NON EXECUTE |
| CIT-E08 | Changement de cause : interface distingue limites, type hors contrat, péremption et obstacle de source; anciennes décisions consultables. | Diagnostic à autoriser; NON EXECUTE |
