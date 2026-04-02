from rest_framework import serializers
from .models import User, Post, Media, Comment, Like, Follow, Story, Note

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'bio', 'avatar_url', 'followers_count', 'following_count']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class StorySerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Story
        fields = ['id', 'author', 'author_name', 'file', 'created_at', 'expires_at']
        read_only_fields = ['author', 'created_at']

class NoteSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Note
        fields = ['id', 'author', 'author_name', 'text', 'created_at']
        read_only_fields = ['author', 'created_at']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file', 'file_type']

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'text', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Like
        fields = ['id', 'user', 'username', 'post']

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.ReadOnlyField(source='author.id') 
    likes_count = serializers.SerializerMethodField()
    media = MediaSerializer(many=True, read_only=True)
    
    # СУРЕТТІ ҚАБЫЛДАУ ҮШІН:
    image = serializers.ImageField(write_only=True, required=False)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'caption', 'image', 'media', 'likes_count', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count() if hasattr(obj, 'likes') else 0