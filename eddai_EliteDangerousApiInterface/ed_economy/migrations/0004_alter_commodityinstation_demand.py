# Generated by Django 4.1 on 2023-04-06 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ed_economy', '0003_commodity_meanprice_commodityinstation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodityinstation',
            name='demand',
            field=models.FloatField(default=0, help_text='the demand of the commodity', verbose_name='demand'),
        ),
    ]
