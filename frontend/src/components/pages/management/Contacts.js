import React, { useState, useEffect } from 'react';
import { useTheme } from '../../../context/ThemeContext';
import axios from 'axios';
import '../../../styles/global.css';

const Contacts = () => {
  const { isDarkMode } = useTheme();
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchContacts();
  }, []);

  const fetchContacts = async () => {
    try {
      const response = await axios.get('/api/contacts/');
      setContacts(response.data);
    } catch (error) {
      setError('خطا در دریافت لیست مخاطبین');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
  };

  const filteredContacts = contacts.filter(contact => {
    const searchTerm = searchQuery.toLowerCase();
    return (
      contact.first_name?.toLowerCase().includes(searchTerm) ||
      contact.last_name?.toLowerCase().includes(searchTerm) ||
      contact.organization?.toLowerCase().includes(searchTerm) ||
      contact.mobile_number_1?.includes(searchTerm) ||
      contact.phone_number_1?.includes(searchTerm)
    );
  });

  if (loading) {
    return (
      <div className={`contacts ${isDarkMode ? 'dark-mode' : ''}`}>
        <div className="container">
          <div className="loading">در حال بارگذاری...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`contacts ${isDarkMode ? 'dark-mode' : ''}`}>
        <div className="container">
          <div className="error">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`contacts ${isDarkMode ? 'dark-mode' : ''}`}>
      <div className="container">
        <div className="contacts-header">
          <h2>مدیریت مخاطبین</h2>
          <button className="add-contact-btn">افزودن مخاطب جدید</button>
        </div>

        <div className="search-section">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => handleSearch(e.target.value)}
            placeholder="جستجو در مخاطبین..."
            className="search-input"
          />
        </div>

        <div className="contacts-table">
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
              {filteredContacts.map(contact => (
                <tr key={contact.id}>
                  <td>
                    <button className="details-btn">جزئیات</button>
                    <button className="edit-btn">ویرایش</button>
                    <button className="delete-btn">حذف</button>
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
      </div>
    </div>
  );
};

export default Contacts; 