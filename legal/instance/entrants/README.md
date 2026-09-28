# Documents reçus

Un fichier par document reçu, **sans exception** — lettre, courriel, acte de
procédure, avis du greffe, message transmis par un tiers.

**Nom du fichier :** `AAAA-MM-JJ_<qui>_<objet-court>.md`
— `qui` ∈ `elise`, `ayoub`, `avocat`, `greffe`, `huissier`, `tiers`.
Exemple : `2026-10-02_ayoub_reponse-assignation.md`.

**En-tête obligatoire** (à remplir avant de lire le document en entier) :

```markdown
---
recu_le: AAAA-MM-JJ
heure: HH:MM
de: 
canal:            # courriel | poste | huissier | greffe | main propre | autre
piece_jointe:     # oui/non — lister
delai_declenche:  # ou "aucun" — vérifier dans ../echeancier.md
analyse:          # lien vers ../analyses/... quand elle existe
---
```

Puis : le contenu intégral, **sans résumé ni commentaire**. Les commentaires
vont dans `../analyses/`.

**Règle.** L'en-tête se remplit avant la lecture complète. Un document lu avant
d'être horodaté est un document dont on se souviendra mal.
