import requests
import os

api_key = os.environ['API_KEY_OMDB_API']


def get_data_from_api(title):
  url = "https://www.omdbapi.com/" + "?t=" + title + "&apikey=" + api_key
  r = requests.get(url)
  data = r.json()
  return data
