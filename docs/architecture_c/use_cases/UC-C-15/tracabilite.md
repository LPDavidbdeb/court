# UC-C-15 — Traçabilité C0A-UML-R2-DIAG

Tous les scénarios applicatifs sont **NON EXECUTES**. La contre-épreuve en
mémoire antérieure établit un défaut du patch, pas le succès de sa correction.
C0A-REV-01 reste ouverte; COV:T-F01 et les espaces de noms existants sont conservés.

| Source | AC | Activité | Séquence | ERD | Classes | Scénario / attendu |
|---|---|---|---|---|---|---|
| NR07 | AC01 | ACT15-REQ/PAIR/GLOBAL | SEQ15-PAIR/GLOBAL | ERD15-PAIR, Document et extrémités | CLS15-PAIR/GLOBAL | C15:T01/T02 : bon couple seulement; ambiguïté sans source ou cible étrangère : erreur globale. |
| CF3-26, ST02/ST04 | AC02 | ACT15-VALID et structure vide | SEQ15-VALID | ERD15-TYPE, ContentType et objet réel | CLS15-TYPE/VALID | C15:T03/T04 : PK homonyme ne donne aucun appui; structure sans contenu n’invente pas de descendants. |
| COV-F-AC01, C0A-REV-01 | AC03 | ACT15-DIAG/RESULT | SEQ15-DIAG/RESULT | ERD15-ARCH et extrémités | CLS15-ITER/DIAG | COV:T-F01 / C15:T05/T06 : valable+invalide, deux ordres et permutations, conservent exactement les valables. |
| Historique distinct du courant | AC04 | ACT15-RESULT | SEQ15-RESULT/LIGNE | AppuiDepotJuillet; DTO non persistant ERD15-DTO | CLS15-RESULT/LIGNES | C15:T07 : origine qualifiée complète, pas de dédoublonnage par cote seule, aucun examen écrit. |
| Erreur globale / technique distincte | AC05 | ACT15-GLOBAL et légende panne | SEQ15-GLOBAL/TECH | aucune table d’erreur, données inchangées | CLS15-GLOBAL, ErreurContexteLecture | C15:T08 : panne propagée, jamais liste complète vide; refus global sans fuite d’autre couple. |
| Export et strict E01 | AC06 | ACT15-EXPORT/STRICT | SEQ15-LIGNE/STRICT | ERD15-DTO : booléen de lecture, pas validation persistée | CLS15-STRICT, EX04 | C15:T09/T10 : appuis visibles, motifs structurés, EX04 faux et strict_possible faux si incomplet; sept EX toujours requis. |
| Aucun examen / source inventé | AC07 | ACT15-RESULT et légende | SEQ15-TECH note lecture seule | ERD15-TYPE/ARCH | LectureAppuis, pas de mutation E01 | C15:T11/T12 : vide ≠ SANS_APPUI; Quote certifiée ≠ Statement ni concordance confirmée. |

| ID | Contre-épreuve / résultat attendu | Lot / exécution |
|---|---|---|
| C15:T01 | Deux couples partageant le même Statement : appuis du seul couple explicitement demandé. | C0-A; NON EXECUTE |
| C15:T02 | Cible étrangère, Document inexistant, origines multiples sans source : erreur globale, pas de résultat complet. | C0-A; NON EXECUTE |
| C15:T03 | Quote/Event de même PK qu’un Statement : diagnostic de type, aucun AppuiDepotJuillet lu par confusion numérique. | C0-A; NON EXECUTE |
| C15:T04 | Source structurelle vide, avec descendants non sélectionnés : aucun appui ni exploration implicite. | C0-A; NON EXECUTE |
| C15:T05 | Une origine valide + type invalide, archive, absence, mauvais Document ou objet absent; inverser les ordres : appuis valides et codes diagnostiques identiques à l’ordre près. | COV:T-F01; C0-A; NON EXECUTE |
| C15:T06 | Plusieurs valides et plusieurs anomalies, permutation des extrémités : aucune perte du sous-ensemble valide; toutes les anomalies représentées. | COV:T-F01; C0-A; NON EXECUTE |
| C15:T07 | Même pièce via deux origines : garder chaque filiation qualifiée, sans union par cote/Statement; comptes des décisions et captures identiques avant/après. | C0-A; NON EXECUTE |
| C15:T08 | Exception de stockage pendant une lecture après un premier appui : résultat d’échec, jamais succès complet vide/partiel. | C0-A; NON EXECUTE |
| C15:T09 | Export d’un ensemble mixte : appuis conservés, diagnostics structurés et visibles, EX04 insatisfait, strict refusé. | C0-A; NON EXECUTE |
| C15:T10 | Lecture sans anomalie mais EX02 ou EX05 faux : strict reste impossible; ne pas réduire strict_possible à lecture_complete. | C0-A; NON EXECUTE |
| C15:T11 | Zéro appui / zéro lien : ne crée pas une décision SANS_APPUI, retrait ou ajout. | C0-A; NON EXECUTE |
| C15:T12 | HERITE puis PHRASE certifiée hors contrat Statement : motif de type indépendant de la certification; aucun appui ou examen nouveau. | C0-A, diagnostic UC12; NON EXECUTE |

Les méthodes antérieures test_lecteur_restreint_au_couple_explicitement_demande,
test_export_ne_melange_pas_les_appuis_dun_autre_document,
test_identifiant_generique_ne_designe_pas_un_statement_homonyme et
test_archive_non_typee_reste_diagnostiquee_sans_deviner ne remplacent pas les
cas mixtes ni la preuve de correction de l’export. Les 38 scénarios NR/CF3 et
EX01–EX07 ne sont ni renumérotés ni déclarés réexécutés.
