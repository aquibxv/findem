# Generated by Django 2.2 on 2019-07-21 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0026_personalinformation_college_university'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(upload_to='photos/profile_pictures'),
        ),
    ]