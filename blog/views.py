from rest_framework import generics, status
from .serializers import PostSerializer, CategoriesSerializer, CommentSerializer, LikeSerializer, PostViewSerializer
from .models import Category, Post, Comment, Like, PostView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from .pagination import PostPagination
from .permission import IsOwnerOrReadOnly


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer

    
class CategoryDetailView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        category = self.kwargs['category'].title()
        return Post.objects.filter(category__name=category)

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PostPagination

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Post created!'
        })

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Post updated!'
        })

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        content = {'message': 'Post deleted!'}
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Post deleted!'
        })

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs['id']
        return Comment.objects.filter(post=post_id)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Comment added successfully!'
        })

class LikeView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs['id']
        return Like.objects.filter(post=post_id)


class PostViewList(generics.ListCreateAPIView):
    queryset = PostView.objects.all()
    serializer_class = PostViewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs['id']
        return PostView.objects.filter(post=post_id)
