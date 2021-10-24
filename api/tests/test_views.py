from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse
import json
from ..serializers import *
from ..views import *
from rest_framework.renderers import JSONRenderer
import io
from rest_framework.parsers import JSONParser
from rest_framework.test import APIClient
import mock
from mock import patch


class TestAPIOverview(APITestCase):
  def test_get(self):
    response = self.client.get(reverse("api_overview"))
    self.assertEqual(200, response.status_code)
    
    response_data = json.loads(response.content)
    self.assertEqual({
      'Detail view of movie': 'movies/post',
      'Get all movies from database': 'movies/get',
      'Get all comments': 'get/comments/',
      'Add comment to movie ID': 'comment/post',
    }, response_data)


class TestGetDataFromApi(APITestCase):
  
  def test_correct(self):
    get_mock = mock.MagicMock()
    get_mock.status_code = 200
    data = {"Title": "Harry Potter and the Deathly Hallows: Part 2",
            "Year": "2011",
            "Rated": "PG-13",
            "Released": "15 Jul 2011"}
    get_mock.json.return_value = data
    mock.seal(get_mock)
    with mock.patch.object(requests, 'get', return_value=get_mock):
      response = get_data_from_api(title="Harry Potter and the Deathly Hallows: Part 2")
    
    self.assertEqual(response, data)


class TestGetMovies(APITestCase):
  def test_get_no_movies(self):
    response = self.client.get(reverse("get_all_films"))
    self.assertEqual(200, response.status_code)
    
    response_data = json.loads(response.content)
    self.assertEqual({'count': 0, 'next': None, 'previous': None, 'results': []}, response_data)
  
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
            "Plot": "Harry, Ron, and Hermione search for Voldemort's remaining Horcruxes in their effort to destroy the Dark Lord as the final battle rages on at Hogwarts.",
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
    serializer = FilmSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
    film_serializer_data = json.dumps(serializer.data)
    film_serializer_data = json.loads(film_serializer_data)
    # get response from the server
    response = self.client.get(reverse("get_all_films"))
    response_data = json.loads(response.content)
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(Film.objects.all().count(), 1)
    self.assertEqual([film_serializer_data], response_data['results'])
    
  def test_filter_by_language(self):
    # add film 1
    serializer = FilmSerializer(data=
                                {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                 'Runtime': '167 min',
                                 'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                 'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                 'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                 'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against Bill the Butcher, his father's killer.",
                                 'Language': 'English, Irish Gaelic, Chinese, Latin', 'Country': 'United States, Italy',
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
      
    film_serializer_data = json.dumps(serializer.data)
    film_serializer_data = json.loads(film_serializer_data)
    # add film 2
    serializer = FilmSerializer(data=
                                {'Title': 'Gangs of New York 2', 'Year': '2002', 'Rated': 'R',
                                 'Released': '20 Dec 2002',
                                 'Runtime': '167 min',
                                 'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                 'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                 'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                 'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against Bill the Butcher, his father's killer.",
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
    response = self.client.get('/api/movies/get?language=english')
    response_data = json.loads(response.content)
    # check if 2 films exist, but only 1 is displayed
    self.assertEqual(200, response.status_code)
    self.assertEqual(Film.objects.all().count(), 2)
    self.assertEqual(response_data['count'], 1)
    self.assertEqual(response_data['results'], [film_serializer_data])


class TestMoviesPost(APITestCase):
  
  def test_incorrect_data(self):
    client = APIClient()
    response = client.post(reverse("post_movie_details"), data={'not a dict': 'something'})
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'"Incorrect format."')
  
  def test_no_title(self):
    client = APIClient()
    response = client.post(reverse("post_movie_details"), {'missingtitle': 'new idea'}, format='json')
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'"Incorrect format, please add \'title\'"')
  
  @mock.patch('api.views.get_data_from_api', return_value={"Response": "False", "Error": "Movie not found!"})
  def test_incorrect_title(self, mock_api_data):
    client = APIClient()
    response = client.post(reverse("post_movie_details"), {'title': 'notexistingtitle'}, format='json')
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'{"Response":"False","Error":"Movie not found!"}')
  
  @mock.patch('api.views.get_data_from_api', return_value=
  {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002', 'Runtime': '167 min',
   'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
   'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
   'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
   'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against Bill the Butcher, his father's killer.",
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
    response = client.post(reverse("post_movie_details"), {'title': 'Gangs of New York'}, format='json')
    
    self.assertEqual(200, response.status_code)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['Title'], 'Gangs of New York')
    self.assertEqual(response_data['Genre'], 'Crime, Drama')
    
    # check if the Film objects got created
    self.assertEqual(Film.objects.all().count(), 1)
  
  @mock.patch('api.views.get_data_from_api', return_value=
  {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002', 'Runtime': '167 min',
   'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
   'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
   'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
   'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against Bill the Butcher, his father's killer.",
   'Language': 'English, Irish Gaelic, Chinese, Latin', 'Country': 'United States, Italy',
   'Awards': 'Nominated for 10 Oscars. 50 wins & 135 nominations total',
   'Poster': 'https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg',
   'Ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'}, {'Source': 'Rotten Tomatoes', 'Value': '73%'},
               {'Source': 'Metacritic', 'Value': '72/100'}], 'Metascore': '72', 'imdbRating': '7.5',
   'imdbVotes': '420,167', 'imdbID': 'tt0217505', 'Type': 'movie', 'DVD': '01 Jul 2003', 'BoxOffice': '$77,812,000',
   'Production': 'N/A', 'Website': 'N/A', 'Response': 'True'}
              )
  def test_correct_title_film_exists_in_db(self, mock_api_data):
    serializer = FilmSerializer(data=
                                {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                 'Runtime': '167 min',
                                 'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                 'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                 'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                 'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against Bill the Butcher, his father's killer.",
                                 'Language': 'English, Irish Gaelic, Chinese, Latin', 'Country': 'United States, Italy',
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
    self.assertEqual(Film.objects.all().count(), 1)
    client = APIClient()
    response = client.post(reverse("post_movie_details"), {'title': 'Gangs of New York'}, format='json')
    
    self.assertEqual(200, response.status_code)
    
    response_data = json.loads(response.content)
    
    self.assertEqual(response_data['Title'], 'Gangs of New York')
    self.assertEqual(response_data['Genre'], 'Crime, Drama')
    
    # check if the is still only 1 Film object
    self.assertEqual(Film.objects.all().count(), 1)


class TestPostComment(APITestCase):
  def test_incorrect_format(self):
    client = APIClient()
    response = client.post(reverse("post_comment"), data={'something': 'something'})
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'"Incorrect format."')
  
  def test_missing_data(self):
    client = APIClient()
    response = client.post(reverse("post_comment"), {"author": "someone", "text": "something"}, format='json')
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'"Incorrect data, please add \\"author\\",\\"text\\",\\"film_id\\""')
  
  def test_film_does_not_exist(self):
    client = APIClient()
    response = client.post(reverse("post_comment"), {"author": "someone", "text": "something", "film_id": 1},
                           format='json')
    
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'"Film with this id does not exist."')
  
  def test_film_exists(self):
    serializer = FilmSerializer(data=
                                {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                 'Runtime': '167 min',
                                 'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                 'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                 'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                 'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against Bill the Butcher, his father's killer.",
                                 'Language': 'English, Irish Gaelic, Chinese, Latin', 'Country': 'United States, Italy',
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
    self.assertEqual(Film.objects.all().count(), 1)
    print(Film.objects.all())
    
    client = APIClient()
    response = client.post(reverse("post_comment"), {"author": "someone", "text": "something", "film_id": 1},
                           format='json')
    response_data = json.loads(response.content)
    self.assertEqual(200, response.status_code)
    self.assertEqual(response.content, b'{"id":2,"text":"something","author":"someone","film":1}')
    self.assertEqual(response_data['text'], 'something')
    self.assertEqual(response_data['author'], 'someone')
    self.assertEqual(response_data['film'], 1)


class TestCommentList(APITestCase):
  def test_get_no_comments(self):
    response = self.client.get(reverse("get_all_comments"))
    self.assertEqual(200, response.status_code)
    
    response_data = json.loads(response.content)
    self.assertEqual({'count': 0, 'next': None, 'previous': None, 'results': []}, response_data)
  
  def test_get_comments(self):
    
    serializer = FilmSerializer(data=
                                {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                 'Runtime': '167 min',
                                 'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                 'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                 'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                 'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against Bill the Butcher, his father's killer.",
                                 'Language': 'English, Irish Gaelic, Chinese, Latin', 'Country': 'United States, Italy',
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
    film = Film.objects.get()
    
    comment = Comment.objects.create(author='somebody', film=film, text='something')
    
    response = self.client.get(reverse("get_all_comments"))
    self.assertEqual(200, response.status_code)
    
    response_data = json.loads(response.content)
    self.assertEqual(response_data['count'], 1)
    self.assertEqual(response_data['results'], [{'id': 1, 'text': 'something', 'author': 'somebody', 'film': 1}])
  
  def test_filtering(self):
    # add film 1
    serializer = FilmSerializer(data=
                                {'Title': 'Gangs of New York', 'Year': '2002', 'Rated': 'R', 'Released': '20 Dec 2002',
                                 'Runtime': '167 min',
                                 'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                 'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                 'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                 'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against Bill the Butcher, his father's killer.",
                                 'Language': 'English, Irish Gaelic, Chinese, Latin', 'Country': 'United States, Italy',
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
    # add film 2
    serializer = FilmSerializer(data=
                                {'Title': 'Gangs of New York 2', 'Year': '2002', 'Rated': 'R',
                                 'Released': '20 Dec 2002',
                                 'Runtime': '167 min',
                                 'Genre': 'Crime, Drama', 'Director': 'Martin Scorsese',
                                 'Writer': 'Jay Cocks, Steven Zaillian, Kenneth Lonergan',
                                 'Actors': 'Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis',
                                 'Plot': "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against Bill the Butcher, his father's killer.",
                                 'Language': 'English, Irish Gaelic, Chinese, Latin', 'Country': 'United States, Italy',
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
    
    # create 2 comment for dif. films
    film1 = Film.objects.get(id=1)
    comment1 = Comment.objects.create(author='somebody', film=film1, text='something')
    
    film2 = Film.objects.get(id=2)
    comment2 = Comment.objects.create(author='somebody', film=film2, text='something')
    
    response = self.client.get("/api/comment/get?film_id=2")
    self.assertEqual(200, response.status_code)
    
    response_data = json.loads(response.content)
    self.assertEqual(response_data['count'], 1)
    self.assertEqual(response_data['results'], [{'id': 2, 'text': 'something', 'author': 'somebody', 'film': 2}])
