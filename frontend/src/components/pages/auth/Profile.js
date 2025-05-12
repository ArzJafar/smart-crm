import React, { useState, useEffect } from 'react';
import { useTheme } from '../../../context/ThemeContext';
import axios from 'axios';
import '../../../styles/global.css';

const Profile = () => {
  const { isDarkMode } = useTheme();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('/api/profile/');
        setProfile(response.data);
      } catch (error) {
        setError('خطا در دریافت اطلاعات پروفایل');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) {
    return (
      <div className={`profile ${isDarkMode ? 'dark-mode' : ''}`}>
        <div className="container">
          <div className="loading">در حال بارگذاری...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`profile ${isDarkMode ? 'dark-mode' : ''}`}>
        <div className="container">
          <div className="error">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`profile ${isDarkMode ? 'dark-mode' : ''}`}>
      <div className="container">
        <div className="profile-card">
          <div className="profile-header">
            <h2>پروفایل کاربری</h2>
            <button className="edit-btn">ویرایش پروفایل</button>
          </div>
          
          <div className="profile-content">
            <div className="profile-info">
              <div className="info-row">
                <span className="label">نام:</span>
                <span className="value">{profile.first_name}</span>
              </div>
              <div className="info-row">
                <span className="label">نام خانوادگی:</span>
                <span className="value">{profile.last_name}</span>
              </div>
              <div className="info-row">
                <span className="label">ایمیل:</span>
                <span className="value">{profile.email}</span>
              </div>
              <div className="info-row">
                <span className="label">شماره موبایل:</span>
                <span className="value">{profile.mobile_number}</span>
              </div>
              <div className="info-row">
                <span className="label">تاریخ عضویت:</span>
                <span className="value">{profile.join_date}</span>
              </div>
            </div>
            
            <div className="profile-actions">
              <button className="change-password-btn">تغییر رمز عبور</button>
              <button className="logout-btn">خروج از حساب کاربری</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile; 