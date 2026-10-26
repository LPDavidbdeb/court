# Preuves de la revue B01

Agent B, rapport final du 22 octobre 2026. Les horodatages originaux des essais
des 21–22 octobre sont conservés. Ces fichiers sont des preuves documentaires;
aucun statut d’approbation ou d’intégration n’en découle.

- `candidat-app.log` : 270 tests, OK.
- `b-independant.log` : six tests B, quatre OK et deux échecs de conformité.
- `candidat-outillage.log` : 33 tests, OK.
- `candidat-schema.log` : aucun changement de migration détecté, check OK.
- `ancienne-contre-epreuve-A.log` : six tests corrigés A contre les deux modules
  antérieurs; deux OK et quatre échecs attendus, dont un sur le motif de refus.
- `ancienne-contre-epreuve-B.log` : deux variantes initiales B, deux échecs
  attendus contre les modules antérieurs.
- `observations_B.json` : entrelacements, PID PostgreSQL distincts, états finaux.
- `reconstruction.json`, `verification_sources.json`, `verification_finale.json`
  et `candidat_sha256.json` : références, périmètre et contrôles d’empreintes.
- `phases_complementaires.json` : commandes et codes des phases complémentaires;
  retour final aux huit fichiers exacts du candidat corrigé.
- `postgresql.log` : cluster privé sans TCP; 102 connexions, toutes locales;
  arrêt confirmé. `initdb_sandbox_refuse.log` conserve seulement la première
  tentative d’initialisation refusée par le bac à sable. L’initialisation a
  ensuite été exécutée avec les permissions système nécessaires, sur ce
  même emplacement jetable; ce refus environnemental n’est pas un test métier.

## Reproduction

Créer un nouveau banc `repo/`, `harness/`, `logs/`, `socket/`, `tmp/`, `media/`,
`static/`, avec PostgreSQL jetable sans TCP et le rôle/base des réglages fournis.
Placer `c0a_settings.py`, `run_tests.py` et `revue_b01_B_tests.py` dans `harness/`.
Ne pas exécuter les lanceurs directement depuis ce dossier de preuves : leur
racine est calculée depuis le répertoire parent du dossier `harness`.

Reconstituer `repo/` à `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`, puis appliquer
les deux patchs exacts du commit `f35ec8586866f4359d44f52a0bc5cc57c0804217`.
Le lanceur synthétique refuse les fichiers `.env`, les réglages réels et toute
connexion hors de son socket privé. Le port est 55439; l’isolation repose sur
le répertoire de socket propre au banc, aucune écoute TCP.

Exécuter les commandes données dans le rapport. Les contre-épreuves anciennes
conservent les tests corrigés A et remplacent temporairement les deux modules
`concordance.py` et `protection.py` par ceux du premier patch, uniquement dans le
banc. `terminer_revue.py` enregistre leurs codes et restaure le candidat dans
un `finally`, puis vérifie ses huit empreintes. Il suppose `avant_delta/` et
`candidat_sha256.json` préparés lors de la reconstitution; il ne constitue
pas une commande à lancer sur le dépôt partagé ou sur une base réelle.
