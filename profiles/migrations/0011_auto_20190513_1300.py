# Generated by Django 2.2 on 2019-05-13 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20190513_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accomplishments',
            name='test_date',
        ),
        migrations.RemoveField(
            model_name='accomplishments',
            name='test_description',
        ),
        migrations.RemoveField(
            model_name='accomplishments',
            name='test_score',
        ),
    ]
