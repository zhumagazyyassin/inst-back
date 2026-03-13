from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Like
from .serializers import LikeSerializer

class LikeToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    # 1. ОСЫ ГЕТ ПОСТТЫҢ ЛАЙКТАРЫН КӨРУГЕ МҮМКІНДІК БЕРЕДІ
    def get(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        likes = Like.objects.filter(post=post)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    # 2. ОСЫ ПОСТ ЛАЙК БАСУҒА НЕМЕСЕ ҚАЙТАРУҒА АРНАЛҒАН
    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like_queryset = Like.objects.filter(user=request.user, post=post)
        
        if like_queryset.exists():
            like_queryset.delete()
            return Response({"message": "Unliked", "is_liked": False}, status=status.HTTP_200_OK)
        else:
            Like.objects.create(user=request.user, post=post)
            return Response({"message": "Liked", "is_liked": True}, status=status.HTTP_201_CREATED)