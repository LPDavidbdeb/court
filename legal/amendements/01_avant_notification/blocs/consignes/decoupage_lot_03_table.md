# Découpage du lot 3 — Table de décision

Branche source `fiches/email-16-portee-retrait`, commit `57241f3`. La comparaison porte sur les neuf blocs de la [copie du 23 novembre 2026](../archive/2026-11-23_avant_decoupage). Chaque ancienne étiquette demeure sur la première partie issue de son paragraphe. Les numéros ci-dessous sont ceux de l’assemblage sans annexes.

## Résultats par bloc

F désigne un fait, C une citation, R un raisonnement et M un paragraphe mixte. Les scissions comptent les anciens paragraphes divisés. Les deux colonnes de renvois donnent les numéros des paragraphes porteurs, selon que le renvoi vise un paragraphe ou une annexe. Un paragraphe peut figurer dans les deux colonnes.

| Bloc | Avant | Après | Scissions F / C / R / M | Paragraphes avec un renvoi § | Paragraphes avec un renvoi à une annexe | Citations |
|---|---:|---:|---|---|---|---:|
| `p3_introduction` | 1 | 1 | 0 / 0 / 0 / 0 | 0 (—) | 0 (—) | 0 |
| `par07_duree_2011` | 9 | 21 | 4 / 0 / 0 / 4 | 3 (334, 344, 346) | 2 (329, 345) | 4 |
| `par07_role_de_pere` | 11 | 41 | 2 / 0 / 1 / 6 | 13 (350, 356, 367, 369, 373, 377, 381–387) | 9 (351, 356, 370–372, 374–376, 378) | 4 |
| `par10_rachat` | 12 | 29 | 2 / 0 / 1 / 5 | 6 (415, 427, 429, 431–433) | 0 (—) | 20 |
| `par14_17_motif` | 21 | 67 | 3 / 0 / 2 / 12 | 28 (436, 438, 445, 449–450, 454, 457, 459, 461, 470–473, 478–482, 486, 490, 492–498, 500) | 0 (—) | 27 |
| `par19_35_acces_autorite` | 23 | 83 | 4 / 0 / 3 / 10 | 30 (558–560, 574, 578, 580–582, 595, 597–601, 603, 607, 610–613, 617–619, 622, 624, 630–631, 635, 637–638) | 0 (—) | 42 |
| `par28_29_mediation` | 15 | 43 | 3 / 0 / 1 / 8 | 21 (642–645, 648, 656–657, 662, 666–667, 671–681) | 0 (—) | 16 |
| `par56_58_assurances` | 18 | 50 | 2 / 0 / 0 / 11 | 11 (683, 685, 692, 702, 714, 717, 724, 727, 729–731) | 0 (—) | 16 |
| `p4_portee` | 9 | 11 | 0 / 0 / 0 / 1 | 2 (737, 742) | 0 (—) | 0 |

## Décisions — `p3_introduction.md`

| Ancienne étiquette | Type | Scindé ? | Raison | Étiquettes après découpage, dans l’ordre |
|---|---|---|---|---|
| `p3-objet` | R | Non | Les deux phrases délimitent le même examen. La seconde précise pourquoi une même allégation peut y reparaître. | `p3-objet` |

## Décisions — `par07_duree_2011.md`

| Ancienne étiquette | Type | Scindé ? | Raison | Étiquettes après découpage, dans l’ordre |
|---|---|---|---|---|
| `par07-allegation` | C | Non | Une déclaration sous serment avec son attribution. | `par07-allegation` |
| `par07-these` | M | Oui | La concession garde sa limite sur la durée de la séparation. La durée de la thérapie et le renvoi relatif à la seconde phrase ont des objets distincts. | `par07-these`, `par07-duree-therapie`, `par07-seconde-phrase` |
| `par07-depart` | F | Oui | La demande de départ et la réaction du demandeur ont des auteurs distincts et la même source testimoniale. | `par07-depart`, `par07-contrition` |
| `par07-hydro` | F | Oui | Les comptes concernent deux logements. Chaque fait garde les sources communes. | `par07-hydro`, `par07-compte-familial` |
| `par07-fin` | M | Oui | La fin de la responsabilité ne fournit qu’une borne maximale. Le retour antérieur repose sur le témoignage. | `par07-fin`, `par07-retour-logement` |
| `par07-therapie` | F | Oui | La durée indicative et ses limites restent ensemble. Les factures de juin établissent une autre proposition. | `par07-therapie`, `par07-factures-juin` |
| `par07-retour` | F | Oui | Deux courriels de deux auteurs, puis une déclaration de la requête. Chaque citation garde sa source. | `par07-retour`, `par07-reponse-amie`, `par07-reprise-vie-commune` |
| `par07-connaissance` | M | Oui | Trois circonstances vécues précèdent la conclusion sur la connaissance. | `par07-connaissance`, `par07-cliente-juin`, `par07-retour-famille`, `par07-duree-vecue` |
| `par07-conclusion` | M | Oui | Les visites à Alexia se distinguent de la comparaison des deux durées. Les trois annexes désignées restent les mêmes. | `par07-conclusion`, `par07-durees-comparees` |

## Décisions — `par07_role_de_pere.md`

| Ancienne étiquette | Type | Scindé ? | Raison | Étiquettes après découpage, dans l’ordre |
|---|---|---|---|---|
| `par07r-allegation` | C | Non | Le passage de la requête garde son attribution. | `par07r-allegation` |
| `par07r-attribution` | F | Oui | L’absence d’auteur, l’absence de pièce et la nature de la démarche de couple se vérifient séparément. | `par07r-attribution`, `par07r-piece`, `par07r-demarche` |
| `par07r-fait` | M | Oui | L’exercice du rôle pendant la période documentée précède la limite temporelle du constat. | `par07r-fait`, `par07r-moment-constat` |
| `par07r-definition` | M | Oui | La définition, la règle citée, le contenu de la requête et les composantes retenues ont des objets distincts. | `par07r-definition`, `par07r-code-civil`, `par07r-dimension`, `par07r-composantes` |
| `par07r-conge` | F | Oui | L’écart admis, les catégories de congé, la décision des parents, les semaines prises par le père et les disponibilités des parents se distinguent. | `par07r-conge`, `par07r-conges-naissance`, `par07r-semaines-mere`, `par07r-semaines-pere`, `par07r-disponibilites` |
| `par07r-pendant-conge` | M | Oui | Les courriels, le témoignage et les photographies sont distincts. Le constat sur le congé renvoie aux pièces de cette période. | `par07r-pendant-conge`, `par07r-natation-mai`, `par07r-ymca`, `par07r-participation-natation`, `par07r-photo-piscine`, `par07r-presence-conge` |
| `par07r-fin-conge` | M | Oui | L’annonce du mercredi se distingue de la portée du partage du congé parental. | `par07r-fin-conge`, `par07r-portee-ecart` |
| `par07r-therapie` | M | Oui | Les périodes et les composantes diffèrent. Le décompte des adaptations du travail garde ses quatre catégories. Le constat de fréquence suit les faits. | `par07r-therapie`, `par07r-sorties-cours`, `par07r-accessibilite-separation`, `par07r-accessibilite-retour`, `par07r-responsabilite`, `par07r-garderie`, `par07r-liens`, `par07r-frequence` |
| `par07r-volume` | F | Non | Le nombre d’événements nommant Alexia précise la population du même relevé. Les deux dénominateurs restent lisibles ensemble. | `par07r-volume` |
| `par07r-connaissance` | M | Oui | Les cours de danse, la photographie et la thérapie sont trois circonstances personnelles distinctes. | `par07r-connaissance`, `par07r-photo-table`, `par07r-factures`, `par07r-vie-commune` |
| `par07r-conclusion` | R | Oui | Attribution du constat, omission, exercice du rôle, portée du congé et place du constat dans la thèse générale sont distincts. | `par07r-conclusion`, `par07r-faits-omis`, `par07r-exercice-role`, `par07r-ecart-conge`, `par07r-these-generale` |

## Décisions — `par10_rachat.md`

| Ancienne étiquette | Type | Scindé ? | Raison | Étiquettes après découpage, dans l’ordre |
|---|---|---|---|---|
| `par10-allegation` | C | Non | Le rachat et sa cause alléguée appartiennent à une seule déclaration citée. | `par10-allegation` |
| `par10-these` | M | Oui | Le rachat admis garde sa limite. Le plan, le courriel à l’avocate et le partage sont distincts. L’aboutissement et l’absence de pièce sur les réparations ont chacun leur portée. | `par10-these`, `par10-charge`, `par10-menace`, `par10-partage`, `par10-aboutissement`, `par10-demande-reparation` |
| `par10-plan` | C | Non | Quatre extraits du plan gardent leur attribution commune. | `par10-plan` |
| `par10-allegations-2013` | M | Oui | Les extraits du courriel gardent leur lien avec la restriction. Leur sort documentaire se distingue de l’absence de plainte rapportée par le demandeur. | `par10-allegations-2013`, `par10-sort-allegations`, `par10-plainte` |
| `par10-pringle` | C | Non | Une déclaration au destinataire nommé. | `par10-pringle` |
| `par10-vendre` | C | Non | Deux extraits du même courriel au supérieur. | `par10-vendre` |
| `par10-evaluation` | F | Oui | Le mandat et le rapport ont des dates différentes. La désignation de la propriété et la finalité de l’évaluation restent dans le même rapport. | `par10-evaluation`, `par10-rapport` |
| `par10-copies` | M | Oui | L’annonce des deux copies est distincte du témoignage sur la seconde. La limite du courriel accompagne ce témoignage. | `par10-copies`, `par10-seconde-copie` |
| `par10-sous-sol` | M | Oui | La portée du corpus, le courriel et la lecture du choix d’affectation sont distincts. | `par10-sous-sol`, `par10-courriel-sous-sol`, `par10-indemnite` |
| `par10-absence` | F | Oui | Le contenu de la requête et l’absence de demande ou de refus dans les pièces couvrent deux corpus. | `par10-absence`, `par10-pieces-reparations` |
| `par10-connaissance` | M | Oui | La réception du plan, la qualité de copropriétaire, la réception du rapport et le rachat précèdent la conclusion de connaissance. La réception garde son attribution au témoignage. | `par10-connaissance`, `par10-copropriete`, `par10-reception`, `par10-rachat-aout`, `par10-connaissance-partage` |
| `par10-conclusion` | R | Oui | La cause alléguée et le motif omis donnent deux conclusions. La première conserve le rachat admis. | `par10-conclusion`, `par10-cause-omise` |

## Décisions — `par14_17_motif.md`

| Ancienne étiquette | Type | Scindé ? | Raison | Étiquettes après découpage, dans l’ordre |
|---|---|---|---|---|
| `par14-allegations` | C | Non | Une suite de paragraphes du même acte conserve ses numéros et son attribution. | `par14-allegations` |
| `par14-changement-motif` | M | Oui | La routine, sa prévision et le fondement historique sont distincts. La comparaison suit les motifs. La délimitation de la section reste liée à celle de l’axe 4. | `par14-changement-motif`, `par14-prevision-juin`, `par14-raison-novembre`, `par14-difference-motifs`, `par14-objet-section` |
| `par14-offre-avril` | F | Oui | L’offre, la réponse qui atteste son envoi et le libellé du modèle se rattachent à des actes précis. | `par14-offre-avril`, `par14-reponse-avril`, `par14-modele` |
| `par14-transition` | M | Oui | Les modalités absentes de la lettre, l’interprétation du paragraphe 14 et la comparaison avec la proposition ultérieure se distinguent. | `par14-transition`, `par14-immediatete`, `par14-mise-en-oeuvre` |
| `par14-refus-routine` | C | Non | Le refus et ses motifs sont cités avec l’autrice, la date et la fiche. | `par14-refus-routine` |
| `par14-routine-conjoncture` | M | Oui | La description du régime et le silence sur la répartition antérieure précèdent la conclusion sur le motif. | `par14-routine-conjoncture`, `par14-soins-anterieurs`, `par14-motif-conjoncturel` |
| `par14-plan-2013` | M | Oui | Les trois extraits d’un même courriel restent groupés. La prévision du motif est une conclusion sur leur portée. | `par14-plan-2013`, `par14-motif-prevu` |
| `par14-fonction-routine` | M | Oui | L’absence de procédure et le départ sont vérifiables séparément. Leur portée pour la routine vient ensuite. | `par14-fonction-routine`, `par14-depart`, `par14-fonction-avril` |
| `par14-protection` | M | Oui | Les passages du plan gardent leur attribution. La conséquence conditionnelle et la fonction du précédent sont deux conclusions. | `par14-protection`, `par14-exposition`, `par14-fonction-precedent` |
| `par14-connaissance-objectif` | M | Oui | La connaissance tient à la destination du plan. Les deux courriels de septembre précèdent la conclusion sur la poursuite de l’objectif. | `par14-connaissance-objectif`, `par14-objectif-septembre`, `par14-accusations-septembre`, `par14-objectif-poursuivi` |
| `par14-projet-aout` | F | Oui | Le projet garde la réserve sur la signature. La garde, la progression et le calendrier initial ont des objets distincts. | `par14-projet-aout`, `par14-garde-projet`, `par14-phases`, `par14-premiere-phase` |
| `par14-proposition-septembre` | M | Oui | La citation conserve l’ensemble de l’offre. Les modalités de la transition et la date de son aboutissement sont examinées séparément. | `par14-proposition-septembre`, `par14-amenagement`, `par14-terme` |
| `par14-refus-septembre` | C | Non | Une réponse citée avec sa date, son autrice et sa fiche. | `par14-refus-septembre` |
| `par14-constat-refus` | M | Oui | Le constat sur la demande du père, l’objet du refus, la portée de l’âge et de la stabilité et l’offre antérieure sont séparément discutables. L’annonce du nombre de sous-items est devenue sans objet. | `par14-constat-refus`, `par14-objet-refus`, `par14-offre-elargissement`, `par14-limite-motifs` |
| `par14-raison-requete` | M | Oui | L’absence de routine, la raison tirée des soins et l’affirmation du paragraphe 25 se distinguent. | `par14-raison-requete`, `par14-repartition-soins`, `par14-milieu-stable` |
| `par14-acces-hebdomadaires` | C | Non | La conclusion de la requête est citée avec le paragraphe qui la porte. | `par14-acces-hebdomadaires` |
| `par14-requalification` | R | Oui | Le caractère conjoncturel, le caractère structurel, la comparaison, la continuité alléguée et l’effacement de l’origine ont chacun leur portée. | `par14-requalification`, `par14-motif-structurel`, `par14-nature-motif`, `par14-continuite`, `par14-origine-routine` |
| `par14-absence-explication` | M | Oui | Les deux lettres de 2015 et le plan de 2013 sont des documents distincts. Le constat sur les écrits de 2015 vient ensuite. | `par14-absence-explication`, `par14-lettre-septembre`, `par14-disponibilite-mere`, `par14-ecrits-2015` |
| `par14-demande-retrait` | M | Oui | Trois écrits avec leurs sources précèdent l’appréciation du grief, sa portée et la conclusion sur la position de l’autrice. | `par14-demande-retrait`, `par14-seuil-septembre`, `par14-cours-natation`, `par14-reproche`, `par14-portee-reproche`, `par14-raison-autrice` |
| `par14-conclusion` | R | Oui | Absence, substitution, contradiction factuelle, désaveu, portée de la perception et raison reçue sous serment sont des conclusions distinctes. | `par14-conclusion`, `par14-substitution`, `par14-contradiction`, `par14-dementi`, `par14-perception`, `par14-raison-sous-serment` |
| `par14-renvoi-axe4` | F | Oui | Deux renvois de lecture portent sur des groupes de paragraphes différents. | `par14-renvoi-axe4`, `par14-faits-axe4` |

## Décisions — `par19_35_acces_autorite.md`

| Ancienne étiquette | Type | Scindé ? | Raison | Étiquettes après découpage, dans l’ordre |
|---|---|---|---|---|
| `par19-allegations` | C | Non | Les passages de la même requête gardent leur attribution, leurs numéros et la cote P-5 au sous-item h). | `par19-allegations` |
| `par19-these` | R | Oui | La concession garde sa limite. Le contexte omis et les deux inexactitudes alléguées sont distincts. | `par19-these`, `par19-contexte`, `par19-inexactitude-acces`, `par19-inexactitude-preference` |
| `par19-depart` | F | Oui | La rupture et les échanges des 2, 3 et 13 février se distinguent. L’offre de crédit et son refus ont des auteurs distincts. Les échanges sur la maladie et la journée familiale gardent chacun leur question et leur réponse. | `par19-depart`, `par19-necessaire`, `par19-credit`, `par19-reponse-credit`, `par19-maladie`, `par19-journee-famille` |
| `par19-offre-partage` | F | Oui | La lettre d’offre et les accès décrits au paragraphe 20 se rattachent à deux sources. | `par19-offre-partage`, `par19-dimanches` |
| `par19-refus-routine` | M | Oui | La réponse, le silence de la lettre sur les circonstances et celui des écrits ultérieurs se vérifient séparément. | `par19-refus-routine`, `par19-circonstances-lettre`, `par19-ecrits-posterieurs` |
| `par19-circonstances-2013` | M | Oui | Les motifs écrits, l’offre de nuitées, le courriel cité, le sort des allégations, le témoignage, le silence de la requête et la comparaison limitée aux nuitées se distinguent. | `par19-circonstances-2013`, `par19-nuitees-avril`, `par19-danger-nomme`, `par19-sort-allegations`, `par19-plainte`, `par19-requete-2015`, `par19-regime-sans-nuitee` |
| `par19-offre-nuitees` | C | Non | Les deux périodes de nuitées appartiennent à la même offre. La date explicite identifie la lettre. | `par19-offre-nuitees` |
| `par19-contradiction-routine` | R | Oui | Le rapprochement de deux positions et les deux branches conditionnelles de son appréciation se distinguent. | `par19-contradiction-routine`, `par19-maintien-circonstances`, `par19-changement-circonstances` |
| `par19-plan-routine` | C | Non | Un extrait du mécanisme exposé dans le courriel, avec son autrice, sa date et sa source. | `par19-plan-routine` |
| `par19-conduite-demandeur` | R | Non | Le motif opposé au demandeur explique la conduite qu’il rapporte. La justification reste avec cette conduite. | `par19-conduite-demandeur` |
| `par19-projet-aout` | F | Oui | L’envoi, le régime de nuitées et la clause sur les décisions sont distincts. | `par19-projet-aout`, `par19-progression`, `par19-decisions` |
| `par19-reponse-septembre` | C | Non | Trois passages de la même réponse restent sous leur attribution et leurs sous-items. | `par19-reponse-septembre` |
| `par19-refus-septembre` | C | Non | Les deux passages de la lettre restent groupés. La précision au sous-item a) qualifie le motif donné dans ce passage. | `par19-refus-septembre` |
| `par19-jugement` | F | Oui | La demande de novembre et les deux décisions du tribunal en janvier se distinguent par leur date ou leur objet. | `par19-jugement`, `par19-horaire-jugement`, `par19-pension-jugement` |
| `par19-omission-progressivite` | M | Oui | Intertitre. La progression alléguée et la conclusion demandée sont les deux prémisses de la comparaison. | `par19-omission-progressivite`, `par19-demande-hebdomadaire`, `par19-augmentation` |
| `par19-omission-routine` | M | Oui | Intertitre. L’origine des accès, le motif de leur maintien et la demande de reconduction précèdent le constat d’omission. | `par19-omission-routine`, `par19-maintien`, `par19-reconduction`, `par19-silence-maintien` |
| `par19-omission-offres` | M | Oui | Intertitre. La concession sur les offres garde la raison de leur refus. La réponse omise, la position au serment et le refus du terme se distinguent. | `par19-omission-offres`, `par19-reponse-omise`, `par19-position-novembre`, `par19-terme-refuse` |
| `par19-presence-tiers` | M | Oui | Intertitre. Les dimanches, les restrictions vécues, les écrits de juin et la conduite de chaque partie ont des dates, des sources ou des acteurs différents. | `par19-presence-tiers`, `par19-tiers-separation`, `par19-restrictions-vie-commune`, `par19-continuite-cadre`, `par19-refus-chalet`, `par19-echange-chalet`, `par19-courriel-soeur`, `par19-cadre-reconduit`, `par19-raison-non-donnee`, `par19-cadre-maintenu` |
| `par19-autorite` | M | Oui | Intertitre. Les messages produits sous P-5, le baptême, la marraine et les deux positions écrites précèdent la comparaison au jour du serment. | `par19-autorite`, `par19-bapteme`, `par19-marraine`, `par19-position-decisions`, `par19-reponse-decisions`, `par19-preference-novembre` |
| `par19-espacement` | M | Oui | Intertitre. L’absence de pièce, l’attribution au père, le régime maintenu, la fréquence et l’antériorité donnent des propositions distinctes. | `par19-espacement`, `par19-relation`, `par19-espacement-regime`, `par19-frequences`, `par19-anteriorite-position` |
| `par19-connaissance` | M | Oui | Les cinq circonstances de connaissance ont des sources et des dates différentes. La conclusion reste datée du serment. | `par19-connaissance`, `par19-demande-requete`, `par19-decision-bapteme`, `par19-information-cliente`, `par19-messages-joints`, `par19-elements-connus` |
| `par19-requalification` | M | Oui | La provenance commune, l’effet des omissions, le motif d’avril et le motif substitué dans la requête sont distincts. | `par19-requalification`, `par19-interpretation`, `par19-motif-avril`, `par19-motif-requete` |
| `par19-conclusion` | R | Oui | L’ampleur de la restriction, la justification qu’elle appelle, le portrait fourni et le contexte connu forment quatre propositions. | `par19-conclusion`, `par19-justification`, `par19-portrait`, `par19-contexte-connu` |

## Décisions — `par28_29_mediation.md`

| Ancienne étiquette | Type | Scindé ? | Raison | Étiquettes après découpage, dans l’ordre |
|---|---|---|---|---|
| `par28-allegations` | C | Non | Deux extraits d’une requête sous une attribution commune. La cote P-4 appartient au second extrait. | `par28-allegations` |
| `par28-these` | M | Oui | La présentation aux paragraphes 28 et 29 précède l’identification de l’intervention. Sa nature, la chronologie du refus et son objet se discutent séparément. | `par28-these`, `par28-identification`, `par28-intervention-unique`, `par28-mediation`, `par28-refus-initial`, `par28-objet-refus` |
| `par28-offre-ecrement` | C | Non | La qualité de la psychologue et la relation préalable restent avec ses propos. Les trois extraits du courriel et leurs sous-items restent ensemble. | `par28-offre-ecrement` |
| `par28-nature` | M | Oui | La forme individuelle et l’exclusion de la médiation par la professionnelle sont distinctes. | `par28-nature`, `par28-exclusion` |
| `par28-origine-offre` | M | Oui | L’offre est citée avec son autrice. La limite sur ce que dit ce courriel est distincte et reste circonscrite à la source. | `par28-origine-offre`, `par28-offre-defenderesse` |
| `par28-acceptation` | F | Oui | L’acceptation, la fixation du rendez-vous et l’indication des frais se distinguent par leur objet et leur auteur. | `par28-acceptation`, `par28-rendez-vous`, `par28-tarif` |
| `par28-annulation` | F | Oui | L’annulation et la réponse sur les services aux enfants sont deux messages. La question reste avec sa réponse. | `par28-annulation`, `par28-services` |
| `par28-portee-refus` | R | Oui | La succession des deux actes et l’objet du refus se distinguent. Le refus limité à la garde garde son pendant sur les services. | `par28-portee-refus`, `par28-limite-refus` |
| `par28-p4` | C | Non | La communication à la défenderesse forme un seul fait avec l’extrait de la pièce P-4. La date identifie le message. | `par28-p4` |
| `par28-p4-contenu` | F | Oui | Le silence et le contenu affirmatif de la pièce, puis l’absence de pièce au paragraphe 28, se vérifient séparément. | `par28-p4-contenu`, `par28-contenu-refus`, `par28-absence-piece` |
| `par28-connaissance-propre` | M | Oui | La rencontre vécue par la défenderesse et la connaissance qu’elle en tirait se distinguent. | `par28-connaissance-propre`, `par28-nature-connue` |
| `par28-email-190` | M | Oui | Le courriel, l’absence d’autre proposition au dossier et les deux emplois successifs de la qualification se distinguent. | `par28-email-190`, `par28-autre-proposition`, `par28-qualification`, `par28-reprise-serment` |
| `par28-accumulation` | M | Oui | La concession sur le paragraphe 29 reste entière. Les deux éléments de la séquence précèdent la conclusion sur son effet. | `par28-accumulation`, `par28-categorie`, `par28-repetition`, `par28-effet` |
| `par28-mot-mediation` | M | Oui | La portée du mot, l’identité de l’autrice de l’offre, la conduite du demandeur et les deux effets du passage assermenté se distinguent. La citation de la psychologue garde son attribution. | `par28-mot-mediation`, `par28-offre-psychologue`, `par28-conduite`, `par28-transformation`, `par28-cooperation` |
| `par28-conclusion` | M | Oui | L’annulation garde l’accord sur les services. L’origine de l’offre, la conclusion limitée aux échanges et les deux sources de connaissance se distinguent. | `par28-conclusion`, `par28-absence-mediation`, `par28-autrice`, `par28-experience`, `par28-connaissance-refus` |

## Décisions — `par56_58_assurances.md`

| Ancienne étiquette | Type | Scindé ? | Raison | Étiquettes après découpage, dans l’ordre |
|---|---|---|---|---|
| `par56-allegations` | C | Non | Trois passages du même acte sous leur attribution commune. | `par56-allegations` |
| `par56-contestation` | M | Oui | La couverture admise garde la limite de la contestation. Le constat sur les pièces produites et celui sur la connaissance sont distincts. | `par56-contestation`, `par56-absence-piece`, `par56-connaissance-contestation` |
| `par56-acces-dimanche` | C | Non | Le libellé du régime d’accès garde la citation qui l’établit. | `par56-acces-dimanche` |
| `par56-depenses-mere` | C | Non | Deux passages d’une même requête sont cités avec leurs paragraphes et un sujet explicite. | `par56-depenses-mere` |
| `par56-prestations` | F | Oui | Les deux modes de paiement se distinguent. Les dates de même nature demeurent groupées dans chaque catégorie. | `par56-prestations`, `par56-sept-prestations`, `par56-trois-depenses` |
| `par56-aucun-dimanche` | M | Oui | Le jour des prestations relève du relevé. La présence des enfants dépend du régime allégué dans la requête. | `par56-aucun-dimanche`, `par56-regime-allegue` |
| `par56-paiements-directs` | F | Non | Le paiement au fournisseur et le solde décrivent le mécanisme d’un même paiement. Le groupe de sept est précisé. | `par56-paiements-directs` |
| `par56-derniere-prestation` | F | Non | La date, les montants et le solde identifient et décomposent une même prestation. Le nom de la prestation rend le paragraphe autonome. | `par56-derniere-prestation` |
| `par56-refus-utilisation` | M | Oui | L’allégation citée, la présence alléguée au point de service, les paiements, le mécanisme d’autorisation et l’état du dossier se vérifient séparément. | `par56-refus-utilisation`, `par56-point-service`, `par56-paiements`, `par56-autorisation`, `par56-refus-documente` |
| `par56-exclusivite` | M | Oui | L’exclusivité alléguée, les bénéficiaires et le rapprochement avec le dimanche ont des objets distincts. | `par56-exclusivite`, `par56-beneficiaires`, `par56-jour-acces` |
| `par56-refus-solde` | M | Oui | L’affirmation citée, le présupposé d’une demande, le texte de la requête et la période couverte par le dossier se distinguent. | `par56-refus-solde`, `par56-demande-prealable`, `par56-demande-citee`, `par56-demandes-documentees` |
| `par56-depenses-juillet` | M | Oui | Les montants décrivent un même remboursement. La correspondance de tarif garde sa source et se distingue du message d’août produit sous P-5. | `par56-depenses-juillet`, `par56-tarif`, `par56-lettre-psychologue` |
| `par56-remboursements` | M | Oui | La portée du paragraphe 57 et l’absence de demande documentée avant le serment sont distinctes. | `par56-remboursements`, `par56-demande-remise` |
| `par56-connaissance` | M | Oui | Les allégations de la défenderesse, les paiements vécus et le message qu’elle produit sous P-5 précèdent la conclusion sur sa connaissance personnelle. | `par56-connaissance`, `par56-achats`, `par56-soldes`, `par56-solde-recent`, `par56-message-aout`, `par56-vecu-serment` |
| `par56-presentation` | F | Oui | La date de présentation, la présence de chaque partie, la preuve mentionnée et les ordonnances ont des objets distincts. La citation reste celle du tribunal. | `par56-presentation`, `par56-presence`, `par56-absence`, `par56-preuve`, `par56-ordonnances` |
| `par56-prestation-janvier` | M | Oui | La prestation conserve son décompte. L’inférence sur le lundi et le rang parmi les prestations entre serment et audience se distinguent. | `par56-prestation-janvier`, `par56-lundi`, `par56-deuxieme-prestation` |
| `par56-contradiction-audience` | M | Oui | Une déclaration au présent et sa confrontation à la prestation précédant l’audience sont distinctes. | `par56-contradiction-audience`, `par56-utilisation-audience` |
| `par56-conclusion` | M | Oui | L’admission reste avec sa limite. Le serment est confronté aux prestations antérieures, la présentation à une prestation ultérieure. Le fondement du paragraphe 58 est distinct. | `par56-conclusion`, `par56-refus-serment`, `par56-presentation-prestation`, `par56-saisine` |

## Décisions — `p4_portee.md`

| Ancienne étiquette | Type | Scindé ? | Raison | Étiquettes après découpage, dans l’ordre |
|---|---|---|---|---|
| `p4-parties-i-ii` | R | Non | Une seule confrontation. La séparation, le refus et l’entente précisent les fonctions attribuées au même portrait. | `p4-parties-i-ii` |
| `p4-partie-iii` | F | Non | La liste délimite le champ d’examen de la partie III. Ses éléments sont les objets d’une même énumération. | `p4-partie-iii` |
| `p4-fait-omis` | F | Non | Le fait omis et la pièce qui l’établit forment une unité. | `p4-fait-omis` |
| `p4-connaissance` | F | Non | La date du serment borne exactement la connaissance examinée. | `p4-connaissance` |
| `p4-audience` | F | Non | La date de présentation et la réserve sur les pièces qualifient le même examen. | `p4-audience` |
| `p4-allegations` | F | Non | Les allégations restent avec leur source, leur destinataire, leur sort et la restriction à laquelle elles se rapportent. | `p4-allegations` |
| `p4-pas-la-garde` | R | Non | Une seule limite à l’objet de la section. | `p4-pas-la-garde` |
| `p4-objet` | R | Non | « Ainsi » rattache l’exposition des restrictions à la manière de montrer le contexte omis. Le paragraphe conserve cette relation. Le sujet est explicité. | `p4-objet` |
| `p4-me-ayoub` | M | Oui | La rédaction de la requête et la représentation devant le tribunal sont deux actes différents. La limite d’attribution des écrits est une troisième proposition sur la portée de la section. | `p4-me-ayoub`, `p4-representation`, `p4-ecrits` |

## Relevé mot à mot

Pour chaque ancien paragraphe, la comparaison porte sur toutes ses parties réunies et comprend la mention devenue intertitre. Les colonnes donnent les occurrences ajoutées et retirées après compensation des mots identiques dans ce même paragraphe. Les citations ont été comparées séparément au caractère près et dans l’ordre. Les chemins de fiches comptent chacun pour un mot. Les étiquettes, les repères de liste, la ponctuation, la casse et la forme de l’apostrophe sont exclus du décompte. Les renvois, y compris aux annexes, sont comptés dans leurs propres colonnes. Une ancienne étiquette absente du relevé n’a aucun écart suivant cette comparaison.

Le seul écart antérieur au lot entre les neuf blocs sources et leurs archives se trouve à `par14-constat-refus`. La branche source portait déjà `{§ax1-offre-avril..ax1-offre-dans-bornes}` à la place de `{§ax1-offre-avril}`. Le relevé le montre parce que son point de comparaison est l’archive.

### p3_introduction

Aucun mot ni renvoi ajouté ou retiré.

### par07_duree_2011

| Ancienne étiquette | Mots ajoutés | Mots retirés | Renvois ajoutés | Renvois retirés |
|---|---|---|---|---|
| `par07-these` | `le`, `demandeur`, `la`, `de`, `séparation`, `du` | `est`, `qui`, `son`, `l'annexe`, `lui`, `consacrée` | `{annexe:ann07_role_de_pere}` | — |
| `par07-depart` | `départ`, `du`, `demandeur`, `témoignage`, `s'est`, `au` | `s'y`, `est` | — | — |
| `par07-hydro` | `d'hydro-québec`, `le`, `demandeur`, `du` ×3, `au`, `1er`, `février`, `29`, `mai`, `2011`, `captures`, `portail`, `client`, `et` ×2, `clavardage`, `avec`, `un`, `agent`, `photodocuments`, `id` ×2, `1`, `2`, `legal/allegation_62_separation_2011.md` | `pendant`, `la`, `même`, `période`, `il` | — | — |
| `par07-fin` | `les`, `d'hydro-québec`, `distinct`, `le` | `ces`, `ce` | `{§par07-hydro}` | — |
| `par07-therapie` | `les`, `factures` | `celles` | — | — |
| `par07-retour` | `le`, `12`, `septembre`, `2011`, `demandeur`, `au`, `l'amie` | `elle`, `lui` | — | — |
| `par07-connaissance` | `la` ×5, `défenderesse` ×3, `élise` ×3, `ayoub` ×3, `de` ×2, `séparation`, `2011` | `cette`, `elle` ×3 | `{§par07-connaissance..par07-retour-famille}` | — |
| `par07-conclusion` | `les`, `de` ×2, `la`, `séparation`, `2011` | `ces`, `annexes`, `a-1`, `a-4`, `a-7` | `{annexe:annA1_soirs_de_danse}`, `{annexe:annA4_enfants_malades}`, `{annexe:annA7_vie_quotidienne}`, `{§par07-fin..par07-factures-juin}` | — |

### par07_role_de_pere

| Ancienne étiquette | Mots ajoutés | Mots retirés | Renvois ajoutés | Renvois retirés |
|---|---|---|---|---|
| `par07r-attribution` | `seconde`, `du` ×2, `paragraphe`, `7`, `le`, `constat`, `au` | `ce`, `à`, `et`, `son` | `{§par07-therapie..par07-factures-juin}` | `{§par07-therapie}` |
| `par07r-fait` | — | `or` | — | — |
| `par07r-definition` | `le`, `parental`, `dans`, `s'apprécie` | `l'annexe`, `apprécie`, `ce` | `{annexe:ann07_role_de_pere}`, `{§par07r-definition..par07r-dimension}` | — |
| `par07r-conge` | `congé`, `de`, `la`, `parental`, `les`, `défenderesse`, `32`, `semaines`, `du` | `cette`, `période` | — | — |
| `par07r-pendant-conge` | `le` ×3, `alexia` ×2, `demandeur` ×4, `la`, `au`, `du`, `cours`, `de` ×3, `natation`, `ymca`, `rue`, `stanley`, `témoignage`, `premier`, `maternité` | `même`, `ce`, `elle` ×2, `et`, `il`, `c'est`, `lui`, `y`, `qui`, `endroit` | `{§par07r-pendant-conge..par07r-natation-mai}` | — |
| `par07r-fin-conge` | — | — | `{§par07r-conge}`, `{§par07r-semaines-mere..par07r-disponibilites}` | — |
| `par07r-therapie` | `pendant` ×4, `la` ×5, `thérapie` ×4, `l'engagement`, `du` ×7, `demandeur` ×7, `est` ×5, `documenté` ×2, `par` ×5, `d'alexia` ×2, `ensuite`, `l'accessibilité`, `documentée` ×3, `sa`, `responsabilité` ×2, `pour` ×2, `documente` ×2 | `puis` ×2, `et` | `{annexe:ann07_role_de_pere}` ×6, `{§par07-retour..par07-reprise-vie-commune}`, `{§par07r-therapie..par07r-liens}` | `{§par07-retour}` |
| `par07r-connaissance` | `les`, `de`, `la` ×6, `défenderesse` ×3, `élise` ×3, `ayoub` ×3, `routine`, `d'alexia`, `thérapie`, `photographie`, `et`, `des` | `ces`, `ceux`, `ses`, `elle` ×2 | `{§par07-therapie..par07-factures-juin}`, `{§par07r-connaissance..par07r-factures}` | `{§par07-therapie}` |
| `par07r-conclusion` | `le` ×2, `paragraphe` ×2, `7` ×2, `constat`, `du` | `et`, `ce` | `{§par07r-attribution}`, `{§par07r-connaissance..par07r-vie-commune}`, `{§par07r-fait}`, `{§par07r-therapie..par07r-frequence}`, `{§par07r-conge..par07r-disponibilites}`, `{§ax4-portrait}`, `{§ax4-termes-contestes..ax4-portrait-vie-commune}` | — |

### par10_rachat

| Ancienne étiquette | Mots ajoutés | Mots retirés | Renvois ajoutés | Renvois retirés |
|---|---|---|---|---|
| `par10-these` | `le` ×3, `sa`, `du` ×2, `juin` ×3, `2013` ×2, `de` ×2, `me`, `marie-josée`, `ayoub` ×2, `à`, `sœur`, `élise`, `la` ×2, `résidence`, `demandeur`, `legal/piece_pdf-1.md`, `26` ×2, `legal/piece_thread-89_email-365.md`, `27`, `partage`, `dont`, `fait`, `état`, `dans`, `son`, `courriel` | `en`, `cette` | — | — |
| `par10-allegations-2013` | `courriel`, `du` ×3, `11` ×2, `juin` ×2, `2013` ×2, `de`, `me`, `marie-josée`, `ayoub` ×2, `à`, `sa`, `sœur`, `élise`, `legal/piece_pdf-1.md`, `les` | `même`, `ces` | `{§par19-circonstances-2013..par19-regime-sans-nuitee}` | `{§par19-circonstances-2013}` |
| `par10-evaluation` | `le`, `27`, `juin`, `2013`, `demandeur`, `legal/piece_pdf-11.md` | `même`, `jour`, `il` | — | — |
| `par10-copies` | `16`, `juillet`, `2013`, `du` | — | — | — |
| `par10-sous-sol` | `19`, `juillet`, `2013`, `du` | — | — | — |
| `par10-connaissance` | `la` ×4, `défenderesse` ×4, `élise` ×4, `ayoub` ×4, `du`, `témoignage`, `demandeur` | `et`, `elle` ×4 | `{§par10-copies..par10-seconde-copie}`, `{§par10-connaissance..par10-rachat-aout}` | `{§par10-copies}` |
| `par10-conclusion` | `le`, `paragraphe`, `10`, `cause`, `la` | `il`, `celle` | `{§par10-absence..par10-pieces-reparations}`, `{§par10-charge..par10-partage}`, `{§par10-connaissance-partage}` | — |

### par14_17_motif

| Ancienne étiquette | Mots ajoutés | Mots retirés | Renvois ajoutés | Renvois retirés |
|---|---|---|---|---|
| `par14-changement-motif` | `le`, `maintien` ×2, `routine` ×2, `de` ×2, `la` ×2, `du`, `au` | `et`, `ce`, `lui` | `{§ax1-routine-judiciaire}`, `{§par14-changement-motif..par14-raison-novembre}` | — |
| `par14-offre-avril` | `de`, `par`, `du`, `me` ×3, `françois` ×2, `poirier` ×2, `à`, `marie-josée`, `ayoub`, `envoi`, `20`, `avril`, `attesté`, `legal/piece_pdf-3.md` | `celle-ci`, `y` | — | — |
| `par14-transition` | `de`, `me`, `françois`, `poirier`, `mise`, `en`, `œuvre`, `une`, `qu'il`, `immédiate`, `n'exigeait`, `pas` | `le`, `contraire` | — | — |
| `par14-routine-conjoncture` | `la`, `du` ×2, `2015`, `de`, `lettre`, `27`, `avril`, `refus` | — | `{§par14-refus-routine..par14-soins-anterieurs}` | — |
| `par14-plan-2013` | `le`, `la`, `routine`, `de`, `du`, `maintien` | `ce` | — | — |
| `par14-fonction-routine` | `la`, `procédure`, `d'urgence`, `l'objet`, `de` | `son`, `objet` | `{§par14-plan-2013}`, `{§par14-refus-routine}` | — |
| `par14-protection` | `le` ×3, `plan` ×3, `du`, `11`, `juin`, `2013`, `de`, `me`, `ayoub`, `à`, `sa`, `sœur`, `que`, `par`, `legal/piece_pdf-1.md`, `visé` | `ce`, `même`, `écrit`, `qu'il` | `{§par14-plan-2013}`, `{§par14-protection..par14-exposition}` | — |
| `par14-connaissance-objectif` | `la` ×3, `défenderesse` ×3, `élise` ×3, `ayoub` ×3, `le`, `plan`, `du` ×3, `11` ×2, `juin` ×2, `2013` ×2, `16`, `septembre`, `2016` | `ce`, `elle` ×3, `en`, `même`, `jour` | `{§par14-connaissance-objectif..par14-accusations-septembre}` | — |
| `par14-projet-aout` | `le` ×2, `13` ×3, `août` ×3, `2015` ×3, `projet` ×2, `de` ×3, `consentement` ×3, `legal/piece_pdf-5.md` ×3, `du` ×3 | `qui`, `et` | — | — |
| `par14-proposition-septembre` | `la` ×2, `des`, `accès`, `de`, `période`, `transition` | `cette`, `elle` | — | — |
| `par14-constat-refus` | `l'échange`, `des`, `2`, `et`, `3`, `septembre`, `2015`, `que`, `le`, `la` ×2, `de`, `refus`, `l'aboutissement`, `à`, `garde`, `partagée`, `n'expliquent` | `cet`, `échange`, `deux`, `choses`, `ne`, `l'expliquent`, `cette` | `{§par14-proposition-septembre..par14-refus-septembre}`, `{§par14-premiere-phase}`, `{§par14-refus-septembre}`, `{§ax1-offre-avril..ax1-offre-dans-bornes}`, `{§par14-refus-routine}`, `{§par14-amenagement..par14-refus-septembre}` | `{§ax1-offre-avril}` |
| `par14-requalification` | `le` ×2, `motif` ×2, `la`, `dans`, `requête` | `il` ×2 | `{§par14-routine-conjoncture}`, `{§par14-plan-2013}`, `{§par14-repartition-soins}` ×2, `{§par14-requalification..par14-motif-structurel}`, `{§par14-motif-structurel}`, `{§par14-refus-routine}`, `{§par14-refus-septembre}` | — |
| `par14-absence-explication` | `la` ×2, `rare` ×2, `disponibilité` ×2, `du` ×2, `père` ×2, `n'apparaît`, `pas` ×2, `lettre`, `2015` ×2, `le` | `ce`, `ni` ×2, `celle` | `{§par14-refus-routine}`, `{§par14-refus-septembre}`, `{§par14-raison-requete..par14-repartition-soins}`, `{§par14-absence-explication..par14-lettre-septembre}` | — |
| `par14-demande-retrait` | `le`, `2016`, `la` ×3, `défenderesse` ×3, `élise` ×2, `ayoub` ×2, `au`, `demandeur`, `ne`, `16`, `septembre`, `reproche`, `répartition`, `inégale`, `d'une`, `décrit` | `n'est`, `ce` ×2, `elle` ×2, `même`, `jour`, `qu'elle`, `est` | `{§par14-demande-retrait..par14-seuil-septembre}`, `{§par14-repartition-soins}`, `{§par14-demande-retrait..par14-portee-reproche}` | — |
| `par14-conclusion` | `la` ×4, `raison` ×3, `donnée` ×3, `au` ×3, `tribunal` ×3, `pour`, `le`, `refus`, `de` ×2, `garde`, `partagée`, `est` ×3, `faits` | `et` | `{§par14-absence-explication..par14-ecrits-2015}`, `{§par14-plan-2013..par14-motif-prevu}`, `{§par14-fonction-routine..par14-fonction-avril}`, `{§ax4-termes-contestes..ax4-portrait-vie-commune}`, `{§par14-demande-retrait..par14-raison-autrice}`, `{§par14-conclusion..par14-dementi}`, `{§par14-conclusion}`, `{§par14-raison-autrice}` | `{§par14-absence-explication}`, `{§par14-plan-2013}`, `{§par14-fonction-routine}` |

### par19_35_acces_autorite

| Ancienne étiquette | Mots ajoutés | Mots retirés | Renvois ajoutés | Renvois retirés |
|---|---|---|---|---|
| `par19-these` | `les`, `19`, `à` ×2, `26`, `30`, `31`, `33`, `35`, `la`, `requête`, `des`, `rapportés`, `l'énoncé`, `va`, `est` ×2, `inexact`, `au`, `jour`, `du`, `serment`, `inexacte` | `ces` ×2, `deux`, `énoncés`, `vont`, `sont`, `inexacts` | `{§par19-omission-progressivite..par19-anteriorite-position}`, `{§par19-position-novembre}`, `{§par19-preference-novembre}` | — |
| `par19-depart` | `de`, `le` ×8, `février` ×2, `2015` ×2, `2` ×2, `demandeur` ×4, `legal/piece_chatsequence-3.md` ×4, `crédit`, `l'offre`, `du` | `les`, `dans`, `semaines`, `qui`, `précèdent`, `et`, `il` | — | — |
| `par19-refus-routine` | `le`, `27` ×2, `avril` ×2, `2015` ×2, `circonstances`, `du`, `les`, `qu'elle`, `invoque`, `invoquées` | `ces` | — | — |
| `par19-circonstances-2013` | `motifs`, `du` ×5, `le`, `legal/piece_pdf-3.md`, `courriel` ×2, `11` ×3, `juin` ×3, `2013` ×3, `allégations`, `n'invoque` | `invoque`, `ne`, `ce` | `{§par14-protection..par14-fonction-precedent}`, `{§par19-dimanches}`, `{§par19-danger-nomme}` | `{§par14-protection}` |
| `par19-offre-nuitees` | `du`, `27`, `avril`, `2015` | `même` | — | — |
| `par19-contradiction-routine` | `la`, `du`, `27`, `avril`, `2015`, `les`, `circonstances`, `invoquées` | `ainsi`, `une`, `elles` | `{§par19-refus-routine}`, `{§par19-offre-nuitees}`, `{§par19-circonstances-lettre..par19-ecrits-posterieurs}`, `{§par19-refus-routine..par19-ecrits-posterieurs}` | — |
| `par19-projet-aout` | `2015` ×2, `projet` ×2, `de` ×2, `consentement` ×2, `legal/piece_pdf-5.md` ×2, `le` ×2, `d'août` ×2, `prévoit` | `il`, `et` | — | — |
| `par19-jugement` | `le` ×2, `14`, `janvier`, `2016`, `en`, `l'absence`, `du`, `demandeur`, `tribunal`, `legal/piece_pdf-14.md` | `et` | — | — |
| `par19-omission-progressivite` | `de`, `la`, `requête` | — | `{§par19-omission-progressivite..par19-demande-hebdomadaire}` | — |
| `par19-omission-routine` | `paragraphe`, `20` ×2, `de`, `la`, `requête`, `le` ×2, `des` ×2, `accès` ×3, `du` ×3, `dimanche` ×3, `les` | `il`, `leur`, `ils`, `puis`, `en` | `{§par19-refus-routine..par19-ecrits-posterieurs}`, `{§par19-jugement..par19-pension-jugement}`, `{§par19-maintien..par19-reconduction}` | `{§par19-refus-routine}`, `{§par19-jugement}` |
| `par19-omission-offres` | `23`, `de`, `la` ×2, `requête` ×2, `paragraphe` | `elle` | — | — |
| `par19-presence-tiers` | `de` ×2, `la` ×5, `requête`, `les`, `du` ×3, `demandeur` ×4, `accès` ×3, `le` ×6, `en` ×2, `présence` ×2, `tiers` ×2, `vie`, `commune`, `défenderesse` ×3, `au`, `des` ×4, `juin` ×3, `2013` ×3, `legal/piece_thread-109.md`, `30`, `à` ×2, `11` ×2, `ayoub`, `élise`, `courriel`, `n'a`, `maintien` | `il` ×3, `ce` ×2, `celle-ci`, `elle` ×2, `lui` ×3, `lendemain`, `a`, `ces` ×2, `n'en` | `{§par19-tiers-separation..par19-restrictions-vie-commune}` ×2, `{§par19-circonstances-2013..par19-regime-sans-nuitee}`, `{§par19-sort-allegations}`, `{§par19-restrictions-vie-commune}`, `{§par19-courriel-soeur}`, `{§par19-refus-routine..par19-ecrits-posterieurs}` | `{§par19-circonstances-2013}`, `{§par19-refus-routine}` |
| `par19-autorite` | `de` ×2, `la` ×5, `requête` ×5, `tait` ×3, `que`, `nicolas` | `elle` | `{§par19-autorite}`, `{§par19-position-decisions}` | — |
| `par19-espacement` | `paragraphes`, `33` ×2, `à` ×2, `35` ×2, `de`, `la`, `requête`, `les` ×2 | `ces`, `ils`, `or` | `{§par19-refus-routine..par19-ecrits-posterieurs}`, `{§par19-jugement..par19-pension-jugement}`, `{§par19-allegations}` | `{§par19-jugement}` |
| `par19-connaissance` | `de` ×2, `la` ×7, `défenderesse` ×4, `elle-même`, `que` | `elle`, `sa` ×2, `propre`, `qu'elle`, `cette`, `même` | `{§par19-connaissance..par19-messages-joints}` | — |
| `par19-requalification` | `des`, `à`, `examinés`, `la`, `routine` | `de`, `ces`, `lui` | `{§par19-omission-offres..par19-terme-refuse}`, `{§par19-autorite..par19-reponse-decisions}` | — |
| `par19-conclusion` | `le`, `justification`, `d'un`, `père`, `désengagé`, `qui`, `refuse` | `ce` | `{§par19-allegations}` ×2, `{§par19-horaire-jugement}`, `{§par19-motif-requete}`, `{§par19-maintien}`, `{§par19-omission-offres..par19-reponse-omise}`, `{§par19-bapteme}`, `{§par19-elements-connus}` | — |

### par28_29_mediation

| Ancienne étiquette | Mots ajoutés | Mots retirés | Renvois ajoutés | Renvois retirés |
|---|---|---|---|---|
| `par28-these` | `le` ×2, `l'intervention`, `claudia`, `écrement`, `consultation` ×2, `demandeur` ×2, `refusée`, `n'a`, `du` | `et`, `or`, `ce`, `refusé`, `il`, `ne`, `l'a`, `son` | `{§par28-these..par28-identification}`, `{§par28-nature..par28-exclusion}`, `{§par28-acceptation}`, `{§par28-annulation}`, `{§par28-p4}` | — |
| `par28-nature` | — | `et` | `{§par28-offre-ecrement/c}` | — |
| `par28-origine-offre` | `du`, `16`, `septembre`, `2015`, `le` | `ce` | — | — |
| `par28-acceptation` | `16`, `septembre`, `2015`, `la`, `rencontre`, `legal/piece_thread-16_ecrement_2015.md` ×2 | `jour`, `même` | — | — |
| `par28-annulation` | `le` ×4, `7`, `octobre` ×2, `2015`, `demandeur` ×2, `du`, `19`, `legal/piece_thread-16_ecrement_2015.md` ×2 | `il` ×2, `ce` | — | — |
| `par28-portee-refus` | `le`, `demandeur` | `il` | `{§par28-acceptation}`, `{§par28-annulation}`, `{§par28-services}` | — |
| `par28-p4` | `7`, `octobre`, `2015`, `la`, `de`, `portée`, `du` ×2, `refus`, `demandeur` | `même`, `jour`, `en` | — | — |
| `par28-p4-contenu` | `la`, `pièce`, `produite` ×2, `au` ×2, `soutien` ×2, `du` ×2, `paragraphe` ×2, `29` ×2 | `elle` | — | — |
| `par28-connaissance-propre` | `la`, `défenderesse` | `elle` | — | — |
| `par28-email-190` | `la` ×2, `défenderesse`, `de`, `médiation`, `qualification` | `elle` ×2, `puis` | `{§par28-p4}`, `{§par28-email-190}`, `{§par28-allegations}` | — |
| `par28-accumulation` | `le` ×2, `paragraphe`, `29`, `que`, `demandeur`, `a`, `accepté`, `de`, `communiquer`, `avec`, `au`, `sujet`, `des`, `enfants`, `elle` | `il` | `{§par28-categorie..par28-repetition}` | — |
| `par28-mot-mediation` | `le`, `la` ×2, `passage`, `assermenté` | `cette` ×2, `et` | `{§par28-allegations}` ×2, `{§par28-offre-defenderesse}`, `{§par28-origine-offre..par28-offre-defenderesse}`, `{§par28-nature..par28-exclusion}` | `{§par28-origine-offre}` |
| `par28-conclusion` | `le`, `demandeur`, `la`, `défenderesse`, `connaissait` | `et`, `il` | `{§par28-acceptation}`, `{§par28-annulation..par28-services}`, `{§par28-nature..par28-exclusion}`, `{§par28-autre-proposition}`, `{§par28-origine-offre..par28-offre-defenderesse}`, `{§par28-connaissance-propre..par28-nature-connue}` | `{§par28-origine-offre}` |

### par56_58_assurances

| Ancienne étiquette | Mots ajoutés | Mots retirés | Renvois ajoutés | Renvois retirés |
|---|---|---|---|---|
| `par56-contestation` | `ne`, `pas`, `paragraphe`, `56`, `les`, `trois`, `affirmations`, `du`, `57`, `des`, `à` ×2, `58`, `que`, `correspondaient`, `ce`, `qu'elle`, `vivait` | `le`, `et`, `de`, `ces` | `{§par56-refus-utilisation..par56-demandes-documentees}`, `{§par56-connaissance..par56-vecu-serment}` | — |
| `par56-depenses-mere` | `la` ×2, `requête` ×2 | `elle` ×2 | — | — |
| `par56-prestations` | `au`, `nom`, `des`, `enfants`, `legal/piece_pdf-63.md` ×2, `pour`, `sont` | `dont` | — | — |
| `par56-aucun-dimanche` | `des`, `dix`, `prestations`, `legal/piece_pdf-63.md`, `les` | `de`, `ces`, `elles` | `{§par56-acces-dimanche}`, `{§par56-aucun-dimanche}` | — |
| `par56-paiements-directs` | `des`, `dix`, `prestations` | `les`, `premières` | — | — |
| `par56-derniere-prestation` | `prestation` | — | — | — |
| `par56-refus-utilisation` | `le`, `paragraphe`, `57`, `affirme`, `du`, `23`, `février`, `au`, `19`, `novembre`, `2015`, `legal/piece_pdf-63.md`, `d'utilisation` | `et` | — | — |
| `par56-exclusivite` | `le`, `paragraphe`, `57`, `affirme`, `enfants`, `legal/piece_pdf-63.md`, `prestation` | — | `{§par56-acces-dimanche}`, `{§par56-aucun-dimanche}` | — |
| `par56-refus-solde` | `le`, `paragraphe`, `57`, `affirme`, `de`, `payer`, `la`, `différence`, `non`, `couverte`, `par`, `les`, `assurances`, `demande`, `ne` | `n'en`, `et` | — | — |
| `par56-depenses-juillet` | `de`, `110`, `legal/piece_pdf-63.md` | — | — | — |
| `par56-remboursements` | `les`, `juillet` ×2, `2015` ×2, `des`, `remboursés`, `en` | `ces` ×2 | — | — |
| `par56-connaissance` | `du`, `allégué`, `par`, `la` ×4, `défenderesse` ×4, `elle-même`, `sept`, `au`, `des`, `moment`, `serment`, `legal/piece_pdf-63.md` | `sa`, `propre`, `allégation`, `elle` ×3, `de`, `ces` | `{§par56-regime-allegue..par56-paiements-directs}`, `{§par56-achats}`, `{§par56-connaissance..par56-message-aout}` | — |
| `par56-presentation` | `le` ×5, `14` ×4, `janvier` ×4, `2016` ×4, `legal/piece_pdf-14.md` ×4, `tribunal` | `et` | — | — |
| `par56-prestation-janvier` | `avant`, `la` ×3, `présentation`, `de`, `requête`, `le`, `11` ×2, `janvier` ×2, `2016` ×2, `du`, `legal/piece_pdf-64.md`, `est` | `plus`, `tôt`, `un`, `c'est` | `{§par56-acces-dimanche}`, `{§par56-prestation-janvier}` | — |
| `par56-contradiction-audience` | — | — | `{§par56-presentation}`, `{§par56-prestation-janvier}` | — |
| `par56-conclusion` | `le`, `refus` ×2, `paragraphe`, `57`, `a`, `de`, `du`, `l'affirmation` | `l'a`, `et`, `cette`, `affirmation` | `{§par56-soldes..par56-solde-recent}`, `{§par56-presentation}`, `{§par56-prestation-janvier}`, `{§par56-allegations}` | — |

### p4_portee

| Ancienne étiquette | Mots ajoutés | Mots retirés | Renvois ajoutés | Renvois retirés |
|---|---|---|---|---|
| `p4-allegations` | — | — | `{§par19-circonstances-2013..par19-regime-sans-nuitee}` | `{§par19-circonstances-2013}` |
| `p4-objet` | `l'objet`, `de`, `la`, `section` | `son`, `objet` | — | — |
| `p4-me-ayoub` | `me` ×2, `marie-josée` ×2, `ayoub` ×2, `n'a`, `pas` ×2, `n'attribue`, `à` | `ni` ×2, `ne`, `lui`, `attribue` | `{§p4-me-ayoub..p4-representation}` | — |

## Renvois entrants ajustés

Chaque ligne indique une occurrence préexistante dont la cible simple a été étendue à toutes ses parties. Les intervalles qui conservaient leurs bornes et les renvois à un sous-item conservé gardent leur cible.

| Bloc porteur | Paragraphe porteur après découpage | Ancienne cible | Cible après découpage |
|---|---|---|---|
| `p2_axe1_plan_juin_2013.md` | `ax1-motifs-successifs` | `{§par14-raison-requete}` | `{§par14-raison-requete..par14-milieu-stable}` |
| `par07_role_de_pere.md` | `par07r-demarche` | `{§par07-therapie}` | `{§par07-therapie..par07-factures-juin}` |
| `par07_role_de_pere.md` | `par07r-accessibilite-retour` | `{§par07-retour}` | `{§par07-retour..par07-reprise-vie-commune}` |
| `par07_role_de_pere.md` | `par07r-factures` | `{§par07-therapie}` | `{§par07-therapie..par07-factures-juin}` |
| `par09_ete_2013.md` | `par09-allegations-2013` | `{§par19-circonstances-2013}` | `{§par19-circonstances-2013..par19-regime-sans-nuitee}` |
| `par10_rachat.md` | `par10-plainte` | `{§par19-circonstances-2013}` | `{§par19-circonstances-2013..par19-regime-sans-nuitee}` |
| `par10_rachat.md` | `par10-reception` | `{§par10-copies}` | `{§par10-copies..par10-seconde-copie}` |
| `par14_17_motif.md` | `par14-conclusion` | `{§par14-absence-explication}` | `{§par14-absence-explication..par14-ecrits-2015}` |
| `par14_17_motif.md` | `par14-substitution` | `{§par14-plan-2013}` | `{§par14-plan-2013..par14-motif-prevu}` |
| `par14_17_motif.md` | `par14-substitution` | `{§par14-fonction-routine}` | `{§par14-fonction-routine..par14-fonction-avril}` |
| `par18_entente.md` | `par18-routine-refus` | `{§par14-constat-refus}` | `{§par14-constat-refus..par14-limite-motifs}` |
| `par19_35_acces_autorite.md` | `par19-danger-nomme` | `{§par14-protection}` | `{§par14-protection..par14-fonction-precedent}` |
| `par19_35_acces_autorite.md` | `par19-maintien` | `{§par19-refus-routine}` | `{§par19-refus-routine..par19-ecrits-posterieurs}` |
| `par19_35_acces_autorite.md` | `par19-reconduction` | `{§par19-jugement}` | `{§par19-jugement..par19-pension-jugement}` |
| `par19_35_acces_autorite.md` | `par19-courriel-soeur` | `{§par19-circonstances-2013}` | `{§par19-circonstances-2013..par19-regime-sans-nuitee}` |
| `par19_35_acces_autorite.md` | `par19-cadre-maintenu` | `{§par19-refus-routine}` | `{§par19-refus-routine..par19-ecrits-posterieurs}` |
| `par19_35_acces_autorite.md` | `par19-espacement-regime` | `{§par19-refus-routine}` | `{§par19-refus-routine..par19-ecrits-posterieurs}` |
| `par19_35_acces_autorite.md` | `par19-espacement-regime` | `{§par19-jugement}` | `{§par19-jugement..par19-pension-jugement}` |
| `par28_29_mediation.md` | `par28-offre-psychologue` | `{§par28-origine-offre}` | `{§par28-origine-offre..par28-offre-defenderesse}` |
| `par28_29_mediation.md` | `par28-autrice` | `{§par28-origine-offre}` | `{§par28-origine-offre..par28-offre-defenderesse}` |
| `p4_portee.md` | `p4-allegations` | `{§par19-circonstances-2013}` | `{§par19-circonstances-2013..par19-regime-sans-nuitee}` |

Trois occurrences proviennent de blocs hors lot, dans l’axe 1, le § 9 et le § 18. Aucun exemple de `METHODE.md` ou d’`objections_en_attente.md` ne devient invalide du fait du lot. Aucun renvoi d’annexe ne requiert d’ajustement.

## Intertitres et cotes de la requête

Les six mentions en italique de `par19_35_acces_autorite.md` sont devenues des intertitres de niveau 4, dans leur ordre initial.

- Paragraphes 19 et 26 de la requête
- Paragraphe 20 de la requête
- Paragraphes 23 et 24 de la requête
- Paragraphe 21 de la requête
- Paragraphes 30 et 31 de la requête
- Paragraphes 33 à 35 de la requête

Chaque occurrence de cote de la requête dans le corps est conservée à l’identique.

| Cote | Ancienne étiquette | Étiquette après découpage | § assemblé |
|---|---|---|---:|
| P-5 | `par19-allegations` | `par19-allegations` | 556 |
| P-5 | `par19-autorite` | `par19-autorite` | 614 |
| P-5 | `par19-connaissance` | `par19-messages-joints` | 629 |
| P-4 | `par28-allegations` | `par28-allegations` | 639 |
| P-4 | `par28-these` | `par28-identification` | 641 |
| P-4 | `par28-p4` | `par28-p4` | 658 |
| P-4 | `par28-email-190` | `par28-qualification` | 666 |
| P-4 | `par28-mot-mediation` | `par28-cooperation` | 676 |
| P-4 | `par28-conclusion` | `par28-connaissance-refus` | 681 |
| P-5 | `par56-depenses-juillet` | `par56-lettre-psychologue` | 709 |
| P-5 | `par56-connaissance` | `par56-message-aout` | 716 |

Dans les notes inchangées sur la médiation, P-4 figure aussi aux notes 1 et 12.

## Contrôles

Les 119 paragraphes du lot donnent 346 paragraphes. 85 anciens paragraphes sont scindés. 114 paragraphes portent un renvoi interne, 11 renvoient à une annexe et 124 portent au moins un de ces renvois. Les 129 passages entre guillemets sont identiques à l’archive, caractère par caractère et dans le même ordre. Le rendu de ces citations concorde également avec celui de la branche de départ.

La relecture des 346 paragraphes du lot dans le Markdown assemblé sans annexes ne relève aucun paragraphe sans verbe conjugué, commençant par un connecteur ou par une mention en italique suivie d’un point. Le lot ne contient aucune thèse en italique. Tous les renvois aux annexes du lot passent par leur identifiant.

| § | Pronom en tête | Justification |
|---:|---|---|
| 379 | C’est | Présentatif. La même phrase nomme les cours de danse et la routine d’Alexia. |
| 486 | Aucun | Son complément dans la phrase désigne les écrits de 2015 versés au dossier. |
| 558 | Chacun | Son complément dans la phrase désigne les faits rapportés. |
| 691 | Aucune | Son complément dans la phrase désigne les dix prestations. |

Le contrôle de lecture des parties III et IV, en excluant seulement le bloc de l’été 2013, inclut aussi les 55 paragraphes du § 18 déjà découpé. Sur ces 401 paragraphes, aucun début par un connecteur ou par une mention en italique, aucune proposition principale sans verbe conjugué, aucune thèse en italique et aucune cote d’annexe saisie à la main. Deux débuts pronominaux s’ajoutent à la liste du lot. Au § 513, « C’est » introduit la date du transfert dans la même phrase. Au § 529, « Rien » est un pronom indéfini négatif sans antécédent requis. Dans le § 18, 19 paragraphes portent un renvoi interne (506, 511, 514, 521–523, 531–532, 535, 539, 543–546, 548–551 et 554). Les 401 paragraphes comptent donc 133 porteurs de renvoi interne, dont un porte aussi un renvoi d’annexe, et 143 porteurs d’au moins un renvoi.

Le vérificateur ciblé produit les mêmes 124 lignes OK, 2 lignes OK* et 1 ligne NO que sur la branche de départ (sortie intégralement identique, code 1). Le NO concerne le texte intégral du paragraphe 29 de la requête, que la fiche abrège. La note 8 du bloc sur la médiation le documente.

Les deux commandes d’assemblage produisent le Markdown et le Word, avec 16 blocs, 742 paragraphes et autant d’étiquettes. L’assemblage complet comprend 9 annexes. Les deux commandes terminent avec le code 0, sans ERREUR ni ALERTE. Les listes de CITATION NO concordent ligne pour ligne avec la référence (65 avec annexes, 2 sans annexes). Les deux fichiers Word s’ouvrent comme paquets OOXML et leur document XML est lisible.
