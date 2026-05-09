import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';

const CustomerModal = ({ isOpen, onClose, onSave, customer, mode }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    note: '',
    is_active: true
  });

  useEffect(() => {
    if (customer && mode !== 'create') {
      setFormData({
        name: customer.name || '',
        email: customer.email || '',
        phone: customer.phone || '',
        address: customer.address || '',
        note: customer.note || '',
        is_active: customer.is_active !== undefined ? customer.is_active : true
      });
    } else {
      setFormData({ name: '', email: '', phone: '', address: '', note: '', is_active: true });
    }
  }, [customer, mode]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({ 
      ...prev, 
      [name]: type === 'checkbox' ? checked : value 
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const isViewOnly = mode === 'view';

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2 style={{ fontSize: '1.5rem', color: 'var(--text-main)' }}>
            {mode === 'create' ? 'Thêm khách hàng' : mode === 'edit' ? 'Sửa khách hàng' : 'Chi tiết khách hàng'}
          </h2>
          <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)' }}>
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="name">Họ và tên</label>
            <input 
              type="text" 
              id="name" 
              name="name"
              className="input-field" 
              value={formData.name}
              onChange={handleChange}
              disabled={isViewOnly}
              required 
            />
          </div>
          <div className="input-group">
            <label htmlFor="email">Email</label>
            <input 
              type="email" 
              id="email" 
              name="email"
              className="input-field" 
              value={formData.email}
              onChange={handleChange}
              disabled={isViewOnly}
              required 
            />
          </div>
          <div className="input-group">
            <label htmlFor="phone">Số điện thoại</label>
            <input 
              type="tel" 
              id="phone" 
              name="phone"
              className="input-field" 
              value={formData.phone}
              onChange={handleChange}
              disabled={isViewOnly}
            />
          </div>
          <div className="input-group">
            <label htmlFor="address">Địa chỉ</label>
            <input 
              type="text" 
              id="address" 
              name="address"
              className="input-field" 
              value={formData.address}
              onChange={handleChange}
              disabled={isViewOnly}
            />
          </div>
          <div className="input-group">
            <label htmlFor="note">Ghi chú</label>
            <textarea 
              id="note" 
              name="note"
              className="input-field" 
              value={formData.note}
              onChange={handleChange}
              disabled={isViewOnly}
              rows="3"
            />
          </div>
          
          {mode !== 'create' && (
            <div className="input-group" style={{ marginBottom: '2rem', flexDirection: 'row', alignItems: 'center', gap: '0.5rem' }}>
              <input 
                type="checkbox" 
                id="is_active" 
                name="is_active"
                checked={formData.is_active}
                onChange={handleChange}
                disabled={isViewOnly}
                style={{ width: '1rem', height: '1rem' }}
              />
              <label htmlFor="is_active" style={{ margin: 0 }}>Tài khoản đang hoạt động (Active)</label>
            </div>
          )}

          {!isViewOnly && (
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
              <button type="button" className="btn btn-outline" onClick={onClose}>
                Hủy
              </button>
              <button type="submit" className="btn btn-primary">
                Lưu
              </button>
            </div>
          )}
          {isViewOnly && (
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
              <button type="button" className="btn btn-primary" onClick={onClose}>
                Đóng
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default CustomerModal;
