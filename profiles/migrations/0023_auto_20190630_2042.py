# Generated by Django 2.2 on 2019-06-30 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0022_auto_20190630_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperience',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]