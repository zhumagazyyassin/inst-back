from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import connection
from django.http import JsonResponse

# Өз жобаңдағы файлдардан импорттау
from .permissions import IsAuthorOrReadOnly 
from .models import Post, Like, Comment, Follow, Media, Story, Note
from .serializers import (
    UserSerializer, PostSerializer, LikeSerializer, 
    CommentSerializer, MediaSerializer, StorySerializer, NoteSerializer
)

User = get_user_model()

# --- БАЗАНЫ ТЕКСЕРУ (HEALTH CHECK) ---
def check_db(request):
    try:
        with connection.cursor() as cursor:
            # Базадағы барлық кестелердің тізімін алу
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = [row[0] for row in cursor.fetchall()]
        return JsonResponse({
            "status": "Connected", 
            "database": connection.settings_dict['NAME'],
            "tables_found": tables
        })
    except Exception as e:
        return JsonResponse({"status": "Error", "message": str(e)})

# 1. ТІРКЕЛУ
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# 2. ПАЙДАЛАНУШЫЛАР
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# 3. СТОРИЗ
class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer
    permission_classes = [AllowAny] 

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else User.objects.first()
        serializer.save(author=user)

# 4. ПОСТТАР (Суретті автоматты Media кестесіне сақтаумен)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [AllowAny] 

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else User.objects.first()
        post = serializer.save(author=user)
        
        # Postman-нан келген суретті Media кестесіне жіберу
        image_data = self.request.FILES.get('image') or self.request.FILES.get('file')
        if image_data:
            Media.objects.create(post=post, file=image_data, file_type='image')

# 5. ЗАМЕТКАЛАР
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else User.objects.first()
        serializer.save(author=user)

# 6. МЕДИА
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [AllowAny]

# 7. ПІКІРЛЕР
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else User.objects.first()
        serializer.save(author=user)

# 8. ЛАЙК ЖӘНЕ 9. ЖАЗЫЛУ (Өзгеріссіз қалды)
class LikeToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)
        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)

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