# Generated by Django 2.2 on 2019-07-07 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_auto_20190707_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='link_1',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='link_2',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='link_3',
            field=models.URLField(blank=True, null=True),
        ),
    ]