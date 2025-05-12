
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useTheme } from '../../../context/ThemeContext';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../../../styles/global.css';
import './Home.css';

const mockUser = {
  is_staff: false,
  firstname: 'کاربر',
};
const DOMAIN = process.env.REACT_APP_API_DOMAIN;

const Home = ({ user = mockUser }) => {
  const { isDarkMode } = useTheme();
  const [time, setTime] = useState(new Date());
  const [date, setDate] = useState('');
  const [weekDay, setWeekDay] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showGuide, setShowGuide] = useState(
    typeof window !== 'undefined'
      ? localStorage.getItem('popupClosed') !== 'true'
      : true
  );
  const searchTimeout = useRef(null);

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      setTime(now);

      const persianDate = new Intl.DateTimeFormat('fa-IR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      }).format(now);
      setDate(persianDate);

      const weekDayNames = [
        'یکشنبه',
        'دوشنبه',
        'سه‌شنبه',
        'چهارشنبه',
        'پنج‌شنبه',
        'جمعه',
        'شنبه',
      ];
      setWeekDay(weekDayNames[now.getDay()]);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleSearch = useCallback((e) => {
    const query = e.target.value;
    setSearchQuery(query);

    if (searchTimeout.current) clearTimeout(searchTimeout.current);

    if (query.trim() === '') {
      setContacts([]);
      setError('');
      return;
    }

    setLoading(true);
    setError('');
    searchTimeout.current = setTimeout(async () => {
      try {
        const encodedQuery = encodeURIComponent(query);
        const response = await axios.get(`/api/contacts/search/?q=${encodedQuery}`);
        setContacts(response.data.slice(0, 15));
      } catch (error) {
        setError('خطا در جستجوی مخاطبین. لطفاً دوباره تلاش کنید.');
        console.error('Error searching contacts:', error);
      } finally {
        setLoading(false);
      }
    }, 400);
  }, []);

  const formatTime = (date) => {
    return date.toLocaleTimeString('fa-IR', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  const handleCloseGuide = useCallback(() => {
    setShowGuide(false);
    if (typeof window !== 'undefined') {
      localStorage.setItem('popupClosed', 'true');
    }
  }, []);

  const handleOpenGuide = useCallback(() => {
    setShowGuide(true);
    if (typeof window !== 'undefined') {
      localStorage.setItem('popupClosed', 'false');
    }
  }, []);

  return (
    <div className={`home ${isDarkMode ? 'dark-mode' : ''}`}>
      <div className="container mt-4">
        <div className="d-flex justify-content-between align-items-center home-header-section">
          <div className="greeting text-right">
            <h3>درود {user.firstname}</h3>
          </div>
          <div className="d-flex align-items-center">
            {user.is_staff && (
              <a
                target="_blank"
                rel="noopener noreferrer"
                href={`${DOMAIN}/admin/`}
                className="btn btn-primary admin-panel-btn ml-3"
                title="پنل مدیریت"
              >
                <i className="fas fa-tachometer-alt admin-panel-icon"></i>
              </a>
            )}
            <div className="home-digital-clock">
              <div className="home-clock-date">{date}</div>
              <div className="home-clock-time">{formatTime(time)}</div>
              <div className="home-clock-day">{weekDay}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mt-4">
        <div className="card shadow-sm p-3 mb-5 bg-white rounded search-card">
          <Link
            to="/contacts/add"
            style={{ width: '50px' }}
            className="btn btn-primary add-contact-btn"
            title="افزودن مخاطب"
          >
            <i className="fas fa-plus"></i>
          </Link>
          {user.is_staff && (
            <Link
              to="/contacts"
              style={{ width: '50px' }}
              className="btn btn-primary manage-contact-btn"
              title="مدیریت مخاطبین"
            >
              <i className="fas fa-cogs"></i>
            </Link>
          )}
          <div className="card-body">
            <h5 className="card-title text-center">جستجو در مخاطبین</h5>
            <div className="text-center mt-3">
              <input
                type="text"
                value={searchQuery}
                onChange={handleSearch}
                className="form-control w-50 mx-auto"
                placeholder="نام، شرکت، شماره تلفن و  ..."
                style={{ textAlign: 'right' }}
              />
            </div>

            <div
              className="mt-3 search-results-box"
              style={{
                maxHeight: '450px',
                overflowY: 'auto',
                display:
                  searchQuery && contacts.length > 0
                    ? 'block'
                    : 'none',
              }}
            >
              <table className="table table-striped table-bordered">
                <thead className="table-dark">
                  <tr className="table-header">
                    <th style={{ width: '5%' }}>عملیات</th>
                    <th style={{ width: '15%' }}>دسته بندی</th>
                    <th style={{ width: '15%' }}>شماره موبایل</th>
                    <th style={{ width: '15%' }}>شماره تلفن</th>
                    <th style={{ width: '15%' }}>شرکت</th>
                    <th style={{ width: '15%' }}>نام خانوادگی</th>
                    <th style={{ width: '20%' }}>نام</th>
                  </tr>
                </thead>
                <tbody>
                  {contacts.map((contact) => (
                    <tr key={contact.id}>
                      <td>
                        <Link
                          to={`/contacts/${contact.id}`}
                          className="btn btn-info btn-sm"
                        >
                          جزئیات
                        </Link>
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
            {error && (
              <p className="text-center mt-3 text-danger" style={{ display: 'block' }}>
                {error}
              </p>
            )}
            {searchQuery && contacts.length === 0 && !loading && !error && (
              <p
                className="text-center mt-3 text-danger"
                style={{ display: 'block' }}
              >
                .نتیجه‌ای یافت نشد
              </p>
            )}
          </div>
        </div>
      </div>
      <div style={{ height: '150px', textAlign: 'right' }}></div>

      {showGuide && (
        <div
          className="guide-popup position-fixed"
          style={{
            bottom: '20px',
            right: '20px',
            zIndex: 1050,
            display: 'block',
          }}
        >
          <div
            className="card shadow-lg border-0"
            style={{
              width: '300px',
              borderRadius: '15px',
              overflow: 'hidden',
            }}
          >
            <div
              className="card-header bg-primary text-white d-flex justify-content-between align-items-center"
              style={{
                padding: '10px 15px',
                textAlign: 'right',
              }}
            >
              <button
                onClick={handleCloseGuide}
                className="btn btn-sm btn-light p-0"
                style={{
                  width: '24px',
                  height: '24px',
                  lineHeight: '24px',
                }}
              >
                ×
              </button>
              <h6 style={{ textAlign: 'right' }} className="mb-0">
                راهنمای استفاده
              </h6>
            </div>
            <div className="card-body p-3 text-right guide-pop-up">
              <p className="mb-2">
                برای اطلاعات بیشتر و راهنمایی، روی دکمه زیر کلیک کنید
              </p>
              <Link
                to="/contacts/guide"
                target="_blank"
                className="btn btn-primary btn-block mt-2"
                style={{
                  borderRadius: '10px',
                  boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
                }}
              >
                برو به صفحه راهنما
              </Link>
            </div>
          </div>
        </div>
      )}

      {!showGuide && (
        <button
          onClick={handleOpenGuide}
          className="btn btn-primary position-fixed"
          style={{
            bottom: '20px',
            right: '20px',
            zIndex: 1000,
            borderRadius: '50%',
            width: '50px',
            height: '50px',
            boxShadow: '0 4px 10px rgba(0,0,0,0.2)',
          }}
        >
          <i className="fas fa-question" style={{ fontSize: '20px' }}></i>
        </button>
      )}
    </div>
  );
};

export default Home;
