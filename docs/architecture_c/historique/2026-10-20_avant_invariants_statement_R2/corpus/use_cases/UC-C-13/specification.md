# UC-C-13 — Modifier une occurrence partageant un Statement

**Dossier C0A-UML-R1 — 20 octobre 2026 — lot C0-A.** Concepteur/réviseur
documentaire : Agent B; implantation et corrections futures : Agent A.
**Approbation utilisateur : aucune.** Statut courant dans le
[registre](../../registre_validation.md); preuves dans [validation](validation.md).

## Contrat et périmètre

Comme rédacteur, je veux modifier une occurrence sans réécrire le contenu des
autres occurrences partageant le même Statement, et retrouver les captures
disponibles des décisions antérieures.

Sources : D03/CF3-D4, US-C-13 initiale, V2:US-02.AC01/02/04/05,
autorisation historique C0-A §10.5 du registre consolidé. Base observée proposée :
`515666eb8c6e7fdcdd265f9187c9c37b769b0fed`; P6 reste la base du patch.
Modèle global cible : [G-C0A-R1](../../modele_global/README.md).
La cible représente le comportement du patch non appliqué et son périmètre
autorisé initial; sa conformité dynamique au nouveau socle reste à éprouver.

Acteur : rédacteur dans l’éditeur existant. Déclencheur : POST de texte/item
sur `ajax_edit_node(request, node_pk)`. Entrées : identité de l’occurrence et
formulaire validable. Précondition de mutation : Document PRODUCED non référent,
contenu Statement vérifié ou occurrence structurelle sans type ni objet.
GET demeure une lecture; occurrence absente : 404; formulaire invalide : 400.

## Critères d’acceptation

| ID local | Résultat observable |
|---|---|
| AC01 | Une occurrence REPRODUCED ou référent historique refuse toute édition, y compris `item`; textes, associations et captures restent inchangés. |
| AC02 | Pour un texte différent porté par un Statement partagé ou protégé, capter l’ancien texte puis créer un Statement privé et repointer uniquement l’occurrence éditée. Les autres occurrences et leurs textes restent identiques. |
| AC03 | Pour un Statement privé mutable, conserver la capture avant modification, modifier son texte, puis capter le résultat. Les captures encore utilisées restent consultables. |
| AC04 | Texte identique : aucun détachement ou capture supplémentaire; `item` peut changer si autorisé. Sur une occurrence sans type ni objet, créer le premier Statement. Un autre type ou une GFK incohérente est refusé. |
| AC05 | À la lecture d’une ConfirmationAppui confirmée ou SANS_APPUI, recharger l’occurrence réelle et comparer Statement associé et empreinte à la capture. Autre texte ou autre Statement, même à texte égal : A_REEXAMINER; décision stockée et ancien texte conservés. |
| AC06 | Le traitement éditorial d’une Correspondance compare le Document et les couples Statement/empreinte aux captures des deux rôles. Divergence de ces valeurs source ou cible : à réexaminer, sans réécrire l’ancienne décision. L’identité complète des compositions d’occurrences reste à L1-A/C0-B. |
| AC07 | Capture, duplication éventuelle, repointage, texte et `item` appartiennent à l’opération atomique. Une exception tardive annule l’ensemble, y compris les nouveaux objets. Un refus ne laisse aucun effet partiel. |
| AC08 | Ni schéma ni migrations modifiés. Identité/numéro de l’occurrence et contenus historiques non édités restent intacts; aucun texte Quote HERITE/PHRASE n’est assimilé à un Statement. |

## Nominal, variantes et refus

1. Charger occurrence, type et Document; valider le formulaire et les gardes.
2. Si Statement et texte différent : capter l’ancien texte, vérifier partage et
   protection, détacher si nécessaire, puis capter le texte résultant.
3. Sauver `item` dans la même transaction HTTP. L’atomicité du service est
   imbriquée; une erreur remonte pour annuler également la vue.
4. Répondre après sortie de la transaction. Les lecteurs calculent ensuite
   l’état courant sans écraser les décisions historiques.

Variantes : texte égal; Statement privé; partage dans un même Document ou entre
Documents; protection par une occurrence source; occurrence initialement vide.
Refus : référent/REPRODUCED, contenu incompatible, validation ou garde tardive.
Annuler avant POST n’écrit rien; une exception dans le traitement provoque le
rollback, pas un nettoyage compensatoire après succès.

## Limites et dépendances

Pas de journal ExamenEditorial, qualification `nature`, manifeste complet
des occurrences ni protection globale d’une version gelée : L1-A/C0-B/L5.
La comparaison par ensembles Statement/empreinte du patch ne prouve pas
l’identité complète des occurrences d’un ancien examen (CF3-20 reste L1-A).
Les anciennes captures disponibles sont protégées; l’histoire manquante n’est
pas reconstruite. Les signaux ORM ne sont pas des gardes SQL/bulk universelles.

Le patch n’ajoute pas de verrou `select_for_update` ni de protocole empêchant
toutes les éditions concurrentes. Le dossier exige le rollback par opération;
il ne promet pas la sérialisation de toutes les modifications simultanées.
Les protections globales et conflits de plan restent dans leurs lots dédiés.

Conception : G-C0A-R1 et contrats de fraîcheur existants. Exécution future :
mandat sur socle approuvé, copie Git et PostgreSQL jetable indépendants de A.
Validation : tests E01 et régime A du SHA, contre-épreuves du patch et revue
de conformité avant intégration. Aucun R01–R08 n’est nécessaire à ce périmètre.

## Vues et preuves

- [Activité](activity.svg) · [source](activity.puml)
- [Séquence](sequence.svg) · [source](sequence.puml)
- [ERD cible local](erd.svg) · [source](erd.puml)
- [Classes et composants](class.svg) · [source](class.puml)
- [Traçabilité et tests](tracabilite.md) · [validation et empreintes](validation.md)
