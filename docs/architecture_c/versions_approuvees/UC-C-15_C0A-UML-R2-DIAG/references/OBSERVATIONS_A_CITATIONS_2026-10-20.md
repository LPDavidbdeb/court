# Source de la revue — observations A sur les citations

Copie documentaire des sections B.3/B.4, sans modification du texte de A.
Source locale lue : `docs/agent_a/PREPARATION_CHANTIER_C_2026-10-20.md`.
SHA-256 du rapport complet : `dd9d84488ac35486fd5f77c7187ffa160ca544f8f15b3b5a3781abfb3bde1d65`.
Date de copie : 20 octobre 2026. L’extrait ne vaut ni essai effectué par B,
ni audit de la base actuelle; ses mentions de données et essais sont celles
du rapport de A. Le fichier source, ses contrôles et ses ressources ne sont
pas modifiés. L’analyse B distingue explicitement faits lus et propositions.

---

### B.3 Changement A : l'édition d'un nœud portant une citation

**Point d'entrée.** `POST /documents/ajax/produced/edit-node/<node_pk>/`, soit
`document_manager.views.produced_views.ajax_edit_node`, décorée `@transaction.atomic`. Elle reçoit
`NodeForm` : `item` obligatoire, `text` facultatif.

**À P6 et au socle actuel [code].** Avec un formulaire valide :
1. le titre (`item`) est enregistré ;
2. le contenu suit l'une de deux branches :
   - si le contenu a un attribut `text`, le texte est réécrit en place ;
   - sinon, un nouveau `Statement(text=…, is_user_created=True)` remplace la clé générique du nœud.

Une `Quote` n'a pas d'attribut `text` (elle porte `quote_text`) : elle prend donc toujours la seconde
branche. **La citation disparaît du nœud**, même pour un simple changement de titre et même avec un texte
vide. La ligne de citation elle-même reste intacte.

Exception : dans le référent historique, la garde `pre_save` E01 de `LibraryNode` refusait déjà.

**Avec C0-A [code, lignes du patch sur `ajax_edit_node`].** Pour un POST au formulaire valide :

| Ordre | Condition | Effet |
|---|---|---|
| 1 | document du nœud `REPRODUCED` (`est_reproduit`) ou référent historique (`est_referent`) | `ModificationRefusee`, **403**, quel que soit le contenu |
| 2 | contenu = `Statement` | `concordance.detacher_pour_edition(noeud, text)` |
| 3 | nœud vide (`content_type_id` et `object_id` tous deux nuls) | nouveau `Statement` |
| 4 | **tout autre cas** | `ModificationRefusee("Cette occurrence ne porte pas un Statement rédactionnel.")`, **403** |
| — | le titre n'est enregistré qu'après l'étape du contenu | un refus laisse aussi le titre intact (transaction annulée) |

Les cas inchangés : nœud inexistant (404), `GET` (rend `item` et `text`, ce dernier vide pour une
citation), formulaire invalide (400).

**Portée du refus.** Le cas 4 vise **tous les nœuds portant une citation** :
- citations de courriel ou de PDF, quel que soit leur régime (`HERITE` ou `PHRASE`) ;
- dans **tout** document ;
- pour **toute** demande valide, y compris un simple changement de titre.

Il vise aussi les nœuds portant un `Event`, une `TrameNarrative` ou un `PhotoDocument`, une clé
générique incomplète, ou une clé dont la cible n'existe plus.

**Exposition dans l'interface [code, non éprouvé dans un navigateur].**
- L'éditeur n'offre pas l'édition en place d'une citation affichée : les gabarits
  `content_types/*_quote_edit.html` n'ont pas la classe `.editable-item`.
- La route n'est donc atteinte, pour un nœud-citation, que de deux façons :
  - par un POST direct ;
  - par un nœud dont le contenu ne se résout pas dans `_get_and_process_tree` (citation absente,
    filtrée ou supprimée). Ce nœud s'affiche alors « Click to add content… » et devient éditable.
- La réponse 403 est celle de Django pour `PermissionDenied` : une page HTML, sans JSON, puisque
  `mysite/urls.py` ne déclare pas de `handler403`.
- Le client (`produced/_js.html`, `saveAndDestroyEditor`) appelle `response.json()` : l'échec ne finit
  qu'en `console.error`, sans alerte. **L'utilisateur ne verrait pas le refus.** Cela concerne le
  comportement de l'interface, pas la règle elle-même.

**Tests existants.**
- **Aucun test au socle ne passe par la route d'édition.**
- Les 5 tests HTTP d'édition de C0-A (`C0AEditionEtConservation`) couvrent :
  - le détachement d'un `Statement` partagé (200) ;
  - le refus du référent (403) ;
  - le refus d'un document REPRODUCED, y compris le simple renommage (403) ;
  - l'annulation après un refus simulé (403).
- **Aucun ne couvre le cas 4** (contenu qui n'est pas un `Statement`, notamment une citation).
- Le test `test_un_identifiant_generique_ne_declenche_pas_la_purge_dun_statement` porte un `Event`, mais
  sur la suppression. Le refus d'édition d'un nœud-citation n'est donc **pas éprouvé**.

### B.4 Changement B : les concordances « à réexaminer »

**État courant [code, inchangé par C0-A].** `Correspondance.etat_courant()` rend `A_REEXAMINER` quand
deux conditions sont réunies : l'état enregistré est `CONFIRME`, et `versions_courantes_examinees()` est
faux. Sinon, il rend l'état enregistré.
- L'état enregistré n'est jamais réécrit.
- `A_ETABLIR` reste `A_ETABLIR`.

**`versions_courantes_examinees()` à P6 [code].** La méthode vérifie seulement que chaque `VersionTexte`
captée est encore courante : son empreinte doit égaler le SHA-256 du texte actuel de son `Statement`.
Elle ne lit pas les extrémités.

**`versions_courantes_examinees()` avec C0-A [code, patch sur `document_manager/models.py`].** Pour chaque
côté (SOURCE, CIBLE), pour chaque extrémité :

| Situation de l'extrémité | Résultat |
|---|---|
| `noeud` nul (occurrence supprimée, extrémité archivée) | **faux** |
| nœud appartenant à un autre document que celui déclaré pour ce côté | **faux** |
| nœud vide (`content_type` et `object_id` nuls) | ignoré |
| contenu qui n'est pas un `Statement` : **citation**, `Event`, cible disparue… | **faux** |
| `Statement` | le couple (PK, SHA-256 de son texte actuel) est ajouté à l'ensemble actuel |

La méthode est ensuite fausse dans deux cas :
- l'ensemble actuel diffère de l'ensemble des captures (`versions_*_examinees`) ;
- aucune extrémité ne porte de texte (`contient_texte`).

**La règle pour une citation.** Une concordance `CONFIRME` dont **au moins une extrémité porte une
citation** est calculée `A_REEXAMINER` dès que C0-A est en place.
- Le contenu, le régime et la certification de la citation n'y changent rien.
- **Reconfirmer ne la rétablit pas** [non éprouvé]. `confirmer_traitement`, que C0-A ne modifie pas, ne
  capte que les `Statement` et passe les citations sous silence. L'extrémité-citation refait donc
  échouer le contrôle. La concordance reste à réexaminer tant que l'extrémité porte une citation.
- À P6, la même concordance restait `CONFIRME` : le côté citation n'était ni capté ni contrôlé.

**Règle voisine pour les appuis [code].** Avec C0-A, `ConfirmationAppui.etat_courant()` (case_manager)
rend `A_REEXAMINER` dès que le nœud ne porte pas un `Statement` (citation comprise), si l'état enregistré
est `CONFIRME` ou `SANS_APPUI`.

**Où ces règles se manifestent [code].**
- Ni vue ni URL ne crée, ne confirme ou n'affiche ces états.
- `relier()` accepte des nœuds de tout type. Il n'est appelé, comme `confirmer_traitement()`, que par
  `manage.py demonstration_e01` et par les tests.
- `ConfirmationAppui` n'est créée que par `demonstration_e01` et par les tests.
- L'état courant est lu par l'export `manage.py exporter_concordance` (`export_concordance.py`) et par
  la démonstration.

Le nombre de concordances réelles concernées n'est pas mesuré : cette mesure est reportée à la revue de
C0-A (mandat complémentaire, § 5).

**Ce que cette règle n'est pas : l'invalidation des empreintes PHRASE.**

| | Concordance « à réexaminer » (E01 / C0-A) | Certification PHRASE ineffective (fournisseur) |
|---|---|---|
| Objet | `Correspondance`, `ConfirmationAppui` (document_manager, case_manager) | `email_manager.Quote`, `pdf_manager.Quote` au régime `PHRASE` |
| Ce qui est comparé | l'identité des `Statement` et `VersionTexte.empreinte` (SHA-256 de `Statement.text`), captées à la confirmation | `source_text_sha256`, `anchored_text_sha256`, `certified_text_sha256` |
| Rôle d'une citation | son **type** seul : une extrémité qui n'est pas un `Statement` | la mutation de **sa** source, de ses bornes ou de son texte certifié |
| Lit le contenu de la citation | non | oui |
| État enregistré modifié | non, calcul à la lecture | non, calcul à la lecture |
| Retour à l'état valide | aucun par reconfirmation tant que l'extrémité porte une citation [non éprouvé] | aucun réancrage ; il faut une nouvelle citation |

Aucune des deux règles ne lit l'autre :
- une PHRASE effectivement certifiée laisserait une concordance à réexaminer, si un nœud la portait
  (aucun ne la porte) ;
- l'invalidation d'une PHRASE n'atteint aucune concordance.

---

Fin de l’extrait exact de A. [Analyse et propositions B](../ANALYSE_CIBLEE_CITATIONS_C0A.md).
