# Socle élargi — appariement par similarité

Généré par `docs/purge_quotes/socle_similarite.py`. Lecture seule.

Mesure : part des **4-grammes de mots** d'une citation retrouvés dans un même fichier `legal/**/*.md` (*taux de reprise*). Contrairement au socle strict, cette mesure attrape les citations tronquées, remaniées, ou dont l'analyse n'a gardé qu'un noyau. Les citations de moins de 6 mots sont écartées : la mesure n'y a pas de sens.

| Palier | Taux | Citations |
|---|---|---|
| reprise quasi intégrale | ≥ 0.85 | 186 |
| largement reprise | ≥ 0.60 | 28 |
| noyau repris | ≥ 0.35 | 15 |
| écho faible | ≥ 0.15 | 17 |
| absente | ≥ 0.00 | 59 |
| **total mesurable** | | **305** |

- socle **strict** (texte mot pour mot) : **115** citations ;
- **+99** citations atteignent un taux ≥ 0,60 sans être dans le socle strict → **socle élargi** ;
- **15** citations entre 0,35 et 0,60 → à trancher à l'œil.

---

## 1. Nouvelles entrées du socle (99) — taux ≥ 0,60, absentes du socle strict

Ces citations ont bel et bien servi à l'analyse : leur texte y figure remanié, tronqué ou fondu dans la phrase. L'égalité stricte les manquait.

| id | source | taux | trames | fichier .md | passage en base |
|---|---|---|---|---|---|
| `pq-96` | pdf-5 p.2 | **1.00** | 50 | `legal/piece_pdf-5.md` | toutefois puisque le père refuse de prendre les décisions importantes eu égard aux enfants il c… |
| `pq-95` | pdf-5 p.2 | **1.00** | 50 | `legal/analyse/Responsabilité civile/requete 21 octobre 2019/analyse preliminaire - echec negociations 2015 et paragraphe 3.md` | les parties continueront d'exercer conjointement l'autorité parentale à l'égard des enfants min… |
| `pq-94` | pdf-5 p.1 | **1.00** | 50 | `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/03_concordance_aout_novembre_2015.md` | les enfants ne font pas l'objet d'une décision de la cour du québec chambre de la jeunesse ni d… |
| `pq-92` | pdf-5 p.3 | **1.00** | 50 | `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md` | à compter de ce jour jusqu'au 28 août 2016 semaine 1 de samedi 10h30 directement à la piscine à… |
| `pq-91` | pdf-5 p.1 | **1.00** | 50,76 | `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/01_inexecution_plan_cohabitation.md` | attendu que le demandeur visite les enfants uniquement quelques heures les dimanches… |
| `pq-69` | pdf-1 p.1 | **1.00** | 62,70,71,72 | `legal/allegation_stmt13_ete2013.md` | tu dois le faire sortir de la maison… |
| `pq-67` | pdf-6 p.2 | **1.00** | 56 | `legal/piece_pdf-6.md` | en ce qui concerne les périodes de garde où votre cliente serait avec les enfants soit les lund… |
| `pq-66` | pdf-6 p.2 | **1.00** | 56 | `legal/piece_pdf-6.md` | cependant il souhaite ajouter un sous-paragraphe e afin de prévoir qu'à compter du 7 février 20… |
| `pq-64` | pdf-1 p.1 | **1.00** | 56,62 | `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md` | le meilleur moment pour lui envoyer la procédure est jeudi pour qu'on aille à la cour vendredi … |
| `pq-63` | pdf-1 p.1 | **1.00** | 56,62 | `legal/allegation_stmt62_separation_2011.md` | tu veux avoir la garde et lui puisse voir les enfants plusieurs fois par semaine… |
| `pq-62` | pdf-1 p.1 | **1.00** | 56,62,70 | `legal/allegation_stmt14_15_16_17_garde_partagee.md` | pendant toute cette procédure les enfants sont avec toi donc cela créé un précédant c'est à dir… |
| `pq-61` | pdf-1 p.1 | **1.00** | 56,62 | `legal/allegation_stmt14_15_16_17_garde_partagee.md` | on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser… |
| `pq-58` | pdf-1 p.1 | **1.00** | 56,62 | `legal/allegation_stmt62_separation_2011.md` | alexia vie dans la violence conjugale depuis sa naissance tout intervenant de la dpj pourra arr… |
| `pq-57` | pdf-1 p.1 | **1.00** | 56,62 | `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/11_memoire_argumentative_verrouillee_continuite_P2_P19.md` | je t'écris comme si tu étais une cliente à laquelle je donnais conseil… |
| `pq-55` | pdf-1 p.1 | **1.00** | 55 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` | si j'étais ton avocate le plan serait le suivant faire une requête pour garde exclusive d'urgen… |
| `pq-34` | pdf-1 p.1 | **1.00** | 48 | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/03_anteriorite_preference_et_fonction_du_registre.md` | alexia vie dans la violence conjugale depuis sa naissance tout intervenant de la dpj pourra arr… |
| `pq-28` | pdf-6 p.2 | **1.00** | 34,40 | `legal/piece_pdf-6.md` | notre client est tout à fait disposé à établir une progression dans les droits d'accès auprès d… |
| `pq-21` | pdf-1 p.1 | **1.00** | 22 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` | on l'oblige également à payer 50 des charges afférentes à la maison on peut également demander … |
| `pq-20` | pdf-1 p.1 | **1.00** | — | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` | on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser et on l'oblige … |
| `pq-16` | pdf-11 p.1 | **1.00** | 20 | `legal/piece_pdf-11.md` | étude de la valeur marchande en date des présentes à des fins de partage… |
| `pq-14` | pdf-6 p.2 | **1.00** | — | `legal/piece_pdf-6.md` | en ce qui concerne les périodes de garde où votre cliente serait avec les enfants soit les lund… |
| `eq-209` | email-238 | **1.00** | — | `legal/piece_chatsequence-1.md` | quand je suis arrêtée je tombe à 80 de mon salaire en passant… |
| `eq-203` | email-180 | **1.00** | 69,75 | `legal/piece_thread-ecrement_2015.md` | bon matin mme écremment je ne pourais pas ce soir de plus je souhaites annuler mon rendez vous … |
| `eq-183` | email-53 | **1.00** | 50,67 | `legal/faits_chronologiques_2010-11-20_2012-02-06.md` | good morning my daughter is sick and i'll be staying at home today with her… |
| `eq-180` | email-64 | **1.00** | 50,67 | `legal/faits_chronologiques_2010-11-20_2012-02-06.md` | good morning i won't be coming in today i have to stay with my daughter she is sick and must go… |
| `eq-175` | email-352 | **1.00** | — | `legal/journal_ete2013.md` | pour la moitié oui sur ma marge ça en vaudrait la peine le 14 octobre aussi c'est pas cher… |
| `eq-170` | email-355 | **1.00** | — | `legal/piece_thread-83_email-355.md` | direction loisirs culture et vie communautaire 600 avenue oak saint-lambert… |
| `eq-161` | email-445 | **1.00** | — | `legal/piece_thread-109.md` | pendant ces 2 nuit alexia n eatit pas inquiete etait tres heureuse c est aussi normale qu elle … |
| `eq-135` | email-475 | **1.00** | 9,38 | `legal/piece_thread-116_email-475.md` | pour ce qui est de la garde je ne peux accepter les termes proposés par élise la raison princip… |
| `eq-131` | email-330 | **1.00** | 62 | `legal/piece_thread-4_email-330.md` | j'arrives à la fin de mes économies a la fin de mon bail de toute évidence je ne peux pas parti… |
| `eq-127` | email-456 | **1.00** | 62 | `legal/piece_thread-111_congediement_bnc.md` | suite au constat que vous ne répondez malheureusement pas aux attentes de votre poste… |
| `eq-126` | email-4 | **1.00** | 62 | `legal/inventaire_incompatibilites.md` | nous avons procédé devant un juge tu as plaidé ta cause et nous la nôtre il y a eu un jugement … |
| `eq-125` | email-448 | **1.00** | — | `legal/piece_thread-109.md` | je ne souhaite pas aller en cours mais tu comprends que l enjeux est enorme… |
| `eq-124` | email-447 | **1.00** | 56 | `legal/piece_thread-109.md` | ce que je comprends de ce que tu m'offre c est - tu va pouvoir faire les choses que tu veux fai… |
| `eq-122` | email-6 | **1.00** | — | `legal/allegation_stmt14_15_16_17_garde_partagee.md` | je ne t'ai jamais traiter d'incapable je t'ai parlé de leur lien d'attachement je ne t'ai jamai… |
| `eq-109` | email-296 | **1.00** | 55 | `legal/piece_thread-6_reconstruction.md` | n'assumes pas ce que j'aurais été en mesure d'accepter si je ne m'étais pas occupé de mes enfan… |
| `eq-98` | email-171 | **1.00** | 53,74 | `legal/allegation_stmt4_5_6.md` | nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année… |
| `eq-97` | email-167 | **1.00** | 53,74 | `legal/allegation_stmt4_5_6.md` | je ne te considérais pas comme mon coloc… |
| `eq-74` | email-349 | **1.00** | 8,26 | `legal/piece_thread-109.md` | ce que je comprends de ce que tu m'offre c est - tu va pouvoir faire les choses que tu veux fai… |
| `eq-73` | email-48 | **1.00** | 5,64 | `legal/axe_agenda_danse_elise.md` | je sais que je dois etre a la maison de bonne heure ce soir parceque tu danses… |
| `eq-59` | email-347 | **1.00** | 65 | `legal/piece_thread-78_email-347.md` | ce matin je me suis reveille tot je suis partis parceque je sais que je dois etre a la maison d… |
| `eq-57` | email-29 | **1.00** | 4,5,65 | `legal/piece_thread-23_email-148.md` | veux tu en profiter pour fêter alexia nicolas voulait aller te voir hier quand je suis aller le… |
| `eq-37` | email-48 | **1.00** | 4,5,65 | `legal/piece_thread-78_email-347.md` | je t'ai ecris que je partais tot je t'ai offert avec beinveillance et bonne volonté de m'occupe… |
| `eq-22` | email-51 | **1.00** | 3,31 | `legal/piece_thread-40_email-50.md` | hi i have to stay home again today my mother in law can t come in you ll bebable tomreach me at… |
| `eq-15` | email-349 | **1.00** | 2,8 | `legal/piece_thread-109.md` | elise les 2 chemins ne mene pas au meme resultat avec alexia pas du tout tout ce que je veux c … |
| `eq-7` | email-33 | **1.00** | 2,11 | `legal/piece_thread-26_emails-33-32.md` | si tu viens demain avec nicholas on passera che josée puis ru prendras la vignettes… |
| `eq-54` | email-7 | **0.98** | — | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/01_architecture_justificative_stabilite.md` | j'étais tout le temps à la maison tu vas honnêtement venir me dire que pendant tout ce temps pa… |
| `eq-42` | email-116 | **0.97** | 5,31,64 | `legal/piece_thread-52_emails-66-115-116.md` | salut ce soir elise ne va pas a son premier cour de danse je sais pas a quelle heure elle va pa… |
| `pq-5` | pdf-1 p.1 | **0.95** | — | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/03_anteriorite_preference_et_fonction_du_registre.md` | faire une requête pour garde exclusive d'urgence et usage exclusif de la résidence familiale on… |
| `eq-132` | email-462 | **0.95** | 62 | `legal/piece_thread-113_email-462.md` | salut mj suite au dernier jugement mon compte de banque a été saisie il y a environ 2 semaines … |
| `eq-61` | email-116 | **0.95** | 31 | `legal/piece_thread-52_emails-66-115-116.md` | salut ce soir elise ne va pas a son premier cour de danse je sais pas a quelle heure elle va pa… |
| `eq-94` | email-7 | **0.94** | 4,50,64 | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/01_architecture_justificative_stabilite.md` | je n'ai pas décider de ne pas m'en occuper 50 du temps je m'excuses mais j'étais tout le temps … |
| `eq-2` | email-40 | **0.93** | 2,3 | `legal/piece_thread-32_email-40.md` | salut karl je vais rester a la maison aujourd hui pour aider ma conjointe avec le bebe elle ne … |
| `eq-34` | email-87 | **0.93** | 24 | `legal/piece_emails_petite_enfance_2010.md` | salut oui viens garder vendredi si tu peux confirme moi pour que j'avertisse la mere à elise… |
| `eq-182` | email-59 | **0.92** | 50,67 | `legal/piece_thread-46_emails-58-59.md` | j'ai essayer de convaincre ma copine que tu avais plus besoins de moi que ma fille mais en vain… |
| `eq-28` | email-30 | **0.92** | 3 | `legal/piece_thread-24_email-30.md` | salut karl je vais à la clinique ce matin avec mon gars et en fonction de ce qu'ils me disent j… |
| `eq-35` | email-86 | **0.91** | 24 | `legal/piece_emails_petite_enfance_2010.md` | salut peux tu arriver vers 7hre - 7h15 demain j'ai une entrevue chez hydro qubec a 8h30 et je d… |
| `eq-208` | email-404 | **0.91** | 44 | `legal/piece_thread-100_email-404.md` | dernière chose est il possible dans l entente que je demande de ne plus avoir a donner mon cons… |
| `eq-69` | email-373 | **0.91** | 8 | `legal/piece_emails_cape_cod_2012.md` | j'ai repensé à alexia et en ai discuté avec ton père si tu as envie de l'amener ca nous permett… |
| `eq-68` | email-49 | **0.90** | 8,31 | `legal/piece_emails_cape_cod_2012.md` | je t'envoie trois possibilités de maisons à cape cod - je m'attends à ce qu'élise ne soit pas d… |
| `eq-107` | email-285 | **0.90** | 55 | `legal/piece_thread-6_reconstruction.md` | donc tu m'as condamnée car je n'étais pas d'accord avec toi donc si on n'est pas d'accord avec … |
| `pq-26` | pdf-1 p.1 | **0.90** | 39 | `legal/analyse/Responsabilité civile/courriel 11 juin 2013 - responsabilite de Me Ayoub.md` | je t'écris comme si tu étais une cliente à laquelle je donnais conseil alexia vie dans la viole… |
| `pq-25` | pdf-1 p.1 | **0.89** | 6,34,36,52 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` | je t'écris comme si tu étais une cliente à laquelle je donnais conseil alexia vie dans la viole… |
| `pq-27` | pdf-3 p.2 | **0.88** | 34,39,42,49,71,72,73,76 | `legal/allegation_stmt19_20_21_acces.md` | nous considérons qu'il y a contre-indication à l'établissement de la garde parlagée des deux 2 … |
| `eq-16` | email-69 | **0.88** | 3,31 | `legal/piece_thread-54_emails-68-69.md` | bon matin catherine je dois rester avec ma petite aujourd hui j'imagine qu il y a des journées … |
| `eq-190` | email-42 | **0.88** | 67 | `legal/piece_thread-34_email-42.md` | bon matin karl je ne retrerai pas travailler aujourd hui je vais rester a la maison avec ma pet… |
| `eq-5` | email-34 | **0.88** | 2 | `legal/piece_thread-27_email-34.md` | bonne fête lp et puis ton party vendredi c'était cool salut eve oui on a eu bien du plaisir y'a… |
| `pq-17` | pdf-1 p.1 | **0.87** | 21 | `legal/amendements/01_avant_notification/faits_experimentaux/01_planification_statu_quo_garde.md` | je t'écris comme si tu étais une cliente à laquelle je donnais conseil si j'étais ton avocate l… |
| `eq-188` | email-55 | **0.87** | 67 | `legal/piece_thread-43_email-55.md` | good morning i have to stay home today with my daugter because she is sick i will be reacheble … |
| `eq-21` | email-53 | **0.87** | 3,31 | `legal/piece_thread-123_email-488.md` | good morning my daugther is sick and i ll be staying at home today with her thanks lp… |
| `pq-82` | pdf-13 p.2 | **0.86** | 62 | `legal/piece_pdf-13.md` | 10h17 04 le tribunal informe monsieur de ne pas parler de ce qui s'est passé avant 2016… |
| `eq-62` | email-137 | **0.85** | 14 | `legal/allegation_stmt66_residence_2014.md` | le sous sol on l'a démolie suite a une inondation l'année dernière et nous ne l'avons jamais te… |
| `pq-10` | pdf-3 p.2 | **0.84** | 9,38,55,56,71,72,73,76 | `legal/allegation_stmt19_20_21_acces.md` | il y a contre-indication à l'établissement de la garde parlagée des deux 2 enfants mineurs vu l… |
| `eq-194` | email-21 | **0.83** | 50,67 | `legal/piece_thread-17_email-21.md` | bonjour nicolas est malade je reste a la maison… |
| `eq-31` | email-21 | **0.83** | 3 | `legal/piece_thread-17_email-21.md` | bonjour nicolas est malade je reste a la maison… |
| `pq-11` | pdf-2 p.1 | **0.83** | 9,34,38,39,47,49,52,56 | `legal/piece_pdf-2.md` | au niveau de la garde des deux 2 enfants mineurs nous ne voyons aucune contre-indication à l'ét… |
| `pq-13` | pdf-7 p.1 | **0.82** | — | `legal/piece_pdf-7.md` | notre cliente considère qu'il est prématuré à te stade ci d'entrevoir l'aménagement d'une garde… |
| `eq-29` | email-28 | **0.81** | 3 | `legal/piece_thread-22_email-28.md` | salut voici le papier du medicine je vais manquer le cmoc et le dîner d équipe mais je suis mal… |
| `eq-19` | email-56 | **0.81** | 3,31 | `legal/piece_thread-44_email-56.md` | salut catherine je dois rester avec ma fille cet avant midi je rentrerai au ttavail cet apres m… |
| `eq-196` | email-28 | **0.81** | 67 | `legal/piece_thread-22_email-28.md` | salut voici le papier du medicine je vais manquer le cmoc et le dîner d'équipe mais je suis mal… |
| `eq-20` | email-55 | **0.80** | 3,31 | `legal/piece_thread-43_email-55.md` | good morning i have to stay home today with my daugter because she is sick i will be reacheble … |
| `eq-192` | email-40 | **0.79** | 67 | `legal/piece_thread-32_email-40.md` | salut karl je vais rester a la maison aujourd hui pour aider ma conjointe avec le bebe elle ne … |
| `pq-74` | pdf-13 p.2 | **0.76** | 62 | `legal/piece_pdf-13.md` | 10h13 11 témoignage de m david - questions du tribunal objection de me ayoub un jugement a été … |
| `pq-83` | pdf-13 p.2 | **0.75** | 62 | `legal/compilation_griefs.md` | 10h38 50 p-2 en liasse plusieurs recherches d'emploi offertes à monsieur… |
| `pq-75` | pdf-13 p.2 | **0.75** | 62 | `legal/compilation_griefs.md` | 10h38 50 p-2 en liasse plusieurs recherches d'emploi offertes à monsieur… |
| `eq-184` | email-51 | **0.75** | 50,67 | `legal/piece_thread-40_email-50.md` | hi i have to stay home again today my mother in law can't come in… |
| `eq-193` | email-30 | **0.72** | 67 | `legal/piece_thread-24_email-30.md` | salut karl je vais à la clinique ce matin avec mon gars et en fonction de ce qu ils me disent j… |
| `pq-84` | pdf-13 p.3 | **0.72** | 62 | `legal/piece_pdf-13.md` | attendu que les parties après le début de l'audition se sont entendues à ce qu'un jugement soit… |
| `pq-32` | pdf-5 p.4 | **0.71** | 48,49,50,55 | `legal/piece_pdf-5.md` | si le père ne désire pas exercer ses droits d'accès prévus audit consentement auprès des enfant… |
| `pq-29` | pdf-7 p.4 | **0.70** | 44 | `legal/piece_photodoc-13.md` | svp pour toi check pour le transfert d autorité parentale je suis serieux je ne vais pas signer… |
| `eq-189` | email-45 | **0.69** | 67 | `legal/piece_thread-36_email-45.md` | salut ma fille a la gastro je dois rester a la maison je serrai disponible au 450 550 2998… |
| `eq-23` | email-47 | **0.68** | 3 | `legal/piece_thread-37_email-47.md` | bonjour je restes a la maison avec ma fille aujourd hui si danilo a des questions je suis dispo… |
| `pq-12` | pdf-59 p.1 | **0.66** | 12,64 | `legal/piece_pdf-59.md` | en 1999 fascinée par la danse elle se joint à l'école de danse les ballets modernes du québec e… |
| `eq-142` | email-410 | **0.65** | 62 | `legal/piece_pension_nonmodif_jan2019.md` | la pension alimentaire ne sera pas modifiée à ce stade-ci nous avons procédé à des représentati… |
| `eq-191` | email-41 | **0.65** | 67 | `legal/implication_parentale_recurrence/04_journees_maladie.md` | bon matin karl je vais etre au fravail lundi la sittuation se stabilise mais nous ne dormons qu… |
| `eq-24` | email-45 | **0.65** | 3 | `legal/piece_thread-36_email-45.md` | salut ma fille a la gastro je dois rester a la maison je serrai disponible au 450 550 2998 loui… |
| `eq-93` | email-343 | **0.65** | 44 | `legal/piece_thread-76_email-343.md` | moi j y vais pas j ai pas ete invité et en fait je savais pas qu elle le faisias baptiser bonjo… |
| `pq-31` | pdf-3 p.2 | **0.60** | 46,47,49,52,55,73,76 | `legal/analyse/Responsabilité Déonthologique/2015 avril, aout.md` | notre cliente réitère son offre à l'élargissement des droits d'accès du père auprès de leurs en… |
| `eq-187` | email-56 | **0.60** | 67 | `legal/piece_thread-44_email-56.md` | salut catherine je dois rester avec ma fille cet avant midi je rentrerai au travail cet apres m… |

### Détail (citation en base vs extrait du .md)

#### `pq-96` — pdf-5 p.2 — taux 1.00 — `legal/piece_pdf-5.md`

- **en base :**

  ```text
  Toutefois, puisque le père refuse de prendre les décisions importantes eu égard aux enfants il consent à ce que la mère prenne seule toutes les décisions les concernant et qu'elle signe seule toutes les autorisations nécessaires reliées à l'éducation, la santé, les soins médicaux, les passeports des enfants mineurs;
  ```

- **dans le `.md` :**

  ```text
  questions d'importance concernant l'éducation la santé les soins médicaux le bien-être des enfants le choix des écoles et ce dans le meilleur intérêt des enfants 3 toutefois puisque le père […] seule toutes les décisions les concernant et qu'elle signe seule toutes les autorisations nécessaires reliées à l'éducation la santé les soins médicaux les passeports des enfants mineurs 4 de plus
  ```

#### `pq-95` — pdf-5 p.2 — taux 1.00 — `legal/analyse/Responsabilité civile/requete 21 octobre 2019/analyse preliminaire - echec negociations 2015 et paragraphe 3.md`

- **en base :**

  ```text
  Les parties continueront d'exercer conjointement l'autorité parentale à l'égard des enfants mineurs et, sans limiter la généralité de ce qui précède, ils se consulteront sur toutes les questions d'importance concernant l'éducation, la santé, les soins médicaux, le bien-être des enfants, le choix des écoles, et ce dans le meilleur intérêt des enfants;
  ```

- **dans le `.md` :**

  ```text
  projet de consentement les parties continueront d'exercer conjointement l'autorité parentale à l'égard des enfants mineurs et sans limiter la généralité de ce qui précède ils se consulteront sur toutes les questions d'importance concernant l'éducation la santé les soins médicaux le bien-être des enfants le choix des écoles et ce dans le meilleur intérêt des enfants piece_pdf-5 md piece_pdf-5
  ```

#### `pq-94` — pdf-5 p.1 — taux 1.00 — `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/03_concordance_aout_novembre_2015.md`

- **en base :**

  ```text
  les enfants ne font pas l'objet d'une décision de la Cour du Québec, chambre de la jeunesse, ni d'une entente avec le directeur de la protection de la jeunesse;
  ```

- **dans le `.md` :**

  ```text
  novembre p-19 affirme les enfants ne font pas l'objet d'une décision de la cour du québec chambre de la jeunesse ni d'une instance en cours ni d'une entente avec le […] ce qu'une véritable comparaison août-novembre pourrait établir p-16 affirme que les enfants ne font l'objet ni d'une décision de la chambre de la jeunesse ni d'une entente avec le directeur
  ```

#### `pq-92` — pdf-5 p.3 — taux 1.00 — `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md`

- **en base :**

  ```text
  À compter de ce jour jusqu'au 28 août 2016 : Semaine 1 De samedi 10h30 (directement à la piscine) à Dimanche 20h00; Semaine 2 Dimanche 16h00 à Mardi matin directement à l'école et/ou la garderie;
  ```

- **dans le `.md` :**

  ```text
  première phase a à compter de ce jour jusqu'au 28 août 2016 semaine 1 de samedi 10h30 directement à la piscine à dimanche 20h00 semaine 2 dimanche 16h00 à mardi matin directement à l'école et ou la garderie pièce p-16 art
  ```

#### `pq-91` — pdf-5 p.1 — taux 1.00 — `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/01_inexecution_plan_cohabitation.md`

- **en base :**

  ```text
  ATTENDU QUE le demandeur visite les enfants uniquement quelques heures les dimanches;
  ```

- **dans le `.md` :**

  ```text
  cette dite date attendu que le demandeur visite les enfants uniquement quelques heures les dimanches - p-16 fiche
  ```

#### `pq-69` — pdf-1 p.1 — taux 1.00 — `legal/allegation_stmt13_ete2013.md`

- **en base :**

  ```text
  [...] Tu dois le faire sortir de la maison [...]
  ```

- **dans le `.md` :**

  ```text
  à la demanderesse tu dois le faire sortir de la maison avant de penser
  ```

#### `pq-67` — pdf-6 p.2 — taux 1.00 — `legal/piece_pdf-6.md`

- **en base :**

  ```text
  En ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse;
  ```

- **dans le `.md` :**

  ```text
  toutes les décisions en ce qui concerne les enfants c le paragraphe 4 devra être reformulé afin que les deux parents consentent et s'autorisent mutuellement à ce que les enfants […] mercredis et jeudis notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse e en ce
  ```

#### `pq-66` — pdf-6 p.2 — taux 1.00 — `legal/piece_pdf-6.md`

- **en base :**

  ```text
  Cependant, il souhaite ajouter un sous-paragraphe « e) » afin de prévoir qu'à compter du 7 février 2016 l'horaire de garde sera en alternance 2-2-3/2-2-3.
  ```

- **dans le `.md` :**

  ```text
  auprès des enfants cependant il souhaite ajouter un sous-paragraphe e afin de prévoir qu'à compter du 7 février 2016 l'horaire de garde sera en alternance 2-2-3 2-2-3 en ce qui
  ```

#### `pq-64` — pdf-1 p.1 — taux 1.00 — `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md`

- **en base :**

  ```text
  [...] le meilleur moment pour lui envoyer la procédure est jeudi pour qu'on aille à la cour vendredi avant son départ. Une pierre deux coups. La procédure et tu lui gâche ses vacances [...]
  ```

- **dans le `.md` :**

  ```text
  protection des enfants le meilleur moment pour lui envoyer la procédure est jeudi pour qu'on aille à la cour vendredi avant son départ une pierre deux coups la procédure et tu lui gâche ses vacances comme il te
  ```

#### `pq-63` — pdf-1 p.1 — taux 1.00 — `legal/allegation_stmt62_separation_2011.md`

- **en base :**

  ```text
  [...] Tu veux avoir la garde et lui puisse voir les enfants plusieurs fois par semaine [...]
  ```

- **dans le `.md` :**

  ```text
  semaine sur deux tu veux avoir la garde et lui puisse voir les enfants plusieurs fois par semaine 2 le 11
  ```

#### `pq-62` — pdf-1 p.1 — taux 1.00 — `legal/allegation_stmt14_15_16_17_garde_partagee.md`

- **en base :**

  ```text
  [...] Pendant toute cette procédure les enfants sont avec toi. Donc, cela créé un précédant, c'est à dire une routine s'instaure entre toi et les enfants et souvent ce qui fonctionne bien les juges hésitent à les changer. [...]
  ```

- **dans le `.md` :**

  ```text
  à la demanderesse pendant toute cette procédure les enfants sont avec toi donc cela créé un précédant c'est à dire une routine s'instaure entre toi et les enfants et souvent ce qui fonctionne bien les juges hésitent à les changer pdfdocument id 1
  ```

#### `pq-61` — pdf-1 p.1 — taux 1.00 — `legal/allegation_stmt14_15_16_17_garde_partagee.md`

- **en base :**

  ```text
  [...] on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser [...]
  ```

- **dans le `.md` :**

  ```text
  procédural à suivre on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser pdfdocument id 1
  ```

#### `pq-58` — pdf-1 p.1 — taux 1.00 — `legal/allegation_stmt62_separation_2011.md`

- **en base :**

  ```text
  [...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis.[...]
  ```

- **dans le `.md` :**

  ```text
  à élise ayoub alexia vie dans la violence conjugale depuis sa naissance tout intervenant de la dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis 7 dans ce
  ```

#### `pq-57` — pdf-1 p.1 — taux 1.00 — `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/11_memoire_argumentative_verrouillee_continuite_P2_P19.md`

- **en base :**

  ```text
  Je t'écris comme si tu étais une cliente à laquelle je donnais conseil. [...]
  ```

- **dans le `.md` :**

  ```text
  deux conditionnels contrefactuels je t'écris comme si tu étais une cliente à laquelle je donnais conseil et si j'étais
  ```

#### `pq-55` — pdf-1 p.1 — taux 1.00 — `legal/analyse/Responsabilité Déonthologique/2013 juin.md`

- **en base :**

  ```text
  [...] Si j'étais ton avocate le plan serait le suivant: faire une requête pour garde exclusive d'urgence, et usage exclusif de la résidence familiale. En urgence on appelle cela une ordonnance de sauvegarde. Lors de cette procédure d'urgence le juge en question n'entend pas de témoin
  ```

- **dans le `.md` :**

  ```text
  donnais conseil et si j'étais ton avocate le plan serait le suivant qualification professionnelle et secret professionnel trois qualifications sont possibles échange purement personnel consultation juridique professionnelle légitime ou conseil […] exclusif de la résidence familiale en urgence on appelle cela une ordonnance de sauvegarde lors de cette procédure d'urgence le juge en question n'entend pas de témoin c'est seulement les
  ```

#### `pq-34` — pdf-1 p.1 — taux 1.00 — `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/03_anteriorite_preference_et_fonction_du_registre.md`

- **en base :**

  ```text
  [...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Tu dois le faire sortir de la maison [...]
  ```

- **dans le `.md` :**

  ```text
  à se relocaliser tu dois le faire sortir de la maison mécanisme de conversion la routine créée pendant la procédure opposable ensuite pendant toute cette procédure les enfants sont avec […] la violence conjugale depuis sa naissance tout intervenant de la dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis tu dois le faire sortir de
  ```

#### `pq-28` — pdf-6 p.2 — taux 1.00 — `legal/piece_pdf-6.md`

- **en base :**

  ```text
  notre client est tout à fait disposé à établir une progression dans les droits d'accès auprès des enfants. Cependant, il souhaite ajouter un sous-paragraphe « e) » afin de prévoir qu'à compter du 7 février 2016 l'horaire de garde sera en alternance 2-2-3/2-2-3. En ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse;
  ```

- **dans le `.md` :**

  ```text
  toutes les décisions en ce qui concerne les enfants c le paragraphe 4 devra être reformulé afin que les deux parents consentent et s'autorisent mutuellement à ce que les enfants […] mercredis et jeudis notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse e en ce
  ```

#### `pq-21` — pdf-1 p.1 — taux 1.00 — `legal/analyse/Responsabilité Déonthologique/2013 juin.md`

- **en base :**

  ```text
  (...) on l'oblige également à payer 50% des charges afférentes à la maison. On peut également demander une pension alimentaire qui prendra en considération ce que monsieur doit payer à savoir l'hypothèque et tout le reste.
  ```

- **dans le `.md` :**

  ```text
  se relocaliser et on l'oblige également à payer 50 des charges afférentes à la maison on peut également demander une pension alimentaire qui prendra en considération ce que monsieur doit payer à savoir l'hypothèque et tout le reste et on peut
  ```

#### `pq-20` — pdf-1 p.1 — taux 1.00 — `legal/analyse/Responsabilité Déonthologique/2013 juin.md`

- **en base :**

  ```text
  (...) on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser et on l'oblige également à payer 50% des charges afférentes à la maison. On peut également demander une pension alimentaire qui prendra en considération ce que monsieur doit payer à savoir l'hypothèque et tout le reste.
  ```

- **dans le `.md` :**

  ```text
  un jugement temporaire on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser pendant toute cette procédure les enfants sont avec toi donc cela créé un […] afférentes à la maison on peut également demander une pension alimentaire qui prendra en considération ce que monsieur doit payer à savoir l'hypothèque et tout le reste et on peut
  ```

#### `pq-16` — pdf-11 p.1 — taux 1.00 — `legal/piece_pdf-11.md`

- **en base :**

  ```text
  Étude de la valeur marchande en date des présentes à des fins de partage
  ```

- **dans le `.md` :**

  ```text
  rapport d'évaluation marchande à des fins de partage référence base de données - modèle id pdf_manager pdfdocument id 11 - titre étude de la valeur marchande à des fins de […] - propriété de louis-philippe david et élise-marie ayoub - fins du rapport verbatim page 1 étude de la valeur marchande en date des présentes à des fins de partage chronologie
  ```

#### `pq-14` — pdf-6 p.2 — taux 1.00 — `legal/piece_pdf-6.md`

- **en base :**

  ```text
  En ce qui concerne les périodes de garde où votre cliente serait avec les enfants, soit les lundis et mardis ou les mercredis et jeudis, notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse;
  ```

- **dans le `.md` :**

  ```text
  toutes les décisions en ce qui concerne les enfants c le paragraphe 4 devra être reformulé afin que les deux parents consentent et s'autorisent mutuellement à ce que les enfants […] mercredis et jeudis notre client est tout à fait disposé à laisser votre cliente choisir afin que l'horaire de garde prenne en considération ses cours de danse e en ce
  ```

#### `eq-209` — email-238 — taux 1.00 — `legal/piece_chatsequence-1.md`

- **en base :**

  ```text
  Quand je suis arrêtée je tombe à 80% de mon salaire en passant.
  ```

- **dans le `.md` :**

  ```text
  janv 2016 - quand je suis arrêtée je tombe à 80 de mon salaire en passant emailthread pk 12
  ```

#### `eq-203` — email-180 — taux 1.00 — `legal/piece_thread-ecrement_2015.md`

- **en base :**

  ```text
  Bon matin Mme Écremment, je ne pourais pas ce soir, de plus, je souhaites annuler mon rendez vous du 19. Je suis bien heureux que mes enfants aient pu profiter de vos services.
  ```

- **dans le `.md` :**

  ```text
  utc 07 51 bon matin mme écremment je ne pourais pas ce soir de plus je souhaites annuler mon rendez vous du 19 je suis bien heureux que mes enfants aient pu profiter de vos services cordialement lp 11
  ```

#### `eq-183` — email-53 — taux 1.00 — `legal/faits_chronologiques_2010-11-20_2012-02-06.md`

- **en base :**

  ```text
  Good morning my daughter is sick and i'll be staying at home today with her
  ```

- **dans le `.md` :**

  ```text
  qu'alexia est malade good morning my daughter is sick and i'll be staying at home today with her emails id 53
  ```

#### `eq-180` — email-64 — taux 1.00 — `legal/faits_chronologiques_2010-11-20_2012-02-06.md`

- **en base :**

  ```text
  Good morning i won't be coming in today i have to stay with my daughter. She is sick and must go to the doctor.
  ```

- **dans le `.md` :**

  ```text
  à son employeure good morning i won't be coming in today i have to stay with my daughter she is sick and must go to the doctor email id 64
  ```

#### `eq-175` — email-352 — taux 1.00 — `legal/journal_ete2013.md`

- **en base :**

  ```text
  Pour la moitié oui sur ma marge! Ça en vaudrait la peine!! Le 14 octobre aussi c'est pas cher
  ```

- **dans le `.md` :**

  ```text
  de l'argent élise pour la moitié oui sur ma marge ça en vaudrait la peine le 14 octobre aussi c'est pas cher les deux parents
  ```

#### `eq-170` — email-355 — taux 1.00 — `legal/piece_thread-83_email-355.md`

- **en base :**

  ```text
  Direction Loisirs, culture et vie communautaire
  600, avenue Oak, Saint-Lambert
  ```

- **dans le `.md` :**

  ```text
  verbatim intégral text direction loisirs culture et vie communautaire 600 avenue oak saint-lambert province de québec
  ```

#### `eq-161` — email-445 — taux 1.00 — `legal/piece_thread-109.md`

- **en base :**

  ```text
  Pendant ces 2 nuit Alexia n eatit pas inquiete etait tres heureuse. C est aussi normale qu elle s ennuit de toi. Moi aussi elle me dis que je lui manque, elle me demande quand je vais rentrer.
  ```

- **dans le `.md` :**

  ```text
  07 46 edt pendant ces 2 nuit alexia n eatit pas inquiete etait tres heureuse c est aussi normale qu elle s ennuit de toi moi aussi elle me dis que je lui manque elle me demande quand je vais rentrer nous n allons
  ```

#### `eq-135` — email-475 — taux 1.00 — `legal/piece_thread-116_email-475.md`

- **en base :**

  ```text
  Pour ce qui est de la garde, je ne peux accepter les termes proposés par
  Élise. La raison principale est que les enfants n'auront pas le temps de
  s'acclimater a passé seulement une nuit a la maison. Moi je n'aurai pas de
  fds complet avec eux pour faire des activités.
  
  Il faut bien comprendre ici que ce n'est pas parce que je n'accepte pas les
  termes qui me sont proposés que je ne souhaite pas m'acquitter de mes
  obligations parentales.
  ```

- **dans le `.md` :**

  ```text
  des obligations parentales pour ce qui est de la garde je ne peux accepter les termes proposés par élise la raison principale est que les enfants n'auront pas le temps […] comprendre ici que ce n'est pas parce que je n'accepte pas les termes qui me sont proposés que je ne souhaite pas m'acquitter de mes obligations parentales portée le courriel
  ```

#### `eq-131` — email-330 — taux 1.00 — `legal/piece_thread-4_email-330.md`

- **en base :**

  ```text
  J'arrives à la fin de mes économies, a la fin de mon bail, de toute
  évidence je ne peux pas partir pour travailler et je ne me suis pas trouvé
  d'emplois à 65k/année.
  
  Il va être temps de finaliser notre entente, je suis prêt à plaider
  coupable pour outrage au tribunal, mais je compte sur vous pour en faire la
  demande.
  ```

- **dans le `.md` :**

  ```text
  intégral salut mj j'arrives à la fin de mes économies a la fin de mon bail de toute évidence je ne peux pas partir pour travailler et je ne me […] va être temps de finaliser notre entente je suis prêt à plaider coupable pour outrage au tribunal mais je compte sur vous pour en faire la demande je penses que
  ```

#### `eq-127` — email-456 — taux 1.00 — `legal/piece_thread-111_congediement_bnc.md`

- **en base :**

  ```text
  ... suite au constat que vous ne répondez malheureusement pas aux attentes de votre poste.
  ```

- **dans le `.md` :**

  ```text
  lp ne répond pas aux attentes de son poste de l'étoile 8 juin 2018 la période de relocalisation est un choix qui vous a été offert comme option alternative au plan d'accompagnement qui a été débuté suite au constat que vous ne répondez malheureusement pas aux attentes de votre poste si vous refusez
  ```

#### `eq-126` — email-4 — taux 1.00 — `legal/inventaire_incompatibilites.md`

- **en base :**

  ```text
  Nous avons procédé devant un juge, tu as plaidé ta cause et nous la nôtre.  Il y a eu un jugement final et non pas une entente.
  ```

- **dans le `.md` :**

  ```text
  ayoub avril 2020 nous avons procédé devant un juge tu as plaidé ta cause et nous la nôtre il y a eu un jugement final et non pas une entente - thread-4 email-4
  ```

#### `eq-125` — email-448 — taux 1.00 — `legal/piece_thread-109.md`

- **en base :**

  ```text
  [...] Je ne souhaite pas aller en cours, mais tu comprends que l enjeux est enorme, [...]
  ```

- **dans le `.md` :**

  ```text
  de la chose je ne souhaite pas aller en cours mais tu comprends que l enjeux est enorme je n ai
  ```

#### `eq-124` — email-447 — taux 1.00 — `legal/piece_thread-109.md`

- **en base :**

  ```text
  [...] Ce que je comprends de ce que tu m'offre c est 
  
  - tu va pouvoir faire les choses que tu veux faire avec ta fille quand je vais etre en confiance que tu vas etre en mesure de repondre a ses besoins.
  
  Tu me juge comme inadequat comme parent, [...]
  ```

- **dans le `.md` :**

  ```text
  ca plus longtemps ce que je comprends de ce que tu m'offre c est - tu va pouvoir faire les choses que tu veux faire avec ta fille quand je vais etre en confiance que tu vas etre en mesure de repondre a ses besoins tu me juge comme inadequat comme parent c est certain
  ```

#### `eq-122` — email-6 — taux 1.00 — `legal/allegation_stmt14_15_16_17_garde_partagee.md`

- **en base :**

  ```text
  [...] Je ne t'ai jamais traiter d'incapable je t'ai parlé de leur lien d'attachement, je ne t'ai jamais accusé de rien depuis que tu es parti [...]
  ```

- **dans le `.md` :**

  ```text
  tard elle écrit je ne t'ai jamais traiter d'incapable je t'ai parlé de leur lien d'attachement je ne t'ai jamais accusé de rien depuis que tu es parti email id 6
  ```

#### `eq-109` — email-296 — taux 1.00 — `legal/piece_thread-6_reconstruction.md`

- **en base :**

  ```text
  [...] n'assumes pas ce que j'aurais été en mesure d'accepter. Si je ne m'étais pas occupé de mes enfants je ne me serais jamais mise dans une position d'exiger quoi que ce soit, j'aurais pris le temps de corriger mes erreurs et de prendre mes responsabilités.
  ```

- **dans le `.md` :**

  ```text
  moi n'y pouvons quoi que ce soit en espèrant que tu ne te soit pas trompé 17 35 utc - élise email-305 lp les enfants veulent te voir et je […] je ne me serais jamais mise dans une position d'exiger quoi que ce soit j'aurais pris le temps de corriger mes erreurs et de prendre mes responsabilités on est tous
  ```

#### `eq-98` — email-171 — taux 1.00 — `legal/allegation_stmt4_5_6.md`

- **en base :**

  ```text
  [...] Nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année, nous ne faisions pas chambre à part et nous avions des activités communes [...]
  ```

- **dans le `.md` :**

  ```text
  id 167 - nous étions conjoints de fait par définition jusqu'à la rupture faite en février de cette année nous ne faisions pas chambre à part et nous avions des activités communes id 171 -
  ```

#### `eq-97` — email-167 — taux 1.00 — `legal/allegation_stmt4_5_6.md`

- **en base :**

  ```text
  [...]  je ne te considérais pas comme mon coloc [...]
  ```

- **dans le `.md` :**

  ```text
  la relation - je ne te considérais pas comme mon coloc id 167 -
  ```

#### `eq-74` — email-349 — taux 1.00 — `legal/piece_thread-109.md`

- **en base :**

  ```text
  Ce que je comprends de ce que tu m'offre c est
  >> 
  >> - tu va pouvoir faire les choses que tu veux faire avec ta fille quand je vais etre en confiance que tu vas etre en mesure de repondre a ses besoins.
  >> 
  >> Tu me juge comme inadequat comme parent
  ```

- **dans le `.md` :**

  ```text
  ca plus longtemps ce que je comprends de ce que tu m'offre c est - tu va pouvoir faire les choses que tu veux faire avec ta fille quand je vais etre en confiance que tu vas etre en mesure de repondre a ses besoins tu me juge comme inadequat comme parent c est certain
  ```

#### `eq-73` — email-48 — taux 1.00 — `legal/axe_agenda_danse_elise.md`

- **en base :**

  ```text
  je sais que je dois etre a la maison de bonne heure ce soir parceque tu
  danses,
  ```

- **dans le `.md` :**

  ```text
  347 lp élise je sais que je dois etre a la maison de bonne heure ce soir parceque tu danses 16 2013-02-09 10
  ```

#### `eq-59` — email-347 — taux 1.00 — `legal/piece_thread-78_email-347.md`

- **en base :**

  ```text
  Ce matin je me suis reveille tot, je suis partis parceque je sais que je dois etre a la maison de bonne heure ce soir parceque tu danses,
  ```

- **dans le `.md` :**

  ```text
  parce qu'élise danse ce matin je me suis reveille tot je suis partis parceque je sais que je dois etre a la maison de bonne heure ce soir parceque tu danses le message rattache
  ```

#### `eq-57` — email-29 — taux 1.00 — `legal/piece_thread-23_email-148.md`

- **en base :**

  ```text
  Veux tu en profiter pour fêter Alexia. (Nicolas voulait aller te voir hier, quand je suis aller le chercher à la garderie)
  ```

- **dans le `.md` :**

  ```text
  com a écrit veux tu en profiter pour fêter alexia nicolas voulait aller te voir hier quand je suis aller le chercher à la garderie 2014-09-16 12 25
  ```

#### `eq-37` — email-48 — taux 1.00 — `legal/piece_thread-78_email-347.md`

- **en base :**

  ```text
  Je t'ai ecris que je partais tot, je t'ai offert, avec beinveillance et bonne volonté, de m'occuper d'alexia pour que tu puisse partir du travail plus tard pour que tu puisse egalement partir de la maison plus tard,
  ```

- **dans le `.md` :**

  ```text
  alexia en charge je t'ai ecris que je partais tot je t'ai offert avec beinveillance et bonne volonté de m'occuper d'alexia pour que tu puisse partir du travail plus tard pour que tu puisse egalement partir de la maison plus tard le passage établit
  ```

#### `eq-22` — email-51 — taux 1.00 — `legal/piece_thread-40_email-50.md`

- **en base :**

  ```text
   Hi i have to stay home again today my mother in law can t come in. You ll bebable tomreach me at home, Thanks
  ```

- **dans le `.md` :**

  ```text
  catherine subject today hi i have to stay home again today my mother in law can t come in you ll bebable tomreach me at home thanks confidentialit ce document
  ```

#### `eq-15` — email-349 — taux 1.00 — `legal/piece_thread-109.md`

- **en base :**

  ```text
  Elise les 2 chemins ne mene pas au meme resultat avec Alexia, pas du tout. Tout ce que je veux c est de pouvoir aller passer des fds au chalet avec. Je t ai aussi dit qu avec toi nous pouvons aller en therapie. Je suis pret a recomencer le processus, avec un autre therapeut. La semaine prochaine si tu veux.
  ```

- **dans le `.md` :**

  ```text
  08 48 edt elise les 2 chemins ne mene pas au meme resultat avec alexia pas du tout tout ce que je veux c est de pouvoir aller passer des […] aussi dit qu avec toi nous pouvons aller en therapie je suis pret a recomencer le processus avec un autre therapeut la semaine prochaine si tu veux en tk nous
  ```

#### `eq-7` — email-33 — taux 1.00 — `legal/piece_thread-26_emails-33-32.md`

- **en base :**

  ```text
   Si tu viens demain.avec Nicholas on passera che Josée puis ru prendras la vignettes
  ```

- **dans le `.md` :**

  ```text
  nicolas johanne écrit si tu viens demain avec nicholas on passera che josée puis ru prendras la vignettes la formulation ne
  ```

#### `eq-54` — email-7 — taux 0.98 — `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/01_architecture_justificative_stabilite.md`

- **en base :**

  ```text
  j'étais tout le temps à la maison. Tu vas honnêtement venir me dire que
  pendant tout ce temps passer a la maison j'etais assis dans le divan a
  écouter la TV pendant que tu t'occupait des enfants, tu preparais le
  souper, tu les faisais manger, tu leurs donnait le bain, tu les couchais
  seules et une fois couché tu faisias le menage, tu plait le linge et tu le
  faisias avec le sourir. Quand les enfants avaient des cours, tu les prenaient les 2 et moi je
  restait a la maison et me saoulais pendant ce temps la. Quand tu allais a tes cours de dance le soir, auxquels tu allais de une a
  trois fois semaine, tu amenais les enfants chez tes soeurs pendant
  qu'encore une fois je me saoulais. tu allais chercher et porter les enfants a la garderie tout les soirs et
  tout les matins.
  ```

- **dans le `.md` :**

  ```text
  je m'excuses mais j'étais tout le temps à la maison tu vas honnêtement venir me dire que pendant tout ce temps passer a la maison j'etais assis dans le divan […] chez tes soeurs pendant qu'encore une fois je me saoulais tu allais chercher et porter les enfants a la garderie tout les soirs et tout les matins je veux dire
  ```

#### `eq-42` — email-116 — taux 0.97 — `legal/piece_thread-52_emails-66-115-116.md`

- **en base :**

  ```text
  salut ce soir elise ne va pas a son premier cour de danse je sais pas a quelle heure elle va partit je t'appel si c est pas trops tard sinon on se vois demain
  ```

- **dans le `.md` :**

  ```text
  danse lp répond ce soir elise ne va pas a son premier cour de danse je sais pas a quelle heure elle va partit je t'appel si c est pas trops tard sinon on se vois demain la formulation ne
  ```

#### `pq-5` — pdf-1 p.1 — taux 0.95 — `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/03_anteriorite_preference_et_fonction_du_registre.md`

- **en base :**

  ```text
  faire une requête pour garde exclusive d'urgence, et usage exclusif de la résidence familiale ... on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser  ... Pendant toute cette procédure les enfants sont avec toi. Donc, cela créé un précédant, c'est à dire une routine s'instaure entre toi et les enfants et souvent ce qui fonctionne bien les juges hésitent à les changer.
  ```

- **dans le `.md` :**

  ```text
  juges à modifier ce qui fonctionne bien une fois cette réalité nouvellement créée pour obtenir la garde recherchée 2 les trois positions et leur relation le courriel ne comporte pas […] cela créé un précédant c'est à dire une routine s'instaure entre toi et les enfants et souvent ce qui fonctionne bien les juges hésitent à les changer le document marque
  ```

#### `eq-132` — email-462 — taux 0.95 — `legal/piece_thread-113_email-462.md`

- **en base :**

  ```text
  Salut MJ, suite au dernier jugement mon compte de banque a été saisie il y a environ 2 semaines et la d'ici 30 jours mon passeport sera annulé, ce qui évidemment m'empêchera d'aller travailler, penses-tu qu'il est possible de faire quelque chose
  ```

- **dans le `.md` :**

  ```text
  verbatim défendeur email-462 suite au dernier jugement mon compte de banque a été saisie il y a environ 2 semaines et la d'ici 30 jours mon passeport sera annulé ce qui évidemment m'empêchera d'aller travailler penses-tu qu'il est possible de faire quelque chose me ayoub email-463
  ```

#### `eq-61` — email-116 — taux 0.95 — `legal/piece_thread-52_emails-66-115-116.md`

- **en base :**

  ```text
  salut ce soir elise ne va pas a son premier cour de danse je sais pas a quelle heure elle va partit
  ```

- **dans le `.md` :**

  ```text
  danse lp répond ce soir elise ne va pas a son premier cour de danse je sais pas a quelle heure elle va partit je t'appel si
  ```

#### `eq-94` — email-7 — taux 0.94 — `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/01_architecture_justificative_stabilite.md`

- **en base :**

  ```text
  [...] Je n'ai pas décider de ne pas m'en occuper 50% du temps, je m'excuses mais j'étais tout le temps à la maison. [...] Tu vas honnêtement venir me dire que pendant tout ce temps passer a la maison [...] tu allais chercher et porter les enfants a la garderie tout les soirs et tout les matins.
  ```

- **dans le `.md` :**

  ```text
  ne pas s'en occuper 50 du temps peut viser la conduite postérieure à la séparation il confirme l'emploi du seuil quantitatif mais ne doit pas servir seul à qualifier l'implication […] chez tes soeurs pendant qu'encore une fois je me saoulais tu allais chercher et porter les enfants a la garderie tout les soirs et tout les matins je veux dire
  ```

#### `eq-2` — email-40 — taux 0.93 — `legal/piece_thread-32_email-40.md`

- **en base :**

  ```text
  Salut Karl, je vais rester a la maison aujourd hui pour aider ma conjointe avec le bebe, elle ne se sent pas tres bien et ma belle mere n' est pas dsiponible
  ```

- **dans le `.md` :**

  ```text
  congė verbatim pertinent je vais rester a la maison aujourd hui pour aider ma conjointe avec le bebe elle ne se sent pas tres bien et ma belle mere n' est pas dsiponible portée probatoire -
  ```

#### `eq-34` — email-87 — taux 0.93 — `legal/piece_emails_petite_enfance_2010.md`

- **en base :**

  ```text
  Salut Oui viens garder vendredi si tu peux, confirme moi pour que j'avertisse la mere à elise !!
  ```

- **dans le `.md` :**

  ```text
  email id 87 oui viens garder vendredi si tu peux confirme moi pour que j'avertisse la mere à elise johanne lp 12
  ```

#### `eq-182` — email-59 — taux 0.92 — `legal/piece_thread-46_emails-58-59.md`

- **en base :**

  ```text
  j'ai essayer de convaincre ma copine que tu avais plus besoins de moi que ma fille mais en vains je resterai donc a la maison avec elle, si jamais il y avait une urgence vous pouvez me rejoindre au 514-550-2998
  ```

- **dans le `.md` :**

  ```text
  lp j ai essayer de convaincre ma copine que tu avais plus besoins de moi que ma fille mais en vains je resterai donc a la maison avec elle si jamais il y avait une urgence vous pouvez me rejoindre catherine liepins j'espere
  ```

#### `eq-28` — email-30 — taux 0.92 — `legal/piece_thread-24_email-30.md`

- **en base :**

  ```text
  Salut Karl, je vais à la clinique ce matin avec mon gars et en fonction de ce qu'ils me disent, je vais rester ici ou rentrer travailler!
  ```

- **dans le `.md` :**

  ```text
  maladie verbatim pertinent je vais à la clinique ce matin avec mon gars et en fonction de ce qu'ils me disent je vais rester ici ou rentrer travailler portée probatoire -
  ```

#### `eq-35` — email-86 — taux 0.91 — `legal/piece_emails_petite_enfance_2010.md`

- **en base :**

  ```text
  Salut, Peux tu arriver vers 7hre - 7h15 demain, j'ai une entrevue chez hydro qubec a 8h30 et je dois prendre le train de 7h30 Merci !
  ```

- **dans le `.md` :**

  ```text
  email id 86 peux tu arriver vers 7hre - 7h15 demain j'ai une entrevue chez hydro qubec a 8h30 et je dois prendre le train de 7h30 contexte le demandeur
  ```

#### `eq-208` — email-404 — taux 0.91 — `legal/piece_thread-100_email-404.md`

- **en base :**

  ```text
  Dernière chose, est il possible dans l entente que je demande de ne plus avoir a donner mon consentement pour que les enfants partent a l étranger. Je veux que la mère puisse exercer l autorité parentale La mère sans avoir a me demander la permission pour tout
  ```

- **dans le `.md` :**

  ```text
  david transcription utile dernière chose est il possible dans l entente que je demande de ne plis avoir a donner mon consentement pour que les enfants partent a l étranger je veux que la mère puisse exercer l autorité parentale la mère sans avoir a me demander la permission pour tout portée - le
  ```

#### `eq-69` — email-373 — taux 0.91 — `legal/piece_emails_cape_cod_2012.md`

- **en base :**

  ```text
  J'ai repensé à Alexia et en ai discuté avec ton père. Si tu as envie de l'amener, ca nous permettrait de passer du temps avec elle. [...] On peut aller à la plage de 9 heures à 11H30 puis aller dîner à la maison, faire la sieste et retourner à la plage vers 3 ou 4 heures - jusqu'au souper à la maison.  Elle aura peut-être à déroger un peu de son horaire mais ça va pas la déranger terriblement.  Après deux jours,elle sera habituée et je pourrai la garder si vous partez en vélo ou même le soir si toi, hugo et ta soeur voulez sortir.  Je pense que ca peut se faire et que ce serait le fun.
  ```

- **dans le `.md` :**

  ```text
  johanne bazinet lp j'ai repensé à alexia et en ai discuté avec ton père si tu as envie de l'amener ça nous permettrait de passer du temps avec elle pour […] en vélo ou même le soir si toi hugo et ta soeur voulez sortir je pense que ça peut se faire et que ce serait le fun 2 374 2012-07-19
  ```

#### `eq-68` — email-49 — taux 0.90 — `legal/piece_emails_cape_cod_2012.md`

- **en base :**

  ```text
  Je t'envoie trois possibilités de maisons à Cape Cod - je m'attends à ce
  qu'Élise ne soit pas d'accord. [...] si ça marche pas cette année, ce sera plus tard lorsque A sera
  plus grande.
  ```

- **dans le `.md` :**

  ```text
  johanne bazinet lp je t'envoie trois possibilités de maisons à cape cod - je m'attends à ce qu'élise ne soit pas d'accord - c'est pas moi qui va mettre de […] une maison que vous louerez avec des amis ce sont des suggestions si ça marche pas cette année ce sera plus tard lorsque a sera plus grande --- thread 93
  ```

#### `eq-107` — email-285 — taux 0.90 — `legal/piece_thread-6_reconstruction.md`

- **en base :**

  ```text
  Donc tu m'as condamnée car je n'étais pas d'accord avec toi [...] Donc si on n'est pas d'accord avec toi tu n'as pas notre respect et donc on ne peut pas s'entendre et trouver un compromis? [...] tu leurs dit votre mère n'était pas d'accord avec moi alors je ne voulais plus être votre père? [...] Je suis désolée que tu aies tant de peine, je m'excuse je n'ai jamais voulu ça, je sais que tu as eu mal et cela n'était pas mon intention, je m'excuse que tu aies eu mal et je m'excuse que tu aies eu de la souffrance.
  ```

- **dans le `.md` :**

  ```text
  élise email-308 salut je sais que tu étais dépassé par dimanche dernier mais les enfants étaient fatigués tu n'as pas eu un traitement différent de ce qu'ils sont habituellement ils […] tu as eu mal et cela n'était pas mon intention je m'excuse que tu aies eu mal et je m'excuse que tu aies eu de la souffrance élise 19 28
  ```

#### `pq-26` — pdf-1 p.1 — taux 0.90 — `legal/analyse/Responsabilité civile/courriel 11 juin 2013 - responsabilite de Me Ayoub.md`

- **en base :**

  ```text
  Je t'écris comme si tu étais une cliente à laquelle je donnais conseil. [...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. Si j'étais ton avocate le plan serait le suivant: faire une requête pour garde exclusive d'urgence, et usage exclusif de la résidence familiale. [...] on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser [...] Pendant toute cette procédure les enfants sont avec toi. Donc, cela créé un précédant, c'est à dire une routine s'instaure entre toi et les enfants et souvent ce qui fonctionne bien les juges hésitent à les changer. [...] le meilleur moment pour lui envoyer la procédure est jeudi pour qu'on aille à la cour vendredi avant son départ. Une pierre deux coups. La procédure et tu lui gâche ses vacances [...]
  ```

- **dans le `.md` :**

  ```text
  le document ainsi je t'écris comme si tu étais une cliente à laquelle je donnais conseil elle introduit ensuite le mécanisme si j'étais ton avocate le plan serait le suivant […] - une procédure où le juge en question n'entend pas de témoin - on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser et on l'oblige
  ```

#### `pq-25` — pdf-1 p.1 — taux 0.89 — `legal/analyse/Responsabilité Déonthologique/2013 juin.md`

- **en base :**

  ```text
  Je t'écris comme si tu étais une cliente à laquelle je donnais conseil. [...] Alexia vie dans la violence conjugale depuis sa naissance. tout intervenant de la Dpj pourra arriver à la conclusion que sa sécurité et son développement sont compromis. [...] Si j'étais ton avocate le plan serait le suivant: faire une requête pour garde exclusive d'urgence, et usage exclusif de la résidence familiale. [...] on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser [...] Pendant toute cette procédure les enfants sont avec toi. Donc, cela créé un précédant, c'est à dire une routine s'instaure entre toi et les enfants et souvent ce qui fonctionne bien les juges hésitent à les changer [...] Tu veux avoir la garde et lui puisse voir les enfants plusieurs fois par semaine.
  ```

- **dans le `.md` :**

  ```text
  les formulations suivantes je t'écris comme si tu étais une cliente à laquelle je donnais conseil et si j'étais ton avocate le plan serait le suivant qualification professionnelle et secret […] documentés communs aux trois tensions le document du 11 juin 2013 formule la qualification suivante alexia vit dans la violence conjugale depuis sa naissance tout intervenant de la dpj pourra
  ```

#### `pq-27` — pdf-3 p.2 — taux 0.88 — `legal/allegation_stmt19_20_21_acces.md`

- **en base :**

  ```text
  nous considérons qu'il y a contre-indication à l'établissement de la garde parlagée des deux (2) enfants mineurs vu leur jeune âge et qu'il n'est pas dans leur intérêt de modifier une routine établie depuis plus deux mois.
  ```

- **dans le `.md` :**

  ```text
  tenu des circonstances nous considérons qu'il y a contre-indication à l'établissement de la garde partagée des deux 2 enfants mineurs vu leur jeune âge et qu'il n'est pas dans leur intérêt de modifier une routine établie depuis plus deux mois pdfdocument id 3
  ```

#### `eq-16` — email-69 — taux 0.88 — `legal/piece_thread-54_emails-68-69.md`

- **en base :**

  ```text
  Bon matin Catherine je dois rester avec ma petite aujourd hui. J'imagine qu il y a des journées prévue pour ca à la banque. Sinon je vais prendre une journée de congé. Merci et bonne journee
  ```

- **dans le `.md` :**

  ```text
  7 mars 2011 bon matin catherine je dois rester avec ma petite aujourd hui j'imagine qu il y a des journées prévue pour ca à la banque sinon je vais prendre une journée de congé lp en réponse
  ```

#### `eq-190` — email-42 — taux 0.88 — `legal/piece_thread-34_email-42.md`

- **en base :**

  ```text
  Bon matin Karl, je ne retrerai pas travailler aujourd hui, je vais rester a la maison avec ma petite qui es malade et qui ne dors pas
  ```

- **dans le `.md` :**

  ```text
  absence verbatim pertinent je ne retrerai pas travailler aujourd hui je vais rester a la maison avec ma petite qui es malade et qui ne dors pas portée probatoire -
  ```

#### `eq-5` — email-34 — taux 0.88 — `legal/piece_thread-27_email-34.md`

- **en base :**

  ```text
  > Bonne fête LP!! Et puis ton party vendredi? C'était cool? Salut Eve, Oui on a eu bien du plaisir, y'avais bcoup d'enfants, de rire et de joie.
  ```

- **dans le `.md` :**

  ```text
  dans le courriel bonne fête lp et puis ton party vendredi c'était cool tu auras compris qu'avec la situation actuelle je n'ai pas pu y aller j'ai annulé ma présence […] un peu mieux avec elise réponse de louis philippe david salut eve oui on a eu bien du plaisir y'avais bcoup d'enfants de rire et de joie ne t'en fait
  ```

#### `pq-17` — pdf-1 p.1 — taux 0.87 — `legal/amendements/01_avant_notification/faits_experimentaux/01_planification_statu_quo_garde.md`

- **en base :**

  ```text
  Je t'écris comme si tu étais une cliente à laquelle je donnais conseil (...) Si j'étais ton avocate le plan serait le suivant: faire une requête pour garde exclusive d'urgence, et usage exclusif de la résidence familiale. (...) on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser...
  ```

- **dans le `.md` :**

  ```text
  lequel elle écrivait je t'écris comme si tu étais une cliente à laquelle je donnais conseil pièce p-2 dans ce courriel me ayoub écrivait alexia vie dans la violence conjugale […] de la résidence et la réduction immédiate de ses contacts avec les enfants on accorde des droits d'accès sans coucher au père et l'oblige à se relocaliser pièce p-2 elle
  ```

#### `eq-188` — email-55 — taux 0.87 — `legal/piece_thread-43_email-55.md`

- **en base :**

  ```text
  Good morning, I have to stay home today with my daugter because she is sick, i will be reacheble all day at my house number 450-550-2998
  ```

- **dans le `.md` :**

  ```text
  objet verbatim pertinent i have to stay home today with my daugter because she is sick i will be reacheble all day at my house number portée probatoire -
  ```

#### `eq-21` — email-53 — taux 0.87 — `legal/piece_thread-123_email-488.md`

- **en base :**

  ```text
  Good morning my daugther is sick and i ll be staying at home today with her, Thanks, Lp
  ```

- **dans le `.md` :**

  ```text
  today verbatim pertinent good morning my daugther is sick and i ll be staying at home today with her concordance et portée
  ```

#### `pq-82` — pdf-13 p.2 — taux 0.86 — `legal/piece_pdf-13.md`

- **en base :**

  ```text
  10h17:04 Le Tribunal informe Monsieur de ne pas parler de ce qui s'est passé avant 2016.
  ```

- **dans le `.md` :**

  ```text
  h 17 - le tribunal informe monsieur de ne pas parler de ce qui s'est passé avant 2016 suite du témoignage
  ```

#### `eq-62` — email-137 — taux 0.85 — `legal/allegation_stmt66_residence_2014.md`

- **en base :**

  ```text
  Le sous sol on l'a démolie suite a une inondation l'année dernière et nous ne l'avons jamais terminé, préférant utiliser l'argent de l'assurance pour changer le système de chauffage.
  ```

- **dans le `.md` :**

  ```text
  choisissant plutôt d'utiliser l'argent de l'assurance pour remplacer le système de chauffage le défendeur écrit en juillet 2013 à son amie ève brunet le sous sol on l'a démolie suite à une inondation l'année dernière et nous ne l'avons jamais terminé préférant utiliser l'argent de l'assurance pour changer le système de chauffage email id
  ```

#### `pq-10` — pdf-3 p.2 — taux 0.84 — `legal/allegation_stmt19_20_21_acces.md`

- **en base :**

  ```text
  il y a contre-indication à l'établissement de la garde parlagée des deux (2) enfants mineurs vu leur jeune âge et qu'il n'est pas dans leur intérêt de modifier une routine établie depuis plus deux mois.
  ```

- **dans le `.md` :**

  ```text
  nous considérons qu'il y a contre-indication à l'établissement de la garde partagée des deux 2 enfants mineurs vu leur jeune âge et qu'il n'est pas dans leur intérêt de modifier une routine établie depuis plus deux mois pdfdocument id 3
  ```

#### `eq-194` — email-21 — taux 0.83 — `legal/piece_thread-17_email-21.md`

- **en base :**

  ```text
  Bonjour, nicolas est malade je reste a la maison
  ```

- **dans le `.md` :**

  ```text
  objet verbatim pertinent nicolas est malade je reste a la maison portée probatoire -
  ```

#### `eq-31` — email-21 — taux 0.83 — `legal/piece_thread-17_email-21.md`

- **en base :**

  ```text
  Bonjour, nicolas est malade je reste a la maison
  ```

- **dans le `.md` :**

  ```text
  objet verbatim pertinent nicolas est malade je reste a la maison portée probatoire -
  ```

#### `pq-11` — pdf-2 p.1 — taux 0.83 — `legal/piece_pdf-2.md`

- **en base :**

  ```text
  [...] au niveau de la garde des deux (2) enfants mineurs, nous ne voyons aucune contre-indication à l’établissement d’une garde partagée et ceci, afin de favoriser un contact optimal entre l’enfant et les deux (2) parents. Compte tenu du jeune âge des enfants, nous croyons qu’il serait opportun d’établir une garde partagée à raison de 2 jours- 2 jours -3 jours, 2 jours- 2 jours- 3 jours.
  ```

- **dans le `.md` :**

  ```text
  un deuxième temps au niveau de la garde des deux 2 enfants mineurs nous ne voyons aucune contre-indication à l'établissement d'une garde partagée et ceci afin de favoriser un contact […] entre l'enfant et les deux 2 parents compte tenu du jeune âge des enfants nous croyons qu'il serait opportun d'établir une garde partagée à raison de 2 jours-2 jours-3 jours
  ```

#### `pq-13` — pdf-7 p.1 — taux 0.82 — `legal/piece_pdf-7.md`

- **en base :**

  ```text
  notre cliente considère qu'il est prématuré à te stade ci d'entrevoir l'aménagement d'une garde partagée dès février 2016. Encore une fois, à cet égard nous avons un discours contradictoire de votre client, puisqu'il refuse de voir les enfants plus de quatre (4) paisemaine.
  ```

- **dans le `.md` :**

  ```text
  des enfants toutefois notre cliente considère qu'il est prématuré à ce stade-ci d'entrevoir l'aménagement d'une garde partagée dès février 2016 encore une fois à cet égard nous avons un discours contradictoire de votre client puisqu'il refuse de voir les enfants plus de quatre 4 heures fois par
  ```

#### `eq-29` — email-28 — taux 0.81 — `legal/piece_thread-22_email-28.md`

- **en base :**

  ```text
  Salut voici le papier du medicine, je vais manquer le CMOC et le dîner d équipe, mais je suis malade et en plus je dois m occuper de mon gars Cordialement, Envoyé de mon iPhone
  ```

- **dans le `.md` :**

  ```text
  objet verbatim pertinent voici le papier du medicine je vais manquer le cmoc et le dîner d équipe mais je suis malade et en plus je dois m occuper de mon gars portée probatoire -
  ```

#### `eq-19` — email-56 — taux 0.81 — `legal/piece_thread-44_email-56.md`

- **en base :**

  ```text
  Salut Catherine je dois rester avec ma fille cet avant midi je rentrerai au ttavail cet apres midi Merci
  ```

- **dans le `.md` :**

  ```text
  midi verbatim pertinent je dois rester avec ma fille cet avant midi je rentrerai au ttavail cet apres midi portée probatoire -
  ```

#### `eq-196` — email-28 — taux 0.81 — `legal/piece_thread-22_email-28.md`

- **en base :**

  ```text
  Salut voici le papier du medicine, je vais manquer le CMOC et le dîner d'équipe, mais je suis malade et en plus je dois m occuper de mon gars
  ```

- **dans le `.md` :**

  ```text
  objet verbatim pertinent voici le papier du medicine je vais manquer le cmoc et le dîner d équipe mais je suis malade et en plus je dois m occuper de mon gars portée probatoire -
  ```

#### `eq-20` — email-55 — taux 0.80 — `legal/piece_thread-43_email-55.md`

- **en base :**

  ```text
  Good morning, I have to stay home today with my daugter because she is sick, i will be reacheble all day at my house number 450-550-2998 Thank you
  ```

- **dans le `.md` :**

  ```text
  objet verbatim pertinent i have to stay home today with my daugter because she is sick i will be reacheble all day at my house number portée probatoire -
  ```

#### `eq-192` — email-40 — taux 0.79 — `legal/piece_thread-32_email-40.md`

- **en base :**

  ```text
  Salut Karl, je vais rester a la maison aujourd hui pour aider ma conjointe avec le bebe, elle ne se sent pas tres bien et ma belle mere n est pas disponible
  ```

- **dans le `.md` :**

  ```text
  congė verbatim pertinent je vais rester a la maison aujourd hui pour aider ma conjointe avec le bebe elle ne se sent pas tres bien et ma belle mere n' est pas
  ```

#### `pq-74` — pdf-13 p.2 — taux 0.76 — `legal/piece_pdf-13.md`

- **en base :**

  ```text
  10h13:11 Témoignage de M. David – Questions du Tribunal.
  Objection de Me Ayoub (un jugement a été prononcé en 2016 sur ces sujets) ;
  Le Tribunal prend connaissance du jugement de 2016 ;
  
  10h17:04 Le Tribunal informe Monsieur de ne pas parler de ce qui s'est passé avant 2016.
  Suite du témoignage de M. David
  ```

- **dans le `.md` :**

  ```text
  h 13 - témoignage de m david questions du tribunal objection de me ayoub un jugement a été prononcé en 2016 sur ces sujets le tribunal prend connaissance du jugement […] p-2 en liasse plusieurs recherches d'emploi offertes à monsieur pendant le témoignage d'élise en interrogatoire par me ayoub - 10 h 44 04 - questions du tribunal à la témoin
  ```

#### `pq-83` — pdf-13 p.2 — taux 0.75 — `legal/compilation_griefs.md`

- **en base :**

  ```text
  10h38:50 P-2 en liasse : plusieurs recherches d'emploi offertes à Monsieur ;
  ```

- **dans le `.md` :**

  ```text
  me ayoub dépose p-2 en liasse plusieurs recherches d'emploi offertes à monsieur pendant le témoignage
  ```

#### `pq-75` — pdf-13 p.2 — taux 0.75 — `legal/compilation_griefs.md`

- **en base :**

  ```text
  10h38:50 P-2 en liasse : plusieurs recherches d'emploi offertes à Monsieur ;
  ```

- **dans le `.md` :**

  ```text
  me ayoub dépose p-2 en liasse plusieurs recherches d'emploi offertes à monsieur pendant le témoignage
  ```

#### `eq-184` — email-51 — taux 0.75 — `legal/piece_thread-40_email-50.md`

- **en base :**

  ```text
  Hi i have to stay home again today my mother in law can't come in.
  ```

- **dans le `.md` :**

  ```text
  catherine subject today hi i have to stay home again today my mother in law can t come
  ```

#### `eq-193` — email-30 — taux 0.72 — `legal/piece_thread-24_email-30.md`

- **en base :**

  ```text
  Salut Karl, je vais à la clinique ce matin avec mon gars et en fonction de ce qu ils me disent, je vais rester ici ou rentrer travailler!
  ```

- **dans le `.md` :**

  ```text
  maladie verbatim pertinent je vais à la clinique ce matin avec mon gars et en fonction de ce qu'ils me disent je vais rester ici ou rentrer travailler portée probatoire -
  ```

#### `pq-84` — pdf-13 p.3 — taux 0.72 — `legal/piece_pdf-13.md`

- **en base :**

  ```text
  Attendu que les parties, après le début de l'audition, se sont entendues à ce qu'un
  jugement soit rendu avec les conclusions suivantes :
  
  ORDONNE à Monsieur David de payer à Madame Ayoub pour les besoins des deux
  enfants mineurs un montant de 650 $
  ```

- **dans le `.md` :**

  ```text
  page 3 dispositif attendu que les parties après le début de l'audition se sont entendues à ce qu'un jugement soit rendu sur leurs conclusions - ordonne à monsieur david de […] contredit par les deux parties attendu que les parties après le début de l'audition se sont entendues à ce qu'un jugement soit rendu avec les conclusions suivantes verbatim page 3
  ```

#### `pq-32` — pdf-5 p.4 — taux 0.71 — `legal/piece_pdf-5.md`

- **en base :**

  ```text
  Si le père ne désire pas exercer ses droits d’accès prévus audit consentement auprès des enfants sur une base régulière, la pensionv alimentaire pour enfants sera majoré de 20% à raison de 465.41$ aux deux semaines;
  ```

- **dans le `.md` :**

  ```text
  ses droits d'accès sur une base régulière pension majorée de 20 à 465 41 aux deux semaines 14 frais particuliers partagés 50 50 garde santé non couverte passeport 15 déductions […] père ne désire pas exercer ses droits d'accès prévus audit consentement auprès des enfants sur une base régulière la pension alimentaire pour enfants sera majoré de 20 portée c'est la
  ```

#### `pq-29` — pdf-7 p.4 — taux 0.70 — `legal/piece_photodoc-13.md`

- **en base :**

  ```text
  Svp, pour toi, check pour le transfert d autorité parentale. Je suis serieux je ne vais pas signer de papiers de voyages, d ecole, de traitment. Je fais juste te dine. Parfait, mais je ne veux pas avoir a être consulter pour les voyages les psychologue etc. Je te le dis maintenant, attends pas d avoir besoins de ma signature pour faire les démarches
  ```

- **dans le `.md` :**

  ```text
  les papier de transfert d autorité parentale pour toi attends pas d'avoir besoins de quelque chose élise lp lp ton avocat attend un plan de garde si tu refuses ca […] veux pas avoir à consulter pour les voyages les psychologue etc je te le dis maintenant attends pas d'avoir besoins de ma signature pour faire les démarches --- contexte portée
  ```

#### `eq-189` — email-45 — taux 0.69 — `legal/piece_thread-36_email-45.md`

- **en base :**

  ```text
  Salut, ma fille a la gastro je dois rester a la maison je serrai disponible au 450 550 2998
  ```

- **dans le `.md` :**

  ```text
  hui verbatim pertinent ma fille a la gastro je dois rester a la maison je serrai disponible portée probatoire -
  ```

#### `eq-23` — email-47 — taux 0.68 — `legal/piece_thread-37_email-47.md`

- **en base :**

  ```text
   Bonjour, Je restes a la maison avec ma fille aujourd hui. Si Danilo a des questions, Je suis disponible 450 550 2998 Bonne jounee Louis-Philippe
  ```

- **dans le `.md` :**

  ```text
  conge verbatim pertinent je restes a la maison avec ma fille aujourd hui si danilo a des questions je suis disponible portée probatoire -
  ```

#### `pq-12` — pdf-59 p.1 — taux 0.66 — `legal/piece_pdf-59.md`

- **en base :**

  ```text
  En 1999, fascinée par la danse, elle se joint à l’école de danse Les Ballets Modernes du Québec. En 2005, elle débute ses classes au Urban Element (maintenant le UEZ) , où elle y rencontre plusieurs pionniers de la danse urbaine. Elle continue toutefois ses cours chez Les Ballet Modernes du Québec où elle observe les talents de Direction d'Hugo Depot et Francine St-Yves, et ce jusqu'en 2016.
  ```

- **dans le `.md` :**

  ```text
  - passages porteurs en 1999 fascinée par la danse elle se joint à l'école de danse les ballets modernes du québec en 2002 elle se joint à la troupe de […] elle continue toutefois ses cours chez les ballets modernes du québec où elle observe les talents de direction d'hugo depot et francine st-yves et ce jusqu'en 2016 elle y chorégraphie
  ```

#### `eq-142` — email-410 — taux 0.65 — `legal/piece_pension_nonmodif_jan2019.md`

- **en base :**

  ```text
  la pension alimentaire ne sera pas modifiée à ce stade-ci.  Nous avons procédé à des représentations aux stades intérimaires et malgré tes demandes de réduction et/ou de suspension de la pension, la juge a décidé que tu devais payer la pension même si tu n’avais pas d’emploi, vu entre autre tes économies et les besoins des enfants.
  ```

- **dans le `.md` :**

  ```text
  refus le scienter la pension alimentaire ne sera pas modifiée à ce stade-ci malgré tes demandes de réduction et ou de suspension la juge a décidé que tu devais payer la pension même si tu n'avais pas d'emploi vu entre autre tes économies et les besoins des enfants c3 - 23
  ```

#### `eq-191` — email-41 — taux 0.65 — `legal/implication_parentale_recurrence/04_journees_maladie.md`

- **en base :**

  ```text
  Bon matin Karl, je vais etre au fravail lundi. La sittuation se stabilise, mais nous ne dormons que quelques heures par nuit depuis une semaine et je suis épuisé. Non seulement le bébé ne dors pas, mais ma plus vieille fait de meme.
  ```

- **dans le `.md` :**

  ```text
  à son supérieur la sittuation se stabilise mais nous ne dormons qje quelqjes heures par nuit depuis une semaine et je suis épuisé non seulement le bébé ne dors pas mais ma plus vieille fait de meme le passage établit
  ```

#### `eq-24` — email-45 — taux 0.65 — `legal/piece_thread-36_email-45.md`

- **en base :**

  ```text
  Salut,ma fille a la gastro je dois rester a la maison je serrai disponible au 450 550 2998 Louis-Philippe
  ```

- **dans le `.md` :**

  ```text
  hui verbatim pertinent ma fille a la gastro je dois rester a la maison je serrai disponible portée probatoire -
  ```

#### `eq-93` — email-343 — taux 0.65 — `legal/piece_thread-76_email-343.md`

- **en base :**

  ```text
  Moi j y vais pas j ai pas ete invité et en fait je savais pas qu elle le
  faisias baptiser.... Bonjour, demain le 19 juillet à 14:00 je ferais baptiser Nicolas a l'église st Thomas d'aquin. Si vous avez envie d'être présentes à la cérémonie vous êtes les bienvenus.
  ```

- **dans le `.md` :**

  ```text
  johanne bazinet raymond bonjour demain le 19 juillet à 14 00 je ferais baptiser nicolas a l'église st thomas d'aquin si vous avez envie d'être présentes à la cérémonie vous […] nous y serons johanne et raymond - 19 juil 2015 - lp johanne moi j'y vais pas j'ai pas été invité et en fait je savais pas qu'elle le faisait
  ```

#### `pq-31` — pdf-3 p.2 — taux 0.60 — `legal/analyse/Responsabilité Déonthologique/2015 avril, aout.md`

- **en base :**

  ```text
  notre cliente réitère son offre à l'élargissement des droits d'accès du père auprès de leurs enfants à savotr :
  - Semaine 1 : 
  - Du mercredi après la garderie et ce jusqu'au jeudi matin à la garderie; Du samedi 14h 00 au dimanche 16h00.
  -Semaine 2 : 
  -Du mercredi après la garderie et ce jusqu'au jeudi matin à la garderie; Dimanche de 15h00 à 20h00.
  ```

- **dans le `.md` :**

  ```text
  mère et les droits d'accès du père d'une fin de semaine sur deux et votre refus à notre proposition que le père ait des droits d'accès prolongés me ayoub présente […] garderie du samedi 14h00 au dimanche 16h00 semaine 2 du mercredi après la garderie et ce jusqu'au jeudi matin à la garderie dimanche de 15h00 à 20h00 27 avril 2015
  ```

#### `eq-187` — email-56 — taux 0.60 — `legal/piece_thread-44_email-56.md`

- **en base :**

  ```text
  Salut Catherine je dois rester avec ma fille cet avant midi je rentrerai au travail cet apres midi
  ```

- **dans le `.md` :**

  ```text
  midi verbatim pertinent je dois rester avec ma fille cet avant midi je rentrerai au ttavail cet apres
  ```

---

## 2. À trancher (15) — taux entre 0,35 et 0,60

Un noyau de la citation se retrouve dans le `.md`, le reste non. Soit l'analyse n'a retenu qu'une partie du passage — auquel cas **c'est cette partie qui est le bloc atomique** —, soit la correspondance est fortuite.

| id | source | taux | trames | fichier .md | passage en base | extrait .md |
|---|---|---|---|---|---|---|
| `eq-185` | email-47 | 0.59 | 50,67 | `legal/piece_thread-37_email-47.md` | je restes a la maison avec ma fille aujourd'hui si danilo a des questi… | conge verbatim pertinent je restes a la maison avec ma fille aujourd h… |
| `eq-134` | email-3 | 0.58 | 62 | `legal/piece_thread-3_email-3.md` | bonjour le 1er juillet je vais avoir une conférence téléphonique avec … | transcription verbatim extraits le 1er juillet je vais avoir une confé… |
| `eq-26` | email-41 | 0.57 | 3 | `legal/implication_parentale_recurrence/04_journees_maladie.md` | bon matin karl je vais etre au fravail lundi la sittuation se stabilis… | à son supérieur la sittuation se stabilise mais nous ne dormons qje qu… |
| `eq-18` | email-59 | 0.55 | 3,31 | `legal/piece_thread-46_emails-58-59.md` | bon matin à tous francis je m'excuse mais je vais devoir te priver de … | verbatim pertinent lp j ai essayer de convaincre ma copine que tu avai… |
| `eq-25` | email-42 | 0.54 | 3 | `legal/piece_thread-34_email-42.md` | bon matin karl je ne retrerai pas travailler aujourd hui je vais reste… | absence verbatim pertinent je ne retrerai pas travailler aujourd hui j… |
| `pq-23` | pdf-11 p.1 | 0.53 | 33 | `legal/piece_pdf-11.md` | requérant e monsieur louis-philippe david lieux 245 avenue macaulay sa… | rapport d'évaluation marchande à des fins de partage référence base de… |
| `eq-30` | email-27 | 0.52 | 3 | `legal/piece_thread-21_email-27.md` | bon après-midi de toute évidence je ne rentre pas aujord hui je viens … | dec verbatim pertinent aucun des enfants ni moi avons dormis la nuit d… |
| `eq-178` | email-69 | 0.52 | 50,67 | `legal/journal_fevrier2011_fevrier2012.md` | bon matin catherine je dois rester avec ma petite aujourd'hui j'imagin… | liepins supérieure bnc je dois rester avec ma petite aujourd'hui j'ima… |
| `eq-162` | email-36 | 0.48 | — | `legal/compilation_griefs.md` | j'habites chez mes parents pour un petit bout question de régler des p… | défendeur écrivait j'habite chez mes parents pour un petit bout questi… |
| `pq-76` | pdf-13 p.3 | 0.44 | — | `legal/piece_pdf-13.md` | attendu que les parties après le début de l'audition se sont entendues… | et tenant compte de la situation financière page 3 dispositif attendu … |
| `pq-87` | pdf-8 p.9 | 0.41 | 62 | `legal/piece_pdf-8.md` | la lpj ne prévoit pas d'obligations du dpj en matière de divulgation d… | obligation du dpj de soumettre un portrait complet et objectif devoir … |
| `eq-149` | email-39 | 0.40 | — | `legal/allegation_stmt13_ete2013.md` | jespere que tu passes de belle vacances je suis dans un processus de s… | hiérarchique karl grimmel je suis dans un processus de séparation je s… |
| `eq-10` | email-358 | 0.40 | 2 | `legal/journal_ete2013.md` | on pourrait peut être souper ensemble dimanche prochain avec alexia po… | on pourrait peut-être souper ensemble dimanche prochain avec alexia po… |
| `eq-99` | email-22 | 0.36 | 53,74 | `legal/allegation_stmt4_5_6.md` | pour moi tu étais mon chum et je ai a quelque reprise embrasse et que … | id 171 - pour moi tu étais mon chum et je ai a quelque reprise embrass… |
| `pq-98` | pdf-5 p.3 | 0.35 | 50 | `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md` | du 28 août 2017 au 25 août 2018 semaine 1 de samedi 10h30 directement … | 28 août 2016 semaine 1 de samedi 10h30 directement à la piscine à dima… |

---

## 3. Tableau complet, par taux décroissant

| id | source | taux | palier | strict | trames | meilleur fichier .md |
|---|---|---|---|---|---|---|
| `pq-104` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 70 | `legal/dossier_plaidoirie/08_these_substitution_des_fondements.md` |
| `pq-103` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 70 | `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md` |
| `pq-96` | pdf-5 p.2 | 1.00 | reprise quasi intégrale | — | 50 | `legal/piece_pdf-5.md` |
| `pq-95` | pdf-5 p.2 | 1.00 | reprise quasi intégrale | — | 50 | `legal/analyse/Responsabilité civile/requete 21 octobre 2019/analyse preliminaire - echec negociations 2015 et paragraphe 3.md` |
| `pq-94` | pdf-5 p.1 | 1.00 | reprise quasi intégrale | — | 50 | `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/03_concordance_aout_novembre_2015.md` |
| `pq-92` | pdf-5 p.3 | 1.00 | reprise quasi intégrale | — | 50 | `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md` |
| `pq-91` | pdf-5 p.1 | 1.00 | reprise quasi intégrale | — | 50,76 | `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/01_inexecution_plan_cohabitation.md` |
| `pq-90` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 50,70 | `legal/piece_pdf-1.md` |
| `pq-88` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 62 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `pq-69` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | — | 62,70,71,72 | `legal/allegation_stmt13_ete2013.md` |
| `pq-68` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 62 | `legal/allegation_stmt19_20_21_acces.md` |
| `pq-67` | pdf-6 p.2 | 1.00 | reprise quasi intégrale | — | 56 | `legal/piece_pdf-6.md` |
| `pq-66` | pdf-6 p.2 | 1.00 | reprise quasi intégrale | — | 56 | `legal/piece_pdf-6.md` |
| `pq-65` | pdf-6 p.2 | 1.00 | reprise quasi intégrale | oui | 56 | `legal/piece_pdf-6.md` |
| `pq-64` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | — | 56,62 | `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md` |
| `pq-63` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | — | 56,62 | `legal/allegation_stmt62_separation_2011.md` |
| `pq-62` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | — | 56,62,70 | `legal/allegation_stmt14_15_16_17_garde_partagee.md` |
| `pq-61` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | — | 56,62 | `legal/allegation_stmt14_15_16_17_garde_partagee.md` |
| `pq-60` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 56,62 | `legal/allegation_stmt19_20_21_acces.md` |
| `pq-59` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 56,62 | `legal/allegation_stmt62_separation_2011.md` |
| `pq-58` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | — | 56,62 | `legal/allegation_stmt62_separation_2011.md` |
| `pq-57` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | — | 56,62 | `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/11_memoire_argumentative_verrouillee_continuite_P2_P19.md` |
| `pq-56` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 9 | `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/02_securite_fondement_objectif.md` |
| `pq-55` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | — | 55 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `pq-54` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 50,55,70,71,76 | `legal/allegation_stmt14_15_16_17_garde_partagee.md` |
| `pq-53` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 55 | `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md` |
| `pq-52` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 50,55 | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/03_anteriorite_preference_et_fonction_du_registre.md` |
| `pq-51` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 50,55,70 | `legal/allegation_stmt62_separation_2011.md` |
| `pq-50` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 50,55,62,70 | `legal/allegation_stmt62_separation_2011.md` |
| `pq-34` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | — | 48 | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/03_anteriorite_preference_et_fonction_du_registre.md` |
| `pq-28` | pdf-6 p.2 | 1.00 | reprise quasi intégrale | — | 34,40 | `legal/piece_pdf-6.md` |
| `pq-24` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 35 | `legal/allegation_stmt62_separation_2011.md` |
| `pq-22` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | — | `legal/allegation_stmt62_separation_2011.md` |
| `pq-21` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | — | 22 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `pq-20` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | — | — | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `pq-18` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 32 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `pq-16` | pdf-11 p.1 | 1.00 | reprise quasi intégrale | — | 20 | `legal/piece_pdf-11.md` |
| `pq-14` | pdf-6 p.2 | 1.00 | reprise quasi intégrale | — | — | `legal/piece_pdf-6.md` |
| `pq-9` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 70,71,72,76 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `pq-8` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 70 | `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md` |
| `pq-7` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 7,48,49,70,72 | `legal/allegation_stmt19_20_21_acces.md` |
| `pq-6` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | 7,48,49,70,72,76 | `legal/allegation_stmt62_separation_2011.md` |
| `pq-4` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | — | `legal/allegation_stmt62_separation_2011.md` |
| `pq-3` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | — | `legal/allegation_stmt62_separation_2011.md` |
| `pq-2` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | — | `legal/allegation_stmt62_separation_2011.md` |
| `pq-1` | pdf-1 p.1 | 1.00 | reprise quasi intégrale | oui | — | `legal/amendements/01_avant_notification/analyses_experimentales/evaluations_sources_partagees_2026-07-27/11_memoire_argumentative_verrouillee_continuite_P2_P19.md` |
| `eq-216` | email-306 | 1.00 | reprise quasi intégrale | oui | — | `legal/allegation_stmt14_15_16_17_garde_partagee.md` |
| `eq-215` | email-275 | 1.00 | reprise quasi intégrale | oui | — | `legal/allegation_stmt14_15_16_17_garde_partagee.md` |
| `eq-209` | email-238 | 1.00 | reprise quasi intégrale | — | — | `legal/piece_chatsequence-1.md` |
| `eq-207` | email-57 | 1.00 | reprise quasi intégrale | oui | 30,70 | `legal/piece_thread-45_email-57.md` |
| `eq-206` | email-106 | 1.00 | reprise quasi intégrale | oui | 30 | `legal/piece_thread-59_email-106.md` |
| `eq-205` | email-177 | 1.00 | reprise quasi intégrale | oui | 69,75 | `legal/piece_thread-ecrement_2015.md` |
| `eq-204` | email-178 | 1.00 | reprise quasi intégrale | oui | 69,75 | `legal/faits/faits_par28-29_2015.md` |
| `eq-203` | email-180 | 1.00 | reprise quasi intégrale | — | 69,75 | `legal/piece_thread-ecrement_2015.md` |
| `eq-201` | email-184 | 1.00 | reprise quasi intégrale | oui | 69 | `legal/piece_thread-ecrement_2015.md` |
| `eq-200` | email-76 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-61_email-76.md` |
| `eq-197` | email-6 | 1.00 | reprise quasi intégrale | oui | 50 | `legal/piece_thread-6_email-6.md` |
| `eq-195` | email-27 | 1.00 | reprise quasi intégrale | oui | 67 | `legal/piece_thread-21_email-27.md` |
| `eq-186` | email-61 | 1.00 | reprise quasi intégrale | oui | 67 | `legal/piece_thread-48_email-61.md` |
| `eq-183` | email-53 | 1.00 | reprise quasi intégrale | — | 50,67 | `legal/faits_chronologiques_2010-11-20_2012-02-06.md` |
| `eq-181` | email-118 | 1.00 | reprise quasi intégrale | oui | 50,67 | `legal/implication_parentale_recurrence/04_journees_maladie.md` |
| `eq-180` | email-64 | 1.00 | reprise quasi intégrale | — | 50,67 | `legal/faits_chronologiques_2010-11-20_2012-02-06.md` |
| `eq-179` | email-68 | 1.00 | reprise quasi intégrale | oui | 50,67 | `legal/piece_thread-54_emails-68-69.md` |
| `eq-177` | email-369 | 1.00 | reprise quasi intégrale | oui | 65 | `legal/implication_parentale_recurrence/02_garderie.md` |
| `eq-175` | email-352 | 1.00 | reprise quasi intégrale | — | — | `legal/journal_ete2013.md` |
| `eq-170` | email-355 | 1.00 | reprise quasi intégrale | — | — | `legal/piece_thread-83_email-355.md` |
| `eq-168` | email-356 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-84_email-357.md` |
| `eq-165` | email-361 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-88_email-361.md` |
| `eq-161` | email-445 | 1.00 | reprise quasi intégrale | — | — | `legal/piece_thread-109.md` |
| `eq-160` | email-443 | 1.00 | reprise quasi intégrale | oui | — | `legal/amendements/01_avant_notification/faits_experimentaux/01_planification_statu_quo_garde.md` |
| `eq-159` | email-6 | 1.00 | reprise quasi intégrale | oui | — | `legal/compilation_griefs.md` |
| `eq-158` | email-484 | 1.00 | reprise quasi intégrale | oui | 63 | `legal/compilation_griefs.md` |
| `eq-156` | email-4 | 1.00 | reprise quasi intégrale | oui | 62 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `eq-155` | email-114 | 1.00 | reprise quasi intégrale | oui | 5,64 | `legal/piece_thread-53_email-114.md` |
| `eq-154` | email-67 | 1.00 | reprise quasi intégrale | oui | 5 | `legal/axe_agenda_danse_elise.md` |
| `eq-153` | email-62 | 1.00 | reprise quasi intégrale | oui | 31 | `legal/piece_thread-49_email-62.md` |
| `eq-152` | email-61 | 1.00 | reprise quasi intégrale | oui | 5 | `legal/piece_thread-48_email-61.md` |
| `eq-150` | email-365 | 1.00 | reprise quasi intégrale | oui | 72 | `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphe 10.md` |
| `eq-148` | email-37 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-29_email-37.md` |
| `eq-144` | email-5 | 1.00 | reprise quasi intégrale | oui | — | `legal/compilation_griefs.md` |
| `eq-139` | email-79 | 1.00 | reprise quasi intégrale | oui | 11 | `legal/axe_presence_quotidienne_activites.md` |
| `eq-138` | email-86 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_emails_petite_enfance_2010.md` |
| `eq-136` | email-90 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-75_email-92.md` |
| `eq-135` | email-475 | 1.00 | reprise quasi intégrale | — | 9,38 | `legal/piece_thread-116_email-475.md` |
| `eq-131` | email-330 | 1.00 | reprise quasi intégrale | — | 62 | `legal/piece_thread-4_email-330.md` |
| `eq-127` | email-456 | 1.00 | reprise quasi intégrale | — | 62 | `legal/piece_thread-111_congediement_bnc.md` |
| `eq-126` | email-4 | 1.00 | reprise quasi intégrale | — | 62 | `legal/inventaire_incompatibilites.md` |
| `eq-125` | email-448 | 1.00 | reprise quasi intégrale | — | — | `legal/piece_thread-109.md` |
| `eq-124` | email-447 | 1.00 | reprise quasi intégrale | — | 56 | `legal/piece_thread-109.md` |
| `eq-123` | email-444 | 1.00 | reprise quasi intégrale | oui | 56,72,76 | `legal/analyse/Responsabilité civile/requete 21 octobre 2019/analyse preliminaire - echec negociations 2015 et paragraphe 3.md` |
| `eq-122` | email-6 | 1.00 | reprise quasi intégrale | — | — | `legal/allegation_stmt14_15_16_17_garde_partagee.md` |
| `eq-121` | email-305 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-6_email-305.md` |
| `eq-120` | email-295 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-6_reconstruction.md` |
| `eq-119` | email-295 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-6_reconstruction.md` |
| `eq-118` | email-267 | 1.00 | reprise quasi intégrale | oui | 9 | `legal/analyse/Responsabilité Déonthologique/2015 avril, aout.md` |
| `eq-114` | email-6 | 1.00 | reprise quasi intégrale | oui | 56 | `legal/piece_thread-6_email-6.md` |
| `eq-113` | email-276 | 1.00 | reprise quasi intégrale | oui | 55 | `legal/analyse/Responsabilité civile/Volume3 Tableau Analytique Allegations.md` |
| `eq-112` | email-293 | 1.00 | reprise quasi intégrale | oui | 55 | `legal/piece_thread-6_reconstruction.md` |
| `eq-111` | email-306 | 1.00 | reprise quasi intégrale | oui | — | `legal/axe_agenda_danse_elise.md` |
| `eq-110` | email-8 | 1.00 | reprise quasi intégrale | oui | 50,55 | `legal/piece_thread-6_email-8.md` |
| `eq-109` | email-296 | 1.00 | reprise quasi intégrale | — | 55 | `legal/piece_thread-6_reconstruction.md` |
| `eq-108` | email-270 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-6_reconstruction.md` |
| `eq-106` | email-10 | 1.00 | reprise quasi intégrale | oui | 55,56 | `legal/piece_thread-6_reconstruction.md` |
| `eq-105` | email-299 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-6_reconstruction.md` |
| `eq-104` | email-305 | 1.00 | reprise quasi intégrale | oui | 55 | `legal/piece_thread-6_email-305.md` |
| `eq-103` | email-287 | 1.00 | reprise quasi intégrale | oui | 55 | `legal/piece_thread-6_reconstruction.md` |
| `eq-102` | email-10 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-6_reconstruction.md` |
| `eq-101` | email-299 | 1.00 | reprise quasi intégrale | oui | 55 | `legal/piece_thread-6_reconstruction.md` |
| `eq-100` | email-305 | 1.00 | reprise quasi intégrale | oui | 55,56 | `legal/piece_thread-6_email-305.md` |
| `eq-98` | email-171 | 1.00 | reprise quasi intégrale | — | 53,74 | `legal/allegation_stmt4_5_6.md` |
| `eq-97` | email-167 | 1.00 | reprise quasi intégrale | — | 53,74 | `legal/allegation_stmt4_5_6.md` |
| `eq-96` | email-16 | 1.00 | reprise quasi intégrale | oui | 50,56,74 | `legal/allegation_stmt14_15_16_17_garde_partagee.md` |
| `eq-95` | email-236 | 1.00 | reprise quasi intégrale | oui | 50,56,74 | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/01_architecture_justificative_stabilite.md` |
| `eq-91` | email-267 | 1.00 | reprise quasi intégrale | oui | 35,55 | `legal/analyse/Responsabilité civile/courriel 11 juin 2013 - responsabilite de Me Ayoub.md` |
| `eq-90` | email-402 | 1.00 | reprise quasi intégrale | oui | 9,34,38,39,42,49,52 | `legal/piece_thread-100_email-401.md` |
| `eq-89` | email-397 | 1.00 | reprise quasi intégrale | oui | 31 | `legal/axe_presence_quotidienne_activites.md` |
| `eq-88` | email-396 | 1.00 | reprise quasi intégrale | oui | 31 | `legal/piece_thread-99_email-396.md` |
| `eq-86` | email-394 | 1.00 | reprise quasi intégrale | oui | 31 | `legal/piece_thread-97_email-390.md` |
| `eq-85` | email-387 | 1.00 | reprise quasi intégrale | oui | 31 | `legal/axe_presence_quotidienne_activites.md` |
| `eq-84` | email-383 | 1.00 | reprise quasi intégrale | oui | 31,70 | `legal/allegation_62_separation_2011.md` |
| `eq-83` | email-382 | 1.00 | reprise quasi intégrale | oui | 31 | `legal/allegation_62_separation_2011.md` |
| `eq-81` | email-71 | 1.00 | reprise quasi intégrale | oui | 31 | `legal/allegation_62_separation_2011.md` |
| `eq-80` | email-106 | 1.00 | reprise quasi intégrale | oui | 30 | `legal/piece_thread-59_email-106.md` |
| `eq-79` | email-74 | 1.00 | reprise quasi intégrale | oui | 30 | `legal/piece_thread-59_email-106.md` |
| `eq-77` | email-349 | 1.00 | reprise quasi intégrale | oui | 8,26,34,48,49,52 | `legal/piece_thread-109.md` |
| `eq-76` | email-7 | 1.00 | reprise quasi intégrale | oui | 11 | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/01_architecture_justificative_stabilite.md` |
| `eq-74` | email-349 | 1.00 | reprise quasi intégrale | — | 8,26 | `legal/piece_thread-109.md` |
| `eq-73` | email-48 | 1.00 | reprise quasi intégrale | — | 5,64 | `legal/axe_agenda_danse_elise.md` |
| `eq-72` | email-163 | 1.00 | reprise quasi intégrale | oui | 8,39,41 | `legal/piece_thread-18_email-163.md` |
| `eq-67` | email-174 | 1.00 | reprise quasi intégrale | oui | 43,69,75 | `legal/compilation_griefs.md` |
| `eq-66` | email-174 | 1.00 | reprise quasi intégrale | oui | 43,69,75 | `legal/analyse/Responsabilité civile/analyse_individuelle_et_cumulative_allegations.md` |
| `eq-65` | email-371 | 1.00 | reprise quasi intégrale | oui | 65 | `legal/axe_garderie_coordination.md` |
| `eq-64` | email-370 | 1.00 | reprise quasi intégrale | oui | 4 | `legal/piece_thread-91_emails-369-370.md` |
| `eq-63` | email-349 | 1.00 | reprise quasi intégrale | oui | 8,19,34,48,52 | `legal/amendements/01_avant_notification/faits_experimentaux/01_planification_statu_quo_garde.md` |
| `eq-60` | email-8 | 1.00 | reprise quasi intégrale | oui | 11,50 | `legal/faits/faits_par14-17_2015.md` |
| `eq-59` | email-347 | 1.00 | reprise quasi intégrale | — | 65 | `legal/piece_thread-78_email-347.md` |
| `eq-58` | email-7 | 1.00 | reprise quasi intégrale | oui | 5,12,64 | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/01_architecture_justificative_stabilite.md` |
| `eq-57` | email-29 | 1.00 | reprise quasi intégrale | — | 4,5,65 | `legal/piece_thread-23_email-148.md` |
| `eq-56` | email-6 | 1.00 | reprise quasi intégrale | oui | 55 | `legal/piece_thread-6_email-6.md` |
| `eq-55` | email-275 | 1.00 | reprise quasi intégrale | oui | 50 | `legal/allegation_stmt14_15_16_17_garde_partagee.md` |
| `eq-53` | email-8 | 1.00 | reprise quasi intégrale | oui | 8,50 | `legal/allegation_stmt14_15_16_17_garde_partagee.md` |
| `eq-52` | email-296 | 1.00 | reprise quasi intégrale | oui | — | `legal/piece_thread-6_reconstruction.md` |
| `eq-51` | email-305 | 1.00 | reprise quasi intégrale | oui | 5,11,64 | `legal/axe_agenda_danse_elise.md` |
| `eq-50` | email-349 | 1.00 | reprise quasi intégrale | oui | 26 | `legal/amendements/01_avant_notification/faits_experimentaux/01_planification_statu_quo_garde.md` |
| `eq-44` | email-349 | 1.00 | reprise quasi intégrale | oui | 44 | `legal/piece_thread-109.md` |
| `eq-43` | email-349 | 1.00 | reprise quasi intégrale | oui | 8,26 | `legal/piece_thread-109.md` |
| `eq-41` | email-66 | 1.00 | reprise quasi intégrale | oui | 5,31,64 | `legal/piece_thread-52_emails-66-115-116.md` |
| `eq-40` | email-100 | 1.00 | reprise quasi intégrale | oui | 5,64 | `legal/axe_agenda_danse_elise.md` |
| `eq-39` | email-81 | 1.00 | reprise quasi intégrale | oui | 5,64 | `legal/piece_thread-66_email-81.md` |
| `eq-38` | email-90 | 1.00 | reprise quasi intégrale | oui | 11,66 | `legal/piece_thread-75_email-92.md` |
| `eq-37` | email-48 | 1.00 | reprise quasi intégrale | — | 4,5,65 | `legal/piece_thread-78_email-347.md` |
| `eq-36` | email-54 | 1.00 | reprise quasi intégrale | oui | 4,31,65 | `legal/allegation_62_separation_2011.md` |
| `eq-22` | email-51 | 1.00 | reprise quasi intégrale | — | 3,31 | `legal/piece_thread-40_email-50.md` |
| `eq-17` | email-64 | 1.00 | reprise quasi intégrale | oui | 3,31 | `legal/piece_thread-50_email-63.md` |
| `eq-15` | email-349 | 1.00 | reprise quasi intégrale | — | 2,8 | `legal/piece_thread-109.md` |
| `eq-14` | email-38 | 1.00 | reprise quasi intégrale | oui | 2 | `legal/piece_thread-30_email-38.md` |
| `eq-11` | email-357 | 1.00 | reprise quasi intégrale | oui | 2 | `legal/piece_thread-84_email-357.md` |
| `eq-8` | email-32 | 1.00 | reprise quasi intégrale | oui | 2,11,66 | `legal/implication_parentale_recurrence/03a_soccer_alexia_ete_2013.md` |
| `eq-7` | email-33 | 1.00 | reprise quasi intégrale | — | 2,11 | `legal/piece_thread-26_emails-33-32.md` |
| `eq-6` | email-360 | 1.00 | reprise quasi intégrale | oui | 2 | `legal/piece_thread-87_email-360.md` |
| `eq-4` | email-362 | 1.00 | reprise quasi intégrale | oui | 2 | `legal/piece_thread-88_email-362.md` |
| `eq-54` | email-7 | 0.98 | reprise quasi intégrale | — | — | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/01_architecture_justificative_stabilite.md` |
| `eq-42` | email-116 | 0.97 | reprise quasi intégrale | — | 5,31,64 | `legal/piece_thread-52_emails-66-115-116.md` |
| `pq-5` | pdf-1 p.1 | 0.95 | reprise quasi intégrale | — | — | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/03_anteriorite_preference_et_fonction_du_registre.md` |
| `eq-132` | email-462 | 0.95 | reprise quasi intégrale | — | 62 | `legal/piece_thread-113_email-462.md` |
| `eq-61` | email-116 | 0.95 | reprise quasi intégrale | — | 31 | `legal/piece_thread-52_emails-66-115-116.md` |
| `eq-94` | email-7 | 0.94 | reprise quasi intégrale | — | 4,50,64 | `legal/amendements/01_avant_notification/analyses_experimentales/analyse_p19_faussetes_2026-07-28/01_architecture_justificative_stabilite.md` |
| `eq-2` | email-40 | 0.93 | reprise quasi intégrale | — | 2,3 | `legal/piece_thread-32_email-40.md` |
| `eq-34` | email-87 | 0.93 | reprise quasi intégrale | — | 24 | `legal/piece_emails_petite_enfance_2010.md` |
| `eq-182` | email-59 | 0.92 | reprise quasi intégrale | — | 50,67 | `legal/piece_thread-46_emails-58-59.md` |
| `eq-28` | email-30 | 0.92 | reprise quasi intégrale | — | 3 | `legal/piece_thread-24_email-30.md` |
| `eq-35` | email-86 | 0.91 | reprise quasi intégrale | — | 24 | `legal/piece_emails_petite_enfance_2010.md` |
| `eq-208` | email-404 | 0.91 | reprise quasi intégrale | — | 44 | `legal/piece_thread-100_email-404.md` |
| `eq-69` | email-373 | 0.91 | reprise quasi intégrale | — | 8 | `legal/piece_emails_cape_cod_2012.md` |
| `eq-68` | email-49 | 0.90 | reprise quasi intégrale | — | 8,31 | `legal/piece_emails_cape_cod_2012.md` |
| `eq-107` | email-285 | 0.90 | reprise quasi intégrale | — | 55 | `legal/piece_thread-6_reconstruction.md` |
| `pq-26` | pdf-1 p.1 | 0.90 | reprise quasi intégrale | — | 39 | `legal/analyse/Responsabilité civile/courriel 11 juin 2013 - responsabilite de Me Ayoub.md` |
| `pq-25` | pdf-1 p.1 | 0.89 | reprise quasi intégrale | — | 6,34,36,52 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `pq-27` | pdf-3 p.2 | 0.88 | reprise quasi intégrale | — | 34,39,42,49,71,72,73,76 | `legal/allegation_stmt19_20_21_acces.md` |
| `eq-16` | email-69 | 0.88 | reprise quasi intégrale | — | 3,31 | `legal/piece_thread-54_emails-68-69.md` |
| `eq-190` | email-42 | 0.88 | reprise quasi intégrale | — | 67 | `legal/piece_thread-34_email-42.md` |
| `eq-5` | email-34 | 0.88 | reprise quasi intégrale | — | 2 | `legal/piece_thread-27_email-34.md` |
| `pq-17` | pdf-1 p.1 | 0.87 | reprise quasi intégrale | — | 21 | `legal/amendements/01_avant_notification/faits_experimentaux/01_planification_statu_quo_garde.md` |
| `eq-188` | email-55 | 0.87 | reprise quasi intégrale | — | 67 | `legal/piece_thread-43_email-55.md` |
| `eq-21` | email-53 | 0.87 | reprise quasi intégrale | — | 3,31 | `legal/piece_thread-123_email-488.md` |
| `pq-82` | pdf-13 p.2 | 0.86 | reprise quasi intégrale | — | 62 | `legal/piece_pdf-13.md` |
| `eq-62` | email-137 | 0.85 | largement reprise | — | 14 | `legal/allegation_stmt66_residence_2014.md` |
| `pq-10` | pdf-3 p.2 | 0.84 | largement reprise | — | 9,38,55,56,71,72,73,76 | `legal/allegation_stmt19_20_21_acces.md` |
| `eq-194` | email-21 | 0.83 | largement reprise | — | 50,67 | `legal/piece_thread-17_email-21.md` |
| `eq-31` | email-21 | 0.83 | largement reprise | — | 3 | `legal/piece_thread-17_email-21.md` |
| `pq-11` | pdf-2 p.1 | 0.83 | largement reprise | — | 9,34,38,39,47,49,52,56 | `legal/piece_pdf-2.md` |
| `pq-13` | pdf-7 p.1 | 0.82 | largement reprise | — | — | `legal/piece_pdf-7.md` |
| `eq-29` | email-28 | 0.81 | largement reprise | — | 3 | `legal/piece_thread-22_email-28.md` |
| `eq-19` | email-56 | 0.81 | largement reprise | — | 3,31 | `legal/piece_thread-44_email-56.md` |
| `eq-196` | email-28 | 0.81 | largement reprise | — | 67 | `legal/piece_thread-22_email-28.md` |
| `eq-20` | email-55 | 0.80 | largement reprise | — | 3,31 | `legal/piece_thread-43_email-55.md` |
| `eq-192` | email-40 | 0.79 | largement reprise | — | 67 | `legal/piece_thread-32_email-40.md` |
| `pq-74` | pdf-13 p.2 | 0.76 | largement reprise | — | 62 | `legal/piece_pdf-13.md` |
| `pq-83` | pdf-13 p.2 | 0.75 | largement reprise | — | 62 | `legal/compilation_griefs.md` |
| `pq-75` | pdf-13 p.2 | 0.75 | largement reprise | — | 62 | `legal/compilation_griefs.md` |
| `eq-184` | email-51 | 0.75 | largement reprise | — | 50,67 | `legal/piece_thread-40_email-50.md` |
| `eq-193` | email-30 | 0.72 | largement reprise | — | 67 | `legal/piece_thread-24_email-30.md` |
| `pq-84` | pdf-13 p.3 | 0.72 | largement reprise | — | 62 | `legal/piece_pdf-13.md` |
| `pq-32` | pdf-5 p.4 | 0.71 | largement reprise | — | 48,49,50,55 | `legal/piece_pdf-5.md` |
| `pq-29` | pdf-7 p.4 | 0.70 | largement reprise | — | 44 | `legal/piece_photodoc-13.md` |
| `eq-189` | email-45 | 0.69 | largement reprise | — | 67 | `legal/piece_thread-36_email-45.md` |
| `eq-23` | email-47 | 0.68 | largement reprise | — | 3 | `legal/piece_thread-37_email-47.md` |
| `pq-12` | pdf-59 p.1 | 0.66 | largement reprise | — | 12,64 | `legal/piece_pdf-59.md` |
| `eq-142` | email-410 | 0.65 | largement reprise | — | 62 | `legal/piece_pension_nonmodif_jan2019.md` |
| `eq-191` | email-41 | 0.65 | largement reprise | — | 67 | `legal/implication_parentale_recurrence/04_journees_maladie.md` |
| `eq-24` | email-45 | 0.65 | largement reprise | — | 3 | `legal/piece_thread-36_email-45.md` |
| `eq-93` | email-343 | 0.65 | largement reprise | — | 44 | `legal/piece_thread-76_email-343.md` |
| `pq-31` | pdf-3 p.2 | 0.60 | largement reprise | — | 46,47,49,52,55,73,76 | `legal/analyse/Responsabilité Déonthologique/2015 avril, aout.md` |
| `eq-187` | email-56 | 0.60 | largement reprise | — | 67 | `legal/piece_thread-44_email-56.md` |
| `eq-185` | email-47 | 0.59 | noyau repris | — | 50,67 | `legal/piece_thread-37_email-47.md` |
| `eq-134` | email-3 | 0.58 | noyau repris | — | 62 | `legal/piece_thread-3_email-3.md` |
| `eq-26` | email-41 | 0.57 | noyau repris | — | 3 | `legal/implication_parentale_recurrence/04_journees_maladie.md` |
| `eq-18` | email-59 | 0.55 | noyau repris | — | 3,31 | `legal/piece_thread-46_emails-58-59.md` |
| `eq-25` | email-42 | 0.54 | noyau repris | — | 3 | `legal/piece_thread-34_email-42.md` |
| `pq-23` | pdf-11 p.1 | 0.53 | noyau repris | — | 33 | `legal/piece_pdf-11.md` |
| `eq-30` | email-27 | 0.52 | noyau repris | — | 3 | `legal/piece_thread-21_email-27.md` |
| `eq-178` | email-69 | 0.52 | noyau repris | — | 50,67 | `legal/journal_fevrier2011_fevrier2012.md` |
| `eq-162` | email-36 | 0.48 | noyau repris | — | — | `legal/compilation_griefs.md` |
| `pq-76` | pdf-13 p.3 | 0.44 | noyau repris | — | — | `legal/piece_pdf-13.md` |
| `pq-87` | pdf-8 p.9 | 0.41 | noyau repris | — | 62 | `legal/piece_pdf-8.md` |
| `eq-149` | email-39 | 0.40 | noyau repris | — | — | `legal/allegation_stmt13_ete2013.md` |
| `eq-10` | email-358 | 0.40 | noyau repris | — | 2 | `legal/journal_ete2013.md` |
| `eq-99` | email-22 | 0.36 | noyau repris | — | 53,74 | `legal/allegation_stmt4_5_6.md` |
| `pq-98` | pdf-5 p.3 | 0.35 | noyau repris | — | 50 | `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md` |
| `eq-141` | email-408 | 0.35 | écho faible | — | 62 | `legal/piece_pension_nonmodif_jan2019.md` |
| `pq-93` | pdf-5 p.3 | 0.34 | écho faible | — | 50 | `legal/compilation_griefs.md` |
| `eq-171` | email-353 | 0.32 | écho faible | — | — | `legal/journal_ete2013.md` |
| `pq-97` | pdf-5 p.3 | 0.31 | écho faible | — | 50 | `legal/amendements/01_avant_notification/analyses_experimentales/01_these_danger_preference_statu_quo.md` |
| `pq-72` | pdf-8 p.2 | 0.31 | écho faible | — | 48,55 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `pq-70` | pdf-8 p.2 | 0.31 | écho faible | — | 62 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `eq-129` | email-454 | 0.30 | écho faible | — | 62 | `legal/piece_thread-111_congediement_bnc.md` |
| `eq-33` | email-88 | 0.29 | écho faible | — | 24 | `legal/piece_emails_petite_enfance_2010.md` |
| `pq-78` | pdf-66 p.1 | 0.23 | écho faible | — | 62 | `legal/piece_pdf-66.md` |
| `pq-102` | pdf-64 p.1 | 0.23 | écho faible | — | 68 | `legal/compilation_griefs.md` |
| `eq-3` | email-35 | 0.23 | écho faible | — | 2,15 | `legal/compilation_griefs.md` |
| `eq-32` | email-89 | 0.22 | écho faible | — | 24 | `legal/piece_emails_petite_enfance_2010.md` |
| `eq-151` | email-474 | 0.21 | écho faible | — | 5,64 | `legal/piece_thread-115_email-474.md` |
| `pq-33` | pdf-5 p.3 | 0.21 | écho faible | — | 34,47,49,50,52,55 | `legal/compilation_griefs.md` |
| `eq-116` | email-319 | 0.19 | écho faible | — | — | `legal/piece_thread-6_reconstruction.md` |
| `pq-77` | pdf-72 p.1 | 0.18 | écho faible | — | — | `legal/piece_pdf-72.md` |
| `pq-79` | pdf-67 p.1 | 0.15 | écho faible | — | 62 | `legal/piece_pdf-67.md` |
| `pq-48` | pdf-47 p.1 | 0.13 | absente | — | 30 | `legal/piece_releve_pension_rq_2026.md` |
| `pq-73` | pdf-9 p.2 | 0.12 | absente | — | 48,55,62 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `pq-71` | pdf-10 p.2 | 0.12 | absente | — | 48,55,62 | `legal/analyse/Responsabilité Déonthologique/2013 juin.md` |
| `eq-117` | email-312 | 0.12 | absente | — | — | `legal/piece_pdf-1.md` |
| `eq-176` | email-367 | 0.12 | absente | — | — | `legal/journal_ete2013.md` |
| `pq-30` | pdf-63 p.1 | 0.09 | absente | — | 68 | `legal/piece_pdf-63.md` |
| `eq-71` | email-78 | 0.08 | absente | — | 44,62 | `legal/faits_chronologiques_2010-11-20_2012-02-06.md` |
| `eq-12` | email-143 | 0.08 | absente | — | 5 | `legal/allegation_stmt19_20_21_acces.md` |
| `pq-85` | pdf-5 p.5 | 0.08 | absente | — | — | `legal/compilation_griefs.md` |
| `pq-46` | pdf-45 p.1 | 0.07 | absente | — | 30 | `legal/piece_releve_pension_rq_2026.md` |
| `eq-157` | email-480 | 0.07 | absente | — | 63 | `legal/piece_thread-97_email-394.md` |
| `pq-101` | pdf-64 p.1 | 0.07 | absente | — | 68 | `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 56 57.md` |
| `pq-45` | pdf-58 p.1 | 0.07 | absente | — | 30 | `legal/piece_releve_pension_rq_2026.md` |
| `pq-43` | pdf-54 p.1 | 0.07 | absente | — | 30 | `legal/piece_releve_pension_rq_2026.md` |
| `pq-42` | pdf-57 p.1 | 0.07 | absente | — | 30 | `legal/piece_releve_pension_rq_2026.md` |
| `pq-100` | pdf-63 p.1 | 0.06 | absente | — | 68 | `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 56 57.md` |
| `pq-44` | pdf-53 p.1 | 0.06 | absente | — | 30 | `legal/piece_releve_pension_rq_2026.md` |
| `pq-86` | pdf-68 p.1 | 0.05 | absente | — | — | `legal/demande_introductive_instance.md` |
| `eq-87` | email-395 | 0.05 | absente | — | — | `legal/allegation_stmt13_ete2013.md` |
| `eq-115` | email-325 | 0.05 | absente | — | — | `legal/piece_chat_caroline_chalet_3mars2012.md` |
| `eq-143` | email-411 | 0.04 | absente | — | 62 | `legal/piece_thread-6_reconstruction.md` |
| `pq-49` | pdf-64 p.1 | 0.04 | absente | — | 68 | `legal/piece_pdf-64.md` |
| `eq-198` | email-11 | 0.03 | absente | — | 68 | `legal/piece_thread-12_email-247.md` |
| `eq-145` | email-11 | 0.03 | absente | — | — | `legal/piece_thread-12_email-247.md` |
| `eq-75` | email-1 | 0.03 | absente | — | — | `legal/faits/faits_par9_2015.md` |
| `pq-15` | pdf-60 p.1 | 0.03 | absente | — | 13 | `legal/allegation_stmt66_residence_2014.md` |
| `eq-128` | email-459 | 0.03 | absente | — | 62 | `legal/organisation_preuve/2019_par_7.md` |
| `pq-99` | pdf-63 p.1 | 0.03 | absente | — | 68 | `legal/analyse/Responsabilité civile/requete novembre 2015/argument paragraphes 56 57.md` |
| `pq-47` | pdf-46 p.1 | 0.02 | absente | — | 30 | `legal/requete_secton_faits_lp.backup_2026-07-12_155744_avant_cotation.md` |
| `pq-81` | pdf-30 p.1 | 0.00 | absente | — | 62 | — |
| `pq-80` | pdf-35 p.1 | 0.00 | absente | — | 62 | — |
| `pq-41` | pdf-57 p.1 | 0.00 | absente | — | — | — |
| `pq-40` | pdf-55 p.1 | 0.00 | absente | — | 30 | — |
| `pq-39` | pdf-50 p.1 | 0.00 | absente | — | 30 | — |
| `pq-38` | pdf-56 p.1 | 0.00 | absente | — | 30 | — |
| `pq-37` | pdf-49 p.1 | 0.00 | absente | — | 30 | — |
| `pq-36` | pdf-52 p.1 | 0.00 | absente | — | 30 | — |
| `pq-35` | pdf-48 p.1 | 0.00 | absente | — | 30 | — |
| `pq-19` | pdf-62 p.1 | 0.00 | absente | — | — | — |
| `eq-217` | email-497 | 0.00 | absente | — | — | — |
| `eq-214` | email-265 | 0.00 | absente | — | — | — |
| `eq-213` | email-12 | 0.00 | absente | — | — | — |
| `eq-211` | email-17 | 0.00 | absente | — | — | — |
| `eq-210` | email-220 | 0.00 | absente | — | — | — |
| `eq-173` | email-350 | 0.00 | absente | — | — | — |
| `eq-172` | email-354 | 0.00 | absente | — | — | — |
| `eq-169` | email-141 | 0.00 | absente | — | — | — |
| `eq-164` | email-130 | 0.00 | absente | — | — | — |
| `eq-163` | email-131 | 0.00 | absente | — | — | — |
| `eq-147` | email-14 | 0.00 | absente | — | — | — |
| `eq-140` | email-469 | 0.00 | absente | — | 62 | — |
| `eq-133` | email-425 | 0.00 | absente | — | 62 | — |
| `eq-130` | email-456 | 0.00 | absente | — | 62 | — |
| `eq-92` | email-26 | 0.00 | absente | — | 9,37 | — |
| `eq-82` | email-110 | 0.00 | absente | — | 31 | — |
| `eq-78` | email-136 | 0.00 | absente | — | — | — |
| `eq-70` | email-380 | 0.00 | absente | — | 8,62 | — |
| `eq-13` | email-31 | 0.00 | absente | — | 5 | — |
| `eq-9` | email-359 | 0.00 | absente | — | 2 | — |
