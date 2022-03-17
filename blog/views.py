from rest_framework import generics
from .serializers import CategorySerializer, PostSerializer
from .models import Category, Post

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    
class CategoryDetailView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        post = self.kwargs['category'].title()
        return Post.objects.filter(category__name=post)