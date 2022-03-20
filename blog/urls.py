from django.urls import path
from .views import CategoryView, CategoryDetailView, PostListView


urlpatterns = [
    path('list/', PostListView.as_view(), name='categories'),
    path('by/<category>/', CategoryDetailView.as_view(), name='details'),
]
