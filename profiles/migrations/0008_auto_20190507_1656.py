# Generated by Django 2.2 on 2019-05-07 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20190507_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinformation',
            name='mobile',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
