# Validation des renvois de pièces ↔ bordereau

> **Nature.** Journal des validations croisées entre la demande, les documents de faits et le bordereau des pièces. Mise à jour : **2026-07-18**.
> **Bordereau final de dépôt :** [bordereau_bloc_depot.md](bordereau_bloc_depot.md) (P-1 → P-99, avec index des sous-cotes).
> **Table de correspondance (model+pk → P-cote) :** [bordereau_pieces.md](bordereau_pieces.md) — colonnes « Fichier d'appui » + « Source (base) ». C'est le **pont** entre le système de travail et les cotes finales.
> **Rappel des deux numérotations** (cf. [feedback_referencing_cotes] en mémoire) : *model+pk* (travail, vérifiable en base : `pdf-1`, `email-16`, `document-1`…) vs *P-cote* (final). ⚠️ Les « P-1/P-2… » écrits dans de vieux fichiers sont souvent des **exhibits de la Requête 2015** qui **entrent en collision** avec les P-cotes finales.

## PASSE FINALE — BORDEREAU DE DÉPÔT DU 18 JUILLET 2026

**Documents contrôlés :** `demande_DEPOT_2026-07-21.md` et `bordereau_bloc_depot.md`.

- Les **99 cotes racines P-1 à P-99** figurent une seule fois au bordereau et sont toutes rattachées à au moins un paragraphe numéroté de la demande.
- Les **21 cotes citées par sous-cote** dans la demande sont indexées; P-79, liasse citée globalement, est également indexée. L’index comporte **159 sous-pièces**, sans doublon ni trou de numérotation.
- P-43 comporte **19 courriels**, et non 16. Les renvois des paragraphes 22 à 24 de la demande ont été corrigés en conséquence.
- Le renvoi au voilier du 13 juillet 2013 est P-57.20, non P-57.19.
- Les contenus réels de P-7, P-14, P-34 et P-72 ont été contrôlés contre leurs sources; leurs descriptions et les allégations correspondantes ont été calibrées.
- P-3, P-6 et P-10 sont conservées et reliées respectivement aux paragraphes 43, 62 et 74; P-87 est reliée aux paragraphes 75 et 240; P-93 et P-94 sont reliées au paragraphe 214.
- L’ancien paragraphe 100 de `requete_secton_faits_lp.md` cite désormais P-20. Dans la demande renumérotée, le fait correspondant se trouve aux paragraphes 123, 124 et 188.
- La convention **R2015-P-n** distingue les anciennes cotes de la Requête du 19 novembre 2015. Les correspondances actives sont P-8 = R2015-P-2, P-13 = R2015-P-5 et P-15 = R2015-P-4.

---

## PASSE 1 — Exposé des faits ↔ bordereau

**Objet :** [requete_secton_faits_lp.md](requete_secton_faits_lp.md) (76 cotes racines, 182 occurrences) croisé avec [bordereau_des_pieces_demande.md](bordereau_des_pieces_demande.md).

**Verdict : très solide.** Aucune référence pendante ; ~74/76 cotes employées dans un contexte cohérent (date + nature). Le piège P-2 (plan)/P-8 (transfert « il me donne la garde ») est **bien distingué** dans l'exposé.

> **Ajout du 16 juillet 2026 — P-90.** Le calendrier Danse HDP (PhotoDocument id=4) est désormais coté P-90 et cité aux §26-B et 101. Il sert à établir la structure des sessions en combinaison avec P-83 et les communications contemporaines; il n'est pas utilisé seul comme horaire historique personnel de la défenderesse.

### Anomalies (2)

| Cote | Bordereau | Exposé | Statut |
|---|---|---|---|
| **P-7** (pdf-2) | « 4 mars 2015 — ébauche Poirier » | cité comme « offre du 20 avril » (§138, §197, §219, §304, §345) | ✅ **RÉSOLU** — 4 mars = ébauche ; la transmission du 20 avril est **attestée par P-9** (réponse Me Ayoub du 27 avril → « missive du 20 avril »). Ne rien changer au bordereau ; **tightener la formulation de l'exposé** (« ébauche P-7 + transmission attestée par P-9 »). |
| **P-64** (chatsequence-11) | « 3 février 2015 » | employé aussi pour un échange du **13 février** (cabane à sucre, §111/§113) | ⚠️ **À CORRIGER au bordereau** — redater « **3 au 13 février 2015** » (ou marquer liasse). |

### Pièces au bordereau, non citées dans l'exposé — ~~11~~ → **6** (MAJ 2026-07-16)

**✅ Résolues (5) :** **P-28, P-29, P-31, P-33** → désormais citées au **nouveau bloc pension** de l'exposé (« Les représentations relatives aux revenus des parties au formulaire du 21 octobre 2019 », §399-A→X) ; **P-4** → cité au §356-A (opposition au chalet, bloc saisine).

**Restantes (6) :** `P-3, P-6, P-10, P-12, P-41, P-87`
- **Authentification / corroboration** : P-87 (transmet le courriel P-2), P-12 (certificat de baptême), P-41 (marraine).
- **Contexte 2013 / réserve** : P-3, P-6, P-10.
- **Décision :** les rattacher à un § (les citer) ou les retirer du bordereau si non plaidées.

> **Note — nouveau bloc (2026-07-16).** Le **volet pension / revenu de la mère** (net juré comme brut) était **absent de l'exposé** alors que la coquille le plaidait déjà (§ 9, § 13, § 26 Chaîne B, § 30 a). Comblé : bloc inséré chronologiquement entre le bloc grand-mère (§399) et le bloc 2023 (§400). Cotes utilisées : P-26, P-28, P-29, P-31, P-33, P-34, P-35 — toutes résolvent. Débloque la **Chaîne B** (causalité) et **R0** (préjudice).

---

## PASSE 2 — Fichiers `faits/` ↔ bordereau

**Objet :** les 15 fichiers de `legal/faits/`, via leur section « Pièces citées ».

### Constat systémique

Les fichiers `faits/` **ne sont pas réconciliés** au bordereau final : leurs « Pièces citées » sont sur le **système de travail** (model+pk), avec des étiquettes « P-N » / « B-N » **périmées** (numéros d'exhibits Requête 2015 / défense) qui **collisionnent** avec les cotes finales. Les références **nommées `piece_X`**, elles, mappent proprement et sont **quasi toutes présentes**.

### Corrections APPLIQUÉES (cotes périmées → convention model+pk) ✅

| Fichier | Corrigé le 2026-07-16 |
|---|---|
| `par14-17_2015` | « P-1 » (plan) → **pdf-1** (3× corps + Pièces citées) |
| `par18_2015` | « P-2 » (msgs 7 avril) → **piece_p2_messages_7avril2015** (3×) ; « P-1 » (plan) → **pdf-1** (faits 1, 56 + « Cadre ») ; Pièces citées nettoyée |
| `par20-21_2015` | « P-1 » (plan) → **pdf-1** (2× + Pièces citées) ; « B-2 » → **email-365** (corps + Pièces citées + note maj) |
| `par7-8_2023` | « P-384 » → **email-330** ; « P-386 » → **email-3** ; « B-16 » → **email-462** |

**Préservé à dessein** (références verbatim/adverses, PAS des cotes de LP) : la « pièce P-2 » de la Requête (§18) et la « **Pièce P-2 en liasse** » (liste d'offres déposée par l'adverse au PV du 4 nov. 2019, `par7-8`).

### Fichiers sans section « Pièces citées » (à doter)

- `faits_par20_2019.md` ❌
- `faits_par3_2019.md` ❌

### État par fichier (13 avec section)

| Fichier | Présence | Gaps / notes |
|---|---|---|
| `par4-5-6_2015` | doc-1, cs-3/4/5/8/9/10/11, thread-18, thread-12, pdf-59 ✅ | ❌ **chatsequence-6** ; emails de contexte non cotés (29, 81, 91, 305, 590, 603) |
| `par7_2015` | doc-1, pdf-35→P-35, photodocs 1/2→P-67, pdfs 45-58→P-66, pdf-1→P-2 ✅ | emails/events de volume — plusieurs non cotés (contexte) |
| `par9_2015` | doc-1, event-312→P-80, email-34→P-81, pdf-60→P-78 ✅ | ❌ **photo-5, pdf-90, pdf-91** ; emails de volume partiels |
| `par10_2015` | doc-1, pdf-1, pdf-60, email-39/137 ✅ | ❌ **PDFDocument id=11 (évaluation agréée)** |
| `par14-17_2015` | doc-1, pdf-2/3/5/6, photo-4558, email-16, thread-6 ✅ | ~~collisions~~ ✅ corrigé ; **email-275** hors liasse P-22 |
| `par18_2015` | doc-1, pdf-2→P-7, pdf-3→P-9 ✅ | ~~collisions~~ ✅ corrigé ; **email-267** hors P-22 |
| `par20-21_2015` | doc-1, pdf-1, thread-109→P-4, email-365→P-3, pdf-2/3/5/6 ✅ | ~~« P-1 »/« B-2 »~~ ✅ corrigé |
| `par23-24_2015` | doc-1, pdf-2/3/5/6, email-399→P-10 ✅ | ❌ **email-401** (thread-100) |
| `par28-29_2015` | doc-1→P-19, thread-écrément→P-14, photo-4551→P-15 ✅ | — **propre** |
| `par30-31_2015` | doc-1, email-343→P-11, photodoc-13→P-13, pdf-5/6 ✅ | ❌ **email-404** (thread-100) |
| `par56-57_2015` | doc-1→P-19, pdf-63→P-84, pdf-64→P-85 ✅ | — **propre** |
| `par59_2015` | thread-109→P-4, pdf-2/3/6 ✅ | `piece_vacances_…` = synthèse (sous-jacents P-4/P-5/P-71) |
| `par7-8_2023` | pièces nommées existent (P-40, P-42, P-34…) | ~~« P-384/P-386/B-16 »~~ ✅ corrigé ; section « À compléter » (extractions en attente) |

---

## ACTIONS À PRENDRE (consolidé)

### A. Gaps — sources citées, ABSENTES du bordereau → coter ou retirer le fait

1. **PDFDocument id=11** — évaluation agréée 2013 (`par10`, réfute le §10 rachat résidence).
2. **email-401 / email-404** — thread-100 (correspondance Poirier) — `par23-24`, `par30-31`.
3. **chatsequence-6** — `par4-5-6`.
4. **photo-5 / pdf-90 / pdf-91** — `par9` (été 2013) — à vérifier.
5. **thread-6 : email-267, email-275** — non énumérés dans la liasse P-22.
6. **Liste d'offres « P-2 en liasse »** (exhibit adverse, PV 4 nov. 2019) — à **extraire et coter** (cote finale distincte de P-2) ; `par7-8` la marque « à extraire ».

### B. Bordereau — corrections

7. **P-64** → redater « 3 au 13 février 2015 ».
8. **Doublons de nommage** à consolider : `pdf-35` = `avis_cotisation_pere_2018` ; `pdf-30` = `avis_cotisation_pere_2019`.
9. **P-7** — description : « ébauche du 4 mars 2015 ; transmission du 20 avril attestée par P-9 » (facultatif, pour lever l'ambiguïté).

### C. Fichiers de faits — à compléter

10. Doter `par20_2019` et `par3_2019` d'une section « Pièces citées ».
11. Décider du sort des **11 pièces du bordereau non citées** (Passe 1) : les rattacher ou les retirer.

### D. Rédaction (plus tard)

12. Dans l'exposé, tightener les renvois « lettre du 20 avril, P-7 » → « ébauche P-7 + transmission attestée par P-9 ».

---

## Légende
✅ présent / corrigé · ❌ absent (gap) · ⚠️ à corriger · ~~barré~~ = résolu cette session.
