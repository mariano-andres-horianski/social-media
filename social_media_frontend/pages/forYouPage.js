import React, { useState, useEffect, memo } from 'react';

const Post = memo(({ post, showStats }) => (
  <div key={post.id}>
    <p>{post.title}</p>
    <p>{post.content}</p>
    <p>{post.updated_at}</p>
    {showStats && (
      <div>
        <p>Comment count: {post.comment_count}</p>
        <p>Repost count: {post.repost_count}</p>
        <p>Quote count: {post.quote_count}</p>
      </div>
    )}
  </div>
));

const ForYouPage = ({ userId }) => {
  const [posts, setPosts] = useState([]);
  const [currentUser, setCurrentUser] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPosts = async () => {
    try {
      const { user, posts: fetchedPosts } = await getForYouPagePosts(userId);
      setCurrentUser(user);
      const sortedPosts = fetchedPosts.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
      setPosts(sortedPosts);
      setIsLoading(false);
    } catch (error) {
      setError(error.message);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, [userId]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      {posts.map((post) => (
        <Post
          key={post.id}
          post={post}
          showStats={currentUser.is_superuser}
        />
      ))}
    </div>
  );
};

export default ForYouPage;