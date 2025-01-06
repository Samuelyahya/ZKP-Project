from login import LoginPage
import tkinter as tk
from kandidat_data import CandidateData



def main():
    root = tk.Tk()
    data_kandidat = CandidateData()
    app = LoginPage(root, data_kandidat)  # Memulai dengan halaman login
    root.mainloop()

if __name__ == "__main__":
    main()  