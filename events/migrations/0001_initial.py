# events/migrations/0001_initial.py
# THIS IS THE MANUALLY CORRECTED FILE

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # These are the correct, final dependencies
        ('photos', '0005_alter_phototype_options_photo_datetime_utc_and_more'),
        ('document_manager', '0005_documentnode_is_falsifiable_documentnode_is_true'),
        ('email_manager', '0005_quote'),
    ]

    operations = [
        # This is the intermediate M2M table model, which we need
        migrations.CreateModel(
            name='EventLinkedPhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'SupportingEvidence_supportingevidence_linked_photos',
                'managed': False,
            },
        ),
        # This is the final version of your Event model
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='The date of the event.')),
                ('explanation', models.TextField(blank=True, help_text='A detailed explanation of the event, auto-filled for photo clusters.')),
                ('email_quote', models.TextField(blank=True, help_text='A specific quote or excerpt from an email.', null=True)),
                # This now correctly points to DocumentNode
                ('allegation', models.ForeignKey(blank=True, help_text='The specific allegation this event supports or refutes.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='document_manager.documentnode')),
                # This now correctly points to the Email model
                ('linked_email', models.ForeignKey(blank=True, help_text='The specific email this quote is from.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='email_manager.email')),
                # The through model now correctly references the new app name
                ('linked_photos', models.ManyToManyField(blank=True, help_text='A collection of photos related to this event.', related_name='events', through='events.EventLinkedPhotos', to='photos.photo')),
                # The self-reference now correctly points to itself
                ('parent', models.ForeignKey(blank=True, help_text='The parent event for this piece of evidence.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='events.event')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                # THIS IS THE CRITICAL LINE: It tells this model to use the existing table
                'db_table': 'SupportingEvidence_supportingevidence',
                'ordering': ['date'],
            },
        ),
    ]