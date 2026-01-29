import customtkinter as ctk
from tkinter import messagebox
import os
import sys

# --- 1. SETUP PATH ---
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir) # Folder 'frontend'
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# --- 2. IMPORT VALIDATOR ---
import utils.validator as validator

# --- 3. IMPORT THEME (FIX IMPORT) ---
try:
    # Coba import langsung (benar jika dijalankan dari dalam frontend)
    from theme import Theme
except ImportError:
    # Fallback
    from frontend.theme import Theme

class ListrikView(ctk.CTkFrame):
    def __init__(self, master, user_data, navigate_callback, transaction_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.user_data = user_data
        self.navigate_callback = navigate_callback
        self.transaction_callback = transaction_callback
        self.selected_package = None
        self.pkg_buttons = []
        self.create_widgets()

    def create_widgets(self):
        # HEADER 
        header = ctk.CTkFrame(self, fg_color=Theme.PRIMARY, height=80, corner_radius=0)
        header.pack(fill="x", anchor="n")
        
        ctk.CTkButton(header, text="←", font=("Arial", 24, "bold"), fg_color=Theme.WHITE, text_color=Theme.PRIMARY,
                      width=40, height=40, corner_radius=20, cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                      command=lambda: self.navigate_callback("home")).pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(header, text="Token Listrik", font=("Arial", 18, "bold"), text_color=Theme.WHITE).pack(side="left", padx=10)
        
        saldo = f"Rp {self.user_data.get('saldo', 0):,}".replace(",", ".")
        ctk.CTkLabel(header, text=f"Saldo: {saldo}", font=("Arial", 12), text_color="#E8F5E9").pack(side="right", padx=20)

        # KONTEN SCROLL
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        self.scroll.pack(fill="both", expand=True)

        # KARTU INPUT
        card = ctk.CTkFrame(self.scroll, fg_color=Theme.WHITE, corner_radius=15)
        card.pack(fill="x", padx=20, pady=20)

        # Input ID Pelanggan
        ctk.CTkLabel(card, text="ID Pelanggan / No. Meter", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(20, 5))
        self.entry_meter = ctk.CTkEntry(card, placeholder_text="Masukkan Nomor Meter", height=50, border_width=0, 
                                        fg_color="#F0F0F0", text_color=Theme.TEXT, font=("Arial", 16, "bold"))
        self.entry_meter.pack(fill="x", padx=20, pady=(0, 15))

        # Paket
        ctk.CTkLabel(card, text="Pilih Nominal Token", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(10, 5))
        
        packages = [
            {"nominal": 20000, "harga": 22500},
            {"nominal": 50000, "harga": 52500},
            {"nominal": 100000, "harga": 102500},
            {"nominal": 200000, "harga": 202500},
            {"nominal": 500000, "harga": 502500}
        ]
        
        for pkg in packages:
            self.create_pkg_item(card, pkg)

        # AKSI TOMBOL
        ctk.CTkButton(self.scroll, text="BELI TOKEN", font=Theme.F_BTN,
                      fg_color=Theme.PRIMARY, height=50, corner_radius=10, 
                      cursor="hand2", hover_color=Theme.BTN_HOVER_DARK,
                      command=self.on_submit).pack(fill="x", padx=20, pady=30)

    def create_pkg_item(self, parent, pkg):
        frame = ctk.CTkFrame(parent, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=10)
        frame.pack(fill="x", padx=20, pady=5)
        frame.configure(cursor="hand2")
        
        ctk.CTkLabel(frame, text=f"Token {pkg['nominal']:,}".replace(",", "."), 
                     font=("Arial", 14, "bold")).pack(side="left", padx=15, pady=15)
        
        ctk.CTkLabel(frame, text=f"Rp {pkg['harga']:,}".replace(",", "."), 
                     font=("Arial", 14, "bold"), text_color=Theme.PRIMARY).pack(side="right", padx=15)
        
        def on_click(e):
            self.selected_package = pkg
            for btn in self.pkg_buttons: 
                btn.configure(border_color="#E0E0E0", fg_color=Theme.WHITE)
            frame.configure(border_color=Theme.PRIMARY, fg_color="#E8F5E9")
            
        def on_enter(e):
            if self.selected_package != pkg:
                frame.configure(border_color=Theme.PRIMARY)
        def on_leave(e):
            if self.selected_package != pkg:
                frame.configure(border_color="#E0E0E0")

        frame.bind("<Button-1>", on_click)
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)

        for c in frame.winfo_children(): 
            c.bind("<Button-1>", on_click)
            c.bind("<Enter>", on_enter)
            c.bind("<Leave>", on_leave)
        
        self.pkg_buttons.append(frame)

    # --- 3. PERBAIKAN LOGIC SUBMIT ---
    def on_submit(self):
        meter_id = self.entry_meter.get().strip()
        
        # Cek Data Kosong
        if not meter_id or not self.selected_package:
            messagebox.showwarning("Data Kurang", "Mohon isi Nomor Meter dan pilih Nominal Token.")
            return
            
        # Validasi Format PLN (Panggil Validator)
        if not validator.is_valid_pln_number(meter_id):
            messagebox.showwarning("Nomor Salah", "Nomor Meter/ID Pelanggan tidak valid!\n(Harus 11-12 digit angka)")
            return

        self.transaction_callback("token", {
            "nomor_meter": meter_id,     
            "provider": "PLN",            
            "nominal": self.selected_package['nominal'],
            "harga": self.selected_package['harga']
        })

class TokenResultView(ctk.CTkFrame):
    def __init__(self, master, token_code, amount, data_transaksi, back_to_home_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.token_code = token_code
        self.amount = amount
        self.data_transaksi = data_transaksi 
        self.back_to_home_callback = back_to_home_callback
        
        self.create_widgets()
        
    def create_widgets(self):
        # HEADER
        header_h = 120
        header = ctk.CTkFrame(self, fg_color=Theme.PRIMARY, height=header_h, corner_radius=0)
        header.pack(fill="x", anchor="n")
        
        ctk.CTkLabel(header, text="Detail Transaksi", font=("Arial", 18, "bold"), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkButton(header, text="←", width=45, height=45, corner_radius=22.5,
                      fg_color="white", text_color=Theme.PRIMARY, hover_color="#FAFAFA",
                      bg_color=Theme.PRIMARY,
                      font=("Arial", 24, "bold"), 
                      command=self.back_to_home_callback).place(x=20, y=30)

        # STATUS SUKSES
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        icon_box = ctk.CTkFrame(content_frame, fg_color=Theme.BTN_GREEN, width=60, height=60, corner_radius=30)
        icon_box.pack(pady=(10, 10))
        ctk.CTkLabel(icon_box, text="✓", font=("Arial", 30, "bold"), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(content_frame, text="Transaksi Berhasil", font=("Arial", 16, "bold"), text_color=Theme.PRIMARY).pack()
        ctk.CTkLabel(content_frame, text=f"Rp {self.amount:,}".replace(",", "."), font=("Arial", 28, "bold"), text_color=Theme.EXPENSE).pack(pady=(5, 20))
        
        # DETAIL CARD
        card = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=15)
        card.pack(fill="x", padx=20)
        
        def add_row(lbl, val, is_bold=False, is_token=False):
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=10)
            
            ctk.CTkLabel(row, text=lbl, font=("Arial", 12), text_color="#757575").pack(side="left")
            
            font_val = ("Arial", 12, "bold") if is_bold else ("Arial", 12)
            if is_token: font_val = ("Arial", 14, "bold")
            
            txt_val = ctk.CTkLabel(row, text=val, font=font_val, text_color=Theme.TEXT)
            txt_val.pack(side="right")

        add_row("Judul", "Token Listrik")
        meter_val = self.data_transaksi.get('nomor_meter') or self.data_transaksi.get('meter') or '-'
        add_row("No. Meter", meter_val)
        add_row("Nama Pelanggan", "USER E-WALLET")
        add_row("Tarif/Daya", "R1/1300VA")    
        
        # DIVIDER
        ctk.CTkFrame(card, height=1, fg_color="#F0F0F0").pack(fill="x", padx=15, pady=5)

        # TOKEN DISPLAY
        raw_token = self.token_code
        if raw_token:
            fmt_token = " ".join([raw_token[i:i+4] for i in range(0, len(raw_token), 4)])
            
            token_frame = ctk.CTkFrame(card, fg_color="#E8F5E9", corner_radius=8)
            token_frame.pack(fill="x", padx=15, pady=10)
            
            ctk.CTkLabel(token_frame, text="Token Listrik (Stroom)", font=("Arial", 11), text_color=Theme.PRIMARY).pack(pady=(10, 0))
            ctk.CTkLabel(token_frame, text=fmt_token, font=("Arial", 18, "bold"), text_color=Theme.TEXT).pack(pady=(5, 10))
    
            btn_copy = ctk.CTkButton(token_frame, text="Salin Token", height=30, width=100, 
                                     fg_color="white", text_color=Theme.PRIMARY, border_width=1, border_color=Theme.PRIMARY,
                                     font=("Arial", 11, "bold"), hover_color="#F1F8E9",
                                     command=lambda: self.salin_token(fmt_token))
            btn_copy.pack(pady=(0, 15))
        
        add_row("Waktu", "21 Jan 2026 18:45") 
        add_row("ID Transaksi", f"TRX-{self.data_transaksi.get('trx_id', '0001')}")

        ctk.CTkButton(self, text="SELESAI", font=Theme.F_BTN, fg_color=Theme.PRIMARY, height=50, corner_radius=25,
                      hover_color=Theme.BTN_HOVER,
                      command=self.back_to_home_callback).pack(side="bottom", fill="x", padx=30, pady=30)

    def salin_token(self, txt):
        self.master.clipboard_clear()
        self.master.clipboard_append(txt)
        messagebox.showinfo("Disalin", "Token berhasil disalin!")