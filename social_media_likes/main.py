from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import requests
import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
CORS(app)


db = SQLAlchemy(app)


# This service will store some basic data for the posts in case that a user likes a deleted post (as you can do in Twitter if a deleted post is cached).
# Will use it to retrieve posts if the Django service stops working. Not gonna think of a leader election algorithm for now.
# Might try to use it for a hinted handoff or delete it.
@dataclass
class Post(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class PostUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'post_id', name='user_post_unique')

@app.route('/api/posts/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()
    
    user_id = json['id']
    post_id = id
    post_like = PostUser.query.filter_by(user_id=user_id, post_id=post_id).first()

    # We'll check if post_like is in the database, if it is we'll remove it, but if it isn't we'll add it
    if post_like:
        db.session.delete(post_like)
        db.session.commit()
        return jsonify({'message': 'Post unliked'})
    else:
        post_like = PostUser(user_id=user_id, post_id=post_id)
        db.session.add(post_like)
        db.session.commit()
        # Notify the post service that a post has been liked
        redis_client.publish('post_likes', f'PostLiked:{id}')

        return jsonify({'message': 'Post liked'})

    
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')