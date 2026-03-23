from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True)  # <-- Add this
    role = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    home_type = models.CharField(max_length=50, blank=True)
    total_predictions = models.IntegerField(default=0)
    failures = models.IntegerField(default=0)
    successes = models.IntegerField(default=0)
    AVATAR_CHOICES = [
        ('default.png', 'Default Avatar'),
        ('AvatarB1.png', 'Avatar 1'),
        ('AvatarB2.png', 'Avatar 2'),
        ('AvatarB3.png', 'Avatar 3'),
        ('AvatarB4.png', 'Avatar 4'),
        ('AvatarB5.png', 'Avatar 5'),
        ('AvatarG1.png', 'Avatar 6'),
        ('AvatarG2.png', 'Avatar 7'),
        ('AvatarG3.png', 'Avatar 8'),
        ('AvatarG4.png', 'Avatar 9'),
        ('AvatarG5.png', 'Avatar 10'),
        
    ]
    profile_pic = models.CharField(max_length=100, choices=AVATAR_CHOICES, default='default.png')


    def save(self, *args, **kwargs):
        # <-- Add this to auto-sync username from linked User
        if self.user:
            self.username = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True)
    room_type = models.CharField(max_length=100)
    material_type = models.CharField(max_length=100)
    lighting = models.CharField(max_length=100)
    predicted_failure = models.BooleanField()
    probability = models.FloatField(null=True, blank=True)
    recommendations = models.JSONField(null=True, blank=True)
    predicted_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # <-- Add this to auto-sync username from linked User
        if self.user:
            self.username = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.room_type} - {self.predicted_failure}"

class Feedback(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}/5"

