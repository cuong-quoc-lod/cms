# Backend CMS

Đây là dự án Backend quản lý khách hàng sử dụng **FastAPI** và **MongoDB**.

## Yêu cầu hệ thống

- Python 3.9+
- MongoDB (đang chạy trên `localhost:27017` hoặc cập nhật đường dẫn vào `.env`)

## Cài đặt

1. Tạo Virtual Environment và kích hoạt:
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/MacOS
   source venv/bin/activate
   ```

2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

3. Sao chép và cấu hình biến môi trường:
   ```bash
   cp .env.example .env
   ```
   *Lưu ý: Mở file `.env` và đảm bảo `MONGO_URI` đang trỏ đúng vào địa chỉ MongoDB của bạn.*

## Chạy Ứng dụng

Chạy server bằng lệnh sau:
```bash
python run.py
```
Hoặc dùng uvicorn trực tiếp:
```bash
uvicorn src.main:app --reload
```

Server sẽ chạy ở địa chỉ: `http://localhost:8000`

## Tài liệu API (Swagger UI)

Truy cập: **http://localhost:8000/docs**

### Hướng dẫn sử dụng API

Hệ thống yêu cầu xác thực bằng JWT (JSON Web Token) cho các API quản lý khách hàng. 

1. **Đăng ký tài khoản (Tạo User)**
   - API: `POST /api/auth/register`
   - Payload:
     ```json
     {
       "username": "admin123",
       "password": "Password123!",
       "full_name": "Admin System"
     }
     ```
   - Kết quả: Trả về một `access_token`.

2. **Đăng nhập**
   - API: `POST /api/auth/login`
   - Nếu bạn đã có tài khoản, đăng nhập với `username` và `password` để lấy `access_token`.

3. **Xác thực (Authorize) trong Swagger**
   - Nhấn vào nút **Authorize** có hình ổ khóa ở góc phải trên cùng hoặc ổ khóa cạnh mỗi API.
   - Nhập `access_token` bạn vừa nhận được ở trên (không cần điền chữ "Bearer " đằng trước, Swagger sẽ tự động thêm vào).
   - Nhấn **Authorize** để lưu Token.

4. **Quản lý khách hàng**
   Sau khi đã gắn token, bạn có thể gọi toàn bộ các API của `Customer` như bình thường:
   - `GET /api/customer`: Lấy danh sách khách hàng (có phân trang và search).
   - `POST /api/customer`: Thêm khách hàng mới.
   - `PUT /api/customer/{id}`: Cập nhật khách hàng.
   - `DELETE /api/customer/{id}`: Xóa khách hàng (Soft delete).

## Lỗi Thường Gặp

- `pymongo.errors.ServerSelectionTimeoutError: [WinError 10061]`: Lỗi này xảy ra khi MongoDB chưa được khởi động. Hãy đảm bảo Database đã chạy trước khi sử dụng các API thao tác dữ liệu.
