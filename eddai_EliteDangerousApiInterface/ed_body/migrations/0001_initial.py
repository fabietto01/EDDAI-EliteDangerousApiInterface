# Generated by Django 5.0 on 2024-05-29 15:09

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ed_system', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AtmosphereComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_eddn', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('note', models.TextField(blank=True, null=True, verbose_name='note')),
            ],
            options={
                'verbose_name': 'atmosphere component',
                'verbose_name_plural': 'atmosphere components',
            },
        ),
        migrations.CreateModel(
            name='AtmosphereType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_eddn', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('note', models.TextField(blank=True, null=True, verbose_name='note')),
            ],
            options={
                'verbose_name': 'atmosphere type',
                'verbose_name_plural': 'atmosphere types',
            },
        ),
        migrations.CreateModel(
            name='BaseBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('bodyID', models.PositiveIntegerField(verbose_name='body ID')),
                ('parentsID', models.PositiveSmallIntegerField(default=0, help_text='enter the body ID of the object which orbit', null=True, verbose_name='parents ID')),
                ('distance', models.FloatField(help_text='distance from the stary center', null=True, validators=[django.core.validators.MinValueValidator(0, 'the distance cannot be less than 0')], verbose_name='distance')),
                ('radius', models.FloatField(blank=True, help_text='radius of the body', null=True, validators=[django.core.validators.MinValueValidator(0, 'the radius cannot be less than 0')], verbose_name='radius')),
                ('surfaceTemperature', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, 'the surface temperature cannot be less than 0')], verbose_name='surface temperature')),
                ('eccentricity', models.FloatField(blank=True, help_text='eccentricity of the orbit', null=True, validators=[django.core.validators.MinValueValidator(0, 'the eccentricity cannot be less than 0'), django.core.validators.MaxValueValidator(1, 'the eccentricity cannot be greater than 1')], verbose_name='eccentricity')),
                ('orbitalInclination', models.FloatField(blank=True, help_text='orbital inclination of the body', null=True, validators=[django.core.validators.MinValueValidator(-360, 'the orbital inclination cannot be less than -360'), django.core.validators.MaxValueValidator(360, 'the orbital inclination cannot be greater than 360')], verbose_name='orbital inclination')),
                ('orbitalPeriod', models.FloatField(blank=True, help_text='orbital period of the body in days', null=True, validators=[django.core.validators.MinValueValidator(0, 'the orbital period cannot be less than 0')], verbose_name='orbital period')),
                ('periapsis', models.FloatField(blank=True, help_text='periapsis of the body', null=True, verbose_name='periapsis')),
                ('semiMajorAxis', models.FloatField(blank=True, help_text='semi major axis of the orbit', null=True, validators=[django.core.validators.MinValueValidator(0, 'the semi major axis cannot be less than 0')], verbose_name='semi major axis')),
                ('ascendingNode', models.FloatField(blank=True, help_text='ascending node of the orbit', null=True, verbose_name='ascending node')),
                ('meanAnomaly', models.FloatField(blank=True, help_text='mean anomaly of the orbit', null=True, verbose_name='mean anomaly')),
                ('axialTilt', models.FloatField(blank=True, help_text='axial tilt of the body', null=True, validators=[django.core.validators.MinValueValidator(-360, 'the axial tilt cannot be less than -360'), django.core.validators.MaxValueValidator(360, 'the axial tilt cannot be greater than 360')], verbose_name='axial tilt')),
                ('rotationPeriod', models.FloatField(blank=True, help_text='rotation period of the body in seconds', null=True, verbose_name='rotation period')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', related_query_name='%(app_label)s_%(class)ss', to='ed_system.system', verbose_name='system')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'body',
                'verbose_name_plural': 'bodies',
            },
        ),
        migrations.CreateModel(
            name='PlanetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('note', models.TextField(blank=True, null=True, verbose_name='note')),
            ],
            options={
                'verbose_name': 'planet type',
                'verbose_name_plural': 'planet types',
            },
        ),
        migrations.CreateModel(
            name='StarLuminosity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('note', models.TextField(blank=True, null=True, verbose_name='note')),
            ],
            options={
                'verbose_name': 'star luminosity',
                'verbose_name_plural': 'star luminosities',
            },
        ),
        migrations.CreateModel(
            name='StarType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_eddn', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('note', models.TextField(blank=True, null=True, verbose_name='note')),
            ],
            options={
                'verbose_name': 'star type',
                'verbose_name_plural': 'star types',
            },
        ),
        migrations.CreateModel(
            name='Volcanism',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_eddn', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('note', models.TextField(blank=True, null=True, verbose_name='note')),
            ],
            options={
                'verbose_name': 'volcanism',
                'verbose_name_plural': 'volcanisms',
            },
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('basebody_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ed_body.basebody')),
                ('terraformState', models.CharField(blank=True, choices=[('Terraformable', 'Terraformable'), ('Terraforming', 'Terraforming'), ('Terraformed', 'Terraformed'), ('', 'Not Terraformable')], max_length=15, null=True, verbose_name='terraform state')),
                ('_compositionIce', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0, 'the composition ice cannot be less than 0')], verbose_name='ice')),
                ('_compositionRock', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0, 'the composition rock cannot be less than 0')], verbose_name='rock')),
                ('_compositionMetal', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0, 'the composition metal cannot be less than 0')], verbose_name='metal')),
                ('landable', models.BooleanField(null=True, verbose_name='landable')),
                ('massEM', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0, 'the mass cannot be less than 0')], verbose_name='Earth masses')),
                ('surfaceGravity', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0, 'the surface gravity cannot be less than 0')], verbose_name='surface gravity')),
                ('surfacePressure', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0, 'the surface pressure cannot be less than 0')], verbose_name='surface pressure')),
                ('tidalLock', models.BooleanField(help_text='Tidal locking results in the moon rotating about its axis in about the same time it takes to orbit Body.', null=True, verbose_name='tidal lock')),
                ('reserveLevel', models.CharField(choices=[('Pristine', 'Pristine'), ('Major', 'Major'), ('Common', 'Common'), ('Low', 'Low'), ('Depleted', 'Depleted')], max_length=10, null=True, verbose_name='reserve level')),
                ('atmosphereType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s_related', related_query_name='%(app_label)s_%(class)ss', to='ed_body.atmospheretype', verbose_name='atmosphere type')),
                ('planetType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s_related', related_query_name='%(app_label)s_%(class)ss', to='ed_body.planettype', verbose_name='planet type')),
                ('volcanism', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s_related', related_query_name='%(app_label)s_%(class)ss', to='ed_body.volcanism', verbose_name='volcanism')),
            ],
            options={
                'verbose_name': 'planet',
                'verbose_name_plural': 'planets',
            },
            bases=('ed_body.basebody',),
        ),
        migrations.CreateModel(
            name='AtmosphereComponentInPlanet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('percent', models.FloatField(validators=[django.core.validators.MinValueValidator(0, 'the percent cannot be less than 0'), django.core.validators.MaxValueValidator(100, 'the percent cannot be greater than 100')], verbose_name='percent')),
                ('atmosphere_component', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s_related', related_query_name='%(app_label)s_%(class)ss', to='ed_body.atmospherecomponent', verbose_name='atmosphere component')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
                ('planet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', related_query_name='%(app_label)s_%(class)ss', to='ed_body.planet', verbose_name='planet')),
            ],
            options={
                'verbose_name': 'atmosphere component in planet',
                'verbose_name_plural': 'atmosphere components in planets',
            },
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('basebody_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ed_body.basebody')),
                ('absoluteMagnitude', models.FloatField(validators=[django.core.validators.MinValueValidator(0, 'the absolute magnitude cannot be less than 0')], verbose_name='absolute magnitude')),
                ('age', models.FloatField(help_text='age in millions of years', validators=[django.core.validators.MinValueValidator(0, 'the age cannot be less than 0')], verbose_name='age')),
                ('stellarMass', models.FloatField(help_text="mass as multiple of Sol's mass", validators=[django.core.validators.MinValueValidator(0, 'the stellar mass cannot be less than 0')], verbose_name='stellar mass')),
                ('subclass', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, 'the subclass cannot be less than 0'), django.core.validators.MaxValueValidator(9, 'the subclass cannot be greater than 9')], verbose_name='subclass')),
                ('luminosity', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s_related', related_query_name='%(app_label)s_%(class)ss', to='ed_body.starluminosity', verbose_name='luminosity')),
                ('starType', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s_related', related_query_name='%(app_label)s_%(class)ss', to='ed_body.startype', verbose_name='star type')),
            ],
            options={
                'verbose_name': 'star',
                'verbose_name_plural': 'stars',
            },
            bases=('ed_body.basebody',),
        ),
        migrations.AddIndex(
            model_name='basebody',
            index=models.Index(fields=['system'], name='ed_body_bas_system__c8c1e4_idx'),
        ),
        migrations.AddIndex(
            model_name='basebody',
            index=models.Index(fields=['bodyID'], name='ed_body_bas_bodyID_f8396f_idx'),
        ),
        migrations.AddConstraint(
            model_name='basebody',
            constraint=models.UniqueConstraint(fields=('name', 'system'), name='unique_body_in_system'),
        ),
        migrations.AddConstraint(
            model_name='basebody',
            constraint=models.UniqueConstraint(fields=('bodyID', 'system'), name='unique_bodyID_in_system'),
        ),
        migrations.AddIndex(
            model_name='planet',
            index=models.Index(fields=['atmosphereType'], name='ed_body_pla_atmosph_0b73ab_idx'),
        ),
        migrations.AddIndex(
            model_name='planet',
            index=models.Index(fields=['planetType'], name='ed_body_pla_planetT_d94fa0_idx'),
        ),
        migrations.AddIndex(
            model_name='planet',
            index=models.Index(fields=['volcanism'], name='ed_body_pla_volcani_a2039a_idx'),
        ),
        migrations.AddIndex(
            model_name='planet',
            index=models.Index(fields=['terraformState'], name='ed_body_pla_terrafo_34bc81_idx'),
        ),
        migrations.AddIndex(
            model_name='planet',
            index=models.Index(fields=['landable'], name='ed_body_pla_landabl_11e03a_idx'),
        ),
        migrations.AddIndex(
            model_name='planet',
            index=models.Index(fields=['tidalLock'], name='ed_body_pla_tidalLo_3b8402_idx'),
        ),
        migrations.AddIndex(
            model_name='planet',
            index=models.Index(fields=['reserveLevel'], name='ed_body_pla_reserve_cb036b_idx'),
        ),
        migrations.AddIndex(
            model_name='atmospherecomponentinplanet',
            index=models.Index(fields=['planet'], name='planet_component_planet_idx'),
        ),
        migrations.AddIndex(
            model_name='atmospherecomponentinplanet',
            index=models.Index(fields=['atmosphere_component'], name='atmo_component_planet_idx'),
        ),
        migrations.AddConstraint(
            model_name='atmospherecomponentinplanet',
            constraint=models.UniqueConstraint(fields=('planet', 'atmosphere_component'), name='planet_atmo_component_uc'),
        ),
        migrations.AddIndex(
            model_name='star',
            index=models.Index(fields=['luminosity', 'starType'], name='luminosity_starType_idx'),
        ),
    ]
