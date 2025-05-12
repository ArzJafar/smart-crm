import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../../../styles/global.css';

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleLogout = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          navigate('/login');
          return;
        }

        // Set the token in the Authorization header
        const config = {
          headers: {
            'Authorization': `Token ${token}`
          }
        };

        // Call the logout API
        await axios.post('/api/auth/logout/', {}, config);

        // Clear the token from localStorage
        localStorage.removeItem('token');
        
        // Clear the Authorization header
        delete axios.defaults.headers.common['Authorization'];

        // Redirect to login page
        navigate('/login');
      } catch (error) {
        console.error('Logout error:', error);
        // Even if the API call fails, clear the token and redirect
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
        navigate('/login');
      }
    };

    handleLogout();
  }, [navigate]);

  return (
    <div className="logout-container">
      <div className="container">
        <div className="logout-card">
          <h2>در حال خروج...</h2>
          <div className="loading-spinner"></div>
        </div>
      </div>
    </div>
  );
};

export default Logout; 