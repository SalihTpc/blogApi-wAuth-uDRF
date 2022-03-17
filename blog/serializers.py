from rest_framework import serializers
from .models import Category, Like, Post, Comment, PostView

class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = ('user', 'post')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'post')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'post', 'content', 'created_date')

class PostSerializer(serializers.ModelSerializer):
    comment_user = CommentSerializer(many=True, write_only=True)
    comments_count = serializers.SerializerMethodField()
    like_user = LikeSerializer(many=True, write_only=True)
    likes_count = serializers.SerializerMethodField()
    postview_user = PostViewSerializer(many=True, write_only=True)
    postviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'category', 'user', 'title', 'comment_user', 'comments_count', 'like_user', 'likes_count', 'postview_user', 'postviews_count')

    def get_comments_count(self, obj):
        return obj.comment_user.count()
    
    def get_likes_count(self, obj):
        return obj.like_user.count()

    def get_postviews_count(self, obj):
        return obj.postview_user.count()

class CategorySerializer(serializers.ModelSerializer):
    post_cate = PostSerializer(many=True, write_only=True)
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'post_cate', 'post_count')
    
    def get_post_count(self, obj):
        return obj.post_cate.count()