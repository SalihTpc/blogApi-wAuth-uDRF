from django.urls import path
from .views import CategoryView, CategoryDetailView, PostListView


urlpatterns = [
    path('list/', PostListView.as_view(), name='postList'),
    path('category/list/', CategoryView.as_view(), name='cetagorylist'),
    path('category/<category>/', CategoryDetailView.as_view(), name='details'),
]
