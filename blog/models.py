from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    category = models.ManyToManyField(Category, related_name='post_cate')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True)
    body = models.TextField()
    image = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.title} || {self.user}'

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} commented on {self.post}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')

    def __str__(self):
        return f'{self.user} liked {self.post}'

    class Meta:
        unique_together = (('user', 'post'))

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postview_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postview_post')
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} viewed {self.post}'

    class Meta:
        unique_together = (('user', 'post'))