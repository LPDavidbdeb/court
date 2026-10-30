# Prompt — analyse et impact de la contre-proposition de protocole de Me Timmons

> À remettre tel quel à un agent d'analyse. Il ne lit **aucune** analyse
> antérieure : son travail doit être indépendant. Complément du mandat de
> validation (`2026-10-30_mandat_validation_externe.md`) : celui-ci critique
> l'analyse de Claude, le présent prompt mesure les **conséquences**.

> 🔴 **Branche : `epic/E01-numerotation-concordance`**, et non `main`. Tous les
> chemins ci-dessous s'y trouvent (dépôt `LPDavidbdeb/court`, commit `46e9a4f`
> ou postérieur). Sur `main`, les documents du 29 octobre n'existent pas.

---

## Le contexte

Tu analyses un dossier civil réel au Québec : Cour supérieure, district de
Longueuil, n° **505-17-016235-261**. Le demandeur, Louis-Philippe David, agit
**seul**, sans avocat. La défenderesse Me Marie-Josée Ayoub est représentée
par Me Patricia Timmons (contentieux du Fonds d'assurance du Barreau). La
défenderesse Élise Marie Ayoub agit seule.

| Date | Fait |
|---|---|
| 24 juill. 2026 | dépôt de la demande en dommages-intérêts |
| 17 sept. 2026 | signification aux deux défenderesses |
| 29 oct. 2026, 13 h 47 | le demandeur notifie sa **proposition de protocole** (formulaire prescrit, signé) |
| 29 oct. 2026, 17 h 24 | Me Timmons lui soumet **son propre protocole**, « en y incorporant certains de vos points », à signer par les trois parties |
| **2 nov. 2026** | dépôt du protocole au greffe, **au plus tard** (45 jours de la signification) |

**Ta question** : quelles seraient, pour le demandeur, les conséquences
d'accepter, en tout ou en partie, la proposition de Me Timmons ? Et que doit-il
faire d'ici le 2 novembre ?

## Les documents — lis-les, et seulement eux

| Document | Chemin |
|---|---|
| Proposition du demandeur (PDF signé, notifié) | `legal/instance/sortants/2026-10-29_proposition_protocole_instance_signee.pdf` |
| Proposition de Me Timmons | `legal/instance/entrants/2026-10-29_avocat_contre-proposition-protocole/Protocole_instance_Matiere_civile_Pat.docx` |
| Son courriel | `legal/instance/entrants/2026-10-29_avocat_contre-proposition-protocole.md` |
| La demande déposée — objet (§ 1), prescription (§§ 234-236), conclusions | `legal/depots/2026-07-24_initial/candidats/demande_DEPOT_2026-07-21.pdf` |
| Code de procédure civile | `legal/analyse/Responsabilité civile/code procédures civiles.pdf` |
| Code civil du Québec | `legal/analyse/Responsabilité civile/CCQ-1991.pdf` |
| Les échanges, dans l'ordre | `legal/instance/journal.md` |

**N'ouvre pas** les autres fichiers de `legal/instance/analyses/`, ni
`guide_rubriques_protocole.md`, ni `protocole_instance.md` : ils contiennent
des analyses déjà faites, qui ne doivent pas orienter la tienne.

## Le travail

### 1. L'inventaire des différences

Compare les deux formulaires **rubrique par rubrique** : page de présentation,
titre, rubriques 1 à 42, blocs de signature. Une ligne par différence.

### 2. L'impact de chaque différence

Pour chaque différence, mesure ses conséquences sur ces sept axes, et seulement
ceux qui s'appliquent :

| Axe | La question |
|---|---|
| **A. Prescription** | La différence touche-t-elle la qualification du recours, le délai applicable (art. 2925 et 2929 C.c.Q.) ou l'interruption acquise (art. 2892, 2894 C.c.Q.) ? |
| **B. Délai de rigueur** | Change-t-elle la date de la demande d'inscription, sa possible prolongation, ou le risque de désistement présumé (art. 173, 177 C.p.c.) ? |
| **C. Calendrier** | Rend-elle la suite (défense, modification de la demande, interrogatoires, communication des pièces) praticable ou non ? |
| **D. Objet du litige** | Le protocole signé fixe-t-il les questions en litige d'une façon conforme à l'objet et aux conclusions de la demande ? Que ne pourrait-on plus débattre, ou plus facilement ? |
| **E. Connaissance de la défense** | La forme de la défense permet-elle de savoir ce qui est admis ou nié (art. 102, 170, 171 C.p.c.) ? |
| **F. Force obligatoire** | Une fois le protocole accepté, que lie-t-il, et que peut-on encore modifier sans le tribunal (art. 150 C.p.c.) ? |
| **G. Exposition personnelle et coûts** | Interrogatoires du demandeur ; sanctions du non-respect du protocole (art. 341, 342 C.p.c.) |

Classe ensuite chaque différence : **favorable**, **défavorable** ou **neutre**
pour le demandeur, avec la raison.

### 3. Les scénarios

| Scénario | Ce que fait le demandeur |
|---|---|
| **S1** | il signe le protocole de Me Timmons tel quel |
| **S2** | il dépose lundi sa proposition telle que notifiée le 29 (art. 152) |
| **S3** | il dépose une proposition **révisée**, qui reprend les points favorables de Me Timmons |
| **S4** | il négocie d'ici lundi un protocole commun, signé par les trois parties |

Pour chacun : ce qui devient obligatoire, et à quelle date ; les risques sur les
axes A à G ; ce que le Code prévoit ensuite, notamment l'art. 152 (« le tribunal
peut soit convoquer les parties pour établir le protocole soit l'établir, même
d'office ») ; et ce que S3 et S4 exigent d'ici lundi (art. 107 : notifier
d'abord, déposer ensuite avec la preuve de notification).

### 4. La recommandation

- Le scénario que tu recommandes, et pourquoi.
- Les points de la proposition de Me Timmons à **accepter**, à **refuser**, à
  **renvoyer au tribunal**.
- Le texte d'une réponse à Me Timmons, envoyée avant le dépôt : sobre, sans
  argument de fond, sans reproche.

## Les règles

- **Cite le texte** des articles, lu dans les PDF fournis. Jamais de mémoire.
- **Distingue** ce que dit le texte de ce que tu en déduis.
- **Pas de jurisprudence** citée de mémoire. Si une question l'exige, dis-le.
- **N'invente aucun fait.** Ce que les documents n'établissent pas va à la
  section des incertitudes.
- **Lecture seule** : ne modifie aucun fichier, n'écris pas en base, ne
  contacte personne.

## Le livrable

Un seul fichier : `legal/instance/analyses/2026-10-30_impact_proposition_timmons_RAPPORT.md`.

1. Le tableau des différences, avec leur classement.
2. L'impact par axe : un tableau des différences × axes A à G.
3. Les quatre scénarios, comparés.
4. La recommandation, les points à accepter ou à refuser, et le texte de réponse.
5. Les incertitudes : ce que tu n'as pas pu établir, et ce qui demanderait de
   la jurisprudence ou l'avis d'un avocat.
