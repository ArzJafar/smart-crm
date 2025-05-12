
import React from 'react';
import { useTheme } from '../../context/ThemeContext';

const educationImg = process.env.PUBLIC_URL + '/images/Logos/Education.png';

const Footer = ({ version }) => {
  const { isDarkMode } = useTheme();

  return (
    <>
      <div
        className={`container-fluid text-light py-4 footer${isDarkMode ? ' dark-mode' : ''}`}
        style={{ backgroundColor: '#666666', marginBottom: 0, paddingBottom: 0 }}
      >
        <div className="row">
          <div className="col-12 text-center">
            <h3>Chekad CRM</h3>
          </div>

          <div className="container d-flex flex-column align-items-center">
            <div className="row d-flex justify-content-center align-items-center w-100">
              <div
                className="col-md-3 text-md-end text-center d-flex flex-column align-items-center"
                style={{ marginBottom: 40 }}
              >
                <img
                  height="150px"
                  src={educationImg}
                  alt="Education"
                  style={{ display: 'block', marginBottom: '12px' }}
                />
                <a
                  target="_blank"
                  rel="noopener noreferrer"
                  href="https://chekad.com/education/"
                  className="btn btn-dark mt-2"
                  style={{ textAlign: 'center' }}
                >
                  سایت آموزشی چکاد
                </a>
              </div>
              <div className="col-md-3 text-md-start text-center">
                <h5 style={{ textAlign: 'right' }} className="mb-3">
                  آخرین مقالات
                </h5>
                <hr style={{ height: 4 }} />
                <ul style={{ textAlign: 'right' }} className="list-unstyled">
                  <li>
                    <a
                      style={{ textDecoration: 'none' }}
                      target="_blank"
                      rel="noopener noreferrer"
                      href="https://chekad.com/education/articles/managing-time/"
                      className="text-white"
                    >
                      مدیریت زمان
                    </a>
                  </li>
                  <hr style={{ margin: '8px auto' }} />
                  <li style={{ textAlign: 'right' }}>
                    <a
                      style={{
                        textDecoration: 'none',
                        direction: 'rtl',
                        display: 'inline-block',
                      }}
                      target="_blank"
                      rel="noopener noreferrer"
                      href="https://chekad.com/education/articles/work-smarter-not-harder/"
                      className="text-white"
                    >
                      ۱۶ رهنمود برای آنکه هوشمندانه‌تر کار کنید، نه سخت‌تر!
                    </a>
                  </li>
                  <hr style={{ margin: '8px auto' }} />
                  <li>
                    <a
                      style={{ textDecoration: 'none' }}
                      target="_blank"
                      rel="noopener noreferrer"
                      href="https://chekad.com/education/google-services/google-sheets/sheets-or-excel/"
                      className="text-white"
                    >
                      تفاوت های گوگل شیت با اکسل
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        style={{ backgroundColor: '#5b5b5b', marginTop: 0, paddingTop: 0 }}
        className={`container-fluid text-light py-1 footer after-footer${isDarkMode ? ' dark-mode' : ''}`}
      >
        <div className="col-12 text-center mt-3">
          <p style={{ fontSize: 10 }}>&copy; Created by Chekad IT Team</p>
          <p style={{ fontSize: 10 }}>{version}</p>
        </div>
      </div>
    </>
  );
};

export default Footer;
