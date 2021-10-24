from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Film
from django.http import HttpResponse, JsonResponse
from .serializers import FilmSerializer, CommentSerializer
import json
from django.core import serializers
from rest_framework import generics
from .models import Comment
import io
from rest_framework.renderers import JSONRenderer
from .filters import LanguagesFilter

api_key = 'f25de7ad'


@api_view(['GET'])
def api_overview(request):
  api_urls = {
    'Detail view of movie': 'movies/post',
    'Get all movies from database': 'movies/get',
    'Get all comments': 'get/comments/',
    'Add comment to movie ID': 'comment/post',
  }
  return Response(api_urls)


def get_data_from_api(title):
  url = "https://www.omdbapi.com/" + "?t=" + title + "&apikey=" + api_key
  r = requests.get(url)
  data = r.json()
  return data


@api_view(['POST'])
def post_movie_details(request):
  try:
    post_body = json.loads(request.body)
    
    if 'title' in post_body:
      title = post_body.get('title')
      
      data_from_api = get_data_from_api(title=title)
      if data_from_api['Response'] == 'False':
        return Response(data_from_api)
      else:
        # check if this film is already in database
        try:
          data = Film.objects.get(Title=data_from_api['Title'])
          serializer = FilmSerializer(data)
          return Response(serializer.data)
        # create new Film object
        except:
          serializer = FilmSerializer(data=data_from_api)
          if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
          return Response(serializer.errors)
    else:
      return Response("Incorrect format, please add 'title'")
  except:
    return Response("Incorrect format.")


class FilmList(generics.ListAPIView):
  queryset = Film.objects.all()
  serializer_class = FilmSerializer
  filterset_class = LanguagesFilter


@csrf_exempt
@api_view(['POST'])
def post_comment(request):
  # taking data from request
  try:
    post_body = json.loads(request.body)
    print(post_body)
    things = ["author", "text", "film_id"]
    if all(key in post_body for key in things):
      print('film_id')
      author = post_body.get('author')
      text = post_body.get('text')
      film_id = post_body.get('film_id')
      
      film = Film.objects.filter(id=film_id)
      
      if film.exists():
        film = Film.objects.get(id=film_id)
        comment = Comment.objects.create(film=film, text=text, author=author)
        serializer = CommentSerializer(comment)

        # deserializing data
        json1 = JSONRenderer().render(serializer.data)
        stream = io.BytesIO(json1)
        data = JSONParser().parse(stream)
        serializer = CommentSerializer(data=data)

        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
        return Response(serializer.errors)
      else:
        return Response('Film with this id does not exist.')
    else:
      return Response('Incorrect data, please add "author","text","film_id"')
  except:
    return Response("Incorrect format.")


class CommentList(generics.ListAPIView):
  serializer_class = CommentSerializer
  
  # filtering by language
  def get_queryset(self):
    queryset = Comment.objects.all()
    film_id = self.request.query_params.get('film_id')
    if film_id is not None:
      queryset = queryset.filter(film=Film.objects.get(id=film_id))
    return queryset
