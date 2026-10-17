"""
Le régime des citations.

Deux régimes cohabitent dans les tables de citations (`email_manager.Quote`,
`pdf_manager.Quote`) :

- HERITE : les citations de l'ancien système, telles qu'elles existaient avant
  le nouveau pont. Toutes les citations existantes y sont classées ;
- PHRASE : les citations du nouveau régime, une phrase entière ancrée dans le
  texte de sa source.

L'ancien système ne voit que l'ancien régime. Chaque modèle de citation porte
trois gestionnaires :

- `objects`, le gestionnaire par défaut, filtré sur HERITE. Les relations
  inverses (`email.quotes`), les M2M (`trame.citations_courriel`), les
  `prefetch_related` et les listes de choix des formulaires en prennent la
  classe : ils sont filtrés aussi ;
- `all_objects`, le gestionnaire de base, sans restriction. Django s'en sert
  pour l'accès direct par clé étrangère, les clés génériques et les
  suppressions en cascade ; l'administration des citations aussi ;
- `phrase_objects`, le nouveau régime seulement, pour le nouveau pont.

Ce que le gestionnaire ne couvre pas : un `set()` ou un `add()` de M2M qui
reçoit des PK brutes les écrit dans la table de liaison sans lire les lignes
visées. Les chemins de l'ancien système qui rattachent des citations à partir
d'identifiants soumis les vérifient d'abord avec `invisible_pks`.

Plan : docs/modele_preuve/PLAN_REGIME_CITATIONS.md.
"""
from django.db import models


class QuoteRegime(models.TextChoices):
    HERITE = "HERITE", "Hérité (ancien régime)"
    PHRASE = "PHRASE", "Phrase (nouveau régime)"


class HeriteQuoteManager(models.Manager):
    """Le gestionnaire par défaut : l'ancien régime seulement."""

    def get_queryset(self):
        return super().get_queryset().filter(regime=QuoteRegime.HERITE)


class PhraseQuoteManager(models.Manager):
    """Le nouveau régime seulement."""

    def get_queryset(self):
        return super().get_queryset().filter(regime=QuoteRegime.PHRASE)


def invisible_pks(model, pks):
    """
    Les PK soumises que le gestionnaire par défaut de `model` ne rend pas.

    Une PK du nouveau régime, ou une PK qui n'existe pas, en fait partie. Les
    valeurs qui ne sont pas des entiers sont laissées au chemin appelant, qui
    les traitait déjà avant ce contrôle.
    """
    wanted = set()
    for pk in pks:
        try:
            wanted.add(int(pk))
        except (TypeError, ValueError):
            continue
    if not wanted:
        return set()
    visible = set(model._default_manager.filter(pk__in=wanted).values_list("pk", flat=True))
    return wanted - visible
