from django.db import models
from pgvector.django import VectorField
from django.urls import reverse
from email_manager.models import Email
from photos.models import Photo
from core.mixins import ExhibitableMixin
from datetime import datetime

class Event(models.Model, ExhibitableMixin):
    embedding = VectorField(dimensions=768, null=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text="The parent event for this piece of evidence."
    )
    date = models.DateField(help_text="The date of the event.")

    # --- bornes de l'événement -------------------------------------------
    # Jusqu'au 13 août 2026, l'intervalle vivait DANS le texte, sous la forme
    # d'un préfixe « On 2012-03-31 between 14:46 and 16:26: ». Une donnée
    # structurée logée dans un champ de prose doit être ré-extraite par
    # expression régulière à chaque manipulation, et chaque ré-extraction est
    # une occasion de la corrompre — ce qui est arrivé (voir E-312 et E-314,
    # dont le texte portait « 05 and 21:05: » en plein milieu).
    #
    # ⚠️ CONVENTION DE FUSEAU — à lire avant toute conversion.
    # `Photo.datetime_original` porte l'étiquette UTC mais contient l'HEURE
    # LOCALE au mur. Vérifié sur les 1729 photographies : lues telles quelles
    # elles donnent une courbe de vie familiale normale (0,2 % entre minuit et
    # 5 h) ; converties vers America/Montreal, 13 % basculeraient en pleine
    # nuit et le spectacle de danse d'E-19 passerait de 20 h 37 à 16 h 37.
    # `debut` et `fin` reprennent donc EXACTEMENT la convention des photos.
    # Ne jamais leur appliquer `localtime()` : formater avec `strftime`, ou
    # passer par `libelle_horodate()`.
    debut = models.DateTimeField(
        null=True, blank=True,
        help_text="Début de l'événement. Initialisé sur la première photographie "
                  "liée, mais modifiable : les photographies bornent l'événement "
                  "par le bas, elles ne le définissent pas."
    )
    fin = models.DateTimeField(
        null=True, blank=True,
        help_text="Fin de l'événement. Même convention que `debut`."
    )

    explanation = models.TextField(
        blank=True,
        help_text="Description de l'événement, en français, SANS horodatage : "
                  "les bornes vivent dans `debut` et `fin`."
    )
    email_quote = models.TextField(
        blank=True,
        null=True,
        help_text="A specific quote or excerpt from an email."
    )
    linked_email = models.ForeignKey(
        Email, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        help_text="The specific email this quote is from."
    )
    linked_photos = models.ManyToManyField(
        Photo,
        blank=True,
        related_name='events',
        help_text="A collection of photos related to this event.",
        through='SupportingEvidenceLinkedPhotos',
    )

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        db_table = 'SupportingEvidence_supportingevidence' 
        ordering = ['date']

    # --- Exhibitable Interface ---
    def get_exhibit_date(self):
        return datetime.combine(self.date, datetime.min.time())

    def get_exhibit_title(self):
        return f"Événement du {self.date}"

    def get_exhibit_type(self):
        return "Événement"

    def get_exhibit_description(self):
        # Cette méthode découpait autrefois sur le dernier « : » pour retirer
        # le préfixe horodaté. Le préfixe n'existe plus, et le découpage était
        # un piège : la première description contenant un deux-points aurait
        # été tronquée sans que rien ne le signale.
        return self.explanation or ""

    # --- bornes ----------------------------------------------------------
    @property
    def empan_photographique(self):
        """
        (première, dernière) photographie horodatée, ou None.

        C'est ce que la preuve photographique borne — à distinguer de
        (`debut`, `fin`), qui est l'événement lui-même. Un écart entre les deux
        n'est pas une erreur : il signale que l'événement a duré plus longtemps
        que sa trace photographique, ou qu'une photographie a été déliée.
        """
        stamps = sorted(p.datetime_original for p in self.linked_photos.all()
                        if p.datetime_original)
        return (stamps[0], stamps[-1]) if stamps else None

    def synchroniser_bornes(self, forcer=False):
        """
        Aligne `debut`/`fin` sur l'empan photographique.

        Ne touche à rien si les bornes sont déjà posées, sauf `forcer=True` :
        une borne saisie à la main vaut mieux que l'empan, qui n'est qu'un
        plancher. Retourne True si quelque chose a changé.
        """
        empan = self.empan_photographique
        if empan is None:
            return False
        if not forcer and self.debut is not None and self.fin is not None:
            return False
        if (self.debut, self.fin) == empan:
            return False
        self.debut, self.fin = empan
        return True

    def libelle_horodate(self):
        """
        « Le 31 mars 2012, entre 14 h 46 et 16 h 26 » — construit à la lecture,
        jamais stocké. Formate sans conversion de fuseau (voir la convention
        documentée sur `debut`).
        """
        MOIS = [None, "janvier", "février", "mars", "avril", "mai", "juin",
                "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        # Le jour vient de `debut` quand il est posé, sinon de `date`. Les deux
        # divergent sur E-326 (date au 6 mars, photographies au 16) ; prendre
        # le jour d'un champ et l'heure de l'autre produirait un libellé qui
        # n'a jamais existé.
        jour_ref = self.debut.date() if self.debut else self.date
        if not jour_ref:
            return ""
        jour = "1er" if jour_ref.day == 1 else str(jour_ref.day)
        tete = f"Le {jour} {MOIS[jour_ref.month]} {jour_ref.year}"
        if not self.debut:
            return tete
        d = self.debut.strftime("%H h %M")
        if not self.fin or self.fin == self.debut:
            return f"{tete}, à {d}"
        return f"{tete}, entre {d} et {self.fin.strftime('%H h %M')}"

    def description_horodatee(self):
        """Le libellé et la description, tels qu'on les présente ensemble."""
        texte = (self.explanation or "").strip()
        libelle = self.libelle_horodate()
        if not texte:
            return libelle
        return f"{libelle} : {texte}" if libelle else texte

    def get_absolute_url(self):
        """Returns the canonical URL for an event."""
        return reverse('events:detail', kwargs={'pk': self.pk})

    def get_public_url(self):
        return self.get_absolute_url()

    def get_display_id(self):
        return f"E-{self.pk}"

    def __str__(self):
        date_str = self.date.strftime('%Y-%m-%d') if self.date else "[No Date]"
        display_id_str = self.get_display_id() if self.pk else "New Event"
        description = self.explanation[:50] + '...' if self.explanation else "No explanation"

        linked_summary = []
        if self.pk:
            if self.linked_photos.exists():
                linked_summary.append(f"{self.linked_photos.count()} photo(s)")
            if self.linked_email:
                 linked_summary.append("1 email")

        linked_str = f" ({', '.join(linked_summary)})" if linked_summary else ""

        return f"{display_id_str} - {description} ({date_str}){linked_str}"

class SupportingEvidenceLinkedPhotos(models.Model):
    supportingevidence = models.ForeignKey(Event, models.DO_NOTHING, db_column='supportingevidence_id')
    photo = models.ForeignKey(Photo, models.DO_NOTHING)

    class Meta:
        db_table = 'SupportingEvidence_supportingevidence_linked_photos'
        # The 'managed = False' line has been removed. Django will now manage this table.
        unique_together = (('supportingevidence', 'photo'),)
