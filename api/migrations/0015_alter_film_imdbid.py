# Generated by Django 3.2.8 on 2021-10-20 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_rename_film_id_comment_film'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='imdbID',
            field=models.IntegerField(null=True),
        ),
    ]
