# Découpage du lot 2 — Table de décision

La comparaison porte sur la [version archivée le 23 novembre 2026](../archive/2026-11-23_avant_decoupage). Les deux blocs de la branche source `fiches/email-16-portee-retrait` au commit `7511971` étaient identiques à cette archive. La première étiquette de chaque ligne est conservée sur la première partie.

## Partie I — Décisions

| Ancienne étiquette | Type | Scindé ? | Raison | Étiquettes après découpage, dans l’ordre |
|---|---|---|---|---|
| `p1-declarations` | C | Non | Les neuf passages du même acte gardent leur date, leur autrice, leur ordre et la marque de coupure. | `p1-declarations` |
| `p1-effets` | R | Oui | La séparation, le refus du partage et l’entente alléguée sont trois objets d’explication distincts. Le premier suit immédiatement les extraits. | `p1-effets`, `p1-effet-refus`, `p1-effet-entente` |
| `p1-portrait-historique` | R | Oui | La représentation commune est distinguée de chacune des trois fonctions qui lui sont attribuées. Les trois traits qui définissent le portrait restent ensemble. | `p1-portrait-historique`, `p1-frictions-conjugales`, `p1-justification-refus`, `p1-justification-entente` |
| `p1-connecteurs` | R | Oui | Trois liens textuels ont des fonctions distinctes. Chaque mot cité reste avec son paragraphe et son interprétation. Le constat sur les deux ensembles suit. | `p1-connecteurs`, `p1-connecteurs-refus`, `p1-connecteur-entente`, `p1-articulation` |
| `p1-unite-acte` | M | Oui | L’absence de connecteur entre les deux ensembles reste avec leur appartenance au même acte. La reconstitution de la représentation commune est une conclusion distincte. | `p1-unite-acte`, `p1-representation-commune` |
| `p1-qualification-participation` | M | Oui | L’absence de mesure du temps, les termes de la requête, la portée d’une inégalité d’horaire et la lecture de ces paragraphes sont distingués. | `p1-qualification-participation`, `p1-termes-participation`, `p1-repartition-inegale`, `p1-portee-participation` |
| `p1-presence-et-residence` | C | Non | Les deux conduites sont ici les termes de deux passages cités de la même requête. Les extraits et leur attribution restent ensemble. | `p1-presence-et-residence` |
| `p1-disponibilite` | M | Oui | Les passages sur le père et la mère restent ensemble avec leur attribution. La conclusion sur le sens de la disponibilité suit. | `p1-disponibilite`, `p1-sens-disponibilite` |
| `p1-portrait-qualitatif` | R | Non | La suppression hypothétique des mots du § 15 et l’énumération de ce qui subsiste servent une seule conclusion sur la portée du portrait. | `p1-portrait-qualitatif` |
| `p1-pere-engage` | R | Non | Un seul rapprochement entre le portrait et une participation qui serait inégale en heures. | `p1-pere-engage` |
| `p1-demande-partage` | M | Oui | La volonté reconnue au § 14 est un fait documentaire. Sa portée pour l’appréciation du portrait reste avec sa limite sur la participation antérieure. | `p1-demande-partage`, `p1-portee-volonte` |
| `p1-incidence-tribunal` | M | Oui | La présentation de chaque parent précède les deux inférences possibles. La continuité des soins garde la précision sur le jeune âge. La synthèse conserve le critère de l’article 33. | `p1-incidence-tribunal`, `p1-role-secondaire`, `p1-continuite-maternelle`, `p1-capacite-incertaine`, `p1-deux-directions` |
| `p1-responsabilites-comparees` | R | Non | Une seule conclusion sur le poids du jeune âge considéré avec les responsabilités comparées. La réserve sur l’âge isolé est indissociable. | `p1-responsabilites-comparees` |
| `p1-these` | R | Oui | La fonction explicative de la thèse, son contenu comparatif et sa portée pour le refus sont trois conclusions distinctes. | `p1-these`, `p1-these-comparative`, `p1-portee-justification` |
| `p1-axes` | F | Oui | Les deux objets de contestation sont distincts. Les quatre axes restent l’énumération des appuis de cette contestation. | `p1-axes`, `p1-connaissance`, `p1-quatre-axes` |

## Axe 4 — Décisions

| Ancienne étiquette | Type | Scindé ? | Raison | Étiquettes après découpage, dans l’ordre |
|---|---|---|---|---|
| `ax4-portrait` | F | Non | Le fait est la présentation que donne la requête. La seconde proposition situe son exposé dans la demande. | `ax4-portrait` |
| `ax4-partage-responsabilites` | F | Oui | Le partage entre les parties, leur coordination et l’exercice de chacune des dimensions par le demandeur sont distincts. Les bornes de la vie commune qualifient la période. | `ax4-partage-responsabilites`, `ax4-coordination-parties`, `ax4-dimensions` |
| `ax4-soirs-de-danse` | M | Oui | L’horaire de danse reste avec ses bornes hebdomadaires et annuelles. La charge exercée seul est distinguée pour chacune des deux périodes. La conclusion sur la présence suit. | `ax4-soirs-de-danse`, `ax4-danse-alexia`, `ax4-danse-deux-enfants`, `ax4-presence-continue` |
| `ax4-garderie` | M | Oui | La répartition des trajets selon les horaires et les soins au retour sont deux faits. Leur portée pour l’organisation de la semaine suit. Les trajets du matin et du soir restent ensemble, car le partage porte sur l’horaire dans son ensemble. | `ax4-garderie`, `ax4-soins-retour`, `ax4-organisation-semaine` |
| `ax4-activites` | M | Oui | L’accompagnement et la garde de l’enfant sans cours sont deux actes. La variation selon les semaines est conservée. La conclusion porte sur le développement par les activités. | `ax4-activites`, `ax4-enfant-sans-cours`, `ax4-developpement-activites` |
| `ax4-enfants-malades` | F | Oui | Trois circonstances de l’absence au travail. La maladie reste avec le fait de prendre soin de l’enfant. Aucune des circonstances n’est présentée comme exclusive. | `ax4-enfants-malades`, `ax4-medecin`, `ax4-defaut-garde` |
| `ax4-sorties` | M | Oui | Les sorties conservent leur fréquence et l’initiative du demandeur. L’appréciation de son investissement suit immédiatement. | `ax4-sorties`, `ax4-investissement` |
| `ax4-famille-paternelle` | M | Oui | La coupure maintenue par Élise, l’organisation de la présence des enfants et le fait de les emmener sont distincts. La conclusion conserve que le lien dépendait du seul demandeur. | `ax4-famille-paternelle`, `ax4-organisation-famille`, `ax4-deplacements-famille`, `ax4-lien-paternel` |
| `ax4-vie-quotidienne` | M | Oui | Les repas, les bains, les couchers et les jeux relèvent du même partage mais peuvent être admis séparément. La conclusion conserve la présence et la disponibilité au quotidien. | `ax4-vie-quotidienne`, `ax4-bains`, `ax4-couchers`, `ax4-jeux`, `ax4-disponibilite-quotidienne` |
| `ax4-cooperation` | M | Oui | La répartition selon les disponibilités, l’exercice par chacune des parties et la coordination au jour le jour sont distincts. Les questions de coordination restent les exemples du même constat. | `ax4-cooperation`, `ax4-part-assumee`, `ax4-coordination-quotidienne`, `ax4-cooperation-familiale` |
| `ax4-participation` | M | Oui | L’exercice avec la défenderesse et la prise en charge de plusieurs responsabilités par le demandeur seul sont distingués. Les deux conclusions portent sur les termes contestés puis sur le portrait d’ensemble. | `ax4-participation`, `ax4-responsabilites-seul`, `ax4-termes-contestes`, `ax4-portrait-vie-commune` |
| `ax4-frictions` | M | Oui | La séparation admise reste avec la contestation de l’asymétrie décrite. Le lien entre répartition et frictions, puis celui entre frictions et fin de la vie commune, sont deux conclusions distinctes. | `ax4-frictions`, `ax4-cause-frictions`, `ax4-fin-vie-commune` |

## Relevé mot à mot

Chaque ligne compare un paragraphe de l’archive à toutes ses parties. Une occurrence déplacée dans le même groupe se compense. Les répétitions ajoutées et les mots grammaticaux remplacés sont comptés. Le relevé neutralise la casse, la forme d’apostrophe, la ponctuation extérieure aux citations et le balisage des listes, des italiques et des étiquettes. Chaque renvoi à un paragraphe ou à une annexe compte pour une unité. Le contrôle distinct des citations compare tous leurs caractères dans leur ordre d’apparition. Un tiret indique un écart nul.

### Partie I — Mots et renvois

| Paragraphe de l’archive | Mots ou fiches ajoutés | Mots ou fiches retirés | Renvois ajoutés | Renvois retirés |
|---|---|---|---|---|
| `p1-declarations` | `la`, `dans`, `requête` | — | — | — |
| `p1-effets` | `les` ×3, `neuf` ×2, `paragraphes` ×2, `de` ×3, `la` ×3, `requête` ×3, `expliquent` ×2, `ensemble` ×2 | `ces` | `{§p1-declarations/f}`, `{§p1-declarations/j}` | — |
| `p1-portrait-historique` | `les`, `des`, `paragraphes`, `4`, `à` ×2, `7`, `14`, `18`, `de` ×4, `la` ×4, `requête`, `représentation` ×2, `historique` ×3, `l'implication` ×3, `du` ×3, `demandeur` ×3, `est` ×2, `invoquée` ×2, `pour`, `surtout`, `justifier` | `ces`, `et`, `cette` | `{§p1-declarations}`, `{§p1-declarations/c}`, `{§p1-effet-refus}`, `{§p1-portrait-historique}`, `{§p1-declarations/j}` | — |
| `p1-connecteurs` | `de` ×3, `la` ×3, `requête` ×3 | — | `{§p1-declarations}`, `{§p1-declarations/f}`, `{§p1-declarations/g}`, `{§p1-declarations/j}`, `{§p1-connecteurs..p1-connecteur-entente}` | — |
| `p1-unite-acte` | `les`, `allégations`, `des` ×3, `paragraphes` ×2, `4` ×2, `à` ×4, `10` ×2, `et` ×2, `14` ×2, `18` ×2, `la`, `le` | `ces`, `leur`, `cette` | `{§p1-portrait-historique}`, `{§p1-articulation..p1-unite-acte}` | — |
| `p1-qualification-participation` | `la` ×2, `requête` ×2, `du` ×3, `temps`, `dans`, `19`, `novembre`, `2015`, `élise`, `ayoub`, `demandeur`, `de`, `inégale`, `consacré`, `aux`, `enfants`, `les`, `sur`, `l'implication` | `ces`, `telle`, `or`, `elle` | `{§p1-qualification-participation..p1-repartition-inegale}` | — |
| `p1-presence-et-residence` | `affirmée`, `solennellement`, `par`, `élise`, `ayoub`, `le` ×2, `19`, `novembre`, `2015`, `historique` | `ce` | — | — |
| `p1-disponibilite` | `la` ×4, `requête` ×2, `affirmée`, `solennellement`, `par`, `élise`, `ayoub`, `le` ×3, `19`, `novembre`, `2015`, `présente`, `demandeur` ×3, `et`, `mère`, `dans`, `les`, `termes`, `suivants`, `au`, `du` | `lorsque`, `cette`, `un`, `celui`, `elle`, `lui` | `{§p1-portee-participation..p1-disponibilite}` | — |
| `p1-portrait-qualitatif` | `le`, `historique`, `du`, `demandeur`, `la`, `de`, `requête` | `ce` | `{§p1-termes-participation}`, `{§p1-presence-et-residence}`, `{§p1-disponibilite/a}` | — |
| `p1-pere-engage` | `dans`, `la`, `requête` | `ainsi` | `{§p1-repartition-inegale}`, `{§p1-portrait-qualitatif}` | — |
| `p1-demande-partage` | `la` ×2, `demandeur`, `une`, `garde`, `partagée`, `dès`, `rupture`, `du`, `d'instaurer` | `cette` | — | — |
| `p1-incidence-tribunal` | `la` ×6, `défenderesse`, `dans` ×3, `requête` ×3, `soins`, `et`, `responsabilités`, `parentales`, `le`, `demandeur`, `présenté`, `des` ×2, `à`, `attribués`, `du`, `historique` | `ce`, `cette`, `sa` | `{§p1-incidence-tribunal}`, `{§p1-declarations/g}`, `{§p1-role-secondaire}`, `{§p1-continuite-maternelle..p1-capacite-incertaine}` | — |
| `p1-responsabilites-comparees` | — | — | `{§p1-incidence-tribunal..p1-capacite-incertaine}` | — |
| `p1-these` | `de` ×2, `la` ×4, `requête` ×2, `et`, `des`, `responsabilités`, `parentales`, `familiales`, `comparative` | `identifiées`, `cette` ×2, `qui`, `c'est` | `{§p1-effets..p1-effet-entente}`, `{§p1-portrait-qualitatif}`, `{§p1-incidence-tribunal..p1-role-secondaire}` | — |
| `p1-axes` | `le`, `demandeur` ×3, `conteste`, `la` ×3, `du` ×4, `portrait`, `historique`, `présenté` ×2, `dans` ×2, `requête` ×2, `l'inexactitude` | `de`, `ce`, `et`, `son`, `inexactitude`, `sa` | — | — |

### Axe 4 — Mots et renvois

| Paragraphe de l’archive | Mots ou fiches ajoutés | Mots ou fiches retirés | Renvois ajoutés | Renvois retirés |
|---|---|---|---|---|
| `ax4-portrait` | — | — | — | — |
| `ax4-partage-responsabilites` | `pendant` ×2, `toute` ×2, `la` ×2, `vie` ×2, `commune` ×2, `les`, `parties`, `responsabilités`, `parentales` | `et` | — | — |
| `ax4-soirs-de-danse` | `la` ×3, `défenderesse` ×2, `cours` ×2, `de` ×8, `danse` ×2, `le` ×2, `les` ×2, `tel` ×2, `qu'il` ×2, `appert` ×2, `soirs` ×2, `demandeur` ×2, `avait`, `seul`, `charge`, `ensuite` | `il`, `des`, `enfants`, `ces`, `soirs-là`, `puis` | `{annexe:annA1_soirs_de_danse}` ×2, `{§ax4-soirs-de-danse..ax4-danse-deux-enfants}` | — |
| `ax4-garderie` | `le` ×3, `demandeur` ×3, `la`, `répartissaient`, `de` ×2, `garderie`, `tel`, `qu'il`, `appert` | `il` ×2, `avec`, `répartissait` | `{annexe:annA2_garderie}`, `{§ax4-garderie..ax4-soins-retour}` | — |
| `ax4-activites` | `le` ×2, `demandeur` ×2, `semaines`, `l'enfant`, `cours`, `tel`, `qu'il`, `appert`, `de` ×2, `d'autres`, `ne` | `il`, `ou`, `celui`, `n'en` | `{annexe:annA3_activites}`, `{§ax4-activites..ax4-enfant-sans-cours}` | — |
| `ax4-enfants-malades` | `le` ×3, `demandeur` ×3, `lorsqu'un`, `enfant`, `s'absentait` ×2, `du` ×2, `travail` ×2, `pour` ×2, `s'en`, `occuper`, `tel` ×2, `qu'il` ×2, `appert` ×2, `de` ×3, `lorsque`, `s'occuper`, `l'enfant` | `il`, `ou` ×2, `que` | `{annexe:annA4_enfants_malades}` ×2 | — |
| `ax4-sorties` | `le` ×2, `demandeur` ×2, `ses`, `enfants` | `il` ×2, `les` | — | — |
| `ax4-famille-paternelle` | `de` ×3, `la` ×2, `famille`, `paternelle` ×2, `enfants`, `tel` ×2, `qu'il` ×2, `appert` ×2, `le` ×3, `demandeur` ×3, `aux` ×3, `repas`, `fêtes`, `traditions` | `il`, `c'est`, `lui`, `qui` ×2, `cette`, `y` | `{annexe:annA6_famille_paternelle}` ×2, `{§ax4-famille-paternelle..ax4-deplacements-famille}` | — |
| `ax4-vie-quotidienne` | `le` ×4, `demandeur` ×4, `partageait` ×3, `avec` ×3, `la` ×3, `défenderesse` ×3, `élise` ×3, `ayoub` ×3, `des` ×3, `enfants` ×3, `tel` ×3, `qu'il` ×3, `appert` ×3, `de` ×3 | `il`, `et` | `{annexe:annA7_vie_quotidienne}` ×3, `{§ax4-vie-quotidienne..ax4-jeux}` | — |
| `ax4-cooperation` | `les`, `parties` ×2, `responsabilités` ×2, `tel` ×2, `qu'il` ×2, `appert` ×2, `des` ×5, `annexes` ×2, `a-1` ×2, `à` ×2, `a-4` ×2, `la`, `répartition` | `elles`, `et`, `cette`, `organisation` | `{§ax4-soirs-de-danse}`, `{§ax4-garderie}`, `{§ax4-enfants-malades}`, `{§ax4-cooperation..ax4-coordination-quotidienne}` | — |
| `ax4-participation` | `le` ×2, `demandeur` ×2, `la`, `défenderesse`, `élise`, `ayoub`, `des`, `responsabilités`, `parentales`, `qui`, `était` | `et`, `il`, `elle`, `en` | `{§ax4-garderie}`, `{§ax4-vie-quotidienne..ax4-cooperation-familiale}`, `{§ax4-danse-alexia..ax4-danse-deux-enfants}`, `{§ax4-famille-paternelle..ax4-lien-paternel}`, `{§p1-declarations}`, `{§ax4-participation..ax4-responsabilites-seul}`, `{§ax4-portrait}`, `{§ax4-partage-responsabilites..ax4-cooperation-familiale}` | — |
| `ax4-frictions` | `les`, `que`, `le`, `la` ×3, `répartition` ×2, `des` ×2, `responsabilités` ×2, `parentales` ×2, `requête`, `attribue`, `paragraphe`, `6`, `de`, `à` | `elle`, `et`, `ces` | `{§ax4-participation..ax4-responsabilites-seul}` | — |

## Contrôles dans la demande assemblée

| Bloc | Avant | Après | Scissions F / C / R / M | Paragraphes portant un renvoi de paragraphe |
|---|---:|---:|---|---|
| Partie I | 15 | 37 | 1 / 0 / 4 / 5 | 21 (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 18, 21, 22, 23, 28, 29, 30, 31, 32, 33) |
| Axe 4 | 12 | 39 | 2 / 0 / 0 / 9 | 12 (300, 303, 306, 315, 320, 323, 324, 325, 326, 327, 328, 329) |

À l’axe 4, 21 paragraphes citent une annexe, dont le § 323 qui porte également des renvois de paragraphe. Au total, 32 paragraphes de l’axe 4 portent l’une ou l’autre forme de renvoi. Les sept annexes conservent leur texte. Aucun intertitre ajouté.

Les 76 paragraphes du lot ont été relus dans le Markdown assemblé (§§ 1 à 37 et 293 à 331). Tous ont un verbe principal conjugué. Aucun ne commence par un connecteur. Au § 31, « Ce n’est donc pas le jeune âge des enfants […] qui favorise » est une construction présentative dont le terme figure dans la même phrase. Au § 322, « Chacune » a pour complément « des parties » dans la même phrase.

Le seul renvoi entrant de la branche source figure dans `par14_17_motif.md`, à `par14-renvoi-axe4`. L’intervalle `{§ax4-portrait..ax4-frictions}` conserve ses deux bornes et se lit « §§ 293 à 329 ». La règle 5 impose de le conserver tel quel, même après la scission de `ax4-frictions`. Aucun renvoi entrant ajusté.

Les 24 citations de la partie I et les 4 de l’axe 4 sont identiques à l’archive au caractère près, dans le même ordre, jusque dans le Markdown assemblé. Le contrôle ciblé reproduit le résultat de départ : 22 fragments `OK`, 1 `OK*` et aucun `NO`. Le `OK*` concerne le paragraphe 7 de la requête, retrouvé phrase par phrase. Le vérificateur ne compte que les fragments dépassant son seuil de longueur.

Les deux assemblages ont produit le Markdown et le Word avec 16 blocs et 522 paragraphes numérotés portant 522 étiquettes. La liste principale de chacun des deux fichiers Word comporte 522 paragraphes. L’assemblage complet inclut 9 annexes, la sortie `/tmp/lot2` contient les blocs seuls. Aucune `ERREUR` et aucune `ALERTE`. Les lignes `CITATION NO` sont identiques à celles de la branche source, soit 65 avec les annexes et 2 sans elles.
