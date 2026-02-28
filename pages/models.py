from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Төмендегі related_name-дерді қосыңыз
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="pages_user_set", # ЖАҢА ЖОЛ
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="pages_user_set", # ЖАҢА ЖОЛ
        related_query_name="user",
    )
    # ... қалған өрістер (bio, avatar_url, т.б.)