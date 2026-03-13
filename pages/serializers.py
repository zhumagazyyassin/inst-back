from rest_framework import serializers
from .models import User, Post, Media, Comment, Follow, Like

class UserSerializer(serializers.ModelSerializer):
    # Пароль доступен только для записи (input), не возвращается в ответе (output)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'avatar_url']

    def create(self, validated_data):
        # Метод create_user автоматически хеширует пароль перед сохранением
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            avatar_url=validated_data.get('avatar_url', '')
        )
        return user

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'post', 'file', 'url', 'mime_type', 'order_idx', 'caption']
        # Поля url и mime_type не являются обязательными при создании
        extra_kwargs = {
            'post': {'required': False},
            'url': {'required': False, 'allow_null': True},
            'mime_type': {'required': False, 'allow_null': True},
        }

class CommentSerializer(serializers.ModelSerializer):
    # Отображает имя пользователя вместо ID
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_at']
        
class PostSerializer(serializers.ModelSerializer):
    # Показывает подробную информацию об авторе (без пароля)
    author = UserSerializer(read_only=True)
    # Показывает список медиафайлов, связанных с постом
    media = MediaSerializer(many=True, read_only=True)
    # Вычисляемые поля для подсчета лайков и комментариев
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'media', 'comments_count', 'likes_count', 'created_at']