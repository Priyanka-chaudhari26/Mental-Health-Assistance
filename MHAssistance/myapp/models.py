from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
# bala 1234
class CustomUserManager(BaseUserManager):
    def create_user(self, password=None, **extra_fields):
        if not password:
            raise ValueError('The Password must be set')

        # anon_username = extra_fields.get('anon_username') or self.generate_anon_username()
        anon_username = extra_fields.pop('anon_username', self.generate_anon_username())
        user = self.model(anon_username=anon_username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(password=password, **extra_fields)

    def generate_anon_username(self):
        adjectives = ['Calm', 'Mindful', 'Happy', 'Peaceful', 'Bright']
        nouns = ['Fox', 'Owl', 'Lion', 'Swan', 'Dolphin']
        unique_id = uuid.uuid4().hex[:6]  # 6-character unique fragment
        return f"{random.choice(adjectives)}{random.choice(nouns)}{unique_id}"

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    anon_username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(unique=True, null= True, blank=True)
    total_score = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'anon_username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.anon_username
    

class Assessment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    assessment = models.ForeignKey(Assessment, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    def clean(self):
        # Validate that at least one option exists
        if not self.pk:  # Skip validation if the question hasn't been saved yet
            return
        if not self.options.exists():
            raise ValidationError("Each question must have at least one option.")
    def __str__(self):
        return f"{self.text} ({self.assessment.title})"
    
class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    score = models.IntegerField()  # e.g., 0 for "Not at all", 3 for "Nearly every day"

    def __str__(self):
        return f"{self.text} - {self.score}"

class UserAssessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    total_score = models.IntegerField()
    result = models.CharField(max_length=255) 
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.assessment.title} ({self.result})"


class SelfCareContent(models.Model):
    CONTENT_TYPES = [
        ('blog', 'Blog'),
        ('video', 'Video'),
        ('tutorial', 'Tutorial'),
    ]

    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"

class Challenge(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class UserChallenge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.challenge.title}"


class ForumPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')  # Optional

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post.title}"

class PostLike(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Prevent multiple likes from the same user

    def __str__(self):
        return f"{self.user} liked {self.post.title}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
