import customtkinter as ctk
from tkinter import messagebox
from vote import VotingSystem
from admin import AdminSystem

class LoginPage:
    def __init__(self, root, data_kandidat):
        self.root = root
        self.data_kandidat = data_kandidat
        self.root.title("Login")
        self.root.geometry("400x300")
        
        # Ubah tema menggunakan CustomTkinter
        ctk.set_appearance_mode("dark")  # Dark mode
        ctk.set_default_color_theme("blue")  # Tema biru

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

              # Membuat frame utama dengan styling
        frame = ctk.CTkFrame(self.root, width=300, height=250)
        frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Label judul
        label_title = ctk.CTkLabel(
            frame, text="Login", font=("Arial", 18, "bold")
        )
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Label dan entry untuk username
        label_username = ctk.CTkLabel(
            frame, text="Username:", font=("Arial", 12)
        )
        label_username.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_username = ctk.CTkEntry(frame, font=("Arial", 12), width=200)
        self.entry_username.grid(row=1, column=1, padx=10, pady=5)

        # Label dan entry untuk password
        label_password = ctk.CTkLabel(
            frame, text="Password:", font=("Arial", 12)
        )
        label_password.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_password = ctk.CTkEntry(frame, show="*", font=("Arial", 12), width=200)
        self.entry_password.grid(row=2, column=1, padx=10, pady=5)

        # Tombol login dengan desain modern
        button_login = ctk.CTkButton(
            frame,
            text="Login",
            font=("Arial", 12, "bold"),
            command=self.login,
            width=200
        )
        button_login.grid(row=3, column=0, columnspan=2, pady=(20, 10))

    def open_admin_page(self):
            # Bersihkan window
            AdminSystem(self.root, self.setup_ui, self.data_kandidat)