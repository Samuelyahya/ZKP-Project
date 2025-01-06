import tkinter as tk
from tkinter import messagebox
from vote import VotingSystem
from admin import AdminSystem

class LoginPage:
    def __init__(self, root, data_kandidat):
        self.root = root
        self.data_kandidat = data_kandidat
        root.title("Login")

        # Simulasi database user
        self.users = {
            "admin": {"password": "admin123", "role": "admin"},
            "user1": {"password": "password123", "role": "user"},
            "user2": {"password": "user456", "role": "user"}
        }


        # # Setup UI
        self.setup_ui()


    # Fungsi untuk memverifikasi login
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Validasi username dan password
        if username in self.users and self.users[username]["password"] == password:
            role = self.users[username]["role"]  # Dapatkan role pengguna
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")

            if role == "admin":
                self.open_admin_page()  # Buka halaman admin
            elif role == "user":
                VotingSystem(self.root, self.data_kandidat)  # Buka halaman voting untuk user
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!")

    def setup_ui(self):

        # Membuat frame untuk form login
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Label dan entry untuk username
        label_username = tk.Label(frame, text="Username:")
        label_username.grid(row=0, column=0, padx=5, pady=5)
        self.entry_username = tk.Entry(frame)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        # Label dan entry untuk password
        label_password = tk.Label(frame, text="Password:")
        label_password.grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = tk.Entry(frame, show="*")  # Gunakan '*' untuk menyembunyikan input
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        # Tombol login
        button_login = tk.Button(frame, text="Login", command=self.login)
        button_login.grid(row=2, columnspan=2, pady=10)

    def open_admin_page(self):
            # Bersihkan window
            AdminSystem(self.root, self.setup_ui, self.data_kandidat)