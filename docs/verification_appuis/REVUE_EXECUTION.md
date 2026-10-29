# Revue de l'exécution de l'épic VA — par Claude

> Chaque story est jugée sur **son critère et son test** dans
> `EPIC_VA_Verification_appuis_depot.md`, vérifiés **dans le dépôt** (commits,
> fichiers, tests relancés), jamais sur le seul rapport de l'agent.

## VA01 — Instantané du constat · revue du 29 oct. 2026

**Verdict de l'agent** : BLOQUÉ (données réelles non autorisées), recette synthétique réussie.
**Mon verdict** : ✅ **conforme sur la partie synthétique ; BLOQUÉ à juste titre**
pour l'instantané réel. Deux réserves, à lever avant PASS.

### Ce que j'ai vérifié

| Point | Constat |
|---|---|
| Tests | relancés par moi : **3/3 OK**, avec le Python système et celui du `.venv`, `-W error::ResourceWarning` |
| Critère « deux générations identiques à l'octet » | couvert : `constat.json` et `SHA256SUMS` comparés à l'octet |
| Critère « numéro imprimé, jamais celui du `.md` » | couvert : le paragraphe de fixture `43` sort `41`, comme la concordance réelle (md 43 → imprimé 41) |
| Hypothèses du code sur les **données réelles** (lues par moi en lecture seule) | ✅ la concordance réelle a bien les champs `numero_md`, `numero_imprime`, `incipit` (198 lignes) ; les textes du doc 9 ne commencent pas par leur numéro, donc l'appariement par incipit fonctionne ; et `LibraryNode.paragraph_number` porte **déjà le numéro imprimé** (item 43 → `paragraph_number` 41), si bien que le contrôle croisé « numéro stocké » est cohérent avec la concordance |
| Protection des données réelles | sérieuse : accord écrit exigé **avant** toute connexion ; session et transaction PostgreSQL `READ ONLY` ; `ContentType.get`, jamais `get_for_model` (qui peut créer) |
| Écrasement | refusé si le contenu diffère ; sortie limitée à `legal/verification_appuis/` |
| Commits annexes `ed973f0` et `80913a0` | ne contiennent que l'outil d'extraction, ses manifestes et les réponses du 29 oct. : rien d'inattendu |

### Réserves

1. **Pas encore commité.** `legal/verification_appuis/` et
   `docs/verification_appuis/execution/` sont hors suivi. L'épic exige « une
   story = un commit = un verdict » : pas de PASS sans le commit, et son SHA au
   rapport.
2. **Le contrôle croisé du numéro stocké n'est pas testé.** La fixture ne
   porte pas de `numero_stocke` : le refus « numéro stocké divergent », qui
   protège précisément contre une erreur de numérotation, n'est jamais exercé.
   **Ajouter deux tests** : numéro stocké égal à l'imprimé → accepté ; numéro
   stocké différent → refus nommant l'énoncé.

Remarque, sans réserve : `--reel` refuse si les effectifs diffèrent de
287 / 515 / 268. C'est une garde d'ancrage défendable, puisque le constat est
figé ; le message le dit.

### Les deux questions de l'agent

- **Stories conditionnelles** : inclure VA08, VA09, VA10, VA15 — d'accord. VA08
  et VA09 sont les deux qui répondent à la question de LP. **Exclure VA14** est
  cohérent avec la proposition révisée (la relecture vient après l'ensemble).
  Conséquence à accepter : aucune synthèse avant que les 515 liens soient
  validés. VA14 pourra être ajoutée plus tard sans rien refaire. **Décision de
  LP.**
- **Lecture seule des données réelles pour VA01–VA17** : le mécanisme est sain.
  ⚠️ Le fichier d'accords `va-accords/1` est **la trace de l'autorisation de
  LP** : il doit être écrit **par LP**, ou dicté par lui mot pour mot, jamais
  rempli par l'agent de sa propre initiative (même principe que `--atteste`).
