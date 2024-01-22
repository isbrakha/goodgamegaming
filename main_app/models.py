from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

class Game(models.Model):
    api_id = models.IntegerField
    name = models.CharField(max_length=255, unique=True)
    rating = models.FloatField(blank=True, null=True)
    released = models.DateField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    platforms = ArrayField(models.CharField(max_length=250), blank=True, null=True)
    developer = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    esrb_rating = models.CharField(max_length=255, blank=True, null=True)
    genres = ArrayField(models.CharField(max_length=250), blank=True, null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='games')
    def __str__(self):
      return f"{self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    # preferred_genres = models.ManyToManyField(Genre, related_name='user_profiles')
    liked_games = models.ManyToManyField(Game)

    def __str__(self):
      return f"{self.user.username}'s profile"



class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.FloatField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.author.username} for {self.game.name}"
    
class Tip(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='tips')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tips')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tip by {self.author.username} for {self.game.name}"


