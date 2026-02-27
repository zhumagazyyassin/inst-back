from rest_framework import serializers
from .models import User, Post, Media, Comment, Follow, Like

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar_url']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'post', 'file', 'url', 'mime_type', 'order_idx', 'caption']
        # Эти строки заставят Django игнорировать отсутствие URL и MIME_TYPE
        extra_kwargs = {
            'post': {'required': False},
            'url': {'required': False, 'allow_null': True},
            'mime_type': {'required': False, 'allow_null': True},
        }

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_at']
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    # 'media' өрісі MediaSerializer арқылы файлдардың толық мәліметін (URL-ін) шығарады
    media = MediaSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'media', 'comments_count', 'likes_count', 'created_at']