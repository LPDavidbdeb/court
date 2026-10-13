# Vérification — les numéros de paragraphes du fichier `.md` ne sont pas tous ceux de l'acte imprimé

> **Constat du 7 octobre 2026**, relevé en prenant connaissance du dossier de P-2.
> **Registre :** vérification matérielle. Aucun contenu n'est en cause — seuls les
> **numéros** le sont, donc les **ancrages** (« ¶ n de la demande déposée ») que le
> corpus utilise pour mesurer la plaidabilité.
>
> **Portée.** L'acte déposé est un document **papier** (`AGENTS.md`). La
> vérification porte sur deux candidats de l'archive gelée :
> `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.md` (source
> de travail, numéros **littéraux**) et le `.pdf` du même nom (sortie mise en
> page). ~~**Lequel des cinq candidats a été imprimé demeure indéterminé**
> (`PROJECT_CONTEXT.md`) ; le présent constat valait pour le PDF vérifié, et les
> deux autres `.docx` de la demande présentent le même mécanisme.~~
>
> ## ✅ Réserve levée — 13 octobre 2026
>
> L'acte déposé est identifié : la **version simple de 44 pages, endos inclus**
> — `demande_DEPOT_2026-07-21.docx` ou son PDF. Confirmé sur le papier par le
> demandeur : 44 pages, endos, premier § numéroté « 1 », trous 110→112, 118→122
> et 139→143. La reconstitution de la numérotation de Word donne **la même suite
> de numéros** pour les quatre candidats de la demande : ils diffèrent par la
> mise en page, non par la numérotation. Seule la **copie 2** de `_double`, issue
> d'une impression d'essai écartée, en porte une autre.
>
> ➜ **Le constat ci-dessous vaut donc pour l'acte déposé lui-même**, et non plus
> seulement pour « le candidat PDF ». Les **47 paragraphes sur 179** sont ceux du
> papier. Détail et méthode :
> [`identification_du_fichier_imprime.md`](identification_du_fichier_imprime.md).
>
> ➜ **La table complète des 198 paragraphes existe désormais** :
> [`concordance_md_imprime.md`](concordance_md_imprime.md). Bâtie par une
> méthode indépendante — reconstitution depuis le XML du `.docx` —, elle
> retrouve **les onze ancrages du § 3 ci-dessous** et le même total de
> **47 écarts sur 179**.

## 1. Le mécanisme

Dans le `.md`, la numérotation est écrite à la main : elle comporte 179
paragraphes numérotés, dont le dernier porte le n° **241**, 19 paragraphes à
suffixe littéral (`8-A`, `9-B`, `103-C`…) et **62 numéros sautés**.

À la conversion, chaque bloc de liste reçoit un `startOverride` Word égal au
**premier** numéro du bloc, puis s'incrémente de 1 à chaque élément. Deux
conséquences :

- un numéro sauté **entre deux blocs** est absorbé — la numérotation se recale ;
- un numéro sauté **à l'intérieur d'un bloc** décale **tout le reste du bloc**.

C'est pourquoi la divergence n'est ni générale ni aléatoire : elle est **locale,
par bloc**, et elle commence exactement là où un numéro manque au `.md`.

## 2. Résultat

| | Nombre |
|---|---|
| Paragraphes numérotés comparés | 179 |
| Numéro **identique** dans le PDF | 132 |
| Numéro **différent** dans le PDF | **47** |

Le premier décalage est **¶ 41 et ¶ 42, absents du `.md`** : ils existent
pourtant à l'impression, où ils portent le texte que le `.md` numérote 43 et 44.

## 3. Ce que cela change pour le bloc de juin 2013

| Ancrage employé dans le corpus | Objet | Numéro imprimé |
|---|---|---|
| ¶ 38 | « comme si tu étais une cliente » / « le plan serait le suivant » | **38** ✅ |
| ¶ 39 | l'objectif attribué + la routine que les juges hésitent à changer (LP-1, LP-2, LP-5) | **39** ✅ |
| ¶ 40 | violence conjugale depuis la naissance + DPJ ; non-reprise en 2015 (LP-1, LP-7) | **40** ✅ |
| ¶ 43 | P-3 — le courriel du 26 juin 2013 à Me Pringle | **41** ⚠️ |
| ¶ 45 | « faire signifier une procédure avant le départ du demandeur » (LP-4) | **43** ⚠️ |
| ¶ 46 | « Le courriel du 11 juin prévoyait une comparution le vendredi 14 » (LP-4) | **44** ⚠️ |
| ¶ 50 | « je vois les enfants à tous les jours » (19 juillet 2013 ; these_test_sincerite, Partie XII) | **48** ⚠️ |
| ¶ 72 | la lettre du 27 avril refusant la garde partagée (LP-8) | **67** ⚠️ |
| ¶ 81 | le projet du 13 août 2015 (LP-9) | **81** ✅ |
| ¶ 110 | « aucune rétractation écrite » (LP-7) | **110** ✅ |
| ¶ 9-B | accès avec couchers non subordonnés à une évaluation (LP-6, LP-7) | suffixe littéral, conservé ✅ |

**Les trois ancrages qui portent le cœur de P-2 — ¶ 38, 39 et 40 — sont exacts.**
Ce sont LP-4 (calendrier), LP-8 et le ¶ 50 de la Partie XII qui visent un autre
numéro que celui de l'acte imprimé.

## 4. Les 47 divergences

| ¶ au `.md` | ¶ au PDF | Début du paragraphe |
|---|---|---|
| 43 | 41 | Le 26 juin 2013, le demandeur a écrit à sa procureure, Me Suzanne Prin |
| 44 | 42 | En juin 2013, les parties faisaient toujours vie commune avec Alexia,  |
| 45 | 43 | Selon le demandeur, la défenderesse projetait alors de voyager à Cuba  |
| 46 | 44 | Le demandeur reconnaît un court intervalle sans contact avec les enfan |
| 47 | 45 | Selon le demandeur, l’absence d’Alexia de ce voyage résultait du refus |
| 48 | 46 | La participation d’Alexia au soccer est documentée du 28 mai au 24 aoû |
| 49 | 47 | Le 29 juillet 2013, la grand-mère paternelle a écrit au demandeur : «  |
| 50 | 48 | Le 19 juillet 2013, le demandeur écrivait qu’il voyait les enfants tou |
| 51 | 49 | Entre les 14 et 19 juillet 2013, la défenderesse a organisé une fête d |
| 65 | 64 | Le 4 mars 2015, son procureur a préparé une proposition de garde parta |
| 66 | 65 | Le 20 avril 2015, le demandeur a transmis par son procureur la lettre  |
| 71 | 66 | Le 27 avril 2015, Me Marie-Josée Ayoub a affirmé au nom de la défender |
| 72 | 67 | Cette lettre refusait la garde partagée en invoquant le jeune âge, des |
| 74 | 68 | Après réception, le demandeur a écrit à son procureur qu’il conservera |
| 76 | 69 | Le même jour, le demandeur a expliqué à son procureur qu’une seule nui |
| 80 | 79 | Le 1er août 2015, le demandeur a demandé à la défenderesse de vérifier |
| 84 | 83 | Le 2 septembre 2015, le demandeur s’est dit « tout à fait disposé à ét |
| 87 | 84 | Le 3 septembre, Me Marie-Josée Ayoub a répondu que la défenderesse se  |
| 91 | 90 | Le 7 octobre, il a annulé cette rencontre « en ce qui a trait à la gar |
| 104 | 103 | Au paragraphe 18, la défenderesse a allégué : |
| 136 | 135 | Le 23 janvier 2019, Me Marie-Josée Ayoub a reconnu que le demandeur ét |
| 138 | 136 | Le 19 août 2019, Allianz Technology SE München, succursale de Bucarest |
| 139 | 137 | Les 26 et 27 septembre 2019, le demandeur a informé Me Marie-Josée Ayo |
| 141 | 138 | Ce jugement ordonnait aussi à la défenderesse de fournir au demandeur, |
| 142 | 139 | Le 15 octobre 2019, le demandeur a transmis à Me Marie-Josée Ayoub l’a |
| 145 | 144 | Au paragraphe 3, la défenderesse a affirmé : |
| 151 | 150 | Au paragraphe 20 de sa déclaration, la défenderesse a affirmé : |
| 158 | 157 | La déclaration de revenus 2018 de la défenderesse indiquait un revenu  |
| 160 | 158 | Selon son avis de cotisation 2018, le revenu total du demandeur était  |
| 162 | 159 | Dans son propre formulaire pour l’année 2019, le demandeur déclarait u |
| 163 | 160 | Le 21 octobre 2019, la défenderesse a transmis au demandeur deux talon |
| 172 | 171 | Le 25 mars 2020, le demandeur a avisé sa propriétaire que, vu les circ |
| 173 | 172 | Le 17 avril 2020, le demandeur a écrit à Me Marie-Josée Ayoub qu’il ar |
| 175 | 173 | Le 22 juin 2020, le demandeur a écrit à la défenderesse qu’il n’exista |
| 178 | 177 | Au paragraphe 6, la défenderesse a reconnu que le demandeur avait subi |
| 182 | 181 | Ni P-42 ni P-40 ne reprochaient au demandeur d’avoir quitté volontaire |
| 189 | 188 | Quant à P-19, le demandeur reproche le passage allégué d’une répartiti |
| 192 | 189 | Quant à P-42 et P-29, les fautes alléguées concernent la présentation  |
| 196 | 195 | La qualité d’avocate de Me Marie-Josée Ayoub et les obligations de bon |
| 199 | 198 | Le concert allégué entre les défenderesses repose sur la séquence suiv |
| 220 | 219 | Le demandeur invoque également l’usage sélectif des normes relatives à |
| 221 | 220 | Conformément au paragraphe 8, P-2 n’est invoqué ni comme publication a |
| 222 | 221 | Le cours de conduite allégué de 2015 à 2023 comprend la répétition de  |
| 224 | 222 | Si le demandeur établit sommairement que les actes en cause peuvent co |
| 230 | 229 | La solidarité sollicitée vise uniquement les dommages-intérêts compens |
| 239 | 238 | Le demandeur ne produit pas ces pièces pour opposer aux défenderesses  |
| 240 | 239 | Subsidiairement, si certaines parties de cette correspondance étaient  |

## 5. Suites

- [ ] Établir lequel des cinq candidats a été imprimé — préalable à toute
      correction d'ancrage (règle déjà posée au `METHODOLOGIE_POST_DEPOT.md` § 3.1).
- [ ] Décider la règle : soit la version amendée adopte une numérotation continue
      sans numéro sauté, soit les ancrages du corpus sont réécrits sur les numéros
      imprimés. Ne pas mélanger les deux.
- [ ] Corriger, le cas échéant, les ancrages de `dossier_plaidoirie/02_inventaire_contradictions.md`
      (LP-4, LP-8) et de `these_test_sincerite_2013.md` (Partie XII, ¶ 50).
- [ ] Vérifier les ancrages de `PROJECT_CONTEXT.md` : § 234 (prescription) est
      exact ; §§ 237-239 (privilège des règlements) sont touchés — 239 s'imprime 238.

## 6. Méthode, pour qu'elle soit rejouable

Texte du PDF extrait avec `fitz` (PyMuPDF), chaque paragraphe du `.md` recherché
par ses 55 premiers caractères, puis lecture du numéro qui le précède
immédiatement dans le PDF. Les ¶ 5 et 6 ne sont retrouvés qu'après retrait des
marqueurs `**` du Markdown ; ils concordent.
