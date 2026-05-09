import React from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut, User } from 'lucide-react';

const Navbar = () => {
  const navigate = useNavigate();
  const username = localStorage.getItem('username') || 'Người dùng';

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    <nav className="top-navbar">
      <div className="navbar-brand">
        <span className="navbar-logo">⚡</span>
        <span className="navbar-title">CMS</span>
      </div>

      <div className="navbar-user">
        <div className="navbar-greeting">
          <div className="user-avatar-sm">
            <User size={16} />
          </div>
          <span>
            Xin chào, <strong>{username}</strong>
          </span>
        </div>

        <button
          id="logout-btn"
          className="btn btn-logout"
          onClick={handleLogout}
          title="Đăng xuất"
        >
          <LogOut size={16} />
          Đăng xuất
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
