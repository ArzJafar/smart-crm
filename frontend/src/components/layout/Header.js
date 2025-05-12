import { NavLink } from 'react-router-dom';
import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useTheme } from '../../context/ThemeContext';
import '../../styles/global.css';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const { isDarkMode, toggleTheme } = useTheme();
  const [menuOpen, setMenuOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();

  // Handle toggling the navbar on mobile
  const handleTogglerClick = useCallback(
    () => setMenuOpen((prev) => !prev),
    []
  );

  // Handle dropdown open/close
  const handleDropdownClick = useCallback(
    (e) => {
      e.preventDefault();
      setDropdownOpen((prev) => !prev);
    },
    []
  );

  // Close dropdown when clicking outside or pressing Escape
  useEffect(() => {
    if (!dropdownOpen) return;
    const handleClick = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    };
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('mousedown', handleClick);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [dropdownOpen]);

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      const config = {
        headers: {
          'Authorization': `Token ${token}`
        }
      };

      await fetch('/api/auth/logout/', {
        method: 'POST',
        headers: config.headers
      });

      localStorage.removeItem('token');
      navigate('/login');
    } catch (error) {
      console.error('Logout error:', error);
      localStorage.removeItem('token');
      navigate('/login');
    }
  };

  return (
    <div className="header-container fixed-top custom-header-bg" dir="rtl">
      <nav className="navbar navbar-expand-lg navbar-light">
        <div className="container d-flex flex-row-reverse justify-content-between align-items-center">
          <NavLink className="navbar-brand order-1" to="/" exact="true">
            <img
              id="logo"
              src="/images/Logos/Smart-chekad-logo.png"
              alt="Chekad Logo"
              className="navbar-logo"
            />
          </NavLink>

          <button
            className="navbar-toggler order-2"
            type="button"
            aria-controls="navbarNav"
            aria-expanded={menuOpen}
            aria-label="Toggle navigation"
            onClick={handleTogglerClick}
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div
            className={`collapse navbar-collapse justify-content-end order-3${menuOpen ? ' show' : ''}`}
            id="navbarNav"
          >
            <ul className="navbar-nav ms-auto align-items-center flex-row flex-lg-row">
              <li className="nav-item mx-2">
                <NavLink
                  className="nav-link link-dark"
                  to="/"
                  activeClassName="active"
                  exact="true"
                >
                  خانه
                </NavLink>
              </li>
              <li className="nav-item mx-2">
                <NavLink
                  className="nav-link link-dark"
                  to="/contacts/colleagues"
                  activeClassName="active"
                  exact="true"
                >
                  داخلی همکاران
                </NavLink>
              </li>
              <li
                className={`nav-item dropdown mx-2${dropdownOpen ? ' show' : ''}`}
                ref={dropdownRef}
              >
                <button
                  className="nav-link dropdown-toggle btn btn-link"
                  id="navbarDropdown"
                  role="button"
                  aria-haspopup="true"
                  aria-expanded={dropdownOpen}
                  onClick={handleDropdownClick}
                  tabIndex={0}
                >
                  مدیریت حساب
                </button>
                <ul
                  className={`dropdown-menu custom-dropdown-menu dropdown-menu-end text-end${dropdownOpen ? ' show' : ''}`}
                  aria-labelledby="navbarDropdown"
                  style={{ direction: 'rtl', textAlign: 'right', minWidth: '150px' }}
                >
                  <li>
                    <NavLink className="dropdown-item" to="/profile" exact="true">
                      ویرایش حساب
                    </NavLink>
                  </li>
                  <li>
                    <button
                      className="dropdown-item"
                      onClick={handleLogout}
                    >
                      <i className="fas fa-sign-out-alt me-2"></i>
                      خروج
                    </button>
                  </li>
                </ul>
              </li>
              <li className="nav-item mx-2">
                <button
                  id="toggle-theme"
                  className="btn toggle-theme-btn"
                  onClick={toggleTheme}
                  title={isDarkMode ? 'حالت روشن' : 'حالت تاریک'}
                >
                  <i className={isDarkMode ? 'fas fa-sun' : 'fas fa-moon'}></i>
                </button>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default Navbar;