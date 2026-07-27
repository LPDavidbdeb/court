# Mémoire de continuité — projet `court`

Dernière mise à jour : 27 juillet 2026

## Objet du projet

Application Django servant à organiser, analyser et produire le dossier d’un litige familial. Elle regroupe notamment les courriels, documents/PDF, photos, vidéos, événements, conversations Google Chat, protagonistes et arguments. Le répertoire `legal/` contient le travail de préparation procédurale et de preuve.

## Situation procédurale actuelle

- La demande/requête introductive et le bordereau de preuve ont été **déposés** avant l’échéance de prescription du **25 juillet 2026**.
- La requête **n’a pas encore été notifiée/signifiée** aux autres parties.
- Selon l’information reçue par le demandeur, la requête peut encore être modifiée malgré son dépôt. Le travail en cours peut donc préparer une version amendée avant notification.
- Le dépôt initial demeure un jalon à préserver : ne pas écraser ni présenter une version subséquente comme si elle avait été celle déposée le 25 juillet.
- La demande doit être notifiée dans les trois mois suivant son dépôt afin d’éviter sa péremption (C.p.c., art. 107). La modification d’un acte est généralement possible avant jugement dans les limites de l’art. 206 C.p.c.; l’application au dossier concret doit être validée au besoin auprès d’un professionnel du droit ou du greffe.

## Règles de travail pour la suite

1. Conserver une trace explicite de la **version déposée** et de la date de dépôt.
2. Produire les corrections sous forme de **version amendée / prête à notifier**, avec une liste claire des changements.
3. Distinguer les preuves déjà au bordereau de celles ajoutées ou réorganisées après le dépôt.
4. Ne pas modifier silencieusement les fichiers déposés; créer une copie versionnée lorsque le contenu procédural change.
5. Avant notification, vérifier le document final, ses annexes/bordereaux, le numéro de dossier et les exigences du greffe applicables.

## État du dépôt et de la preuve dans le dépôt Git

- Le répertoire `legal/` comprend les faits, axes, pièces, bordereaux, annexe et fichiers de génération du dépôt.
- `legal/expose/README.md` décrit la méthode de traçabilité des sources, des pièces et des cotes.
- À la date de cette note, l’arbre Git contient plusieurs modifications locales, principalement dans `legal/`, ainsi que des pièces nouvellement générées ou en préparation. Elles ne doivent pas être présumées déposées ou signifiées sans vérification explicite.

## Audit automatisé de la chaîne des pièces

La commande suivante valide en lecture seule les fiches `legal/piece*.md`, le
registre technique `legal/bordereau_pieces.md`, le bordereau procédural
`legal/bordereau_bloc_depot.md`, les objets PostgreSQL, les fichiers originaux,
les renderers et l’assemblage `pieces_pdf/` :

```bash
python manage.py audit_piece_files
```

Options utiles :

```bash
# Échec de la commande si une erreur bloquante est constatée
python manage.py audit_piece_files --strict

# Rapports détaillés JSON et CSV
python manage.py audit_piece_files --output-dir /tmp/audit-piece-chain
```

L’audit distingue trois seuils : `source_ready`, `render_ready` et
`communication_ready`. Un placeholder, une cote manquante, une divergence de
source ou un PDF invalide bloque `communication_ready`.

### État constaté le 27 juillet 2026

- Le registre technique et le bordereau de dépôt contiennent tous deux les
  cotes P-1 à P-106.
- Les 22 groupes de sous-cotes indexés dans le bordereau de dépôt concordent
  avec leur source technique.
- L’assemblage existant ne contient que 105 cotes : P-106 n’est pas assemblée.
- Dix PDF assemblés sont des placeholders : P-19, P-40, P-42 et P-58 à P-64.
- Le dossier assemblé actuel n’est donc pas considéré comme prêt à communiquer.

## Méthodologie postérieure au dépôt

La méthodologie approuvée est consignée dans
`legal/METHODOLOGIE_POST_DEPOT.md`.

Elle fixe notamment :

- la conservation immuable du dépôt initial;
- la séparation de la demande amendée;
- le verrouillage des cotes P-1 à P-106;
- la concordance entre versions;
- les identifiants stables des faits;
- le journal des changements;
- les barrières `source_ready`, `render_ready` et `communication_ready`.

La forme définitive de la section « Exposé des faits » demeure expressément
ouverte. Plusieurs variantes doivent pouvoir être expérimentées sans qu’un plan
chronologique, thématique, juridique ou hybride soit présumé choisi.
