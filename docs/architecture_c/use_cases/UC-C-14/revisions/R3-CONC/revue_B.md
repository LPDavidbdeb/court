# Attestation indépendante B — UC14 R3-CONC

**23 octobre 2026 — VALIDE_ARCHITECTURE pour la conception uniquement.**
Relecteur : agent distinct `/root/revue_uc14_r3`. Revue sollicitée explicitement
par le mandat utilisateur; effectuée en lecture seule, sans écriture de
fichier, Git, banc ou base. Le présent document restitue son attestation et
ses réserves, reçues dans la session, avec des liens locaux adaptés.

**Aucun écart bloquant identifié dans le dossier examiné. Ce verdict ne
valide aucun code et ne lève pas le blocage du candidat `f35ec85`.**

## Pièces examinées et intégrité

Le [manifeste de conception](manifest_conception.json) comporte 27 fichiers.
SHA-256 vérifié indépendamment :
`258ca9a719c0b172461f75dc5f27bb98b74335b532340c00654b5165f7e87b0d`.
Les 27 empreintes et celle de la dépendance de style correspondent.
Sept PNG inspectés visuellement. Vérification indépendante du relevé
préalable : 671 fichiers suivis hors docs/legal contrôlés, dont le code
applicatif, et 206 documents protégés, sans différence.

| Axe | Attestation indépendante |
|---|---|
| Technique | VALIDE_ARCHITECTURE. Plan attendu, acquisition effective, relecture comparative et verrous jusqu'au commit externe sont associés. RELEASE SAVEPOINT est distingué de la fin de transaction. Parents Treebeard, Statement archivés et instances périmées ont des protections identifiées. |
| Fonctionnel | VALIDE_ARCHITECTURE. Les deux issues conformes sont représentées : modification T2 validée avant protection puis refus T1; ou protection T1, attente T2, retrait validé puis refus T2 sans résurrection. Les annulations distinguent les écritures non validées des transactions indépendantes committées. |
| Architectural | VALIDE_ARCHITECTURE. Quatre vues principales et trois compléments cohérents; sept critères UC14 repris exactement. ERD inchangé sauf chemin d'inclusion. Impact technique UC13 explicite sans transfert d'approbation. Aucun schéma nouveau nécessaire à la solution proposée. |

## Constats déterminants

- L'[analyse](analyse_coherence.md#2-protection-locale-recommandée) prévoit
  un archivage à partir des lignes rechargées après protection et maintient
  celle-ci pendant les gardes, le SQL et le commit externe. Elle ferme
  conceptuellement la fenêtre sans compter sur une dernière lecture seule.
- La [séquence principale](sequence.puml) expose les cas A/B, l'attente et
  le refus sans INSERT de substitution.
- Les [classes](class.puml) assignent les parents Treebeard, LibraryNode.save,
  l'ordre des protections et les erreurs transactionnelles. La lecture du
  Treebeard installé confirme son appel à parent.save avant la suppression ORM.
- Le [plan T01–T24](plan_tests.md) couvre les variantes requises. T05/T06/T07
  doivent discriminer l'ancien candidat par une violation de conformité;
  un timeout ne peut servir de reproduction.
- L'orphelin tardif demeure distinct et expressément non corrigé.

## Vérifications impératives sur le futur candidat

1. Les instances rechargées sous verrou doivent réellement remplacer les
   anciennes pour contrôler et archiver. Aucun cache content_object, de
   relation ou de descendants ne doit réintroduire l'état ancien.
2. Connexion et alias doivent rester identiques pour protection, archives,
   sauvegardes, retraits et transaction externe.
3. L'ordre doit être effectif, inclure les parents et ne pas être contredit
   par une acquisition tardive. Aucune garantie générale contre tous les
   ajouts ou déplacements d'arbre n'est acquise par les verrous locaux.
4. Vérifier UPDATE seul sans update_fields, avec update_fields et contre
   force_insert sur ancienne instance, tout en préservant la création neuve.
5. Les observations PostgreSQL doivent prouver l'attente réelle, les deux
   ordonnancements, les rollbacks et la fidélité des archives.

**Tests applicatifs exécutés dans cette revue : aucun.** Les scénarios R3
restent NON EXECUTES. Le candidat antérieur reste NON CONFORME; l'implantation
attend l'approbation explicite de l'utilisateur.
