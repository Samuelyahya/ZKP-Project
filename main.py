from login import LoginPage
import customtkinter as ctk
from kandidat_data import CandidateData



def main():
    root = ctk.CTk()
    data_kandidat = CandidateData()
    app = LoginPage(root, data_kandidat)  # Memulai dengan halaman login
    root.mainloop()

if __name__ == "__main__":
    main()  