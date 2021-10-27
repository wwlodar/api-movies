from .views import MovieViewSet, CommentViewSet, ApiOverviewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'movie', MovieViewSet, basename='movie')
router.register(r"comments", CommentViewSet, basename="comments")
router.register(r'', ApiOverviewSet, basename='api_overview')
urlpatterns = router.urls


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)