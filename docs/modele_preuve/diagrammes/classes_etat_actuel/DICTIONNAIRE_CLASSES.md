# Dictionnaire des classes actuelles

Généré le 2026-10-20 depuis `212a7feee81aef46a5b43d36e8eeafe0f8870064`. Extraction statique; aucune donnée lue.

Les modèles, attributs et méthodes sont réels. Les types absents du Python ne sont pas devinés.
Les attributs ORM utilisent des types de valeur abrégés; leurs contraintes complètes restent dans l’ERD.

| Classe | Nature | Vue complète | Source |
|---|---|---|---|
| `ai_services.models.GeminiResponse` | model | [10_utilisateurs_ia](10_utilisateurs_ia.svg) | [ai_services/models.py:6](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/ai_services/models.py#L6) |
| `ai_services.utils.EvidenceFormatter` | class | [13_import_audit_traitement](13_import_audit_traitement.svg) | [ai_services/utils.py:9](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/ai_services/utils.py#L9) |
| `argument_manager.mixins.EvidenceDeleteMixin` | mixin | [13_import_audit_traitement](13_import_audit_traitement.svg) | [argument_manager/mixins.py:5](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/argument_manager/mixins.py#L5) |
| `argument_manager.models.AppuiFait` | model | [04_argumentation](04_argumentation.svg) | [argument_manager/models.py:611](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/argument_manager/models.py#L611) |
| `argument_manager.models.Axe` | model | [04_argumentation](04_argumentation.svg) | [argument_manager/models.py:428](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/argument_manager/models.py#L428) |
| `argument_manager.models.Fait` | model | [04_argumentation](04_argumentation.svg) | [argument_manager/models.py:473](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/argument_manager/models.py#L473) |
| `argument_manager.models.NatureFait` | enum | [04_argumentation](04_argumentation.svg) | [argument_manager/models.py:454](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/argument_manager/models.py#L454) |
| `argument_manager.models.PerjuryArgument` | model | [04_argumentation](04_argumentation.svg) | [argument_manager/models.py:383](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/argument_manager/models.py#L383) |
| `argument_manager.models.RattachementAxe` | model | [04_argumentation](04_argumentation.svg) | [argument_manager/models.py:560](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/argument_manager/models.py#L560) |
| `argument_manager.models.RoleAppui` | enum | [04_argumentation](04_argumentation.svg) | [argument_manager/models.py:420](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/argument_manager/models.py#L420) |
| `argument_manager.models.TrameNarrative` | model | [04_argumentation](04_argumentation.svg) | [argument_manager/models.py:14](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/argument_manager/models.py#L14) |
| `case_manager.cotes_concordance.LockIndisponible` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [case_manager/cotes_concordance.py:35](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/cotes_concordance.py#L35) |
| `case_manager.evidence_audit.ReferenceOccurrence` | dataclass | [13_import_audit_traitement](13_import_audit_traitement.svg) | [case_manager/evidence_audit.py:110](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/evidence_audit.py#L110) |
| `case_manager.models.AISuggestion` | model | [05_dossiers_transmissions](05_dossiers_transmissions.svg) | [case_manager/models.py:55](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L55) |
| `case_manager.models.AncrageCitation` | model | [03_bordereau_appuis](03_bordereau_appuis.svg) | [case_manager/models.py:684](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L684) |
| `case_manager.models.AppuiDepotJuillet` | model | [03_bordereau_appuis](03_bordereau_appuis.svg) | [case_manager/models.py:295](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L295) |
| `case_manager.models.BordereauDepotJuillet` | model | [03_bordereau_appuis](03_bordereau_appuis.svg) | [case_manager/models.py:132](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L132) |
| `case_manager.models.ConfirmationAppui` | model | [03_bordereau_appuis](03_bordereau_appuis.svg) | [case_manager/models.py:572](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L572) |
| `case_manager.models.DestinataireInstance` | model | [05_dossiers_transmissions](05_dossiers_transmissions.svg) | [case_manager/models.py:408](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L408) |
| `case_manager.models.EtatAppui` | enum | [03_bordereau_appuis](03_bordereau_appuis.svg) | [case_manager/models.py:564](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L564) |
| `case_manager.models.ExhibitRegistry` | model | [05_dossiers_transmissions](05_dossiers_transmissions.svg) | [case_manager/models.py:16](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L16) |
| `case_manager.models.FichierTransmis` | model | [05_dossiers_transmissions](05_dossiers_transmissions.svg) | [case_manager/models.py:515](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L515) |
| `case_manager.models.LegalCase` | model | [05_dossiers_transmissions](05_dossiers_transmissions.svg) | [case_manager/models.py:8](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L8) |
| `case_manager.models.PerjuryContestation` | model | [05_dossiers_transmissions](05_dossiers_transmissions.svg) | [case_manager/models.py:31](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L31) |
| `case_manager.models.ProducedExhibit` | model | [05_dossiers_transmissions](05_dossiers_transmissions.svg) | [case_manager/models.py:90](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L90) |
| `case_manager.models.Transmission` | model | [05_dossiers_transmissions](05_dossiers_transmissions.svg) | [case_manager/models.py:458](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/models.py#L458) |
| `case_manager.piece_file_audit.AuditIssue` | dataclass | [13_import_audit_traitement](13_import_audit_traitement.svg) | [case_manager/piece_file_audit.py:72](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/case_manager/piece_file_audit.py#L72) |
| `cause_manager.models.Cause` | model | [01_causes_documents](01_causes_documents.svg) | [cause_manager/models.py:12](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/cause_manager/models.py#L12) |
| `cause_manager.models.EtatCause` | model | [01_causes_documents](01_causes_documents.svg) | [cause_manager/models.py:63](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/cause_manager/models.py#L63) |
| `cause_manager.models.LienCause` | model | [01_causes_documents](01_causes_documents.svg) | [cause_manager/models.py:82](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/cause_manager/models.py#L82) |
| `cause_manager.models.StatutCause` | enum | [01_causes_documents](01_causes_documents.svg) | [cause_manager/models.py:5](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/cause_manager/models.py#L5) |
| `core.mixins.ChampsEditables` | mixin | [11_heritage_regimes](11_heritage_regimes.svg) | [core/mixins.py:39](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/core/mixins.py#L39) |
| `core.mixins.ExhibitableMixin` | mixin | [11_heritage_regimes](11_heritage_regimes.svg) | [core/mixins.py:4](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/core/mixins.py#L4) |
| `core.piece_import.Adaptateur` | dataclass | [13_import_audit_traitement](13_import_audit_traitement.svg) | [core/piece_import.py:33](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/core/piece_import.py#L33) |
| `core.quote_regime.HeriteQuoteManager` | manager | [11_heritage_regimes](11_heritage_regimes.svg) | [core/quote_regime.py:39](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/core/quote_regime.py#L39) |
| `core.quote_regime.PhraseQuoteManager` | manager | [11_heritage_regimes](11_heritage_regimes.svg) | [core/quote_regime.py:46](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/core/quote_regime.py#L46) |
| `core.quote_regime.QuoteRegime` | enum | [11_heritage_regimes](11_heritage_regimes.svg) | [core/quote_regime.py:34](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/core/quote_regime.py#L34) |
| `document_manager.export_concordance.ExportStrictRefuse` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [document_manager/export_concordance.py:409](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/export_concordance.py#L409) |
| `document_manager.export_concordance.Verdict` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [document_manager/export_concordance.py:48](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/export_concordance.py#L48) |
| `document_manager.models.Correspondance` | model | [02_historique_e01](02_historique_e01.svg) | [document_manager/models.py:552](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L552) |
| `document_manager.models.Document` | model | [01_causes_documents](01_causes_documents.svg) | [document_manager/models.py:41](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L41) |
| `document_manager.models.DocumentSource` | enum | [01_causes_documents](01_causes_documents.svg) | [document_manager/models.py:16](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L16) |
| `document_manager.models.EtatConfirmation` | enum | [02_historique_e01](02_historique_e01.svg) | [document_manager/models.py:546](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L546) |
| `document_manager.models.ExtremiteCorrespondance` | model | [02_historique_e01](02_historique_e01.svg) | [document_manager/models.py:654](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L654) |
| `document_manager.models.FormatNumero` | enum | [01_causes_documents](01_causes_documents.svg) | [document_manager/models.py:268](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L268) |
| `document_manager.models.InstantaneNoeud` | model | [02_historique_e01](02_historique_e01.svg) | [document_manager/models.py:429](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L429) |
| `document_manager.models.InstantaneReferent` | model | [02_historique_e01](02_historique_e01.svg) | [document_manager/models.py:397](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L397) |
| `document_manager.models.LibraryNode` | model | [01_causes_documents](01_causes_documents.svg) | [document_manager/models.py:176](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L176) |
| `document_manager.models.Niveau` | model | [01_causes_documents](01_causes_documents.svg) | [document_manager/models.py:308](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L308) |
| `document_manager.models.NoeudArchive` | model | [02_historique_e01](02_historique_e01.svg) | [document_manager/models.py:692](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L692) |
| `document_manager.models.NumberingMode` | enum | [01_causes_documents](01_causes_documents.svg) | [document_manager/models.py:20](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L20) |
| `document_manager.models.PorteeNumero` | enum | [01_causes_documents](01_causes_documents.svg) | [document_manager/models.py:276](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L276) |
| `document_manager.models.ReferentHistorique` | model | [02_historique_e01](02_historique_e01.svg) | [document_manager/models.py:349](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L349) |
| `document_manager.models.RoleExtremite` | enum | [02_historique_e01](02_historique_e01.svg) | [document_manager/models.py:649](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L649) |
| `document_manager.models.RoleNiveau` | enum | [01_causes_documents](01_causes_documents.svg) | [document_manager/models.py:255](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L255) |
| `document_manager.models.SchemaNiveaux` | model | [01_causes_documents](01_causes_documents.svg) | [document_manager/models.py:282](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L282) |
| `document_manager.models.Statement` | model | [01_causes_documents](01_causes_documents.svg) | [document_manager/models.py:153](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L153) |
| `document_manager.models.TraitementEditorial` | enum | [02_historique_e01](02_historique_e01.svg) | [document_manager/models.py:535](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L535) |
| `document_manager.models.VersionTexte` | model | [02_historique_e01](02_historique_e01.svg) | [document_manager/models.py:470](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/models.py#L470) |
| `document_manager.numerotation.AmbiguiteOccurrence` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [document_manager/numerotation.py:267](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/numerotation.py#L267) |
| `document_manager.numerotation.NumeroResolu` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [document_manager/numerotation.py:239](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/numerotation.py#L239) |
| `document_manager.protection.ModificationRefusee` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [document_manager/protection.py:44](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/protection.py#L44) |
| `document_manager.protection.SuppressionRefusee` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [document_manager/protection.py:40](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/protection.py#L40) |
| `document_manager.protection._Contexte` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [document_manager/protection.py:51](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/protection.py#L51) |
| `document_manager.protection.metadonnees_autorisees` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [document_manager/protection.py:59](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/protection.py#L59) |
| `document_manager.protection.suppression_autorisee` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [document_manager/protection.py:78](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/protection.py#L78) |
| `document_manager.reprise_numeros.Rapport` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [document_manager/reprise_numeros.py:126](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/reprise_numeros.py#L126) |
| `document_manager.reprise_numeros.RattachementRefuse` | class | [12_classes_services_e01](12_classes_services_e01.svg) | [document_manager/reprise_numeros.py:31](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/document_manager/reprise_numeros.py#L31) |
| `email_manager.models.Email` | model | [06_courriels](06_courriels.svg) | [email_manager/models.py:122](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/email_manager/models.py#L122) |
| `email_manager.models.EmailThread` | model | [06_courriels](06_courriels.svg) | [email_manager/models.py:11](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/email_manager/models.py#L11) |
| `email_manager.models.Quote` | model | [06_courriels](06_courriels.svg) | [email_manager/models.py:245](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/email_manager/models.py#L245) |
| `events.models.Event` | model | [08_photos_evenements](08_photos_evenements.svg) | [events/models.py:9](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/events/models.py#L9) |
| `events.models.SupportingEvidenceLinkedPhotos` | model | [08_photos_evenements](08_photos_evenements.svg) | [events/models.py:189](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/events/models.py#L189) |
| `googlechat_manager.models.ChatMessage` | model | [09_google_chat](09_google_chat.svg) | [googlechat_manager/models.py:28](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/googlechat_manager/models.py#L28) |
| `googlechat_manager.models.ChatParticipant` | model | [09_google_chat](09_google_chat.svg) | [googlechat_manager/models.py:6](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/googlechat_manager/models.py#L6) |
| `googlechat_manager.models.ChatSequence` | model | [09_google_chat](09_google_chat.svg) | [googlechat_manager/models.py:61](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/googlechat_manager/models.py#L61) |
| `googlechat_manager.models.ChatSubject` | model | [09_google_chat](09_google_chat.svg) | [googlechat_manager/models.py:41](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/googlechat_manager/models.py#L41) |
| `googlechat_manager.models.ChatThread` | model | [09_google_chat](09_google_chat.svg) | [googlechat_manager/models.py:21](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/googlechat_manager/models.py#L21) |
| `googlechat_manager.models.SubjectGroup` | model | [09_google_chat](09_google_chat.svg) | [googlechat_manager/models.py:50](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/googlechat_manager/models.py#L50) |
| `pdf_manager.models.PDFDocument` | model | [07_pdf_protagonistes](07_pdf_protagonistes.svg) | [pdf_manager/models.py:28](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/pdf_manager/models.py#L28) |
| `pdf_manager.models.PDFDocumentType` | model | [07_pdf_protagonistes](07_pdf_protagonistes.svg) | [pdf_manager/models.py:13](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/pdf_manager/models.py#L13) |
| `pdf_manager.models.Quote` | model | [07_pdf_protagonistes](07_pdf_protagonistes.svg) | [pdf_manager/models.py:222](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/pdf_manager/models.py#L222) |
| `photos.models.Photo` | model | [08_photos_evenements](08_photos_evenements.svg) | [photos/models.py:37](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/photos/models.py#L37) |
| `photos.models.PhotoDocument` | model | [08_photos_evenements](08_photos_evenements.svg) | [photos/models.py:127](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/photos/models.py#L127) |
| `photos.models.PhotoType` | model | [08_photos_evenements](08_photos_evenements.svg) | [photos/models.py:32](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/photos/models.py#L32) |
| `photos.services.PhotoProcessingService` | class | [13_import_audit_traitement](13_import_audit_traitement.svg) | [photos/services.py:13](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/photos/services.py#L13) |
| `protagonist_manager.models.Protagonist` | model | [07_pdf_protagonistes](07_pdf_protagonistes.svg) | [protagonist_manager/models.py:4](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/protagonist_manager/models.py#L4) |
| `protagonist_manager.models.ProtagonistEmail` | model | [07_pdf_protagonistes](07_pdf_protagonistes.svg) | [protagonist_manager/models.py:43](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/protagonist_manager/models.py#L43) |
| `users.models.CustomUser` | model | [10_utilisateurs_ia](10_utilisateurs_ia.svg) | [users/models.py:4](https://github.com/LPDavidbdeb/court/blob/212a7feee81aef46a5b43d36e8eeafe0f8870064/users/models.py#L4) |

## ai_services.models.GeminiResponse

Bases directes : `django.db.models.Model`.

- `__str__()`.

## ai_services.utils.EvidenceFormatter

Bases directes : aucune explicite.

- `_xml_escape(text)` [staticmethod].
- `format_narrative_context_xml(narrative)` [classmethod].
- `format_police_context_xml(narratives_queryset)` [classmethod].
- `get_label(obj, exhibit_map)` [staticmethod].
- `get_date(obj)` [staticmethod].
- `_get_protagonist_display(protagonist, fallback_name)` [staticmethod].
- `collect_global_evidence(narratives)` [classmethod].
- `format_timeline_item(item, exhibit_label=None)` [classmethod].
- `format_document_reference(obj, exhibit_label=None)` [classmethod].

## argument_manager.mixins.EvidenceDeleteMixin

Bases directes : aucune explicite.

- `form_valid(form)`.
- `get_deleted_message(deleted_narrative_titles)`.

## argument_manager.models.AppuiFait

Bases directes : `django.db.models.Model`.

- `__str__()`.

## argument_manager.models.Axe

Bases directes : `django.db.models.Model`.

- `__str__()`.

## argument_manager.models.Fait

Bases directes : `django.db.models.Model`.

- `__str__()`.
- `numero_plaide(document=None, noeud=None)`.
- Propriété `est_plaide`.

## argument_manager.models.NatureFait

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## argument_manager.models.PerjuryArgument

Bases directes : `django.db.models.Model`.

- `__str__()`.

## argument_manager.models.RattachementAxe

Bases directes : `django.db.models.Model`.

- `__str__()`.

## argument_manager.models.RoleAppui

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## argument_manager.models.TrameNarrative

Bases directes : `django.db.models.Model`, `core.mixins.ChampsEditables`.

- `__str__()`.
- `evidence_totals(pks)` [classmethod].
- `flag_orphans(evidence_items)` [classmethod].
- `is_supported_only_by(evidence)`.
- `get_chronological_evidence()`.
- `get_source_documents()`.
- `get_structured_analysis()`.

## case_manager.cotes_concordance.LockIndisponible

Bases directes : `builtins.Exception`.

Aucune opération ou propriété déclarée directement dans cette classe.

## case_manager.evidence_audit.ReferenceOccurrence

Bases directes : aucune explicite.

- Propriété `canonical_key` : `str`.

## case_manager.models.AISuggestion

Bases directes : `django.db.models.Model`.

- `__str__()`.
- Propriété `suggestion_sec1`.
- Propriété `suggestion_sec2`.
- Propriété `suggestion_sec3`.
- Propriété `suggestion_sec4`.

## case_manager.models.AncrageCitation

Bases directes : `django.db.models.Model`.

- `__str__()`.
- Propriété `resolu`.

## case_manager.models.AppuiDepotJuillet

Bases directes : `django.db.models.Model`.

- `__str__()`.

## case_manager.models.BordereauDepotJuillet

Bases directes : `django.db.models.Model`.

- `__str__()`.
- `pieces_de_la_liasse()`.
- Propriété `est_liasse`.

## case_manager.models.ConfirmationAppui

Bases directes : `django.db.models.Model`.

- `__str__()`.
- `empreinte_portee(portee)` [staticmethod].
- `etat_courant()`.

## case_manager.models.DestinataireInstance

Bases directes : `django.db.models.Model`.

- `__str__()`.
- `est_valide_le(jour)`.

## case_manager.models.EtatAppui

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## case_manager.models.ExhibitRegistry

Bases directes : `django.db.models.Model`.

- `get_label()`.

## case_manager.models.FichierTransmis

Bases directes : `django.db.models.Model`.

- `__str__()`.

## case_manager.models.LegalCase

Bases directes : `django.db.models.Model`.

- `__str__()`.

## case_manager.models.PerjuryContestation

Bases directes : `django.db.models.Model`.

- `__str__()`.

## case_manager.models.ProducedExhibit

Bases directes : `django.db.models.Model`.

- `__str__()`.

## case_manager.models.Transmission

Bases directes : `django.db.models.Model`.

- `__str__()`.
- Propriété `bloquee`.

## case_manager.piece_file_audit.AuditIssue

Bases directes : aucune explicite.

Aucune opération ou propriété déclarée directement dans cette classe.

## cause_manager.models.Cause

Bases directes : `django.db.models.Model`.

- `__str__()`.
- `get_absolute_url()`.
- `get_statut_display()`.
- `consigner_etat(statut, *, date_effet=None, motif='')`.
- Propriété `etat_actuel`.
- Propriété `statut`.

## cause_manager.models.EtatCause

Bases directes : `django.db.models.Model`.

- `__str__()`.

## cause_manager.models.LienCause

Bases directes : `django.db.models.Model`.

- `__str__()`.

## cause_manager.models.StatutCause

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## core.mixins.ChampsEditables

Bases directes : aucune explicite.

Aucune opération ou propriété déclarée directement dans cette classe.

## core.mixins.ExhibitableMixin

Bases directes : aucune explicite.

- `get_exhibit_date()`.
- `get_exhibit_title()`.
- `get_exhibit_type()`.
- `get_exhibit_parties()`.
- `get_exhibit_description()`.
- `get_exhibit_public_url()`.

## core.piece_import.Adaptateur

Bases directes : aucune explicite.

- `correspond(nom_fichier)`.
- `objet(correspondance, pour_import=False)`.

## core.quote_regime.HeriteQuoteManager

Bases directes : `django.db.models.Manager`.

- `get_queryset()`.

## core.quote_regime.PhraseQuoteManager

Bases directes : `django.db.models.Manager`.

- `get_queryset()`.

## core.quote_regime.QuoteRegime

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.export_concordance.ExportStrictRefuse

Bases directes : `builtins.Exception`.

- `__init__(verdicts_manquants)`.

## document_manager.export_concordance.Verdict

Bases directes : aucune explicite.

- `__init__(code, satisfait, motifs=None)`.
- `as_dict()`.

## document_manager.models.Correspondance

Bases directes : `django.db.models.Model`.

- `__str__()`.
- `noeuds_source()`.
- `noeuds_cible()`.
- `versions_courantes_examinees()`.
- `etat_courant()`.
- Propriété `est_scission`.
- Propriété `est_fusion`.

## document_manager.models.Document

Bases directes : `django.db.models.Model`, `core.mixins.ExhibitableMixin`.

- `get_absolute_url()`.
- `get_public_url()`.
- `__str__()`.
- `get_exhibit_date()`.
- `get_exhibit_title()`.
- `get_exhibit_type()`.
- `get_exhibit_parties()`.
- `get_exhibit_description()`.

## document_manager.models.DocumentSource

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.models.EtatConfirmation

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.models.ExtremiteCorrespondance

Bases directes : `django.db.models.Model`.

- `__str__()`.

## document_manager.models.FormatNumero

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.models.InstantaneNoeud

Bases directes : `django.db.models.Model`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.models.InstantaneReferent

Bases directes : `django.db.models.Model`.

- `__str__()`.

## document_manager.models.LibraryNode

Bases directes : `treebeard.mp_tree.MP_Node`.

- `__str__()`.

## document_manager.models.Niveau

Bases directes : `django.db.models.Model`.

- `__str__()`.

## document_manager.models.NoeudArchive

Bases directes : `django.db.models.Model`.

- `__str__()`.

## document_manager.models.NumberingMode

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.models.PorteeNumero

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.models.ReferentHistorique

Bases directes : `django.db.models.Model`.

- `__str__()`.

## document_manager.models.RoleExtremite

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.models.RoleNiveau

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.models.SchemaNiveaux

Bases directes : `django.db.models.Model`.

- `__str__()`.
- `niveau(profondeur)`.
- `profondeur_du_role(role)`.

## document_manager.models.Statement

Bases directes : `django.db.models.Model`.

- `save(*args, **kwargs)`.
- `__str__()`.

## document_manager.models.TraitementEditorial

Bases directes : `django.db.models.TextChoices`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.models.VersionTexte

Bases directes : `django.db.models.Model`.

- `__str__()`.
- `empreinte_de(texte)` [staticmethod].
- `capter(statement, motif='')` [classmethod].
- Propriété `est_courante`.

## document_manager.numerotation.AmbiguiteOccurrence

Bases directes : `builtins.Exception`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.numerotation.NumeroResolu

Bases directes : aucune explicite.

- `__init__(noeud, genre, numero, origine, manquant, calcule)`.
- `__repr__()`.
- Propriété `pk`.

## document_manager.protection.ModificationRefusee

Bases directes : `django.core.exceptions.PermissionDenied`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.protection.SuppressionRefusee

Bases directes : `django.core.exceptions.PermissionDenied`.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.protection._Contexte

Bases directes : aucune explicite.

Aucune opération ou propriété déclarée directement dans cette classe.

## document_manager.protection.metadonnees_autorisees

Bases directes : aucune explicite.

- `__enter__()`.
- `__exit__(*a)`.

## document_manager.protection.suppression_autorisee

Bases directes : aucune explicite.

- `__init__(noeud_pk)`.
- `__enter__()`.
- `__exit__(*a)`.

## document_manager.reprise_numeros.Rapport

Bases directes : aucune explicite.

- `__init__()`.
- `resume()`.
- Propriété `conforme`.

## document_manager.reprise_numeros.RattachementRefuse

Bases directes : `builtins.Exception`.

Aucune opération ou propriété déclarée directement dans cette classe.

## email_manager.models.Email

Bases directes : `django.db.models.Model`, `core.mixins.ExhibitableMixin`, `core.mixins.ChampsEditables`.

- `get_absolute_url()`.
- `get_public_url()`.
- `__str__()`.
- `get_exhibit_date()`.
- `get_exhibit_title()`.
- `get_exhibit_type()`.
- `get_exhibit_parties()`.
- `get_exhibit_description()`.
- Propriété `eml_filename`.

## email_manager.models.EmailThread

Bases directes : `django.db.models.Model`, `core.mixins.ExhibitableMixin`, `core.mixins.ChampsEditables`.

- `__str__()`.
- `get_exhibit_date()`.
- `get_exhibit_title()`.
- `get_exhibit_type()`.
- `get_exhibit_parties()`.
- `get_exhibit_description()`.
- `get_absolute_url()`.
- `get_public_url()`.

## email_manager.models.Quote

Bases directes : `django.db.models.Model`, `core.mixins.ChampsEditables`.

- `get_absolute_url()`.
- `__str__()`.
- Propriété `source_text`.
- Propriété `position_in_source`.
- Propriété `full_sentence`.

## events.models.Event

Bases directes : `django.db.models.Model`, `core.mixins.ExhibitableMixin`.

- `get_exhibit_date()`.
- `get_exhibit_title()`.
- `get_exhibit_type()`.
- `get_exhibit_description()`.
- `synchroniser_bornes(forcer=False)`.
- `libelle_horodate()`.
- `description_horodatee()`.
- `get_absolute_url()`.
- `get_public_url()`.
- `get_display_id()`.
- `__str__()`.
- Propriété `empan_photographique`.

## events.models.SupportingEvidenceLinkedPhotos

Bases directes : `django.db.models.Model`.

Aucune opération ou propriété déclarée directement dans cette classe.

## googlechat_manager.models.ChatMessage

Bases directes : `django.db.models.Model`.

- `__str__()`.

## googlechat_manager.models.ChatParticipant

Bases directes : `django.db.models.Model`.

- `__str__()`.

## googlechat_manager.models.ChatSequence

Bases directes : `django.db.models.Model`.

- `update_dates()`.
- `__str__()`.
- `get_absolute_url()`.
- `get_public_url()`.

## googlechat_manager.models.ChatSubject

Bases directes : `django.db.models.Model`.

- `__str__()`.

## googlechat_manager.models.ChatThread

Bases directes : `django.db.models.Model`.

- `__str__()`.

## googlechat_manager.models.SubjectGroup

Bases directes : `django.db.models.Model`.

- `save(*args, **kwargs)`.

## pdf_manager.models.PDFDocument

Bases directes : `django.db.models.Model`, `core.mixins.ExhibitableMixin`, `core.mixins.ChampsEditables`.

- `__str__()`.
- `get_absolute_url()`.
- `get_public_url()`.
- `transcription_pages()`.
- `has_text_layer(min_chars=200)`.
- `get_exhibit_date()`.
- `get_exhibit_title()`.
- `get_exhibit_type()`.
- `get_exhibit_parties()`.
- `get_exhibit_description()`.
- Propriété `transcription`.

## pdf_manager.models.PDFDocumentType

Bases directes : `django.db.models.Model`.

- `__str__()`.

## pdf_manager.models.Quote

Bases directes : `django.db.models.Model`, `core.mixins.ChampsEditables`.

- `get_absolute_url()`.
- `__str__()`.
- Propriété `source_text`.
- Propriété `position_in_source`.
- Propriété `full_sentence`.

## photos.models.Photo

Bases directes : `django.db.models.Model`, `core.mixins.ExhibitableMixin`.

- `__str__()`.
- `get_absolute_url()`.
- `get_exhibit_date()`.
- `get_exhibit_title()`.
- `get_exhibit_type()`.
- `get_exhibit_description()`.

## photos.models.PhotoDocument

Bases directes : `django.db.models.Model`, `core.mixins.ExhibitableMixin`, `core.mixins.ChampsEditables`.

- `get_exhibit_date()`.
- `get_exhibit_title()`.
- `get_exhibit_type()`.
- `get_exhibit_parties()`.
- `get_exhibit_description()`.
- `__str__()`.
- `get_absolute_url()`.
- `get_public_url()`.

## photos.models.PhotoType

Bases directes : `django.db.models.Model`.

- `__str__()`.

## photos.services.PhotoProcessingService

Bases directes : aucune explicite.

- `__init__()`.
- `create_photo_from_upload(uploaded_file, photo_type=None, artist=None, datetime_original=None, gps_latitude=None, gps_longitude=None, custom_file_name=None)`.
- `_parse_date(tags)`.
- `_to_float(val)`.
- `_to_int(val)`.
- `create_and_process_photo(source_path: str, datetime_original: datetime, photo_type=None)`.
- `process_photo_file(source_path: str, date_from_folder=None, photo_type=None)`.

## protagonist_manager.models.Protagonist

Bases directes : `django.db.models.Model`.

- `__str__()`.
- `get_full_name()`.
- `get_full_name_with_role()`.
- `get_absolute_url()`.

## protagonist_manager.models.ProtagonistEmail

Bases directes : `django.db.models.Model`.

- `__str__()`.

## users.models.CustomUser

Bases directes : `django.contrib.auth.models.AbstractUser`.

- `__str__()`.

Publication du 21 octobre 2026 : liens de code fixés au socle P6 annoncé, sans changement des classes ou opérations décrites. [Copie originale](../../../architecture_c/historique/2026-10-21_publication/README.md).
