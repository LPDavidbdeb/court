"""
Index sur la clé générique d'un appui.

La question « quelles pièces n'appuient aucun paragraphe ? » se pose sur les
334 lignes du bordereau contre ~500 appuis, par le couple
(content_type, object_id). Sans index, c'est un balayage complet à chaque
lecture — la même raison qui a valu le sien à `RattachementAxe`.

La contrainte d'unicité sur `Fait.statement` a été écartée : trois paragraphes
portent aujourd'hui plusieurs `Fait`, deux axes ayant chacun créé le sien. Les
fusionner est une décision de fond, pas une migration.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('argument_manager', '0011_rattachement_axe'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='appuifait',
            index=models.Index(fields=['content_type', 'object_id'],
                               name='appui_cle_generique_idx'),
        ),
    ]
