const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const getAuthHeaders = () => {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};
const handle401 = (res) => {
  if (res.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
    return true;
  }
  return false;
};
// Helper: parse error message from backend response
const parseError = async (res, fallback) => {
  try {
    const body = await res.json();
    if (body.detail) {
      // 422 validation errors come as array
      if (Array.isArray(body.detail)) {
        return body.detail.map((e) => e.msg || e.message).join(", ");
      }
      return body.detail;
    }
  } catch (_) {}
  return fallback;
};

export const api = {
  // Auth
  login: async (username, password) => {
    const res = await fetch(`${API_URL}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) throw new Error(await parseError(res, "Đăng nhập thất bại"));
    return res.json();
  },

  register: async (username, password, full_name) => {
    const res = await fetch(`${API_URL}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, full_name }),
    });
    if (!res.ok) throw new Error(await parseError(res, "Đăng ký thất bại"));
    return res.json();
  },

  // Customers
  getCustomers: async (search = "") => {
    const url = new URL(`${API_URL}/api/customer`);
    if (search) url.searchParams.append("search", search);

    const res = await fetch(url, {
      headers: { ...getAuthHeaders() },
    });
    if (res.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
      return;
    }
    if (!res.ok)
      throw new Error(await parseError(res, "Lỗi lấy danh sách khách hàng"));
    return res.json();
  },

  createCustomer: async (data) => {
    const res = await fetch(`${API_URL}/api/customer`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
      body: JSON.stringify(data),
    });
    if (handle401(res)) return;
    if (!res.ok) throw new Error(await parseError(res, "Lỗi tạo khách hàng"));
    return res.json();
  },

  updateCustomer: async (id, data) => {
    const res = await fetch(`${API_URL}/api/customer/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
      body: JSON.stringify(data),
    });
    if (handle401(res)) return;
    if (!res.ok)
      throw new Error(await parseError(res, "Lỗi cập nhật khách hàng"));
    return res.json();
  },

  deleteCustomer: async (id) => {
    const res = await fetch(`${API_URL}/api/customer/${id}`, {
      method: "DELETE",
      headers: { ...getAuthHeaders() },
    });
    if (handle401(res)) return;
    if (!res.ok) throw new Error(await parseError(res, "Lỗi xóa khách hàng"));
    return res.json();
  },
};
