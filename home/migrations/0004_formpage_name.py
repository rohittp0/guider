# Generated by Django 4.2.7 on 2023-11-14 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_assessment_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='formpage',
            name='name',
            field=models.CharField(default='', max_length=30),
        ),
    ]
