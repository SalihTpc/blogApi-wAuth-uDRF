from django.urls import path
from .views import CategoryView, CategoryDetailView


urlpatterns = [
    path('list/', CategoryView.as_view(), name='categories'),
    path('list/<category>/', CategoryDetailView.as_view(), name='details'),
]
