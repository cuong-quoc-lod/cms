import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { api } from '../utils/api';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await api.login(username, password);
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('username', data.username || username);
      navigate('/customers');
    } catch (err) {
      setError(err.message || 'Đã có lỗi xảy ra');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card animate-fade-in">
        <h2 style={{ textAlign: 'center', marginBottom: '2rem', fontSize: '1.875rem' }}>Đăng nhập</h2>
        {error && <div style={{ color: 'var(--danger)', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="username">Tên đăng nhập</label>
            <input 
              type="text" 
              id="username" 
              className="input-field" 
              placeholder="admin"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required 
            />
          </div>
          <div className="input-group" style={{ marginBottom: '2rem' }}>
            <label htmlFor="password">Mật khẩu</label>
            <input 
              type="password" 
              id="password" 
              className="input-field" 
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required 
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: '100%', marginBottom: '1rem', padding: '0.75rem' }}>
            {loading ? 'Đang xử lý...' : 'Đăng nhập'}
          </button>
        </form>
        <p style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
          Chưa có tài khoản? <Link to="/register" style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: '500' }}>Đăng ký ngay</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
