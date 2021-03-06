# Generated by Django 3.2.6 on 2021-10-26 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_film_imdbid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=200, unique=True)),
                ('Year', models.CharField(max_length=200)),
                ('Rated', models.CharField(max_length=200)),
                ('Released', models.CharField(max_length=200)),
                ('Runtime', models.CharField(max_length=200)),
                ('Genre', models.CharField(max_length=200)),
                ('Director', models.CharField(max_length=200)),
                ('Writer', models.CharField(max_length=200)),
                ('Actors', models.CharField(max_length=200)),
                ('Plot', models.CharField(max_length=400)),
                ('Language', models.CharField(max_length=200)),
                ('Country', models.CharField(max_length=200)),
                ('Awards', models.CharField(max_length=200)),
                ('Poster', models.CharField(max_length=200)),
                ('Metascore', models.CharField(max_length=200, null=True)),
                ('totalSeasons', models.IntegerField(null=True)),
                ('imdbRating', models.DecimalField(decimal_places=1, max_digits=5, null=True)),
                ('imdbVotes', models.CharField(max_length=200, null=True)),
                ('imdbID', models.CharField(max_length=200, null=True)),
                ('Type', models.CharField(max_length=200, null=True)),
                ('DVD', models.CharField(max_length=200, null=True)),
                ('BoxOffice', models.CharField(max_length=200, null=True)),
                ('Production', models.CharField(max_length=200, null=True)),
                ('Website', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='ratings',
            name='film',
        ),
        migrations.AddField(
            model_name='ratings',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Ratings', to='api.movie'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.movie'),
        ),
        migrations.DeleteModel(
            name='Film',
        ),
    ]
