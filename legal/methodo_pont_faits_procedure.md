# Méthodologie — du fait brut à la demande introductive

> **Objet du document.** Fixer la méthode de transformation des dossiers `faits/` et `analyse/` en paragraphes plaidables pour une demande introductive d'instance. Ce fichier sert de référence de travail et pourra être amélioré au fil des tests.

---

## 1. Problème à résoudre

Le dossier contient déjà deux couches distinctes :

1. **Les faits bruts** (`legal/faits/faits_par...`) : propositions datées, sourcées, sans conclusion.
2. **Les analyses** (`legal/analyse/.../argument...`) : démonstration, qualification, inférences, responsabilité, effet procédural.

Le problème est que la demande introductive ne peut pas simplement recopier l'une ou l'autre couche.

- Recopier les **faits bruts** produit un document trop volumineux et trop probatoire.
- Recopier les **analyses** transforme l'exposé des faits en plaidoirie.
- Intégrer directement la preuve dans les allégations risque de violer la discipline procédurale : on allègue les faits essentiels, on ne plaide pas la preuve.

La méthode introduit donc une troisième couche : le **pont**.

```text
preuve dense / pièces
→ faits bruts
→ pont / faits plaidables
→ demande introductive
```

---

## 2. Objectif de la couche “pont”

Le pont transforme une démonstration probatoire complexe en **faits essentiels plaidables**, utilisables dans une procédure.

Il doit répondre à quatre questions :

1. **Quelle allégation adverse est visée ?**
2. **Quels faits essentiels doivent être allégués ?**
3. **Quelle inférence ou qualification doit être réservée aux moyens de droit ?**
4. **Quelle preuve soutient chaque fait, sans être plaidée dans le corps du fait ?**

Le pont n'est donc ni un fichier de preuve, ni un mémoire, ni un plaidoyer.

Il est une **chambre de décompression** entre la preuve et la procédure.

---

## 3. Règle cardinale

Dans l'exposé des faits :

```text
Faits : ce qui est arrivé.
Moyens : pourquoi cela constitue une faute.
Pièces : comment on le prouve.
```

Un paragraphe de faits doit normalement contenir :

- une date ou un ancrage temporel ;
- une seule proposition ;
- une source ou cote de pièce ;
- aucun qualificatif juridique ;
- aucune conclusion de mauvaise foi, d'abus, de diffamation ou de mens rea.

---

## 4. Structure recommandée d'un fichier-pont

Chaque fichier-pont devrait être nommé selon l'allégation ou le bloc visé :

```text
legal/pont/pont_par4-5-6_2015.md
legal/pont/pont_par14-17_2015.md
legal/pont/pont_par18_2015.md
```

Structure proposée :

```markdown
# Pont — §X de la Requête de [année]

## 1. Allégation visée

Verbatim ou résumé fidèle de l'allégation adverse.

## 2. Objectif de démonstration

Ce que ce bloc doit établir dans la demande introductive.

## 3. Force probatoire

Très forte / forte / moyenne / faible, avec justification courte.

## 4. Faits essentiels plaidables

1. ...
2. ...
3. ...

## 5. Inférences réservées aux moyens

- ...

## 6. Pièces nécessaires

| Fait | Pièce | Statut |
|---|---|---|
| 1 | P-X | à coter |

## 7. Prudences de rédaction

- Ce qu'il faut concéder.
- Ce qu'il ne faut pas plaider.
- Ce qui est seulement corroboratif.

## 8. Version procédurale distillée

Les seuls paragraphes destinés à être intégrés dans la demande introductive.

## 9. Usage dans la demande introductive

Emplacement du bloc, doublons à éviter et relation avec les ponts déjà intégrés.
```

---

## 5. Typologie des contestations

Chaque contestation doit être classée avant rédaction.

### A. Fausseté affirmative

L'allégation est directement contredite par une pièce ou un faisceau documentaire fort.

Exemples :

- un accord allégué contredit par une offre formelle opposée ;
- un refus allégué contredit par des transactions objectives ;
- une durée alléguée contredite par un registre institutionnel.

Usage : peut soutenir le noyau de la demande.

### B. Demi-vérité ou omission

Le fait allégué est partiellement vrai, mais sa présentation omet un contexte déterminant.

Exemples :

- rapporter une réponse du défendeur sans le geste qui l'a suscitée ;
- présenter un accès restreint comme un choix du père sans rappeler le contexte connu ;
- produire une pièce défavorable sans produire la pièce qui la qualifie.

Usage : utile pour démontrer la présentation trompeuse, mais doit être rédigé avec prudence.

### C. Vrai à concéder

L'allégation est exacte ou substantiellement exacte.

Usage : doit être concédée franchement ; elle peut parfois devenir favorable une fois contextualisée.

### D. Non étayé / non falsifiable / faible rendement

L'allégation est vague, subjective ou trop difficile à réfuter par une pièce précise.

Usage : à abandonner comme cible autonome, ou à utiliser seulement comme contexte corroboratif.

---

## 6. Évaluation de la force probatoire

La force d'un bloc se mesure par la qualité des faits qui le soutiennent.

### Très forte

- Document institutionnel ou tiers neutre.
- Pièce contemporaine directe.
- Aveu ou désaveu de la partie adverse.
- Contradiction discrète, datée, vérifiable.
- Plusieurs sources indépendantes convergent.

### Forte

- Faisceau documentaire cohérent.
- Chronologie serrée.
- Inférence raisonnable appuyée sur plusieurs pièces.
- Peu de dépendance au témoignage du demandeur.

### Moyenne

- Fait vrai, mais sens contesté.
- Démonstration par omission ou contextualisation.
- Une partie de la preuve repose sur connaissance directe ou pièce à verser.
- Risque que l'adverse propose une lecture alternative plausible.

### Faible

- Allégation vague.
- Cible non falsifiable.
- Preuve incomplète ou à sourcer.
- Valeur surtout rhétorique ou corroborative.

---

## 7. Discipline de rédaction

### À faire

- Concéder les faits vrais.
- Séparer la preuve de l'allégation.
- Réduire les faits à leurs éléments essentiels.
- Garder les qualifications pour les moyens.
- Mentionner les pièces par cote, sans recopier tout le verbatim.
- Numéroter chaque fait de façon autonome.

### À éviter

- “La preuve démontre que...”
- “Cela prouve la mauvaise foi...”
- “Il est clair que...”
- “Le plan a causé...”, sauf si la causalité est directement documentée.
- Les théories spéculatives dans l'exposé des faits.
- Les conclusions comme “abusif”, “diffamatoire”, “mensonger”, “instrumental”.

---

## 8. Exemple de transformation

### Fait brut trop probatoire

> Entre mars 2011 et février 2016, le défendeur a adressé à ses supérieurs à la Banque Nationale au moins vingt courriels l'informant qu'il demeurait à la maison ou s'absentait du travail pour s'occuper d'un enfant malade ou l'accompagner à un rendez-vous médical, incluant les courriels id=...

### Fait plaidable

> Entre mars 2011 et février 2016, le demandeur s'est absenté de son travail à plusieurs reprises pour s'occuper des enfants malades ou les accompagner à des rendez-vous médicaux (pièce P-__).

### Inférence réservée aux moyens

> Cette série documentaire est incompatible avec la qualification d'un père “rarement disponible” ou “minimalement impliqué”.

---

## 9. Assemblage de la demande introductive

La demande introductive devrait être assemblée à partir des sections **Faits essentiels plaidables** des fichiers-ponts.

L'assemblage se fait désormais **au fur et à mesure** : dès qu'un pont satisfait au critère de réussite, sa version procédurale distillée est intégrée à la demande introductive. Il ne faut pas attendre que tous les ponts soient terminés.

Ordre recommandé :

1. Parties et contexte.
2. Actes procéduraux visés.
3. Faits essentiels par séquence chronologique.
4. Faits de connaissance.
5. Moyens de droit.
6. Préjudice.
7. Conclusions.
8. Bordereau des pièces.
9. Signature, avis, endos.

Les ponts alimentent principalement les sections 3 et 4.

Les analyses alimentent principalement les moyens de droit.

Les fichiers `piece_*` alimentent le bordereau et les annexes.

### 9.1 Cycle d'intégration continue

Pour chaque bloc contesté :

1. vérifier les sources et les faits bruts ;
2. organiser, au besoin, la preuve détaillée dans une annexe ou un axe ;
3. rédiger le pont ;
4. valider sa force probatoire, ses concessions et ses limites ;
5. extraire une version procédurale distillée ;
6. intégrer immédiatement cette version dans la demande introductive ;
7. inscrire l'effet de cette intégration dans le journal d'évolution de la thèse ;
8. effectuer périodiquement une révision transversale de la procédure.

Le contenu du pont n'est jamais copié intégralement dans la procédure. Seuls les faits essentiels nécessaires à la démonstration y sont transférés. Les raisonnements, verbatims, inventaires de pièces et limites détaillées demeurent dans le pont, les faits bruts et les annexes.

Dans une même version de travail, le niveau de citation doit rester uniforme. Si les cotes ne sont pas encore stabilisées, la procédure peut demeurer sans références internes, à condition que la traçabilité soit conservée dans les ponts et dans une table de correspondance distincte.

### 9.2 Journal d'évolution de la thèse

Le fichier `legal/journal_evolution_these_requete_2015.md` consigne l'impression cumulative qui se dégage de la Requête à mesure que les ponts sont intégrés.

Ce journal est un document de travail interne. Il ne constitue ni une pièce, ni une allégation, ni une conclusion destinée au dépôt.

Il comprend :

- une **synthèse actuelle**, mise à jour après chaque pont ;
- un **historique append-only**, dont les états antérieurs ne sont pas réécrits ;
- les faits nouvellement établis ;
- l'effet de ces faits sur l'impression générale ;
- les thèses qui se renforcent ou s'affaiblissent ;
- les explications alternatives encore possibles ;
- les concessions, limites et questions non résolues ;
- la prochaine démonstration nécessaire.

Le journal doit distinguer explicitement :

```text
fait établi
≠ inférence raisonnable
≠ impression cumulative
≠ hypothèse à vérifier
```

Il doit également consigner les éléments défavorables ou compatibles avec une autre lecture. Sa fonction est de mesurer honnêtement la progression de la thèse, non de confirmer automatiquement l'hypothèse de départ.

### 9.3 Révision transversale périodique

Après quelques intégrations, la procédure doit être relue dans son ensemble afin de :

- préserver une chronologie intelligible ;
- supprimer les répétitions entre les ponts ;
- harmoniser le niveau de détail ;
- vérifier qu'une même source n'est pas utilisée pour soutenir deux propositions incompatibles ;
- distinguer les faits essentiels des moyens de droit ;
- vérifier que chaque bloc contribue à une conclusion recherchée.

La procédure doit raconter une histoire juridique continue, et non juxtaposer une collection de réfutations autonomes.

---

## 10. Application initiale — Requête de novembre 2015

Pour la Requête de novembre 2015, les blocs probatoires les plus forts à transformer en ponts sont :

1. §18 — accord de garde exclusive allégué.
2. §56-57 — refus allégué d'utilisation des assurances.
3. §4-5-6 — relation / implication parentale / aveu du 11 janvier 2016.
4. §14-17 — motif du refus de garde partagée et glissement de l'implication.
5. §9 — “parti tout l'été 2013”.

Les blocs à traiter avec prudence :

- §20-21 : omission de contexte ; éviter les inférences trop affirmatives.
- §23-24 : vrai en partie ; utile comme demi-vérité.
- §10 : mener avec la chronologie, non avec le motif interne.
- §30-31 : concéder §31 ; viser l'omission et la surextension.
- §28-29 : décider si §28 vise le même événement que Dr Écrement ; sinon abandonner.
- §59 : corroboratif seulement.

---

## 11. Critère de réussite

Un fichier-pont est réussi si :

- les faits peuvent être copiés presque tels quels dans une demande introductive ;
- chaque fait est autonome, daté et sourcé ;
- les conclusions juridiques ont été retirées des faits ;
- les concessions sont clairement nommées ;
- les inférences fortes sont conservées pour les moyens ;
- les zones spéculatives ou faibles sont écartées ou rétrogradées.
- une version procédurale distillée a été intégrée à la demande introductive ;
- l'intégration a été consignée dans le journal d'évolution de la thèse ;
- la table de correspondance entre pont, procédure, annexes et pièces a été mise à jour.
