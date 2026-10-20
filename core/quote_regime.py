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

Étape 2 : l'ancrage, la certification et le point d'entrée du régime PHRASE
(plus bas).

Plan : docs/modele_preuve/PLAN_REGIME_CITATIONS.md.
"""
import hashlib

from django.core.exceptions import ValidationError
from django.db import models, transaction


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


# ---------------------------------------------------------------------------
# Étape 2 : l'ancrage et la certification d'une citation PHRASE (plan, § 4)
# ---------------------------------------------------------------------------
#
# Le texte de référence d'une citation est le texte canonique de sa source :
# le corps d'un courriel (`body_plain_text`), la transcription d'un PDF (le champ
# `ai_analysis` sans son en-tête). `start` est inclus, `end` exclu, en indices
# Python dans ce texte.
#
# Trois empreintes, trois objets distincts :
#   source_text_sha256    le texte de référence est toujours le même ;
#   anchored_text_sha256  les bornes désignent toujours la même tranche ;
#   certified_text_sha256 le verbatim certifié par l'humain est toujours le même.
# Pour une citation ordinaire, les deux dernières portent sur le même texte. Pour
# un scan corrigé (`corrected_on_scan`), elles diffèrent volontairement : la
# tranche est la lecture OCR, `quote_text` la lecture certifiée du scan.
#
# La certification effective est recalculée à chaque lecture :
#   valid_anchor = 0 <= start < end <= len(source_text)
#                  AND sha256(source_text) == source_text_sha256
#                  AND sha256(source_text[start:end]) == anchored_text_sha256
#                  AND sha256(quote_text) == certified_text_sha256
#                  AND (corrected_on_scan OR source_text[start:end] == quote_text)
#   effective_certification = certified AND valid_anchor
# Toute mutation d'une composante qui a participé à la certification la rend
# immédiatement ineffective. Ces empreintes protègent contre une mutation
# accidentelle ou non autorisée ; elles ne sont pas une signature.
#
# Trois couches gardent les invariants que la base ne peut pas vérifier (la
# longueur et le contenu d'un texte situé dans une autre table) :
#   1. `create_phrase_quote`, le point d'entrée applicatif normal ;
#   2. la garde de `save()` (et de `clean()`), même hors du point d'entrée ;
#   3. l'audit, `manage.py audit_phrase_quotes`, pour ce qui contourne `save()`
#      (`update()`, `bulk_create()`).
# La base porte le reste : bornes obligatoires et `0 <= start < end` pour le
# régime PHRASE, unicité de (source, start, end) dans ce régime.



def sha256_text(text):
    """L'empreinte SHA-256, en hexadécimal, d'un texte encodé en UTF-8."""
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


class PhraseAnchor:
    """
    L'ancrage et la certification d'une citation du régime PHRASE.

    Mélangé aux deux modèles de citation. Ils déclarent eux-mêmes les champs
    (`start`, `end`, `source_text_sha256`, `anchored_text_sha256`,
    `certified_text_sha256`, `certified`, `corrected_on_scan`, `derived_from`),
    les contraintes en base, et `reference_text` (le texte de référence de leur
    source) et `source_field` (le nom de la clé étrangère vers la source).

    Une citation de l'ancien régime n'a pas d'ancrage : elle n'est jamais
    certifiée au sens de ce régime, et la garde ne la concerne pas.
    """

    def anchor_problems(self):
        """Les invariants d'ancrage violés : une liste vide si l'ancrage tient."""
        if self.start is None or self.end is None:
            return ["bornes absentes"]
        text = self.reference_text
        problems = []
        in_text = 0 <= self.start < self.end <= len(text)
        if not in_text:
            problems.append(f"bornes [{self.start}, {self.end}) hors du texte de référence ({len(text)} caractères)")
        if sha256_text(text) != self.source_text_sha256:
            problems.append("le texte de référence a changé (source_text_sha256)")
        if in_text:
            tranche = text[self.start:self.end]
            if sha256_text(tranche) != self.anchored_text_sha256:
                problems.append("les bornes ne désignent plus la même tranche (anchored_text_sha256)")
            if not self.corrected_on_scan and tranche != self.quote_text:
                problems.append("quote_text diffère de la tranche désignée")
        return problems

    def certification_problems(self):
        """Ce qui empêche la certification d'être effective, hors de l'ancrage."""
        if not self.certified_text_sha256:
            return ["aucune empreinte du texte certifié (certified_text_sha256)"]
        if sha256_text(self.quote_text) != self.certified_text_sha256:
            return ["le texte certifié a changé (certified_text_sha256)"]
        return []

    def derivation_problems(self):
        """L'antécédent, s'il y en a un : une citation de l'ancien régime, sur la même source."""
        if self.derived_from_id is None:
            return []
        antecedent = type(self).all_objects.filter(pk=self.derived_from_id).first()
        if antecedent is None:
            return [f"antécédent {self.derived_from_id} introuvable"]
        problems = []
        if antecedent.regime != QuoteRegime.HERITE:
            problems.append(f"l'antécédent {antecedent.pk} n'est pas de l'ancien régime")
        champ = self.source_field + "_id"
        if getattr(antecedent, champ) != getattr(self, champ):
            problems.append(f"l'antécédent {antecedent.pk} porte sur une autre source")
        return problems

    @property
    def valid_anchor(self):
        if self.regime != QuoteRegime.PHRASE:
            return False
        return not self.anchor_problems() and not self.certification_problems()

    @property
    def effective_certification(self):
        return bool(self.certified) and self.valid_anchor

    def audit_problems(self):
        """Ce que l'audit signale : un invariant violé, ou une certification déclarée mais ineffective."""
        problems = self.anchor_problems() + self.derivation_problems()
        if self.certified:
            problems += self.certification_problems()
        return problems

    def check_phrase_invariants(self):
        """La garde : une citation PHRASE qui viole un invariant d'ancrage est refusée."""
        if self.regime != QuoteRegime.PHRASE:
            return
        problems = self.anchor_problems() + self.derivation_problems()
        if problems:
            raise ValidationError("citation PHRASE refusée : " + " ; ".join(problems))

    def check_phrase_uniqueness(self):
        """
        Une seule citation PHRASE par (source, start, end).

        La base le garantit (contrainte d'unicité conditionnelle). Mais
        `full_clean()` valide les contraintes par le gestionnaire par défaut, filtré
        sur l'ancien régime : il ne verrait pas la citation PHRASE déjà présente.
        Le point d'entrée la cherche donc ici, par le gestionnaire de base.
        """
        if self.regime != QuoteRegime.PHRASE:
            return
        champ = self.source_field + "_id"
        doublon = (type(self).all_objects
                   .filter(regime=QuoteRegime.PHRASE, start=self.start, end=self.end, **{champ: getattr(self, champ)})
                   .exclude(pk=self.pk).values_list("pk", flat=True).first())
        if doublon is not None:
            raise ValidationError(f"citation PHRASE refusée : la même tranche est déjà citée (citation {doublon})")

    def clean(self):
        super().clean()
        self.check_phrase_invariants()
        self.check_phrase_uniqueness()

    def save(self, *args, **kwargs):
        self.check_phrase_invariants()
        super().save(*args, **kwargs)


def _page_of(document, position):
    """La page de la transcription où tombe `position` : la dernière marque de page qui la précède."""
    page = None
    for marque in document.PAGE_MARKER.finditer(document.transcription):
        if marque.start() > position:
            break
        page = int(marque.group(1))
    return page


def create_phrase_quote(source, start, end, *, derived_from=None, page_number=None, certify=None):
    """
    Le point d'entrée applicatif normal du régime PHRASE.

    Lit le texte de référence de `source` (un `Email` ou un `PDFDocument`),
    vérifie `0 <= start < end <= len`, calcule `quote_text` et les empreintes,
    appelle `full_clean()` (contraintes en base comprises), puis enregistre.

    Un courriel est certifié dans le même geste : l'original est la base. Un PDF
    ne l'est pas par défaut : un scan se certifie après la lecture du scan, par
    `certify_phrase_quote`. `certify` force l'un ou l'autre choix.

    Pour un PDF, la page se déduit des marques de la transcription ; à défaut,
    `page_number` la donne.
    """
    from email_manager.models import Email
    from email_manager.models import Quote as EmailQuote
    from pdf_manager.models import PDFDocument
    from pdf_manager.models import Quote as PDFQuote

    if isinstance(source, Email):
        quote = EmailQuote(email=source)
        certify = True if certify is None else certify
    elif isinstance(source, PDFDocument):
        if page_number is None:
            page_number = _page_of(source, start if isinstance(start, int) else 0)
        if page_number is None:
            raise ValidationError("aucune marque de page avant la citation : préciser page_number")
        quote = PDFQuote(pdf_document=source, page_number=page_number)
        certify = False if certify is None else certify
    else:
        raise TypeError(f"source inattendue : {type(source).__name__}")

    text = quote.reference_text
    if not (isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(text)):
        raise ValidationError(f"bornes [{start}, {end}) hors du texte de référence ({len(text)} caractères)")
    quote.regime = QuoteRegime.PHRASE
    quote.start, quote.end = start, end
    quote.quote_text = text[start:end]
    quote.source_text_sha256 = sha256_text(text)
    quote.anchored_text_sha256 = sha256_text(quote.quote_text)
    quote.derived_from = derived_from
    if certify:
        quote.certified = True
        quote.certified_text_sha256 = sha256_text(quote.quote_text)
    with transaction.atomic():
        quote.full_clean()
        quote.save()
    return quote


def certify_phrase_quote(quote, *, certified_text=None):
    """
    La certification d'une citation PHRASE, acte distinct pour un PDF scanné.

    `certified_text` est le verbatim lu sur l'original ; à défaut, la tranche
    elle-même. S'il diffère de la tranche, la citation est déclarée corrigée sur
    le scan (`corrected_on_scan`) : les bornes et `anchored_text_sha256` restent
    sur la transcription, `quote_text` et `certified_text_sha256` portent la
    lecture certifiée.
    """
    if quote.regime != QuoteRegime.PHRASE:
        raise ValidationError("seule une citation PHRASE se certifie ainsi")
    if quote.anchor_problems():
        raise ValidationError("ancrage invalide : " + " ; ".join(quote.anchor_problems()))
    tranche = quote.reference_text[quote.start:quote.end]
    text = tranche if certified_text is None else certified_text
    if not text:
        raise ValidationError("texte certifié vide")
    quote.quote_text = text
    quote.corrected_on_scan = text != tranche
    quote.certified = True
    quote.certified_text_sha256 = sha256_text(text)
    with transaction.atomic():
        quote.full_clean()
        quote.save()
    return quote
