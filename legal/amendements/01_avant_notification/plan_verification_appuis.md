# Vérifier que les pièces appuient ce que la demande leur fait appuyer

> **Demande de LP, 29 oct. 2026** : valider que chaque pièce appuie ce que la
> demande allègue qu'elle appuie, et **persister** l'exercice. Questions : la
> source doit-elle être la base (`document_manager`) ou le fichier ? Et
> n'avait-on aucune version entièrement conforme à l'acte déposé ?

## 1. Où nous en sommes

| Sujet | État | Source |
|---|---|---|
| **Quel fichier est l'acte déposé** | ✅ **Tranché le 13 oct.** : la version simple de **44 pages**, endos inclus — le PDF (`candidats/demande_DEPOT_2026-07-21.pdf`, sha256 `00a20c79…`), qui est aussi la copie signifiée (`legal/docx_file/…pdf`, même empreinte). Numérotation imprimée 1 … 241 | `identification_du_fichier_imprime.md` |
| « Aucune version 100 % conforme » | ⚠️ **Dépassé.** Seule réserve : le référent officiel reste le papier détenu par le greffe, et aucune copie conforme n'a été obtenue | archive, README § 2 |
| **Document 9** (base) = la demande transcrite le 12 août, depuis le `.md` | ✅ **Vérifié le 29 oct.** : **287 énoncés sur 287** se retrouvent mot pour mot dans le `.md` (`0f141193…`) et dans le texte du PDF déposé. Les 9 qui résistaient ne diffèrent que par la césure des mots en fin de ligne à l'extraction du PDF (« dommages-intérêts », « Marie-Josée »), pas par le texte | ce document, § 2 |
| Numérotation du document 9 | ⚠️ celle du `.md`, qui diffère de l'imprimé pour **47 paragraphes sur 179**. Table de passage complète : 198/198, appariés sans ambiguïté | `concordance_md_imprime.json` |
| **Ce que la demande CITE** | ✅ persisté : `AppuiDepotJuillet` — **515 liens** sur **148 paragraphes** (198 par liasse entière), tirés de la prose | `persister_appuis_depot`, `verifier_appuis_depot` |
| **Ce que les pièces APPUIENT réellement** | ❌ **jamais vérifié systématiquement**. 0 lien n'a de passage précis (`precision`) ; 394 liens sur 515 n'ont aucun verbatim | — |
| Les pièces elles-mêmes | ✅ 260 cotes sur 267 extraites, identiques octet pour octet à la base ; 7 transcriptions à produire (P-58 à P-64) | `legal/instance/outils/README_extraction_pieces.md` |
| Protection du document 9 contre une modification | ❌ aucune : « rien ne protège sa représentation en base » | `legal/instance/suivi_paragraphes_en_base.md` § 4 |

## 2. La source : la base, ancrée au PDF

**Recommandation : travailler sur le document 9 et `AppuiDepotJuillet`, et
contrôler contre le PDF déposé.** Repartir du `.docx` ou du PDF obligerait à
redécouper les paragraphes et à reconstruire les 515 liens que la base porte
déjà. Ce serait plus long, et sans gain de fidélité.

| | Base (doc 9 + appuis) | Fichier (`.docx` / PDF) |
|---|---|---|
| Fidélité du texte | **identique** à l'acte déposé (287/287, ci-dessus) | c'est l'acte |
| Découpage en paragraphes | fait (287 énoncés) | à refaire |
| Liens paragraphe → pièce | **515, déjà persistés** | à reconstruire depuis la prose |
| Où persister un verdict | sur le lien exact (énoncé × ligne du bordereau) | nulle part de stable |
| Numérotation | celle du `.md` → **toujours afficher le numéro imprimé**, par la table de passage | imprimée |
| Risque | une modification d'un énoncé du doc 9 passerait inaperçue → **geler une empreinte des 287 énoncés** avant de commencer | aucun, le fichier est gelé |

Le PDF reste **le référent** ; la base est **l'instrument**. Cette répartition
tient tant que l'empreinte gelée des 287 énoncés est vérifiée avant chaque
passe.

## 3. Ce qu'on vérifie : l'unité et la grille

**L'unité est la proposition**, pas le paragraphe (`legal/CLAUDE.md` : « un fait
= une proposition »). Un paragraphe peut alléguer trois faits et citer deux
pièces ; chacune peut appuyer l'un et pas l'autre.

⚠️ **Un paragraphe qui allègue plusieurs faits est lui-même un défaut de l'acte**
(remarque de LP, 29 oct.). Ce que dit le texte, lu au Code :

> **Art. 99 al. 1 C.p.c.** — « Ses énoncés doivent être présentés avec
> **clarté, précision et concision**, dans un ordre logique et être **numérotés
> consécutivement**. »

Le Code actuel n'écrit pas « un seul fait par paragraphe » en toutes lettres.
L'ancien Code le disait (art. 76 : chaque paragraphe ne contenant, autant que
possible, qu'une seule allégation), et l'exigence de clarté et de précision le
commande. ⚠️ Le *Règlement de la Cour supérieure en matière civile* n'est pas
au dépôt : ne rien en citer avant lecture.

La numérotation, elle, est une exigence **expresse** : l'acte déposé va de 1 à
241 avec 62 numéros manquants et 19 suffixes (`8-A`).

➜ **La vérification par proposition sert donc deux fois.** Elle dit si chaque
fait est appuyé, et elle **dresse la liste des paragraphes à scinder** dans la
demande modifiée : un fait par paragraphe, numérotés consécutivement.

**Pour chaque couple (proposition, pièce citée)** :

| Verdict | Sens |
|---|---|
| **APPUIE** | la pièce établit la proposition telle qu'elle est écrite |
| **APPUIE EN PARTIE** | elle en établit une partie : dire laquelle, et ce qui reste sans appui |
| **N'APPUIE PAS** | elle ne dit pas ce que le paragraphe lui fait dire |
| **CONTREDIT** | elle dit autre chose, ou l'inverse |
| **À VÉRIFIER SUR L'ORIGINAL** | le support ne permet pas de conclure en l'état (scan à relire, photo sans date EXIF…) |

Chaque verdict porte : le **passage** de la pièce, au mot, avec sa
localisation (en-tête et date du courriel, page du PDF, date EXIF de la photo) ;
la **raison** ; **qui** l'a posé (proposé par Claude / **validé par LP**) ; la
date ; et deux **empreintes**, celle du texte de l'énoncé et celle du fichier de
la pièce (manifeste d'extraction). Un écart d'empreinte signale qu'un verdict
porte sur un état qui a changé.

**Règles qui gouvernent la lecture** (mémoire du dossier) :
- lire **l'original** — la base, le `.eml`, le scan —, jamais la fiche
  `piece_*.md` (*verbatim sur l'original*) ;
- calibrer : contredit / vrai mais cadré / non étayé ; ne jamais réfuter une
  absence par une absence (*evidentiary calibration*) ;
- actes adverses P-19, P-40, P-42 : l'unité est **leur** paragraphe, lu sur le
  **scan** (le document 3 diverge du scan aux § 6 c) et § 8).

## 4. Où persister — décision de LP

| Option | Pour | Contre |
|---|---|---|
| **A. Fichiers versionnés** — `legal/verification_appuis/verdicts.jsonl` + une vue `.md` par paragraphe, clés : pk de l'appui, pk de l'énoncé, cote, § imprimé | faisable **maintenant**, hors système, donc hors processus de lots ; versionné par Git ; importable plus tard | pas d'interrogation SQL directe |
| B. Table en base, liée à `AppuiDepotJuillet` | requêtes, écrans | modification du système : **un lot est requis**, et C0-A non intégré bloque l'ouverture du suivant |
| C. Le champ `note` d'`AppuiDepotJuillet` | sans migration | texte libre, sans structure ni empreinte ; mêle constat et vérification |

✅ **Décision de LP, 29 oct. : B, une table en base.**

**Ce que cela implique, d'après `docs/PROCESSUS_CHANGEMENT.md`.** Une table est
une modification du système. Elle relève donc d'un **lot** : mandat écrit
(`docs/architecture_c/lots/<LOT>/MANDAT.md`), quatre vues UML (activité,
séquence, ERD cible, classes), revue B, approbation de LP, puis exécution dans
une copie isolée. Et **« un lot non atterri bloque le lot suivant »** : C0-A
n'est pas intégré. Le § 7 du processus en exclut `legal/`, pas le code.

**Adapter `AppuiDepotJuillet` plutôt que créer une table ? (question de LP,
29 oct.)** Ce serait aussi une migration, donc aussi un lot : on n'y gagne pas
de procédure. Et trois raisons de ne pas y écrire les verdicts :

1. **Elle est un constat** : « ce paragraphe invoque cette pièce », tiré du
   texte déposé, figé comme lui. Sa docstring sépare expressément les couches :
   « jamais par accident ». Un verdict est une **évaluation**, qui se propose,
   se valide et peut changer.
2. **La granularité ne colle pas** : une ligne d'appui = un paragraphe × une
   pièce ; un verdict = **une proposition** × une pièce. Un paragraphe de trois
   faits ne tient pas dans une ligne.
3. **L'historique** : « proposé par Claude » puis « validé par LP », ou un
   verdict révisé, demandent plusieurs lignes dans le temps.

➜ **La bonne forme est d'étendre sans modifier** : une table **fille**, liée par
clé étrangère à `AppuiDepotJuillet` (un appui → N verdicts), dans
`case_manager`, à côté de la table qu'elle complète. Le constat reste intact,
et chaque verdict reste attaché au lien exact.

**Ce qui peut avancer sans attendre** (la rédaction de dossiers n'est pas
bloquée) : le mandat et les quatre vues du lot ; l'empreinte gelée des
287 énoncés ; la liste de travail ; et les premiers verdicts, saisis dans un
fichier d'attente **au schéma exact de la table**, importé tel quel à
l'atterrissage.

## 5. Les étapes

0. **Ancrage** — ✅ comparaison doc 9 ≡ PDF faite le 29 oct. (§ 1). Reste :
   **geler l'empreinte des 287 énoncés** (fichier `SHA256SUMS`-like) et la
   vérifier avant chaque passe.
1. **Inventaire** (script, lecture seule) : une liste de travail par paragraphe
   — numéro **imprimé**, texte, propositions, pièces citées (515 liens) — plus
   les paragraphes factuels qui ne citent **aucune** pièce.
2. **Ordre de passage**, du plus exposé au moins exposé :
   1. la prescription (§ 234-236 : P-40, P-105) ;
   2. les paragraphes qui invoquent P-19, P-40, P-42 (les actes dont la
      demande fait déclarer le contenu faux) ;
   3. le préjudice et le quantum (§ 200-217) ;
   4. le reste, dans l'ordre de l'acte.
3. **Passes par lots** d'une vingtaine de liens : je propose le verdict et le
   passage, LP valide ou corrige ; le fichier est écrit à chaque lot.
4. **Synthèse pour la demande modifiée** : les propositions sans appui ou
   contredites → renforcer par une pièce **au soutien d'un fait déjà allégué**,
   reformuler, ou retirer. ⚠️ Jamais de fait nouveau (verrou de prescription).

**Échéance utile** : avant la rédaction finale de la demande modifiée
(1er févr. 2027). Rien de cela ne conditionne la communication du 6 novembre.
