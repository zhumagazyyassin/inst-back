from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. User моделі (Стандартты пайдаланушыны кеңейту)
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Қақтығысты болдырмау үшін:
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name="pages_user_set",                
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name="pages_user_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.username

# 2. Post моделі
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.caption[:20]}"

# 3. Media моделі
class Media(models.Model):
    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    file = models.FileField(upload_to='posts/', blank=True, null=True)
    url = models.CharField(max_length=512, blank=True, null=True)
    mime_type = models.CharField(max_length=64, blank=True, null=True)
    order_idx = models.IntegerField(default=0)
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Media for Post {self.post.id}"

# 4. Follow моделі (Қақтығыссыз related_name)
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followee')
        verbose_name_plural = "Follows"

    def __str__(self):
        return f"{self.follower.username} follows {self.followee.username}"

# 5. Comment моделі
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

# 6. Like моделі
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.id}"