import React, { useState, useEffect } from 'react';
import { useTheme } from '../../../context/ThemeContext';
import axios from 'axios';
import '../../../styles/global.css';

const Dashboard = () => {
  const { isDarkMode } = useTheme();
  const [stats, setStats] = useState({
    totalContacts: 0,
    activeEmployees: 0,
    totalFiles: 0,
    recentActivities: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [contactsRes, employeesRes, filesRes, activitiesRes] = await Promise.all([
          axios.get('/api/contacts/count/'),
          axios.get('/api/employees/active-count/'),
          axios.get('/api/production-files/count/'),
          axios.get('/api/activities/recent/')
        ]);

        setStats({
          totalContacts: contactsRes.data.count,
          activeEmployees: employeesRes.data.count,
          totalFiles: filesRes.data.count,
          recentActivities: activitiesRes.data
        });
      } catch (error) {
        setError('خطا در دریافت اطلاعات داشبورد');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className={`dashboard ${isDarkMode ? 'dark-mode' : ''}`}>
        <div className="container">
          <div className="loading">در حال بارگذاری...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`dashboard ${isDarkMode ? 'dark-mode' : ''}`}>
        <div className="container">
          <div className="error">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`dashboard ${isDarkMode ? 'dark-mode' : ''}`}>
      <div className="container">
        <h2>داشبورد</h2>
        
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">
              <i className="fas fa-users"></i>
            </div>
            <div className="stat-info">
              <h3>مخاطبین</h3>
              <p>{stats.totalContacts}</p>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="stat-icon">
              <i className="fas fa-user-tie"></i>
            </div>
            <div className="stat-info">
              <h3>کارمندان فعال</h3>
              <p>{stats.activeEmployees}</p>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="stat-icon">
              <i className="fas fa-file-alt"></i>
            </div>
            <div className="stat-info">
              <h3>فایل‌های تولید</h3>
              <p>{stats.totalFiles}</p>
            </div>
          </div>
        </div>

        <div className="recent-activities">
          <h3>فعالیت‌های اخیر</h3>
          <div className="activities-list">
            {stats.recentActivities.map(activity => (
              <div key={activity.id} className="activity-item">
                <div className="activity-icon">
                  <i className={`fas fa-${activity.icon}`}></i>
                </div>
                <div className="activity-content">
                  <p>{activity.description}</p>
                  <span className="activity-time">{activity.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 