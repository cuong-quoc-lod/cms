import React, { useState, useEffect, useCallback } from 'react';
import { Search, Plus } from 'lucide-react';
import CustomerCard from '../components/CustomerCard';
import CustomerModal from '../components/CustomerModal';
import Navbar from '../components/Navbar';
import { api } from '../utils/api';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState('create'); // 'create', 'edit', 'view'
  const [selectedCustomer, setSelectedCustomer] = useState(null);

  const fetchCustomers = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.getCustomers(searchTerm);
      setCustomers(data.customers || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [searchTerm]);

  useEffect(() => {
    // Debounce search slightly
    const delayDebounceFn = setTimeout(() => {
      fetchCustomers();
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [fetchCustomers]);

  const handleCreate = () => {
    setSelectedCustomer(null);
    setModalMode('create');
    setIsModalOpen(true);
  };

  const handleEdit = (customer) => {
    setSelectedCustomer(customer);
    setModalMode('edit');
    setIsModalOpen(true);
  };

  const handleView = (customer) => {
    setSelectedCustomer(customer);
    setModalMode('view');
    setIsModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa khách hàng này?')) {
      try {
        await api.deleteCustomer(id);
        fetchCustomers();
      } catch (err) {
        alert(err.message);
      }
    }
  };

  const handleSaveModal = async (formData) => {
    try {
      if (modalMode === 'create') {
        await api.createCustomer(formData);
      } else if (modalMode === 'edit') {
        await api.updateCustomer(selectedCustomer.id, formData);
      }
      setIsModalOpen(false);
      fetchCustomers();
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <>
      <Navbar />
      <div className="page-wrapper">
      <div className="dashboard-layout">
      <div className="header">
        <h1 style={{ fontSize: '2rem', color: 'var(--text-main)' }}>Quản lý Khách hàng</h1>
        
        <div style={{ display: 'flex', gap: '1rem', flex: 1, justifyContent: 'flex-end', flexWrap: 'wrap' }}>
          <div className="search-bar">
            <Search size={20} />
            <input 
              type="text" 
              placeholder="Tìm kiếm khách hàng..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field"
            />
          </div>
          
          <button className="btn btn-primary" onClick={handleCreate}>
            <Plus size={20} /> Tạo khách hàng
          </button>
        </div>
      </div>

      {error && <div style={{ color: 'var(--danger)', marginBottom: '1rem' }}>{error}</div>}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>Đang tải dữ liệu...</div>
      ) : (
        <div className="customer-grid">
          {customers.length > 0 ? (
            customers.map(customer => (
              <CustomerCard 
                key={customer.id} 
                customer={customer} 
                onView={handleView}
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            ))
          ) : (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
              Không tìm thấy khách hàng nào.
            </div>
          )}
        </div>
      )}

      <CustomerModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleSaveModal}
        customer={selectedCustomer}
        mode={modalMode}
      />
    </div>
      </div>
    </>
  );
};

export default CustomerList;
