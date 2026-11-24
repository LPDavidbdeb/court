# Consigne de conversion n° 1 — quatre sections vers le format des blocs

*Rédigée le 23 novembre 2026. Destinataire : un agent qui n'a pas participé aux travaux précédents. Travail mécanique : changer la forme, jamais le fond.*

## Contexte à lire d'abord

Branche : `fiches/email-16-portee-retrait` du dépôt `LPDavidbdeb/court`. Lisez, dans cet ordre :

1. `AGENTS.md` (racine) et `legal/CLAUDE.md` ;
2. `legal/amendements/01_avant_notification/blocs/METHODE.md` — en particulier les §§ 4 et 5 ;
3. `legal/amendements/01_avant_notification/blocs/conventions.md` ;
4. le bloc déjà converti, comme modèle : `blocs/par28_29_mediation.md`.

## Ce qu'il faut convertir

| Source (`sections/`) | Bloc à créer (`blocs/`) | Préfixe des étiquettes |
|---|---|---|
| `proposition_par14_17_requalification_motif.md` | `par14_17_motif.md` | `par14-` |
| `proposition_par18_entente_alleguee.md` | `par18_entente.md` | `par18-` |
| `proposition_par19_35_acces_autorite.md` | `par19_35_acces_autorite.md` | `par19-` |
| `proposition_par56_58_assurances.md` | `par56_58_assurances.md` | `par56-` |

Les fichiers sources restent intacts.

## Règles de conversion

1. **Le fond ne change pas.** Le texte de chaque paragraphe, de chaque citation et de chaque note est repris mot pour mot. Si vous remarquez une erreur, ne la corrigez pas : signalez-la dans votre compte rendu.
2. **En-tête.** Remplacez la ligne d'introduction en italique par l'en-tête YAML du modèle : `bloc`, `requete` (paragraphes de la requête de 2015 traités), `statut: à valider`, `depend_de`, `registre` (entrées P citées dans le fichier, s'il y en a), `remplace` (ce que la section remplaçait selon sa ligne d'introduction, et le fichier source).
3. **Paragraphes.** Chaque `**N.**` devient une ligne `1. ` ; chaque sous-paragraphe `  a)` devient `   a) ` (trois espaces). Un texte qui suit un sous-paragraphe sans numéro reste en retrait de trois espaces, comme dans le modèle. Les intertitres `####` sont conservés ; le titre `#` aussi.
4. **Étiquettes.** Ajoutez une étiquette `{#prefixe-mot-cle}` à la fin de tout paragraphe qui est cité par un renvoi, dans ce bloc ou dans un autre. Vous pouvez en ajouter à d'autres paragraphes ; elles doivent rester uniques dans tout le répertoire.
5. **Renvois internes.** Un renvoi à un paragraphe de la demande (« § 212 », « §§ 212 à 214 », « § 219 a) ») devient `{§etiquette}`, `{§etiq1..etiq2}` ou `{§etiquette/a}`. Les sections ont été numérotées à la suite les unes des autres : un numéro peut désigner un paragraphe d'une autre des quatre sections, ou du bloc des §§ 28 et 29 ; dans ce cas, le renvoi pointe vers l'étiquette de l'autre bloc, et ce bloc va dans `depend_de`.
6. **Ce qui reste en texte.**
   - Les paragraphes de la requête de 2015 (« paragraphe 20 », « paragraphes 14 à 17 de la requête ») : inchangés.
   - Un renvoi à un paragraphe qui n'appartient à aucun bloc (document de travail du 19 novembre, axes de la partie II) : laissé tel quel, et énuméré dans votre compte rendu.
7. **Notes.** Le texte se termine par le marqueur `<!-- fin-du-texte -->`, suivi de `## Notes de rédaction`. Dans les notes, un renvoi à un paragraphe du bloc s'écrit avec le nom de son étiquette entre accents graves (`par56-dates`), comme dans le modèle.
8. **Ordre d'assemblage.** Remplacez le contenu de `blocs/ordre.txt` par :
   ```
   par14_17_motif.md
   par18_entente.md
   par19_35_acces_autorite.md
   par28_29_mediation.md
   par56_58_assurances.md
   ```
9. **Ne modifiez aucun autre fichier** que les quatre nouveaux blocs, `blocs/ordre.txt` et `journal_modifications.md`.

## Contrôles à exécuter

```
cd legal/amendements/01_avant_notification
python3 outils/verif_citations.py blocs/par14_17_motif.md blocs/par18_entente.md blocs/par19_35_acces_autorite.md blocs/par56_58_assurances.md
python3 outils/assembler.py          # ou --sans-word si Node et le paquet docx ne sont pas installés
```

Attendus : aucune `ERREUR` ; chaque ligne `ALERTE` (numéro écrit en dur) correspond à un renvoi que la règle 6 laisse en texte, et figure dans votre compte rendu ; chaque citation `NO` existait déjà dans la source (dites-le).

## Rendu

- Travaillez sur une nouvelle branche `conv/blocs-sections`, créée à partir de `fiches/email-16-portee-retrait`. Un commit par bloc, puis un commit pour `ordre.txt` et le journal. Poussez si votre environnement le permet ; ne touchez à aucune autre branche.
- Si vous n'avez pas de clone complet, dites-le et précisez quels contrôles ont porté sur une copie partielle (`METHODE.md`, § 5).
- Compte rendu : pour chaque bloc, le nombre de paragraphes et d'étiquettes ; les renvois entre blocs créés ; les renvois laissés en texte ; les citations `NO` et leur origine ; toute erreur de fond remarquée et non corrigée.
