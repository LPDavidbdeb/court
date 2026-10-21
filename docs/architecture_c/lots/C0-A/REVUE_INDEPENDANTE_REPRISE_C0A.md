# C0-A — Revue indépendante de la reprise

**Agent B — 21 octobre 2026. Verdict : C. NON CONFORME avant intégration.**

Un défaut bloquant subsiste dans UC14 : la garde de concurrence compare un
effectif total, ce qui permet de supprimer une occurrence non contrôlée et
non archivée lorsqu’une autre occurrence a disparu entre-temps. B l’a reproduit
avec deux connexions PostgreSQL, pour un Statement puis une citation.
Une correction locale et une nouvelle vérification ciblée sont nécessaires;
aucune reprise générale de conception n’est demandée.

## 1. Objet et preuves vérifiées

Revue du [patch livré](C0A_REPRISE_DIFF_COMPLET.patch), **110 457 octets**, SHA-256
`fd275e7f4951e7c34686918d875eb1a6cd794e699535a23f345383800ae67708`, et du
[rapport A](RAPPORT_REPRISE_C0A.md), SHA-256
`66430e64b661f4ebc9670ae031d9048f02d87cee3481d34bfcff130da0131bad`.
Le diff du banc arrêté de A est exactement le patch fourni. B l’a reconstruit
sur `515666eb8c6e7fdcdd265f9187c9c37b769b0fed` dans sa propre copie : les huit
fichiers correspondent octet pour octet aux fichiers du banc A.

Références examinées : spécifications, critères et quatre sources UML des
dossiers approuvés [UC13 R2-ST](../../versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md),
[UC14 R2-HIST](../../versions_approuvees/UC-C-14_C0A-UML-R2-HIST/README.md) et
[UC15 R2-DIAG](../../versions_approuvees/UC-C-15_C0A-UML-R2-DIAG/README.md).
Leurs manifestes originaux et tous leurs fichiers sont vérifiés par SHA-256.

| Contrôle | Résultat indépendant |
|---|---|
| Périmètre | Exactement les huit fichiers autorisés; 1 616 insertions, 140 suppressions; aucun autre fichier applicatif du banc A modifié |
| Schéma | Déclarations de champs et classes Meta inchangées dans les deux fichiers de modèles; aucune migration; journal A `No changes detected` vérifié |
| Référence et reprise A | Journaux vérifiés : **205/205** au socle; **267/267** à la reprise; **33/33** pour l’outillage. B n’a pas réexécuté systématiquement ces suites |
| Tests historiques | Comparaison AST : **huit méthodes adaptées seulement**, dont trois renommées; aucune autre méthode historique supprimée/modifiée; **31 méthodes nouvelles** |
| Isolation A | Scripts synthétiques identiques aux scripts conservés; journaux avec refus avant libpq de la connexion externe; socket privé, réglages sans `.env` réel, cluster arrêté. Aucune intervention dans ce banc par B |
| Contre-épreuves B | Copie distincte, nouveau cluster PostgreSQL 18 jetable sans TCP, mêmes scripts d’isolation. **5 méthodes exécutées : 3 témoins A passent, 1 reproduction d’orphelin réussit, 1 méthode de conformité échoue dans ses 2 sous-cas Statement/Quote. Code de sortie 1** |

Les [journaux et le scénario B sont conservés](preuves_revue_B/manifest_sha256.json),
avec leurs empreintes. Le cluster B est arrêté. Le patch et le code applicatif
de A n’ont pas été modifiés; les 670 fichiers applicatifs relevés dans le dépôt
partagé restent identiques. Aucun commit, push, fusion ou déploiement effectué.

## 2. B01 — Blocage : une égalité d’effectifs masque une suppression sans archive

**Références : UC14 AC01–AC04 et AC06; ACT14-GARDE/TYPE/ARCH/DELETE/ROLLBACK;
SEQ14-BLOC/ARCH/DELETE/ROLLBACK.** Localisation : `supprimer_occurrence`,
`document_manager/concordance.py`, lignes 369–400 de l’état reconstitué.

Entrelacement démontré, sans écriture SQL de contournement :

1. T1 charge et précontrôle le bloc **P, E1, E2** : trois occurrences.
2. Avant sa première archive, T2 retire E1 par le service habituel, puis ajoute
   E3 sous P par `add_child`; ces opérations sont validées sur une autre connexion.
3. T1 archive son ancienne liste. Le retrait de E1 retourne **0**; celui de
   E2 retourne **1**. Treebeard retire ensuite P **et E3**, soit **2** occurrences.
4. La somme **0 + 1 + 2 = 3** satisfait la garde; aucun nœud ne reste sous P.
   T1 répond succès, en annonçant P/E1/E2. **E3 a disparu sans aucune archive.**

Les deux variantes B produisent ce résultat. Lorsque E3 porte une Quote,
le service retire aussi un contenu que C14-D2 lui impose de refuser faute
d’archive fidèle. Les objets de contenu ne sont pas purgés, mais l’identité,
l’intitulé, la position et le rattachement documentaire de cette occurrence
ne sont pas conservés par une archive. Le retour ne désigne pas les occurrences
réellement retirées.

**Ce défaut est bloquant pour C0-A.** Il retire effectivement une occurrence
hors du bloc archivé par UC14; il ne peut pas être reporté à la seule garantie
globale de L5. Les transactions sont présentes, mais aucun refus ne déclenche
leur annulation puisque la garde accepte une égalité trompeuse.

**Correction minimale attendue de A :** dans le service et ses gardes locales,
vérifier les identités des occurrences effectivement retirées contre celles
du bloc précontrôlé et archivé. Une occurrence manquante ou supplémentaire
doit provoquer `SuppressionRefusee` et le rollback du service, sans compensation
entre un retrait nul et un retrait multiple. Dans le parcours du bas vers
le haut, chaque retrait doit porter sur l’occurrence attendue seule; conserver
les gardes ORM et la cohérence des compteurs Treebeard. Une garde au passage
du collecteur ORM peut contrôler les identités sans verrouillage général.

Ajouter la contre-épreuve de remplacement à effectif constant dans le fichier
de tests autorisé, pour Statement et Quote. Attendu : refus atomique, aucune
archive de T1 conservée, aucune suppression par T1 des nœuds restants; les
opérations déjà validées de T2 restent conservées. Les corrections tiennent
dans `concordance.py`, éventuellement `protection.py`, et les tests autorisés.

## 3. Orphelin tardif signalé par A : reproduction et qualification

B a reproduit un chemin utilisant la **vue réelle `ajax_add_node`** :

1. T1 a retiré P dans sa transaction et vient de lire le contrôle final vide.
2. T2 lit encore P, visible avant le commit de T1, puis prépare l’ajout d’un enfant.
3. L’UPDATE Treebeard du compteur de P attend le verrou de suppression détenu par T1.
4. T1 valide. L’UPDATE de T2 ne retrouve plus P; Treebeard n’exige pas une ligne
   mise à jour et insère l’enfant sous l’ancien chemin de P.
5. L’ajout répond **200/success**. L’enfant et son Statement existent, mais le
   parent manque. `_get_and_process_tree` ne le rattache à aucun parent et
   **ne l’affiche pas dans l’éditeur**.

Le texte n’est pas détruit; le lien parent/enfant devient incohérent et le
succès d’ajout masque une occurrence invisible. Ce risque est distinct de B01 :
T1 n’a pas supprimé cet enfant, créé après son contrôle. Il relève de la voie
d’ajout sur parent périmé (UC02) et de la coordination concurrente de l’arbre,
explicitement non garantie par UC14. **Pris isolément, il reste une réserve
non bloquante du profil C0-A borné, après correction de B01.** Son incidence
rédactionnelle justifie un traitement ciblé avant un usage concurrent soutenu.

Une correction locale est plausible pour cette voie : charger et verrouiller
le parent avec `select_for_update()` dans la transaction existante de l’ajout,
puis refuser l’ajout si le parent a disparu après attente. Le fichier est déjà
dans la liste des huit, mais l’action `ajax_add_node` sort du périmètre fonctionnel
édition/suppression du mandat actuel : prévoir un avenant ciblé. Un verrou ou
un contrôle supplémentaire dans la seule suppression ne ferme pas les créations
après son commit. Les autres voies d’ajout/déplacement restent à qualifier dans
UC02/L5; aucune refonte générale n’est requise pour corriger la voie démontrée.

## 4. Conformité des corrections et des tests

| Élément | Conclusion |
|---|---|
| C0A-ST-01 / UC13 | Corrigé : aucun changement de texte en place, objet neuf même pour un privé apparent; texte égal sans détachement; protections, fraîcheur identité/empreinte et rollback couverts |
| C0A-14-01 / UC14 | Conservation sans purge et refus des contenus non archivables implantés au nominal; **garantie de bloc encore non conforme à cause de B01** |
| C0A-REV-01 / UC15 | Corrigé : appuis valides et diagnostics locaux conservés dans plusieurs ordres, erreurs globales distinctes, pannes propagées, EX04 enrichi et EX01–EX07 cumulatifs; aucune confirmation créée |
| 403 JSON et 404 | Conformes aux réponses lisibles et au 404 déjà dessinés. Compatibilité du JSON vérifiée par lecture du JavaScript existant et des tests HTTP; aucun parcours navigateur réalisé par B |
| Garde de concurrence ajoutée | Correction pertinente à périmètre constant pour l’ajout simple; les trois témoins concurrentiels A passent aussi chez B. Sa vérification agrégée reste insuffisante dans B01 |

Les huit adaptations historiques sont justifiées, sans affaiblissement identifié :

| Test adapté | Pourquoi l’attente change et ce qui reste vérifié |
|---|---|
| T22 — `statement_exclusivement_produced…` | AC05 UC14 : contenu conservé; occurrence retirée, archive et texte vérifiés |
| T23 — `les_appuis_d_origine_restent_consultables…` | AC04 UC15 : mêmes appuis dans `appuis_valides`, complétude et absence d’anomalie ajoutées |
| T23 — `une_scission_ne_confirme_pas…` | Résultat qualifié; un appui par cible et absence de confirmation automatique préservés |
| Patch — `edition_privee…` | AC03 UC13 : objet neuf et ancien texte/capture conservés, au lieu d’une réécriture en place |
| Patch — `identifiant_generique…purge…` | AC02 UC14 : refus total, aucune archive, Event et Statement homonyme intacts |
| Patch — `lecteur_restreint_au_couple…` | Même couple et même pièce vérifiés via le nouveau résultat; lecture complète |
| Patch — `identifiant_generique_ne_designe_pas…` | Diagnostic de type remplace ValueError/note libre; aucun faux appui, EX04 et strict refusés |
| Patch — `archive_non_typee…` | Archive identifiée dans le diagnostic; aucun appui deviné, EX04 et strict refusés |

Les nouveaux tests vérifient les POST, refus sans effets, captures avant/après,
échecs après écritures, archivage, conservation des décisions, lectures mixtes,
permutations et strict cumulatif. Leur lacune décisive est le remplacement
concurrent à effectif constant. Le journal `dev1-e01` confirme huit méthodes
en échec avant adaptation. **Précision de comptage :** la contre-épreuve du
patch historique contient 20 méthodes distinctes en échec, avec 31 incidents
de sous-cas (11 failures, 20 errors), plutôt que les 21 méthodes annoncées.
Cette imprécision du rapport ne change pas le diagnostic fonctionnel.

## 5. Limites de l’éditeur et incidence rédactionnelle

- **Texte refusé encore affiché :** l’alerte est désormais exploitable, mais
  le texte présenté peut diverger de l’état enregistré jusqu’au rechargement.
  La base reste protégée; ce comportement ne contredit pas le contrat C0-A
  borné. Correction UX à prioriser dans L1-B/UC02, sans l’annoncer livrée ici.
- **Citations non modifiables/non supprimables :** conforme aux refus approuvés
  d’UC13 et C14-D2. Cela empêche concrètement de retirer/remplacer une citation
  déjà insérée, et bloque aussi le retrait d’un bloc qui en contient une.
  C’est une capacité manquante importante pour la rédaction et la restructuration
  d’un acte utilisant des citations; sa fréquence réelle n’a pas été mesurée.
  Prioriser le parcours rédactionnel concerné et l’archivage fidèle nécessaire
  à la levée de C14-D2. UC12 seul ne rend pas les citations éditables/supprimables.
  Aucune implantation UC02/UC12 ni conversion HERITE/PHRASE n’a été entreprise.

## 6. Décision proposée

**Ne pas préparer la promotion du patch actuel vers l’intégration avant B01.**
Demander à A cette correction locale et ses deux contre-épreuves, puis les
régressions affectées et la suite du socle sur PostgreSQL jetable. B pourra
revoir le delta et les résultats sans recommencer les dossiers UML ni les
analyses déjà acquises. L’orphelin tardif et les limites de l’éditeur restent
des réserves explicitement affectées; L1-A/C0-B et L5 ne sont pas réputés livrés.
Aucune fusion, aucun déploiement et aucun lot suivant ne découlent de ce rapport.
