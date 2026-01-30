import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# --- 1. SETUP PATH (PENTING: Agar Python tahu lokasi folder project) ---
current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(current_dir)

# --- 2. IMPORT SERVICE & THEME (PERBAIKAN UTAMA) ---
# Hapus awalan 'frontend.' karena kita sudah ada di dalam folder tersebut
try:
    from service.wallet_service import WalletService
    from theme import Theme
except ImportError as e:
    print(f"Error Import: {e}")
    print("Pastikan nama folder adalah 'service' (bukan 'services') dan sejajar dengan main.py")
    sys.exit(1)

# --- 3. IMPORT VIEW ---
from views.login import LoginApp
from views.home import HomeView
from views.history import HistoryView
from views.profile import ProfileFrame
from views.fiturTransfer import TransferView
from views.tarikTunai import WithdrawView
from views.topup import TopUpView
from views.fiturPulsa import PulsaView
from views.fiturTokenListrik import ListrikView, TokenResultView

class MainApp:
    def __init__(self, root, token,user_data, logout_callback):
        self.root = root
        self.logout_callback = logout_callback
        self.token = token 
        self.user_data = user_data
      
        # Init Backend
        self.service = WalletService(token=self.token)
        
        self.W, self.H = 520, 930
        self.root.geometry(f"{self.W}x{self.H}")
        self.root.configure(bg=Theme.BG)

        # Container Utama
        self.container = ctk.CTkFrame(self.root, fg_color=Theme.BG)
        self.container.pack(fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(self.container, width=self.W, height=self.H, bg=Theme.BG, highlightthickness=0)
        self.active_frame = None

        self.show_page("home")

    def clear_screen(self):
        self.canvas.pack_forget()
        self.canvas.delete("all")
        if self.active_frame:
            self.active_frame.destroy()
            self.active_frame = None

    def get_user_dict(self):
        result = self.service.get_current_user_data() 

        if result:
            # Jika hasil dari service berbentuk {"data": {...}}, ambil isinya
            if isinstance(result, dict) and "data" in result:
                self.user_data = result["data"]
            else:
                self.user_data = result
            return self.user_data
        # kembalikan self.user_data lama yang didapat dari respons Login Go.
        return self.user_data

    def show_page(self, page_name):
        self.clear_screen()
        user_data = self.get_user_dict() 
    
        if page_name == "home":
            self.canvas.pack(fill="both", expand=True)
            view = HomeView(self.canvas, self.W, self.H, self.show_page, user_data)
            view.draw()

        elif page_name == "history":
            self.canvas.pack(fill="both", expand=True)
            riwayat = user_data.get("riwayat_transaksi", [])
            view = HistoryView(self.canvas, self.W, self.H, self.show_page, riwayat)
            view.draw()

        elif page_name == "profile":
            self.active_frame = ProfileFrame(
                self.container, user_data, 
                navigate_callback=None, 
                logout_callback=self.handle_logout,
                back_to_home_callback=lambda: self.show_page("home")
            )
            # Inject custom behavior edit
            orig_show_edit = self.active_frame.show_edit_page
            def wrapped_show_edit(k, t, v):
                orig_show_edit(k, t, v, self.handle_update_profile)
            self.active_frame.navigate_callback = wrapped_show_edit
            
            self.active_frame.pack(fill="both", expand=True)

        # --- FITUR TRANSAKSI ---
        elif page_name == "fitur_transfer":
            self.active_frame = TransferView(self.container, user_data, self.show_page, self.handle_transfer)
            self.active_frame.pack(fill="both", expand=True)

        elif page_name == "fitur_topup":
            self.active_frame = TopUpView(self.container, user_data, self.show_page, self.handle_topup)
            self.active_frame.pack(fill="both", expand=True)
            
        elif page_name == "fitur_tarik":
            self.active_frame = WithdrawView(self.container, user_data, self.show_page, self.handle_withdraw)
            self.active_frame.pack(fill="both", expand=True)

        elif page_name == "fitur_pulsa":
            self.active_frame = PulsaView(self.container, user_data, self.show_page, self.handle_ppob)
            self.active_frame.pack(fill="both", expand=True)

        elif page_name == "fitur_listrik":
            self.active_frame = ListrikView(self.container, user_data, self.show_page, self.handle_ppob)
            self.active_frame.pack(fill="both", expand=True)

    # --- CALLBACK HANDLERS ---
    def handle_transfer(self, nomor, nominal, catatan):
        success, msg = self.service.process_transfer(nomor, nominal, catatan)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.show_page("home")
        else:
            messagebox.showerror("Gagal", msg)

    def handle_topup(self, nominal, metode):
        success, msg = self.service.process_topup(nominal, metode)
        if success:
            messagebox.showinfo("Top Up", f"{msg}\nCek History untuk status.")
            self.show_page("home")
        else:
            messagebox.showerror("Top Up Gagal", msg)

    def handle_withdraw(self, nominal, admin, lokasi):
        # Generate kode di Client sementara
        import random, string
        code_val = "".join(random.choices(string.digits, k=6))
        
        success, msg = self.service.process_withdraw(nominal, admin, lokasi, code_val)
        if success:
            return code_val
        else:
            messagebox.showerror("Gagal", f"Tarik Tunai Gagal:\n{msg}")
            return None

    def handle_ppob(self, tipe, data):
        if tipe == "token":
            import random, string
            # Simulasi generate token listrik dummy (idealnya dari respon API)
            token_val = "".join(random.choices(string.digits, k=20))
            data['token'] = token_val 
            
            success, msg = self.service.process_ppob(tipe, data)
            if success:
                self.clear_screen()
                self.active_frame = TokenResultView(self.container, 
                                                    token_code=token_val,
                                                    amount=data['harga'],
                                                    data_transaksi=data,
                                                    back_to_home_callback=lambda: self.show_page("home"))
                self.active_frame.pack(fill="both", expand=True)
                return
            else:
                messagebox.showerror("Transaksi Gagal", msg)
                return
        
        success, msg = self.service.process_ppob(tipe, data)
        if success:
            messagebox.showinfo("Sukses", "Transaksi Berhasil")
            self.show_page("home")
        else:
            messagebox.showerror("Transaksi Gagal", msg)

    def handle_update_profile(self, key, new_val):
        success, msg = self.service.update_info(key, new_val)
        if success:
            messagebox.showinfo("Sukses", msg)
            if isinstance(self.active_frame, ProfileFrame):
                self.active_frame.user_data[key] = new_val 
                self.active_frame.refresh_ui()
        else:
            messagebox.showerror("Gagal Update", msg)

    def handle_logout(self):
        if messagebox.askyesno("Keluar", "Yakin ingin keluar?"):
            self.container.destroy()
            self.logout_callback() 

# --- APP CONTROLLER ---
class AppController:
    def __init__(self):
        ctk.set_appearance_mode("Light")
        self.root = ctk.CTk()
        self.root.title("E-SAKU App")
        self.root.geometry("520x930") 
        self.current_app = None
        
        self.show_login()

    def show_login(self):
        self.clear_root()
        self.current_app = LoginApp(self.root, on_login_success=self.show_dashboard)

    # DI FILE main.py (AppController)
    def show_dashboard(self, data): # Terima data user lengkap
        token = data.get("token")
        user_info = data.get("user") # Ambil objek user-nya
        
        self.clear_root()
        # Kirim user_info ke MainApp agar langsung bisa dipakai
        self.current_app = MainApp(self.root, token, user_info, logout_callback=self.show_login)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppController()
    app.run()