import uuid
from django.db import models
from django.contrib.auth.models import User
from main_app.models import Niche
from managers.models import Campaign


class CreatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField()
    niches = models.ManyToManyField(Niche)
    audience_demographic = models.TextField()

    def __str__(self):
        return self.bio

class SocialPlatform(models.Model):
    PLATFORMS = (
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('Instagram', 'Instagram'),
        ('Pinterest', 'Pinterest'),
        ('Blog', 'Blog'),
        ('YouTube', 'YouTube'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(CreatorProfile, on_delete=models.CASCADE)
    platform = models.CharField(max_length=65, choices=PLATFORMS)
    account_name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    metrics = models.TextField()

    def __str__(self):
        return self.account_name


class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(CreatorProfile, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    offering = models.TextField()
    price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
