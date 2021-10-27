from .renderers import CustomBrowsableAPIRenderer
from .models import Movie
from .serializers import MovieSerializer, CommentSerializer
from .models import Comment
from .filters import MoviesFilter
from .utils import get_data_from_api

from rest_framework import viewsets
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response


class ApiOverviewSet(viewsets.ReadOnlyModelViewSet):
  
  def list(self, request):
    api_urls = {
      'Get or post a movie': 'api/movie/',
      'Get or post a comment': 'api/comments/',
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


class CommentViewSet(viewsets.GenericViewSet):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  filter_fields = ('movie',)
  
  def list(self, request):
    assets = self.filter_queryset(self.get_queryset())
    serializer = CommentSerializer(assets, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    required_fields = ["author", "text", "movie"]
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
