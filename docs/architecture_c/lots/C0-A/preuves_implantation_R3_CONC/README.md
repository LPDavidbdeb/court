# Preuves de l'implantation UC14 R3-CONC

Agent A, 23 octobre 2026. Ces fichiers sont des preuves documentaires du
[rapport d'implantation](../RAPPORT_IMPLANTATION_R3_CONC.md). Aucun statut
d'approbation ou d'intégration n'en découle. Les horodatages d'origine sont
conservés. Banc : `/private/tmp/court-r3conc-20261023-ZyKFPa`, hors dépôt.

## Index

| Fichier | Contenu |
|---|---|
| `C0A_R3_CONC_candidat.bundle` | Les deux commits du banc sur le socle `515666e` : témoin `ef2c219` (tag `ancien-f35ec85`) et candidat `a7af209` (tag `candidat-r3-conc`) |
| `journaux/r3-candidat-{1,2,3}.log` | Passe finale : les 28 essais R3-CONC, trois fois, sur le candidat |
| `journaux/candidat-app-complete.log` | Suite applicative, 16 paquets, base de test neuve : 298 OK |
| `journaux/candidat-outillage.log`, `journaux/candidat-schema.log` | 33 OK ; *No changes detected* et *0 issues* |
| `journaux/ancienne-contre-epreuve-R3.log` | Les 28 essais contre les modules de production du témoin : 13 ok, 14 FAIL, 1 ERROR |
| `journaux/ancienne-contre-epreuve-reprise-C0A.log` | `C0ARepriseConcurrence`, adaptée, contre le témoin : 3 échecs de libellé sur 6 |
| `journaux/ancien-app.log`, `ancien-outillage.log`, `ancien-schema.log` | Référence du témoin avant correction : 270, 33, aucun changement |
| `journaux/ancien-app-etiquette-unique-erreur-harnais.log` | **Erreur de harnais**, sans valeur de test. Sous zsh, `$P` non découpé a passé les 16 paquets en une seule étiquette. Relancé correctement dans `ancien-app.log` |
| `journaux/postgresql_extrait.log` | Extrait filtré du journal serveur : démarrages, arrêts, 1256 connexions `[local]`, 166 attentes de verrou avec PID détenteur et requête, 28 interblocages. Le journal complet n'est pas versionné |
| `journaux/initdb.log` | Initialisation du cluster jetable |
| `*.depouillement.json` | Issue de chaque essai et message de l'exception, extraits des journaux |
| `observations_R3.json` | Lignes `R3_OBSERVATION` : PID T1/T2, `pg_blocking_pids`, `wait_event`, `pg_locks`, état retiré, issues ; trois exécutions du candidat et le témoin |
| `contre_epreuve_ancienne.json` | Empreintes des modules du témoin utilisés, codes des phases, candidat restauré et vérifié |
| `comparaison_schema_ast.json` | Champs et `Meta` de `document_manager/models.py` et `case_manager/models.py` : identiques au socle |
| `reconstruction.json` | Socle, entrées extraites de `f35ec85`, empreintes des huit fichiers (témoin et candidat), commits, arbres, livrables |
| `isolation.json` | Paramètres du cluster, connexions par rôle et par base, attentes, interblocages, arrêts |
| `versions_environnement.json`, `pip_freeze.txt` | Versions et paquets |
| `harnais/` | `c0a_settings.py` et `run_tests.py` de B, identiques à l'octet ; scripts propres à cette campagne |
| `passes_intermediaires/` | Passes antérieures, conservées sans réécriture (ci-dessous) |
| `manifest_sha256.json` | Empreintes de tous les fichiers de ce dossier, des deux patches et des deux rapports |

## Passes intermédiaires

- `passe0/`. Premières exécutions des essais (27, avant T23b), premières
  suites complètes (297), et deux contre-épreuves sur le témoin. Dans la
  première (`premiere-passe-*`), la troisième variante de T08 échouait en
  cascade de la deuxième, qui avait recréé E2. Chaque variante part désormais
  de son propre état.
- `passe1_5a34274/`. Passe complète sur le commit de banc `5a34274`, avant
  l'ajout à T21 de l'assertion sur le motif de l'archive (contrôle V06 de la
  grille de revue). Résultats identiques à la passe finale.

## Commandes de la passe finale

Elles ont été exécutées depuis `<banc>`, cluster démarré. `R3` désigne les
classes `document_manager.test_e01_numerotation.C0AR3Concurrence`,
`…C0AR3SauvegardeExistante` et `…C0AR3Retrait`. `P` désigne les 16 paquets
`DAL Utils ai_services argument_manager case_manager cause_manager core
document_manager email_manager events googlechat_manager helpers pdf_manager
photos protagonist_manager video_manager`.

```sh
<banc>/venv/bin/python <banc>/harness/run_tests.py r3-candidat-1 $R3   # puis -2, -3
dropdb -h <banc>/socket -p 55439 -U c0a_owner --if-exists test_court_c0a
<banc>/venv/bin/python <banc>/harness/run_tests.py candidat-app-complete $P
<banc>/venv/bin/python <banc>/harness/run_tests.py candidat-outillage scripts.regime_citations.test_projection scripts.regime_citations.test_verifier_ab
<banc>/venv/bin/python <banc>/harness/run_tests.py candidat-schema C0A_SCHEMA_CHECK
<banc>/venv/bin/python <banc>/harness/contre_epreuve_ancienne.py
pg_ctl -D <banc>/pgdata -m fast -w stop
<banc>/venv/bin/python <banc>/harness/extraire_journal_pg.py <banc>/logs/postgresql.log <banc>/logs/postgresql_extrait.log
<banc>/venv/bin/python <banc>/harness/comparer_schema_ast.py <banc>/repo 515666e… ancien-f35ec85 candidat-r3-conc
<banc>/venv/bin/python <banc>/harness/consigner_references.py <banc> <livraison>
```

Le cluster a été démarré avec :
`-k <banc>/socket -p 55439 -h '' -c max_connections=30 -c shared_buffers=32MB
-c fsync=off -c log_connections=on -c log_lock_waits=on -c deadlock_timeout=1s
-c log_line_prefix='%m [%p] %q%u@%d '`.

## Reconstituer le candidat

```sh
git init <copie> && git -C <copie> fetch <dépôt> 515666eb8c6e7fdcdd265f9187c9c37b769b0fed
git -C <copie> fetch C0A_R3_CONC_candidat.bundle candidat-r3-conc:refs/tags/candidat-r3-conc ancien-f35ec85:refs/tags/ancien-f35ec85
# ou bien, sur une copie au socle :
git -C <copie> apply ../C0A_R3_CONC_DIFF_COMPLET.patch   # arbre 1e0c504e744f95b2558f0ca320717ca57165ed43
```

Ne pas exécuter les lanceurs depuis ce dossier : leur racine se calcule
depuis le parent du dossier `harness/`. Les scripts de banc ne font pas
partie du delta applicatif.
