import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import getLoginData from '../utils/getLoginData';
import PostsConsumer from '../utils/rabbitmq';

const HomePage = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loginData, setLoginData] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const fetchData = async () => {
      const response = await getLoginData();
      setLoginData(response);
      setIsLoggedIn(response.is_authenticated);
    };
    fetchData();
  }, []);

  useEffect(() => {
    if (!isLoggedIn) {
      router.push('/login');
    } else {
      router.push('/for_you_page');
    }
  }, [isLoggedIn]);

  return (
    <div>
      <p>Redirecting...</p>
      <PostsConsumer />
    </div>

  );
};

export default HomePage;