import React from 'react';
import { useTheme } from '../../../context/ThemeContext';
import './Footer.css';

const Footer = () => {
  const { isDarkMode } = useTheme();

  return (
    <footer className={`footer ${isDarkMode ? 'dark-mode' : ''}`}>
      <div className="container">
        <div className="footer-content">
          <div className="footer-section education">
            <img 
              src="/education.png" 
              alt="Education" 
              className="education-logo"
            />
            <a 
              href="https://chekad.com/education/" 
              target="_blank" 
              rel="noopener noreferrer"
              className="education-link"
            >
              سایت آموزشی چکاد
            </a>
          </div>

          <div className="footer-section articles">
            <h5>آخرین مقالات</h5>
            <div className="article-links">
              <a 
                href="https://chekad.com/managing-time1/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="article-link"
              >
                مدیریت زمان
              </a>
              <a 
                href="https://chekad.com/work-smarter-not-harder/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="article-link"
              >
                ۱۶ رهنمود برای آنکه هوشمندانه‌تر کار کنید، نه سخت‌تر!
              </a>
              <a 
                href="https://chekad.com/sheets-or-excel/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="article-link"
              >
                تفاوت‌های گوگل شیت با اکسل
              </a>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p className="copyright">
            &copy; Created by Chekad IT Team
          </p>
          <p className="version">
            Version 1.0.5
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 