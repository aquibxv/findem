# Generated by Django 2.2 on 2019-05-25 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_project_college'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='author',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='project',
            name='domain',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='project',
            name='skill_1',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='project',
            name='skill_2',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='project',
            name='skill_3',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='project',
            name='skill_4',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=40),
        ),
    ]
