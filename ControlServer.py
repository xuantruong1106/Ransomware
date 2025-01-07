# import socket
# import threading
# import json
# import os
# import logging
# from colorama import init, Fore, Style
# import random
# import string

# # Initialize Colorama for colored terminal output
# init(autoreset=True)

# class ControlServer:
#     def __init__(self, host, port, log_file):
#         self.host = host
#         self.port = port
#         self.server = None
#         self.setup_logging(log_file)

#     def setup_logging(self, log_file):
#         """
#         Setup logging configuration to write logs to a file.
#         """
#         logging.basicConfig(
#             filename=log_file,
#             level=logging.INFO,
#             format='%(asctime)s - %(levelname)s - %(message)s'
#         )

#     def save_file(self, filename, content):
#         """
#         Save a file with its content to a randomly generated folder in Downloads.
#         """
#         # Define the Downloads directory
#         downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

#         # Generate a random folder name
#         random_folder = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
#         save_directory = os.path.join(downloads_path, random_folder)
#         os.makedirs(save_directory, exist_ok=True)
        
#         # Build the full file path
#         file_path = os.path.join(save_directory, filename)
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)

#         # Save the file content as binary
#         with open(file_path, 'wb') as f:
#             f.write(content.encode('latin1'))  # Encode binary data correctly

#         # Log and print success message
#         logging.info(f"Saved file: {file_path}")
#         print(f"{Fore.GREEN}Saved file: {file_path}{Style.RESET_ALL}")

#     def handle_client(self, connection, address):
#         """
#         Handle incoming client connection and process their data.
#         """
#         try:
#             data = connection.recv(4096)  # Receive up to 4KB of data
#             if not data:
#                 return

#             # Decode and parse JSON data
#             message = json.loads(data.decode())
#             if 'filename' in message and 'content' in message:
#                 # Save file if required fields exist
#                 self.save_file(message['filename'], message['content'])
#             else:
#                 # Log and print received data
#                 logging.info(f"Data received from {address}: {message}")
#                 print(f"{Fore.YELLOW}Data received: {message}{Style.RESET_ALL}")
#         except json.JSONDecodeError:
#             logging.error("Invalid JSON data received.")
#         finally:
#             connection.close()

#     def start(self):
#         """
#         Start the server to listen for incoming connections.
#         """
#         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server.bind((self.host, self.port))
#         self.server.listen(5)  # Listen for up to 5 concurrent connections
#         logging.info(f"Server listening at {self.host}:{self.port}")
#         print(f"{Fore.CYAN}Server listening at {self.host}:{self.port}{Style.RESET_ALL}")

#         try:
#             while True:
#                 # Accept new connections
#                 connection, address = self.server.accept()
#                 logging.info(f"Connection established from {address}")
#                 print(f"{Fore.GREEN}Connection established from {address}{Style.RESET_ALL}")

#                 # Handle the client in a separate thread
#                 client_thread = threading.Thread(target=self.handle_client, args=(connection, address))
#                 client_thread.start()
#         except KeyboardInterrupt:
#             logging.info("Shutting down the server.")
#             print(f"{Fore.RED}Server shut down{Style.RESET_ALL}")
#         finally:
#             self.server.close()

# if __name__ == "__main__":
#     # Configuration settings
#     HOST = '0.0.0.0'            # Listen on all interfaces
#     PORT = 12345                # Port number
#     LOG_FILE = 'server_log.txt' # Log file name

#     # Create and start the server
#     control_server = ControlServer(HOST, PORT, LOG_FILE)
#     control_server.start()
