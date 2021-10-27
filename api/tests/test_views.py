from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse
import requests
import json
from ..views import *
from rest_framework.test import APIClient
import mock


class TestAPIOverview(APITestCase):
  def test_get(self):
    response = self.client.get(reverse("api_overview-list"))
    self.assertEqual(200, response.status_code)
    
    response_data = json.loads(response.content)
    self.assertEqual({
      'Get or post a movie': 'api/movie/',
      'Get or post a comment': 'api/comments/',
    }, response_data)


class TestGetMovies(APITestCase):
  def test_get_no_movies(self):
    response = self.client.get(reverse("movie-list"))
    self.assertEqual(200, response.status_code)
    
    response_data = json.loads(response.content)
    self.assertEqual([], response_data)
  
  def test_get_one_movie(self):
    # create film object and get json representation of it
    data = {"id": 1,
            "Title": "Harry Potter and the Deathly Hallows: Part 2",
            "Year": "2011",
            "Rated": "PG-13",
            "Released": "15 Jul 2011",
            "Runtime": "130 min",
            "Genre": "Adventure, Drama, Fantasy",
            "Director": "David Yates",
            "Writer": "Steve Kloves, J.K. Rowling",
            "Actors": "Daniel Radcliffe, Emma Watson, Rupert Grint",
            "Plot": "Harry, Ron, and Hermione search for Voldemort's remaining Horcruxes in their effort to destroy "
                    "the Dark Lord as the final battle rages on at Hogwarts.",
            "Language": "English",
            "Country": "United Kingdom, United States",
            "Awards": "Nominated for 3 Oscars. 46 wins & 94 nominations total",
            "Poster": "https://m.media-amazon.com/images/M/MV5BMGVmMWNiMDktYjQ0Mi00MWIxLTk0N2UtN2ZlYTdkN2IzNDNlXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_SX300.jpg",
            "Metascore": "85",
            "imdbRating": "8.1",
            "imdbVotes": "802,088",
            "imdbID": "tt1201607",
            "Type": "movie",
            "DVD": "11 Nov 2011",
            "BoxOffice": "$381,409,310",
            "Production": "N/A",
            "Website": "N/A",
            "Ratings": [
              {
                "Source": "Internet Movie Database",
                "Value": "8.1/10"
              },
              {
                "Source": "Rotten Tomatoes",
                "Value": "96%"
              },
            ]}
    serializer = MovieSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
    film_serializer_data = json.dumps(serializer.data)
    film_serializer_data = json.loads(film_serializer_data)
    # get response from the server
    response = self.client.get(reverse("movie-list"))
    response_data = json.loads(response.content)
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(Movie.objects.all().count(), 1)
    self.assertEqual([film_serializer_data], response_data)
  
  def test_filter_by_language(self):
    # add film 1
    serializer = MovieSerializer(data=
                                 {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                  'Runtime': '167 min',
                                  'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                  'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                  'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                  'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City "
                                          "seeking revenge against Bill the Butcher, his father's killer.",
                                  'Language': 'English, Irish Gaelic, Chinese, Latin',
                                  'Country': 'United States, Italy',
                                  'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
                                  'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
                                  'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                                              {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                                              {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
                                  'imdbRating': '7.5',
                                  'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
                                  'BoxOffice': '$77,812,000',
                                  'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
                                 )
    if serializer.is_valid():
      serializer.save()
    id_first_movie = serializer.data['id']
    film_serializer_data = json.dumps(serializer.data)
    film_serializer_data = json.loads(film_serializer_data)
    # add film 2
    serializer = MovieSerializer(data=
                                 {'Title': 'Gangs of New York 2', 'Year': '2002', 'Rated': 'R',
                                  'Released': '20 Dec 2002',
                                  'Runtime': '167 min',
                                  'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                  'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                  'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                  'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City "
                                          "seeking revenge against Bill the Butcher, his father's killer.",
                                  'Language': 'Irish Gaelic, Chinese, Latin', 'Country': 'United States, Italy',
                                  'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
                                  'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
                                  'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                                              {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                                              {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
                                  'imdbRating': '7.5',
                                  'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
                                  'BoxOffice': '$77,812,000',
                                  'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
                                 )
    if serializer.is_valid():
      serializer.save()
    
    # get response from the server
    response = self.client.get('/api/movie/?language=english')
    response_data = json.loads(response.content)
    
    # check if 2 films exist, but only 1 is displayed
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(Movie.objects.all().count(), 2)
    self.assertEqual([film_serializer_data], response_data)
    
    response_data_dict = (response_data[0])
    self.assertEqual(response_data_dict['id'], id_first_movie)
  
  def test_filter_by_genre(self):
    # add film 1
    serializer = MovieSerializer(data=
                                 {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                  'Runtime': '167 min',
                                  'Genre': 'Crime', 'Director': 'Martin Scorsese',
                                  'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                  'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                  'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City "
                                          "seeking revenge against Bill the Butcher, his father's killer.",
                                  'Language': 'English, Irish Gaelic, Chinese, Latin',
                                  'Country': 'United States, Italy',
                                  'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
                                  'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
                                  'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                                              {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                                              {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
                                  'imdbRating': '7.5',
                                  'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
                                  'BoxOffice': '$77,812,000',
                                  'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
                                 )
    if serializer.is_valid():
      serializer.save()
    id_first_movie = serializer.data['id']
    film_serializer_data = json.dumps(serializer.data)
    film_serializer_data = json.loads(film_serializer_data)
    # add film 2
    serializer = MovieSerializer(data=
                                 {'Title': 'Gangs of New York 2', 'Year': '2002', 'Rated': 'R',
                                  'Released': '20 Dec 2002',
                                  'Runtime': '167 min',
                                  'Genre': 'Drama', 'Director': 'Martin Scorsese',
                                  'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                  'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                  'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City "
                                          "seeking revenge against Bill the Butcher, his father's killer.",
                                  'Language': 'Irish Gaelic, Chinese, Latin', 'Country': 'United States, Italy',
                                  'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
                                  'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
                                  'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                                              {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                                              {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
                                  'imdbRating': '7.5',
                                  'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
                                  'BoxOffice': '$77,812,000',
                                  'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
                                 )
    if serializer.is_valid():
      serializer.save()
    id_second_movie = serializer.data['id']
    # get response from the server
    response = self.client.get('/api/movie/?genre=crime')
    response_data = json.loads(response.content)
    # check if 2 films exist, but only 1 is displayed
    self.assertEqual(200, response.status_code)
    self.assertEqual(Movie.objects.all().count(), 2)
    self.assertEqual([film_serializer_data], response_data)
    
    response_data_dict = (response_data[0])
    self.assertEqual(response_data_dict['id'], id_first_movie)
  
  def test_filter_by_country(self):
    # add film 1
    serializer = MovieSerializer(data=
                                 {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                  'Runtime': '167 min',
                                  'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                  'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                  'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                  'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City "
                                          "seeking revenge against Bill the Butcher, his father's killer.",
                                  'Language': 'English, Irish Gaelic, Chinese, Latin', 'Country': 'United States',
                                  'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
                                  'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
                                  'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                                              {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                                              {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
                                  'imdbRating': '7.5',
                                  'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
                                  'BoxOffice': '$77,812,000',
                                  'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
                                 )
    if serializer.is_valid():
      serializer.save()
    id_first_movie = serializer.data['id']
    film_serializer_data = json.dumps(serializer.data)
    film_serializer_data = json.loads(film_serializer_data)
    # add film 2
    serializer = MovieSerializer(data=
                                 {'Title': 'Gangs of New York 2', 'Year': '2002', 'Rated': 'R',
                                  'Released': '20 Dec 2002',
                                  'Runtime': '167 min',
                                  'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                  'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                  'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                  'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City "
                                          "seeking revenge against Bill the Butcher, his father's killer.",
                                  'Language': 'Irish Gaelic, Chinese, Latin', 'Country': 'Italy',
                                  'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
                                  'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
                                  'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                                              {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                                              {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
                                  'imdbRating': '7.5',
                                  'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
                                  'BoxOffice': '$77,812,000',
                                  'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
                                 )
    if serializer.is_valid():
      serializer.save()
    
    # get response from the server
    response = self.client.get('/api/movie/?country=united states')
    response_data = json.loads(response.content)
    # check if 2 films exist, but only 1 is displayed
    self.assertEqual(200, response.status_code)
    self.assertEqual(Movie.objects.all().count(), 2)
    self.assertEqual([film_serializer_data], response_data)
    
    response_data_dict = (response_data[0])
    self.assertEqual(response_data_dict['id'], id_first_movie)


class TestMoviesPost(APITestCase):
  
  def test_incorrect_data(self):
    client = APIClient()
    response = client.post(reverse("movie-list"), data={'not a dict': 'something'})
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'"Error, missing Title."')
  
  def test_no_title(self):
    client = APIClient()
    response = client.post(reverse("movie-list"), {'missingtitle': 'new idea'}, format='json')
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'"Error, missing Title."')
  
  @mock.patch('api.views.get_data_from_api', return_value={"Response": "False", "Error": "Movie not found!"})
  def test_incorrect_title(self, mock_api_data):
    client = APIClient()
    response = client.post(reverse("movie-list"), {'Title': 'notexistingtitle'}, format='json')
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'{"Response":"False","Error":"Movie not found!"}')
  
  @mock.patch('api.views.get_data_from_api', return_value=
  {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002', 'Runtime': '167 min',
   'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
   'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
   'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
   'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against "
           "Bill the Butcher, his father's killer.",
   'Language': 'English, Irish Gaelic, Chinese, Latin', 'Country': 'United States, Italy',
   'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
   'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
   'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'}, {'Source': 'Rotten Tomatoes', 'Value': '73%'},
               {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72', 'imdbRating': '7.5',
   'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003', 'BoxOffice': '$77,812,000',
   'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
              )
  def test_correct_title_film_does_not_exist_in_db(self, mock_api_data):
    client = APIClient()
    response = client.post(reverse("movie-list"), {'Title': 'Gangs of New York'}, format='json')
    
    self.assertEqual(201, response.status_code)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['Title'], 'Gangs of New York')
    self.assertEqual(response_data['Genre'], 'Crime, Drama')
    
    # check if the Film objects got created
    self.assertEqual(Movie.objects.all().count(), 1)
  
  @mock.patch('api.views.get_data_from_api', return_value=
  {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002', 'Runtime': '167 min',
   'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
   'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
   'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
   'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against "
           "Bill the Butcher, his father's killer.",
   'Language': 'English, Irish Gaelic, Chinese, Latin', 'Country': 'United States, Italy',
   'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
   'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
   'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'}, {'Source': 'Rotten Tomatoes', 'Value': '73%'},
               {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72', 'imdbRating': '7.5',
   'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003', 'BoxOffice': '$77,812,000',
   'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
              )
  def test_correct_title_film_exists_in_db(self, mock_api_data):
    serializer = MovieSerializer(data=
                                 {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                  'Runtime': '167 min',
                                  'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                  'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                  'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                  'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City "
                                          "seeking revenge against Bill the Butcher, his father's killer.",
                                  'Language': 'English, Irish Gaelic, Chinese, Latin',
                                  'Country': 'United States, Italy',
                                  'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
                                  'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
                                  'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                                              {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                                              {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
                                  'imdbRating': '7.5',
                                  'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
                                  'BoxOffice': '$77,812,000',
                                  'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
                                 )
    if serializer.is_valid():
      serializer.save()
    # check if the Film objects got created
    self.assertEqual(Movie.objects.all().count(), 1)
    client = APIClient()
    response = client.post(reverse("movie-list"), {'Title': 'Gangs of New York'}, format='json')
    
    self.assertEqual(201, response.status_code)
    
    response_data = json.loads(response.content)
    
    self.assertEqual(response_data['Title'], 'Gangs of New York')
    self.assertEqual(response_data['Genre'], 'Crime, Drama')
    
    # check if the is still only 1 Film object
    self.assertEqual(Movie.objects.all().count(), 1)


class TestPostComment(APITestCase):
  def test_incorrect_format(self):
    client = APIClient()
    response = client.post(reverse("comments-list"), data={'something': 'something'})
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'"Incorrect data, please add \\"author\\",\\"text\\",\\"film\\""')
  
  def test_missing_data(self):
    client = APIClient()
    response = client.post(reverse("comments-list"), {"author": "someone", "text": "something"}, format='json')
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'"Incorrect data, please add \\"author\\",\\"text\\",\\"film\\""')
  
  def test_film_does_not_exist(self):
    client = APIClient()
    response = client.post(reverse("comments-list"), {"author": "someone", "text": "something", "movie": 1},
                           format='json')
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'"Incorrect data, please add \\"author\\",\\"text\\",\\"film\\""')
  
  def test_film_exists(self):
    serializer = MovieSerializer(data=
                                 {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                  'Runtime': '167 min',
                                  'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                  'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                  'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                  'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City "
                                          "seeking revenge against Bill the Butcher, his father's killer.",
                                  'Language': 'English, Irish Gaelic, Chinese, Latin',
                                  'Country': 'United States, Italy',
                                  'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
                                  'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
                                  'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                                              {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                                              {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
                                  'imdbRating': '7.5',
                                  'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
                                  'BoxOffice': '$77,812,000',
                                  'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
                                 )
    if serializer.is_valid():
      serializer.save()
    # check if the Film objects got created
    self.assertEqual(Movie.objects.all().count(), 1)
    
    client = APIClient()
    response = client.post(reverse("comments-list"), {"author": "someone", "text": "something", "movie": 1},
                           format='json')
    response_data = json.loads(response.content)
    self.assertEqual(201, response.status_code)
    self.assertEqual(response.content, b'{"id":1,"text":"something","author":"someone","movie":1}')
    self.assertEqual(response_data['text'], 'something')
    self.assertEqual(response_data['author'], 'someone')
    self.assertEqual(response_data['movie'], 1)


class TestCommentList(APITestCase):
  def test_get_no_comments(self):
    response = self.client.get(reverse("comments-list"))
    self.assertEqual(200, response.status_code)
    
    response_data = json.loads(response.content)
    self.assertEqual([], response_data)
  
  def test_get_comments(self):
    
    serializer = MovieSerializer(data=
                                 {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                  'Runtime': '167 min',
                                  'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                  'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                  'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                  'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City "
                                          "seeking revenge against Bill the Butcher, his father's killer.",
                                  'Language': 'English, Irish Gaelic, Chinese, Latin',
                                  'Country': 'United States, Italy',
                                  'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
                                  'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
                                  'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                                              {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                                              {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
                                  'imdbRating': '7.5',
                                  'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
                                  'BoxOffice': '$77,812,000',
                                  'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
                                 )
    if serializer.is_valid():
      serializer.save()
    movie = Movie.objects.get()
    
    comment = Comment.objects.create(author='somebody', movie=movie, text='something')
    
    response = self.client.get(reverse("comments-list"))
    self.assertEqual(200, response.status_code)
    
    response_data = json.loads(response.content)
    self.assertEqual([response_data[0]],
                     [{'id': comment.pk, 'text': 'something', 'author': 'somebody', 'movie': movie.pk}])
  
  def test_filtering(self):
    # add film 1
    serializer = MovieSerializer(data=
                                 {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                  'Runtime': '167 min',
                                  'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                  'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                  'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                  'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City "
                                          "seeking revenge against Bill the Butcher, his father's killer.",
                                  'Language': 'English, Irish Gaelic, Chinese, Latin',
                                  'Country': 'United States, Italy',
                                  'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
                                  'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
                                  'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                                              {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                                              {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
                                  'imdbRating': '7.5',
                                  'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
                                  'BoxOffice': '$77,812,000',
                                  'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
                                 )
    if serializer.is_valid():
      serializer.save()
    id_first_movie = serializer.data['id']
    # add film 2
    serializer = MovieSerializer(data=
                                 {'Title': 'Gangs of New York 2', 'Year': '2002', 'Rated': 'R',
                                  'Released': '20 Dec 2002',
                                  'Runtime': '167 min',
                                  'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                  'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                  'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                  'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City "
                                          "seeking revenge against Bill the Butcher, his father's killer.",
                                  'Language': 'English, Irish Gaelic, Chinese, Latin',
                                  'Country': 'United States, Italy',
                                  'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
                                  'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
                                  'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                                              {'Source': 'Rotten Tomatoes', 'Value': '73%'},
                                              {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72',
                                  'imdbRating': '7.5',
                                  'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003',
                                  'BoxOffice': '$77,812,000',
                                  'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
                                 )
    if serializer.is_valid():
      serializer.save()
    id_second_movie = serializer.data['id']
    # create 2 comment for dif. films
    film1 = Movie.objects.get(id=id_first_movie)
    comment1 = Comment.objects.create(author='somebody', movie=film1, text='something')
    
    film2 = Movie.objects.get(id=id_second_movie)
    comment2 = Comment.objects.create(author='somebody2', movie=film2, text='something2')
    url = "/api/comments/?movie=" + str(serializer.data['id'])
    response = self.client.get(url)
    self.assertEqual(200, response.status_code)
    
    response_data = json.loads(response.content)
    self.assertEqual([response_data[0]],
                     [{'id': comment2.pk, 'text': 'something2', 'author': 'somebody2', 'movie': id_second_movie}])
