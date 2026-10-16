from django.db import models, transaction
from django.urls import reverse


class StatutCause(models.TextChoices):
    A_PRECISER = 'A_PRECISER', 'À préciser'
    EN_COURS = 'EN_COURS', 'En cours'
    SUSPENDUE = 'SUSPENDUE', 'Suspendue'
    CLOSE = 'CLOSE', 'Close'


class Cause(models.Model):
    """Identité judiciaire, indépendante des systèmes de construction de preuve."""

    numero_dossier = models.CharField('numéro de dossier', max_length=100, unique=True)
    titre = models.CharField(max_length=255)
    tribunal = models.CharField(max_length=255, blank=True)
    district_judiciaire = models.CharField(
        'district judiciaire', max_length=255, blank=True,
        help_text="District du dossier enregistré, par exemple Longueuil ou Montréal. "
                  "Laisser vide s'il reste à vérifier.",
    )
    notes = models.TextField(blank=True)
    creee_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['numero_dossier']
        verbose_name = 'cause'

    def __str__(self):
        return f'{self.numero_dossier} — {self.titre}'

    def get_absolute_url(self):
        return reverse('cause_manager:detail', kwargs={'pk': self.pk})

    @property
    def etat_actuel(self):
        # Le dernier état consigné gouverne. Sa date d'effet peut être inconnue.
        return next(iter(self.etats.all()), None)

    @property
    def statut(self):
        etat = self.etat_actuel
        return etat.statut if etat else StatutCause.A_PRECISER

    def get_statut_display(self):
        return StatutCause(self.statut).label

    def consigner_etat(self, statut, *, date_effet=None, motif=''):
        """Ajoute une observation sans écraser l'historique ni inventer sa date."""
        with transaction.atomic():
            Cause.objects.select_for_update().get(pk=self.pk)
            etat = EtatCause(
                cause=self, statut=statut, date_effet=date_effet, motif=motif,
            )
            etat.full_clean()
            etat.save()
        # Une instance préchargée doit refléter l'observation qu'elle vient d'ajouter.
        getattr(self, '_prefetched_objects_cache', {}).pop('etats', None)
        return etat


class EtatCause(models.Model):
    cause = models.ForeignKey(Cause, on_delete=models.PROTECT, related_name='etats')
    statut = models.CharField(max_length=20, choices=StatutCause.choices)
    date_effet = models.DateField(
        "date d'effet", null=True, blank=True,
        help_text="Laisser vide si la date réelle du changement est inconnue.",
    )
    motif = models.TextField(blank=True, help_text="Contexte ou source de cette observation.")
    consigne_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-consigne_le', '-pk']
        verbose_name = 'état consigné'
        verbose_name_plural = 'états consignés'

    def __str__(self):
        return f'{self.cause.numero_dossier} : {self.get_statut_display()}'


class LienCause(models.Model):
    cause = models.ForeignKey(Cause, on_delete=models.PROTECT, related_name='liens_sortants')
    cause_liee = models.ForeignKey(Cause, on_delete=models.PROTECT, related_name='liens_entrants')
    description = models.TextField(help_text="Expliquer le rapport entre les deux causes.")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cause', 'cause_liee'], name='cause_lien_unique'),
            models.CheckConstraint(
                condition=~models.Q(cause=models.F('cause_liee')), name='cause_lien_distinct',
            ),
        ]
        verbose_name = 'lien entre causes'
        verbose_name_plural = 'liens entre causes'

    def __str__(self):
        return f'{self.cause.numero_dossier} → {self.cause_liee.numero_dossier}'
