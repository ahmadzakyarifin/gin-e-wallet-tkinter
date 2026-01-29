import customtkinter as ctk
from tkinter import messagebox
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from theme import Theme
except ImportError:
    from frontend.theme import Theme

class TopUpView(ctk.CTkFrame):
    def __init__(self, master, user_data, navigate_callback, topup_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.user_data = user_data
        self.navigate_callback = navigate_callback
        self.topup_callback = topup_callback
        
        self.selected_method = None
        self.method_buttons = []
        
        self.create_widgets()

    def create_widgets(self):
        # --- HEADER ---
        header = ctk.CTkFrame(self, fg_color=Theme.PRIMARY, height=80, corner_radius=0)
        header.pack(fill="x", anchor="n")
        
        ctk.CTkButton(header, text="←", font=("Arial", 24, "bold"), fg_color=Theme.WHITE, text_color=Theme.PRIMARY,
                      width=40, height=40, corner_radius=20, cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                      command=lambda: self.navigate_callback("home")).pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(header, text="Top Up Saldo", font=("Arial", 18, "bold"), text_color=Theme.WHITE).pack(side="left", padx=10)
        
        saldo = f"Rp {self.user_data.get('saldo', 0):,}".replace(",", ".")
        ctk.CTkLabel(header, text=f"Saldo: {saldo}", font=("Arial", 12), text_color="#E8F5E9").pack(side="right", padx=20)

        # --- SCROLLABLE CONTENT ---
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        self.scroll.pack(fill="both", expand=True)

        # --- INPUT NOMINAL ---
        card = ctk.CTkFrame(self.scroll, fg_color=Theme.WHITE, corner_radius=15)
        card.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(card, text="Nominal Top Up", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(20, 5))
        self.entry_nominal = ctk.CTkEntry(card, placeholder_text="Rp 0", height=50, border_width=0, 
                                          fg_color="#F0F0F0", text_color=Theme.TEXT, font=("Arial", 16, "bold"))
        self.entry_nominal.pack(fill="x", padx=20, pady=(0, 15))
        self.entry_nominal.bind("<KeyRelease>", self.format_rupiah)

        # Aksi Cepat (Quick Buttons)
        q_frame = ctk.CTkFrame(card, fg_color="transparent")
        q_frame.pack(fill="x", padx=20, pady=(0, 20))
        for amt in [50000, 100000, 200000, 500000]:
            ctk.CTkButton(q_frame, text=f"{amt//1000}k", width=60, height=35, 
                          fg_color=Theme.BTN_LIGHT, text_color=Theme.TEXT, 
                          border_width=0, cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                          command=lambda x=amt: self.set_nominal(x)).pack(side="left", padx=(0,10), expand=True, fill="x")

        # --- PILIH METODE ---
        ctk.CTkLabel(self.scroll, text="Metode Pembayaran", font=("Arial", 14, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(0, 10))
        
        methods = [
            {"name": "BCA Virtual Account", "icon": "🔵", "desc": "Cek Otomatis"},
            {"name": "BNI Virtual Account", "icon": "🟠", "desc": "Cek Otomatis"},
            {"name": "Mandiri VA", "icon": "🟡", "desc": "Cek Otomatis"},
            {"name": "Indomaret", "icon": "🏪", "desc": "Bayar di Kasir"},
            {"name": "Alfamart / Alfamidi", "icon": "🔴", "desc": "Bayar di Kasir"},
        ]
        for m in methods:
            self.create_method_item(m)

        # --- TOMBOL SUBMIT ---
        ctk.CTkButton(self.scroll, text="LANJUTKAN TOP UP", font=Theme.F_BTN,
                      fg_color=Theme.PRIMARY, height=50, corner_radius=10, 
                      cursor="hand2", hover_color=Theme.BTN_HOVER_DARK,
                      command=self.on_submit).pack(fill="x", padx=20, pady=30)

    def create_method_item(self, method):
        frame = ctk.CTkFrame(self.scroll, fg_color=Theme.WHITE, corner_radius=12, border_width=2, border_color="#E0E0E0")
        frame.pack(fill="x", padx=20, pady=5)
        frame.configure(cursor="hand2")

        ctk.CTkLabel(frame, text=method['icon'], font=("Arial", 24)).pack(side="left", padx=15, pady=15)
        
        info = ctk.CTkFrame(frame, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(info, text=method['name'], font=("Arial", 13, "bold"), text_color=Theme.TEXT).pack(anchor="w")
        ctk.CTkLabel(info, text=method['desc'], font=("Arial", 11), text_color=Theme.MUTED).pack(anchor="w")

        def on_click(e):
            self.selected_method = method['name']
            for btn in self.method_buttons: btn.configure(border_color="#E0E0E0")
            frame.configure(border_color=Theme.PRIMARY)
        
        frame.bind("<Button-1>", on_click)
        for child in frame.winfo_children():
            child.bind("<Button-1>", on_click)
            if isinstance(child, ctk.CTkFrame):
                for sub in child.winfo_children(): sub.bind("<Button-1>", on_click)
        
        self.method_buttons.append(frame)

    def format_rupiah(self, event):
        val = self.entry_nominal.get().replace(".", "")
        if val.isdigit():
            self.entry_nominal.delete(0, "end")
            self.entry_nominal.insert(0, f"{int(val):,}".replace(",", "."))

    def set_nominal(self, x):
        self.entry_nominal.delete(0, "end")
        self.entry_nominal.insert(0, f"{x:,}".replace(",", "."))

    def on_submit(self):
        val = self.entry_nominal.get().replace(".", "")
        
        # Validasi sederhana (Angka & Minimal)
        if not val.isdigit() or int(val) < 1000:
            messagebox.showwarning("Error", "Minimal Top Up Rp 1.000")
            return
            
        if not self.selected_method:
            messagebox.showwarning("Error", "Silakan pilih metode pembayaran")
            return
            
        # Panggil Callback ke Main -> Service
        self.topup_callback(int(val), self.selected_method)