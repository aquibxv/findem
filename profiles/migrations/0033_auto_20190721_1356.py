# Generated by Django 2.2 on 2019-07-21 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0032_auto_20190721_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='/media/photos/user.gif', null=True, upload_to='photos/profile_pictures/'),
        ),
    ]
