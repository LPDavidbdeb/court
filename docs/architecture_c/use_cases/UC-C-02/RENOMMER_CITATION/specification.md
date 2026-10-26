# UC-C-02::RENOMMER_CITATION — Intitulé rédactionnel distinct du contenu

**CIT-UML-R1 — 20 octobre 2026 — EN_REVUE; aucune approbation.**
Quatre vues d’un sous-cas proposé, pas validation de tout UC02. Modèle global
G-C0A-R3-CIT; source [analyse CIT-D1/D2](../../../ANALYSE_CIBLEE_CITATIONS_C0A.md).
Socle lu 515666e; lot naturel L1-B. Une extension limitée C0-A exigerait
approbation du sous-cas et mandat supplémentaire de fichiers, non délivrés.

Acteur : rédacteur; action distincte RENOMMER_OCCURRENCE sur une occurrence
portant EmailQuote ou PDFQuote. Le contrat UC13 approuvé reste inchangé :
ce sous-cas n’emprunte pas sa branche d’édition de texte et ne transforme pas
la citation en Statement. Noms d’endpoint/service proposés, non existants.

| AC | Critère proposé |
|---|---|
| AC01 | Document PRODUCED éditable et occurrence non protégée seulement; REPRODUCED, référent ou version protégée : refus intégral, y compris item. |
| AC02 | Requête explicite item seul, avec cible et état attendu. Champ de contenu, repointage ou régime demandé : refus; jamais de création de Statement ou sauvegarde de Quote. |
| AC03 | Résoudre la citation par type complet, PK et régime via gestionnaire explicite HERITE/PHRASE. Absence, type incompatible ou ambiguïté : refus; aucun fallback de PK ou derived_from. |
| AC04 | Intitulé demandé comme présentation, genre et numérotation du Document entier inchangés, sans examen/relation/ancrage ou dépendance contextuelle affectable. Sinon ou si indéterminable : refus explicite; pas de décision ancienne reconfirmée. |
| AC05 | Dans une opération locale atomique, recharger la cible, recontrôler les préconditions et l’état attendu puis sauver seulement item. Conflit détecté : refus 409; erreur : rollback. Association, quote_text, source, ancres, certification et autres occurrences restent identiques. Texte inchangé n’entraîne aucune copie. |
| AC06 | Afficher succès/refus et son motif de façon exploitable; le client ne masque pas un HTML 403 en échec JSON silencieux. Aucun chemin de rendu PHRASE ou contrôle de A n’est activé par ce renommage. |

Un intitulé identique est un no-op. Le calcul de genre/index n’établit pas
l’absence d’effet sémantique : dès qu’une dépendance d’examen est possible et
non conservable, ce profil refuse. Le changement de rôle ou de portée reste
L1-B avec manifeste L1-A/C0-B. Une certification ineffective est un diagnostic
probatoire distinct; elle n’autorise aucune écriture de citation.

**Arbitrage CIT-D1/D2 ouvert :** recommander ce renommage limité par action
distincte, ou différer tous les renommages de citations à L1-B. La règle 403
actuelle n’est pas approuvée par défaut. L’élargissement des routes/formulaires/
interface sort des huit fichiers du patch et devra être signalé avant code.
Quatre vues disponibles pour la revue; toutes les contre-épreuves sont NON EXECUTEES.

[Activité](activity.svg) · [Séquence](sequence.svg) · [ERD](erd.svg) · [Classes](class.svg).
Sources homonymes .puml; [traçabilité](tracabilite.md), [validation](validation.md).
