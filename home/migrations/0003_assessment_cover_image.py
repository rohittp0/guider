# Generated by Django 4.2.7 on 2023-11-14 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_response_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='cover_image',
            field=models.ImageField(default=0, upload_to=''),
            preserve_default=False,
        ),
    ]