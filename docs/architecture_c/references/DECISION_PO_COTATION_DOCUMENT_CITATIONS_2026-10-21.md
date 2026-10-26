# Complément au mandat — Décision du Product Owner sur la cotation

Le Product Owner confirme définitivement la règle fonctionnelle suivante :

**La cote principale est attribuée au document source. Les citations extraites de ce document reçoivent des sous-cotes rattachées à cette cote principale.**

Conséquences pour la conception :

1. Un document possède une identité intrinsèque `(modèle, PK)` et une cote calculée dans le contexte de chaque `VersionActe`.
2. Une citation (`EmailQuote`, `PDFQuote`, etc.) possède sa propre identité et conserve son rattachement au document dont elle provient.
3. Une citation ne reçoit pas de cote principale autonome : elle reçoit une sous-cote associée au document coté.
4. Le bordereau détermine les cotes et sous-cotes applicables à chaque version.
5. Le gel de `VersionActe` conserve les associations exactes entre documents, citations, cotes, sous-cotes et utilisations probatoires.
6. La concordance entre versions doit permettre de retrouver les documents malgré leur recotation et les citations malgré les changements de sous-cotes.

Les relations conceptuelles à représenter sont donc notamment :

- `(VersionActe, DocumentSource) → cote`
- `(VersionActe, Citation, DocumentSource) → sous-cote`
- `(VersionActe, occurrence rédactionnelle, utilisation probatoire) → document ou citation sélectionné`

Ces expressions sont des règles fonctionnelles à traduire dans l'ERD; elles ne prescrivent pas des clés primaires physiques.

Cette décision doit être intégrée aux user stories, use cases UC08/09/16/17 concernés, au modèle transversal et au backlog.

Ne présente plus le principe « cote du document / sous-cote des citations » comme un arbitrage ouvert.

Signale seulement les questions techniques résiduelles, notamment les règles exactes d'ordonnancement des citations et le traitement des documents sans citation, si elles ne sont pas déjà déterminées par les décisions existantes.

Aucun développement n'est autorisé par ce complément.
