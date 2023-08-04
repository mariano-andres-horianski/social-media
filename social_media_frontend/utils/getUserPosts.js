import axios from 'axios';

const getUserPosts = async (userId) => {
  const response = await axios.get('/get_user_posts/${userId}');
  return response.data;
};

export default getUserPosts;