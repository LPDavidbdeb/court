# VA06 — série 1, quarante propositions

**Verdict : PASS pour l’exécution des 40 propositions ; validation LP en attente.**

Exactement les 40 premiers liens de priorité 1 de VA03, dans leur ordre, de 1 à 277 (identifiants non consécutifs), ont chacun une proposition CODEX de grille v1.1. 18 supports distincts : 13 PDF originaux locaux, dont les trois scans imposés, et cinq EML locaux. Les propositions et le dossier portent les empreintes, passages, localisations, raisons, limites, contrôles d’attribution et périmètres lus.

## Tests et sorties

[Trois tests de série synthétiques](SERIE_1.tests.txt), code 0 : refus du mauvais ordre, des effectifs différents et des décisions LP ; fichier final changé détecté avant le premier ajout ; contradictions en tête du tableau. [Recette complète](RECETTE_PHASE0.tests.txt) : 45 tests, code 0. [Exécution réelle](SERIE_1.reel.txt) ; [ancrage réel préalable](SERIE_1.ancrage.txt), code 0.

## Fichiers

`serie_1.py`, `preparer_serie_1.py`, `tests/test_va06_serie1.py`, `observations.jsonl` en ajout seulement ; nouveau dossier `serie_1/` (sélection, lectures et rendus, inventaire, 40 propositions, dossier à valider, couverture et bilan) ; présent rapport et sorties.

## Lecture réelle et résultat documentaire

Accords VA06, VA11–VA13 en vigueur. Les 18 fichiers ont été lus : tous les textes PDF/EML, toutes les pages des scans P-19 (16), P-42 (4), P-29 (8), P-40 (5) vues ; sept vues complémentaires sur les autres PDF, soit 40 vues. Les courriels sont lus avec leurs antécédents cités ; une copie compacte retire les préfixes de citation et les répétitions pour la navigation, jamais pour faire autorité. Quatre écarts de cadrage sont proposés sur les liens 40, 43 (deux) et 273 ; zéro contradiction directe proposée, zéro écart NE_L_ETABLIT_PAS. Les autres contributions restent décrites avec leurs limites, sans assimiler une absence dans une pièce à une réfutation de la réalité.

## Écarts et raisons

Priorité 1 porte sur tous les liens des paragraphes concernés, et inclut donc les autres cotes associées à P-19/P-40/P-42 : l’ordre exact de VA03 est conservé. Un premier repère de fin de citation native ne correspondait pas aux blancs du PDF ; la borne a été corrigée avant toute écriture d’observations, sans changer le texte prélevé. PyMuPDF local sert aux vues (Poppler indisponible, aucune installation réseau) ; les rendus sont plafonnés à 1800 pixels après une limite de transfert d’image. Les copies de lecture et les citations JSONL conservent les caractères sources ; les captures texte brutes sont exclues du contrôle d’espaces Git, et non nettoyées. Le premier contrôle Git a signalé les espaces de fin de ligne des citations natives dans le dossier Markdown ; son affichage les neutralise désormais, sans modifier le journal ni les citations canoniques. Aucun changement source ou base, aucune nouvelle cote, aucun push.

## Arrêt

55 versions de journal, dont six décisions dictées de LP ; 40 ajouts de cette série exclusivement PROPOSE. Couverture globale : 468 NON_EXAMINE, 41 PROPOSE, 6 VALIDE. Pilote inchangé à 6/7 validés (85,714 %), 472 en attente. Aucun autre lien ni VA14, VA17 ou phase 1. SHA au registre après commit.

## Commit vérifié et fichiers exacts

`b6695840c4ed01784005bbcba378a48d31feeec8` — legal: VA06 livrer les quarante propositions de la série 1 et arrêter

- `docs/verification_appuis/execution/reprise_2026-10-29/RECETTE_PHASE0.tests.txt`
- `docs/verification_appuis/execution/reprise_2026-10-29/SERIE_1.md`
- `docs/verification_appuis/execution/reprise_2026-10-29/SERIE_1.reel.txt`
- `docs/verification_appuis/execution/reprise_2026-10-29/SERIE_1.tests.txt`
- `legal/verification_appuis/observations.jsonl`
- `legal/verification_appuis/preparer_serie_1.py`
- `legal/verification_appuis/serie_1.py`
- `legal/verification_appuis/serie_1/A_VALIDER_PAR_LP.md`
- `legal/verification_appuis/serie_1/bilan.json`
- `legal/verification_appuis/serie_1/couverture_globale.json`
- `legal/verification_appuis/serie_1/couverture_globale.md`
- `legal/verification_appuis/serie_1/couverture_pilote.json`
- `legal/verification_appuis/serie_1/couverture_pilote.md`
- `legal/verification_appuis/serie_1/derives.json`
- `legal/verification_appuis/serie_1/lectures/P-16-page-3.png`
- `legal/verification_appuis/serie_1/lectures/P-16-page-6.png`
- `legal/verification_appuis/serie_1/lectures/P-16.txt`
- `legal/verification_appuis/serie_1/lectures/P-18-page-1.png`
- `legal/verification_appuis/serie_1/lectures/P-18.txt`
- `legal/verification_appuis/serie_1/lectures/P-19-page-1.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-10.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-11.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-12.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-13.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-14.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-15.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-16.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-2.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-3.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-4.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-5.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-6.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-7.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-8.png`
- `legal/verification_appuis/serie_1/lectures/P-19-page-9.png`
- `legal/verification_appuis/serie_1/lectures/P-19.txt`
- `legal/verification_appuis/serie_1/lectures/P-2-page-1.png`
- `legal/verification_appuis/serie_1/lectures/P-2-page-2.png`
- `legal/verification_appuis/serie_1/lectures/P-2.txt`
- `legal/verification_appuis/serie_1/lectures/P-20.txt`
- `legal/verification_appuis/serie_1/lectures/P-22.1.txt`
- `legal/verification_appuis/serie_1/lectures/P-22.2.txt`
- `legal/verification_appuis/serie_1/lectures/P-22.3.txt`
- `legal/verification_appuis/serie_1/lectures/P-22.4.txt`
- `legal/verification_appuis/serie_1/lectures/P-29-page-1.png`
- `legal/verification_appuis/serie_1/lectures/P-29-page-2.png`
- `legal/verification_appuis/serie_1/lectures/P-29-page-3.png`
- `legal/verification_appuis/serie_1/lectures/P-29-page-4.png`
- `legal/verification_appuis/serie_1/lectures/P-29-page-5.png`
- `legal/verification_appuis/serie_1/lectures/P-29-page-6.png`
- `legal/verification_appuis/serie_1/lectures/P-29-page-7.png`
- `legal/verification_appuis/serie_1/lectures/P-29-page-8.png`
- `legal/verification_appuis/serie_1/lectures/P-29.txt`
- `legal/verification_appuis/serie_1/lectures/P-40-page-1.png`
- `legal/verification_appuis/serie_1/lectures/P-40-page-2.png`
- `legal/verification_appuis/serie_1/lectures/P-40-page-3.png`
- `legal/verification_appuis/serie_1/lectures/P-40-page-4.png`
- `legal/verification_appuis/serie_1/lectures/P-40-page-5.png`
- `legal/verification_appuis/serie_1/lectures/P-40.txt`
- `legal/verification_appuis/serie_1/lectures/P-42-page-1.png`
- `legal/verification_appuis/serie_1/lectures/P-42-page-2.png`
- `legal/verification_appuis/serie_1/lectures/P-42-page-3.png`
- `legal/verification_appuis/serie_1/lectures/P-42-page-4.png`
- `legal/verification_appuis/serie_1/lectures/P-42.txt`
- `legal/verification_appuis/serie_1/lectures/P-66.1.txt`
- `legal/verification_appuis/serie_1/lectures/P-66.2.txt`
- `legal/verification_appuis/serie_1/lectures/P-66.3.txt`
- `legal/verification_appuis/serie_1/lectures/P-66.4.txt`
- `legal/verification_appuis/serie_1/lectures/P-7-page-3.png`
- `legal/verification_appuis/serie_1/lectures/P-7.txt`
- `legal/verification_appuis/serie_1/lectures/P-9-page-2.png`
- `legal/verification_appuis/serie_1/lectures/P-9.txt`
- `legal/verification_appuis/serie_1/lectures/courriels_lecture_compacte.txt`
- `legal/verification_appuis/serie_1/lectures/inventaire.json`
- `legal/verification_appuis/serie_1/propositions.json`
- `legal/verification_appuis/serie_1/selection.json`
- `legal/verification_appuis/tests/test_va06_serie1.py`
