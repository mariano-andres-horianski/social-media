import redis
from posts.models import Post

# Connect to Redis broker
redis_client = redis.Redis(host='localhost', port=6379, db=0)
pubsub = redis_client.pubsub()
pubsub.subscribe('post_likes')

for message in pubsub.listen():
    if message['type'] == 'message':
        data = message['data']
        if data.startswith(b'PostLiked:'):
            post_id = int(data.split(b':')[1])
            print(f"Post liked: {post_id}")
            # Once this service has been notified of a post been liked, increment it's like count by 1
            post = Post.query.get(post_id)
            post.likes += 1
            post.save()
            print("likes count increased")