from django.urls import path
from . import views
from .views import  CommentList
from .views import MovieViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movie', MovieViewSet, basename='movie')
router.register(r"comment", CommentViewSet, basename="comment")
urlpatterns = router.urls


# urlpatterns = [
#   path('', views.api_overview, name='api_overview'),
#   path('movies/post', views.post_movie_details, name='post_movie_details'),
#   path('movies/get', FilmList.as_view(), name='get_all_films'),
#   path('comment/post', views.post_comment, name='post_comment'),
#   path('comment/get', CommentList.as_view(), name='get_all_comments'),
# ]
