import React, { useState, useEffect } from 'react';
import { useTheme } from '../../../context/ThemeContext';
import axios from 'axios';
import './Home.css';

const Home = () => {
  const { isDarkMode } = useTheme();
  const [searchQuery, setSearchQuery] = useState('');
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [weekDay, setWeekDay] = useState('');

  useEffect(() => {
    // Update time every second
    const timer = setInterval(() => {
      const now = new Date();
      const persianDate = new Intl.DateTimeFormat('fa-IR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      }).format(now);
      
      const persianTime = new Intl.DateTimeFormat('fa-IR', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      }).format(now);
      
      const persianWeekDay = new Intl.DateTimeFormat('fa-IR', {
        weekday: 'long'
      }).format(now);

      setDate(persianDate);
      setTime(persianTime);
      setWeekDay(persianWeekDay);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleSearch = async (query) => {
    setSearchQuery(query);
    if (query.trim() === '') {
      setContacts([]);
      return;
    }

    setLoading(true);
    try {
      const response = await axios.get(`/api/contacts/search/?query=${query}`);
      setContacts(response.data);
    } catch (error) {
      console.error('Error searching contacts:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`home ${isDarkMode ? 'dark-mode' : ''}`}>
      <div className="container">
        <div className="header-section">
          <div className="time-section">
            <div className="digital-clock">
              <div className="date">{date}</div>
              <div className="time">{time}</div>
              <div className="day">{weekDay}</div>
            </div>
          </div>
          <div className="greeting">
            <h3>درود کاربر گرامی</h3>
          </div>
        </div>

        <div className="search-section">
          <div className="search-card">
            <div className="search-header">
              <button className="add-contact-btn" title="افزودن مخاطب">
                <i className="fas fa-plus"></i>
              </button>
            </div>
            
            <div className="search-body">
              <h5>جستجو در مخاطبین</h5>
              <div className="search-input-container">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => handleSearch(e.target.value)}
                  placeholder="... نام، شرکت، شماره تلفن و"
                  className="search-input"
                />
                {loading && <div className="search-loading"></div>}
              </div>
            </div>

            {contacts.length > 0 && (
              <div className="search-results">
                <table>
                  <thead>
                    <tr>
                      <th>عملیات</th>
                      <th>دسته‌بندی</th>
                      <th>شماره موبایل</th>
                      <th>شماره تلفن</th>
                      <th>شرکت</th>
                      <th>نام خانوادگی</th>
                      <th>نام</th>
                    </tr>
                  </thead>
                  <tbody>
                    {contacts.map(contact => (
                      <tr key={contact.id}>
                        <td>
                          <button className="details-btn">
                            جزئیات
                          </button>
                        </td>
                        <td>{contact.category || '-'}</td>
                        <td>{contact.mobile_number_1 || '-'}</td>
                        <td>{contact.phone_number_1 || '-'}</td>
                        <td>{contact.organization || '-'}</td>
                        <td>{contact.last_name || '-'}</td>
                        <td>{contact.first_name || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home; 