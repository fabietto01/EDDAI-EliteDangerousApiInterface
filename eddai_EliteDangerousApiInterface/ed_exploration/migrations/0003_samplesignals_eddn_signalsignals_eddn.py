# Generated by Django 5.1.1 on 2025-01-16 16:41

import django.db.models.functions.comparison
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ed_exploration', '0002_alter_samplesignals__eddn_alter_signalsignals__eddn'),
    ]

    operations = [
        migrations.AddField(
            model_name='samplesignals',
            name='eddn',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.functions.comparison.Coalesce('_eddn', 'name'), output_field=models.CharField(), verbose_name='eddn'),
        ),
        migrations.AddField(
            model_name='signalsignals',
            name='eddn',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.functions.comparison.Coalesce('_eddn', 'name'), output_field=models.CharField(), verbose_name='eddn'),
        ),
    ]
