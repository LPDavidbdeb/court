# Source du mandat — UC14, conception préalable à correction

Message utilisateur reçu dans la session du **23 octobre 2026**. Le présent
relevé conserve les exigences opérationnelles de ce complément; il ne vaut
ni nouvelle approbation, ni remplacement des décisions précédentes.

L'utilisateur impose, **avant toute modification de code**, une séquence
montrant T1 suppression et T2 édition/repointage : état contrôlé, acquisition
et durée des protections, archive/repointage, DELETE SQL et finalisation,
deux ordres conformes, rollbacks et transactions indépendantes. Vérifier et
actualiser les activités/classes; vérifier l'ERD et le conserver si le
schéma n'a pas besoin de changer. Garder les versions approuvées et leurs
références. Soumettre les diagrammes et la cohérence à B pour revue préalable.

Instruction déterminant la porte d'autorisation, reproduite exactement :

> La correction du code ne pourra être autorisée qu'après validation de la conception révisée et approbation explicite de l'utilisateur.

Le bloc suivant du même message demande une correction ciblée après le
verdict B01 NON CONFORME : identifier la fenêtre ORM/SQL, privilégier une
sérialisation locale sans supposer `select_for_update()` suffisant, garantir
l'archive exacte, garder l'API Treebeard/gardes/atomicité, couvrir les éditions
HTTP et repointages citation, empêcher la résurrection par instance ORM
périmée. Aucun verrouillage général d'arbre, migration ou extension C0-A.

Contre-épreuves exigées : T2 committée avant protection T1 implique refus T1
et conservation T2; T1 protégée avant édition T2 implique attente légitime
puis refus T2 sans recréation après commit T1. Reproduire les deux variantes
tardives B; exercer plusieurs occurrences et les effets indépendants. Ne
pas forcer T2 à réussir pendant qu'un verrou légitime l'en empêche.

Après autorisation seulement : delta limité, tests discriminants ancienne /
nouvelle version, non-régression complète, preuve d'archive fidèle, rapport
et nouvelle revue B. Aucun merge, déploiement ou accès à la base réelle.
Un changement du contrat approuvé doit être soumis avant de poursuivre.

La porte préalable explicite gouverne donc cette livraison documentaire :
le second bloc ne permet pas de commencer le code avant revue et approbation.
