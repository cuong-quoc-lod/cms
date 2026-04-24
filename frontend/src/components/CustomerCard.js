import React from 'react';
import { Edit2, Trash2, Mail, Phone, Clock } from 'lucide-react';

const CustomerCard = ({ customer, onView, onEdit, onDelete }) => {
  const getInitials = (name) => {
    return name ? name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() : 'KH';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('vi-VN');
  };

  return (
    <div className="customer-card animate-fade-in" onClick={() => onView(customer)}>
      <div className="card-header">
        <div className="avatar">
          {getInitials(customer.name)}
        </div>
        <div>
          <h3 style={{ fontSize: '1.125rem', color: 'var(--text-main)', marginBottom: '0.25rem' }}>
            {customer.name}
          </h3>
          <span style={{ 
            fontSize: '0.75rem', 
            padding: '0.25rem 0.5rem', 
            borderRadius: '999px',
            backgroundColor: customer.is_active ? '#dcfce7' : '#f1f5f9',
            color: customer.is_active ? '#166534' : '#475569',
            fontWeight: '500'
          }}>
            {customer.is_active ? 'Active' : 'Inactive'}
          </span>
        </div>
      </div>
      
      <div className="card-body">
        <p><Mail size={16} /> {customer.email}</p>
        <p><Phone size={16} /> {customer.phone || 'Chưa cập nhật'}</p>
        <p><Clock size={16} /> Tham gia: {formatDate(customer.created_at)}</p>
      </div>

      <div className="card-actions" onClick={(e) => e.stopPropagation()}>
        <button className="btn btn-outline" onClick={(e) => { e.stopPropagation(); onEdit(customer); }}>
          <Edit2 size={16} /> Sửa
        </button>
        <button className="btn btn-danger" onClick={(e) => { e.stopPropagation(); onDelete(customer.id); }}>
          <Trash2 size={16} /> Xóa
        </button>
      </div>
    </div>
  );
};

export default CustomerCard;
