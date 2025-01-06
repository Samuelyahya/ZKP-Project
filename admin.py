import customtkinter as ctk
from tkinter import messagebox

class AdminSystem:
    def __init__(self, root, logout_callback, data_kandidat):
        """
        Halaman Admin menggunakan CustomTkinter
        :param root: Tkinter root window
        :param logout_callback: Fungsi callback untuk logout ke halaman login
        :param data_kandidat: Objek yang menangani data kandidat (misalnya penyimpanan dan pengambilan data)
        """
        self.root = root
        self.candidate_data = data_kandidat
        self.logout_callback = logout_callback
        self.candidates = self.candidate_data.load_candidates()

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # Bersihkan window (hapus semua widget sebelumnya)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Judul halaman admin
        title = ctk.CTkLabel(self.root, text="Halaman Admin", font=("Arial", 16, "bold"))
        title.pack(pady=20)

        # Pesan selamat datang
        welcome_label = ctk.CTkLabel(self.root, text="Selamat datang di Panel Admin!", font=("Arial", 12))
        welcome_label.pack(pady=10)

        # Frame untuk menampilkan daftar kandidat
        self.candidate_frame = ctk.CTkFrame(self.root)
        self.candidate_frame.pack(pady=10, expand=True, anchor="center")

        # Membuat label untuk setiap kandidat
        self.update_candidate_list()

        # Input untuk menambahkan kandidat baru
        self.new_candidate_entry = ctk.CTkEntry(self.root, width=250)
        self.new_candidate_entry.pack(pady=5)

        # Tombol untuk menambahkan kandidat
        add_candidate_button = ctk.CTkButton(
            self.root, text="Tambah Kandidat", command=self.add_candidate
        )
        add_candidate_button.pack(pady=10)

        # Tombol untuk logout
        logout_button = ctk.CTkButton(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=20)

    def update_candidate_list(self):
        """
        Memperbarui daftar kandidat dengan label.
        """
        # Hapus label kandidat lama
        for widget in self.candidate_frame.winfo_children():
            widget.destroy()

        # Tambahkan label untuk setiap kandidat
        for candidate in self.candidates:
            candidate_label = ctk.CTkLabel(
                self.candidate_frame,
                text=candidate,
                font=("Arial", 12),
                anchor="w",
                width=200
            )
            candidate_label.pack(pady=5, padx=20, fill="x")

    def add_candidate(self):
        """
        Menambahkan kandidat baru ke daftar.
        """
        new_candidate = self.new_candidate_entry.get().strip()

        if new_candidate:
            if new_candidate not in self.candidates:
                self.candidates.append(new_candidate)
                self.candidate_data.save_candidates(self.candidates)
                self.update_candidate_list()  # Perbarui tampilan
                self.new_candidate_entry.delete(0, ctk.END)  # Bersihkan input
                messagebox.showinfo("Sukses", f"Kandidat '{new_candidate}' berhasil ditambahkan!")
            else:
                messagebox.showerror("Error", f"Kandidat '{new_candidate}' sudah ada!")
        else:
            messagebox.showerror("Error", "Nama kandidat tidak boleh kosong!")

    def logout(self):
        """
        Fungsi untuk kembali ke halaman login
        """
        if messagebox.askyesno("Logout", "Apakah Anda yakin ingin logout?"):
            for widget in self.root.winfo_children():
                widget.destroy()
            self.logout_callback()

