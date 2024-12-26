# Generated by Django 5.0 on 2024-05-30 18:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ed_economy', '0001_initial'),
        ('ed_station', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='commodityinstation',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', related_query_name='%(app_label)s_%(class)ss', to='ed_station.station', verbose_name='station'),
        ),
        migrations.AddField(
            model_name='commodityinstation',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated by'),
        ),
        migrations.AddIndex(
            model_name='commodityinstation',
            index=models.Index(fields=['station'], name='ed_economy__station_5fb3ee_idx'),
        ),
        migrations.AddIndex(
            model_name='commodityinstation',
            index=models.Index(fields=['commodity'], name='ed_economy__commodi_eb3c60_idx'),
        ),
        migrations.AddConstraint(
            model_name='commodityinstation',
            constraint=models.UniqueConstraint(fields=('station', 'commodity'), name='unique_commodity_in_station'),
        ),
    ]