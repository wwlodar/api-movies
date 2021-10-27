from django.test import TestCase
from ..models import *


class TestMovieModel(TestCase):
  def test_custom_str(self):
    data = {
      'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
      'Runtime': '167 min',
      'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
      'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
      'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
      'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City",
      'Language': 'English, Irish Gaelic, Chinese, Latin',
      'Country': 'United States, Italy',
      'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
      'Poster': 'https://m.media-amazon.com/images/M/M.jpg',
      'imdbRating': '7.5',
      'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
      'BoxOffice': '$77,812,000',
      'Production': 'N/A', 'Website': 'N/A'}
    movie = Movie.objects.create(**data)
    self.assertEqual(str(movie), 'Id: 1, Name: Gangs of New York')

