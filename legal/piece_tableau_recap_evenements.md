# Pièce — Tableau récapitulatif des événements documentés (présence du demandeur avec les enfants, 2009-2015)

> **Nature : pièce d'AGRÉGATION** (couche ② de [methodo_preuve_volume.md](methodo_preuve_volume.md)). Résumé chronologique de la présence documentée du demandeur avec l'un ou l'autre des enfants, **généré depuis le modèle `events.Event`** de la base. Adosse les **faits de densité** de la section Coparentalité ([document_de_faits.md](document_de_faits.md), Bloc A). **Substrat (couche ③) :** les **1 521 photographies horodatées** liées à ces événements (art. 2855 C.c.Q.), produites **en liasse** sous une seule cote, disponibles pour vérification.
>
> **Vérifiabilité (verrou) :** chaque ligne du tableau renvoie à un `Event` id et à ses photos réellement produites — l'agrégation est reconstituable par la requête ci-dessous.

---

## Synthèse — par année

| Année | Événements | Photographies |
|---|---|---|
| 2009 | 2 | 2 |
| 2010 | 24 | 159 |
| **2011** | **92** | **573** |
| 2012 | 61 | 370 |
| 2013 | 49 | 199 |
| 2014 | 30 | 217 |
| 2015 | 1 | 1 |
| **TOTAL** | **259** | **1 521** |

*Étalement : continu de la naissance d'Alexia (oct. 2009) à 2015. Le pic de 2011 coïncide avec la période de séparation physique des parties (fév. 2011 – fév. 2012) — le demandeur y est documenté avec Alexia plusieurs fois par semaine.*

## Synthèse — par catégorie

| Catégorie | Événements |
|---|---|
| Domicile (quotidien) | 101 |
| Sorties / voyages | 92 |
| Parc | 18 |
| Famille paternelle | 16 |
| Danse (présence du demandeur) | 8 |
| Activités structurées (natation, gym, soccer) | 6 |
| Garderie / école | 2 |
| Autre | 16 |

## Synthèse — solo vs unité familiale (sous-filtrage)

Distinction entre les occasions où le demandeur est **seul** avec un enfant (axe *implication* — il assure seul) et celles en **présence des deux parents** (pertinentes pour réfuter §5, foyer fonctionnel). *(Sous-ensemble où un enfant est explicitement nommé : 255 lignes.)*

| Année | Solo | Famille |
|---|---|---|
| 2009 | 2 | 0 |
| 2010 | 13 | 11 |
| **2011** | **59** | 30 |
| 2012 | 53 | 7 |
| 2013 | 39 | 10 |
| 2014 | 27 | 3 |
| 2015 | 1 | 0 |
| **TOTAL** | **194 (1 166 ph.)** | **61 (349 ph.)** |

*« Solo » inclut les soirs où la demanderesse était à ses cours de danse (donc absente). Tableau **row-level complet** (255 lignes, colonne Type solo/famille) : [exhibit_tableau_evenements_2009-2015.md](exhibit_tableau_evenements_2009-2015.md) — c'est l'exhibit à produire.*

---

## Requête de génération (reproductible / vérifiable)

```python
from events.models import Event
import datetime
from django.db.models import Q
Event.objects.filter(
    date__gte=datetime.date(2009,1,1), date__lte=datetime.date(2015,12,31)
).filter(Q(explanation__icontains='LP') | Q(explanation__icontains='Louis')).order_by('date')
# → 266 brut ; 259 retenus après exclusion des 7 entrées hors-sujet (ci-dessous)
# colonnes exhibit : Event.id | date | explanation | linked_photos.count()
```

**7 entrées exclues (hors champ) :** Events id=312, 313, 314, 315 (« Élise planifie une fête-surprise ») ; id=205, 206 (sous-sol / appartement) ; id=47 (Jason). *Exclusions notées pour transparence.*

---

## Production (mécanique, méthodo couche ② + ③)
1. **Exhibit présenté** : le tableau row-level complet (259 lignes : date · description · enfant(s) · Event id · nb photos), généré depuis la DB.
2. **Substrat en liasse** : les 1 521 photographies, une cote, sur support.
3. **Plaidé** : le **fait de densité** (un § dans l'exposé — C11), pas les 259 lignes.

## Calibration
- **Plancher, non plafond** : ces chiffres ne couvrent que les moments **photographiés** ; le corpus réel d'interactions est nécessairement supérieur (note méthodologique, art. 2855).
- **Distinction disponible** : « Sorties/voyages » inclut des voyages familiaux (avec la demanderesse — Cuba, Cape Cod) ; pour l'axe *implication*, les événements **solo** (demandeur seul avec un enfant) sont les plus probants ; pour réfuter §5 (relation difficile), les voyages **familiaux** servent. Sous-filtrer au besoin.
- **Réfute « rarement disponible / minimalement »** ; **n'établit pas** une garde 50/50.

## Contexte d'usage
- [document_de_faits.md](document_de_faits.md) Bloc A (faits de densité C7-C15).
- [methodo_preuve_volume.md](methodo_preuve_volume.md) (couches ①②③).
