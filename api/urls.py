from .views import MovieViewSet, CommentViewSet, ApiOverviewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movie', MovieViewSet, basename='movie')
router.register(r"comments", CommentViewSet, basename="comments")
router.register(r'', ApiOverviewSet, basename='api_overview')
urlpatterns = router.urls
