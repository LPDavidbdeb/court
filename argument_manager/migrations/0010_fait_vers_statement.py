"""
Fait → Statement, et Axe en plusieurs-à-plusieurs.

⚠️ L'ORDRE DES OPÉRATIONS EST PORTEUR. La migration générée automatiquement
supprimait la clé étrangère `axe` AVANT de créer la relation `axes` : les
rattachements existants auraient disparu sans avertissement. On intercale donc
une migration de données entre la création et la suppression, et on la rend
réversible dans les deux sens.
"""
import django.db.models.deletion
from django.db import migrations, models


def fk_vers_m2m(apps, schema_editor):
    """Recopie `fait.axe` dans `fait.axes` avant que la colonne disparaisse."""
    Fait = apps.get_model('argument_manager', 'Fait')
    for fait in Fait.objects.exclude(axe__isnull=True):
        fait.axes.add(fait.axe)


def m2m_vers_fk(apps, schema_editor):
    """
    Retour arrière : on ne peut retenir qu'un seul axe par fait. Le premier
    est conservé; s'il y en avait plusieurs, l'information est perdue — c'est
    la nature même du retour à une clé étrangère.
    """
    Fait = apps.get_model('argument_manager', 'Fait')
    for fait in Fait.objects.all():
        premier = fait.axes.first()
        if premier:
            fait.axe = premier
            fait.save(update_fields=['axe'])


class Migration(migrations.Migration):

    dependencies = [
        ('argument_manager', '0009_axe_fait_appuifait'),
        ('document_manager', '0015_schemaniveaux_document_schema_niveau'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fait',
            options={'ordering': ['ordre'], 'verbose_name': 'Fait',
                     'verbose_name_plural': 'Faits'},
        ),
        # 1. la nouvelle relation
        migrations.AddField(
            model_name='fait',
            name='axes',
            field=models.ManyToManyField(related_name='faits',
                                         to='argument_manager.axe'),
        ),
        # 2. les données passent de l'une à l'autre — AVANT toute suppression
        migrations.RunPython(fk_vers_m2m, m2m_vers_fk),
        # 3. seulement maintenant, l'ancienne colonne peut tomber
        migrations.RemoveField(
            model_name='fait',
            name='axe',
        ),
        migrations.AddField(
            model_name='fait',
            name='nature',
            field=models.CharField(
                choices=[('PROPOSITION', "Ce que l'axe affirme"),
                         ('DOCUMENTAIRE', "Ce qu'une pièce dit"),
                         ('STRUCTUREL', "La structure d'une institution ou d'un cadre"),
                         ('RESERVE', "Ce qui n'est PAS allégué — neutralise une objection"),
                         ('INFERENCE', "Tiré d'une conduite, non d'une affirmation"),
                         ('CONSEQUENCE', 'Découle des faits précédents')],
                default='DOCUMENTAIRE', max_length=14),
        ),
        migrations.AddField(
            model_name='fait',
            name='raison',
            field=models.TextField(
                blank=True,
                help_text="POURQUOI ce fait est formulé ainsi. Ne se plaide pas — "
                          "c'est ce qui empêche une relecture de couper une clause "
                          "porteuse en la prenant pour du remplissage."),
        ),
        migrations.AddField(
            model_name='fait',
            name='statement',
            field=models.ForeignKey(
                blank=True,
                help_text="Le paragraphe PRODUCED qui plaide ce fait. NULL = le "
                          "fait n'est pas encore au dossier.",
                null=True, on_delete=django.db.models.deletion.SET_NULL,
                related_name='faits', to='document_manager.statement'),
        ),
        migrations.AlterField(
            model_name='fait',
            name='enonce',
            field=models.TextField(
                help_text="Le fait tel qu'on souhaite le plaider. Brouillon tant "
                          "que `statement` est vide."),
        ),
    ]
