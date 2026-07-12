# Inventaire des pièces référencées dans les contestations

## Périmètre

- 15 fichiers Markdown dans `legal/faits/`;
- 19 fichiers Markdown dans `legal/pont/`;
- références dédupliquées;
- références relevées sous forme de liens `piece_*.md` ou de mentions directes d'un modèle et d'une PK;
- modèles et PK des fichiers descriptifs vérifiés dans la base Django locale lorsque la correspondance n'était pas donnée par le nom du fichier.

## Inventaire Django consolidé

| Modèle Django | Nombre de PK distinctes | PK référencées |
|---|---:|---|
| `document_manager.Document` | 3 | 1, 2, 3 |
| `email_manager.Email` | 115 | 1, 3, 5, 6, 8, 16, 20, 22, 27, 29, 32-35, 37-40, 42, 45, 47, 51, 53-56, 58-61, 64, 66-69, 71, 78, 81, 84, 85, 91, 106, 111, 112, 114, 116, 118, 120, 121, 136, 137, 163, 167, 171-184, 267, 270, 271, 275, 295, 305, 306, 330, 343, 347, 349-352, 355, 357, 360-365, 369, 371, 382, 383, 399, 401, 404, 443-449, 462, 475, 484-486, 488, 535, 590, 603, 615, 633, 642 |
| `email_manager.EmailThread` | 11 | 1, 6, 16, 18, 26, 27, 63, 80, 109, 111, 159 |
| `events.Event` | 98 | 25, 36, 37, 46, 52, 54, 62, 75-83, 88, 106, 113-125, 136, 140, 150, 171-180, 213-214, 235-267, 274, 278, 284, 291, 312-326 |
| `googlechat_manager.ChatMessage` | 36 | 111-146 |
| `googlechat_manager.ChatSequence` | 8 | 3-6, 8-11 |
| `pdf_manager.PDFDocument` | 39 | 1, 2, 3, 5, 6, 7, 11-16, 26, 30, 35, 45-60, 63, 64, 80-82, 90-92 |
| `photos.Photo` | 8 | 4517-4522, 4551, 4558 |
| `photos.PhotoDocument` | 6 | 1, 2, 3, 5, 13, 17 |
| **Total** | **324 objets Django distincts** | Hors objets non individualisés de la pièce d'agrégation |

Les listes et plages compactes des contestations (`Emails id=…`, `Events id=…`, `ChatMessages id=…`) ont été développées lors du réaudit chronologique. Les 324 lignes sont classées dans le classeur `inventaire_pieces_contestations_chronologique.xlsx` : 318 objets ont une date exploitable et 6 sont rangés à la fin sans date probante.

## Correspondances vérifiées pour les noms descriptifs

| Référence citée | Modèle Django | PK | Observation |
|---|---|---:|---|
| `piece_avis_cotisation_pere_2018.md` | `pdf_manager.PDFDocument` | 35 | Vérifié par le chemin du PDF en base |
| `piece_avis_cotisation_pere_2019.md` | `pdf_manager.PDFDocument` | 30 | Vérifié par le chemin du PDF en base |
| `piece_denonciation_declinatoire_2023.md` | `document_manager.Document` | 2 | Source de vérité indiquée dans la pièce |
| `piece_modele_fixation_pension.md` | `pdf_manager.PDFDocument` | 26 | Vérifié par le chemin du PDF en base |
| `piece_p2_messages_7avril2015.md` | `photos.PhotoDocument` | 3 | Le document photo contient `photos.Photo` PK 4526 |
| `piece_thread-109.md` | `email_manager.EmailThread` | 109 | Source de vérité indiquée dans la pièce |
| `piece_thread-111_congediement_bnc.md` | `email_manager.EmailThread` | 111 | Source de vérité indiquée dans la pièce |
| `piece_thread-6_reconstruction.md` | `email_manager.EmailThread` | 6 | Source de vérité indiquée dans la pièce |
| `piece_thread-ecrement_2015.md` | `email_manager.EmailThread` | 16 | Thread vérifié en base; pièce composite de 14 courriels |
| `piece_thread-ecrement_2015.md` | `email_manager.Email` | 20, 172–184 selon la liste ci-dessous | PK exactes : 20, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184 |
| `piece_vacances_2013_cape_cod_cuba_chalet.md` | plusieurs modèles | plusieurs PK | Voir le détail ci-dessous |

### Détail de `piece_vacances_2013_cape_cod_cuba_chalet.md`

| Modèle Django | PK |
|---|---|
| `pdf_manager.PDFDocument` | 1 |
| `email_manager.EmailThread` | 63, 80 |
| `email_manager.Email` | 78, 349, 535, 270 |

## Références sans PK unique

| Référence citée | Modèle / nature | PK | Motif |
|---|---|---|---|
| `piece_tableau_recap_evenements.md` | Agrégation produite depuis `events.Event` | multiple | Le tableau agrège 259 événements et 1 521 photos; ce n'est pas un objet Django autonome à PK unique. Les 34 PK d'événements citées individuellement dans les contestations figurent dans l'inventaire consolidé. |
| `piece_jurisprudence_cs-mg-2005.md` | Autorité juridique conservée comme fichier de pièce | aucune PK repérée | Aucun enregistrement Django correspondant n'a été trouvé par le titre ou le nom de source dans `pdf_manager.PDFDocument`. |

## Anomalie de base repérée

| Modèle Django | PK | Statut |
|---|---:|---|
| `email_manager.Email` | 449 | La PK est comprise dans la plage `443-449` citée par `faits_par9_2015.md`, mais elle est absente de la base locale. |

## Limites de cette première passe

- Les cotes textuelles comme `P-64 à P-354` ne sont pas converties en PK sans table de correspondance explicite.
- Une absence alléguée de pièce n'est pas comptée comme une pièce.
- Les renvois vers d'autres fichiers `faits_*.md` ou `pont_*.md` ne sont pas comptés comme des pièces.
- Le classeur chronologique rattache chaque objet aux fichiers `faits` et `pont` où sa référence a été relevée; il ne produit pas encore une matrice par paragraphe contesté.
