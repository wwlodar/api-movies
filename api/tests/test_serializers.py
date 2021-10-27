from rest_framework import serializers
from django.test import TestCase
from ..models import Ratings, Comment, Movie
from ..serializers import RatingsSerializer, MovieSerializer, CommentSerializer


class TestRatingsSerializer(TestCase):
  def setUp(self):
    self.rating_attributes = {
      'Source': 'Rotten Tomatoes',
      'Value': 9.7
    }
    
    self.serializer_data = {
      'Source': 'Rotten Tomatoes',
      'Value': 9.7
    }
    
    self.rating = Ratings.objects.create(**self.rating_attributes)
    self.serializer = RatingsSerializer(instance=self.rating)
  
  def test_contains_expected_fields(self):
    data = self.serializer.data
    
    self.assertEqual(set(data.keys()), set(['Source', 'Value']))
  
  def test_Source_field_content(self):
    data = self.serializer.data
    
    self.assertEqual(data['Source'], self.rating_attributes['Source'])
  
  def test_Value_field_content(self):
    data = self.serializer.data
    
    self.assertEqual(float(data['Value']), self.rating_attributes['Value'])


class TestMovieSerializer(TestCase):
  def setUp(self):
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
      'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                  {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                  {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
      'imdbRating': '7.5',
      'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
      'BoxOffice': '$77,812,000',
      'Production': 'N/A', 'Website': 'N/A'}
    
    self.movie_attributes = data
    self.movie_data = data
    
    # creating movie serializer
    self.serializer = MovieSerializer(data=self.movie_data)
    if self.serializer.is_valid():
      self.serializer.save()
  
  def test_contains_expected_fields(self):
    data = self.serializer.data
    
    self.assertCountEqual(data.keys(), ['id', 'Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director',
                                        'Writer', 'Actors', 'Plot',
                                        'Language', 'Country', 'Awards', 'Poster', 'Metascore', 'imdbRating',
                                        'imdbVotes',
                                        'imdbID', 'Type', 'DVD', 'BoxOffice', 'Production', 'Website', 'Ratings'])
  
  def test_Title_field_content(self):
    data = self.serializer.data
    
    self.assertEqual(data['Title'], self.movie_attributes['Title'])
    self.assertEqual(data['Year'], self.movie_attributes['Year'])
    self.assertEqual(data['Rated'], self.movie_attributes['Rated'])
    self.assertEqual(data['Released'], self.movie_attributes['Released'])
    self.assertEqual(data['Runtime'], self.movie_attributes['Runtime'])
    self.assertEqual(data['Genre'], self.movie_attributes['Genre'])
    self.assertEqual(data['Director'], self.movie_attributes['Director'])
    self.assertEqual(data['Writer'], self.movie_attributes['Writer'])
    self.assertEqual(data['Actors'], self.movie_attributes['Actors'])
    self.assertEqual(data['Plot'], self.movie_attributes['Plot'])
    self.assertEqual(data['Language'], self.movie_attributes['Language'])
    self.assertEqual(data['Country'], self.movie_attributes['Country'])
    self.assertEqual(data['Awards'], self.movie_attributes['Awards'])
    self.assertEqual(data['Poster'], self.movie_attributes['Poster'])
    self.assertEqual(data['Metascore'], self.movie_attributes['Metascore'])
    self.assertEqual(data['imdbRating'], self.movie_attributes['imdbRating'])
    
    # This value should not be equal as ',' is removed during create().
    self.assertNotEqual(data['imdbVotes'], self.movie_attributes['imdbVotes'])
    self.assertEqual(data['imdbID'], self.movie_attributes['imdbID'])
    
    list = []
    for item in data['Ratings']:
      list.append(dict(item))
    
    self.assertEqual(list, self.movie_attributes['Ratings'])


class TestCommentSerializer(TestCase):
  def setUp(self):
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
      'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                  {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                  {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
      'imdbRating': '7.5',
      'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
      'BoxOffice': '$77,812,000',
      'Production': 'N/A', 'Website': 'N/A'}
    
    self.movie_attributes = data
    self.movie_data = data
    
    # creating movie serializer
    self.movie_serializer = MovieSerializer(data=self.movie_data)
    if self.movie_serializer.is_valid():
      self.movie_serializer.save()
    
    self.comment_data = {
      "text": "Some text",
      "author": "Some author",
      "movie": Movie.objects.first(),
    }
    
    self.serializer = CommentSerializer(instance=self.comment_data)
  
  def test_contains_expected_fields(self):
    data = self.serializer.data
    
    self.assertCountEqual(data.keys(), ('text', 'movie', 'author'))
  
  def test_Source_field_content(self):
    data = self.serializer.data
    
    self.assertEqual(data['author'], self.comment_data['author'])
    self.assertEqual(data['text'], self.comment_data['text'])
    self.assertEqual(data['movie'], Movie.objects.first().id)
