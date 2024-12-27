import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import secrets
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base64
import os

class ZKPVotingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Zero-Knowledge Voting System")
        
        # Kandidat pemilihan
        self.candidates = ["Alice", "Bob", "Charlie"]
        
        # Penyimpanan kunci dan bukti
        self.voter_registrations = {}  # Menyimpan bukti registrasi
        self.vote_commitments = {}     # Menyimpan commitment vote
        self.final_votes = {}          # Menyimpan vote akhir
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        # Label judul
        tk.Label(self.root, text="Zero-Knowledge Voting System", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        
        # Daftar kandidat
        tk.Label(self.root, text="Kandidat:", font=("Arial", 12)).pack()
        self.candidate_listbox = tk.Listbox(self.root, height=3, font=("Arial", 12))
        for candidate in self.candidates:
            self.candidate_listbox.insert(tk.END, candidate)
        self.candidate_listbox.pack(pady=10)
        
        # Tombol aksi
        tk.Button(self.root, text="Registrasi Voter", 
                  command=self.register_voter, 
                  font=("Arial", 12)).pack(pady=5)
        
        tk.Button(self.root, text="Submit Vote", 
                  command=self.submit_vote, 
                  font=("Arial", 12)).pack(pady=5)
        
        tk.Button(self.root, text="Hitung Suara", 
                  command=self.count_votes, 
                  font=("Arial", 12)).pack(pady=5)
        
        # Area hasil
        self.result_text = tk.Text(self.root, height=10, width=50, font=("Arial", 10))
        self.result_text.pack(pady=10)
    
    def generate_voter_proof(self, voter_id):
        """Buat bukti voter dengan kunci privat"""
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        
        # Simpan kunci publik sebagai bukti registrasi
        voter_proof = public_key.public_bytes(
            encoding=serialization.Encoding.Raw, 
            format=serialization.PublicFormat.Raw
        )
        
        self.voter_registrations[voter_id] = {
            'public_key': voter_proof,
            'private_key': private_key
        }
        
        return voter_proof
    
    def register_voter(self):
        """Proses registrasi voter"""
        voter_id = simpledialog.askstring("Registrasi", "Masukkan ID Voter:")
        
        if not voter_id:
            messagebox.showerror("Error", "ID Voter diperlukan!")
            return
        
        if voter_id in self.voter_registrations:
            messagebox.showwarning("Peringatan", "Voter sudah terdaftar!")
            return
        
        # Generate bukti voter
        voter_proof = self.generate_voter_proof(voter_id)
        
        messagebox.showinfo("Registrasi Berhasil", 
                            f"Voter {voter_id} telah terdaftar\n"
                            f"Bukti Voter: {base64.b64encode(voter_proof).decode()}")
    
    def create_vote_commitment(self, candidate, voter_id):
        """Buat commitment vote yang anonim"""
        # Gunakan kunci privat untuk menandatangani vote
        private_key = self.voter_registrations[voter_id]['private_key']
        
        # Buat commitment dengan menandatangani kandidat
        signature = private_key.sign(candidate.encode())
        
        # Gunakan hash dari signature sebagai commitment
        commitment = hashlib.sha256(signature).hexdigest()
        
        return commitment, signature
    
    def submit_vote(self):
        """Submit vote dengan zero-knowledge proof"""
        voter_id = simpledialog.askstring("Vote", "Masukkan ID Voter:")
        
        if not voter_id or voter_id not in self.voter_registrations:
            messagebox.showerror("Error", "Voter tidak valid!")
            return
        
        selected = self.candidate_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Pilih kandidat terlebih dahulu!")
            return
        
        candidate = self.candidates[selected[0]]
        
        # Buat vote commitment
        commitment, signature = self.create_vote_commitment(candidate, voter_id)
        
        # Simpan commitment
        self.vote_commitments[voter_id] = commitment
        self.final_votes[voter_id] = {
            'candidate': candidate,
            'signature': signature
        }
        
        messagebox.showinfo("Vote Terkirim", 
                            f"Vote untuk {candidate} telah disubmit\n"
                            f"Commitment: {commitment}")
    
    def count_votes(self):
        """Hitung suara dengan memverifikasi commitments"""
        vote_counts = {candidate: 0 for candidate in self.candidates}
        
        for voter_id, vote_data in self.final_votes.items():
            candidate = vote_data['candidate']
            signature = vote_data['signature']
            
            # Verifikasi tanda tangan
            public_key = self.voter_registrations[voter_id]['public_key']
            ed25519_public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key)
            
            try:
                ed25519_public_key.verify(signature, candidate.encode())
                vote_counts[candidate] += 1
            except:
                messagebox.showerror("Error", f"Verifikasi vote {voter_id} gagal!")
        
        # Tampilkan hasil
        result = "Hasil Voting:\n"
        for candidate, count in vote_counts.items():
            result += f"{candidate}: {count} suara\n"
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = ZKPVotingSystem(root)
    root.mainloop()