# 31 — État du plan de rédaction de la nouvelle version

> **Question du demandeur, 14 octobre 2026** : existe-t-il un plan de rédaction
> de la nouvelle version de la demande ?
>
> **Réponse initiale : non, pas un plan unique.** Quatre pièces existent, trois d'entre
> elles sont solides, et ce qui manque est nommable. Ce fichier relève l'état;
> il **ne choisit aucune architecture** — ce choix est expressément réservé au
> demandeur (`legal/METHODOLOGIE_POST_DEPOT.md` § 4.1 et § 10).
>
> ⚠️ **Mise à jour du 14 octobre 2026, même jour.** Le demandeur a tranché
> pour la section « EXPOSÉ DES FAITS » : périmètre limité à cette section,
> principe organisateur **par actes de la partie adverse, chronologiquement**
> (requête de nov. 2015 → déclaration assermentée de 2019 → dénonciation d'un
> moyen déclinatoire). Voir le [32](32_plan_expose_des_faits.md). Ce qui suit
> est conservé tel quel, sous réserve des corrections datées ci-dessous.

**État courant — précisions du demandeur, 14 octobre 2026.** Le
[32](32_plan_expose_des_faits.md) consigne une **structure de rédaction
incomplète**, fondée sur l'analyse de la requête de 2015, de l'affidavit de
2019 et de la dénonciation d'un moyen déclinatoire. Pour chaque acte : **une
démonstration majeure complexe et plusieurs démonstrations plus simples**.
Les **trois démonstrations complexes sont désormais précisées**; la troisième
vise **P-40 § 8** et comporte deux temps (§ 5.6 du 32).
**Aucune démonstration simple n'est précisée à ce stade.**

**Continuité.** Avant toute nouvelle évaluation des démonstrations, consulter
le [32](32_plan_expose_des_faits.md) § 5.7, **« Objections déjà examinées »**.
Une réouverture exige un élément nouveau ou une erreur précise et
l'explication de ce qui rend la réponse déjà retenue insuffisante.

---

## 1. Ce qui existe

### 1.1 La proposition de fond et son architecture — pour une partie seulement

[`25_presentation_argument_complet.md`](25_presentation_argument_complet.md) § 1
propose sept parties (I à VII) et dit pourquoi dans cet ordre : l'allégation et
son socle, puis la conduite de son autrice, puis ses paroles, puis la réalité,
puis le remède refusé, puis le coût, puis la seule partie qui argumente.

**Statut inchangé : « proposition de Claude, 30 septembre 2026 — non arrêtée »**,
avec huit points à arbitrer à son § 3 (cotes à attribuer, chevauchement avec le
bloc du § 3 de 2019, contexte omis, ce qui reste en argumentation, ton,
privilège des règlements, ¶ 24 du bloc 21, ¶ 7 c).

⚠️ **Cette architecture ne couvre pas l'acte.** Son périmètre est celui du
[`02_perimetre_et_exclusions.md`](02_perimetre_et_exclusions.md) : les
§§ 4-6, 7 et 14-18 de la requête du 19 novembre 2015. Les §§ 13, 19-21 et 23-24
en sont exclus. L'acte déposé compte 198 paragraphes numérotés et des
sections I à VIII.

### 1.2 Un ordre de travail — arrêté, et partiellement exécuté

[`00_README.md`](00_README.md) : on arrête les **allégations**
([14](14_allegations_proposees.md)), on les porte au **texte**
([13](13_texte_assemble.md)), puis on ajoute le **niveau 3** — densité,
tableaux chronologiques, liasses.

| Étape | État |
|---|---|
| Allégations | base constituée |
| Texte | **incomplet** — sept allégations établies n'y figurent pas : A2, A3, A4, A5, A8, B6, C9 |
| Niveau 3 | non commencé |

Blocs arrêtés : [20](20_bloc_juin2013_projet.md) (juin 2013),
[21](21_bloc_aout2015_projet.md) (août 2015),
[22](22_bloc_desaveu_explicite_projet.md) (désaveu explicite),
[23](23_bloc_11janvier_transformation.md) (11 janvier 2016).
[24](24_demonstration_sincerite_et_presentation.md) porte la sincérité et la
présentation de la preuve récurrente; [30](30_evaluation_trois_propositions.md)
l'évaluation des trois propositions jurées.

### 1.3 La machine — opérationnelle depuis aujourd'hui

E01 est **validée, 18/18**. Le trou identifié le 7 octobre dans
[`../instance/suivi_paragraphes_en_base.md`](../instance/suivi_paragraphes_en_base.md)
§ 2 — « il manque un seul champ », le lien d'un paragraphe reformulé vers son
antécédent — **est comblé** : `document_manager.concordance` fournit
`relier`, `confirmer_traitement`, `antecedents_de`, `appuis_dorigine`,
`detacher_pour_edition`, `supprimer_occurrence`.

| | Source | Cible |
|---|---|---|
| Document | **9** — acte déposé | **10** — version 2 |
| Mode | `STORED` | `AUTO` |
| Nœuds | 371 | — |
| Paragraphes | 198 | 2 admissibles |

[`lot_editorial_01.md`](../amendements/01_avant_notification/lot_editorial_01.md)
§ 11 : **étape 1 appliquée le 14 octobre** sur l'instruction « commençons par 1 » —
985 (§ 93) → 1233 (§ 1), `REFORMULE`, `deplace=True`, `CONFIRME`; appui P-19
confirmé pour la teneur de l'acte, non sa véracité; deux ancrages de citation,
dont le libellé historique « P-2 » conservé littéral sur le nœud 1243.

**Compteur réel : 1 paragraphe sur 198.** L'export strict reste refusé pour
EX02 (197 occurrences source sans décision, plus le § 2 cible) et EX05 (appuis
du § 2 non examinés).

### 1.4 Le cadre de contrainte

[`../instance/communication_pieces.md`](../instance/communication_pieces.md)
§ 10 fixe ce que la réécriture impose, et deux règles de méthode qui valent
comme contraintes de rédaction :

- **la table de concordance se construit pendant la réécriture, pas après** —
  « un paragraphe amendé qui s'écrit sans son antécédent est un paragraphe à
  refaire » (§ 10.5);
- **le balayage amendé → déposé est celui qui défend** — il renseigne le
  demandeur sur ce qui est repris, reformulé, fusionné, abandonné et nouveau.
  Ce n'est pas une règle de droit : l'art. 206 permet ce qu'il permet
  (position du demandeur, 13 octobre, § 10.2 b).

---

## 2. Ce qui reste à préciser dans le plan

| | Manque | Conséquence |
|---|---|---|
| a | ✅ **Tranché le 14 oct. pour l'EXPOSÉ DES FAITS** — par actes de la partie adverse, chronologiquement ([32](32_plan_expose_des_faits.md)). **Reste ouvert pour les autres sections** de l'acte, que la décision ne rouvre pas; la grille de 12 critères du § 4.4 n'a jamais été appliquée | Le fichier 25 demeure une proposition sur un périmètre partiel, à raccorder au premier axe du nouveau plan |
| b | **Aucun projet pour les sections hors des trois blocs** — §§ 13, 19-21, 23-24 exclus du périmètre de l'atelier. Les sections de l'acte autres que l'exposé des faits ne sont pas rouvertes par la décision du 14 oct. | Les paragraphes du déposé qui portent la charge probatoire restent sans projet : le lot 01 § 5 en relève cinq (§§ 95, 97, 101, 102, 105) totalisant 28 appuis |
| c | **Aucun ordre de traitement des 197 occurrences restantes, aucun découpage en lots au-delà du lot 01** | « Combien de temps » reste sans réponse, faute de dénombrement du travail |
| d | **Aucune date, aucun jalon** | Rien ne s'inscrit au protocole du 1er novembre |

### Les décisions du § 10.4 — mise à jour

| Décision | État au 7 oct. | État au 14 oct. |
|---|---|---|
| Renumérotation et réécriture intégrale | ✅ tranchée le 7 oct. | inchangée |
| Quel candidat du dépôt fait référence | ❌ **préalable bloquant** | ✅ **tranchée le 13 oct.** — version simple de 44 pages, endos inclus (`PROJECT_CONTEXT.md`; `identification_du_fichier_imprime.md`) |
| Combien de pièces additionnelles, déjà extraites ? | ❌ non tranchée | **toujours non tranchée** |

➜ **Le préalable qui bloquait l'estimation est levé.** Ce qui reste ouvert est
une décision de périmètre, et elle appartient au demandeur.

---

## 3. L'horizon réel

⚠️ **L'échéance du 19 septembre 2026 est consommée.** La signification a été
faite le **17 septembre 2026** aux deux défenderesses et l'interruption est
acquise (`../instance/echeancier.md` § 1). `AGENTS.md` et `PROJECT_CONTEXT.md`
présentent encore le 19 septembre comme « échéance gouvernante » : ce relevé
est périmé et doit être corrigé par le demandeur.

Ce qui gouverne désormais la rédaction :

| Date | Objet | Source |
|---|---|---|
| depuis le 17 sept. | communication des **pièces** — seule la liste a été signifiée (art. 145 al. 1, « dans les plus brefs délais ») | `echeancier.md` |
| **1er novembre 2026** | **protocole de l'instance** — c'est là que le calendrier de l'amendement et celui de la communication deviennent des termes de l'instance (art. 207 al. 2) | `communication_pieces.md` § 10.3 |
| après notification de l'acte modifié | **10 jours** pour s'opposer (art. 207); le moyen est l'art. 206 — « une demande entièrement nouvelle sans rapport avec la demande initiale » | `communication_pieces.md` § 10.5 a |
| jusqu'à l'inscription | 🔴 chaîne art. 173 → 177 C.p.c. → 2894 C.c.Q. : l'interruption acquise se **défait rétroactivement** à défaut de diligence | `../instance/carte_de_l_instance.md` § 3.2 |

**Échéance utile : avant le 1er novembre — 18 jours.** Non pas pour faire le
travail, mais pour **arrêter le périmètre** et pouvoir inscrire une date.

---

## 4. Ce qu'un plan devrait trancher

Posé comme questions, sans réponse suggérée :

1. ~~**Architecture.**~~ ✅ **Tranchée le 14 oct. pour l'exposé des faits** —
   voir le [32](32_plan_expose_des_faits.md). Demeure à trancher : comment le
   fichier 25 § 1, bâti sur les trois blocs de P-19, se raccorde au premier
   axe du nouveau plan.
2. **Sort des paragraphes hors périmètre.** Repris tels quels, reformulés, ou
   abandonnés délibérément ? Un abandon est toujours sûr; une disparition sans
   décision ne l'est pas.
3. **Découpage en lots.** Le lot 01 traite deux paragraphes. Sur quel critère
   se forment les lots suivants — par bloc d'allégation, par section de l'acte,
   par densité d'appuis ?
4. **Pièces additionnelles.** Combien, et combien sont déjà extraites en
   `piece_<model>-<id>.md` ? Une pièce déjà extraite ne coûte que son
   rattachement; une pièce à extraire coûte l'extraction, l'assemblage et
   l'empreinte.
5. **Ce qui est inscrit au protocole.** Une date d'amendement, une date de
   communication, ou les deux.

---

## 5. Inscriptions

- 14 octobre 2026 — création. Aucune architecture choisie, aucun texte d'acte
  modifié, aucune donnée en base touchée. Relevé de l'existant et des décisions
  ouvertes, avec la mise à jour des trois décisions du
  `communication_pieces.md` § 10.4 et le signalement du relevé périmé du
  19 septembre dans `AGENTS.md` et `PROJECT_CONTEXT.md`.
- 14 octobre 2026, même jour — révision après la décision du demandeur sur
  l'EXPOSÉ DES FAITS. L'en-tête, le § 2 a, le § 2 b et la question 1 du § 4
  sont corrigés : ce qui y était ouvert est tranché pour cette section et
  demeure ouvert pour le reste de l'acte. Plan : [32](32_plan_expose_des_faits.md).
- 14 octobre 2026, même jour — précision du cadrage et de l'état courant :
  structure incomplète, une démonstration majeure complexe et plusieurs
  démonstrations simples par acte. Les trois démonstrations complexes sont
  désormais précisées; la troisième porte sur P-40 § 8 et ses deux temps
  sont consignés au § 5.6 du [32](32_plan_expose_des_faits.md). Aucune
  démonstration simple n'est précisée. Aucune donnée en base touchée.
- 14 octobre 2026, même jour — renvoi vers les objections déjà examinées au
  § 5.7 du [32](32_plan_expose_des_faits.md), à consulter avant toute nouvelle
  évaluation des démonstrations. Règle de réouverture approuvée par le
  demandeur. Aucune donnée en base touchée.
