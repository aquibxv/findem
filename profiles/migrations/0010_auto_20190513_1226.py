# Generated by Django 2.2 on 2019-05-13 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_workexperience'),
    ]

    operations = [
        migrations.AddField(
            model_name='workexperience',
            name='description',
            field=models.TextField(blank=True, default=' '),
        ),
        migrations.AddField(
            model_name='workexperience',
            name='from_date',
            field=models.DateField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='workexperience',
            name='to_date',
            field=models.DateField(blank=True, default=None),
        ),
    ]