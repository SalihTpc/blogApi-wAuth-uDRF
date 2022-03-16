from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    category = models.ManyToManyField(Category)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True)
    body = models.TextField()
    image = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} commented on {self.post}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} liked {self.post}'

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} viewed {self.post}'