# Outiller les envois : bordereaux, journal des transmissions, trace des dispositions

> **Question du demandeur, 13 octobre 2026** : bâtir un protocole d'envoi utilisant
> l'API Gmail, journaliser les envois en base sous forme de « plumitif maison »,
> et tenir une trace des articles du C.p.c. et du C.c.Q. — **l'investissement en
> vaut-il le gain ?**
>
> **Réponse courte : oui pour deux tiers, non pour le tiers le plus coûteux — et
> la pièce la plus utile n'est pas dans la question.** Ce qui manque n'est pas
> un envoyeur : c'est un **générateur de bordereaux** au sens de l'art. 134 C.p.c.

---

## 1. Ce qui existe déjà

| Composant | État | Conséquence |
|---|---|---|
| `DAL/gmailDAO.py` | opérationnel, scope **`gmail.readonly`** uniquement | lit et archive ; **ne peut pas envoyer** |
| `download_raw_eml_file(message_id, path)` | existe | le `.eml` natif, en-têtes intacts, est déjà archivable |
| `email_manager.Email` | `message_id` unique, `sender`, `recipients_to/cc/bcc`, `date_sent`, `eml_file`, `eml_file_path`, `sender_protagonist`, `recipient_protagonists`, `analyse`, `note` | **la table de journal existe déjà** |
| `email_manager.EmailThread` | `thread_id` unique, `protagonist`, `subject` | le fil est déjà modélisé |

➜ **La moitié « ingestion » est entièrement bâtie.** Rien à réécrire.

## 2. Les trois demandes n'ont pas le même rendement

### 2.1 Envoyer par l'API — ⚠️ le seul morceau que je déconseille

**Coût** : nouveau scope OAuth (`gmail.send` ou `gmail.compose`), nouveau
consentement, nouveau jeton, assemblage MIME avec pièces jointes, gestion
d'erreurs.

**Coût caché, et c'est le vrai** : l'envoi automatisé **supprime la friction sur
laquelle le dossier repose**. La règle n° 2 de [`README.md`](README.md) est
« jamais de réponse sur le fond le jour même », et la liste de vérification de
[`sortants/README.md`](sortants/README.md) s'ouvre sur « *Rien ne m'oblige à
envoyer ceci aujourd'hui* ». Un envoi déclenché par un script travaille contre
cette architecture.

**Gain réel, et il existe** : la fidélité — garantir que ce qui part est
exactement ce qui est au fichier, sans dérive de copier-coller.

➜ **Le gain s'obtient sans le coût : produire un BROUILLON, pas un envoi.**
Scope `gmail.compose`, le script assemble le brouillon depuis le `.md` du
`sortants/` + les pièces jointes + le bordereau, et le dépose dans les brouillons
Gmail. Le demandeur l'ouvre, le relit, et appuie lui-même. Fidélité conservée,
friction conservée, **envoi accidentel impossible**.

*Variante à coût zéro, si l'on veut éviter tout nouveau scope* : générer un
fichier `.eml` localement et le glisser dans Gmail. Plus rustique, aucune
dépendance nouvelle.

### 2.2 Le journal des transmissions — ✅ oui, et c'est presque gratuit

Envoyer depuis Gmail, puis **ingérer le message envoyé** avec le DAO existant.
La ligne `Email` **est** l'entrée de journal ; le `.eml` **est** la preuve.

**Pourquoi c'est strictement meilleur que la ligne écrite à la main** — et le
dossier l'a déjà établi, en sens inverse. Les courriels d'Élise et de Timmons ont
été analysés par leurs **en-têtes** : `Message-ID`, `Date` à la seconde,
`In-Reply-To`, `dkim=pass`, `spf=pass`, `dmarc=pass`. Le courrier sortant du
demandeur porte exactement les mêmes. Une ligne de `journal.md` est **son
affirmation** ; un `.eml` horodaté et signé est une **preuve**.

**Coût** : une commande qui ingère par requête (`from:me`, plage de dates), plus
de quoi rattacher la ligne au fichier du `sortants/` et la marquer comme acte de
l'instance. Petit.

### 2.3 La trace des dispositions — ⏸️ pas maintenant

`legal_reference_dispositions_verifiees.md` fait déjà le travail, et le fait
bien : texte vérifié, date de vérification, source locale.

La modéliser en base n'achète de la valeur que pour **un** usage, et il n'est pas
encore là : **lier les dispositions aux `Statement`** de la demande modifiée,
pour vérifier la couverture — *quel paragraphe repose sur quelle disposition*.
C'est utile, mais c'est **en aval de la réécriture**, et c'est une autre
fonctionnalité que « garder une trace des articles ».

➜ Garder le Markdown. Y revenir quand la question « quel § repose sur quoi ? » se
posera pour de vrai.

## 3. 🔴 Ce qui manque et qui n'était pas dans la question : le bordereau

**L'art. 134 C.p.c. prescrit son contenu, poste par poste** :

> « Le bordereau indique **la nature du document transmis**, **le numéro du
> dossier** du tribunal, **le nom de l'expéditeur et du destinataire et leurs
> coordonnées**, de même que **le lieu, la date et l'heure et les minutes de la
> transmission**; il doit contenir également, à moins que la transmission ne soit
> effectuée par l'entremise d'un huissier, **l'information nécessaire pour
> permettre au destinataire de vérifier l'intégrité de la transmission**. Ce
> bordereau n'est produit au greffe que si une partie le demande. »

Quatre raisons d'en faire la première pièce d'outillage :

1. **C'est la preuve de la notification** (art. 134 al. 1), pour chaque acte
   sortant d'ici l'instruction. Les deux défenderesses en ont produit un le
   29 septembre ; Timmons aussi le 5 octobre. Le demandeur n'en a pas encore.
2. **Les champs sont prescrits** : rien à concevoir, il n'y a qu'à les remplir —
   et tous existent déjà en base ou dans les en-têtes du message.
3. 🔴 **« L'information nécessaire pour permettre de vérifier l'intégrité » = les
   empreintes SHA-256.** C'est exactement ce que les deux lettres promettent
   déjà : « Chaque lot comportera un index ainsi que les empreintes SHA-256 des
   fichiers transmis » (`sortants/2026-10-07_…` et `sortants/2026-10-13_…`).
   **Le bordereau de l'art. 134 et le manifeste du § 7 de
   [`communication_pieces.md`](communication_pieces.md) sont le même artefact.**
   Une seule chose à bâtir, deux obligations servies.
4. **« Produit au greffe que si une partie le demande »** — donc il faut pouvoir
   le reproduire des mois plus tard. Généré depuis la base : toujours
   reproductible. Tenu à la main : il dérive.

### ⚠️ L'ordre des opérations découle du texte

Le bordereau doit porter **l'heure et les minutes de la transmission**. Un
bordereau produit *avant* l'envoi ne peut pas les connaître. D'où la séquence :

```
1. brouillon assemblé (§ 2.1) + bordereau provisoire en pièce jointe
2. relecture humaine, envoi manuel depuis Gmail
3. ingestion du message envoyé (§ 2.2)
4. bordereau DÉFINITIF estampillé depuis l'en-tête Date réel, archivé
```

L'étape 3 n'est pas de la comptabilité : **c'est elle qui rend le bordereau
exact.**

## 4. Verdict sur l'investissement

| Morceau | Verdict | Motif |
|---|---|---|
| **Générateur de bordereaux** (art. 134 + SHA-256) | ✅ **à faire, en premier** | Contenu prescrit, obligation récurrente, converge avec le manifeste déjà promis |
| **Journal des transmissions** par ingestion du sortant | ✅ **à faire** | Presque gratuit, et transforme une affirmation en preuve |
| **Brouillon** via `gmail.compose` | 🟡 **utile, optionnel** | Garantit la fidélité sans supprimer la friction |
| **Envoi automatisé** | ❌ **non** | Nouveau scope, et travaille contre la règle n° 2 |
| **Dispositions en base** | ⏸️ **plus tard** | Le Markdown suffit ; la version utile (dispositions ↔ `Statement`) est en aval de la réécriture |

### ⚠️ Et la question du moment

Le protocole est au **1er novembre** et la réécriture est le chemin critique.
Bâtir de l'outillage y prend du temps.

Ce qui justifie quand même de faire les deux premiers morceaux **maintenant** :
ils servent **dès le prochain envoi** — les deux lettres qui attendent — puis à
chaque acte jusqu'à l'instruction. Le reste attend.

➜ **Décision prise le 13 octobre : bordereaux et journal implémentés, envoi
automatisé écarté.** Ce qui suit décrit ce qui tourne.

---

## 5. Ce qui a été construit

| Pièce | Où |
|---|---|
| `DestinataireInstance`, `Transmission`, `FichierTransmis` | `case_manager/models.py` (migration 0014) |
| Empreintes, vérifications, rendu du bordereau | `case_manager/transmission_service.py` |
| `init_destinataires` | peuple le registre des adresses et de leurs fenêtres |
| `preparer_transmission` | empreinte, vérifie, produit le bordereau **provisoire** |
| `confirmer_transmission` | rattache le message envoyé, estampe le bordereau **définitif** |

**Aucune de ces commandes n'envoie quoi que ce soit**, et aucune ne le pourra :
le scope OAuth du projet reste `gmail.readonly`, et le dépôt ne contient aucun
appel d'envoi. L'envoi demeure un geste manuel, fait depuis Gmail.

⚠️ **Lever une ambiguïté de vocabulaire, avant qu'elle ne trompe à la
relecture.** Dans le dossier, « transmission » veut dire *un envoi*. Le modèle
`Transmission` ne porte pas ce sens tant qu'il est à l'état **`PREPAREE`** :
c'est une **fiche de préparation**, locale, qui n'a jamais quitté la machine.
Seul l'état **`ENVOYEE`** — qui ne peut être posé que par
`confirmer_transmission`, après qu'un message réel a été retrouvé et rattaché —
atteste d'un envoi. Lire une ligne `PREPAREE` comme un envoi serait une erreur
de fait.

### 5.1 Les trois natures de vérification

La distinction porte tout le dispositif. **Un contrôle automatique qui prétend
couvrir un jugement humain est pire que pas de contrôle : il rassure.**

| Nature | Ce que c'est | Effet |
|---|---|---|
| **BLOCAGE** | fait objectif, vérifiable sans interprétation | rien ne part |
| **SIGNALEMENT** | indice lexical, souvent un faux positif | on regarde, on passe |
| **ATTESTATION** | jugement que seule une personne peut porter | exigée nommément, par `--atteste` |

🔴 **`--atteste` ne se passe que par le demandeur.** Ces cinq clés sont ses
déclarations, inscrites à son dossier sous son nom. Les porter à sa place —
fût-ce pour éprouver une commande — y consignerait une déclaration qui n'est pas
la sienne. C'est la défaillance même que le dispositif existe pour empêcher.
*(Fait une fois, le 13 octobre 2026, lors d'un essai ; la ligne a été supprimée
le jour même. Consigné ici pour que la règle ait une raison d'être nommée.)*

**Les blocages** : adresse du destinataire périmée à la date du jour (avec
indication de la relève) ; mise en copie croisée entre parties ; numéro de
dossier absent du fichier source ; pièce jointe introuvable ou dont l'empreinte
a changé depuis la préparation ; délai de refroidissement de 12 h non écoulé.

**Les signalements** sont tirés de la liste fermée de [`pieges.md`](pieges.md)
§ D : le 21 juillet 2023 comme point de départ, « annuler/réviser un jugement »,
« exercice normal », l'effet protecteur, « diffamation », les prénoms des
enfants, et les points d'exclamation.

**Les attestations** sont les cinq de [`sortants/README.md`](sortants/README.md)
que rien ne peut vérifier à la place du demandeur : `delai`, `relu_a_froid`,
`aucun_fait_nouveau`, `aucun_engagement`, `ton`. ⚠️ **Une attestation est une
signature, pas une case.** Elle est consignée au rapport sous le nom de celui
qui la porte.

### 5.2 Ce que le dispositif ne fait PAS, et pourquoi

- Il ne juge pas si un fait est nouveau. Il exige qu'on le dise.
- Il ne lit pas le ton. Il signale sept motifs grossiers et demande une
  attestation pour le reste.
- Il n'empêche pas de passer outre : `relu_a_froid` lève le refroidissement.
  **Mais le dépassement reste consigné au rapport, nommément** — ce n'est pas un
  contournement, c'est un transfert de responsabilité qui laisse une trace.

### 5.3 La séquence

```bash
# 0. une fois
python manage.py init_destinataires --ecrire
python manage.py preparer_transmission --destinataires   # qui reçoit, et où, aujourd'hui

# 1. avant l'envoi
python manage.py preparer_transmission \
  --fichier legal/instance/sortants/<acte>.md \
  --nature "…" --destinataire <pk> \
  --piece "P-40=chemin/vers/piece.pdf" \
  --atteste delai,relu_a_froid,aucun_fait_nouveau,aucun_engagement,ton \
  --ecrire

# 2. l'envoi, à la main, depuis Gmail

# 3. après l'envoi
python manage.py sync_threads                 # ingérer le sortant
python manage.py confirmer_transmission --transmission <pk> --ecrire
```

L'étape 3 n'est pas de la comptabilité : **c'est elle qui rend le bordereau
exact**, puisque l'art. 134 exige l'heure et les minutes réelles, reprises de
l'en-tête `Date` du message. Elle refait en outre deux contrôles *a posteriori*
que la préparation ne peut pas faire : le message est-il bien parti à l'adresse
voulue, et personne d'étranger n'était-il en copie.

### 5.4 Ce qui reste à la main

**La ligne du journal.** `confirmer_transmission` le rappelle à chaque fois. Le
`.eml` et la ligne `Email` sont la preuve ; `journal.md` reste le récit, et il se
tient à la main parce qu'il porte un sens que la base n'a pas.
