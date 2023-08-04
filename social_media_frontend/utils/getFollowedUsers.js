import axios from 'axios';

const getFollowedUsers = async (userId) => {
  const response = await axios.get('/get_followed_users/${userId}');
  return response.data;
};

export default getFollowedUsers;