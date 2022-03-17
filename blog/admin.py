from django.contrib import admin
from .models import Category, Post, Comment, Like, PostView 

class CategoryAdmin(models.ModelAdmin):
    exclude = ('slug',)

class PostAdmin(models.ModelAdmin):
    exclude = ('slug',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(PostView)
