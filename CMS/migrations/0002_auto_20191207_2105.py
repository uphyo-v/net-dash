# Generated by Django 2.2.7 on 2019-12-07 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='EndDate',
            field=models.TextField(default='dd/mm/yyyy'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='StartDate',
            field=models.TextField(default='dd/mm/yyyy'),
        ),
    ]