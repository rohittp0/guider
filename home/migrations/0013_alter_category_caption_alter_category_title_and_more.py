# Generated by Django 4.2.7 on 2024-02-17 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_question_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='caption',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='options',
            name='option_text',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='caption',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='url',
            field=models.CharField(max_length=500),
        ),
    ]
