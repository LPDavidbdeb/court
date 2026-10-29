# Mandat d'exécution reçu de LP — 29 octobre 2026

Ce document consigne la portée opérationnelle du message de LP ; le fichier
`legal/verification_appuis/accords.json` reproduit exactement son JSON dicté.

- Inclure VA08, VA09, VA10 et VA15 ; exclure VA14 pour l'instant.
- Exécuter VA01 réel, puis VA02–VA13 et VA15 dans l'ordre de l'épic.
- Exécuter ensuite VA16 : proposer les observations des liens des §§ imprimés
  234–236, puis **s'arrêter** pour validation du pilote et de la grille par LP.
- Ne pas exécuter VA17, VA18–VA24 ni d'autre série d'examens dans ce mandat.
- PostgreSQL : uniquement la base locale `court_project_pg`, en transaction
  READ ONLY ; supports sous `media/`, `storage/` et le dossier d'extraction
  `~/Documents/Pieces_505-17-016235-261_2026-11-06/` avec son manifeste.
- Aucune écriture en base, aucune modification des supports, aucun accès
  réseau (Gmail compris). La contradiction avec la demande de push après PASS
  est soumise à LP ; aucun push dans l'attente de sa réponse.
- Les écritures d'artefacts sont limitées à `legal/verification_appuis/` et
  `docs/verification_appuis/execution/`, temporaires de tests compris.
- L'auteur d'une proposition est **CODEX**. Seul LP peut marquer une observation
  VALIDE ou REJETE. Les acteurs LP des fixtures sont fictifs et étiquetés tels.
- Une story donne lieu à un commit et à un verdict avant la suivante. Le
  rapport conserve fichiers, résultats bruts des tests, écarts motivés et
  lectures réelles effectuées. Le SHA est relevé après le commit dans le
  registre, sans réécriture du commit qui a produit ce SHA.

Ces décisions priment sur le vocabulaire CLAUDE de l'épic et sur la dépendance
VA17 → relectures VA14. L'épic et la revue externe restent inchangés, car ils
sont hors du périmètre de fichiers modifiables de ce mandat.
