# Generated by Django 3.2.8 on 2021-10-15 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20211015_1840'),
    ]

    operations = [
        migrations.RenameField(
            model_name='film',
            old_name='title',
            new_name='Title',
        ),
        migrations.AddField(
            model_name='film',
            name='Year',
            field=models.IntegerField(default=2000),
            preserve_default=False,
        ),
    ]
