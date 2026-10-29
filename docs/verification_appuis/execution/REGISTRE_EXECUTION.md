# Registre des commits et verdicts — phase 0

Le commit de livraison d'une story réunit son code, ses tests et leur rapport.
Son SHA est ensuite relevé dans ce registre ; les commits de suivi documentaire
ne modifient pas le code livré. Aucune story suivante n'a été lancée avant le
commit et le verdict de VA01 ci-dessous.

| Story | Verdict | Commit de livraison | Recette | Données réelles |
|---|---|---|---|---|
| VA01 | **BLOQUÉ** pour l'instantané réel ; recette synthétique conforme | `97d65740f3cb9a8b075ca3808fb2c90f9beb84ee` | **5/5 OK** avec Python système et `.venv` ; [rapport](VA01.md), [sortie système](VA01.tests.txt), [sortie .venv](VA01.venv.tests.txt) | Aucune connexion ni lecture de support probatoire exécutée par cette story ; accord LP en attente. |

Les deux réserves de la revue reçue ont été traitées : fichiers VA01 suivis
dans le commit ci-dessus, et deux tests supplémentaires du numéro stocké.
Le verdict du réviseur dans `../REVUE_EXECUTION.md` reste conservé tel que reçu.

## Superpush préalable

Le superpush demandé a publié sur
`origin/epic/E01-numerotation-concordance`, sans force :

- `20d25139b17d286d009cb9fcf2206de42d2b646c` : conception et concordance ;
- `ed973f0639ef12a1b0253d45c83eaf3679ae936a` : extraction et manifestes ;
- `80913a0c216060dcc425d54dce1bfe4cef537588` : échanges du 29 octobre.

Sortie du push préalable, code 0 :

```text
To github.com:LPDavidbdeb/court.git
   aa7fa51..80913a0  epic/E01-numerotation-concordance -> epic/E01-numerotation-concordance
```

Ces commits préalables ne contiennent pas le code VA01. La publication
préalable ne constitue ni une autorisation de lecture réelle ni une validation
de LP. Aucun fichier d'accords n'a été créé par l'agent.
