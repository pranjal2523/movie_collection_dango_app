from django.db import models
from django.contrib.auth.models import User

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    uuid = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Movie(models.Model):
    collection = models.ForeignKey(Collection, related_name='movies', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    genres = models.CharField(max_length=200, blank=True, null=True)
    uuid = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    

class RequestCounter(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.usermane
