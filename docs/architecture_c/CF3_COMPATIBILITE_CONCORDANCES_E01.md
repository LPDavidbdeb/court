# CF3 — Compatibilité de la reprise partielle avec les concordances E01

Addendum de l’Agent B — 19 octobre 2026. Statut : **recommandation technique soumise à approbation, sans autorisation d’implémentation**.

**Conclusion de conception : réutiliser `Correspondance` et `ExtremiteCorrespondance` avec une qualification persistante de leur nature et un examen correctement rattaché aux occurrences.** Leur structure N:M convient aux trois opérations demandées. En revanche, les consommateurs historiques ne peuvent pas accueillir CF3 tels quels : certains assimilent tous les antécédents aux appuis de juillet, les exports exigent une comparaison exhaustive et le réexamen peut manquer un détachement de texte.

Périmètre constaté : dépôt principal en lecture seule au commit `14f7533650d2a28832698b2222ced1df1cd89bb1` (`epic/E01-numerotation-concordance`). Lecture comparative de `integration/quote-regime-step1` au commit `212a7feee81aef46a5b43d36e8eeafe0f8870064`. L’addendum antérieur est préservé sur `docs/agent-b-pont-probatoire-20261019`, commit `06fe44c1a7e8582792f9d1fcfcba8155046168ee`. Aucun changement de branche, index, code, migration, base, serveur ou fichier du dépôt. Aucun test Django exécuté. Les résultats ci-dessous sont des constats de lecture statique et des exigences de vérification future, pas une certification d’exécution.

Sources de continuité lues : `AGENTS.md`, `PROJECT_CONTEXT.md`, `legal/METHODOLOGIE_POST_DEPOT.md`. Le dépôt judiciaire de juillet est un acte papier; son archive est intouchable. Ce travail ne modifie aucune politique de cotes ni aucun état procédural. Les critères E01 cités décrivent le contrat technique de cette branche; ils n’accordent aucune approbation supplémentaire à D05 ou aux autres décisions en attente.

Rapports de conception utilisés : l’addendum de neuf livrables conservé au commit `06fe44c` et [Validation fonctionnelle de l’architecture C](./VALIDATION_FONCTIONNELLE_ARCHITECTURE_C.md), notamment CF1–CF4 et VF02/VF03/VF04/VF05/VF08. Les noms `Acte`, `VersionActe`, `UtilisationPreuve`, `SelectionPreuve`, `LienRedactionnel`, `CompositionCitation` et `InsertionRendu` restent des éléments proposés de C; ils ne sont pas implémentés dans le code Python examiné.

## 1. Inventaire des modèles et consommateurs existants

### 1.1 Modèles, contraintes et limites effectives

Toutes les références de ligne portent sur `14f7533`. Le fichier des modèles est identique sur la branche d’intégration comparée.

| Élément | Contrat effectivement porté par le code | Limite pour CF3 |
|---|---|---|
| [Document, source et numérotation](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/models.py:41) | `source_type`, `numbering_mode`, `schema` et métadonnées propres au document. `AUTO` et `STORED` sont indépendants de `PRODUCED`/`REPRODUCED`. | Aucun `Acte`/`VersionActe` ne permet aujourd’hui de prouver que deux Documents sont des versions du même acte. Le titre n’est pas une identité de version. |
| [LibraryNode](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/models.py:176) | Occurrence avec PK propre, appartenance à un Document, arbre Treebeard et contenu générique. Le numéro conservé appartient à l’occurrence. | Le contenu générique ne garantit pas qu’il s’agit d’un Statement. Les groupes et sources doivent être distingués à la validation. |
| [VersionTexte](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/models.py:470) | Texte capturé et SHA-256, unicité `(statement, empreinte)`. `capter()` réutilise une capture identique. | `statement` est en `CASCADE`; une capture n’est pas intrinsèquement immuable. `est_courante` compare la capture à **son Statement**, pas au Statement actuellement porté par une occurrence. |
| [Correspondance](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/models.py:552) | Un couple `document_source` / `document_cible`, un traitement principal, `deplace`, état, motif et date, deux ensembles M2M de textes examinés. Source `PROTECT`, cible `CASCADE`. | « Deux versions d’un même acte » est le contrat exprimé par la docstring et les aides, pas une contrainte relationnelle vérifiable en base. Aucun discriminant A/B/C. Aucune contrainte d’inégalité des Documents ni `clean()` spécifique. |
| [TraitementEditorial et EtatConfirmation](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/models.py:535) | `CONSERVE`, `DEPLACE`, `REFORMULE`, `SCINDE`, `FUSIONNE`, `AJOUT`, `RETRAIT`, `A_ETABLIR`; état distinct `A_ETABLIR`/`CONFIRME`/`A_REEXAMINER`. | Ces catégories qualifient une transformation, pas la nature historique ou interdocumentaire de la relation. |
| [ExtremiteCorrespondance](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/models.py:654) | Rôle SOURCE/CIBLE, FK vers occurrence `PROTECT`, FK vers archive `SET_NULL`, ordre. Unique `(correspondance, role, noeud)`. | Pas de contrôle SQL « occurrence vivante XOR archive ». Pas de contrôle modèle de l’appartenance au bon côté. Les rôles sont des `choices`, pas un contrôle SQL explicite; les écritures ORM directes ne passent pas par la validation du service. |
| [NoeudArchive](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/models.py:692) | Document, ancien PK, position, texte au retrait, empreinte et motif. Document en `CASCADE`. | Ni les anciennes confirmations ni tous leurs textes examinés ne sont recopiés dans l’archive. Le ContentType de l’ancien contenu générique n’est pas conservé : `statement_pk` reçoit object_id sans qualification. Supprimer le Document peut détruire les archives; supprimer une archive peut laisser une extrémité vide. |
| [ReferentHistorique et instantanés](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/models.py:349) | Statut historique indépendant du type de source; captures d’occurrences et contrôles de dérive. | Ce dispositif ne constitue pas le gel complet d’une VersionActe de C. Il ne conserve pas le contrat complet CF3, les UP, les compositions ou les liens proposés. |
| [ConfirmationAppui](/Users/Louis-Philippe/Documents/GitHub/court/case_manager/models.py:572) | Confirmation probatoire par occurrence, source et portée, distincte de Correspondance. `issu_de` historique est informatif. | La vérification de fraîcheur reprend le défaut `VersionTexte.est_courante`; une capture absente n’est pas systématiquement refusée. Ce modèle historique n’est pas converti automatiquement en UP. |
| [AncrageCitation](/Users/Louis-Philippe/Documents/GitHub/court/case_manager/models.py:684) | Occurrence, source, coordonnées, texte de cote, version textuelle facultative, caractère littéral. | Le rendu actuel ne vérifie pas le rattachement de `version_texte` à l’occurrence; il contrôle surtout la sous-chaîne aux coordonnées. Ne pas l’assimiler à la validation complète d’InsertionRendu proposée. |

La migration [0016](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/migrations/0016_document_numbering_mode_librarynode_paragraph_number_and_more.py:1) confirme ces relations et l’unicité des extrémités. Elle n’ajoute pas d’identité d’acte commune ou de séparation entre A, B et C. Les conventions exposées ci-dessus ne sont donc pas des interdictions de schéma empêchant la réutilisation; leurs effets dans les services restent néanmoins réels.

### 1.2 Services qui lisent ou modifient directement la filiation

| Consommateur | Fonctionnement actuel et dépendance à corriger |
|---|---|
| [`concordance.relier()`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/concordance.py:45) | Transaction atomique; refuse le groupe vide et vérifie le Document de chaque occurrence selon son côté. Crée le groupe et les extrémités ordonnées. N’exige ni même acte, ni référent, ni traitement compatible avec les cardinalités. N’impose pas le motif d’un ajout/retrait. Une liste comportant deux fois la même occurrence échoue sur l’unicité. |
| [`confirmer_traitement()`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/concordance.py:83) | Écrit traitement/état/date; efface puis remplit les deux ensembles de VersionTexte pour les extrémités vivantes portant un Statement. Ignore les autres contenus et les archives. Pas de verrou de lecture explicite ni de garde de gel de la correspondance. Une reconfirmation remplace les associations de l’examen précédent sur cette ligne : ce n’est pas un journal complet de toutes les décisions. |
| [`correspondances_de()` / `antecedents_de()`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/concordance.py:114) | Recherche par occurrence et rôle, puis rassemble les sources. Aucun filtre de nature ni de couple de Documents. `noeuds_source()` peut rendre `None` après archivage; les lecteurs doivent en tenir compte. |
| [`appuis_dorigine()`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/concordance.py:132) | Parcourt tous ces antécédents; filtre AppuiDepotJuillet sur `statement_id=ant.object_id`; étiquette systématiquement les résultats « appui du dépôt de juillet ». Ne qualifie pas le ContentType avant d’utiliser object_id comme Statement.pk. |
| [`detacher_pour_edition()`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/concordance.py:164) | Détache le Statement si partagé/protégé; sinon réécrit le Statement en place. Capture le texte après édition, mais **ne capture pas systématiquement l’ancien texte dans la branche non partagée**. Protège les occurrences source partagées si ce service est appelé. Ne garantit pas à lui seul le réexamen correct des confirmations ni le gel C. |
| [`supprimer_occurrence()` / `historique_de()`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/concordance.py:212) | Vérifie le bloc, refuse REPRODUCED/référent, archive, remplace toutes ses extrémités par les archives, supprime les occurrences puis certains Statements inutilisés. Ne distingue aucun propriétaire de gel de la relation; ne vérifie pas les M2M d’examens avant de supprimer un Statement. `historique_de` restitue les archives du Document. |
| [Méthodes de Correspondance](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/models.py:612) | Nœuds des deux côtés; détection 1:N/N:1 par compte des extrémités; `versions_courantes_examinees()` et `etat_courant()`. Les ensembles de versions ne gardent pas la carte des occurrences effectivement examinées. |

### 1.3 Exports, commandes, vues et autres consommateurs

| Famille | Inventaire vérifié |
|---|---|
| Export E01 | [`export_concordance.construire()`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/export_concordance.py:203) filtre déjà les groupes par couple de Documents. `_ex02` fait de même, mais exige une décision pour **tous** leurs paragraphes. `_ligne()` appelle ensuite `appuis_dorigine(nc)` sans transmettre ce périmètre : une autre relation entrante peut contaminer les appuis historiques de la ligne. La restitution déroule les couples SOURCE × CIBLE du groupe, conserve son ID, puis ajoute les occurrences non couvertes « à établir ». |
| Contrôles E01 | Dans le même module : EX01 exige un référent protégé et contrôlé; EX02 la couverture complète et les examens courants; EX03 les numéros; EX04 les citations et le lock; EX05 ConfirmationAppui sur la cible; EX06 archives/orphelins; EX07 état de cotation. Ce n’est pas un validateur générique de reprise partielle. |
| Formats | `en_json`, `en_csv`, `COLONNES_CSV`, `ExportStrictRefuse`, lignes 365–418 du même module. Libellés historiques `paragraphe_depose`, `paragraphe_modifie`, `ancienne_cote`, `nouvelle_cote`. À préserver dans le profil E01. |
| Commande d’export | [`exporter_concordance`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/management/commands/exporter_concordance.py:17) reçoit source/cible, contrôle le lock et le référent, puis appelle ce constructeur. Elle n’a pas de mode CF3. |
| Démonstration | [`demonstration_e01`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/management/commands/demonstration_e01.py:199) crée et confirme les groupes avec `relier`/`confirmer_traitement`. Sa boucle de confirmation filtre le couple mais pas une nature. Elle doit rester une démonstration E01, sans reconfirmer d’autres profils par accident. |
| Protections | [`protection.py`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/protection.py:104) : identification par occurrences; archivage; signaux de suppression Document/LibraryNode/Statement et d’écriture Statement/LibraryNode. Chargement par [`DocumentManagerConfig.ready()`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/apps.py:8). Aucune garde actuelle équivalente pour tout le contenu relationnel d’une VersionActe gelée. |
| Éditeur actif | [`ajax_edit_node`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/views/produced_views.py:230) modifie directement l’objet de contenu; [`ajax_delete_node`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/views/produced_views.py:254) appelle directement `delete()`. Ils n’appellent ni le service de détachement ni celui d’archivage. Les routes actives sont [`urls.py:35`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/urls.py:35). Ce sont des consommateurs indirects déterminants. |
| Formulaires et administration | `DocumentForm` dans `forms/__init__.py`, `ProducedDocumentForm`, `NodeForm`, `LibraryNodeCreateForm` dans `forms/manual_forms.py`; le fichier historique homonyme `forms.py` ne contient pas non plus de formulaire de correspondance. Aucun formulaire, écran ou gabarit directement consacré à Correspondance trouvé dans la recherche Python/HTML/JS. `document_manager/admin.py` ne l’enregistre pas. Cela n’exclut pas les effets des suppressions ORM/cascades. |
| Ajout générique d’occurrence | [`add_library_node_ajax`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/views/library_node_ajax.py:113) peut rattacher un contenu existant. Son contrôle du nouveau régime de citations diffère sur l’intégration; il ne doit pas être contourné par une copie CF3 de contenus techniques. |
| Numérotation et présentations | [`numerotation.resoudre`, `index_par_noeud`, `index_par_statement`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/numerotation.py:276) dépendent du Document et des occurrences, **pas** de Correspondance. Les vues et sorties utilisant le résolveur n’acquièrent aucune nouvelle filiation automatiquement. L’index par Statement traite l’ambiguïté; CF3 doit employer l’index par occurrence. |
| Référent et reprise des numéros | [`referent.py`](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/referent.py:37), `reprise_numeros.py`, commandes `designer_referent`, `reprendre_numeros_imprimes`, contrôles de schémas : ils travaillent sur le référent, les occurrences ou la table de numéros imprimés. Cette « reprise » des numéros n’est pas CF3. Aucune consommation du modèle de filiation n’y a été trouvée. |
| Pièces et cotes | `case_manager/cotes_concordance.py`, `citations.py`, table autonome et cotation chronologique : appelés par l’export E01, sans autorité de filiation entre textes. CF3 ne doit pas leur faire importer le registre de l’analyse dans la demande. |
| Faux positifs écartés | `link_document_sources` utilise « Correspondance Exacte » pour des noms de PDF; `init_schemas_niveaux` nomme un schéma « Correspondance reproduite ». Ils n’utilisent pas les deux modèles audités. |

Recherche directe des classes, relations inverses et fonctions de service dans les sources Python/HTML/JS du dépôt, puis recherche des imports/appels indirects et des chemins d’édition/suppression. Les tests consommateurs sont détaillés en partie 8. La comparaison des fichiers pertinents entre E01 et l’intégration ne montre qu’un changement dans `document_manager/views/library_node_ajax.py` : consultation du gestionnaire par défaut pour respecter le régime de citations. Les modèles, services de concordance, protections et exports examinés ne divergent pas sur ce périmètre. Cela ne constitue pas un audit de toute l’intégration de l’Agent A.

## 2. Comparaison des trois opérations de filiation éditoriale

| Dimension | A — Concordance historique E01 | B — Révision d’un même acte | C — Reprise entre documents indépendants |
|---|---|---|---|
| Question | Que devient une occurrence déposée dans une rédaction ultérieure? | Que devient une occurrence d’une version précédente? | D’où provient ce passage repris, et qu’a-t-on retenu/modifié? |
| Identité des Documents | Source de juillet identifiée; cible ultérieure | Documents distincts rattachés au même Acte, une fois CF1 disponible | Documents et contextes de version indépendants; analyses ou demande |
| Couverture | Complète pour qualifier la concordance E01 de complète | Complète si l’on demande une comparaison complète; sinon périmètre déclaré | Limitée au plan de reprise; les passages non choisis restent hors opération |
| Texte non retenu | Peut recevoir un RETRAIT explicite | Peut recevoir un RETRAIT dans le périmètre comparé | N’est **pas retiré de l’analyse**; aucune décision de retrait n’est créée pour lui |
| Occurrences | Identités source conservées; nouvelles identités cible | Même principe, avec protection de chaque version gelée | Nouvelles identités cible, source entièrement conservée |
| Traitement | Décision éditoriale, pas qualification juridique automatique | Décision sur les textes de ces versions | Décision nouvelle dans le contexte destination; les confirmations antérieures ne sont pas reprises |
| Pièces | Appuis de juillet consultables, distincts des appuis retenus | Appuis de la version source consultables comme tels | Seulement les UP/sélections explicitement reprises; aucune qualification « juillet » induite |
| Numérotation | Papier source/STORED identifié; cible selon son profil | Chaque version selon son profil | Deux numérotations propres, même si le Statement est partagé |
| Gel | Référent de juillet conservé; rendus historiques inchangés | Version précédente isolée; nouvelle version modifiable | Analyse et demande gelables indépendamment; aucune synchronisation de rédaction implicite |

Le couple de Documents, les rôles et les groupes N:M sont communs. La **signification** et la **complétude attendue** ne le sont pas. Il faut une nature persistante de relation et des consommateurs explicitement contextualisés.

Exemple concret : une cible de la demande peut avoir simultanément un lien E01 depuis juillet et un lien de reprise depuis l’analyse danse. Les deux sont légitimes. Le second ne confirme ni ne remplace le premier. L’export juillet → demande ne doit y voir que la filiation E01 et les appuis historiques correspondant à son périmètre. L’historique rédactionnel de la cible peut montrer les deux relations, chacune qualifiée.

## 3. Invariants à préserver

| ID | Invariant et portée |
|---|---|
| I01 | Une occurrence garde son Document. CF3 crée de nouveaux LibraryNode; il ne déplace pas les nœuds de l’analyse vers la demande et ne recopie pas leurs PK/path Treebeard. |
| I02 | Chaque extrémité vivante appartient au Document du côté déclaré. SOURCE signifie antécédent rédactionnel; CIBLE signifie résultat rédactionnel. Ce ne sont pas les « sources probatoires » de Preuve. |
| I03 | Une relation porte un couple de Documents et une nature explicite. Une même occurrence peut participer à plusieurs relations qualifiées; aucun consommateur historique ne les mélange. |
| I04 | Les groupes décrivent exactement le plan N:M. Une fusion conserve tous ses antécédents; une scission toutes ses cibles. Ni numéro égal ni Statement partagé ne crée/ confirme un lien. |
| I05 | Texte partagé seulement avec édition isolée sur **toutes** les voies pertinentes. Capturer l’ancien texte avant chaque modification, puis détacher quand il faut préserver une autre occurrence ou un examen conservé. |
| I06 | Une confirmation nouvelle porte sur les occurrences, les deux ensembles de textes et la transformation effectivement examinés dans ce contexte. Elle n’hérite ni date, ni état, ni motif de validation d’une autre relation. |
| I07 | Toute modification d’un texte source ou cible, de son rattachement, de la composition ou de la qualification de la relation impose un réexamen. Un déplacement d’affichage seul ou une cote calculée différente ne l’impose pas. Une décision historique reste lisible avec ses textes. |
| I08 | Correspondance ne crée aucun appui. En C, les rattachements documentaires restent exclusivement UP/SelectionPreuve; la filiation et LienRedactionnel restent des responsabilités distinctes. AppuiDepotJuillet ne reçoit aucune copie destinée à faire passer la reprise pour un dépôt historique. |
| I09 | Reprise partielle explicite : appuis d’ancêtres hors bloc, réserves, prémisses, liens et insertions ont un devenir décidé. Un choix non résolu bloque l’application; il ne devient pas une omission silencieuse. |
| I10 | Une suppression physique autorisée conserve les identités, textes nécessaires et relations. Elle ne vaut pas RETRAIT éditorial. Un bloc comportant un élément protégé est refusé entièrement. |
| I11 | Le gel protège les occurrences, textes, examens, usages, liens et rendus de la version concernée. Une reprise ultérieure crée des objets destination et ne réécrit pas cette version. L’instantané historique E01 seul ne fournit pas cette garantie C. |
| I12 | Les contrôles et restitutions sont qualifiés par nature, couple et périmètre. CF3 ne dispense pas une demande de sa concordance E01, de ses citations ou des contrôles de cotes qui lui sont applicables. |

Ces invariants prolongent E01, notamment le [contrat, points 7–19](/Users/Louis-Philippe/Documents/GitHub/court/epic_numerotation_concordance_prompt_tests_rapport.md:159), [C07–C12](/Users/Louis-Philippe/Documents/GitHub/court/epic_numerotation_concordance_prompt_tests_rapport.md:231) et [EX01–EX07](/Users/Louis-Philippe/Documents/GitHub/court/epic_numerotation_concordance_prompt_tests_rapport.md:300). La reprise CF3 ne réutilise pas le contrôle des 198 numéros imprimés comme condition de copie d’une analyse; ce contrôle garde sa fonction E01 propre.

## 4. Incompatibilités et écarts constatés dans le code actuel

### 4.1 Le mélange historique est un risque de consommation réel

Le schéma ne sait pas distinguer A/B/C. `appuis_dorigine` remonte tous les groupes d’une cible, puis présente leurs appuis comme ceux du dépôt. Même quand `construire(juillet, demande)` sélectionne le bon couple, `_ligne` perd ce périmètre lors de son appel à cette fonction.

Contre-exemple de lecture : une occurrence analytique partage un Statement avec juillet; elle devient antécédent CF3 de la demande. Les AppuiDepotJuillet de ce Statement sont trouvés depuis cette filiation interdocumentaire et peuvent s’ajouter aux résultats de la ligne E01. Sans partage de Statement ou appui historique correspondant, le mélange n’est pas systématique; cela ne rend pas le contrat sûr. Autre défaut : un antécédent portant un objet générique non Statement peut rencontrer par coïncidence numérique un Statement de même PK. Enfin, un antécédent archivé peut être `None` et provoquer une erreur dans le lecteur actuel.

**Adaptation :** nature + couple dans les lectures historiques; contrôle du ContentType; accès explicite à l’archive. L’historique général peut montrer plusieurs origines, mais chaque source de filiation reste qualifiée. Aucune remontée transitive analyse → version intermédiaire → juillet n’est assimilée à une décision E01 directe.

### 4.2 Une confirmation peut rester courante après détachement

Scénario : source S et cible T portent le même Statement X. La relation est confirmée, ses M2M retiennent X/V1. `detacher_pour_edition(T, V2)` donne à T un Statement Y; X reste inchangé pour S. Toutes les captures X/V1 sont encore `est_courante=True` sur X. La boucle de [models.py:628](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/models.py:628) peut donc laisser la relation `CONFIRME` alors que T porte Y/V2.

Le test existant [T18, ligne 601](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/test_e01_numerotation.py:601) réécrit une cible initialement **non partagée**. Il exerce la mutation de son Statement en place. [T16, ligne 778](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/test_e01_numerotation.py:778) vérifie bien le détachement partagé, mais n’y associe pas une confirmation éditoriale préalable. Leur combinaison manque. Le même défaut peut toucher [ConfirmationAppui.etat_courant](/Users/Louis-Philippe/Documents/GitHub/court/case_manager/models.py:649).

La simple comparaison des ensembles de Statement/empreintes corrigerait ce cas, mais ne prouverait pas qu’une occurrence ajoutée ou substituée avec le **même** Statement figurait dans l’examen initial. Le contrat doit aussi conserver l’identité des extrémités examinées. Les ensembles vides rendent actuellement la vérification vraie; ils ne doivent pas certifier par défaut un groupe portant des textes non examinés.

**Adaptation :** manifeste persistant d’examen par occurrence, empreinte de sa composition et conservation des décisions successives, décrits en 6.2. Pas de nouveau moteur de confirmation probatoire.

### 4.3 Le bon service ne garantit pas le bon chemin d’édition

`ajax_edit_node` écrit en place. Si X est porté par un référent historique ou un acte REPRODUCED, le signal peut refuser la sauvegarde : la source est protégée, mais l’édition cible n’est pas réalisée par détachement. Si X est partagé seulement entre deux Documents PRODUCED ordinaires, la garde actuelle ne le refuse pas : l’analyse et la demande peuvent changer ensemble.

`ajax_delete_node` ne passe pas par l’archive. Une occurrence liée est protégée par son FK `PROTECT`, donc le chemin direct peut échouer; une occurrence non liée peut disparaître sans archive par ce chemin. Le [rapport E01, ligne 373](/Users/Louis-Philippe/Documents/GitHub/court/rapport_execution_epic_E01.md:373) décrit les gardes; il ne démontre pas le routage de ces vues par les services. Les tests de service ne remplacent pas les tests de requête de ces routes.

**Adaptation :** raccorder édition et suppression aux contrats communs avant d’autoriser CF3 avec partage. Le refus de modifier la source historique reste obligatoire. Un chemin d’écriture non raccordé doit refuser une mutation partagée; il ne doit pas la réaliser en place.

### 4.4 Les archives peuvent perdre une partie de l’examen

[La suppression autorisée](/Users/Louis-Philippe/Documents/GitHub/court/document_manager/concordance.py:239) archive le texte actuel et dénoue les extrémités. Elle peut ensuite supprimer un Statement sans occurrence ni AppuiDepotJuillet. Si ses VersionTexte sont seulement référencées par les M2M de Correspondance, `CASCADE` peut emporter ces captures et leurs associations. L’archive du dernier texte ne remplace pas une capture V1 examinée avant une réécriture V2. D’autres relations `PROTECT`, par exemple une ConfirmationAppui, peuvent au contraire bloquer une suppression : on ne peut donc pas annoncer une disparition systématique, mais le risque existe dans le cas purement éditorial.

La cible Document est en `CASCADE`; NoeudArchive dépend également du Document en `CASCADE`; `archive=SET_NULL` autorise une extrémité devenue vide. `archiver_noeud()` ne conserve pas le ContentType et affecte object_id à `statement_pk` quel que soit le modèle : un lecteur ne peut donc pas qualifier sûrement une ancienne archive à partir de ce nombre seul. Il faut fermer ces chemins sans interdire toutes les suppressions d’occurrences PRODUCED.

**Adaptation :** conserver les captures encore nécessaires aux examens, archiver les occurrences autorisées, protéger les archives citées et refuser la destruction du conteneur Document si elle ferait disparaître la filiation utile. Aucun changement de FK n’est indispensable si les gardes couvrent réellement instance/lot/cascade; cette couverture doit être testée, pas supposée.

### 4.5 L’export E01 n’est pas le validateur d’une sélection CF3

EX01 demande un référent historique; EX02 parcourt tous les paragraphes des deux Documents; EX04 dépend du lock de juillet; EX05 attend les ConfirmationAppui historiques du mécanisme E01. Une analyse de vingt paragraphes dont on reprend trois n’est ni un référent fictif à créer, ni dix-sept RETRAITS à décider. Relâcher ces contrôles globalement serait une régression.

**Adaptation :** conserver le profil et les formats E01; produire pour CF3 un compte rendu de filiation limité au plan, avec libellés source/destination et appuis explicitement sélectionnés. Un simple compte rendu CF3 ne prétend pas être une concordance E01 complète ou un résultat C prêt à geler.

### 4.6 Le gel C n’existe pas encore dans ces services

Les signaux actuels portent sur les protections REPRODUCED/référent et certains objets. Ils ne verrouillent pas Correspondance, ses extrémités, ses M2M et les objets proposés de C. `confirmer_traitement` peut remplacer les textes examinés. `supprimer_occurrence` modifie toutes les extrémités qui touchent le bloc, sans examen d’un gel propriétaire. Les écritures de masse ne sont pas couvertes par un simple `pre_save`; un protocole transactionnel et les gardes relationnelles prévus par D08 restent nécessaires.

**Adaptation :** inclure la filiation dans le contenu canonique et les protections neutres. Cela relève du gel global déjà prévu, pas d’un mécanisme historique concurrent. Aucun premier gel réel C avant la réalisation et les tests de L5.

Les écarts 4.2–4.4 sont des limites du code déjà présent mises en évidence par l’audit. Ils ne sont pas causés par une implémentation CF3, puisqu’aucune n’existe. Leur correction est un préalable à l’élargissement sûr.

## 5. Comparaison des trois solutions

| Critère | 1 — Schéma inchangé | 2 — Extension explicite de Correspondance | 3 — Filiation distincte |
|---|---|---|---|
| Fidélité A/B/C | N:M représentable, mais la nature dépendrait des paramètres d’appel ou d’une déduction externe non garantie aujourd’hui. | Les trois natures deviennent consultables après relecture; même identité d’occurrence et même groupe de transformation. | Représentable, mais une cible aurait deux systèmes de filiation à consulter. |
| E01 existant | Les services doivent déjà être corrigés; aucun filtre persistant fiable n’est disponible. | Profil E01 conservé; filtres et examens durcis explicitement; données historiques non reconstruites par supposition. | Les anciennes tables restent réservées à E01; cela ne corrige pas leurs défauts de réexamen et d’archivage. |
| Migrations | Aucune sur ces tables. Une qualification déduite d’un futur Acte déplacerait le problème vers un contexte nouveau à rendre obligatoire et immuable. | Deux champs proposés sur Correspondance : `nature` et `examens_editoriaux` (manifestes et empreintes conservés); un champ `type_contenu` sur NoeudArchive. Aucun modèle de filiation supplémentaire. Transition des anciennes décisions/archives à traiter explicitement. | Nouveau modèle, extrémités, examens et migrations; éventuellement des adaptateurs ou une table d’union. |
| Duplication | Évitée, au prix d’une qualification implicite ou d’un registre externe. | Une autorité de filiation. Les manifestes conservent les décisions sur des états passés; ils ne constituent pas une seconde carte active de liens. | Risque de doubles relations, moteurs de lecture et règles divergentes sur les mêmes LibraryNode. |
| Suppression / archives | Doit être renforcée dans les services existants. | Même mécanisme d’archive, avec protection des examens et des conteneurs utiles. | Doit coordonner deux ensembles de FK et deux propriétaires d’historique. |
| Gel | Le contenu doit tout de même capturer le contexte et les extrémités examinées. | Une sérialisation de filiation et des gardes communes; propriété du gel explicitée. | Deux sérialisations et contrôles; risque d’en oublier une. |
| Tests | Tous les nouveaux comportements + preuve que les appelants transmettent toujours le bon contexte. | E01 conservé, profils mélangés, migration, examen par occurrence et tests CF3. | E01 + nouveau système + tests d’intégration entre eux. |
| Complexité | Faible en schéma, élevée et fragile dans les conventions distribuées. | Extension limitée, mais corrections réelles de consommateurs et chemins d’écriture. | Plus de tables et de services pour des invariants fondamentaux identiques. |
| Avis | Non retenue avec le code et le contexte actuels. | **Recommandée sous les conditions ci-dessous.** | Non justifiée par une incompatibilité structurelle démontrée. |

Le contrat E01 exige des occurrences, un couple, des transformations N:M et des décisions liées aux textes; aucun invariant ne commande que la table soit exclusivement réservée à juillet. En revanche, ses consommateurs historiques imposent une spécialisation qu’il faut isoler explicitement. C’est ce constat qui justifie la solution 2, et non une préférence abstraite pour réutiliser une table.

Une future preuve que tous les Documents sont obligatoirement rattachés à des Actes immuables pourrait permettre de dériver certaines distinctions. Cette preuve n’existe pas dans le code audité et ne rendrait toujours pas « reprise de texte » équivalent à « décision historique de concordance ». Elle ne fonde donc pas le verdict sans modification de schéma.

## 6. Contrat final recommandé pour CF3

### 6.1 Qualification persistante et compatibilité E01

Proposition de trois valeurs de `Correspondance.nature` :

| Nature | Sens et contrôle |
|---|---|
| `E01` | Concordance au sens du mécanisme existant. La création de liens peut précéder la reprise des numéros, conformément à T02. L’export strict garde ses contrôles historiques complets. Cette valeur est un profil de traitement; à elle seule, elle ne certifie pas que le Document est celui réellement déposé. |
| `REVISION_ACTE` | Transformation entre deux VersionActe distinctes d’un même Acte, selon le contexte neutre CF1 une fois disponible. |
| `REPRISE_DOCUMENTAIRE` | Filiation entre rédactions indépendantes, y compris analyse → analyse et analyse → demande. Les deux Documents restent distincts. |

Le sens des rôles SOURCE/CIBLE et les FK existants sont conservés. Mettre à jour les descriptions du modèle pour nommer les trois natures; garder les descriptions historiques dans le seul profil E01.

Compatibilité de l’entrée existante `relier()` : conserver le défaut `E01` pour ses appelants hérités identifiés; les nouvelles entrées CF3 doivent passer leur nature explicitement. Un constructeur CF3 ne peut pas bénéficier d’un défaut historique. Toute nouvelle relation vérifie les deux Documents distincts, les contextes pertinents, les rôles, l’appartenance, l’absence de doublons dans un côté et un groupe non vide. Une même occurrence des deux côtés d’un même groupe est refusée.

Migration envisagée après approbation : valeur `E01` pour les lignes antérieures **au sens de conservation du profil hérité**, sans certifier leurs sources ni les requalifier en B/C. Inventorier les éventuelles lignes atypiques dans un diagnostic avant bascule. Ne pas utiliser un titre, un numéro ou `PRODUCED` comme preuve de leur nature réelle. Aucune migration n’est écrite ici et aucune donnée n’est inspectée en base.

### 6.2 Examen par occurrence et conservation des décisions

Proposer un second champ sur Correspondance, `examens_editoriaux`, contenant des manifestes d’examen versionnés, ajoutés successivement sans modification des entrées antérieures. Un JSON structuré sur le modèle existant suffit au périmètre demandé; aucune nouvelle table de filiation n’est nécessaire. Son format et sa validation appartiennent au contrat neutre L1. Une empreinte seule ne suffirait pas à conserver la carte des occurrences examinées ni le motif/date d’une décision remplacée.

Chaque nouvelle entrée contient :

- Un identifiant d’examen et la version de son format, la date, le motif, le traitement et `deplace` décidés.
- La nature et les identités du couple de Documents examinés.
- Pour chaque côté, les extrémités ordonnées avec leurs PK d’occurrence, type de contenu qualifié, Statement et VersionTexte examinée/empreinte; les groupes sans texte sont identifiés comme tels.
- Une empreinte SHA-256 de ce manifeste canonique. Elle ne comprend ni numéro d’affichage, ni cote calculée, ni position courante dans le Document.

Les extrémités restent **l’unique carte active de filiation**. Les manifestes sont l’histoire des examens de cette carte. Les VersionTexte restent l’autorité des textes capturés et sont protégées tant qu’un examen conservé les utilise. Le contenu de gel capture aussi les textes; il ne dépend pas de la disponibilité future d’un Statement modifiable.

Après bascule d’une relation sur ce contrat, le dernier examen explicite est l’autorité de sa décision courante. Les champs hérités `etat`, `traitement`, `decide_le`, `motif` et M2M restent des projections de compatibilité, alimentées atomiquement par le même service. Ils ne sont plus modifiables indépendamment pour confirmer la relation. Une différence entre projection et manifeste est une anomalie bloquante, pas une occasion de choisir arbitrairement l’un des deux. Les anciennes relations sans manifeste restent identifiées comme héritées selon la transition ci-dessous.

Règles d’examen :

1. Sous transaction et verrou approprié, relire la correspondance, ses deux Documents, extrémités et Statements. Refuser l’examen d’une ligne protégée par un gel propriétaire.
2. Vérifier les invariants de chaque côté. Pour les occurrences textuelles, la capture doit appartenir au Statement **actuellement porté** et son empreinte doit correspondre au texte examiné. Les ensembles doivent couvrir exactement les textes des extrémités de chaque rôle, sans capture manquante ou étrangère.
3. Les groupes structurels sans Statement peuvent être tracés, mais ne reçoivent pas par vacuité une confirmation de texte. Leur identité est dans le manifeste; les propositions reprises sont examinées par leurs occurrences textuelles. Un contenu générique étranger au profil est refusé.
4. Ajouter le manifeste, son empreinte et la nouvelle décision seulement lors d’un examen explicite, puis mettre à jour les projections héritées. Une nouvelle CF3 commence `A_ETABLIR`, y compris pour un texte identique. Elle ne copie ni `etat`, ni `decide_le`, ni manifestes, ni M2M d’une autre Correspondance.
5. Au contrôle courant d’une relation modifiable, reconstruire la partie comparable du manifeste avec les extrémités et contenus actuels; toute différence impose `A_REEXAMINER`. L’ajout d’une deuxième occurrence portant le même Statement est ainsi détecté, contrairement à une simple comparaison de sets. La décision et les textes précédents restent lisibles après réexamen **et après reconfirmation**, grâce aux entrées conservées.
6. Une renumérotation ou un déplacement dans l’arbre sans changement des extrémités/textes ne change pas cette empreinte. Une modification explicite de la qualification ou de l’ordre des extrémités du groupe exige, elle, une nouvelle décision. `deplace` est une qualification de l’opération, pas une égalité automatique de chemins entre deux Documents.

**Transition des confirmations existantes :** ne pas fabriquer un manifeste historique depuis la composition actuelle. Cela prétendrait démontrer que ces extrémités étaient présentes lors de la décision. Conserver les champs et textes historiques; diagnostiquer séparément l’absence de manifeste. Avant de remplacer une décision héritée, en conserver le relevé disponible avec ses anciens textes, date et motif et une mention explicite « composition examinée non attestée »; ce relevé n’acquiert pas la qualité d’un examen complet.

Un ancien rendu figé conserve son état historique et n’est jamais régénéré pour le « corriger ». Pour un nouvel export strict soumis au contrat renforcé, un examen sans provenance suffisante demande une revue explicite sur une rédaction modifiable. Les groupes dont le contrôle est déjà faux après détachement ne doivent pas continuer à satisfaire EX02. Cette restriction de transition doit être approuvée et expliquée; elle n’est pas un recalcul silencieux des confirmations en base. Dans une version gelée, les lecteurs utilisent l’examen conservé dans son contenu, sans le requalifier selon les brouillons actuels.

Ce champ répond à deux lacunes démontrées : les M2M décrivent des textes mais ne mémorisent pas la carte des occurrences examinées, et leur remplacement ne conserve pas toutes les décisions successives. Il ne constitue ni une confirmation probatoire ni un moteur d’inférence. Son ajout ne reconstruit aucune décision ancienne perdue.

### 6.3 Entrées et plan de reprise

Signature conservée : `reprendre_sous_arbre(source, destination, plan_de_reprise)`.

`source` désigne un Document/version et des occurrences identifiées; `destination` un Document/version et un emplacement autorisé. Le plan est un objet de service explicite, pas un nouveau modèle parallèle de filiation. Il fixe :

- Les occurrences et descendants retenus, leur rôle dans le profil destination, leur ordre et les textes à conserver/reformuler.
- Les groupes de transformation attendus, avec listes SOURCE/CIBLE. Les nouvelles cibles sont identifiées d’abord par des clés de plan, puis par leurs PK créés.
- Les réserves et prémisses incluses, les omissions décidées et leurs motifs. Reprendre le sous-arbre complet est le comportement de départ; retrancher un sous-item pertinent exige un choix visible.
- Les UP et sélections exactement retenues, leur cible et leur portée destination; les usages d’ancêtres hors bloc sont traités séparément.
- Les compositions/insertions et leur remappage ou leur état à réancrer.
- Les liens rédactionnels à créer dans la destination, ceux conservés vers l’extérieur et ceux retirés explicitement; les cibles de version gelée restent identifiées comme telles.
- Les empreintes de précontrôle nécessaires pour refuser un plan devenu périmé avant application.

Le mode rapport ne crée aucun objet. L’application relit le même état et réussit entièrement ou échoue sans copie partielle. Les changements concurrents de source, destination, appuis ou liens pertinents sont refusés si le plan ne les couvre plus. La prévention d’un double envoi de la même application peut relever de l’entrée transactionnelle; aucune table de sessions de copie n’est imposée par ce mandat.

### 6.4 Ordre d’application et cardinalités

1. Contrôler les contextes CF1 et les protections. La source peut être une analyse PRODUCED modifiable ou gelée; la destination doit être une rédaction PRODUCED modifiable. Le profil CF3 n’autorise pas à modifier un acte REPRODUCED ou le référent de juillet. Une reprise rédactionnelle de source externe passe par le chemin documentaire prévu, pas par une copie aveugle d’objet générique.
2. Lire le bloc et ses relations, calculer la clôture de contexte à proposer. Un point de contexte non résolu bloque l’application; une omission expressément décidée reste visible dans le rapport et dans le motif de filiation.
3. Créer de nouvelles occurrences dans la destination et une carte ancien → nouveaux. Une scission peut donner plusieurs nouveaux PK pour un ancien; une fusion plusieurs anciens pour un nouveau. Ne pas copier path/depth/numéro source comme une identité destination.
4. Partager un Statement inchangé seulement lorsque tous les chemins d’édition sont protégés par le contrat de détachement. Sinon, créer dès la reprise un Statement destination et capturer ses textes. Le partage n’est pas une condition de conservation textuelle; la filiation est portée par Correspondance. Toujours capter V1 avant l’édition, même non partagée; préserver les captures utiles aux examens.
5. Créer les groupes `REPRISE_DOCUMENTAIRE` et leurs extrémités. Utiliser `SCINDE` pour 1:N, `FUSIONNE` pour N:1; une transformation collective N:M peut être qualifiée `REFORMULE` avec motif explicite. Aucun nouvel enum n’est nécessaire pour le cas démontré. Un déplacement peut compléter la qualification principale.
6. Copier seulement les usages, sélections et objets de rendu choisis, puis les liens choisis, selon les règles suivantes. Recueillir séparément les nouvelles décisions nécessaires; une réussite technique de copie ne confirme pas les traitements.
7. Résoudre les numéros sur le Document destination entier; produire le rapport de reprise et les diagnostics. Calculer les pièces/cotes uniquement depuis les usages destination et le résultat central C, lorsqu’il est disponible.

La reprise partielle ne crée ni AJOUT ni RETRAIT E01. En CF3, les groupes de filiation ont au moins une source et une cible. Les créations sans antécédent et les passages source non sélectionnés restent hors de cette opération; une décision historique supplémentaire peut ensuite être prise dans son propre profil.

Un groupe N:M signifie une transformation **collective** des textes déclarés. Il ne permet pas d’inventer toutes les filières possibles d’un lot hétérogène. Pour `s1→t1` et `s2→t2`, créer deux groupes, pas un groupe qui suggérerait quatre couples. Le compte rendu conserve les IDs des groupes. Le produit cartésien de présentation de l’export E01 ne crée aucun appui et ne doit pas devenir un algorithme de copie CF3.

Un groupe reste rattaché à **un couple de Documents**. « Plusieurs sources et cibles » désigne plusieurs occurrences de ces deux Documents. Si une application combine deux analyses indépendantes dans la même demande, créer des groupes par couple dans une transaction commune. On ne place pas des occurrences d’une seconde analyse dans les extrémités du premier couple. Une fusion éditoriale réellement globale de plusieurs Documents peut être présentée dans le rapport commun, sans prétendre qu’un unique groupe actuel la représente. Aucune identité persistante supplémentaire d’opération multidocumentaire n’est requise par les scénarios soumis.

### 6.5 Appuis : décision destination et autorité unique

Les UP destination reçoivent de nouveaux PK, la VersionActe destination et les nouvelles occurrences cibles. Les SelectionPreuve nouvelles pointent vers les **mêmes** nœuds de preuve autorisés, avec les rangs choisis. Les sources, leur identité et les preuves ne sont pas dupliquées pour une simple reprise. La sélection d’une racine/groupe doit être explicitement voulue; une copie de paragraphe ne sélectionne pas toute sa preuve.

Dans la conception C, une UP est un rattachement documentaire déclaré par l’auteur, pas une confirmation de vérité ou de pertinence démontrée. Le schéma proposé ne possède pas d’état probatoire automatique à recopier. Le plan accepté peut déclarer ces nouveaux usages; il ne peut importer l’autorité d’une ancienne ConfirmationAppui, d’une certification d’un autre texte ou de `Correspondance.etat`. Les candidats non choisis restent dans le précontrôle, sans devenir des UP destination. Une reformulation exige de revoir les sélections/portées proposées avant de les retenir.

Un usage attaché à un ancêtre non repris donne trois possibilités explicites : ne pas le reprendre, le rattacher à une occurrence destination identifiée avec portée adaptée, ou reprendre aussi le groupe pertinent. Le service ne le propage pas au nouvel enfant. En scission/fusion, chaque cible dispose de ses choix; l’union des appuis des sources n’est jamais automatiquement confirmée.

Conserver AppuiDepotJuillet, Fait/Axe et les appréciations héritées en dehors de toute copie probatoire implicite. Les fonctions historiques demeurent des lecteurs de l’histoire E01. Une projection de l’origine peut proposer des candidats; elle ne constitue pas une seconde écriture d’autorité.

### 6.6 Réserves, prémisses, liens et insertions

- **Réserves sous-items :** reprises avec le bloc par défaut. Un retrait explicite interdit de présenter la nouvelle rédaction comme inchangée sans examen. Le service ne peut pas reconnaître toutes les réserves sémantiques par traitement du langage : le choix de bloc et la revue de l’auteur demeurent nécessaires.
- **Prémisses :** celles dans le bloc sont remappées; celles hors bloc sont recensées à partir des liens déclarés et de la revue de contexte. Soit elles sont reprises, soit une référence externe explicite est retenue, soit leur retrait est décidé. Le logiciel ne certifie pas qu’il a détecté toutes les prémisses implicites d’une prose.
- **Lien interne CF2 :** créer un nouveau lien seulement s’il figure dans le plan; remapper ses deux extrémités vers les nouvelles occurrences. Une reformulation impose de revoir les textes examinés; ne pas capter automatiquement les nouveaux textes pour faire apparaître une déclaration ancienne comme réexaminée. Copier un texte seul ne crée pas ces déclarations.
- **Lien externe :** conserver le Document, la version et l’occurrence externe réellement visés; aucune recherche par numéro similaire. Une dépendance déclarée vers une autre rédaction encore mutable peut exister en brouillon, mais bloque le gel strict selon CF2; alternative : reprendre les prémisses dans le Document destination. Un simple renvoi de navigation conserve le statut de capture de référence déjà défini, sans import d’appuis.
- **Analyse gelée :** viser V1 et son occurrence, pas un alias « dernière analyse ». Créer V2 de l’analyse n’actualise pas le renvoi historique de la demande. Toute actualisation est une nouvelle décision dans une version modifiable.
- **Rendu :** remapper les insertions vers l’occurrence, la VersionTexte, les usages et compositions destination. Leur compatibilité demande le bon Statement et le texte exact; des offsets encore dans les bornes ou une cote identique ne suffisent pas. Après reformulation, une insertion reste à réancrer jusqu’à validation. Les rendus conservés de la source ne sont jamais réutilisés comme fichiers destination modifiables.

### 6.7 Suppression, archives et gel indépendant

**Archive typée.** Ajouter `NoeudArchive.type_contenu`, libellé qualifié stable tel que `document_manager.statement`. Pour une nouvelle archive, une valeur vide explicite désigne un nœud structurel sans objet; une valeur nulle désigne une archive héritée dont le type n’est pas attesté. Conserver l’identité d’objet dans le champ existant seulement avec cette qualification; le nom historique `statement_pk` ne permet pas d’inférer un type. Aucun appui de juillet n’est retrouvé par égalité numérique depuis une archive de type inconnu. Une migration ne devine pas ce type; un contrôle documenté peut le renseigner si la provenance permet réellement de le prouver.

**Suppression d’une occurrence modifiable.** Précontrôler le bloc entier et toutes les relations qu’elle touche, dans les deux rôles et toutes les natures. Archiver avant suppression; chaque extrémité possède exactement une occurrence vivante ou une archive du même Document/côté. Préserver les textes examinés encore utiles, y compris des versions différentes du dernier texte archivé. Leur conservation peut empêcher la purge d’un Statement devenu sans occurrence; un Statement sans usage ni histoire utile reste supprimable conformément à E01.

Les lecteurs rendent explicitement les extrémités archivées; ils ne déréférencent pas `None`. Une relation dont des extrémités ont disparu devient une filiation historique archivée, pas une justification courante du contenu restant. Sa décision ancienne reste lisible. Pour une comparaison complète E01, les occurrences encore actives doivent recevoir des décisions actuelles explicites; l’ancien groupe archivé ne vaut pas une couverture automatique, ni un RETRAIT automatique. Le lecteur strict distingue ainsi historique consultable et décisions applicables, sans être définitivement bloqué par une décision ancienne déjà remplacée dans le périmètre courant.

**Suppression d’un conteneur ou de l’histoire.** Refuser la destruction d’un Document ou d’une archive si elle effacerait un examen ou une filiation encore nécessaires. Conserver le conteneur avec son état d’archive rédactionnel selon le cycle de vie retenu; ne pas confondre cela avec le gel judiciaire. Fermer les cascades et suppressions directes de Correspondance/extrémités/textes historiques utiles. Cette protection doit être commune aux natures. Il n’est pas nécessaire de rendre tous les LibraryNode logiquement supprimés ni d’introduire une nouvelle table de filiation.

**Propriété du gel.** La relation de filiation nouvellement créée appartient à l’histoire rédactionnelle de sa destination. Geler une source ne doit pas interdire de créer plus tard une nouvelle relation entrante dans une autre rédaction à partir de ses occurrences protégées. C’est précisément ce qu’exige E01 lorsqu’on relie juillet à un nouveau brouillon. En revanche, une relation et un examen déjà inclus dans un contenu gelé ne sont jamais réécrits ou dénoués par une opération ultérieure. Une suppression qui exigerait de toucher une telle relation est refusée; elle doit être réalisée dans une nouvelle version avec de nouveaux objets.

Ainsi, une analyse V1 gelée peut être l’antécédent de la demande D1 modifiable sans modifier V1. Le gel de D1 conserve ses filiations entrantes, manifestes d’examen, textes source observés, références à V1 et propres usages/rendus. Créer analyse V2 ou demande D2 ne change ni le contenu conservé de V1/D1, ni leurs confirmations. La liste actuelle des documents qui ont ensuite repris V1 peut être une projection extérieure datée; elle ne devient pas rétroactivement une partie du contenu gelé de V1.

Capturer dans le même contenu canonique C les natures, couples, extrémités/archives, textes examinés, empreintes, décisions et références de versions. Les FK vivants servent à la navigation; les rendus historiques se lisent depuis les données conservées, sans dépendre de la rédaction actuelle. Le protocole de gel ne reçoit aucun fichier incomplet; une nouvelle composante de contenu est versionnée sans réécrire les anciens contenus.

### 6.8 Adaptation exacte des consommateurs

| Point | Changement contractuel demandé après approbation |
|---|---|
| `relier` et confirmation | Qualification; validations communes; examen par occurrence et empreinte; préservation avant édition; refus de mutation d’objets gelés. |
| `correspondances_de` / `antecedents_de` | Accepter des filtres explicites de nature/couple; une lecture générale garde les relations qualifiées. Préserver l’API héritée pour les appels E01 identifiés, sans exposer une liste non qualifiée comme des appuis historiques. |
| `appuis_dorigine` | Rester lecteur E01; périmètre de couple/nature transmis depuis l’export. Ne pas en faire le lecteur des UP de CF3. Contrôler le type et gérer les archives. La lecture générale de filiation est distincte de cette projection historique. |
| `_ex02`, `construire`, `_ligne` | Filtrer E01; conserver la couverture complète et les codes EX01–EX07; gérer explicitement l’histoire archivée. Transmettre le périmètre jusque dans la lecture des appuis d’origine. |
| `exporter_concordance` et démonstration | Profil E01 conservé, aucun assouplissement pour faire passer CF3. La boucle de confirmation ne touche que les groupes du profil demandé. |
| Rapport CF3 | Périmètre du plan, groupes exacts, source/destination, carte de nouvelles occurrences, contexte omis décidé, usages choisis et examens restant à faire. Ne pas reprendre les colonnes « déposé » et « juillet » comme libellés génériques. |
| Vues d’édition/suppression | Appeler les services communs; traiter le refus de protection et les archives; tests HTTP indispensables. Conserver le contrôle de régime des citations de la branche d’intégration. |
| `ConfirmationAppui` / citations anciennes | Durcir la fraîcheur par occurrence lorsque ce chemin reste utilisé; ne pas convertir ces données en UP. Ne pas faire du rendu ancien une implémentation implicite d’InsertionRendu. |
| Numérotation | Aucun second résolveur. Résolution complète puis filtrage; liens par PK. Aucun numéro historique inventé dans une nouvelle destination. |

## 7. Conséquences sur CF1, CF2, L1 et L2

| Élément | Conséquence concrète | Condition de sortie |
|---|---|---|
| CF1 | Analyses et demandes utilisent les mêmes contextes neutres Acte/VersionActe proposés, avec nature interne admise. Une VersionActe possède son Document. Permettre de distinguer B/C par identités formelles, sans titre ou dépôt fictif. | Contextes vérifiés avant toute UP persistée. Aucune analyse interne déclarée déposée/transmise pour satisfaire E01. |
| CF2 | LienRedactionnel conserve son autorité de déclaration; reprise de liens explicite, contrôle des textes par occurrence, renvois de version gelée et règle externe stricte inchangés. | Texte copié, filiation, appui et dépendance ne s’engendrent pas mutuellement. Les cycles déclarés restent contrôlés selon le contrat CF2; aucun graphe entre Preuve n’est ajouté. |
| L1 — neutre | Inclure qualification de filiation, examen par occurrence, préservation des textes et correction des chemins d’édition/suppression. Définir et tester la copie d’occurrences/texte et le remappage rédactionnel sans import de proof_manager. Les deux champs de Correspondance et le champ d’archive typée proposés appartiennent à document_manager. | Non-régression E01 et tests de lecture mixte; séparation des profils; aucune prétention au gel complet ou à la copie d’usages avant leur disponibilité. |
| L2 — usages | Orchestration atomique du plan complet : primitives neutres L1 + nouvelles UP/sélections retenues; choix d’ancêtres explicite. proof_manager appelle la couche neutre; document_manager n’importe pas proof_manager. | Aucun « succès complet CF3 » si le texte est copié mais les relations choisies échouent. Les tests VF02/03/05 et les variantes scission/fusion passent sur base isolée. |
| L3/L4 | Résultat central par version et validation/réancrage des compositions/insertions. Les parties du plan qui en dépendent ne sont pas déclarées fonctionnelles avant ces lots. | VF04 et fidélité des passages; aucune réutilisation d’offsets ou d’anciens fichiers à titre de validation. |
| L5 | Extension du contenu canonique et des gardes au contrat de filiation, avec propriété du gel destination et références externes. | VF08 et tests de gel/suppression via toutes les voies. Aucun gel réel annoncé avant L5. |

Le découpage conserve L1 neutre et L2 probatoire. Une primitive L1 peut être testée avec un plan texte seul; elle ne vaut pas acceptation de CF3 complet. Les fonctions de rendu et de gel restent livrées dans les lots déjà prévus. CF4 Photo→Event n’est pas modifié par cet audit.

Ordre de développement proposé : (1) approbations ciblées; (2) corrections E01 communes et tests de contre-exemples; (3) qualification/migration contrôlée et lecteurs filtrés; (4) primitives neutres de reprise et CF1/CF2; (5) orchestration L2; (6) validation avec rendus/gel au moment des lots concernés. Le choix de branche d’implémentation et toute intégration restent des décisions ultérieures; aucune branche existante n’est modifiée ici.

## 8. Matrice des tests positifs et négatifs

**Statut de toutes les lignes : spécification ou relecture de tests, non exécutée dans ce mandat.** Les références E01 désignent les contrats et tests présents, pas un résultat de cette session. Les futurs tests s’exécutent sur une base jetable dédiée, sans base réelle ni serveur. Les données anciennes restent des références; une migration ne « répare » pas leur histoire.

### 8.1 Non-régression E01

| ID | Référence existante | Contrôle positif | Contre-épreuve / résultat attendu |
|---|---|---|---|
| NR01 | C02/C09; T02 dans `document_manager/test_e01_numerotation.py:477` | Référent PRODUCED ou REPRODUCED protégé; création d’un lien E01 possible avant T01, sans inventer le numéro imprimé. | Écriture/suppression source par instance/lot/cascade refusée, transaction intacte. CF3 ne contourne pas ces gardes. |
| NR02 | C04/C06/C07; T05–T10, T16–T18 | Deux occurrences d’un même Statement gardent leurs numéros propres; renumérotation d’affichage conserve les examens applicables. | Aucun numéro copié d’un autre Document; index par Statement ambigu ne choisit pas une occurrence. |
| NR03 | C07/C09; T18, T16 (`:601`, `:778`) | Confirmer puis réécrire une cible non partagée et une cible partagée : nouveau contrôle à réexaminer, ancienne capture lisible. | Cas partagé X→Y refusé comme encore confirmé, même si X/V1 reste courant sur la source. Variante : modification du côté SOURCE dans une rédaction B/C mutable. |
| NR04 | C07; T19/T20 (`:656`, `:668`) | 1:N et N:1 conservent tous les antécédents/cibles et leur ordre. | Mauvais Document, doublon, rôle invalide, extrémité vide ou incohérente : refus sans groupe partiel. |
| NR05 | C08/C09; T21/T22 (`:678`, `:701`) | AJOUT/RETRAIT motivés restent des décisions; occurrence PRODUCED liée archivée, origine intacte. | Absence de lien ne devient pas décision; suppression physique ne retire pas automatiquement les antécédents. Groupe archivé consultable, décisions courantes explicites pour les occurrences actives. |
| NR06 | C09/C11; T18/T23 | Reconfirmer uniquement l’appui ne résout pas EX02; reconfirmer uniquement le traitement ne résout pas EX05. | Copier état, date ou appréciations d’une autre relation ne confirme pas le nouveau texte. |
| NR07 | C10/C11; T23 dans `case_manager/test_e01_cotes_concordance.py:608` | Depuis le bon groupe E01, appuis de tous les antécédents consultables comme historiques; aucun appui retenu créé. | Ajouter un antécédent CF3 d’un autre Document partageant un Statement historique : les lignes de l’export E01 du couple initial restent identiques sur ce point. |
| NR08 | C13–C17; T24–T28 | Export E01 conserve codes EX01–EX07, colonnes, cohérence source/cote, citations littérales et reproductibilité d’un même état. | Un échec indépendant de chaque EX continue de bloquer le strict; CF3 ne contourne ni lock ni contrôle de référent. |
| NR09 | C16/C17; T27/T29 (`case_manager/test_e01_cotes_concordance.py:650`, `:810`) | Parcours diagnostique → décisions séparées → strict; suppression historique correctement restituée. | Un groupe de reprise ne couvre pas une occurrence E01 manquante et ne rend pas strict un état probatoire incomplet. |
| NR10 | T11 et nouvelle migration | Valeur de profil héritée conservée, textes/PK/extrémités/M2M inchangés; nouvelles confirmations ajoutent leur manifeste; archives héritées non qualifiées signalées. | Pas de classification par titre, de type d’archive deviné ou de manifeste historique fabriqué. Ancien examen sans manifeste diagnostiqué; retour de migration sur base jetable documente la perte des seules métadonnées nouvelles. |
| NR11 | C09; routes `produced_views.py:230/254` | Requête HTTP d’édition d’une cible partagée détache et préserve la source; suppression autorisée archive. | Requête vers un référent/gel refusée; le chemin ne réalise pas d’écriture partagée. Vérifier les messages et l’absence d’effets partiels. |
| NR12 | C08/C09; archives et VersionTexte | Confirmer V1, réécrire et reconfirmer V2, archiver la cible : les deux décisions, leurs textes et le type du contenu au retrait restent consultables. | Purge Statement/VersionTexte, Document cible ou archive utile : refus si elle détruit l’histoire. Un Statement sans usage ni histoire utile reste supprimable. |

Les tests E01 de services présents ne démontrent pas NR03 dans sa variante partagée, NR07 avec plusieurs profils, ni NR11 par requête HTTP. Ils doivent être ajoutés comme contre-épreuves de ces écarts, sans remplacer les attentes métier existantes par les résultats de l’implémentation testée.

### 8.2 Acceptation CF3 et contre-épreuves

| ID | Scénario et rattachement | Résultat positif attendu | Refus ou résultat interdit |
|---|---|---|---|
| CF3-01 | VF02, analyse danse → demande | Nouveaux LibraryNode et groupes REPRISE_DOCUMENTAIRE; source intacte; numérotation destination; nouveaux usages choisis vers mêmes éléments. | Aucun déplacement des nœuds source, aucune requalification comme juillet, aucune copie de PK/path source. |
| CF3-02 | Analyse A → analyse B | Contextes internes distincts; copie partielle et filiation consultables sans dépôt/transmission. | Impossible d’exiger un ReferentHistorique fictif ou EX04 juillet pour valider cette seule reprise. |
| CF3-03 | VF02, édition après partage | Confirmer la relation nouvelle, modifier la cible puis la source en brouillon; détachement approprié et réexamen des relations concernées. | Modifier l’un changeant silencieusement l’autre, ou confirmation restant courante sur l’ancien Statement détaché. |
| CF3-04 | Reprise conservée/reformulée | Texte conservé traçable même avec un Statement destination distinct; reformulation possède ses captures. | Statement partagé ou même hash considéré comme confirmation automatique de pertinence ou filiation. |
| CF3-05 | Reprise partielle N:M | Deux sources et trois cibles d’un même couple forment un groupe collectif déclaré; toutes les identités et textes examinés sont conservés. | Réduire la fusion à un seul antécédent ou inventer des filières pour un lot dont les liens sont indépendants. |
| CF3-06 | Liens parcimonieux; plusieurs Documents | `s1→t1` et `s2→t2` restent deux groupes. Deux analyses vers une demande donnent des groupes par couple dans une application atomique. | Mettre une occurrence du second Document dans le premier côté SOURCE; prétendre représenter un groupe unique à trois Documents. |
| CF3-07 | VF03, ancêtre hors bloc | Usage de groupe proposé, puis explicitement omis ou rattaché avec portée à une nouvelle cible. | Héritage silencieux, cible destination absente, annulation laissant texte ou usages partiellement copiés. |
| CF3-08 | Appuis sélectionnés | Source avec cinq usages; plan en retient deux et quelques feuilles. Destination contient exactement ces UP/sélections, nouvelles identités et même preuve. | Union de tous les usages source, sélection automatique de racine, seconde autorité par Correspondance. |
| CF3-09 | Nouvelle portée après reformulation/scission | Les candidats sont revus par cible; le plan accepté déclare les portées destination. | Hériter d’une ConfirmationAppui/absence confirmée, ou utiliser la confirmation éditoriale comme validation probatoire. |
| CF3-10 | VF04, reprise à l’identique | Nouvelle insertion remappée au bon Statement/version, composition et usages destination; rendu correct dans cet état. | Réutiliser simplement les offsets/source et conclure qu’ils sont valides car dans les bornes. |
| CF3-11 | VF04, reformulation | Réancrage explicite après changement de texte; ancien rendu source intact. | Cote identique au même offset mais texte examiné différent : aucun faux succès de validation. |
| CF3-12 | VF05, séparation des opérations | Copier le texte seul; créer séparément des usages; déclarer séparément un LienRedactionnel. | Une seule opération créant automatiquement les deux autres. Les options explicites d’un plan restent des décisions séparées. |
| CF3-13 | Réserves et contexte | S3 et ses sous-items de réserve sont repris par défaut; une omission volontaire est identifiée et motivée. | Copie du seul parent présentée comme sous-arbre complet; aucune tentative de détection sémantique automatique prétendument exhaustive. |
| CF3-14 | Prémisses/liens internes | Liens choisis remappés vers les nouvelles occurrences; textes réexaminés si reformulation. | Lien restant sur un ancien numéro ou déclaré courant par simple recapture automatique de la nouvelle prose. |
| CF3-15 | Prémisse hors bloc | Reprise de prémisse ou maintien d’une cible externe explicitement choisie. | Référence manquante, décision non résolue ou cible imaginée à partir d’un paragraphe de même numéro : application refusée. |
| CF3-16 | VF08, analyse V1 gelée → demande D1 | Dépendance vers l’occurrence V1, puis gel D1; analyse V2 modifiée sans effet sur renvoi, textes, examens, usages et rendus V1/D1. | Alias « dernière version » actualisant le renvoi historique; création de V2 modifiant les objets de V1. |
| CF3-17 | VF08, dépendance externe mutable | Brouillon possible avec suivi; gel strict après gel de la cible ou reprise explicite des prémisses. | Gel strict tant que cette dépendance reste sur une analyse externe mutable. Simple RENVOI reste une capture qualifiée selon CF2, sans import d’appuis. |
| CF3-18 | Gel propriétaire de la filiation | Nouvelle demande pouvant référencer une source déjà gelée; sa nouvelle relation appartient à la destination. | Geler la source interdisant toute reprise future; ou reprendre en modifiant une relation déjà incluse dans un contenu gelé. |
| CF3-19 | Archive d’une occurrence liée | Archive lisible avec ancien PK, Document, dernier texte, examen antérieur et motif; relation historique distinguée de la couverture courante. | Extrémité `None` non traitée, perte V1 par CASCADE, source réputée retirée par la seule suppression cible. |
| CF3-20 | Changement de composition après confirmation | Ajouter/substituer une occurrence portant le même Statement, changer rôle/couple/qualification : examen à refaire ou mutation refusée. | Ensembles de versions identiques permettant de conserver l’examen d’autres occurrences. |
| CF3-21 | Numérotation et sous-ensemble | Numéros issus des Documents complets; renvoi actif suit le PK après déplacement; rendu gelé garde ses repères. | Numérotation du bloc isolé utilisée comme numérotation globale, numéro source forcé dans la demande. |
| CF3-22 | Plan périmé / concurrence | Vérification au précontrôle puis sous transaction de source, destination et relations; conflit explicite. | Édition entre rapport et application acceptée sans recontrôle; source gelée pendant la transaction puis modifiée; copie partielle après échec d’usage. |
| CF3-23 | Sources/destination invalides | Analyse PRODUCED avec contexte valide, destination modifiable, éléments sélectionnés cohérents. | Destination gelée, REPRODUCED ou référent; contexte absent; source hors Document; sélection d’une autre preuve; usage visant une autre version : refus atomique. |
| CF3-24 | Rendu et cotes | Résultat destination utilise seulement les sources sélectionnées, une identité documentaire par pièce selon C, cotes qualifiées par version. | Importer tout le bordereau source ou modifier les cotes/associations de juillet pour faire réussir la copie. |
| CF3-25 | Gel / voies de mutation | Gardes exercées sur textes, occurrences, relations, M2M, usages, archives et fichiers conservés. | `update`, bulk, suppression/cascade ou écriture autorisée en brouillon contournant le gel. La seule présence de hashes n’est pas un succès. |
| CF3-26 | Type générique et régime de citation | Seuls les contenus rédactionnels admis sont repris; citations techniques restent sous les adaptateurs/règles de régime existants. | object_id d’un objet non Statement pris pour un Statement de même PK; ancien régime liant silencieusement une citation du nouveau régime. |

Les tests VF02/03/04/05/08 sont ainsi repris sans réduire la non-régression à des tests de copie. L’acceptation exige aussi les cas de mélange de profils et les refus qui protègent juillet et les versions gelées. Les garanties de L5 doivent être vérifiées au niveau où elles s’appliquent réellement, notamment pour les écritures de masse; les tests de services seuls ne les prouvent pas.

## 9. Décisions qui exigent encore approbation

| Décision | Proposition à approuver | Conséquence si non retenue |
|---|---|---|
| CF3-D1 — Autorité de filiation | Solution 2 : même Correspondance/ExtremiteCorrespondance pour A/B/C, nature persistante et consommateurs contextualisés. | Ne pas activer de reprises indépendantes dans ces tables sous le contrat implicite actuel. Réexaminer la solution distincte seulement si un invariant incompatible est établi. |
| CF3-D2 — Examen et transition | Manifestes append-only d’examen des occurrences, avec décisions et empreintes; projections héritées mises à jour par un seul service; correction après détachement; transition sans certification rétroactive. | Définir un autre moyen persistant et démontrable de conserver la composition examinée. Des sets de textes seuls ne satisfont pas le contrôle demandé. |
| CF3-D3 — Portée de reprise | Nouvelles occurrences, plan explicite, groupes par couple, sous-arbre/contexte conservés par défaut et omissions décidées; UP/SelectionPreuve seules autorités des appuis. | Pas d’application automatique d’une reprise dont le contexte, les cibles d’appuis ou les liens restent indéterminés. |
| CF3-D4 — Édition et conservation | Raccordement des chemins actifs aux services; préservation avant réécriture; archives typées et textes examinés protégés; suppression physique PRODUCED maintenue lorsqu’elle ne perd pas l’histoire utile. | Partage de Statements entre rédactions interdit tant que les chemins ne sont pas sûrs; la copie de texte seule ne résout pas les autres garanties CF3. |
| CF3-D5 — Gel | Filiation entrante appartenant à la destination; capture canonique complète; une nouvelle reprise peut viser une source gelée sans la modifier; aucune mutation d’une relation déjà conservée dans un gel. | Pas de gel réel C satisfaisant VF08; pas d’assimilation d’InstantaneReferent au protocole complet. |
| CF3-D6 — Lots et validation | L1 neutre, L2 orchestrateur des usages, rendus L3/L4 et gel L5; matrice ci-dessus comme condition d’acceptation sur environnement isolé. | Ne pas déclarer CF3 complet sur la seule livraison de primitives L1 ou de tests de services hérités. |

Les orientations favorables sur C et CF1–CF4 ne remplacent pas ces approbations. D01–D12 restent en attente de décision consolidée. Cet addendum ne donne aucune autorisation de développer, migrer, lancer L1/L2 ou intervenir sur une branche, PostgreSQL ou le serveur. La publication éventuelle de ce document doit rester séparée des branches validées et faire l’objet d’une instruction ultérieure.

Le verdict est fondé sur les contrats réels : le couple de Documents et les groupes N:M sont réutilisables; la restriction « même acte » n’est pas imposée par une contrainte incompatible. En revanche, la projection des appuis de juillet, les critères de complétude des exports, les examens liés au mauvais Statement après détachement et les chemins d’édition/archivage imposent des adaptations avant extension. La qualification, les manifestes d’examen conservés et le type des archives, avec des corrections ciblées de services/consommateurs, constituent l’extension recommandée; une nouvelle autorité de filiation n’est pas justifiée par les scénarios examinés. La compatibilité reste conditionnée à leur approbation et à leur validation future, pas démontrée par une exécution déjà réalisée.

**CF3 COMPATIBLE AVEC E01 SOUS ADAPTATIONS CIBLÉES**
