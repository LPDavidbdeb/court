# UC-C-13 — Traçabilité TRANS-04

Version C0A-UML-R1. Les tests nommés appartiennent au patch conservé, **pas au
code principal actuel**. Résultats historiques : rapport isolé P6; nouvelle
exécution sur `515666e` : **NON EXECUTEE** pour chaque ligne.

| Exigence | AC | Activité | Séquence | ERD cible | Classes | Scénario / contre-épreuve à exécuter |
|---|---|---|---|---|---|---|
| NR01/11, autorisation C0-A | AC01 | ACT-REFUS | SEQ-02, refus sans mutation | ReferentHistorique.document_id; Document.source_type | CLS-VUE / protection.est_referent, est_reproduit | `C0AEditionEtConservation.test_http_referent_refuse_sans_effet_partiel`; `test_http_reproduced_refuse_aussi_le_simple_renommage` |
| Détachement CF3-D4, NR03/11 | AC02 | ACT-CAP/COW | SEQ-04/05 | LibraryNode.object_id; GFK typée vers Statement; ERD-CAP | CLS-CAP; detacher_pour_edition | `test_http_edition_detache_deux_documents_produced`; `test_http_cible_detache_le_texte_du_referent`; variantes même Document et source protégée |
| Conservation des captures | AC03 | ACT-CAP | SEQ-04/06/07 | VersionTexte.texte/empreinte; UQ(statement,empreinte) | VersionTexte.capter; CLS-GARDE | `test_edition_privee_capture_le_texte_avant_modification`; ancienne capture toujours lisible |
| Édition sans faux détachement | AC04 | ACT-NOOP; branche vide; ACT-REFUS | SEQ-03/09; refus de type | LibraryNode.content_type_id/object_id; Statement.id | CLS-VUE; Statement.save | `test_sauvegarde_identique_ne_detache_pas_le_statement`; variantes création sur vide, type non Statement et GFK incomplète |
| Fraîcheur de l’appui NR03/TR02 | AC05 | ACT-FRESH | SEQ-10 | ERD-FRESH; ConfirmationAppui.version_examinee_id → VersionTexte.statement_id | CLS-FRESH; ConfirmationAppui.etat_courant | `C0AFraicheurEtPerimetre.test_confirmation_appui_perimee_apres_detachement`; `test_meme_texte_autre_statement_invalide_meme_un_noeud_deja_charge`; `test_absence_dappui_reexaminee_apres_detachement`; sans capture → réexamen |
| Fraîcheur éditoriale | AC06 | ACT-FRESH | SEQ-10 | Correspondance M2M SOURCE/CIBLE; ExtremiteCorrespondance.noeud_id/role | Correspondance.versions_courantes_examinees | `test_traitement_reexamine_apres_detachement_partage`; `test_meme_texte_autre_statement_reexamine_le_traitement`; `test_detachement_du_cote_source_perime_aussi_le_traitement`; CF3-20 complet différé |
| Refus atomiques NR11 | AC07 | ACT-ITEM/ROLLBACK | SEQ-08, SEQ-ROLLBACK | Identités LibraryNode/Statement/VersionTexte restaurées; aucune contrainte SQL nouvelle prétendue | CLS-VUE/CLS-GARDE; service atomique | `test_refus_apres_detachement_annule_aussi_les_nouveaux_objets`; compter objets et comparer les relations avant/après |
| P6, NR02, CF3-26 typé | AC08 | ACT-REFUS et postcondition finale | SEQ-02/09/10 | LibraryNode.id/paragraph_number; GFK conditionnelle | LibraryNode.save; gardes protection | Suites E01/régime A du socle, test homonymie d’identifiants; aucun nouveau champ/table; pas de réécriture historique |

Les scénarios supplémentaires sans nom de méthode identifient des variantes
à ajouter ou à rattacher par A; ils ne sont pas déclarés présents ou passés.
Le [rapport](../../RAPPORT_REVUE_COUVERTURE_ET_C0A.md) distingue la vérification
syntaxique du patch, réellement exécutée, de ces tests applicatifs.
