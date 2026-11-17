# Mise en demeure de reconnaître l'origine et l'intégrité — art. 264 C.p.c.

**Statut : 🟡 PROJET — non envoyé. ⚠️ POUR Me TIMMONS SEULE.**

🔴 **Écarté pour Élise (décision de LP, 6 nov.)** : adressée à une partie non
représentée, « mise en demeure » ne se lit pas comme un article du Code mais
comme une sommation. Pour elle, le ressort doux de l'**art. 174 al. 2** couvre
ce qui compte — voir `../communication_pieces.md` § 37.1 et § 37.6. Supprimer
ci-dessous les variantes « Madame ».

⚠️ **NE PART PAS AVANT L'ÉTAPE 2.**
Voir la séquence impérative de `../communication_pieces.md` § 36.4 : régler
l'accès, **faire confirmer l'accès**, puis mettre en demeure. Envoyée à une
partie qui est au dossier comme n'ayant pas accès aux fichiers, elle reçoit la
réponse toute faite — « je n'ai rien reçu, je ne peux rien reconnaître ».

| | |
|---|---|
| Destinataire | **`patricia.timmons@farpbq.ca`** seule, Mme Barry en copie |
| ⚠️ | **pas à Élise** (§ 37.1) ; jamais d'envoi commun, jamais de copie croisée (§ 1) |
| Nature | **notification** (art. 133) — consentement de Me Timmons acquis le 16 oct. |
| Bordereau | **oui, art. 134** — ⚠️ cette fois **par le mécanisme** `preparer_transmission` / `confirmer_transmission`, jamais à la main (leçon du § 31.3) |
| Condition de validité | notifiée **au moins 30 jours avant l'instruction** (art. 264 al. 2). ✅ aucune date d'instruction n'est fixée |
| Pièce jointe | aucune — l'index et `SHA256SUMS` sont déjà entre leurs mains depuis le 5 nov. |

---

## Texte

> Objet : Dossier 505-17-016235-261 — mise en demeure de reconnaître l'origine et l'intégrité des pièces (art. 264 C.p.c.)
>
> Madame, *(ou : Maître,)*
>
> Conformément à l'article 264 du Code de procédure civile, je vous mets en
> demeure de reconnaître l'origine des pièces qui vous ont été communiquées le
> 5 novembre 2026 ainsi que l'intégrité de l'information qu'elles portent.
>
> **Les éléments visés.** Les 911 fichiers répartis sous les 105 cotes
> énumérées à l'index « 00_Index_des_pieces.pdf » qui vous a été transmis le
> 5 novembre 2026, dont l'empreinte SHA-256 est
> `4100b9ab…`. La pièce P-86, qui figure à la liste des pièces signifiée le
> 17 septembre 2026, est retirée et n'est pas visée par la présente.
>
> **Accès.** Les pièces vous ont déjà été communiquées. Conformément au
> deuxième alinéa de l'article 264, la présente est accompagnée de l'indication
> permettant d'y avoir accès : *[lien, ou la voie convenue à l'issue de
> l'étape 1]*. L'index identifie, pour chaque cote, la date et la description
> portées à la liste signifiée, puis les fichiers qui la composent ; pour chaque
> courriel, il indique la date, l'expéditeur, le destinataire et l'objet.
>
> **Moyen de vérification.** Le fichier `SHA256SUMS` qui vous a été transmis le
> même jour porte l'empreinte SHA-256 de chacun des 911 fichiers. Lancée dans le
> dossier, la commande `shasum -a 256 -c SHA256SUMS` vérifie chaque fichier et
> nomme celui qui différerait.
>
> **Ce que prévoit l'article 264.** Son troisième alinéa prévoit que la partie
> mise en demeure admet ou nie l'origine ou l'intégrité de l'élément de preuve
> dans une déclaration sous serment où elle précise ses motifs, et qu'elle
> notifie cette déclaration à l'autre partie dans un délai de dix jours. Son
> quatrième alinéa prévoit que le silence de la partie mise en demeure vaut
> reconnaissance de l'origine et de l'intégrité de l'élément de preuve, mais non
> de la véracité de son contenu.
>
> **Portée de la présente.** Elle ne porte que sur l'origine et l'intégrité.
> Elle ne vous demande aucune admission quant à la véracité du contenu des
> pièces, ni quant à la pertinence ou à la portée que l'une ou l'autre des
> parties pourra leur attribuer.
>
> Si une cote ou un fichier en particulier soulevait une difficulté d'origine ou
> d'intégrité, je vous invite à me l'indiquer : je fournirai les précisions ou
> les éléments complémentaires nécessaires.
>
> Veuillez recevoir, Madame, mes salutations distinguées. *(ou : Maître,)*
>
> Louis-Philippe David
> 222, rue Sainte-Catherine Est, c.p. 1433, Montréal (Québec) H2X 1L1
> louisphilippe.david@gmail.com
> Dossier 505-17-016235-261

---

## Ce que cet acte fait

- **Il attache une conséquence à leur silence**, ce que l'envoi du 5 novembre ne
  faisait pas (§ 36.3). Le délai de dix jours vient du Code, non du demandeur :
  la règle [[feedback_aucun_delai_sans_avantage]] n'est pas touchée.
- **Il ne demande rien d'autre que l'origine et l'intégrité**, et le dit
  expressément. Un adversaire ne peut pas lire la lettre comme une tentative
  d'obtenir une admission sur le fond, et le quatrième alinéa de l'article le
  confirme de lui-même.
- **Il se rédige froid**, sans un mot sur l'épisode de la clé USB ni sur la
  conduite de l'adjointe (`pieges.md` § A.2 — riposte art. 51-54).
- **Il offre la coopération en terminant** : l'invitation à signaler une
  difficulté précise retire d'avance l'excuse « nous n'avons pas pu vérifier ».

## ⚠️ Les trois issues, et aucune n'est mauvaise — mais la deuxième se prépare

| Issue | Résultat |
|---|---|
| **Silence** | reconnaissance de l'origine et de l'intégrité des 911 fichiers, par l'effet du 4ᵉ alinéa |
| **Déclaration sous serment motivée** | leur position est **cristallisée tôt et sous serment**, sur un terrain (l'intégrité) où le demandeur a 911 empreintes, une vérification par aller-retour et un rapport de vérification indépendante |
| **Demande de précisions sur une cote** | coopération, et le demandeur répond |

🔴 **Ce que la deuxième issue coûte, et il faut l'avoir vu avant d'envoyer.**
La mise en demeure **les force à regarder**. Le § 28.4 recense déjà une vingtaine
de réserves qu'un contentieux d'assureur trouvera en regardant — notamment les
dates du bordereau démenties par le contenu (P-58, P-59, P-38), le contenu de
P-45.2, les 4 pages de P-33. Ces réserves portent sur les **descriptions du
bordereau**, non sur l'origine ni l'intégrité des fichiers : une reconnaissance
sous l'art. 264 ne les validerait pas, et une dénégation sous serment ne les
atteindrait pas non plus sans sortir de l'objet de l'article. **Mais elles
seront lues.** Mieux vaut que ce soit après la réécriture et sa table de
concordance (§ 10.5) que la veille.

➜ **Conséquence sur l'ordre** : cette mise en demeure se place **après**
l'étape 2 (confirmation d'accès), et son moment optimal est à arbitrer contre
l'avancement de la réécriture. Elle n'est pas urgente — aucune date
d'instruction n'est fixée.

## Liste de vérification avant envoi

- [ ] ⚠️ **L'accès est confirmé** par le destinataire (étape 2 du § 36.4).
- [ ] ⚠️ **Élise n'est pas destinataire** ; aucune copie croisée ; aucun Cci.
- [ ] Bordereau de l'art. 134 produit **par le mécanisme**, avec heure et minutes réelles.
- [ ] Le lien ou la voie d'accès indiqué est **actif et vérifié** le jour de l'envoi.
- [ ] L'empreinte de l'index citée dans la lettre correspond au fichier réellement transmis le 5 nov.
- [ ] Aucune échéance ajoutée par le demandeur ; seuls les délais de l'article sont cités.
- [ ] Aucune mention de la conduite de l'adverse, ni de l'épisode du véhicule.
- [ ] Ligne inscrite à [`../journal.md`](../journal.md) le jour de l'envoi.
