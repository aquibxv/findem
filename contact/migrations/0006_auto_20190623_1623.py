# Generated by Django 2.2 on 2019-06-23 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_auto_20190623_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptedproject',
            name='message',
            field=models.CharField(default='has accepted your connection request.', max_length=50),
        ),
    ]