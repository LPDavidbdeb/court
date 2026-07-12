# REGISTRE DES PIÈCES — inventaire canonique `(model, PK)` ↔ cote P- + bordereau

> **Source unique de vérité du dossier.** Inventaire **dédupliqué** de toutes les sources distinctes citées dans l'exposé consolidé [requete_secton_faits_lp.md](../requete_secton_faits_lp.md). Une source = une seule entrée = une seule cote future, quel que soit le nombre de sections qui l'invoquent. Cotes P- **provisoires** (`PP-xx`) en Phase A ; figées en Phase B, **dans l'ordre de première invocation**, sur signal de gel. Le mapping fin `P-[●]` → cote se fait au **rendu**.
>
> **Statut :** ✅ pièce/verbatim extrait · ⚠️ source en base, `piece_`/collecte à faire · ❌ à sourcer.
> **Recevabilité :** 🟢 libre · 🟡 privilège de règlement (à trancher) · 🔴 secret professionnel (à trancher) · 🔵 avocat-client du demandeur (renonciation à délimiter).
> **Nature :** *natif* · *agrégé* (liasse d'`Event`/photos + index généré).

## ⚠️ Flags à trancher (priorité)

1. **Conflit `PDFDocument 35`** : cité comme **relevé Hydro-Québec** (résidence distincte 2011, `faits_par7`) **et** comme **avis de cotisation 2018** (bordereau antérieur, volet 2023). Deux pièces différentes ne peuvent partager une cote — **vérifier lequel est pdf-35** et coter l'autre séparément.
2. ❌ **6 mars 2012** (« rentrer tôt car elle danse ») — aucune `Email id` dans `faits_par4-5-6` ni `faits_par14-17` → **à sourcer** ou retirer (PP-33).
3. ⚠️ **9 déc. 2010** (calendrier danse) — `Email 80` vs `100`/`81` à confirmer (PP-30).
4. **Recevabilité — trois familles à faire trancher avant le gel** : P-1 (🔴), correspondance de négociation pdf-2/3/5/6/7 (🟡), courriels du demandeur à ses avocats (🔵). Elles changent la trame et la séquence des cotes.
5. **Pièce omise ajoutée — `ChatMessages 111-146`** (inventaire des activités et coûts des enfants, 23 oct. 2014) : absente du registre → **ajoutée en PP-66** (réconciliation avec l'inventaire atomique §4-6).
6. **`Email 488`** : gardé **distinct** d'`Email 53` (doublon / variante / messages liés — non tranché).
7. **Fairmont n° 62292490** (`.eml`, **sans PK**) : source sans identifiant DB → à **coter à la main** lors de la collecte.
8. **`PhotoDocument 4`, `PhotoDocument 15`** : à situer dans une liasse. **`Email 163`** (fil fiscal, propos du **défendeur**) : à **exclure** comme fondement (réserve du dossier).
9. **`PDFDocument 6`** : confirmer qu'il s'agit bien de la **lettre du 2 sept. 2015** (PP-11, 🟡) et non d'une autre pièce.
10. **Constituants des liasses** : les `Event`/`Email` atomiques (dont `Event 256`, `Event 327`) qui étendent les plages de mes liasses (escalade, parcs, tableau récap.) sont énumérés dans l'inventaire atomique `union_exhaustive_pieces_paragraphes_4-5-6.xlsx` — qui sert d'**index de contenu** des liasses.

## 1. Inventaire canonique (par famille)

### I. Actes de procédure et jugements

| Prov. | Désignation | Model + PK | Recev. | Statut | Sections |
|---|---|---|---|---|---|
| PP-01 | Requête assermentée du 19 nov. 2015 | Document 1 | 🟢 | ✅ | §4-6,7,9,14-17,18,20-21,23-24,28-29,30-31,56-57,59 |
| PP-02 | Jugement du 14 janv. 2016 | PDFDocument 14 | 🟢 | ✅ | §4-6 (portée) + volet effets |
| PP-03 | Jugement intérimaire du 27 sept. 2019 (« aucun revenu ») | PDFDocument 15 | 🟢 | ✅ | §3-2019, 2023 |
| PP-04 | Procès-verbal + jugement du 4 nov. 2019 | PDFDocument 13 | 🟢 | ✅ | §3-2019, 2023 |
| PP-05 | Déclaration assermentée du 21 oct. 2019 (DA-2019) | Document 3 | 🟢 | ✅ | §3-2019, §7-2019, §20-2019, 2023 |
| PP-06 | Dénonciation du 21 juill. 2023 | Document 2 | 🟢 | ✅ | 2023 |

### II. Le courriel du 11 juin 2013 (P-1)

| Prov. | Désignation | Model + PK | Recev. | Statut | Sections |
|---|---|---|---|---|---|
| PP-07 | Courriel de Me Ayoub à Élise Ayoub, 11 juin 2013 | PDFDocument 1 | 🔴 | ✅ | §7,14-17,18,20-21,3-2019 |

### III. Correspondance de négociation entre procureurs

| Prov. | Désignation | Model + PK | Recev. | Statut | Sections |
|---|---|---|---|---|---|
| PP-08 | Offre de garde partagée 2-2-3 (ébauche 4 mars / lettre 20 avr. 2015) | PDFDocument 2 | 🟡 | ✅ | §14-17,18,20-21,23-24,59,3-2019 |
| PP-09 | Lettre de Me Ayoub du 27 avr. 2015 | PDFDocument 3 | 🟡 | ✅ | §14-17,18,20-21,23-24,30-31,59,3-2019 |
| PP-10 | Projet de consentement du 13 août 2015 | PDFDocument 5 | 🟡 | ✅ | §14-17,20-21,23-24,30-31,3-2019 |
| PP-11 | Réponse du demandeur du 2 sept. 2015 | PDFDocument 6 | 🟡 | ✅ | §14-17,20-21,23-24,30-31,59,3-2019 |
| PP-12 | Lettre de Me Ayoub du 3 sept. 2015 | PDFDocument 7 | 🟡 | ✅ | §3-2019 |

### IV. Messages textes et courriels entre les parties

| Prov. | Désignation | Model + PK | Recev. | Statut | Sections |
|---|---|---|---|---|---|
| PP-13 | P-2 — messages du 7 avr. 2015 + transfert du 21 avr. (« il me confirme qu'il me donne la garde ») | piece_p2_messages_7avril2015 ; Email 267 (thread-6) | 🟢 | ✅ | §18,20-21,14-17 |
| PP-14 | Fil du 27 févr. 2015 — déclarations de la défenderesse | Email 22, 167, 171 (thread-18) | 🟢 *(pas les propos du demandeur du fil)* | ✅ | §4-6 |
| PP-15 | Courriel du 11 janv. 2016 | Email 16 (thread-12) | 🟢 | ✅ | §4-6,7,14-17 |
| PP-16 | Fil du 16 sept. 2016 (« jamais traité d'incapable » ; aide familiale) | Email 6, 8, 305, 275 (thread-6) | 🟢 | ✅ | §4-6,14-17,18 |
| PP-17 | Fil du 30 juin 2013 (chalet) | thread-109 | 🟢 | ✅ | §20-21,59 |
| PP-18 | Baptême de Nicolas (19 juill. 2015) + confirmation paroissiale | Email 343 (thread-76) ; Email 633 (thread-158) | 🟢 | ✅ | §30-31 |

### V. ChatSequences (SMS entre les parties, 2014-2015)

| Prov. | Désignation | Model + PK | Recev. | Statut | Sections |
|---|---|---|---|---|---|
| PP-19 | SMS — solidarité financière et coordination (prêt 9 000 $, « nous 4 », matelas, cabane à sucre, etc.) | ChatSequence 3, 4, 5, 6, 8, 9, 10, 11 | 🟢 | ✅ | §4-6 |
| PP-66 | Inventaire des activités et coûts des enfants (23 oct. 2014) | ChatMessages 111 → 146 | 🟢 | ⚠️ | §4-6, §14-17 |

### VI. Communications du demandeur à ses avocats

| Prov. | Désignation | Model + PK | Recev. | Statut | Sections |
|---|---|---|---|---|---|
| PP-20 | 26 juin 2013 → Me Pringle | Email 365 (thread-89) | 🔵 | ✅ | §20-21,3-2019 |
| PP-21 | 27 avr. / 8 mai 2015 → Me Poirier | Email 399, 401 (thread-100) | 🔵 | ✅ | §23-24 |
| PP-22 | 12 mai 2015 → Me Poirier | Email 404 (thread-100) | 🔵 | ✅ | §30-31 |
| PP-23 | 15 mai 2015 → Me Poirier (P-1 jointe) | Email 475 (thread-116) | 🔵 + 🔴 | ✅ | §3-2019 |

### VII. Implication parentale — courriels à l'employeur (BNC)

| Prov. | Désignation | Model + PK | Recev. | Statut | Sections |
|---|---|---|---|---|---|
| PP-24 | Liasse — absences pour soins d'Alexia (11+) | Email 42,45,47,51,53(/488),55,56,59,61,64,69 | 🟢 | ⚠️ | §4-6,7,14-17 |
| PP-25 | Absence 19 déc. 2014 | Email 27 | 🟢 | ⚠️ | §14-17 |
| PP-26 | Diagnostic contesté 3 mai 2011 | Email 118 | 🟢 | ⚠️ | §7 |
| PP-27 | Coordination garderie/école | Email 54, 369, 371, 29 | 🟢 | ⚠️ | §4-6,14-17 |
| PP-28 | Petite enfance 2010 (soins, natation) | Email 590, 603, 91 | 🟢 | ⚠️ | §4-6 |
| PP-29 | « bon papa » 12 sept. 2011 | Email 382, 383 | 🟢 | ⚠️ | §7 |
| PP-30 | Calendrier danse 9 déc. 2010 | Email 80 *(100/81 ⚠️)* | 🟢 | ⚠️ | §4-6 |
| PP-31 | Infidélité / départ 2011 | Email 84, 85, 106 | 🟢 | ✅ | §7 |
| PP-32 | « rentrer tôt car elle danse » 6 mars 2012 | Email **?** | 🟢 | ❌ **à sourcer** | §4-6,14-17 |

### VIII. Implication parentale — Events / activités (liasses agrégées)

| Prov. | Désignation | Model + PK | Recev. | Statut | Sections |
|---|---|---|---|---|---|
| PP-33 | Natation YMCA | Event 62 | 🟢 | ⚠️ | §4-6,14-17 |
| PP-34 | AcroGym | Event 136, 150 | 🟢 | ⚠️ | §4-6,14-17 |
| PP-35 | Soccer (match + médailles) | Event 239, 263 | 🟢 | ⚠️ | §4-6,9,14-17 |
| PP-36 | Escalade (11×) | Event 316 → 326 | 🟢 | ⚠️ | §4-6,9 |
| PP-37 | Routine du soir pendant la danse (fév. 2011) | Event 46, 52 | 🟢 | ⚠️ | §4-6,7,14-17 |
| PP-38 | Présence pendant la danse (2014) | Event 274, 278 | 🟢 | ⚠️ | §4-6 |
| PP-39 | Accompagnement maternelle (oct. 2012) | Event 213, 214 | 🟢 | ⚠️ | §4-6,14-17 |
| PP-40 | Parc Alexandra (≥15) | Event 25,54,75,76,79,80,82,83,88,171,172,180,235,237,240 | 🟢 | ⚠️ | §4-6,7 |
| PP-41 | Famille paternelle (repas/fêtes) | Event 36, 37, 140, 284, 291 | 🟢 | ⚠️ | §4-6 |
| PP-42 | Voilier des grands-parents (13 juill. 2013) | Event 254 | 🟢 | ⚠️ | §9 |
| PP-43 | Cape Cod avec Nicolas (14 août 2013) | Event 259 | 🟢 | ⚠️ | §4-6,9 |
| PP-44 | Été 2013 — sorties familiales (jazz, Bromont, ferme, etc.) | Event 241-267, 312-320 | 🟢 | ⚠️ | §9 |
| PP-45 | Voyage à Cuba (sept.-oct. 2011) | Event 113 → 125 | 🟢 | ⚠️ | §7 |

### IX. Pièces documentaires et structurelles

| Prov. | Désignation | Model + PK | Recev. | Statut | Sections |
|---|---|---|---|---|---|
| PP-46 | Tableau récapitulatif (≥190 occ. / 1 100+ photos) | piece_tableau_recap_evenements | 🟢 | ⚠️ | §4-6,7,9,14-17 |
| PP-47 | Biographie de danse de la défenderesse | PDFDocument 59 | 🟢 | ✅ | §14-17 |
| PP-48 | Relevé Hydro-Québec (résidence distincte 2011) ⚠️ *voir Flag 1* | PDFDocument 35 ; PhotoDocument 1, 2 | 🟢 | ⚠️ | §7 |
| PP-49 | Factures de thérapie (Pistorio) | PDFDocuments 45 → 58 | 🟢 | ⚠️ | §7 |
| PP-50 | RQAP — congé parental 2009 | piece_photo-4558 | 🟢 | ⚠️ | §14-17 |
| PP-51 | Été 2013 — pièces documentaires | PDFDocument 60, 90, 91 ; PhotoDocument 5 | 🟢 | ⚠️ | §9 |
| PP-52 | Intervention Écrement (16 sept.–7 oct. 2015) | thread-ecrement_2015 ; piece_photo-4551 | 🟢 | ⚠️ | §28-29 |
| PP-53 | Certificat de baptême | piece_photodoc-13 *(+ pdf-80)* | 🟢 | ⚠️ | §30-31 |
| PP-54 | Relevés d'assurance Industrielle Alliance 2015-2016 | PDFDocument 63, 64 | 🟢 | ✅ | §56-57 |
| PP-55 | Avis de cotisation 2019 du demandeur | PDFDocument 30 | 🟢 | ✅ | §3-2019, 2023 |
| PP-56 | Avis de cotisation 2018 du demandeur ⚠️ *voir Flag 1* | PDFDocument 35 ? | 🟢 | ⚠️ | 2023 |
| PP-57 | Salaires médians (Guichet-Emplois) | PDFDocument 12 | 🟢 | ✅ | 2023 |
| PP-58 | Relevé de Revenu Québec (pension ; crédit 1 000 $) | PDFDocument 81 | 🟢 | ✅ | §20-2019 |
| PP-59 | Constat de fin d'emploi BNC (juin 2018) | thread-111_congediement_bnc | 🟢 | ✅ | 2023 |

### X. Communications 2019-2020 (contribution et emploi)

| Prov. | Désignation | Model + PK | Recev. | Statut | Sections |
|---|---|---|---|---|---|
| PP-60 | Courriel du 6 juin 2019 (contribution grand-mère) | Email 484 (thread-119) | 🟢 | ✅ | §20-2019 |
| PP-61 | Courriel B-11 du 21 oct. 2019 (demande de preuve) | Email 485 (thread-120) | 🟢 | ✅ | §7-2019 |
| PP-62 | Transmission des candidatures (15 oct. 2019) | Email 615 (thread-156) | 🟢 | ✅ | 2023 |
| PP-63 | Courriel du 17 févr. 2020 (passeport) | Email 462 (thread-113) | 🟢 | ✅ | 2023 |
| PP-64 | Courriel du 17 avr. 2020 | Email 330 (thread-4) | 🟢 | ✅ | 2023 |
| PP-65 | Courriel du 22 juin 2020 | Email 3 (thread-3) | 🟢 | ✅ | 2023 |

## 2. Bordereau (cotes P- figées)

*(Vide — cotes non figées ; attribution en Phase B, dans l'ordre de première invocation, sur signal de gel.)*

## 3. Journal d'attribution

- Passe de retrace complète effectuée sur `requete_secton_faits_lp.md` (12 sections 2015-2019 + 2023). **65 pièces canoniques provisoires** `PP-01…PP-65`. Cotes non figées.
- **Réconciliation §4-6** avec l'inventaire atomique exhaustif (`union_exhaustive_pieces_paragraphes_4-5-6.xlsx`, 218 réf.) : le registre est exhaustif au niveau **pièces/liasses** ; une omission réelle corrigée (**PP-66**, ChatMessages 111-146) ; flags 5-10 ajoutés. Le classeur atomique sert d'**index des constituants** des liasses.
- Reste : trancher les 10 flags ci-dessus ; puis mapping fin `P-[●]` → cote au rendu (Phase B).
