# UC14 — Spécification technique limitée R3-CONC

**Proposition du 23 octobre 2026.** Préalable : [revue indépendante](validation.md)
puis approbation utilisateur de cette version exacte. Aucun code modifié.
Socle applicatif : `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`, patch de
reprise puis delta B01 de `f35ec8586866f4359d44f52a0bc5cc57c0804217`.

## Contrat approuvé conservé

Les sept lignes suivantes sont reprises textuellement de la spécification
UC14 R2-HIST. Leur approbation historique reste celle du 20 octobre 2026,
commit `30724df7ec5cbd1aba8ef25d59b5c3a162d20dab`, PR #31.

| AC | Critère observable |
|---|---|
| AC01 | Précontrôler tout le bloc avant la première archive. REPRODUCED, référent ou protection historique, ConfirmationAppui ou AncrageCitation détruit par la cascade : refus total. |
| AC02 | Seuls les Statement réels vérifiés par ContentType/PK et les structures sans type ni objet sont archivables dans ce profil. Autre contenu, objet manquant ou GFK incohérente : refus total avant écriture; jamais de faux Statement ou d’archive citation vidée de son contenu. |
| AC03 | Archiver chaque occurrence autorisée : Document, ancien ID, path/depth, item, paragraph_number, texte et empreinte disponibles, motif. statement_pk seulement pour Statement vérifié; un texte Statement vide reste distingué d’une structure sans contenu. |
| AC04 | Basculer toutes les extrémités concernées de noeud vers archive, puis supprimer les occurrences du bas vers le haut. Conserver relations, anciennes décisions et captures; une archive consultable n’est pas un appui courant. |
| AC05 | Ne purger automatiquement aucun Statement ni VersionTexte dans C0-A. Un contenu devenu sans occurrence n’est ni détruit ni déclaré réutilisable. Ne pas déduire provenance ou propriété de son nombre d’usages; la propriété durable reste L1-A. |
| AC06 | Archives, repointages et suppressions forment une opération atomique de service. Échec à toute étape : rollback complet avant interception HTTP, y compris les éventuelles nouvelles archives; refus 403 lisible, erreur technique 500, aucun succès partiel. |
| AC07 | Les gardes ORM prévues du patch continuent de refuser la destruction des captures utilisées, archives liées et Documents nécessaires. Aucun contournement par suppression directe n’est promis fermé globalement par C0-A : SQL/bulk et gel restent L1-A/C0-B/L5. |

## Garanties techniques proposées pour satisfaire ce contrat

| ID | Garantie à démontrer par la future correction |
|---|---|
| G01 | Le plan attendu contient l'ensemble exact des occurrences et leurs états, pas seulement un effectif. Aucun membre supplémentaire n'est accepté par compensation. |
| G02 | T1 protège les lignes du bloc et les parents nécessaires aux compteurs Treebeard; elle relit et compare les états après acquisition effective. Un plan modifié est refusé en entier. |
| G03 | Les textes Statement utilisés sont stabilisés et vérifiés avant archivage. Les archives sont constituées depuis les états rechargés et protégés effectivement retirés. |
| G04 | Les protections restent effectives pendant les gardes, le DELETE SQL et jusqu'au commit de la transaction externe; un savepoint relâché ne marque pas la fin de cette durée. |
| G05 | T2 validée avant protection effective de T1 entraîne le refus de T1 si l'état attendu diffère. Le commit T2 et ses données restent conservés. |
| G06 | T2 bloquée par T1 reprend après finalisation. Si T1 a supprimé la cible, l'édition HTTP ou la sauvegarde ORM existante refuse sans recréer la ligne, même par un save sans update_fields. |
| G07 | Si T1 est annulée, archives, repointages, compteurs et retraits de T1 sont annulés ensemble. T2 peut reprendre sur l'état restauré après ses propres contrôles. |
| G08 | Les ensembles connus de plusieurs lignes sont protégés dans un ordre commun; un refus annule toute l'opération concernée. Une transaction déjà validée sur une autre occurrence n'est pas annulée. |
| G09 | Gardes ORM, API Treebeard, refus des contenus citation et conservation des contenus/captures restent effectifs. Aucun nouveau schéma ou gel global n'est introduit. |
| G10 | UC13 conserve son contrat de détachement neuf sur texte distinct, ses captures et son atomicité. La barrière d'existence intervient avant ses écritures; une cible disparue pendant l'opération produit un refus 403, distinct du 404 initial. |

G01–G10 explicitent le mécanisme nécessaire; ils ne constituent pas de
nouveaux résultats exécutés. Les [essais prévus](plan_tests.md) restent tous
NON EXECUTES pour R3-CONC. Le candidat antérieur est toujours bloqué.

Les classes/services proposés sont des interfaces de conception, sans
engagement sur leur découpage exact en fonctions Python. Un changement de
contrat approuvé, un fichier hors périmètre, ou l'impossibilité de fermer
la fenêtre avec ce mécanisme doit être signalé avant toute extension.
