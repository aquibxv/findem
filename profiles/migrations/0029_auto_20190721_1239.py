# Generated by Django 2.2 on 2019-07-21 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0028_auto_20190721_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='photos/user.gif', upload_to='photos/profile_pictures/'),
        ),
    ]
