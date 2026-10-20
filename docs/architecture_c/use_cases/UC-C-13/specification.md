# UC-C-13 — Éditer une rédaction PRODUCED en préservant les sources REPRODUCED

**C0A-UML-R2-ST — 20 octobre 2026 — lot C0-A.** Auteur et revue documentaire : B;
implantation future : A, non autorisée. **APPROUVE_UTILISATEUR pour C0A_ISOLER seulement le 20 octobre 2026.**
La décision métier ST01–ST05 vient du [mandat](../../references/MANDAT_INVARIANTS_STATEMENT_2026-10-20.md);
le profil technique ci-dessous est approuvé au seul périmètre consigné dans [la décision](approbation.json). [Statut](../../registre_validation.md)
et [validation/empreintes](validation.md).

## Contrat et périmètre proposé à approbation

Les REPRODUCED sont des sources immuables dont seuls les Statement d’origine
attestée peuvent être réutilisés. La rédaction PRODUCED utilise des contenus
privés non partageables; reprendre son texte dans une autre occurrence crée
un nouvel objet. Toute protection historique demeure prioritaire, y compris
pour un Document PRODUCED devenu référent.

Autorité détaillée : [invariants et analyse ST-R1](../../INVARIANTS_STATEMENT_REPRODUCED_PRODUCED.md).
Sources conservées : D03/CF3-D4, V2:US-02.AC01/02/04/05, mandat historique C0-A.
Socle observé proposé : `515666eb8c6e7fdcdd265f9187c9c37b769b0fed`;
P6 reste le socle initial du patch, inchangé. [Modèle global G-C0A-R2-ST approuvé](../../versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md).

**Sous-cas approuvé : `UC-C-13::C0A_ISOLER`.** Les quatre vues portent exactement
ce profil sans nouveau schéma : sur changement de texte, créer un objet neuf
pour l’occurrence au lieu d’écrire sur l’ancien Statement. Aucun décompte
actuel ne prouve que l’ancien est d’origine privée. Ce sous-cas ne réalise
pas à lui seul le contrôle de tous les rattachements ST04 de l’application.
Le chemin de modification directe d’un privé attesté est défini comme
condition future et **hors activation C0-A**; sa revalidation relève de L1-A.

Acteur : rédacteur. POST vers `ajax_edit_node`, formulaire texte/item validable,
occurrence PRODUCED non protégée; un REPRODUCED ou référent est refusé.
GET reste une lecture; cible absente : 404; formulaire invalide : 400.
Une GFK autre que Statement, incomplète ou incohérente n’est pas une source
rédactionnelle admissible. Une occurrence sans type ni objet peut recevoir
son premier Statement.

## Critères d’acceptation

Les identifiants AC01–AC08 sont conservés. **Seuls AC02 et AC03 changent de
formulation**; AC01/04/05/06/07/08 restent identiques à la version R1.

| ID local | Résultat observable |
|---|---|
| AC01 | Une occurrence REPRODUCED ou référent historique refuse toute édition, y compris `item`; textes, associations et captures restent inchangés. |
| AC02 | Pour une occurrence PRODUCED éditable réutilisant un Statement d’origine REPRODUCED attestée, tout changement réel de texte conserve une capture antérieure, crée un Statement privé neuf et repointe seulement cette occurrence. Le texte source n’est jamais modifié. |
| AC03 | La modification directe n’est admissible que si origine privée, propriétaire de l’occurrence, mutabilité et interdiction effective des rattachements sont établis. Dans le profil C0A_ISOLER, elle est désactivée : tout texte différent reçoit un Statement neuf, même si l’ancien paraît privé. Capter avant/après et préserver les captures utiles, sans déduire l’origine de la cardinalité actuelle. |
| AC04 | Texte identique : aucun détachement ou capture supplémentaire; `item` peut changer si autorisé. Sur une occurrence sans type ni objet, créer le premier Statement. Un autre type ou une GFK incohérente est refusé. |
| AC05 | À la lecture d’une ConfirmationAppui confirmée ou SANS_APPUI, recharger l’occurrence réelle et comparer Statement associé et empreinte à la capture. Autre texte ou autre Statement, même à texte égal : A_REEXAMINER; décision stockée et ancien texte conservés. |
| AC06 | Le traitement éditorial d’une Correspondance compare le Document et les couples Statement/empreinte aux captures des deux rôles. Divergence de ces valeurs source ou cible : à réexaminer, sans réécrire l’ancienne décision. L’identité complète des compositions d’occurrences reste à L1-A/C0-B. |
| AC07 | Capture, duplication éventuelle, repointage, texte et `item` appartiennent à l’opération atomique. Une exception tardive annule l’ensemble, y compris les nouveaux objets. Un refus ne laisse aucun effet partiel. |
| AC08 | Ni schéma ni migrations modifiés. Identité/numéro de l’occurrence et contenus historiques non édités restent intacts; aucun texte Quote HERITE/PHRASE n’est assimilé à un Statement. |

## Nominal et variantes du profil C0-A

1. Contrôler méthode/formulaire, occurrence, type et protections avant mutation.
2. Texte égal : ne pas détacher; traiter `item` dans sa propre branche logique.
3. Texte différent : capter l’ancien texte, créer un Statement neuf, repointer
   cette occurrence et capter le résultat. Ne jamais sauvegarder le nouveau
   texte sur l’ancien objet dans ce profil.
4. Sauver `item` et l’association dans la même opération atomique; refus ou
   échec tardif annule captures/objet neuf/repointage/item.
5. À la consultation, relire l’identité et le texte actuels pour calculer la
   fraîcheur. Conserver les décisions/captures antérieures sans les reconfirmer.

La création du nouvel objet établit qu’il est créé pour cette opération et
cette occurrence, pas une preuve persistante de provenance des anciens objets.
L1-A assurera la propriété durable et les refus sur tous les rattachements.
Aucune association héritée n’est déliée, supprimée ou reclassée par une tâche
automatique. Une édition explicitement demandée sur la cible ne régularise pas
les autres usages de l’ancien objet, qui restent à diagnostiquer.

Le partage observé entre deux PRODUCED peut être soit une réutilisation
légitime d’une origine REPRODUCED attestée, soit une anomalie héritée : ne pas
trancher d’après le seul type de ces deux occurrences. Le premier cas est un
parcours admissible; le second est une contre-épreuve de non-altération, pas
une autorisation de créer ce partage.

## Conditions du chemin direct et limites

Le contrat complet permet de modifier en place un contenu privé si l’origine,
le propriétaire, la mutabilité et la fermeture des écritures de rattachement
sont effectivement garantis. `is_user_created=True` ou « un usage à cet instant »
ne suffisent pas. Le modèle actuel ne conserve pas ces preuves; **ce chemin
n’est pas proposé à l’activation C0-A**. La solution minimale L1-A est décrite
au §6 des invariants, sans entité nouvelle ni migration créée ici.

La nouvelle règle supprime le scénario « privé devenant partagé » des parcours
autorisés, mais pas du code existant : une création par PK peut s’intercaler
après le contrôle de partage. Copier avant édition évite d’écrire dans cet
ancien objet sans inventer de verrou général. Deux éditions de la même
occurrence, ou un gel concurrent, restent des questions distinctes; aucune
sérialisation universelle n’est déclarée livrée.

`item` est une propriété de l’occurrence; une modification sans texte ne crée
pas de Statement. Dans certains profils il influe sur le genre/numérotation
(`C-…`, item vide). Les contrôles C0-A de fraîcheur textuelle ne garantissent
pas la détection de cet effet de contexte; L1-A/C0-B doivent définir/capturer
le contexte pertinent des examens. Un simple renommage d’affichage n’est
pas automatiquement un nouvel examen. Sur une occurrence protégée, les deux
sortes d’édition restent refusées.

Les limites du journal, de la composition complète d’occurrences, des archives
historiques typées et du gel SQL/stockage restent L1-A/C0-B/L5. Aucun champ
`nature`, manifeste ancien ou nouvelle garantie de citation n’est inventé.
C0A-REV-01 reste ouverte dans UC15, distincte de cette révision.

## Écart avec le patch et décision demandée

Le patch conservé a une branche de modification privée en place; il ne satisfait
pas le profil proposé à AC03. Ses 209 tests P6 ne valident ni la nouvelle règle
ni ce profil. Ses fixtures de partage privé PRODUCED deviennent des données
héritées adverses; les tests sont conservés et non renommés silencieusement.

**Approuvé le 20 octobre 2026 : la version C0A-UML-R2-ST du seul sous-cas C0A_ISOLER**, avec
l’absence d’écriture en place et les limites ci-dessus. Ce n’est ni l’approbation
d’un schéma L1-A, ni celle du contrat complet de propriété, ni un mandat de code.
L’ancienne attestation B R1 n’est pas transférée à cette version; la validation
R2 précise sa portée. Tout élargissement des fichiers de correction doit être
justifié et autorisé avant écriture par A.

## Vues et preuves

- [Activité](activity.svg) · [source](activity.puml)
- [Séquence](sequence.svg) · [source](sequence.puml)
- [ERD cible local](erd.svg) · [source](erd.puml)
- [Classes et composants](class.svg) · [source](class.puml)
- [Traçabilité et tests](tracabilite.md) · [validation](validation.md)
- [Version R1 conservée](../../historique/2026-10-20_avant_invariants_statement_R2/corpus/use_cases/UC-C-13/specification.md)


## Enregistrement de l’approbation — suivi administratif

Décision : [mandat utilisateur](../../references/MANDAT_APPROBATION_UC13_VALIDATION_C0A_2026-10-20.md),
[PR #30](https://github.com/LPDavidbdeb/court/pull/30), fusion `cd584c3`.
Le [manifeste et les 24 fichiers approuvés](../../versions_approuvees/UC-C-13_C0A-UML-R2-ST/README.md)
sont conservés à l’identique. Les quatre sources et leurs huit rendus ne sont
pas modifiés. Les annotations de suivi ne changent ni AC01–AC08 ni le contrat.
**PRET_DEVELOPPEMENT : NON**; les conditions de C0-A restent à satisfaire.
