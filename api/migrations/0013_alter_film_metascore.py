# Generated by Django 3.2.8 on 2021-10-18 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20211018_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='Metascore',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
