import React from 'react';
import { useTheme } from '../../../context/ThemeContext';
import { Link } from 'react-router-dom';
import '../../../styles/global.css';
import './NotFound.css';


const NotFound = () => {
  const { isDarkMode } = useTheme();

  return (
    <div className={`not-found ${isDarkMode ? 'dark-mode' : ''}`}>
      <div className="container">
        <div className="not-found-content">
          <img
            src="/images/Logos/404.png"
            alt="404 Not Found"
            className="not-found-img"
          />
          <h1>۴۰۴</h1>
          <h2>صفحه مورد نظر پیدا نشد!</h2>
          <p>
            اوه! به نظر می‌رسد در بیابان اینترنت گم شدی... <br />
            شاید آدرس را اشتباه وارد کردی یا این صفحه دیگر وجود ندارد.
          </p>
          <Link to="/" className="home-link">
            <span role="img" aria-label="home">🏠</span> بازگشت به خانه
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;