from rest_framework import serializers
from django.utils.timezone import now
from .models import Category, Like, Post, Comment, PostView

def getDuration(then, now = now(), interval = "default"):

    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration = now - then # For build-in functions
    duration_in_s = duration.total_seconds() 
    
    def years():
      return divmod(duration_in_s, 31536000) # Seconds in a year=31536000.

    def days(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 86400) # Seconds in a day = 86400

    def hours(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 3600) # Seconds in an hour = 3600

    def minutes(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 60) # Seconds in a minute = 60

    def seconds(seconds = None):
      if seconds != None:
        return divmod(seconds, 1)   
      return duration_in_s
    
    def totalDuration():
        y = years()
        d = days(y[1]) # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        if int(y[0]) < 0:
            return 'Just Now'
        elif int(y[0]) == 0 and int(d[0]) == 0:
            return '{} hours, {} minutes {} seconds ego'.format(int(h[0]), int(m[0]), int(s[0]))
        elif int(y[0]) == 0:
            return '{} days, {} hours, {} minutes {} seconds ego'.format(int(d[0]), int(h[0]), int(m[0]), int(s[0]))
        else:
            return "{} years, {} days, {} hours, {} minutes {} seconds ego".format(int(y[0]), int(d[0]), int(h[0]), int(m[0]), int(s[0]))

        # if int(y[0]) == 0 and int(d[0]) == 0:
        #     return '{} hours, {} minutes {} seconds ego'.format(int(h[0]), int(m[0]), int(s[0]))
        # if int(y[0]) == 0:
        #     return '{} days, {} hours, {} minutes {} seconds ego'.format(int(d[0]), int(h[0]), int(m[0]), int(s[0]))
        # return "{} years, {} days, {} hours, {} minutes {} seconds ego".format(int(y[0]), int(d[0]), int(h[0]), int(m[0]), int(s[0]))

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()
    }[interval]

class PostViewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = PostView
        fields = ('user', 'post')

    def create(self, validated_data):
        user = self.context['request'].user
        if 'user' in validated_data:
            user = validated_data['user']
        return PostView.objects.create(user=user, **validated_data)

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = Like
        fields = ('user', 'post')

    def create(self, validated_data):
        user = self.context['request'].user
        if 'user' in validated_data:
            user = validated_data['user']
        return Like.objects.create(user=user, **validated_data)

class CommentSerializer(serializers.ModelSerializer):
    since_creation = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = ('user', 'post', 'content', 'since_creation', 'created_date')
    
    def get_since_creation(self, obj):
        final = getDuration(obj.created_date)
        return final
    
    def create(self, validated_data):
        user = self.context['request'].user
        if 'user' in validated_data:
            user = validated_data['user']
        return Comment.objects.create(user=user, **validated_data)

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id', 'name')

class PostSerializer(serializers.ModelSerializer):
    since_creation = serializers.SerializerMethodField()
    comment_post = CommentSerializer(many=True, read_only=True, required=False)
    comments_count = serializers.SerializerMethodField()
    like_post = LikeSerializer(many=True, read_only=True, required=False)
    likes_count = serializers.SerializerMethodField()
    postview_post = PostViewSerializer(many=True, read_only=True, required=False)
    postviews_count = serializers.SerializerMethodField()
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault()) #buna bakılacak
    category = CategorySerializer(many=True, required=False)
    user = serializers.StringRelatedField(required=False)
    
    class Meta:
        model = Post
        fields = ('id', 'category', 'user', 'title', 'body', 'image', 'since_creation', 'comment_post', 'comments_count', 'like_post', 'likes_count', 'postview_post', 'postviews_count')

    def get_comments_count(self, obj):
        return obj.comment_post.count()
    
    def get_likes_count(self, obj):
        return obj.like_post.count()

    def get_postviews_count(self, obj):
        return obj.postview_post.count()
    
    def get_since_creation(self, obj):
        final = getDuration(obj.created_date)
        return final

    def create(self, validated_data):
        user = self.context['request'].user
        category = validated_data.pop("category")
        validated_data["user"] = user
        post = Post.objects.create(**validated_data)
        if category:
            for cate in category:
                new_cat, _ = Category.objects.get_or_create(name=cate.get('name'))
                post.category.add(new_cat.id)
        post.save()
        return post

class CategoriesSerializer(serializers.ModelSerializer):
    post_cate = PostSerializer(many=True, write_only=True)
    post_count = serializers.SerializerMethodField() 
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'post_cate', 'post_count')
    
    def get_post_count(self, obj):
        return obj.post_cate.count()