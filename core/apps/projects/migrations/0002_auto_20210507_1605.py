# Generated by Django 3.1.7 on 2021-05-07 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='point_duration',
            field=models.FloatField(default=1.0, help_text='An approximate story point duration (in hours).', verbose_name='point duration'),
        ),
        migrations.AddField(
            model_name='product',
            name='point_duration',
            field=models.FloatField(default=1.0, help_text='An approximate story point duration (in hours).', verbose_name='point duration'),
        ),
    ]
