# Generated by Django 5.1.1 on 2025-01-16 16:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eddn', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datalog',
            options={'ordering': ['-updated_at'], 'verbose_name': 'data log', 'verbose_name_plural': 'data logs'},
        ),
        migrations.RemoveField(
            model_name='datalog',
            name='creat_at',
        ),
        migrations.RemoveField(
            model_name='datalog',
            name='update',
        ),
        migrations.AddField(
            model_name='datalog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datalog',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
    ]
