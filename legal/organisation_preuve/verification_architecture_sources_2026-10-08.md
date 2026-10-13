# Vérification de l’architecture des fiches et des sources — 8 octobre 2026

Contrôle demandé : comprendre le nommage des fichiers `legal/piece*.md`, retrouver une source de chaque modèle de preuve et comparer les contenus. Les sources primaires de l’échantillon ont toutes été retrouvées. La correspondance documentaire est confirmée, mais la fidélité textuelle et certaines métadonnées présentent les écarts décrits ci-dessous.

La base a été consultée dans des transactions PostgreSQL en **lecture seule**, avec `transaction_read_only=on`. Aucune donnée, fiche existante, cote ou archive de dépôt n’a été modifiée. Ce rapport est un nouvel artefact de vérification; il ne constitue pas une correction des sources ni une validation de l’ensemble du corpus.

## Architecture constatée

Les conventions documentaires ont été lues dans `PROJECT_CONTEXT.md`, `legal/METHODOLOGIE_POST_DEPOT.md`, `legal/CLAUDE.md` et `legal/expose/README.md`. Les relations ont été vérifiées dans les modèles Django, `core/piece_import.py`, les modules d’audit des pièces et le renderer documentaire.

**Identité technique : `(modèle, PK)`.** Une PK ne suffit pas seule : `PDFDocument:9`, `PhotoDocument:9` et `Email:9` sont trois identités différentes. Une cote procédurale P-n constitue encore une autre identité. Le corpus courant comporte 296 fiches `piece*.md` directement dans `legal/`; leur intégralité n’a pas été auditée.

| Nommage / unité | Résolution et relations |
|---|---|
| `piece_thread-T_email-E.md` | Source primaire `Email:E`; `Email.thread_id` doit être T. T désigne la PK de `EmailThread`, distincte de son champ `thread_id`, qui contient l’identifiant d’export. |
| `piece_thread-T.md` | `EmailThread:T`, puis sa relation inverse `emails`. Les citations imbriquées dans les corps peuvent répéter les messages précédents. |
| `piece_thread-T_emails-E1-E2.md` | Fiche portant sur plusieurs `Email` du même `EmailThread:T`. Les nombres après `emails-` sont une sélection explicite, pas nécessairement un intervalle ni tous les membres du fil. L’analyse est importée sur le fil. |
| `piece_pdf-P.md` | `PDFDocument:P`, son fichier PDF et sa transcription dans `ai_analysis` / la propriété `transcription`. |
| `piece_photodoc-D.md` | `PhotoDocument:D`, puis `photos` : les images composent le document. Le nombre d’images ne correspond pas à un nombre de documents distincts. |
| Ancien renvoi `piece_photo-P.md` | `Photo:P`, avec remontée vers son `PhotoDocument` lorsqu’il existe. Le registre courant ne traite pas cette famille comme une famille à importer. Aucun fichier autonome `piece_photo-*.md` n’a été trouvé directement dans `legal/`. |
| `piece_event-E.md` | `Event:E`; description dans `explanation`, bornes dans `debut` / `fin`; images dans `linked_photos` via `SupportingEvidenceLinkedPhotos`. Un événement peut aussi pointer vers `linked_email`. |
| `piece_events-E1-E2.md` | Fiche composite : plusieurs `Event` explicitement identifiés dans son contenu. Elle ne doit pas être réduite au premier identifiant. |
| `piece_document-D.md` | `Document:D` → `nodes` (`LibraryNode`) → `content_object`, notamment `Statement.text`. Les paragraphes sont numérotés à la lecture suivant l’ordre des chemins et la profondeur des nœuds; la PK d’un `Statement` n’est pas son numéro de paragraphe. |
| `piece_chatsequence-S.md` | `ChatSequence:S` → `messages` (`ChatMessage`) → auteur `ChatParticipant`. Chaque message possède aussi son `ChatThread`, son horodatage et `raw_data`. Une séquence peut sélectionner seulement certains messages ou une seule voix. |

Les fiches comportent des métadonnées, des citations, des coupures et de l’analyse. La comparaison doit donc distinguer l’extrait documentaire de l’interprétation. Sur `Email`, `EmailThread`, `PDFDocument` et `PhotoDocument`, `analyse` est l’analyse HTML importée du corpus et `analyse_source` indique son fichier; ces champs sont distincts du texte du courriel ou de la transcription de l’original. Leur concordance ne suffit pas à prouver la fidélité de la citation à la source primaire.

**Horodatages :** les courriels ont été convertis d’UTC vers `America/Toronto` pour comparer les heures locales. Selon la convention documentée du projet, les horodatages photographiques et les bornes des `Event` ont été lus comme des heures murales, sans conversion de fuseau.

## Échantillon vérifié

| Fiche | Source retrouvée | Comparaison réalisée et résultat |
|---|---|---|
| [piece_thread-17_email-21.md](../piece_thread-17_email-21.md) | `Email:21` → `EmailThread:17` | Citation « nicolas est malade je reste a la maison » retrouvée dans `body_plain_text`; auteur, destinataires, fil et date du 3 août 2015 concordent. Heure locale : 07:39:09 HAE. |
| [piece_thread-26_emails-33-32.md](../piece_thread-26_emails-33-32.md) | `EmailThread:26` → `Email:33`, `Email:32` | Deux citations retrouvées. Dates locales conformes : 29 juillet 2013 à 18:49 et 21:58 HAE. Le fil contient quatre courriels : la fiche en sélectionne deux. |
| [piece_thread-109.md](../piece_thread-109.md) | `EmailThread:109` → 443, 444, 445, 446, 447, 448, 349 | Sept membres retrouvés, tous du 30 juin 2013. Les passages propres transcrits concordent après homogénéisation des espaces et retrait du balisage. Le remplacement du lien Groupon est explicitement signalé dans la fiche; les chaînes citées ne sont pas intégralement recopiées. |
| [piece_pdf-66.md](../piece_pdf-66.md) | `PDFDocument:66` | Date 2024-01-23 et données salariales confirmées dans la transcription BD et le PDF lié, également lu visuellement : Québec 21,00 $/h; Montérégie 18,10 / 20,50 / 26,83 $/h. Les calculs annualisés appartiennent à l’analyse. |
| [piece_photodoc-9.md](../piece_photodoc-9.md) | `PhotoDocument:9` → `Photo:4551` | Relation et original JPEG confirmés. Corps du courriel conforme à la transcription et à l’image; adresse de l’expéditrice différente dans la fiche, voir ci-dessous. Son en-tête conserve l’ancien nom `photo-4551`. |
| [piece_photodoc-18.md](../piece_photodoc-18.md) | `PhotoDocument:18` → `Photo:4562` | Titre, PK, relation et chemin de fichier concordent. Image lue : formulaire du père préparé le 15 octobre 2019, tampon du 4 novembre 2019; salaire père 0, assurance-emploi 7 658, REER 35 000, total 42 658; mère 112 569,08. La comparaison avec le PDF 82 n’a pas été réalisée. |
| [piece_event-19.md](../piece_event-19.md) | `Event:19` → `Photo:3583` | Description actuelle exactement conforme, date 2010-06-13, une photo, bornes 20:37:10. L’image présente un spectacle de danse; l’identification des personnes et l’attribution de la prise de vue ne sont pas établies par l’image seule. |
| [piece_events-83-84.md](../piece_events-83-84.md) | `Event:83`, `Event:84` → 16 photos | Deux événements du 2 juillet 2011; 4 + 12 photos; bornes 10:23–10:45 et 15:22–15:49 conformes. Les explications actuelles sont en français, tandis que la fiche cite les anciennes versions anglaises. Les 16 images n’ont pas été examinées individuellement. |
| [piece_document-3.md](../piece_document-3.md) | `Document:3` → 36 `LibraryNode` → `Statement` | Titre, fichier source et structure retrouvés; 23 paragraphes principaux. Dix-neuf concordent suivant la méthode ci-dessous; quatre présentent des différences. Les quatre pages du PDF original ont été lues visuellement pour examiner les écarts. |
| [piece_chatsequence-8.md](../piece_chatsequence-8.md) | `ChatSequence:8` → six `ChatMessage`, dont 405 et 417 | Citations retrouvées dans les messages 405 et 417; date du 4 novembre 2014 conforme. Pour les six messages, texte et auteur concordent avec `raw_data`. Les six auteurs sont Élise : la séquence ne contient pas la voix de LP. |

Ces contrôles couvrent les neuf modèles sources reconnus par `case_manager.evidence_audit.MODEL_CLASSES` : `PDFDocument`, `Document`, `Email`, `EmailThread`, `Event`, `Photo`, `PhotoDocument`, `ChatMessage`, `ChatSequence`. `Photo` et `ChatMessage` ont été contrôlés comme éléments des regroupements; `LibraryNode` et `Statement` l’ont été comme composants documentaires. Aucun fichier `piece_video*.md` n’a été trouvé dans ce périmètre.

## Écarts à conserver dans la lecture

Pour `Document:3`, la comparaison a retiré le balisage Markdown, homogénéisé les espaces, la casse et les apostrophes et admis les coupures explicitement marquées `[…]`. Il s’agit d’une concordance d’extraits, pas d’une identité octet par octet.

| Passage | Fiche | Base | Contrôle dans le PDF original |
|---|---|---|---|
| §11 → `Statement:116` | « À ce jour » | « ce jour » | La page 3 comporte « À ce jour » : le mot initial manque en base. |
| §12 → `Statement:117` | « un 5 et ½ » | « un 5 et 21 » suivi d’un caractère invisible | La page 3 comporte « un 5 et ½ » : la fraction est mal transcrite en base. |
| §16 → `Statement:121` | « l’intention du défendeur est d’aller » | « l’intention du défendeur et d’aller » | La page 3 porte « et d’aller » : la fiche corrige la graphie de l’original. |
| §18 → `Statement:123` | « s’est vue rejetée » | « s’est vu rejetée » | La page 3 porte « s’est vu rejetée » : la fiche corrige aussi la graphie de l’original. |

La fiche indique encore que `Document.document_original_date` est erroné et vaut `2019-09-21`. Au contrôle, ce champ vaut déjà **`2019-10-21`**, conformément à la signature et au serment de la page 4. L’avertissement décrit donc un ancien état de la base.

Dans `piece_photodoc-9.md`, l’adresse est transcrite `claudia.ecrement@videotron.ca`. L’image et les champs `description` / `ai_analysis` portent **`claudia.screment@videotron.ca`**. Le corps cité reste concordant, mais l’en-tête n’est pas entièrement fidèle.

Dans `piece_chatsequence-8.md`, la présentation « échange Élise ↔ LP » ne décrit pas le contenu effectivement sélectionné : **six messages d’Élise seulement**. Les citations sont conformes; la complétude de l’échange n’est pas confirmée.

## Concordance des analyses importées

Six analyses ont été comparées à une nouvelle conversion en mémoire par `core.piece_import.convertir`, sans import ni écriture en base. Les six champs `analyse_source` correspondent au nom de la fiche testée.

- **HTML exactement identique pour quatre fiches :** Email 21, fil 26, PhotoDocument 9 et PhotoDocument 18.
- **Fil 109 :** la fiche actuelle possède une ligne supplémentaire « Analyse ciblée » renvoyant à `these_refus_30juin2013.md`, absente de l’analyse importée. La transcription des sept courriels reste concordante.
- **PDF 66 :** le texte visible de l’analyse est identique après retrait des marqueurs de renvois non résolus. Le HTML diffère pour le lien secondaire `piece_pdf-12.md` : l’analyse stockée possède `/pdfs/pdf/12/`, tandis que la reconversion ne résout pas ce renvoi. Le contrôle ne permet pas de conclure à sa cause.

Les contrôles programmatiques ciblés ont produit 48 résultats, dont 44 concordants et les quatre différences textuelles de `Document:3`. Les écarts d’adresse, de date descriptive, de sélection des interlocuteurs et d’analyse importée ont été examinés séparément. Ce décompte ne mesure pas la conformité de toutes les fiches ni la véracité des conclusions analytiques.

Originaux PDF consultés : [PDFDocument 66](../../media/pdf_documents/Représentantreprésentante_.pdf) et [Document 3](../../media/evidence_files/déclaration_assermentée_de_la_demanderesse.pdf).
