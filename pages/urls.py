from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, UserViewSet, PostViewSet, 
    CommentViewSet, LikeToggleView, FollowToggleView,
    MediaViewSet, StoryViewSet, NoteViewSet  # Жаңа ViewSet-тер қосылды
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'media', MediaViewSet)
router.register(r'stories', StoryViewSet) # Сториз үшін маршрут
router.register(r'notes', NoteViewSet)       # Заметкалар үшін маршрут

urlpatterns = [
    # Router арқылы тіркелген барлық GET, POST, PUT, DELETE жолдары
    path('', include(router.urls)),
    
    # Бөлек GenericAPIView арқылы жасалған логикалар
    path('register/', RegisterView.as_view(), name='register'),
    path('posts/<int:pk>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('users/<int:user_id>/follow/', FollowToggleView.as_view(), name='follow-toggle'),
]