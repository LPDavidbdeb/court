# Phase 0 — outils autonomes de vérification des relations du dépôt

Le mandat est limité à VA01–VA17 de
[`EPIC_VA_Verification_appuis_depot.md`](../../docs/verification_appuis/EPIC_VA_Verification_appuis_depot.md).
Les outils sont extérieurs à l'application Django. Ils ne créent ni migration,
ni table, ni modification du constat existant.

## VA01 — instantané

Recette synthétique, sans configuration Django ni connexion réelle :

```sh
python3 -W error::ResourceWarning -m unittest legal.verification_appuis.tests.test_va01 -v
python3 -m legal.verification_appuis.outil instantane --help
```

Le générateur prend une base SQLite de fixture et une table de concordance.
Les trois tables synthétiques `enonces`, `liens` et `cotes` contiennent un
identifiant et un objet JSON ; leur constructeur figure dans `tests/aide.py`.
La fixture de recette utilise des textes inventés et les numéros décalés
43 → 41, 44 → 42 et 45 → 43 de la concordance fournie au mandat.

Les sorties sont `constat.json` et `SHA256SUMS`. Le premier conserve les
textes exacts ; la normalisation sert uniquement à apparier leurs incipits à
la table des numéros imprimés. Les énoncés sans numéro imprimé propre gardent
la valeur `null`, sans numéro fabriqué. Un appariement ambigu est refusé.

Une sortie différente ne peut pas écraser une capture existante. Le
répertoire de sortie est limité à `legal/verification_appuis/` ou au temporaire
des tests, après résolution des liens symboliques.

## Accès aux sources réelles

L'option `--reel` exige un fichier d'accords `va-accords/1`, avec une entrée
pour la story concernée, l'auteur `LP`, le mode `LECTURE_SEULE` et la référence
au message d'autorisation. Ce fichier consigne une autorisation réellement
reçue ; il n'est jamais rempli par défaut. L'accord de lecture ne constitue
pas une validation des observations.

L'adaptateur impose la lecture seule à la connexion PostgreSQL puis dans une
transaction à vue cohérente. Il n'appelle aucune commande de persistance ni
aucune méthode de création. Une divergence avec les effectifs réels attendus
287/515/268 provoque un refus explicite.

Les accords concernant les cinq stories conditionnelles et la lecture réelle
sont en attente. La présence de l'adaptateur ne signifie pas qu'il a été
exécuté sur la base réelle. Les rapports sous
`docs/verification_appuis/execution/` font foi de ce qui a réellement été lancé.
