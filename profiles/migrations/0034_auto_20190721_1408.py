# Generated by Django 2.2 on 2019-07-21 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0033_auto_20190721_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='photos/profile_pictures/user.gif', null=True, upload_to='photos/profile_pictures/'),
        ),
    ]
