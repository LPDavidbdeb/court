# UC-C-14 — Traçabilité TRANS-04

C0A-UML-R1. Toutes les exécutions applicatives sur `515666e` sont **NON EXECUTEES**.

| Source | AC | Activité | Séquence | ERD | Classes | Scénarios et contre-épreuves |
|---|---|---|---|---|---|---|
| NR01/11; mandat C0-A | AC01 | ACT-BLOC/PRE/REFUS | SEQ-02/03 | Document.source_type; ReferentHistorique.document_id; ConfirmationAppui.noeud_id; AncrageCitation.noeud_id | CLS-GARDE | `C0AFraicheurEtPerimetre.test_suppression_avec_decision_dappui_refuse_tout_le_bloc`; variante ancrage et descendant référent |
| Captures disponibles | AC02 | ACT-ARCH | SEQ-04 | NoeudArchive.noeud_pk/statement_pk/texte/texte_sha256 | CLS-ARCH | `C0AEditionEtConservation.test_http_suppression_liee_archive_et_preserve_la_source`; homonyme GFK non Statement |
| CF3-D4, NR12 partiel | AC03 | ACT-REL | SEQ-05 | ExtremiteCorrespondance.archive_id/noeud_id; ERD-ARCH | CLS-REL | Même test, relation lisible via archive; C0A-REV-01 traité par UC15; NR12 complet reste C0-B |
| Conservation des objets utiles | AC04 | ACT-PURGE | SEQ-06/07 | Statement.id; VersionTexte.statement_id; LibraryNode GFK vérifiée | CLS-PURGE | `test_suppression_conserve_les_captures_du_statement_devenu_prive`; `test_un_identifiant_generique_ne_declenche_pas_la_purge_dun_statement` |
| Refus atomique | AC05 | ACT-ROLLBACK | SEQ-ROLLBACK | Ensemble des IDs avant/après; atomicité portée par séquence, pas contrainte ERD inventée | supprimer_occurrence; service avant catch vue | `test_echec_archivage_annule_tout_le_bloc_http`; refus après archives/repointages à tester |
| Protection historique locale | AC06 | ACT-PRE et archives conservées | SEQ-03/07; gardes suppression | VersionTexte et NoeudArchive; FK/cascades existantes | protection.gardes pre_delete | `test_purge_directe_du_statement_examine_est_refusee`; `test_purge_directe_dune_capture_examinee_est_refusee`; `test_suppression_document_ne_detruit_pas_sa_concordance`; `test_suppression_archive_liee_est_refusee` |

Présence d’une méthode dans le patch et succès rapporté sur P6 ne valent pas
nouvelle exécution. Variantes sans méthode citée : à ajouter/rattacher lors du
mandat A. Les protections globales CF3-25 restent L5.
