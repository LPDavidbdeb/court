# UC-C-14 — Supprimer les occurrences sans perdre leur histoire

**C0A-UML-R2-HIST — 20 octobre 2026 — contrat conservateur proposé C0-A.**
Socle lu : 515666e; modèle global G-C0A-R3-CIT. Approbation utilisateur :
**AUCUNE**. Le patch conservé n’est pas modifié; aucun développement autorisé.
Sources : ST01–ST05, NR01/11/12 partiel, CF3-D4, [mandat](../../references/MANDAT_APPROBATION_UC13_VALIDATION_C0A_2026-10-20.md).
[Recommandations C14-D1/D2](../../ANALYSE_CIBLEE_CITATIONS_C0A.md#4-conservation-lors-dune-suppression--recommandations-uc14).

Acteur : rédacteur; déclencheur : POST ajax_delete_node. Méthode différente :
405; cible absente : 404 sans mutation. Le bloc comprend la cible et tous ses
descendants; aucune sélection implicite de ceux qui seraient supprimables.

| AC | Critère observable |
|---|---|
| AC01 | Précontrôler tout le bloc avant la première archive. REPRODUCED, référent ou protection historique, ConfirmationAppui ou AncrageCitation détruit par la cascade : refus total. |
| AC02 | Seuls les Statement réels vérifiés par ContentType/PK et les structures sans type ni objet sont archivables dans ce profil. Autre contenu, objet manquant ou GFK incohérente : refus total avant écriture; jamais de faux Statement ou d’archive citation vidée de son contenu. |
| AC03 | Archiver chaque occurrence autorisée : Document, ancien ID, path/depth, item, paragraph_number, texte et empreinte disponibles, motif. statement_pk seulement pour Statement vérifié; un texte Statement vide reste distingué d’une structure sans contenu. |
| AC04 | Basculer toutes les extrémités concernées de noeud vers archive, puis supprimer les occurrences du bas vers le haut. Conserver relations, anciennes décisions et captures; une archive consultable n’est pas un appui courant. |
| AC05 | Ne purger automatiquement aucun Statement ni VersionTexte dans C0-A. Un contenu devenu sans occurrence n’est ni détruit ni déclaré réutilisable. Ne pas déduire provenance ou propriété de son nombre d’usages; la propriété durable reste L1-A. |
| AC06 | Archives, repointages et suppressions forment une opération atomique de service. Échec à toute étape : rollback complet avant interception HTTP, y compris les éventuelles nouvelles archives; refus 403 lisible, erreur technique 500, aucun succès partiel. |
| AC07 | Les gardes ORM prévues du patch continuent de refuser la destruction des captures utilisées, archives liées et Documents nécessaires. Aucun contournement par suppression directe n’est promis fermé globalement par C0-A : SQL/bulk et gel restent L1-A/C0-B/L5. |

Nominal : valider la requête → charger le bloc → vérifier mutabilité,
décisions/cascades et archivabilité de chaque membre → créer les archives →
repointage des extrémités → supprimer les nœuds du bas vers le haut → conserver
tous les contenus → commit et retour des identifiants retirés/archives.
La liste statements_supprimes reste vide dans ce profil; aucun collecteur
externe n’est lancé comme effet secondaire.

Refus avant écriture : un seul descendant protégé ou non archivable fait
refuser tout le bloc. Les gardes finales restent actives; leur refus après
création d’archives annule la transaction de service imbriquée dans celle de
la vue. Aucun verrou général des arbres ou gel universel n’est annoncé.
Les conflits de modification simultanée doivent être contre-éprouvés sur
base jetable lors du mandat d’implantation, pas supposés résolus par atomic.

Après succès, le dernier texte et les anciennes captures restent consultables.
L’examen antérieur reste stocké; son applicabilité courante change lorsque
l’extrémité devient archivée. UC15 diagnostique l’archive non typée au lieu de
reconstituer un Statement depuis son ancien identifiant. L1-A/C0-B conserveront
plus finement les identités typées et le contexte d’examen.

## Décisions soumises avec les vues

**C14-D1 :** conserver tous les contenus, sans purge automatique C0-A.
**C14-D2 :** refuser les contenus non Statement faute d’archive typée fidèle.
Ces recommandations évitent de détruire une origine inconnue ou la trace d’une
citation. Elles restent à approuver expressément dans ce dossier. L’alternative
purge/archivage partiel n’est pas considérée acquise par le comportement actuel.

Le patch a une purge conditionnelle et autorise certains contenus génériques :
écart **C0A-14-01**. Ses tests sont conservés comme résultats historiques;
les nouvelles contre-épreuves sont NON EXECUTEES. Aucun schéma ou journal
nouveau en C0-A; aucune activation anticipée de L1-A ou de L5.

[Vues et sources](activity.svg) : [activité](activity.puml), [séquence](sequence.svg)
([source](sequence.puml)), [ERD](erd.svg) ([source](erd.puml)),
[classes](class.svg) ([source](class.puml)).
[Traçabilité](tracabilite.md) · [Validation B](validation.md) · [Empreintes](manifest_sha256.json).
Version R1 préservée au [commit cd584c3](https://github.com/LPDavidbdeb/court/tree/cd584c307fcc31096dd93daae6a8fc26ab949eaf/docs/architecture_c/use_cases/UC-C-14).
