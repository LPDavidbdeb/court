# `_sources_verifiees/` — documents originaux vérifiés

Contient les **originaux** des pièces, copiés depuis la base de données (média Django) après confirmation de `(model, PK)` et calcul du **hash** (Phase A, étapes A2-A4). Ces fichiers — non les extraits `piece_*.md` — sont ce qui sera **communiqué à la partie adverse** (art. 145/247 C.p.c.).

## Conventions

- **Sources natives** (`PDFDocument`, `Email`, `PhotoDocument`) : un fichier original par source, dédupliqué par hash (un même hash n'est copié qu'une fois).
- **Faits agrégés/structurels** (comptes d'`Event`, densité) : la pièce est un **tableau + liasse générés** ; ce dossier héberge alors les **fichiers constitutifs** (photos, exports) + l'**index de liasse** produit.
- **Nommage** :
  - *avant gel des cotes* — nom d'origine ou `<model>-<PK>.<ext>` (staging) ;
  - *après gel (Phase B)* — nom définitif de dépôt `P-<N>[_<k>]_<désignation courte>.<ext>`.
- **Recevabilité** : une source marquée 🟡/🔴/🔵 au registre est copiée ici pour vérification, mais **n'est pas versée** au dépôt tant que sa recevabilité n'est pas tranchée.

*(Vide pour l'instant — se remplit à la collecte.)*
