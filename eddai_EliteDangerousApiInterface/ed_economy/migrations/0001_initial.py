# Generated by Django 4.1 on 2022-08-11 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Economy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'economy',
                'verbose_name_plural': 'economies',
            },
        ),
    ]
