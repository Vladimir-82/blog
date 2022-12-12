from django.db import models
from django.contrib.auth.models import User




class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', null=True,
                                 on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos', blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=150)


    def __str__(self):
        return self.title

