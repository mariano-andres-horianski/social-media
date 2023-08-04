from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post

class PostView(APIView):
    def get(self, request):
        posts = Post.objects.filter(owner=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        post = Post(owner=request.user)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        post = Post.objects.get(id=id)
        post.delete()
        return Response(f'Post {id} was deleted')

    def put(self, request, id):
        post = Post.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)