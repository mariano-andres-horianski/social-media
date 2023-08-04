from django.urls import path
from .views import PostView

app_name = 'posts'

urlpatterns = [
    path('posts/', PostView.as_view(), name='posts_view'),
]