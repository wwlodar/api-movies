from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Movie
from .serializers import MovieSerializer, CommentSerializer
import json
from rest_framework import generics
from .models import Comment
import io
from .filters import MoviesFilter
from .utils import get_data_from_api
from rest_framework import viewsets
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .renderers import CustomBrowsableAPIRenderer


class ApiOverviewSet(viewsets.ReadOnlyModelViewSet):
  
  def list(self, request):
    api_urls = {
      'Get or post a movie': 'movie/',
      'Get or post a comment': 'comment/',
    }
    return Response(api_urls)


class MovieViewSet(viewsets.GenericViewSet):
  queryset = Movie.objects.all()
  serializer_class = MovieSerializer
  filter_class = MoviesFilter
  renderer_classes = (JSONRenderer, CustomBrowsableAPIRenderer, TemplateHTMLRenderer)
  
  def list(self, request):
    assets = self.filter_queryset(self.get_queryset())
    serializer = MovieSerializer(assets, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    if 'Title' in request.data:
      title = request.data.get('Title')
      data_from_api = get_data_from_api(title=title)
      if data_from_api['Response'] == 'False':
        return Response(data_from_api)
      else:
        serializer = MovieSerializer(data=data_from_api)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response('Error, missing Title.')
  
  def perform_create(self, serializer):
    serializer.save()


# @api_view(['POST'])
# def post_movie_details(request):
#   try:
#     post_body = json.loads(request.body)
#     if 'title' in post_body:
#       title = post_body.get('title')
#
#       data_from_api = get_data_from_api(title=title)
#       if data_from_api['Response'] == 'False':
#         return Response(data_from_api)
#       else:
#         # check if this film is already in database
#         try:
#           data = Movie.objects.get(Title=data_from_api['Title'])
#           serializer = MovieSerializer(data)
#           return Response(serializer.data)
#         # create new Film object
#         except:
#           serializer = MovieSerializer(data=data_from_api)
#           if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#           return Response(serializer.errors)
#     else:
#       return Response("Incorrect format, please add 'title'")
#   except:
#     return Response("Incorrect format.")
#

# class FilmList(generics.ListAPIView):
#   queryset = Movie.objects.all()
#   serializer_class = MovieSerializer
#   filterset_class = MoviesFilter

class CommentViewSet(viewsets.GenericViewSet):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  
  def list(self, request):
    assets = self.filter_queryset(self.get_queryset())
    serializer = CommentSerializer(assets, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    required_fields = ["author", "text", "movie"]
    print(request.data)
    if all(key in request.data for key in required_fields):
      author = request.data.get('author')
      text = request.data.get('text')
      movie_id = request.data.get('movie')
      
      movie = Movie.objects.filter(id=movie_id)
      if movie.exists():
        movie = Movie.objects.get(id=movie_id)
        comment = Comment.objects.create(movie=movie, text=text, author=author)
        serializer = CommentSerializer(comment)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      else:
        return Response('Incorrect data, please add "author","text","film"')
    else:
      return Response('Incorrect data, please add "author","text","film"')


# @csrf_exempt
# @api_view(['POST'])
# def post_comment(request):
#   # taking data from request
#   try:
#     post_body = json.loads(request.body)
#     print(post_body)
#     things = ["author", "text", "film_id"]
#     if all(key in post_body for key in things):
#       print('film_id')
#       author = post_body.get('author')
#       text = post_body.get('text')
#       film_id = post_body.get('film_id')
#
#       film = Movie.objects.filter(id=film_id)
#
#       if film.exists():
#         film = Movie.objects.get(id=film_id)
#         comment = Comment.objects.create(film=film, text=text, author=author)
#         serializer = CommentSerializer(comment)
#
#         # deserializing data
#         json1 = JSONRenderer().render(serializer.data)
#         stream = io.BytesIO(json1)
#         data = JSONParser().parse(stream)
#         serializer = CommentSerializer(data=data)
#
#         if serializer.is_valid():
#           serializer.save()
#           return Response(serializer.data)
#         return Response(serializer.errors)
#       else:
#         return Response('Film with this id does not exist.')
#     else:
#       return Response('Incorrect data, please add "author","text","film_id"')
#   except:
#     return Response("Incorrect format.")


class CommentList(generics.ListAPIView):
  serializer_class = CommentSerializer
  
  # filtering by film_id
  def get_queryset(self):
    queryset = Comment.objects.all()
    film_id = self.request.query_params.get('film_id')
    if film_id is not None:
      queryset = queryset.filter(film=Movie.objects.get(id=film_id))
    return queryset
