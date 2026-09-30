# Instance — gestion des interactions avec les défenderesses

Ce répertoire couvre la vie du dossier **505-17-016235-261** à partir de la
signification. Il ne contient pas de stratégie de fond (elle vit dans `legal/`) :
il contient ce qui doit être **fait, surveillé et répondu**, et la trace de
chaque contact.

## Les parties

| | | |
|---|---|---|
| **Demandeur** | Louis-Philippe David | 465, av. Curzon, Saint-Lambert — district de **Longueuil** |
| **Défenderesse 1** | Élise Marie Ayoub | **domicile** 245, rue Macaulay, Saint-Lambert — district de **Longueuil** |
| **Défenderesse 2** | Me Marie-Josée Ayoub, avocate | **domicile** 1091, rue Gendron, Longueuil — district de **Longueuil** |

**Adresses de notification depuis le 29 septembre 2026** — les deux se
représentent seules et ont désigné leur adresse dans leur réponse à
l'assignation :

| | Où tout s'adresse désormais |
|---|---|
| Élise Marie Ayoub | 245, rue Macaulay, Saint-Lambert (Québec) J4R 2H1 · `elise.ayoub@gmail.com` |
| Me Marie-Josée Ayoub | **Ayoub Avocats Inc., 425, rue Saint-Sulpice, Montréal (Québec) H2Y 2V7** · `mjayoub@ayoubavocats.ca` — ⚠️ **son étude**, plus son domicile |

Les deux défenderesses sont **domiciliées** dans le district où la demande est
déposée : **aucune prise pour un déclinatoire de district** (art. 167 C.p.c.).
L'adresse professionnelle élue par la défenderesse 2 est à Montréal, mais c'est
le **domicile** qui fonde la compétence territoriale — le risque reste écarté.
Aucune des deux n'a d'ailleurs soulevé la question dans sa réponse.

## Les cinq règles

Elles ne sont pas des conseils. Ce sont les règles qui compensent le fait que
la partie adverse est avocate et que le demandeur ne l'est pas.

1. **Rien de substantiel au téléphone.** Un appel ne laisse d'autre trace que
   la note que l'autre partie rédige au dossier. Si on appelle : « je préfère
   que nos échanges soient par écrit », et on met fin à l'appel. On confirme
   ensuite par courriel que l'appel a eu lieu, à quelle heure, et ce qui y a
   été dit.
2. **Jamais de réponse sur le fond le jour même.** Accuser réception le jour
   même (une ligne, sans contenu), répondre après analyse. Aucun délai
   procédural ne se compte en heures.
3. **Tout entre et tout sort par ce répertoire.** Un document reçu qui n'est
   pas dans `entrants/` n'existe pas ; un document envoyé qui n'est pas dans
   `sortants/` n'aurait pas dû partir.
4. **Aucun engagement, aucune concession, aucune renonciation dans une
   correspondance.** Les positions se prennent dans les actes de procédure,
   pas dans les lettres.
5. **Le ton est une pièce.** Voir `pieges.md` § B. Chaque message intempérant
   devient une annexe de leur demande en rejet pour abus. La froideur est une
   protection procédurale, pas une politesse.

## Les fichiers

| Fichier | Rôle |
|---|---|
| [`echeancier.md`](echeancier.md) | **Source unique** des dates qui gouvernent. Aucune date ne se calcule ailleurs. |
| [`journal.md`](journal.md) | Registre chronologique de **tout** contact, dans les deux sens. |
| [`pieges.md`](pieges.md) | Les manœuvres prévisibles, la parade de chacune, et ce qu'il ne faut jamais concéder. |
| [`protocole_instance.md`](protocole_instance.md) | Le premier vrai champ de bataille (45 j) : ce qu'on accepte, ce qu'on refuse. |
| [`communication_pieces.md`](communication_pieces.md) | Les 107 pièces : à qui, par quel support, dans quel ordre. |
| [`modeles.md`](modeles.md) | Réponses types à recopier, pour ne pas improviser sous pression. |
| `entrants/` | Un fichier par document reçu. |
| `sortants/` | Un fichier par document envoyé + la liste de vérification avant envoi. |
| `analyses/` | Une analyse par prétention adverse. |

## Le réflexe, quand quelque chose arrive

1. Déposer le document dans `entrants/` selon la convention (voir
   `entrants/README.md`) — **sans le lire en entier d'abord**, pour que
   l'horodatage soit fait à froid.
2. Inscrire une ligne dans `journal.md`.
3. Vérifier dans `echeancier.md` si le document déclenche ou modifie un délai.
4. Me le signaler pour analyse. Je produis la fiche dans `analyses/`.
5. Ne répondre qu'ensuite, par `sortants/`, après la liste de vérification.
