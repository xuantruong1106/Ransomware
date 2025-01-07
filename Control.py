import socket
import threading
import json
import os
import random
import string
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # For handling images
import platform
import subprocess


class ControlServer:
    def __init__(self, host, port, log_file, update_log_callback):
        self.host = host
        self.port = port
        self.server = None
        self.update_log = update_log_callback
        self.saved_files = []

    def save_file(self, filename, content):
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        random_folder = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        save_directory = os.path.join(downloads_path, random_folder)
        os.makedirs(save_directory, exist_ok=True)
        
        file_path = os.path.join(save_directory, filename)
        with open(file_path, 'wb') as f:
            f.write(content.encode('latin1'))

        self.saved_files.append(save_directory)
        self.update_log(f"Saved file: {file_path}", "success")

    def handle_client(self, connection, address):
        self.update_log(f"Connection established from {address}", "info")
        try:
            data = connection.recv(4096)
            if not data:
                return

            message = json.loads(data.decode())
            if 'filename' in message and 'content' in message:
                self.save_file(message['filename'], message['content'])

                # Check if the file is an image (based on filename extension)
                if message['filename'].lower().endswith(('jpg', 'jpeg', 'png', 'gif')):
                    self.update_log(f"Received image file: {message['filename']}", "info")
            else:
                self.update_log(f"Data received from {address}: {message}", "info")
        except json.JSONDecodeError:
            self.update_log("Invalid JSON data received.", "error")
        finally:
            connection.close()

    def start(self):
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
        if self.server:
            self.server.close()
            self.update_log("Server stopped successfully!", "error")


class ServerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Control Server")
        self.master.geometry("600x600")

        # Load and set background image
        self.background_image = Image.open("p.png")  # Replace with your image path
        self.background_image = self.background_image.resize((600, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(master, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.server = None

        # Style customization
        self.main_color = "#111"  # Blackish gray
        self.accent_color = "#ff0000"  # Red

        # GUI Components
        self.label = tk.Label(
            master, text="Control Server", font=("Arial", 16, "bold"), fg=self.accent_color, bg=self.main_color
        )
        self.label.pack(pady=10)

        self.start_button = tk.Button(
            master, text="Start Server", command=self.start_server, bg=self.accent_color, fg="white"
        )
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(
            master, text="Stop Server", command=self.stop_server, bg=self.accent_color, fg="white"
        )
        self.stop_button.pack(pady=5)

        self.read_button = tk.Button(
            master, text="Read Files", command=self.read_files, bg=self.accent_color, fg="white"
        )
        self.read_button.pack(pady=5)

        self.log_label = tk.Label(
            master, text="Server Log", font=("Arial", 12), fg=self.accent_color, bg=self.main_color
        )
        self.log_label.pack(pady=5)

        self.log_text = tk.Text(master, height=20, width=60, bg=self.main_color, fg="white")
        self.log_text.tag_configure("info", foreground="cyan")
        self.log_text.tag_configure("success", foreground="green")
        self.log_text.tag_configure("error", foreground="red")
        self.log_text.pack(pady=10)

    def start_server(self):
        if not self.server:
            self.server = ControlServer('0.0.0.0', 12345, 'server_log.txt', self.update_log)
            threading.Thread(target=self.server.start, daemon=True).start()
            self.update_log("Server started successfully!", "success")

    def stop_server(self):
        if self.server:
            self.server.stop()
            self.server = None
            self.update_log("Server stopped successfully!", "error")

    def read_files(self):
        if self.server and self.server.saved_files:
            last_folder = self.server.saved_files[-1]
            self.open_folder(last_folder)
        else:
            messagebox.showinfo("Saved Files", "No files saved yet!")

    def open_folder(self, folder_path):
        try:
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", folder_path])
            else:
                subprocess.run(["xdg-open", folder_path])
        except Exception as e:
            self.update_log(f"Error opening folder: {e}", "error")

    def update_log(self, message, tag="info"):
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)

    def display_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((200, 200), Image.LANCZOS)  # Resize the image to fit the UI
            img = ImageTk.PhotoImage(img)

            img_label = tk.Label(self.master, image=img)
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.pack(pady=10)
        except Exception as e:
            self.update_log(f"Error displaying image: {e}", "error")


# Create the main window
root = tk.Tk()
app = ServerApp(root)
root.mainloop()
