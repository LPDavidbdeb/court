# P-43 — Courriels professionnels relatifs aux soins des enfants

## Définition matérielle

P-43 est une liasse homogène de **19 courriels professionnels** regroupés en
**16 occurrences distinctes**, du 7 mars 2011 au 3 août 2015. Les documents sont
tous des courriels adressés à des supérieurs de la Banque Nationale du Canada,
ou une réponse de la supérieure dans le même fil, et soutiennent la même
proposition : le demandeur a interrompu ou modifié son travail afin de prendre
soin d'un enfant ou de l'accompagner à un rendez-vous médical.

Chaque occurrence reçoit une subdivision `P-43.1` à `P-43.16`. Les courriels
complémentaires du même fil restent sous la même subdivision et ne sont pas
comptés comme une nouvelle occurrence.

## Sous-ensembles utilisés dans la demande

- `P-43.1` à `P-43.11` : onze occurrences entre le 7 mars 2011 et le
  10 septembre 2012;
- `P-43.1` à `P-43.8` : huit occurrences distinctes en 2011;
- `P-43.1` à `P-43.16` : seize occurrences entre 2011 et 2015;
- `P-43.3`, `P-43.4`, `P-43.6`, `P-43.8` et `P-43.15` : exemples particuliers
  cités individuellement dans la demande.

## Règles de comptage

- `Email:118` est le suivi médical de l'absence documentée par `Email:64` : une
  seule occurrence (`P-43.2`);
- `Email:58` est la réponse de la supérieure au courriel `Email:59` : une seule
  occurrence (`P-43.4`);
- `Email:488` est une seconde importation du même courriel que `Email:53` et est
  exclu de la liasse;
- `Email:41` décrit une période de fatigue familiale, mais pas assez clairement
  une interruption de travail; il est exclu du comptage;
- `Email:15`, daté de 2016, est hors du périmètre 2011–2015 retenu dans la
  demande et n'est pas inclus dans P-43.

## Production

`index_p43.csv` est l'ordre de production et la source de vérité pour le futur
script de téléchargement. Les fichiers devront être exportés dans cet ordre,
avec un nom comprenant la subdivision, la date et le tuple canonique. Une
pagination continue pourra être ajoutée lors de la fusion en PDF sans modifier
les subdivisions stables.

`concordance_demande.csv` relie chaque paragraphe de la demande aux
subdivisions exactes qui le soutiennent.
