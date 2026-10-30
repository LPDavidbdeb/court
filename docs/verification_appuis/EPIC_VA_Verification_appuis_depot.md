*Relations entre les paragraphes et les pièces de la demande déposée*

**Document de travail — version 1.1 — 29 octobre 2026**

| **Mode de maintenance** | Modifier uniquement la section ou la story visée ; conserver les identifiants VA01–VA24. |
|---|---|
| **Validation** | Une story = un commit = un verdict **PASS**, **FAIL** ou **BLOQUÉ** avant la suivante. |
| **Autorité probatoire** | Le support original fait autorité (`.eml`, scan, fichier) ; les fiches `piece_*.md` servent à se repérer, jamais à constater. |
| **Données réelles** | Les tests tournent sur des **fixtures synthétiques**. Toute exécution sur la base ou les fichiers réels demande l'accord de LP, story par story. |
| **Processus** | Phase 0 : hors application (`legal/verification_appuis/`), non régie par `docs/PROCESSUS_CHANGEMENT.md` (§ 7). Phase 1 : **un lot**, après C0-A intégré ou dérogation expresse de LP. |

# Journal des versions

| **Version** | **Date** | **Portée** | **État** |
|---|---|---|---|
| 1.0 | 2026-10-29 | Découpage de `PROPOSITION_DISPOSITIF.md` (révisée) et de sa revue en 24 stories. | Base de travail |
| 1.1 | 2026-10-29 | Recette du pilote dictée par LP dans `execution/PROMPT_SUITE_PILOTE_2026-10-29.md` : attribution réelle CODEX acceptée ; chaque nouvel écart distingue CONTREDIT / ETABLIT_EN_CADRANT_AUTREMENT / NE_L_ETABLIT_PAS ; contrôle que les mots attribués sont dans la cote, sinon recherche locale dans le même fil/document et écart IDENTITE_PIECE avec modèle et pk. P-38 refaite sur Email 4, changement de rattachement annoncé et conservé dans les instantanés. | Grille approuvée par LP ; six décisions dictées, lien 472 en nouvelle proposition avant prochaine recette. |

# 1. Objectif

Produire une **image durable, vérifiable et révisable** des relations entre les
paragraphes de la demande déposée le 24 juillet 2026 et les pièces qu'ils
citent. Pour chacun des **515 liens** existants : quelle relation s'observe, à
partir de quel élément de la pièce, avec quelle portée **au regard du texte du
paragraphe**, et avec quels écarts.

**Le constat est intouchable** : document 9 (287 énoncés), `BordereauDepotJuillet`
(268 lignes cotées), `AppuiDepotJuillet` (515 liens). Rien ne s'y écrit.

**Sources** : `PROPOSITION_DISPOSITIF.md` (révisée) ; `REVUE_PROPOSITION_REVISEE_2026-10-29.md`.
Les stories tirées de la revue portent la mention **« revue § 2.x — à confirmer
par LP »**.

# 2. Vocabulaire fixé

| Terme | Valeurs |
|---|---|
| **Résultat** | RELATION_REPEREE · AUCUNE_RELATION_REPEREE · INDETERMINE |
| **Portée au regard du paragraphe** *(si relation)* | ETABLIT_L_ENONCE · EN_ETABLIT_UNE_PARTIE · ECLAIRE_SEULEMENT |
| **Type d'écart** *(cumulable)* | DATE · CITATION · ATTRIBUTION · SENS · IDENTITE_PIECE |
| **Degré de l'écart** | CONTREDIT · ETABLIT_EN_CADRANT_AUTREMENT · NE_L_ETABLIT_PAS |
| **Avancement** | NON_EXAMINE · PROPOSE · VALIDE · REJETE · A_REVOIR |
| **Auteur** | agent d'examen (CODEX, CLAUDE) · LP |

**Grille v1.1.** Le degré porte sur l'énoncé identifié dans la description,
jamais sur la vérité objective des événements. Ne pas écrire « ne dit pas
explicitement » si la pièce dit le contraire. Lorsqu'un paragraphe attribue
des mots ou un fait à une pièce, contrôler leur présence dans la cote ; si
absents, chercher localement dans le même fil ou document, nommer le modèle
et le pk où ils se trouvent, puis proposer IDENTITE_PIECE. Toute recherche
reste dans les accès autorisés. Les versions historiques sont conservées ;
la qualification des écarts de ces versions peut être consignée dans le
dossier de recette sans réécrire une décision de LP.

# 3. Les stories

Format : *En tant que…, je veux…, afin de…* · **Critère de succès** · **Test**.

## Phase 0 — ancrage et premiers examens, hors application

### VA01 — Instantané du constat
*En tant que LP, je veux un instantané versionné du constat (287 énoncés avec
texte, ordre et numéro imprimé ; 515 liens ; 268 cotes), afin que tout examen
porte sur un état connu.*
- **Critère** : `legal/verification_appuis/constat/` contient l'instantané et
  ses empreintes ; deux générations successives sont identiques octet pour
  octet ; les numéros viennent de `concordance_md_imprime.json`, jamais du `.md`.
- **Test** : sur fixture (3 énoncés, 4 liens, dont un paragraphe des 47 à
  numéro décalé) : générer deux fois, comparer les octets ; vérifier que le
  paragraphe décalé porte son numéro **imprimé**.

### VA02 — Contrôle d'ancrage
*En tant que LP, je veux qu'une série d'examens refuse de démarrer si le
constat a bougé, afin de ne jamais examiner un texte modifié.*
- **Critère** : `verifier_ancrage` sort en code 0 si tout concorde ; sinon code
  non nul et liste des énoncés, liens ou cotes en écart.
- **Test** : instantané de fixture, puis modifier un mot d'un énoncé dans la
  base de test → code non nul, l'énoncé nommé ; supprimer un lien → idem.

### VA03 — Liste de travail ordonnée
*En tant que LP, je veux la liste de tous les liens à examiner, dans l'ordre
de priorité, afin de savoir quoi faire et ce qui reste.*
- **Critère** : 515 liens, plus les paragraphes sans référence, signalés à
  part ; ordre : § 234-236, puis P-19/P-40/P-42, puis § 200-217, puis le reste
  dans l'ordre de l'acte ; chaque ligne a son numéro imprimé.
- **Test** : fixture couvrant chaque groupe → l'ordre de sortie respecte les
  quatre groupes ; nombre de lignes = liens + paragraphes sans référence.

### VA04 — Format du fichier d'attente et son validateur
*En tant que LP, je veux un format d'observation unique et contrôlé, afin que
l'import en base (VA20) ne trouve aucune ligne invalide.*
- **Critère** : schéma JSONL `va-observation/1` documenté ; le validateur
  refuse : un résultat sur un lien NON_EXAMINE ; une RELATION_REPEREE sans
  élément observé ni localisation ; une AUCUNE_RELATION_REPEREE sans
  périmètre lu ; un INDETERMINE sans obstacle ; une VALIDE sans auteur LP.
- **Test** : une ligne conforme et une ligne par cas de refus → la conforme
  passe, chaque autre échoue avec son motif.

### VA05 — Fiche d'examen d'un lien
*En tant que LP, je veux pour chaque lien une fiche qui réunit le paragraphe
entier, son numéro imprimé, la référence telle que citée et le support exact
de la pièce, afin de lire la bonne chose.*
- **Critère** : la fiche donne le chemin, l'empreinte (manifeste d'extraction
  du 29 oct.) et la qualification du support (« dérivé en base » pour une
  photo) ; pour P-19, P-40, P-42 : le scan.
- **Test** : fixture avec un courriel et une photo → l'empreinte affichée est
  égale au SHA-256 recalculé du fichier ; la photo est qualifiée de dérivé.

### VA06 — Enregistrer une observation proposée
*En tant que Claude, je veux ajouter une observation PROPOSE au fichier
d'attente, afin que LP la valide.*
- **Critère** : ajout seulement, aucune ligne existante modifiée ; auteur CLAUDE,
  date, empreinte de l'énoncé et de la pièce.
- **Test** : empreinte du fichier avant l'ajout = empreinte des lignes
  antérieures après ; la nouvelle ligne passe VA04.

### VA07 — Valider, corriger ou rejeter
*En tant que LP, je veux valider, corriger ou rejeter une observation, afin que
seules mes validations comptent.*
- **Critère** : chaque décision crée une **nouvelle version** qui renvoie à la
  précédente (`remplace`) ; rien n'est écrasé ; une correction proposée
  n'écarte pas la dernière version validée tant qu'elle n'est pas validée.
- **Test** : proposer → valider → corriger : 3 versions, chaîne `remplace`
  intacte ; la version courante validée reste celle d'avant la correction
  jusqu'à la validation de la correction.

### VA08 — Portée au regard du paragraphe *(revue § 2.1 — à confirmer par LP)*
*En tant que LP, je veux que toute relation repérée dise si la pièce établit
l'énoncé tel qu'écrit, en établit une partie ou l'éclaire seulement, afin de
répondre à la question de départ.*
- **Critère** : RELATION_REPEREE exige une portée ; EN_ETABLIT_UNE_PARTIE exige
  « ce qui reste sans pièce ».
- **Test** : RELATION_REPEREE sans portée → refus ; EN_ETABLIT_UNE_PARTIE sans
  reste → refus ; ETABLIT_L_ENONCE seul → accepté.

### VA09 — Écarts typés *(revue § 2.2 — à confirmer par LP)*
*En tant que LP, je veux que chaque écart de date, de citation, d'attribution,
de sens ou d'identité de pièce soit typé, afin de tous les lister avant les
défenderesses.*
- **Critère** : un écart porte un type et sa description ; plusieurs types
  possibles ; compatible avec tout résultat.
- **Test** : une observation avec écart CITATION et DATE → les deux apparaissent
  dans le rapport des écarts (VA11) ; un type inconnu → refus.

### VA10 — Observation de liasse *(revue § 2.4 — à confirmer par LP)*
*En tant que LP, je veux pouvoir examiner en une observation une liasse citée
en bloc, afin de ne pas faire 23 examens pour les 23 photos de P-56.*
- **Critère** : permise seulement si les liens sont `via_liasse` ; porte le
  manifeste ordonné des membres examinés ; couvre exactement ces liens. Une
  sous-cote nommée exige son propre examen.
- **Test** : liasse de 3 membres citée en bloc → une observation couvre 3 liens ;
  la même tentée sur une sous-cote nommée → refus ; manifeste incomplet → les
  membres manquants restent NON_EXAMINE.

### VA11 — Rapport de couverture et de travail restant
*En tant que LP, je veux savoir à tout moment ce qui est examiné, validé,
indéterminé ou à revoir, afin de piloter l'exercice.*
- **Critère** : dénominateurs visibles ; total = somme des avancements ;
  liste des écarts typés ; paragraphes sans référence à part.
- **Test** : fixture de 10 liens à états variés → les comptes égalent la
  somme ; un lien NON_EXAMINE n'a aucun résultat affiché.

### VA12 — Image du dépôt, paragraphe par paragraphe
*En tant que LP, je veux pour chaque paragraphe son texte complet, son numéro
imprimé, ses références telles que citées et les observations validées, afin
d'avoir l'image du dépôt.*
- **Critère** : seules les versions validées courantes ; propositions en
  attente signalées à part ; export Markdown et JSON des mêmes données.
- **Test** : paragraphe à 3 liens (1 validé, 1 proposé, 1 non examiné) → 1
  observation affichée, 2 restes signalés ; l'export JSON contient les mêmes.

### VA13 — Dérive
*En tant que LP, je veux qu'un changement de texte, de lien ou de support
remette les observations concernées « à revoir », avec leur histoire, afin
qu'aucune validation ne porte sur un état disparu.*
- **Critère** : empreinte d'énoncé ou de pièce différente → A_REVOIR ; l'historique
  reste lisible.
- **Test** : modifier l'empreinte d'une pièce de fixture → son observation
  passe A_REVOIR ; les autres restent VALIDE.

### VA14 — Relecture par paragraphe *(revue § 2.3 — à confirmer par LP)*
*En tant que LP, je veux relire ensemble les pièces d'un paragraphe dès
qu'elles sont toutes examinées, afin d'apprécier comment elles se complètent.*
- **Critère** : refusée tant qu'un lien du paragraphe n'est pas VALIDE ;
  elle cite les observations utilisées (versions) ; A_REVOIR si l'une change.
- **Test** : paragraphe à 2 liens, 1 non validé → refus ; les 2 validés →
  acceptée ; corriger une observation → la relecture passe A_REVOIR.

### VA15 — Liste « art. 99 » *(revue § 2.5 — à confirmer par LP)*
*En tant que LP, je veux la liste des paragraphes qui allèguent plusieurs
faits, afin de préparer leur scission dans la demande modifiée.*
- **Critère** : sous-produit des fragments validés ; aucune décision de
  scission prise par l'outil.
- **Test** : un paragraphe à 2 fragments validés y figure ; un paragraphe à 1
  fragment n'y figure pas.

### VA16 — Pilote sur la prescription
*En tant que LP, je veux éprouver la grille sur les § 234-236 avant tout le
reste, afin de la corriger tôt.*
- **Critère** : tous les liens des § 234-236 examinés et validés par LP ; au
  moins une contribution **limitée** (une date, un échange) décrite comme telle ;
  ajustements de grille consignés dans le journal des versions de l'épic.
- **Test** : **recette par LP** sur la fiche produite par VA12 pour ces trois
  paragraphes ; VA11 affiche 100 % validé sur ce périmètre.

### VA17 — Relecture d'ensemble
*En tant que LP, je veux l'appréciation globale du dépôt une fois tout
examiné, afin d'avoir l'image complète.*
- **Critère** : refusée tant que la couverture n'est pas complète et
  courante ; cite les relectures par paragraphe utilisées.
- **Test** : un lien NON_EXAMINE → refus nommant le lien ; tout VALIDE →
  acceptée.

## Phase 1 — le lot de persistance en base

### VA18 — Conception du lot
*En tant que LP, je veux la spécification, les quatre vues UML par use case
(activité, séquence, ERD cible, classes), la revue B et mon approbation de la
version précise, afin d'ouvrir le lot selon le processus.*
- **Critère** : documents dans `docs/architecture_c/lots/<LOT>/` ; approbation
  datée ; mandat écrit avec fichiers modifiables et **interdictions** (aucune
  écriture dans le doc 9, le bordereau, les appuis).
- **Test** : liste de contrôle du processus (§ 2-5 de `PROCESSUS_CHANGEMENT.md`)
  cochée et référencée ; C0-A intégré ou dérogation écrite de LP.

### VA19 — Modèles et migration
*En tant que LP, je veux les tables des observations, fragments, versions et
relectures, liées au constat en PROTECT, afin de persister sans toucher au
constat.*
- **Critère** : migration sur clone ; aucune colonne ajoutée ni modifiée dans
  `Statement`, `BordereauDepotJuillet`, `AppuiDepotJuillet`.
- **Test** : diff du schéma avant/après limité aux tables nouvelles ; supprimer
  un `AppuiDepotJuillet` portant une observation → refusé.

### VA20 — Import contrôlé du fichier d'attente
*En tant que LP, je veux importer les observations de la phase 0, afin de ne
rien refaire.*
- **Critère** : idempotent ; auteurs, dates et validations conservés tels
  quels ; aucune validation inventée ; comptes égaux à ceux du fichier.
- **Test** : importer deux fois → aucun doublon ; une ligne PROPOSE reste
  PROPOSE ; comptes base = comptes fichier.

### VA21 — Saisie et validation en base
*En tant que LP, je veux proposer et valider dans l'application, afin que le
fichier d'attente cesse d'être nécessaire.*
- **Critère** : mêmes règles que VA04, VA07 à VA10, appliquées en base.
- **Test** : rejouer en base les tests de VA04, VA07 à VA10 → mêmes verdicts.

### VA22 — Parité des rapports
*En tant que LP, je veux que les rapports tirés de la base soient identiques à
ceux du fichier pour les mêmes données, afin de prouver que la bascule ne
change rien.*
- **Critère** : VA11, VA12 et VA13 identiques octet pour octet entre les deux
  sources.
- **Test** : même fixture chargée en fichier et en base → rapports identiques.

### VA23 — Intégration du lot
*En tant que LP, je veux le lot intégré selon les six conditions du processus,
afin qu'il soit « fait ».*
- **Critère** : rapport d'exécution au répertoire du lot ; tests verts sur le
  socle principal ; fusion autorisée ; limites réaffectées nommément.
- **Test** : liste des six conditions (§ 5 du processus) cochée et référencée.

## Clôture

### VA24 — Livraison de l'image du dépôt
*En tant que LP, je veux l'image complète et expliquée du dépôt, afin de m'en
servir pour la demande modifiée, les interrogatoires et la concordance.*
- **Critère** : VA12 et VA17 validés ; couverture à 100 % ; aucun A_REVOIR ;
  export livré avant la rédaction finale de la demande modifiée.
- **Test** : **recette par LP** ; VA02 en code 0 le jour de la livraison.

# 4. Ordre et dépendances

```
VA01 → VA02 → VA03 → VA04 → VA05 → VA06 → VA07
                                   ├→ VA08, VA09, VA10   (à confirmer par LP)
                                   └→ VA11 → VA12 → VA13
VA16 (pilote) dès VA07 ; VA14 après VA12 ; VA15 après les fragments ; VA17 en fin de passes
Phase 1 : VA18 → VA19 → VA20 → VA21 → VA22 → VA23 (après C0-A ou dérogation)
VA24 : clôture
```

**Avant le 6 novembre** : rien de cet épic n'est requis. **Avant le 1er février
2027** : VA01 à VA17 dans le fichier d'attente suffisent à livrer l'image ; la
phase 1 peut suivre.
