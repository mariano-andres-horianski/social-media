import axios from 'axios';

const getLoginData = async () => {
  const response = await axios.get('/get_login_data/');
  return response.data;
};

export default getLoginData;