from rest_framework import generics
from .serializers import CategorySerializer, PostSerializer
from .models import Category, Post
from rest_framework.permissions import IsAdminUser

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)

    
class CategoryDetailView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        post = self.kwargs['post_cate'].title()
        return Post.objects.filter(category__name=post)