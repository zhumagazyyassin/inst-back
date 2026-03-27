from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Post, Like, Comment, Follow, Media
from .serializers import (
    UserSerializer, PostSerializer, LikeSerializer, 
    CommentSerializer, MediaSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Токен иесін автор ретінде автоматты түрде сақтайды
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_404(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)
        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)

class FollowToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        follow_obj = Follow.objects.filter(follower=request.user, following=user_to_follow)
        if follow_obj.exists():
            follow_obj.delete()
            return Response({"message": "Unfollowed"}, status=status.HTTP_200_OK)
        Follow.objects.create(follower=request.user, following=user_to_follow)
        return Response({"message": "Followed"}, status=status.HTTP_201_CREATED)