# Generated by Django 2.2 on 2019-07-07 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0025_remove_personalinformation_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinformation',
            name='college_university',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]