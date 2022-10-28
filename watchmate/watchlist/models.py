from statistics import mode
from tkinter import CASCADE
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class StreamPlatform(models.Model):
    name=models.CharField(max_length=50)
    about=models.CharField(max_length=200)
    website=models.URLField(max_length=200)

    def __str__(self):
        return self.name

class WatchList(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    platform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name='watch_list')
    active=models.BooleanField(default=True)  #means movie is released or not
    created=models.DateTimeField(auto_now_add=True)
    avg_rating=models.FloatField(default=0)
    total_rating=models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Review(models.Model):
    review_user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    text=models.TextField(max_length=200,null=True)
    watchlist=models.ForeignKey(WatchList,on_delete=models.CASCADE ,related_name='reviews')
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return f'{self.watchlist.title} rates {self.rating} star by {self.review_user}'
    