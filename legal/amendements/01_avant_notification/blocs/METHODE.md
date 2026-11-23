# Méthode de rédaction par blocs — demande amendée

*Consigné le 23 novembre 2026, à la demande du demandeur. Ce fichier s'adresse à tout agent ou rédacteur qui reprend le travail : lisez-le avant de modifier un bloc. Il décrit le contexte, l'utilité, l'implantation et l'état d'avancement de la méthode. Les décisions encore ouvertes sont signalées comme telles.*

---

## 1. Contexte

La demande introductive d'instance (dossier 505-17-016235-261, Cour supérieure du Québec) conteste la requête assermentée par Élise Ayoub le 19 novembre 2015. Elle a été déposée le 24 juillet 2026 (`legal/depots/2026-07-24_initial/`, **à ne jamais modifier**). Sa réécriture se fait dans `legal/amendements/01_avant_notification/`.

Jusqu'ici, la partie III (contestation de la requête paragraphe par paragraphe) vivait dans un seul document de travail (`sections/contestation_requete_2015_document_travail_2026-11-19.md`), puis a été évaluée bloc par bloc (`analyses_experimentales/evaluation_partie_III.md`) et réécrite en sections de remplacement, d'abord avec des numéros de paragraphes fixes (§§ 176 à 229, par exemple).

Deux problèmes en ont découlé :
1. **La numérotation.** La demande dépasse 200 paragraphes et les sections se renvoient les unes aux autres (« §§ 212 à 214 »). Ajouter ou retirer un paragraphe oblige à renuméroter tout ce qui suit, et à corriger chaque renvoi.
2. **La taille du contexte.** Un agent qui doit relire le document entier, ou le registre des précisions (plus de 300 Ko), pour modifier un paragraphe travaille mal. Une section autonome de quelques pages s'analyse et se corrige bien.

## 2. Principe

- **Un bloc = un fichier**, autonome, avec ses notes de rédaction. Le bloc traite un paragraphe ou un groupe de paragraphes de la requête de 2015.
- **Aucun numéro de paragraphe dans les fichiers.** Les paragraphes sont des items de liste ; leur numéro est attribué à l'assemblage, par la liste Word.
- **Les renvois internes passent par des étiquettes**, jamais par des numéros.
- **Le document est reconstitué par programme**, à partir d'un fichier d'ordre.
- **GitHub est la source unique.** Une version = un commit ; pas de suffixes `_v1`, `_v2` dans ce répertoire. (Les copies du projet claude.ai, suffixées, ne font pas foi.)

**Rattachement à la méthodologie post-dépôt.** La méthode applique deux règles déjà approuvées dans `legal/METHODOLOGIE_POST_DEPOT.md` : des identifiants internes stables, indépendants du numéro final (§ 3.5), et une numérotation procédurale continue générée seulement à l'assemblage de la version retenue (§ 3.5). Elle doit aussi produire la table de concordance entre la demande déposée et la version amendée qu'exige le § 3.4 ; l'assembleur pourra la générer à partir du champ `requete:` et d'un champ `depose:` (paragraphes de la demande déposée que le bloc remplace), à ajouter lorsque la concordance sera établie. Lire aussi `AGENTS.md` et `PROJECT_CONTEXT.md` avant tout travail.

## 3. Arborescence

```
legal/amendements/01_avant_notification/
├── blocs/
│   ├── METHODE.md          ← ce fichier
│   ├── conventions.md      ← style et vocabulaire
│   ├── ordre.txt           ← ordre d'assemblage, un nom de fichier par ligne
│   ├── par28_29_mediation.md ← un fichier par bloc
│   ├── …
│   └── tests/              ← consignes de test de la méthode
├── outils/
│   ├── verif_citations.py  ← vérification des citations
│   ├── assembler.py        ← assemblage, contrôles, Markdown et Word
│   ├── rendre_docx.js      ← production du Word (appelé par assembler.py)
│   └── package.json        ← dépendance npm « docx » (npm install)
└── build/                  ← sorties de l'assemblage (non versionnées, .gitignore)
```

Nom d'un bloc : `par<premier paragraphe>_<mot-clé>.md`, sur deux chiffres (`par07_…`, `par19_35_acces_autorite.md`). Le nom n'est pas un numéro de paragraphe de la demande.

## 4. Format d'un fichier de bloc

```markdown
---
bloc: par10_rachat
requete: [10]                 # paragraphes de la requête de 2015 visés
statut: brouillon             # brouillon | à valider | arrêté
depend_de: [par14_17_motif]   # blocs auxquels celui-ci renvoie
registre: [P242, P244, P251]  # entrées du registre des précisions qui le fondent
---

# Titre du bloc

1. Premier paragraphe numéroté. {#par10-objet}

1. Paragraphe avec sous-paragraphes :
   a) premier sous-paragraphe ;
   b) second sous-paragraphe.

#### Intertitre

1. Paragraphe qui renvoie à un autre : voir {§par10-objet} et {§par14-routine..par14-refus}.

<!-- fin-du-texte -->

## Notes de rédaction

Tout ce qui suit le marqueur est exclu du document assemblé.
```

Règles de syntaxe :

| Élément | Syntaxe dans le .md | Rendu dans Word |
|---|---|---|
| Paragraphe numéroté | ligne commençant par `1. ` (toujours « 1. ») | item de la liste principale : 1, 2, 3… continu sur toute la demande |
| Sous-paragraphe | `   a) ` (trois espaces) | item de second niveau : a), b)… |
| Intertitre | `#### ` | titre non numéroté ; la liste continue après lui |
| Titre du bloc | `# ` | titre de section |
| Étiquette | `{#etiquette}` en fin de paragraphe numéroté | signet sur le paragraphe |
| Renvoi simple | `{§etiquette}` | « § N » |
| Renvoi à une plage | `{§etiq1..etiq2}` | « §§ N à M » |
| Renvoi à un sous-paragraphe | `{§etiquette/b}` | « § N b) » |
| Paragraphe de la requête de 2015 | « paragraphe 20 de la requête », en toutes lettres | texte ordinaire (ces numéros sont fixes) |
| Fin du texte | `<!-- fin-du-texte -->` | tout ce qui suit est exclu |

Étiquettes : minuscules, chiffres et traits d'union, préfixées par le bloc (`par10-plan-juin-2013`) pour rester uniques dans toute la demande.

Pièces : désignées par le chemin de leur fiche (`legal/piece_pdf-3.md`). Les cotes (P-xx) seront substituées à l'assemblage à partir d'une table de correspondance, au moment du bordereau (décision reportée). Ne jamais recycler une cote.

## 5. Procédure pour modifier ou rédiger un bloc

1. Lire ce fichier, puis `conventions.md`, puis le bloc visé et ceux de `depend_de`.
2. Lire les entrées du registre indiquées dans `registre:` (registre des précisions, projet claude.ai `claude/registre_precisions_suite_axe4_participation.md`, et sa copie au dépôt `analyses_experimentales/registre_precisions_projet.md`).
3. Rédiger ou modifier sans numéro ; ajouter une étiquette à tout paragraphe qui peut être cité ailleurs.
4. Vérifier les citations : `python3 legal/amendements/01_avant_notification/outils/verif_citations.py blocs/<bloc>.md`. Toute ligne `NO` doit être corrigée sur la fiche pièce, ou expliquée dans les notes (source hors corpus, par exemple un courriel Gmail non versé).
5. Mettre à jour `statut:`, `depend_de:` et `registre:` ; inscrire la modification au `journal_modifications.md`.
6. Committer le bloc seul, avec un message qui nomme le bloc. Ne pousser qu'à la demande du demandeur.

**Portée des retouches.** Ne modifier que les paragraphes visés par la demande. Toute autre retouche, même de pure précision, est signalée dans le compte rendu et dans les notes, avec sa raison ; elle peut être refusée à la validation.

**Travail sans clone du dépôt.** Un agent qui n'accède au dépôt que par un connecteur (sans clone) peut rédiger et committer, mais ses contrôles portent sur une copie partielle. Il exécute au moins `assembler.py --sans-word` et `verif_citations.py` sur les fiches qu'il a récupérées, le dit dans son compte rendu, et la vérification complète (toutes les fiches, Word) est refaite sur un clone avant d'intégrer le bloc.

**Installation des outils.** Python 3 suffit pour les contrôles. Pour le Word : Node.js, puis `npm install` dans `outils/` (le fichier `package.json` y déclare le paquet `docx`).

### Objections pendant la composition (registre P459)

Jusqu'à ce que la section portant sur la requête de 2015 soit entièrement composée, les objections des revues et des comptes rendus de conversion sont consignées dans `blocs/objections_en_attente.md`, sans être traitées. Elles seront évaluées ensemble une fois la section composée. Les corrections mécaniques sans incidence sur le fond sont faites à la validation. Toute modification du fond d'un bloc est soumise au demandeur, texte à l'appui, avant d'être appliquée (P453).

## 6. L'assemblage (`outils/assembler.py`, version minimale en place le 23 novembre 2026)

Ce que fait l'outil :
1. lire `blocs/ordre.txt` et concaténer les blocs dans cet ordre ;
2. retirer l'en-tête YAML et tout ce qui suit `<!-- fin-du-texte -->` ;
3. vérifier que chaque étiquette est unique et que chaque renvoi pointe vers une étiquette existante (erreur bloquante sinon) ;
4. relancer `verif_citations.py` sur l'ensemble ;
5. produire un fichier Word dont les paragraphes numérotés sont les items d'**une seule liste Word** (numérotation continue, gérée par Word), les sous-paragraphes un second niveau de cette liste ;
6. rendre les renvois : dans la version minimale, l'assembleur calcule les numéros et les écrit en texte ; le .md restant la source, il suffit de réassembler après chaque modification ;
7. produire un PDF de contrôle et en vérifier la numérotation avant tout envoi (LibreOffice : `soffice --headless --convert-to pdf build/demande_assemblee.docx`).

Dépendances : Python 3 ; Node.js et le paquet npm `docx` (`npm install docx`) pour le Word ; LibreOffice, facultatif, pour le PDF. `python3 outils/assembler.py --sans-word` fait les contrôles et le Markdown assemblé sans Node.

Les annexes suivent les blocs dans les deux fichiers assemblés. `blocs/annexes/ordre_annexes.txt` liste leurs fichiers dans l'ordre, à raison d'un nom par ligne. Chaque fichier a un identifiant stable dans le champ YAML `annexe:` et un titre Markdown de niveau `#`. Le titre devient « Annexe N — ‹titre› » selon l'ordre de la liste et commence sur une nouvelle page dans Word. Le fichier d'ordre est facultatif. S'il est absent ou vide, seuls les blocs sont assemblés.

Dans un bloc, `{annexe:ann07_role_de_pere}` donne « l'annexe 1 » si le fichier correspondant est en première position. Un identifiant inconnu bloque l'assemblage. `--sans-annexes` produit les blocs seuls et continue de résoudre leurs renvois selon le fichier d'ordre. Les étiquettes de sections d'annexe participent au contrôle des doublons sur l'ensemble du document.

Éprouvé le 23 novembre 2026 sur le bloc `par28_29_mediation.md` : quatorze paragraphes numérotés par la liste Word, sous-paragraphes a) à c) qui recommencent sous chaque paragraphe, intertitres sans rupture de la numérotation, renvois rendus « § 3 a) » et « §§ 8 à 10 ».

Évolution possible, si le texte est un jour modifié directement dans Word (par un avocat, par exemple) : rendre les renvois comme des champs Word (signet + champ REF avec numéro de paragraphe) pour qu'ils se mettent à jour dans Word même. Non nécessaire tant que le .md est la source.

## 7. Angles morts connus, et parades

| Risque | Parade |
|---|---|
| Les blocs ne sont pas entièrement autonomes : ils se renvoient les uns aux autres et partagent des arguments | Étiquettes plutôt que numéros ; champ `depend_de` ; l'assembleur bloque sur un renvoi orphelin |
| Un même fait sert dans plusieurs blocs (la lettre du 27 avril 2015 : blocs C, D, G et I) ; une correction faite à un endroit reste fausse ailleurs | Donner à chaque fait un bloc d'attache et y renvoyer ailleurs ; vérification des citations sur l'ensemble à chaque assemblage |
| Perte de cohérence globale : thèse, noms (« Élise Ayoub », « Me Marie-Josée Ayoub »), mots exclus | `conventions.md` lu avec chaque bloc ; relecture du document assemblé avant chaque étape importante |
| Deux sources de vérité (projet claude.ai et GitHub) | GitHub fait foi ; le projet ne garde que des copies de lecture |
| Les notes de rédaction contiennent les faiblesses, les lacunes, les questions de privilège et la stratégie | Dépôt privé ; marqueur `<!-- fin-du-texte -->` obligatoire ; l'assembleur exclut les notes. Si le dépôt devait être communiqué, les notes partiraient avec lui : un avocat pourra préférer les loger dans des fichiers séparés |
| Une citation vérifiée contre une analyse plutôt que contre sa pièce | `verif_citations.py` ne cherche que dans les fiches `piece_*.md` |
| Les sections déjà rédigées ont des numéros fixes et des renvois codés en dur | À convertir dans ce format, au fur et à mesure ou en une passe avant le premier assemblage |
| Le document de travail du 19 novembre devient caduc à mesure que les blocs existent | Ne plus le modifier ; il reste comme historique |

## 8. Conventions de fond (résumé ; à détailler dans `conventions.md`)

- **Aucune qualification** juridique ou morale dans le texte : ni « parjure », « calomnie », « manipulation », « tromperie », « domination », « hostile », « gaslighting », « témérité ». Décrire et juxtaposer ; le tribunal conclut.
- **Par personne.** Me Marie-Josée Ayoub n'a ni rédigé la requête de 2015, ni représenté sa sœur devant le tribunal (2013 à janvier 2016). Elle répond de ses propres écrits : le courriel du 11 juin 2013, les lettres de négociation de 2015.
- **Deux dates.** Ce que la défenderesse savait s'apprécie au 19 novembre 2015 (assermentation) ; la présentation au tribunal, au 14 janvier 2016. Les écrits de 2016 et de 2020 éclairent la conception, non les faits de 2015.
- **Allégations de 2013.** Ne pas les citer ni en discuter le fond ; les mentionner comme des allégations ni étayées ni retirées. Ne jamais écrire « accès supervisés » : écrire « en présence de tiers ».
- **Secret professionnel et privilège.** Les courriels du demandeur à ses avocats (Me Poirier, Me Pringle) ne sont pas utilisés sans sa décision de renoncer au secret ; les lettres de négociation « Sous toutes réserves » sont à valider par un avocat avant production.
- **Orthographe source** dans toute citation ; « […] » pour une coupure ; crochets pour un ajout éditorial.
- **Annexes.** Les fichiers déclarés dans `blocs/annexes/ordre_annexes.txt` utilisent les titres `##` et `###`, les listes `- ` et les tableaux Markdown. Placer les étiquettes `{#ann07-mot-cle}` à la fin des titres `##`. `<!-- fin-du-texte -->` marque le début des notes exclues du rendu. Dans les blocs, renvoyer à l'identifiant YAML avec `{annexe:identifiant}`.

## 9. État au 23 novembre 2026

| Bloc (paragraphes de la requête) | Contenu disponible | Format de ce répertoire |
|---|---|---|
| §§ 4 à 6 | Pas de bloc, par décision (registre P234) : la chaîne causale tombe avec la thèse générale | — |
| § 7, durée (« un (1) an ») | `blocs/par07_duree_2011.md` | **rédigé** (23 novembre 2026) ; revue contradictoire à faire |
| § 7, rôle de père | `blocs/par07_role_de_pere.md` et `blocs/annexes/ann07_role_de_pere.md` (annexe 1) | annexe **convertie** et validée ; bloc **rédigé** (23 novembre 2026) ; revue contradictoire à faire |
| § 9 | Annexe (`claude/annexe_paragraphe9_ete_2013_v2.md`) | à convertir |
| § 10 | `blocs/par10_rachat.md` | **rédigé** (23 novembre 2026) ; revue contradictoire à faire |
| §§ 14 à 17 | `blocs/par14_17_motif.md` | **converti** (conversion n° 1) |
| § 18 | `blocs/par18_entente.md` | **converti** ; attribution de `par18-conclusion` corrigée |
| §§ 19 à 26, 30, 31, 33 à 35 | `blocs/par19_35_acces_autorite.md` | **converti** ; allégations de 2013 citées (P448) |
| §§ 28 et 29 | `blocs/par28_29_mediation.md` | **converti** (23 novembre 2026) ; modifié et validé lors du test n° 1 |
| §§ 56 à 58 | `blocs/par56_58_assurances.md` | **converti** (conversion n° 1) |
| Axes de la partie II, annexes A-1 à A-7 | Document de travail et `annexes_axe4/` | à décider |

Hors champ par choix : §§ 22, 25 et 32 de la requête ; le volet financier (revenu de référence de février 2015) est réservé.

## 10. Décisions ouvertes

1. **Qui modifiera le texte après nos travaux** : le demandeur et un agent dans les .md (l'assembleur minimal suffit), ou un avocat directement dans Word (renvois en champs Word, et le .md cesse d'être la source).
2. **Emplacement des notes de rédaction** : dans le bloc (actuel) ou dans un fichier séparé.
3. **Ordre d'assemblage** et place des annexes (liste distincte, numérotation propre).
4. **Table des cotes** : à établir avec le bordereau.
