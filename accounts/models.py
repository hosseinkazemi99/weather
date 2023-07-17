from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(unique=True)
    text = models.TextField(max_length=800, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
