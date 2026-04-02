from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

# Өз жобаңдағы файлдардан импорттау (папка аттарын тексер)
from .permissions import IsAuthorOrReadOnly 
from .models import Post, Like, Comment, Follow, Media, Story, Note
from .serializers import (
    UserSerializer, PostSerializer, LikeSerializer, 
    CommentSerializer, MediaSerializer, StorySerializer, NoteSerializer
)

User = get_user_model()

# 1. ТІРКЕЛУ (Барлығына ашық)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# 2. ПАЙДАЛАНУШЫЛАРМЕН ЖҰМЫС
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        refresh = RefreshToken.for_user(instance)
        return Response({
            "message": "User updated successfully",
            "user": serializer.data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

# 3. СТОРИЗБЕН ЖҰМЫС (GET барлығына ашық, POST тек логинмен)
class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer
    # Эмуляторда деректерді көру үшін AllowAny уақытша қойылды
    permission_classes = [AllowAny] 
    http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer):
        # Пост салғанда авторды автоматты түрде тіркеу
        serializer.save(author=self.request.user)

# 4. ПОСТТАРМЕН ЖҰМЫС (Android эмуляторы үшін негізгі бөлім)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    # Android-та бірден көрінуі үшін AllowAny қалдырамыз
    permission_classes = [AllowAny] 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# 5. ЗАМЕТКАМЕН ЖҰМЫС
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# 6. МЕДИА ФАЙЛДАРМЕН ЖҰМЫС
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'delete']

# 7. ПІКІРЛЕРМЕН ЖҰМЫС
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# 8. ЛАЙК БАСУ (Тек тіркелгендерге)
class LikeToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)
        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)

# 9. ЖАЗЫЛУ (FOLLOW)
class FollowToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
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