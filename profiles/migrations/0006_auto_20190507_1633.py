# Generated by Django 2.2 on 2019-05-07 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_personalinformation_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinformation',
            name='language_1',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='language_2',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='language_3',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
