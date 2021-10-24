from django.urls import path
from . import views
from .views import FilmList, CommentList

urlpatterns = [
  path('', views.api_overview, name='api_overview'),
  path('movies/post', views.post_movie_details, name='post_movie_details'),
  path('movies/get', FilmList.as_view(), name='get_all_films'),
  path('comment/post', views.post_comment, name='post_comment'),
  path('comment/get', CommentList.as_view(), name='get_all_comments'),
]
