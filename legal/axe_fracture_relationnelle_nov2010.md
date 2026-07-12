# Chronologie — Fracture relationnelle de novembre 2010

**Objet :** Ce document établit la chronologie précise de la rupture relationnelle survenue en novembre-décembre 2010 (infidélité de LP, éviction temporaire, retour au domicile, rupture entre Élise et Johanne Bazinet). Cette fracture est structurante pour toute la période subséquente, jusqu'à la séparation physique du 6 février 2011 et au-delà — elle explique notamment le contexte dans lequel certains schémas comportementaux documentés ailleurs (visites conditionnelles de Johanne, dynamique familiale tendue) se sont mis en place.

**Portée :** Ce document est un fondement contextuel, pas un axe argumentatif autonome contestant une allégation précise. Il sert à ancrer chronologiquement et factuellement les autres axes qui en dépendent, notamment `axe_agenda_danse_elise.md`.

---

## Chronologie

> **Requête DB :** `Email.objects.filter(id__in=[82, 84])` ; réservation Fairmont (à intégrer comme pièce — voir note en fin de document)

| Date | Fait | Source |
|---|---|---|
| 19 ou 20 novembre 2010 | Le demandeur commet une infidélité | Allégation Doc 1 (Requête nov. 2015), ¶7 |
| Lendemain (20 ou 21 nov. 2010) | Le demandeur admet son indiscrétion à la défenderesse | Allégation Doc 1, ¶7 (suite) |
| — | La défenderesse chasse le demandeur du domicile familial | Allégation Doc 1, ¶7 (suite) |
| — | Le demandeur se rend chez un ami | Allégation Doc 1, ¶7 (suite) |
| **22 novembre 2010, 14h57** | **Le demandeur reçoit une confirmation de réservation pour une chambre au Fairmont Le Reine Élisabeth, pour la nuit du 22 au 23 novembre 2010, pour un adulte (confirmation #62292490, 144,00$ CAD)** | **Email de confirmation Fairmont Hotels and Resorts** |
| **23 novembre 2010, 17h20** | **Le demandeur écrit à la défenderesse : *"qu'es ce qui ferrais ton affaire pour ce soir, si ce que tu veux c'est que je revienne et que je couche en bas, c'est ce que je vais faire"*** | **Email id=84** |
| Avant le 1er décembre 2010 | La défenderesse met un terme à sa relation avec Johanne Bazinet (mère du demandeur) par courriel | Allégation Doc 1, ¶7 (suite) |
| **1er décembre 2010, 15h37** | **Johanne Bazinet répond, exprimant le souhait de préserver son lien avec Alexia malgré la rupture : *"je me rends bien compte que c'est très immature et pas vraiment en lien avec moi... je veux juste m'assurer que je vais garder mon lien avec Alexia"*** | **Email id=82** |
| 6 février 2011 | Le demandeur quitte la résidence familiale | Établi par ailleurs (voir `axe_agenda_danse_elise.md` et chronologie générale) |

---

## Lecture de la séquence

**19-23 novembre 2010 — Crise aiguë et résolution rapide :** En l'espace de 4 jours, la séquence complète se déroule : infidélité, aveu, éviction, hébergement chez un ami, réservation d'hôtel (une seule nuit), puis offre de retour au domicile sous condition (chambre séparée, *"coucher en bas"*). La réservation Fairmont — pièce générée par un tiers neutre, horodatée — fixe une date certaine dans cette séquence et confirme que l'éviction n'a duré que quelques jours avant une tentative de réconciliation pratique.

**Fin novembre - 1er décembre 2010 — Élargissement du conflit à la famille de LP :** La rupture ne reste pas confinée au couple — la défenderesse coupe également les liens avec Johanne Bazinet, mère du demandeur. La réponse de Johanne (1er décembre) révèle sa préoccupation principale : préserver le contact avec Alexia, indépendamment du conflit entre les adultes.

**Conséquence structurelle pour la période subséquente :** Cette rupture avec Johanne explique le **mécanisme documenté ailleurs** dans le dossier — la règle tacite selon laquelle Johanne ne visite Alexia que lorsque la défenderesse est absente (voir Email id=67, *"la voiture d'Élise était là donc j'ai pensé que je ne devais pas arrêter"*, et Email id=81, *"si Élise n'est pas là demain soir, j'aimerais passer"*, dans `axe_agenda_danse_elise.md`). Cette règle apparaît dès le 7 décembre 2010 — **moins d'une semaine** après la rupture du 1er décembre. Elle n'est donc pas une politesse abstraite ou une coïncidence : c'est une conséquence directe et immédiate du conflit familial documenté ici.

**Cohabitation sous tension (déc. 2010 - fév. 2011) :** Entre le retour de LP au domicile (fin novembre 2010, sous condition de chambres séparées) et son départ définitif (6 février 2011), les parties cohabitent dans un climat dégradé pendant environ deux mois et demi. Cette période précède directement celle où les schémas de garde documentés dans les autres axes (danse, garderie) commencent à apparaître avec densité dans la preuve documentaire.

---

## Application — pourquoi ce document est un fondement, pas un axe de contestation autonome

Ce document n'a pas pour fonction de contester une allégation précise — la séquence factuelle qu'il établit est largement cohérente avec les allégations de la Requête de 2015 elle-même (Doc 1, ¶7). Sa fonction est de :

1. **Fixer des dates certaines** dans une séquence narrative qui serait autrement difficile à dater avec précision (la réservation Fairmont et l'Email id=84 ancrent fermement le 22-23 novembre 2010)
2. **Expliquer le contexte** d'autres pièces déjà utilisées dans les axes existants (la règle de visite conditionnelle de Johanne)
3. **Établir la continuité temporelle** entre la crise de novembre 2010 et la séparation physique de février 2011 — ce n'est pas un événement isolé, mais le point de départ d'une dégradation progressive de la relation qui culmine deux mois et demi plus tard

---

## Note — pièce à intégrer formellement

La confirmation de réservation Fairmont existe actuellement comme fichier `.eml` (Downloads). Elle devrait être importée dans la DB comme `Email` (expéditeur : Fairmont Hotels and Resorts, destinataire : LP, daté du 22 novembre 2010, 14h57 EST) afin d'obtenir un PK citable, au même titre que les autres pièces de ce document.

**Détails de la réservation pour l'enregistrement :**
- Confirmation # 62292490
- Hôtel : Fairmont Le Reine Élisabeth, 900 René Lévesque Blvd W, Montréal, QC H3B 4A5
- Arrivée : 22/11/2010 — Départ : 23/11/2010 (1 nuit)
- 1 adulte, 0 enfant
- Tarif : 144,00$ CAD (168,23$ CAD avec taxes)
