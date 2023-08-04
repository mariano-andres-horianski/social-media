
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('owner', 'image', 'likes', 'created_at', 'updated_at', 'caption')