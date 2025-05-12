import React, { useState, useEffect } from 'react';
import { useTheme } from '../../../context/ThemeContext';
import axios from 'axios';
import '../../../styles/global.css';

const ProductionFiles = () => {
  const { isDarkMode } = useTheme();
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await axios.get('/api/production-files/');
        setFiles(response.data);
      } catch (err) {
        setError('خطا در دریافت فایل‌ها');
        console.error('Error fetching files:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('/api/production-files/upload/', formData);
      // Refresh files list
      const response = await axios.get('/api/production-files/');
      setFiles(response.data);
    } catch (err) {
      setError('خطا در آپلود فایل');
      console.error('Error uploading file:', err);
    }
  };

  if (loading) return <div className="loading">در حال بارگذاری...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className={`production-files-container ${isDarkMode ? 'dark-mode' : ''}`}>
      <div className="files-header">
        <h2>مدیریت فایل‌های تولید</h2>
        <div className="upload-section">
          <input
            type="file"
            id="file-upload"
            onChange={handleFileUpload}
            style={{ display: 'none' }}
          />
          <label htmlFor="file-upload" className="btn btn-primary">
            آپلود فایل جدید
          </label>
        </div>
      </div>

      <div className="files-grid">
        {files.map(file => (
          <div key={file.id} className="file-card">
            <div className="file-icon">
              <i className={`fas fa-${getFileIcon(file.type)}`}></i>
            </div>
            <div className="file-info">
              <h4>{file.name}</h4>
              <p>حجم: {formatFileSize(file.size)}</p>
              <p>تاریخ آپلود: {formatDate(file.upload_date)}</p>
            </div>
            <div className="file-actions">
              <button className="btn btn-info">دانلود</button>
              <button className="btn btn-danger">حذف</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Helper functions
const getFileIcon = (type) => {
  if (type.includes('image')) return 'image';
  if (type.includes('pdf')) return 'file-pdf';
  if (type.includes('word')) return 'file-word';
  if (type.includes('excel')) return 'file-excel';
  return 'file';
};

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('fa-IR').format(date);
};

export default ProductionFiles; 