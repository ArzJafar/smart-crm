import React from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../../../context/ThemeContext';
import './Header.css';

const Header = () => {
  const { isDarkMode, toggleTheme } = useTheme();

  return (
    <header className="header">
      <nav className="navbar">
        <div className="container">
          <Link to="/" className="logo">
            <img src="/logo.png" alt="Smart Chekad" />
          </Link>

          <div className="nav-links">
            <Link to="/contacts/colleagues">داخلی همکاران</Link>
            <Link to="/profile">مدیریت حساب</Link>
            <Link to="/">خانه</Link>
            
            <button 
              className="theme-toggle"
              onClick={toggleTheme}
              aria-label="تغییر تم"
            >
              <i className={`fas fa-${isDarkMode ? 'sun' : 'moon'}`}></i>
            </button>
          </div>

          <button className="mobile-menu-btn">
            <i className="fas fa-bars"></i>
          </button>
        </div>
      </nav>
    </header>
  );
};

export default Header; 