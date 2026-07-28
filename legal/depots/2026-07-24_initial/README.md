# Archive du dépôt initial — 24 juillet 2026

> **Répertoire gelé.** Aucun fichier de ce répertoire ne doit être modifié.
> Le travail postérieur au dépôt vit dans `legal/amendements/`.

## 1. Le dépôt, établi par la preuve

Reçu du ministère de la Justice, Palais de justice de **Longueuil**
(`preuve_de_depot.pdf`, marqué « ORIGINAL ») :

| | |
|---|---|
| **Date et heure du dépôt** | **24 juillet 2026, 15 h 19** |
| **N° de dossier (DIIN)** | **505-17-016235-261** |
| N° d’encaissement | 0585314-0035 |
| Droit de greffe | 616,00 $ (payé 700,00 $, retour 84,00 $) |
| Commit d’ancrage | `1f0af56` — « etat au dépot » |

## 2. Ce qui a été remis au greffe

**Aucun fichier n’a été transmis.** Une **copie imprimée** de la demande
introductive et du bordereau des pièces a été remise au comptoir. L’acte
déposé est donc **un document papier détenu par le greffe**; ce dépôt n’a
aucune empreinte numérique propre.

Conséquences :

1. Le référent officiel est le papier. Les fichiers conservés ici sont la
   **source d’impression**, non l’acte lui-même.
2. Il reste à établir **lequel des candidats a été imprimé** — c’est le seul
   moyen de reconstituer ce que le greffe détient. Les cinq candidats ont été
   produits le 24 juillet entre 13 h 57 et 14 h 29, et le reçu est de 15 h 19 :
   tous sont antérieurs au dépôt, aucun n’est exclu par l’horodatage.
3. Il serait utile d’obtenir du greffe une **copie conforme** de l’acte déposé,
   pour figer le référent papier et vérifier qu’il correspond bien à l’un des
   candidats.

| Candidat | Modifié le |
|---|---|
| `demande_DEPOT_2026-07-21_entete.docx` | 24 juil. 13:57 |
| `demande_DEPOT_2026-07-21_double.docx` | 24 juil. 14:14 |
| `demande_DEPOT_2026-07-21.docx` | 24 juil. 14:17 |
| `demande_DEPOT_2026-07-21.pdf` | 24 juil. 14:23 |
| `bordereau_bloc_depot.docx` | 24 juil. 14:29 |

Les sources Markdown correspondantes sont également conservées.

## 3. Le numéro de dossier manque à l’acte déposé

L’acte porte « N° : ______________ », laissé en blanc — le numéro n’est
attribué qu’au moment du dépôt. La version amendée doit porter
**505-17-016235-261**, ainsi que le bordereau, les pièces assemblées et le
cahier.

## 4. Empreintes

`SHA256SUMS` fige les huit fichiers de `candidats/`. La preuve de dépôt :
`fb9d4559bd9b408f179b65af4629a5efa85e0bbb17ea1c6083f1498b7059fe2f`.

```bash
cd legal/depots/2026-07-24_initial && shasum -a 256 -c SHA256SUMS
```

## 5. Verrou des cotes

`cotes.lock.json` fige l’identité des 106 cotes au dépôt : cote → source
résolue en base → fiche d’appui → empreinte du PDF assemblé.

État matériel constaté au dépôt :

- **P-106** n’est pas assemblée (105 PDF pour 106 cotes);
- **P-19, P-40, P-42, P-58 à P-64** sont des placeholders dans l’assemblage.
  Leur empreinte n’est volontairement pas figée : c’est la pièce réelle qui la
  fixera, sans que la cote change de source.

**Les originaux de P-19, P-40 et P-42 sont en main** — `media/evidence_files/`,
liés par `Document.file_source` (documents 1, 2 et 3). Ce sont des numérisations
des actes originaux (16, 5 et 4 pages), sans couche texte. Leur statut de
placeholder est un défaut de câblage de l’assemblage, **non** une absence de
preuve. Voir `legal/METHODOLOGIE_POST_DEPOT.md` §9.2.

## 6. État de la demande déposée

Numérotation : 179 paragraphes numérotés de 1 à 241, soit **62 numéros
manquants**, plus des paragraphes suffixés (`22-A`). Des paragraphes ont été
retirés sans renumérotation. Toute table de concordance ancien/nouveau devra
partir de cette numérotation lacunaire, et les renvois internes devront être
revalidés un à un.
