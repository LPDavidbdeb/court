# Inventaire et évaluation de l'organisation du dossier `legal/`

> **État au 30 septembre 2026.** Relevé fait sur le disque et dans git ; **rien n'a été déplacé ni supprimé.** Ce document décrit et évalue ; les réorganisations proposées au §4 attendent la décision du demandeur.

---

## 1. Vue d'ensemble

| Mesure | Valeur |
|---|---|
| Fichiers à la racine de `legal/` | **398**, dont **296 fiches de pièces** (`piece_*`) et **102 documents de travail** |
| Sous-dossiers | 14 (≈ 300 fichiers) |
| Liens Markdown vers des fiches | **2 002 liens dans 229 fichiers** |
| Documents de travail de la racine modifiés pour la dernière fois **avant ou au dépôt** (24 juillet) | **65 sur 102** |
| Fichiers « bruit » suivis par git | **10** (5 copies `.backup_`/`.bak`, 5 fichiers verrous Office `~$`) |

---

## 2. Inventaire par rôle

### 2.1 Les données — ce qui est vrai indépendamment de l'argument

| Famille | Où | Nb | Contenu | Rôle | État |
|---|---|---|---|---|---|
| **Fiches de pièces** `piece_<modèle>-<id>.md` | racine | 296 (142 courriels, 73 événements, 37 PDF, 10 conversations, 6 photodocs, …) | verbatim + métadonnées + contextes d'usage | **source de vérité** du corpus ; lue par l'outil d'audit (`case_manager/piece_file_audit.py` attend `legal/piece*.md`) | convention claire (`legal/CLAUDE.md`), bien suivie ; quelques noms hors convention (`piece_avis_cotisation_pere_2019`, `piece_p2_messages_7avril2015`, `piece_tablefix…`) |
| **Textes de loi** | `analyse/Responsabilité civile/` (C.c.Q., C.p.c.) ; `analyse/Responsabilité Déonthologique/` (code de déontologie) | 3 PDF | textes officiels | **référence** | ⚠️ rangés parmi les analyses, dans des dossiers aux noms à espaces et accents (et une coquille : « Déonthologique ») |
| **Dépôt gelé** | `depots/2026-07-24_initial/` | 12 | reçu du greffe, candidats d'impression, `cotes.lock.json`, `SHA256SUMS` | **archive probante**, jamais écrite | ✅ exemplaire |
| **Rendus Word/PDF** | `docx_file/` (+ `revision_2026-07-14/`, `-07-17/`) | 26 | exports `.docx` des documents Markdown | **produits dérivés** | ⚠️ contient des fichiers verrous `~$` suivis par git ; plusieurs rendus d'états périmés |
| **Annexes de preuve** | `annexes/` | 5 | annexes A-D par axe + index | **pièces de soutien** rédigées | stable depuis le 27 juillet |

### 2.2 Les registres — ce qui relie les données à l'acte

| Famille | Où | Nb | Rôle | État |
|---|---|---|---|---|
| **Bordereaux** | racine (`bordereau_pieces.md`, `_des_pieces_demande`, `_bloc_depot`, `_liens_acces`, + `.bak`) ; `amendements/…/bordereau_amende.md` | 6 | cote ↔ pièce ↔ fiche | ⚠️ cinq bordereaux à la racine sans indication de celui qui fait autorité ; un `.bak` suivi |
| **Inventaires, validations, concordances** | racine (`inventaire_*` ×6, `validation_*` ×2, `concordance_*`, `historique_procedural_plumitif`) ; `expose/registre_pieces.md` ; `organisation_preuve/registre_procedural/` | ≈ 15 | contrôles et tables de correspondance | utiles mais dispersés ; `validation_citations_a_creer.md` fait 2 949 lignes |
| **Cotes après dépôt** | `amendements/01_avant_notification/` (cartes P-107+, plans de liasses JSON, journal) | 12 | verrou et suite des cotes | ✅ cohérent avec `METHODOLOGIE_POST_DEPOT.md` |

### 2.3 L'analyse — ce que l'on tire des données

**a) Par paragraphe de l'acte adverse** (l'unité est le § contesté). **Sept couches parallèles** traitent la même unité. Exemple pour les §§14-17 de la requête de 2015 :

| Couche | Fichier | Rôle |
|---|---|---|
| analyse de l'allégation | `allegation_stmt14_15_16_17_garde_partagee.md` (racine) | décomposition, calibration |
| faits | `faits/faits_par14-17_2015.md` | liste de faits (art. 99) |
| pont | `pont/pont_par14-17_2015.md` | lien faits → procédure |
| organisation de la preuve | `organisation_preuve/2015_par_14_17.md` (+ `.csv`, `.xlsx`) | union des pièces |
| consolidé | `ponts_requete_2015_consolides.md` (racine, 1 857 lignes, généré par `regenerate_ponts_consolides.py`) | assemblage |
| réécriture | `redaction_v2/12_blocs_7_et_14-18_projet.md` | nouvelle version |
| analyse de responsabilité | `analyse/Responsabilité civile/justifications_garde_exclusive_2015.md` | moyens de droit |

**b) Par idée transversale** (l'unité est la thèse) : `these_*` ×20 et `axe_*` ×7 (racine) ; `implication_parentale_recurrence/` (12, avec cadre commun) ; `dossier_plaidoirie/` (8, numérotés) ; `memoire*`, `_note_*`, `synthese_*`, `compilation_griefs.md` (2 094 lignes).

### 2.4 La rédaction — les actes

| Famille | Où | État |
|---|---|---|
| Demande déposée et ses sources | `demande_DEPOT_2026-07-21.md`, `demande_introductive_instance.md`, `requete_secton_faits_lp.md` (+ **4 copies `.backup_` et 1 `.bak`**, 1 094 lignes chacune), `ebauche_*`, `procedure_introductive_*`, `poursuite_expose_des_faits.md`, `expose_faits_volet_2015.md`, `expose/` | base de la première demande, **figée de fait** mais non marquée comme telle |
| Atelier de la nouvelle version | `redaction_v2/` (base 14, texte 13, blocs 20-25, journal) | ✅ règles écrites (`00_README.md`) |
| Espace d'amendement | `amendements/01_avant_notification/` | ✅ |
| Phase instance | `instance/` (README, journal, `entrants/`, `sortants/`, `analyses/`, arguments, plaidable) | ✅ la partie la mieux organisée |

### 2.5 Le pilotage et le code

| Famille | Où | État |
|---|---|---|
| Conventions et méthode | `CLAUDE.md`, `METHODOLOGIE_POST_DEPOT.md`, `methodo_*` ×2, `plan_de_travail.md`, `etat_travail_demande.md` | `plan_de_travail` et `etat_travail_demande` datent de juillet ; statut incertain |
| Journaux | `journal_evolution_these_requete_2015.md` (journal de travail) ; `journal_ete2013.md`, `journal_fevrier2011_fevrier2012.md` (**journaux de faits**) | ⚠️ même préfixe pour deux rôles différents |
| Code | `create_court_reference_docx.py`, `markdown_to_docx_service.py`, `regenerate_ponts_consolides.py` (racine) ; `faits/PictureHEIC.py` ; `__pycache__/` | ⚠️ du code parmi les contenus |

---

## 3. Évaluation — l'organisation n'est pas optimale, mais ses meilleures parties sont récentes

### 3.1 Ce qui fonctionne

1. **La convention des fiches** : une source, une fiche, un nom déterministe, et un outil d'audit qui la vérifie. C'est le socle, et il tient.
2. **Les espaces créés depuis le dépôt** — `depots/`, `amendements/`, `redaction_v2/`, `instance/` — ont chacun un README, un journal et des règles d'écriture. Ils montrent l'organisation qui marche : **un dossier par phase, avec son régime**.
3. **Le gel du dépôt** (sommes de contrôle, verrou des cotes) est exemplaire.

### 3.2 Ce qui ne fonctionne pas

1. **La racine mélange les données et le travail.** 296 fiches et 102 documents de travail côte à côte ; aucune séparation visible entre ce qui est **vrai** (fiche) et ce qui est **soutenu** (thèse).
2. **Sept couches parallèles par paragraphe, sans carte.** La même unité (un § contesté) vit dans sept fichiers à des niveaux différents, sans index qui dise laquelle gouverne. Seul le §3 de 2019 a un index (`instance/INDEX_contre_argument_par3.md`), et il constate lui-même que les couches anciennes sont « partiellement périmées ». **C'est la cause des erreurs récurrentes** consignées en mémoire (« une thèse remplace, elle ne s'empile pas » ; travail du 29 septembre fait dans la mauvaise couche).
3. **Aucun statut de fichier.** 65 des 102 documents de travail de la racine n'ont pas bougé depuis le dépôt : on ne peut pas savoir, sans les lire, s'ils sont la **base figée** (point de repli voulu par `redaction_v2/00_README.md`), **actifs**, ou **périmés**.
4. **Le bruit est suivi par git** — copies de sauvegarde, fichiers verrous Office — alors que git conserve déjà les versions, et que **le dépôt est public**.
5. **Des éléments mal rangés** : textes de loi parmi les analyses ; code parmi les contenus ; doublon divergent (`faits_par7-8_2023.md` existe à la racine **et** dans `faits/`, avec des contenus différents) ; même préfixe `journal_` pour un journal de travail et deux journaux de faits.
6. **Des noms qui résistent aux outils** : espaces, accents et coquille dans `analyse/Responsabilité civile/`, `analyse/Responsabilité Déonthologique/`, `memoire faille structurelle.md`.
7. **Cinq bordereaux à la racine** sans indication de celui qui fait autorité aujourd'hui.

---

## 4. Recommandations, par rapport gain / coût

**Contraintes à respecter.** 2 002 liens pointent vers les fiches depuis 229 fichiers ; l'outil d'audit attend `legal/piece*.md` ; le dépôt est gelé ; la base de la première demande doit rester intacte comme point de repli ; le dépôt git est public.

| # | Mesure | Gain | Coût / risque |
|---|---|---|---|
| 1 | **Carte par paragraphe** : un fichier `legal/CARTE_PARAGRAPHES.md` qui, pour chaque § contesté, liste les sept couches et dit **laquelle gouverne** (sur le modèle de `instance/INDEX_contre_argument_par3.md`) | **le plus élevé** : supprime la cause des erreurs de couche | faible ; rien ne bouge |
| 2 | **En-tête de statut** dans chaque document de travail : `base figée` / `actif` / `périmé → voir X` | élevé : rend lisible ce que 65 fichiers taisent | faible ; une ligne par fichier, à faire progressivement |
| 3 | ✅ **Fait le 30 septembre 2026 (non commité).** Les 10 fichiers sont retirés du suivi (`git rm --cached`) mais **restent sur le disque** ; `*.bak`, `*.backup_*` et `~$*` ajoutés au `.gitignore`. Les quatre journaux d'intégration du 12 juillet (`organisation_preuve/registre_procedural/integration_*`) nomment les copies en texte : leur contenu reste récupérable dans l'historique git | moyen : moins de confusion, moins d'exposition publique | très faible ; git garde l'historique |
| 4 | **Résoudre le doublon** `faits_par7-8_2023.md` (racine / `faits/`) : désigner celle qui gouverne, marquer l'autre | moyen | faible ; décision du demandeur sur le contenu |
| 5 | **Un dossier `legal/references/`** pour les textes de loi, avec des noms sans espaces | moyen | faible ; mettre à jour la mémoire `textes-de-loi-locaux` |
| 6 | **Déplacer le code** vers un dossier d'outils (hors des contenus) | faible à moyen | vérifier les imports et les chemins codés en dur |
| 7 | **Désigner le bordereau qui fait autorité** (en-tête des autres : « historique ») | moyen | faible |
| 8 | Renommer `journal_ete2013` et `journal_fevrier2011_fevrier2012` en `chronologie_*` | faible | faible ; vérifier les liens entrants |
| 9 | **Ne pas** déplacer les fiches dans un sous-dossier maintenant | — | 2 002 liens et l'outil d'audit à réécrire : à faire, si jamais, par script avec audit complet avant/après |
| 10 | **Ne pas** fusionner ni supprimer les couches anciennes | — | elles sont la base de repli voulue ; les **marquer** (mesures 1-2), pas les détruire |

**Ordre proposé** : 3 (sans risque, immédiat) → 1 et 2 (le vrai gain) → 4, 7 (décisions de contenu) → 5, 6, 8 (rangement).
