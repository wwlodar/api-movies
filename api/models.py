from django.db import models


class Movie(models.Model):
  Title = models.CharField(max_length=200, unique=True)
  Year = models.CharField(max_length=200)
  Rated = models.CharField(max_length=200)
  Released = models.CharField(max_length=200)
  Runtime = models.CharField(max_length=200)
  Genre = models.CharField(max_length=200)
  Director = models.CharField(max_length=200)
  Writer = models.CharField(max_length=200)
  Actors = models.CharField(max_length=200)
  Plot = models.CharField(max_length=400)
  Language = models.CharField(max_length=200)
  Country = models.CharField(max_length=200)
  Awards = models.CharField(max_length=200)
  Poster = models.CharField(max_length=200)
  Metascore = models.CharField(max_length=200, null=True)
  totalSeasons = models.IntegerField(null=True)
  imdbRating = models.DecimalField(decimal_places=1, max_digits=5, null=True)
  imdbVotes = models.CharField(max_length=200, null=True)
  imdbID = models.CharField(max_length=200, null=True)
  Type = models.CharField(max_length=200, null=True)
  DVD = models.CharField(max_length=200, null=True)
  BoxOffice = models.CharField(max_length=200, null=True)
  Production = models.CharField(max_length=200, null=True)
  Website = models.CharField(max_length=200, null=True)


class Ratings(models.Model):
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='Ratings', null=True, blank=True)
  Source = models.CharField(max_length=200)
  Value = models.CharField(max_length=200)

  class Meta:
    verbose_name_plural = "Ratings"


class Comment(models.Model):
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
  text = models.CharField(max_length=1000)
  author = models.CharField(max_length=200)
