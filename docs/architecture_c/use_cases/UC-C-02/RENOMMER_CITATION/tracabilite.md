# UC02::RENOMMER_CITATION — Traçabilité CIT-UML-R1

CIT-D1/D2 ouverts. Tous les scénarios sont **NON EXECUTES**; aucun mandat de code.

| Source | AC | Activité | Séquence | ERD | Classes | Scénario attendu |
|---|---|---|---|---|---|---|
| ST01/ST05 | AC01 | ACT02-GARDE | SEQ02-GARDE | Document.source_type, LibraryNode.document_id | CLS02-GARDE | CIT-I01 : REPRODUCED/référent et protection historique refusent item sans aucune mutation. |
| Responsabilité rédactionnelle | AC02 | ACT02-REQ/PAYLOAD | SEQ02-REQ/PAYLOAD | ERD02-ITEM : seule colonne permise | CLS02-ACTION/ITEM | CIT-I02 : contenu/repointage soumis refusé; aucun Statement créé, aucun save Quote. |
| Régimes distincts | AC03 | ACT02-TYPE | SEQ02-TYPE | ERD02-QUOTE, GFK qualifiée | CLS02-TYPE | CIT-I03 : Email/PDF × HERITE/PHRASE, même PK intermodèle et objet filtré; jamais de substitution. |
| item et contexte | AC04 | ACT02-CONTEXTE/SEM | SEQ02-CONTEXTE | ERD02-CONTEXTE : contexte non capturé | CLS02-CONTEXTE | CIT-I04/I05 : intitulé pur admissible selon profil, rôle/index ou dépendance d’examen : refus. |
| Atomicité / non-altération | AC05 | ACT02-TX/ITEM/ROLLBACK/NOOP | SEQ02-RELOAD/ITEM/ROLLBACK/ECHEC | LibraryNode.item; tous attributs Quote inchangés | CLS02-ITEM | CIT-I06/I07 : no-op sans écriture; conflit/refus tardif/échec laisse tous les états intacts. |
| Erreur visible / A préservé | AC06 | ACT02-RESULT | SEQ02-RESULT | pas de table nouvelle ou source modifiée | ActionRenommage.afficher_succes_refus | CIT-I08 : erreur exploitable affichée; aucune activation du rendu PHRASE ni modification des contrôles A. |

| ID | Résultat attendu | Lot / exécution |
|---|---|---|
| CIT-I01 | Renommage protégé : refus, item/GFK/citation/source/captures inchangés. | L1-B ou extension C0-A expresse; NON EXECUTE |
| CIT-I02 | Payload contient text, quote_text, nouvelle GFK ou changement de régime : refus, même si la valeur est vide. | Même périmètre conditionnel; NON EXECUTE |
| CIT-I03 | Citation identifiée via régime explicite, PHRASE non visible par objects correctement distinguée; citation manquante refusée. | Même périmètre; NON EXECUTE |
| CIT-I04 | Présentation seule sans dépendance d’examen, genre/index inchangés : item modifié seulement; associations et autres occurrences inchangées. | Même périmètre; NON EXECUTE |
| CIT-I05 | C-… / vide / changement d’index ou contexte d’examen possible/indéterminable : refus; aucune reconfirmation fabriquée. | Limite C0-A, compléments L1-A/C0-B/L1-B; NON EXECUTE |
| CIT-I06 | Item identique : no-op; état attendu périmé : 409 sans effet. | Même périmètre; NON EXECUTE |
| CIT-I07 | Échec/refus tardif : rollback du seul item; source Quote et certification strictement inchangées. | Même périmètre; NON EXECUTE |
| CIT-I08 | Refus visible dans l’interface, sans erreur JSON silencieuse; contrôles de A inchangés. | Route/formulaire/interface à autoriser; NON EXECUTE |
