from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Post, Like, Comment, Follow, Media
from .serializers import (
    UserSerializer, PostSerializer, LikeSerializer, 
    CommentSerializer, MediaSerializer
)

User = get_user_model()

# 1. ТІРКЕЛУ (Кез келген қолданушы үшін)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # Тіркелуге бәріне рұқсат

# 2. ПОСТТАР (Көру және Жасау)
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Постты жасағанда оның авторын автоматты түрде қазіргі юзер қылып бекіту
        serializer.save(author=self.request.user)

# 3. ЛАЙК БАСУ/АЛЫП ТАСТАУ (Like Toggle)
class LikeToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like_queryset = Like.objects.filter(user=request.user, post=post)
        
        if like_queryset.exists():
            like_queryset.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)
        
        Like.objects.create(user=request.user, post=post)
        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)

# 4. КОММЕНТАРИЙЛЕР
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# 5. ЖАЗЫЛУ (Follow/Unfollow)
class FollowToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        if request.user == user_to_follow:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        
        follow_obj = Follow.objects.filter(follower=request.user, following=user_to_follow)
        
        if follow_obj.exists():
            follow_obj.delete()
            return Response({"message": "Unfollowed"}, status=status.HTTP_200_OK)
            
        Follow.objects.create(follower=request.user, following=user_to_follow)
        return Response({"message": "Followed"}, status=status.HTTP_201_CREATED)