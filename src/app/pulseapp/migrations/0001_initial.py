# Generated by Django 3.2.6 on 2022-04-08 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='covtype',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, max_length=200, null=True)),
                ('typedef', models.CharField(blank=True, max_length=200, null=True)),
                ('unitdef', models.CharField(blank=True, max_length=200, null=True)),
                ('units', models.CharField(blank=True, max_length=200, null=True)),
                ('idtype', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='polygon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('polygonid', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('pop', models.FloatField(blank=True, null=True)),
                ('type', models.CharField(blank=True, default='swrCat', editable=False, max_length=200, null=True)),
                ('wkt', models.CharField(blank=True, max_length=200, null=True)),
                ('link', models.CharField(blank=True, max_length=200, null=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='sampledata',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sampleid', models.CharField(blank=True, max_length=200, null=True)),
                ('submited_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('datestart', models.DateField(blank=True, null=True)),
                ('dateend', models.DateField(blank=True, null=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('type', models.CharField(blank=True, default='rawWW', editable=False, max_length=200, null=True)),
                ('collection', models.CharField(blank=True, default='cpTP24h', editable=False, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='site',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('siteID', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('publicHealthDepartment', models.CharField(blank=True, max_length=200, null=True)),
                ('healthRegion', models.CharField(blank=True, max_length=200, null=True)),
                ('type', models.CharField(blank=True, max_length=200, null=True)),
                ('geoLat', models.FloatField(blank=True, default=None, null=True)),
                ('geoLong', models.FloatField(blank=True, default=None, null=True)),
                ('link', models.CharField(blank=True, max_length=200, null=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('polygonID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pulseapp.polygon')),
            ],
        ),
        migrations.CreateModel(
            name='uwtp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uwwName', models.CharField(blank=True, max_length=200, null=True)),
                ('station', models.CharField(blank=True, max_length=200, null=True)),
                ('agg_name', models.CharField(blank=True, max_length=200, null=True)),
                ('uwwLatitud', models.FloatField(blank=True, default=None, null=True)),
                ('uwwLongitu', models.FloatField(blank=True, default=None, null=True)),
                ('agg_type', models.CharField(blank=True, max_length=200, null=True)),
                ('init', models.CharField(blank=True, max_length=200, null=True)),
                ('station_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pulseapp.site')),
            ],
        ),
        migrations.CreateModel(
            name='variantType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='wwmeasure',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('wwmeasureid', models.CharField(blank=True, max_length=200, null=True)),
                ('submited_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('analysisdate', models.DateField(blank=True, null=True)),
                ('reportdate', models.DateField(blank=True, null=True)),
                ('fractionAnalyzed', models.CharField(blank=True, default='liquid', max_length=200, null=True)),
                ('value', models.FloatField(blank=True, default=None, null=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('covtype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pulseapp.covtype')),
                ('sampleid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pulseapp.sampledata')),
            ],
        ),
        migrations.CreateModel(
            name='variants',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sampleid', models.CharField(blank=True, max_length=200, null=True)),
                ('Lineage', models.CharField(blank=True, max_length=200, null=True)),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
                ('submited_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('datestart', models.DateField(blank=True, null=True)),
                ('dateend', models.DateField(blank=True, null=True)),
                ('VariantType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pulseapp.varianttype')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pulseapp.uwtp')),
                ('loginname', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='trends',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('submited_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('fromdate', models.DateField(blank=True, null=True)),
                ('todate', models.DateField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, default=None, null=True)),
                ('loginname', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('samplestationid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pulseapp.uwtp')),
            ],
        ),
        migrations.AddField(
            model_name='sampledata',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pulseapp.uwtp'),
        ),
        migrations.AddField(
            model_name='sampledata',
            name='loginname',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
