# Generated by Django 2.2 on 2019-07-21 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0034_auto_20190721_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='photos/profile_pictures/user.gif', null=True, upload_to='photos/profile_pictures/'),
        ),
    ]
