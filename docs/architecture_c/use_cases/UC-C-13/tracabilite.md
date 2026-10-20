# UC-C-13 — Traçabilité TRANS-04, révision Statement

**C0A-UML-R2-ST — sous-cas C0A_ISOLER.** Tous les scénarios applicatifs sont
**NON EXECUTES**. Seuls les contrôles documentaires et de compilation sont
réalisés. AC02/AC03 seuls sont reformulés; les six autres critères, les 38
scénarios NR/CF3 et les méthodes du patch ne sont pas effacés.

| Source / invariant | AC | Activité | Séquence | ERD | Classes | Scénarios et portée |
|---|---|---|---|---|---|---|
| ST01/ST05, NR01/11 | AC01 | ACT-REFUS | SEQ-GARDE | Document.source_type; ReferentHistorique.document_id | CLS-GARDE | ST:T01; tests du patch test_http_referent_refuse_sans_effet_partiel et test_http_reproduced_refuse_aussi_le_simple_renommage; pas de garantie globale de toutes les entrées en C0-A |
| ST02/ST03, NR03/11 | AC02 | ACT-CAP/PRIVE/ASSOC | SEQ-AVANT/COPIE/ASSOC/APRES | ERD-ORIG; LibraryNode.object_id; VersionTexte | CLS-PRIVE/CAP/ASSOC | ST:T02; partage entre PRODUCED conservé comme contre-épreuve adverse, pas droit de créer ce partage |
| ST04/ST05, sécurité locale | AC03 | ACT-PRIVE; aucune branche d’écriture en place | SEQ-COPIE et note aucun UPDATE de l’ancien | ERD-ORIG, preuves persistantes absentes en C0-A | CLS-PRIVE; note L1-A | ST:T03/T08 pour le profil; ST:T09/T12 pour propriété persistante et chemin direct hors C0-A. L’ancien test_edition_privee_capture_le_texte_avant_modification ne prouve pas cette nouvelle garantie |
| Texte distinct de item | AC04 | ACT-NOOP/NEUF/ITEM | SEQ-NOOP/NEUF/ITEM | ERD-ITEM; LibraryNode.item/content_type_id/object_id | CLS-ITEM/EDIT | ST:T04; test_sauvegarde_identique_ne_detache_pas_le_statement conservé; contexte sémantique ST:T11 séparé |
| Fraîcheur d’appui, NR03/TR02 | AC05 | ACT-FRESH | SEQ-FRESH | ConfirmationAppui.version_examinee_id; VersionTexte.statement_id/empreinte | CLS-FRESH | ST:T05; test_meme_texte_autre_statement_invalide_meme_un_noeud_deja_charge, réexamen SANS_APPUI; décisions/textes antérieurs intacts |
| Fraîcheur éditoriale | AC06 | ACT-FRESH | SEQ-FRESH | Correspondance M2M SOURCE/CIBLE; ExtremiteCorrespondance.noeud_id/role | Correspondance.versions_courantes_examinees | ST:T05; identité/empreinte source et cible; manifeste complet et item sémantique différés L1-A/C0-B |
| Atomicité, NR11 | AC07 | ACT-TX/ROLLBACK | SEQ-ROLLBACK | Identités LibraryNode/Statement/VersionTexte restaurées; atomicité portée par séquence | CLS-EDIT/CAP/ASSOC | ST:T06; test_refus_apres_detachement_annule_aussi_les_nouveaux_objets; pas de nouvel objet orphelin après refus |
| CF3-26 et fournisseur A | AC08 | ACT-REFUS | branche autre type / GFK incohérente | ContentType + GFK typée; pas de Quote assimilée à Statement | CLS-GARDE | ST:T07; suites E01 et régime A inchangées; aucun champ/migration C0-A ajouté |

## Scénarios supplémentaires identifiés

| ID | Construction et résultat attendu | Lot / exécution |
|---|---|---|
| ST:T01 | Tenter texte puis item sur REPRODUCED et référent PRODUCED : refus sans mutation. Ne pas convertir le référent en REPRODUCED. | C0-A local; toutes entrées L1-A/L5; NON EXECUTE |
| ST:T02 | Origine REPRODUCED attestée, deux usages PRODUCED : éditer un usage crée un objet neuf; original et autre usage inchangés, captures disponibles. | C0-A profil; NON EXECUTE |
| ST:T03 | Un seul usage observé en PRODUCED : changement réel de texte crée un objet neuf dans C0A_ISOLER, sans écrire sur l’ancien. La cardinalité ne prouve pas la propriété. | C0-A; NON EXECUTE |
| ST:T04 | Texte identique puis item seul : identité/captures inchangées. Premier texte sur une occurrence vide : nouvel objet privé. | C0-A; NON EXECUTE |
| ST:T05 | Changement de texte ou autre Statement au même texte : réexamen si identité/contenu divergent, décisions et textes antérieurs conservés. | C0-A, compléments L1-A/C0-B; NON EXECUTE |
| ST:T06 | Échec après création/repointage, puis à la sauvegarde de item : rollback de tout l’ensemble. | C0-A; NON EXECUTE |
| ST:T07 | PK homonyme Quote HERITE ou PHRASE : refus comme Statement d’édition; aucun changement du régime A. | C0-A; NON EXECUTE |
| ST:T08 | Attacher N2 à l’ancien S après le dernier contrôle T1. Dans R2, T1 crée S2 sans écrire S : N2 garde l’ancien texte. Cet attachement reste interdit et à empêcher séparément. | C0-A sécurité locale, L1-A ST04; test PostgreSQL à mandater, NON EXECUTE |
| ST:T09 | Deuxième propriétaire privé, rattachement après retrait du propriétaire, allocation concurrente à deux occurrences : refus L1-A; pas d’attribution libérée par SET_NULL. | L1-A, impacts UC14/C0-B; NON EXECUTE |
| ST:T10 | Reprise PRODUCED à texte identique : nouveau Statement, filiation conservée, aucun appui reconfirmé par hash/partage. Origine REPRODUCED attestée : réutilisation admissible et source inchangée. | UC02/07, L1-B/L2; NON EXECUTE |
| ST:T11 | item renommé vs item devenant C-… ou vide : observer genre/numérotation, sans détachement. C0-A ne prétend pas périmer l’examen de contexte; L1-A/C0-B devront le faire si son sens change. | UC02/05E/12, L1-A/C0-B; NON EXECUTE |
| ST:T12 | Historiques de création distincts mais usages identiques : ne pas inventer l’origine. Changer is_user_created ou le type du Document ne blanchit pas une provenance une fois attribuée. | L1-A; audit historique distinct, NON EXECUTE |

Les fixtures anciennes de partage privé PRODUCED sont conservées comme
contre-épreuves de données incompatibles, sans création de ces associations
dans les parcours autorisés. Leur succès P6 ne prouve pas l’interdiction de
rattachement ni la propriété persistante.

[C0A-REV-01 / UC15](../UC-C-15/specification.md) reste distincte et ouverte.


## Décision et traçabilité de version

Le 20 octobre 2026, l’utilisateur approuve uniquement UC-C-13::C0A_ISOLER
C0A-UML-R2-ST au commit de fusion cd584c3 (PR #30).
[Décision exacte](approbation.json) et [dossier contractuel préservé](../../versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md).
Scénarios et critères ci-dessus inchangés; NON EXECUTES demeure applicable.
Aucune approbation des mécanismes futurs ST:T09/T12, de L1-A ou de UC14/15.
