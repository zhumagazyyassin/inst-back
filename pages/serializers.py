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

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# --- СТОРИЗ СЕРИАЛИЗАТОРЫ ---
class StorySerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Story
        fields = ['id', 'author', 'author_name', 'file', 'created_at', 'expires_at']
        read_only_fields = ['author', 'created_at']

# --- ЗАМЕТКА СЕРИАЛИЗАТОРЫ ---
class NoteSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Note
        fields = ['id', 'author', 'author_name', 'text', 'created_at']
        read_only_fields = ['author', 'created_at']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'post', 'file', 'file_type']

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.ReadOnlyField(source='author.id')
    
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
    liked_by = LikeSerializer(source='likes', many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_name', 'caption', 
            'media', 'likes_count', 'liked_by', 'comments', 'created_at'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count() if hasattr(obj, 'likes') else 0

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'