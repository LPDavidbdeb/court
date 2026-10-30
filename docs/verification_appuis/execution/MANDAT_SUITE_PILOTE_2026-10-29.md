# Suite du pilote — mandat transmis par LP le 29 octobre 2026

LP a transmis le fichier `PROMPT_SUITE_PILOTE_2026-10-29.md` dans la
conversation de l'agent d'exécution. Ses sections 0 à 5 constituent les
instructions de cette reprise et la dictée des décisions de recette. Le
fichier transmis est conservé sans modification ; `accords.json` reste intact.

- Branche : `epic/E01-numerotation-concordance` ; départ `acd4e09`.
- Lectures réelles : accords antérieurs, PostgreSQL local par socket Unix en
  transaction READ ONLY ; fichiers locaux autorisés. Aucun accès réseau ni push.
- Écritures limitées à `legal/verification_appuis/` et
  `docs/verification_appuis/`, ainsi qu'aux métadonnées Git des commits demandés.
- Aucun changement de base, d'application, de cote, de source ou de l'archive
  gelée. L'état antérieur du constat et des observations est conservé.
- Première porte : nouvel instantané VA01 puis VA02 ; seule la cote de ligne
  377 peut différer, `source_id` (object_id en base) 330 → 4 et `source_ref`.
  Toute autre différence impose l'arrêt avant la suite.
- VA05 : actualiser les liens de 377 depuis Email 4 ; accepter les PDF de
  P-58 à P-64 uniquement à partir de la page 2, empreinte du fichier entier.
- VA13 : démontrer A_REVOIR pour l'ancienne proposition 472.
- Recette LP : valider 468, 470, 471, 473, 474 ; corriger uniquement la
  description DATE de 469 mot pour mot selon le prompt puis la valider ;
  refaire 472 sur Email 4 en proposition sans décision LP.
- Référence des décisions : « Message de LP du 29 octobre 2026 à l'agent
  d'exécution de l'épic VA — recette du pilote ».
- Grille v1.1 : auteur agent d'examen CODEX/CLAUDE ou LP ; degré explicite
  pour chaque nouvel écart ; contrôle des attributions à la cote. Inscription
  au journal des versions de l'épic.
- Ensuite seulement : les 40 premiers liens de priorité 1 de la liste VA03,
  dans l'ordre existant, propositions CODEX uniquement ; dossier série 1 avec
  tableau des écarts classés par degré. Arrêt strict après ces 40 liens.
- VA14, VA17, phase 1 et toute autre série restent exclus.
- Chaque reprise de story reçoit son commit, verdict, rapport et sortie réelle
  de tests ; les SHA sont ajoutés au registre après création des commits.

Les validations enregistrées exécutent les décisions dictées par LP. CODEX
ne prend aucune décision de validation de son propre chef.
