from django.urls import path
from .views import PostListCreateView, LikeToggleView

urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/like/', LikeToggleView.as_view()),
]