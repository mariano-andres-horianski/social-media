import React, { useState, useEffect } from 'react';

/*
  Component that displays personalized posts for a user, based on which users do they follow
  and when were they last updated.
  @param {string} userId - The id of the user whose posts are to be displayed.
*/
const ForYouPage = ({ userId }) => {
  // State to store the fetched and sorted posts
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    /**
     * Fetches and sorts the posts for the given user.
     * @returns {Promise<void>} - A promise that resolves when the posts are fetched and sorted.
    */
    const fetchAndSortPosts = async () => {
      try {
        // Fetch posts of the users followed by the given user
        const response = await getForYouPagePosts(userId);

        // Sort the fetched posts based when they were last updated, newest first
        const sortedPosts = response.sort(
          (a, b) => new Date(b.updated_at) - new Date(a.updated_at)
        );

        setPosts(sortedPosts);
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    };

    // Fetch and sort the posts when the userId prop changes
    fetchAndSortPosts();
  }, [userId]);

  return (
    <div>
      {/* Render the sorted posts */}
      {posts.map((post) => (
        <div key={post.id}>
          <p>{post.title}</p>
          <p>{post.content}</p>
          <p>{post.updated_at}</p>
        </div>
      ))}
    </div>
  );
};

export default ForYouPage;