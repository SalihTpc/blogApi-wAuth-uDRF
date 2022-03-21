from django.urls import path
from .views import CategoryView, CategoryDetailView, PostListView, PostDetailView, CommentView, LikeView, PostViewList


urlpatterns = [
    path('list/', PostListView.as_view(), name='postList'),
    path('list/<int:id>/', PostDetailView.as_view(), name='post-detail'),
    path('list/<int:id>/comment/', CommentView.as_view(), name='comment'),
    path('list/<int:id>/like/', LikeView.as_view(), name='like'),
    path('list/<int:id>/view/', PostViewList.as_view(), name='postView'),
    path('category/list/', CategoryView.as_view(), name='cetagorylist'),
    path('category/<category>/', CategoryDetailView.as_view(), name='details'),
]
