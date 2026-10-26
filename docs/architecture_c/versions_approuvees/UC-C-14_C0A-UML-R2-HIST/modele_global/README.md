# Modèle global proposé — G-C0A-R3-CIT

**20 octobre 2026.** UC13 R2-ST est approuvé pour C0A_ISOLER seulement.
La [version exacte G-C0A-R2-ST approuvée](../versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md)
reste inchangée, au manifeste de cd584c3. Le présent R3-CIT est une **proposition**,
sans transfert d’approbation. Code lu 515666e; aucun schéma, code ou patch modifié.

- [ERD](erd_consolide.svg) · [PNG](erd_consolide.png) · [source](erd_consolide.puml).
- [Classes](classes_consolidees.svg) · [PNG](classes_consolidees.png) · [source](classes_consolidees.puml).

Les données représentées existent déjà : deux types Quote sont ajoutés à la
projection pour distinguer le contenu probatoire de l’occurrence éditoriale.
Les FK vers les sources Email/PDF et les champs hors mutation sont résumés;
les GFK ne sont pas transformées en FK vers Statement ou Quote. Aucun journal
ExamenEditorial, champ nature, provenance ou propriété durable ajouté en C0-A.
Les DTO/classes de service proposés restent non persistants et sont étiquetés.

Changements limités aux décisions analysées :

- UC14 proposé : précontrôle d’archivabilité, pas de purge de contenu;
  refus des contenus non Statement faute d’archive typée fidèle.
- UC15 proposé : LectureAppuis + DiagnosticAppui + erreur de contexte distincte;
  agrégation EX04 et strict après collecte; pas de perte d’appuis valides.
- UC02/12 : services ciblés proposés pour intitulé de citation et diagnostic
  d’examen, clairement séparés du cœur et des capacités futures.
- UC13 : copie neuve sur texte différent et ses frontières demeurent celles
  du R2 approuvé; ses quatre vues et son modèle approuvé sont conservés.

UC14/15 font l’objet d’une revue B distincte; leurs choix restent à approuver.
Les sous-cas UC02/12 restent EN_REVUE avec arbitrages CIT-D1–D4 ouverts.
La compatibilité de projection avec UC13 ne vaut pas approbation de R3-CIT.
Les gardes SQL/bulk, gel global, journal et adaptateurs futurs restent leurs lots.

Les sources .puml font autorité; le générateur R1 ne doit pas être relancé.
Compiler uniquement les nouvelles vues concernées, rendre SVG/PNG puis revoir
leurs empreintes. Ne pas régénérer ou modifier les douze fichiers approuvés UC13.
