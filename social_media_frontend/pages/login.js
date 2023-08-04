import React, { useState, useEffect } from 'react';
import getLoginData from '../utils/getLoginData';

const LoginPage = () => {
  const [loginData, setLoginData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await getLoginData();
      setLoginData(response);
    };
    fetchData();
  }, []);

  return (
    <div>
      {loginData ? (
        <form method="POST" action="/login/">
          <input type="hidden" name="csrfmiddlewaretoken" value={loginData.csrf_token} />
          <div dangerouslySetInnerHTML={{ __html: loginData.form }} />
          <button type="submit">Log in</button>
        </form>
      ) : (
        <p>Loading login data...</p>
      )}
    </div>
  );
};

export default LoginPage;