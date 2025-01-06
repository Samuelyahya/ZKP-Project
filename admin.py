import tkinter as tk
from tkinter import messagebox




class AdminSystem:
    def __init__(self, root, logout_callback, data_kandidat ):
        """
        Halaman Admin
        :param root: Tkinter root window
        :param logout_callback: Fungsi callback untuk logout ke halaman login
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
        title = tk.Label(self.root, text="Halaman Admin", font=("Arial", 16))
        title.pack(pady=20)

        # Pesan selamat datang
        welcome_label = tk.Label(self.root, text="Selamat datang di Panel Admin!", font=("Arial", 12))
        welcome_label.pack(pady=10)

        # List kandidat
        self.candidate_listbox = tk.Listbox(self.root, height=10, width=30)
        self.candidate_listbox.pack(pady=10)

        # Update daftar kandidat
        self.update_candidate_list()

        # Input untuk menambahkan kandidat baru
        self.new_candidate_entry = tk.Entry(self.root, width=25)
        self.new_candidate_entry.pack(pady=5)

        # Tombol untuk menambahkan kandidat
        add_candidate_button = tk.Button(
            self.root, text="Tambah Kandidat", command=self.add_candidate
        )
        add_candidate_button.pack(pady=10)

        # Tombol untuk logout
        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=20)

    def update_candidate_list(self):
        """
        Memperbarui Listbox kandidat dengan data terbaru.
        """
        # Hapus semua item di Listbox
        self.candidate_listbox.delete(0, tk.END)

        # Tambahkan kandidat ke Listbox
        for candidate in self.candidates:
            self.candidate_listbox.insert(tk.END, candidate)

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
                self.new_candidate_entry.delete(0, tk.END)  # Bersihkan input
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
            

        
