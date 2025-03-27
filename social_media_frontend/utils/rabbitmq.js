import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PostsConsumer = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/posts/');
                setPosts(response.data);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch posts');
                setLoading(false);
            }
        };

        fetchPosts();
    }, []);

    if (loading) return <div>Loading posts...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="posts-container">
            {posts.map((post) => (
                <div key={post.id} className="post">
                    <div className="post-header">
                        <img 
                            src={post.author.profile_picture || '/default-avatar.png'} 
                            alt={post.author.username}
                            className="author-avatar"
                        />
                        <span className="author-name">{post.author.username}</span>
                    </div>
                    <p className="post-content">{post.content}</p>
                    <div className="post-footer">
                        <span className="post-date">
                            {new Date(post.created_at).toLocaleDateString()}
                        </span>
                        <div className="post-actions">
                            <button className="like-button">
                                ❤️ {post.likes_count || 0}
                            </button>
                        </div>
                    </div>
                </div>
            ))}
            <style jsx>{`
                .posts-container {
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .post {
                    background: white;
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .post-header {
                    display: flex;
                    align-items: center;
                    margin-bottom: 10px;
                }
                .author-avatar {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    margin-right: 10px;
                }
                .author-name {
                    font-weight: bold;
                }
                .post-content {
                    margin: 10px 0;
                    line-height: 1.5;
                }
                .post-footer {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-top: 10px;
                    color: #666;
                }
                .post-actions button {
                    background: none;
                    border: none;
                    cursor: pointer;
                    padding: 5px 10px;
                    border-radius: 5px;
                }
                .post-actions button:hover {
                    background: #f0f0f0;
                }
            `}</style>
        </div>
    );
};

export default PostsConsumer;
