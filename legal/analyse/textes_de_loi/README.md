# Textes de loi — les règles du jeu

> **Pourquoi ce dossier existe.** Le 6 novembre 2026, une analyse de délai a été
> faite sur un C.p.c. **à jour au 24 octobre 2025** — douze mois de retard, dans
> un code modifié en 2020 et en 2024. Et la Loi concernant le cadre juridique des
> technologies de l'information, décisive pour le support des pièces, était
> **absente du dépôt**. On ne plaide pas sur un texte dont on ignore le
> millésime.
>
> ⚠️ **Règle : ne jamais citer une disposition de mémoire.** On la lit ici, et on
> note le « À jour au » de la page de garde.

## Lire un article

```bash
scripts/loi/lire.sh C-25.01 249 264        # un ou plusieurs articles
scripts/loi/lire.sh I-16 61
scripts/loi/lire.sh CCQ-1991 2840
```

Le script extrait la couche texte avec **PDFKit** (via `scripts/loi/pdftxt.swift`,
compilé à la première utilisation), met le résultat en cache à côté du PDF, puis
imprime l'article demandé. Il affiche la date de consolidation du texte en
en-tête de sa sortie.

⚠️ **Pourquoi PDFKit et non `fitz`/`pypdf`** : ni l'un ni l'autre n'est
installable sur cette machine (Homebrew cassé). `scripts/loi/article.py` retire
par ailleurs les fragments de pied de page que LegisQuébec intercale **au milieu
des phrases** — sans quoi une citation recopiée depuis la sortie contient des
caractères qui ne sont pas dans la loi.

## État des textes

✅ **Tous installés le 7 novembre 2026.**

| Code | Texte | Fichier | À jour au |
|---|---|---|---|
| **C-25.01** | Code de procédure civile | `C-25.01_2026-10-15.pdf` | **15 oct. 2026** |
| **CCQ-1991** | Code civil du Québec | `CCQ-1991_2026-10-15.pdf` | **15 oct. 2026** |
| **I-16** | Loi d'interprétation | `I-16_2026-10-15.pdf` | **15 oct. 2026** |
| **C-1.1** | Cadre juridique des technologies de l'information | `C-1.1_2022-01-01.pdf` | ⚠️ **1er janv. 2022** |

⚠️ **La seule réserve restante porte sur C-1.1**, obtenu par la vue « Imprimer »,
qui a rendu une consolidation au 1er janvier 2022. Les art. 23, 29 et 31 y
portent leur note de source d'origine (« 2001, c. 32 »), donc non modifiés **à
cette date**. Une consolidation au 15 octobre 2026 resterait à obtenir pour
exclure une modification postérieure.

### Audit du changement de consolidation — 7 nov. 2026

Les **35 articles** du C.p.c. sur lesquels le dossier s'appuie ont été comparés
mot à mot entre la consolidation du **24 octobre 2025** et celle du **15 octobre
2026** : **35 identiques, aucun écart réel.** Rien de ce qui a été cité ou plaidé
avant le 7 novembre n'est atteint. Les copies d'origine restent sous
`legal/analyse/Responsabilité civile/`.

## ⚠️ Deux pièges de l'extraction, tous deux corrigés — mais à connaître

1. 🔴 **La couche texte est en Unicode DÉCOMPOSÉ** (A + accent grave combinant,
   et non « À »). **Un `grep` ordinaire portant un accent renvoie ZÉRO alors que
   le mot est présent.** Constaté le 7 nov. : une recherche de « férié » dans la
   Loi d'interprétation ne trouvait rien, alors que l'art. 61, 23° définit
   précisément ce mot. `charger()` normalise désormais en NFC, et
   **`scripts/loi/chercher.py` est le seul moyen sûr de chercher** :

   ```bash
   scripts/loi/chercher.py I-16 "jour férié"
   ```

2. 🔴 **Les énumérations peuvent perdre leur texte.** LegisQuébec met parfois les
   étiquettes (« 23° », « a) », « b) ») dans un flux et leur contenu dans un
   autre ; l'article s'imprime alors avec ses marqueurs seuls. `lire.sh`
   **avertit** maintenant et marque l'article comme tronqué. Dans ce cas, passer
   par `chercher.py`.

## Ce qui attend ces textes

| Question ouverte | Article | Pourquoi elle compte |
|---|---|---|
| ~~Le dimanche est-il un « jour férié » ?~~ | **61, 23° a) I-16** ; **52 I-16** ; art. 82-83 C.p.c. | ✅ **RÉPONDU le 7 nov. : oui.** « les mots "jour de fête" et "jour férié" désignent : **les dimanches** ». Voir `communication_pieces.md` § 42 |
| Peut-on exiger un support précis ? | **29 C-1.1** | la demande de clé USB du 6 nov. ⚠️ Son exception d'**entente** rend l'engagement écrit du 6 nov. pertinent dans les deux sens — `communication_pieces.md` § 39.7 |
| Le support réclamé par le destinataire | **23 C-1.1** | la même question, vue de leur côté |
| Présomption de transmission et de réception | **31 C-1.1** | l'« accès » contre la « transmission » — § 34.3 et § 39.1 |
| Modifications du C.p.c. depuis oct. 2025 | **C-25.01** entier | toute vérification faite le 6 nov. porte cette réserve |
