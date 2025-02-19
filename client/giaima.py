import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

class DecryptorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("File Decryptor")
        self.master.geometry("500x300")
        
        # Label and Entry for decryption key
        self.key_label = tk.Label(master, text="Enter Decryption Key:")
        self.key_label.pack(pady=5)
        
        self.key_entry = tk.Entry(master, width=50, show="*")
        self.key_entry.pack(pady=5)
        
        # Button to browse directory
        self.browse_button = tk.Button(master, text="Select Folder", command=self.browse_directory)
        self.browse_button.pack(pady=5)
        
        # Button to start decryption
        self.decrypt_button = tk.Button(master, text="Decrypt Files", command=self.decrypt_all_files, bg="green", fg="white")
        self.decrypt_button.pack(pady=10)
        
        self.directory = ""
    
    def browse_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            messagebox.showinfo("Directory Selected", f"Selected Folder: {self.directory}")
    
    def find_encrypted_files(self):
        """Find all encrypted files in the selected directory."""
        encrypted_files = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".encrypted"):
                    encrypted_files.append(os.path.join(root, file))
        return encrypted_files
    
    def decrypt_file(self, file_path, fernet):
        """Decrypt a specific file."""
        try:
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()

            decrypted_data = fernet.decrypt(encrypted_data)
            
            original_file_path = file_path.replace(".encrypted", "")
            with open(original_file_path, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)
            
            os.remove(file_path)
            print(f"[✔] Decrypted: {original_file_path}")
        except Exception as e:
            print(f"[❌] Error decrypting {file_path}: {e}")
    
    def decrypt_all_files(self):
        """Decrypt all encrypted files in the selected directory."""
        if not self.directory:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return
        
        key = self.key_entry.get()
        if not key:
            messagebox.showwarning("Warning", "Please enter the decryption key!")
            return
        
        try:
            fernet = Fernet(key.encode())
            encrypted_files = self.find_encrypted_files()
            
            if not encrypted_files:
                messagebox.showinfo("Info", "No encrypted files found!")
                return
            
            for file in encrypted_files:
                self.decrypt_file(file, fernet)
            
            messagebox.showinfo("Success", "All files decrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid Key or Decryption Failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DecryptorGUI(root)
    root.mainloop()
