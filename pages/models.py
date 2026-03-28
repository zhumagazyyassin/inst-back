from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username}"

class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    # Файлды сақтау жолы
    file = models.FileField(upload_to='post_media/') 
    # Файл түрі (image немесе video)
    file_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])

    def __str__(self):
        return f"{self.file_type} for Post {self.post.id}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('post', 'user')

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    
    class Meta:
        unique_together = ('follower', 'following')

# --- ЖАҢАДАН ҚОСЫЛҒАН КЕСТЕЛЕР ---

class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    file = models.FileField(upload_to='stories/')
    created_at = models.DateTimeField(auto_now_add=True)
    # Сториздің мерзімі (мысалы, 24 сағат)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Story by {self.author.username}"

class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    text = models.CharField(max_length=60) # Заметка әдетте қысқа болады
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.author.username}"