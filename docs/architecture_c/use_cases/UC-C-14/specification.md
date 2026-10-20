# UC-C-14 — Suppression autorisée et archives disponibles

**C0A-UML-R1 — 20 octobre 2026 — C0-A — EN_REVUE.** Auteur : B; implantation
future : A. Approbation utilisateur : **AUCUNE**. Socle proposé `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`;
modèle global [G-C0A-R2-ST](../../modele_global/README.md).

Comme rédacteur, supprimer une occurrence PRODUCED et ses descendants autorisés
en conservant les traces disponibles, sans détruire une décision incompatible
avec la suppression. Sources : US-C-14, CF3-D4, NR01/11/12 pour le seul périmètre
C0-A, autorisation historique §10.5. Précondition : POST vers `ajax_delete_node`;
autre méthode : 405; cible absente : erreur sans mutation.

| AC | Critère observable |
|---|---|
| AC01 | Précontrôler tout le bloc avant la première archive. Un référent, REPRODUCED, une ConfirmationAppui ou un AncrageCitation détruit par la cascade entraîne un refus total. |
| AC02 | Pour une suppression autorisée, archiver chaque occurrence, son ancien ID, Document, position, texte disponible, empreinte et motif avant toute suppression. Un `statement_pk` n’est rempli que si le type est Statement vérifié. |
| AC03 | Basculer chaque extrémité concernée de `noeud` vers l’archive; conserver la filiation et permettre sa consultation historique. Une archive non typée ne sert pas à reconstituer un appui par égalité numérique. |
| AC04 | Supprimer du bas vers le haut, puis purger uniquement les candidats Statement vérifiés sans autre occurrence, protection, appui historique ni capture utilisée. Conserver les objets encore utiles. |
| AC05 | L’échec de capture, de garde ou d’écriture annule tout le service, avant son catch HTTP; aucun bloc, archive ou repointage partiel ne subsiste. |
| AC06 | Les captures utilisées, archives liées et Documents nécessaires aux concordances refusent leur suppression par les voies ORM gardées du patch. Ne pas présenter ces gardes comme une protection SQL/bulk globale. |

Nominal : déterminer le bloc → précontrôler chaque membre → transaction de
service : archives → repointage des extrémités → retrait des occurrences →
purge conditionnelle → retour des IDs. Refus métier : 403; échec inattendu :
500. Le service `@transaction.atomic` est imbriqué dans la transaction HTTP;
ses exceptions annulent son savepoint avant interception par la vue.

Variantes : Statement partagé conservé; Statement privé encore examiné conservé;
homonyme GFK d’un autre modèle jamais purgé; archive existante nécessaire à une
concordance non supprimable. Le seul retrait d’une cible ne devient pas une
décision E01 de retrait de son antécédent.

Limites : aucune archive typée nouvelle, aucun journal exhaustif des décisions,
aucune garantie de gel SQL/stockage. L1-A/C0-B/L5 les complètent. Pas de promesse
universelle de sérialisation d’éditions/suppressions simultanées. Conception :
contrat de capture de 13; exécution : même mandat/copie indépendante/DB jetable
que C0-A; validation sur le nouveau socle encore à autoriser.

Vues : [activité](activity.svg) ([source](activity.puml)),
[séquence](sequence.svg) ([source](sequence.puml)),
[ERD](erd.svg) ([source](erd.puml)),
[classes](class.svg) ([source](class.puml)).
[Traçabilité](tracabilite.md) · [Validation](validation.md).


## Impact documentaire ST-R1

Le [contrat de provenance et propriété](../../INVARIANTS_STATEMENT_REPRODUCED_PRODUCED.md)
complète ce dossier. Critères et quatre vues locales R1 sont inchangés;
le contexte global est G-C0A-R2-ST. Les conséquences propres à ce use case
et les limites L1-A/C0-B figurent au §7 de la [validation](validation.md).
Aucune approbation, correction du patch ou attestation F/A supplémentaire.
