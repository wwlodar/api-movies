# Generated by Django 3.2.8 on 2021-10-18 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20211018_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='imdbRating',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='film',
            name='imdbVotes',
            field=models.CharField(max_length=200),
        ),
    ]
