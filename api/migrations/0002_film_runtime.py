# Generated by Django 3.2.8 on 2021-10-15 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='runtime',
            field=models.CharField(default=42, max_length=200),
            preserve_default=False,
        ),
    ]