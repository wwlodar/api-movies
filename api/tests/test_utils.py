from ..utils import get_data_from_api
from django.test import TestCase
from unittest.mock import patch

data = {"Title": "Gangs of New York", "Year": "2002", "Rated": "R", "Released": "20 Dec 2002", "Runtime": "167 min",
        "Genre": "Crime, Drama", "Director": "Martin Scorsese",
        "Writer": "Jay Cocks, Steven Zaillian, Kenneth Lonergan",
        "Actors": "Leonardo DiCaprio, Cameron Diaz, Daniel Day-Lewis",
        "Plot": "In 1862, Amsterdam Vallon returns to the Five Points area of New York City seeking revenge against Bill the Butcher, his father's killer.",
        "Language": "English, Irish Gaelic, Chinese, Latin", "Country": "United States, Italy",
        "Awards": "Nominated for 10 Oscars. 50 wins & 135 nominations total",
        "Poster": "https://m.media-amazon.com/images/M/MV5BNDg3MmI1ZDYtMDZjYi00ZWRlLTk4NzEtZjY4Y2U0NjE5YmRiXkEyXkFqcGdeQXVyNzAxMjE1NDg@._V1_SX300.jpg",
        "Ratings": [{"Source": "Internet Movie Database", "Value": "7.5/10"},
                    {"Source": "Rotten Tomatoes", "Value": "73%"},
                    {"Source": "Metacritic", "Value": "72/100"}], "Metascore": "72", "imdbRating": "7.5",
        "imdbVotes": "421,762", "imdbID": "tt0217505", "Type": "movie", "DVD": "01 Jul 2003",
        "BoxOffice": "$77,812,000",
        "Production": "N/A", "Website": "N/A", "Response": "True"}


class MockResponseSuccess:
  
  def __init__(self):
    self.status_code = 200
  
  def json(self):
    return data


class MockResponseFail:
  
  def __init__(self):
    self.status_code = 404
  
  def json(self):
    return {"Response": "False", "Error": "Movie not found!"}


class TestGetDataFromApi(TestCase):
  @patch("requests.get", return_value=MockResponseSuccess())
  def test_get_correct_name(self, mock_result):
    title = 'Gangs of New York'
    result = get_data_from_api(title=title)
    self.assertEqual(result, data)
  
  @patch("requests.get", return_value=MockResponseFail())
  def test_get_incorrect_name(self, mock_result):
    title = 'Gang of New York'
    result = get_data_from_api(title=title)
    self.assertEqual(result, {"Response": "False", "Error": "Movie not found!"})
