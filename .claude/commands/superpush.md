---
description: add + commit + push en une passe, message de commit rédigé automatiquement
---
Lance le sous-agent `Git` avec la consigne `superpush`.

C'est un mandat explicite pour add + commit + push sur la branche courante. L'agent lit les diffs, exécute son contrôle anti-secrets, stage par chemins explicites, rédige le ou les messages de commit et pousse.

Transmets-lui tout argument fourni après `/superpush` comme précision de contexte (par exemple une branche cible ou un thème à respecter dans le message).

Relaie ensuite son rapport : SHA, messages, fichiers, destination.
