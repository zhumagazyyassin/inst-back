from django.urls import path
from .views import (
    PostListCreateView, LikeListView, LikeToggleView, FollowListCreateView
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/like/', LikeToggleView.as_view()),
    path('likes/', LikeListView.as_view()), # Міне, сен сұраған лайктар ГЕТ-і
    path('follows/', FollowListCreateView.as_view()),
]