# README

## Mô tả dự án
Đây là một dự án gồm hai phần chính: **server** và **client**. Mục tiêu của dự án là thực hiện giao tiếp giữa client và server để xử lý dữ liệu.

## Cấu trúc thư mục
```
├── server
│   ├── ControlServer.py
│   ├── background.jpg
│   ├── e.jpg
│   ├── p.png
│   ├── server.py
│   ├── server_log.txt
│
├── client
│   ├── client
│   ├── client.py
│   ├── giaima.py
│   ├── giaodien.txt
```

## Mô tả các tệp tin
### **Server**
- `ControlServer.py`: Mã nguồn để điều khiển hoạt động của server.
- `background.jpg`: Ảnh nền có thể được sử dụng trong giao diện hoặc mục đích khác.
- `e.jpg`: Một tệp hình ảnh.
- `p.png`: Một tệp hình ảnh.
- `server.py`: Mã nguồn chính của server, xử lý yêu cầu từ client.
- `server_log.txt`: Tệp nhật ký ghi lại hoạt động của server.

### **Client**
- `client`: Một tệp hoặc thư mục liên quan đến client (cần làm rõ thêm).
- `client.py`: Mã nguồn chính của client, gửi yêu cầu đến server.
- `giaima.py`: Xử lý giải mã dữ liệu từ server.
- `giaodien.txt`: Có thể chứa thông tin giao diện hoặc cấu hình.

## Hướng dẫn sử dụng
### 1. **Chạy trên máy ảo Ubuntu**
- Truy cập thư mục `Documents` và tạo thư mục `container-code`.
- Tiến hành chạy server và client theo hướng dẫn bên dưới.

### 2. **Chạy Server**
Mở terminal và chạy lệnh sau trong thư mục `server`:
```bash
python server.py
```

### 3. **Chạy Client**
Mở terminal và chạy lệnh sau trong thư mục `client`:
```bash
python client.py
```

### 4. **Quá trình mã hóa**
- Mặc định chương trình sẽ quét tại thư mục `Downloads`.
- Hãy đặt các tệp ảnh vào thư mục này để quá trình mã hóa diễn ra.

### 5. **Giải mã tệp tin**
- Chạy tệp `giaima.py` để tiến hành giải mã.
- Khóa giải mã được lưu trong thư mục `container-code/[ip-client]/encryption_key.txt`.
- Chọn thư mục đang chứa các tệp bị mã hóa và nhấn `Decrypt Files` để thực hiện giải mã.

## Lưu ý quan trọng
### Ransomware
Đây là mã độc, được sử dụng với mục đích nghiên cứu và học tập để phòng tránh trong môn **Bảo mật hệ thống thông tin**.

- **Xin vui lòng không sử dụng với mục đích vi phạm pháp luật.**
- **Chúng tôi hoàn toàn không chịu trách nhiệm dưới mọi hình thức.**

