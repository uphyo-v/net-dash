# Generated by Django 2.2.7 on 2020-01-21 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CMS', '0007_auto_20200102_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='Category',
            field=models.CharField(choices=[('Router', 'Router'), ('Switch', 'Switch'), ('WAN Optimizer', 'WAN Optimizer'), ('Choose category', 'Choose the category')], default='Choose category', max_length=500),
        ),
        migrations.CreateModel(
            name='Circuit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CircuitID', models.TextField(default='Circuit ID')),
                ('Bandwidth', models.TextField(default='Mbps')),
                ('WANIP', models.TextField(default='x.x.x.x - y')),
                ('CircuitType', models.CharField(choices=[('Primary', 'Primary'), ('Secondary', 'Secondary'), ('Choose circuit type', 'Choose circuit type')], default='Choose circuit type', max_length=500)),
                ('Project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.Projects')),
                ('Site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.Sites')),
            ],
        ),
    ]
