import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useTheme } from './context/ThemeContext';
import './styles/global.css';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Home from './components/pages/Home/Home';
import Profile from './components/pages/auth/Profile';
import Login from './components/pages/auth/Login';
import Logout from './components/pages/auth/Logout';
import NotFound from './components/pages/common/NotFound';
import Dashboard from './components/pages/dashboard/Dashboard';
import Contacts from './components/pages/management/Contacts';
import HR from './components/pages/hr/HR';
import ProductionFiles from './components/pages/management/ProductionFiles';

const App = () => {
  const { isDarkMode } = useTheme();

  return (
    <Router>
      <div className={`app ${isDarkMode ? 'dark-mode' : ''}`}>
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/login" element={<Login />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="*" element={<NotFound />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/contacts" element={<Contacts />} />
            <Route path="/hr" element={<HR />} />
            <Route path="/production-files" element={<ProductionFiles />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
