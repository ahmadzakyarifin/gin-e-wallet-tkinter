import customtkinter as ctk
from tkinter import messagebox
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import utils.validator as validator

try:
    from frontend.theme import Theme
except ImportError:
    class Theme:
        BG = "#F5F5F5"
        WHITE = "#FFFFFF"
        PRIMARY = "#05B048"
        TEXT = "#333333"
        BTN_GREEN = "#05B048"
        BTN_HOVER = "#008e36"
        F_HEAD = ("Arial", 16, "bold")
        F_BODY = ("Arial", 12)
        F_BTN = ("Arial", 12, "bold")

class PulsaView(ctk.CTkFrame):
    def __init__(self, master, user_data, navigate_callback, transaction_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.user_data = user_data
        self.navigate_callback = navigate_callback
        self.transaction_callback = transaction_callback
        self.selected_operator = None
        self.selected_package = None
        self.op_buttons = []
        self.pkg_buttons = []
        self.create_widgets()

    def create_widgets(self):
        # 1. HEADER STANDAR
        header = ctk.CTkFrame(self, fg_color=Theme.PRIMARY, height=80, corner_radius=0)
        header.pack(fill="x", anchor="n")
        
        ctk.CTkButton(header, text="←", font=("Arial", 24, "bold"), fg_color=Theme.WHITE, text_color=Theme.PRIMARY,
                      width=40, height=40, corner_radius=20, cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                      command=lambda: self.navigate_callback("home")).pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(header, text="Isi Pulsa", font=("Arial", 18, "bold"), text_color=Theme.WHITE).pack(side="left", padx=10)
        
        saldo = f"Rp {self.user_data.get('saldo', 0):,}".replace(",", ".")
        ctk.CTkLabel(header, text=f"Saldo: {saldo}", font=("Arial", 12), text_color="#E8F5E9").pack(side="right", padx=20)

        # 2. KONTEN SCROLL
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        self.scroll.pack(fill="both", expand=True)

        # 3. KARTU INPUT
        card = ctk.CTkFrame(self.scroll, fg_color=Theme.WHITE, corner_radius=15)
        card.pack(fill="x", padx=20, pady=20)

        # Input Nomor
        ctk.CTkLabel(card, text="Nomor HP", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(20, 5))
        self.entry_nomor = ctk.CTkEntry(card, placeholder_text="08xx...", height=50, border_width=0, 
                                        fg_color="#F0F0F0", text_color=Theme.TEXT, font=("Arial", 16, "bold"))
        self.entry_nomor.pack(fill="x", padx=20, pady=(0, 15))

        # Operator
        ctk.CTkLabel(card, text="Pilih Operator", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(0, 5))
        op_frame = ctk.CTkFrame(card, fg_color="transparent")
        op_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ops = ["Telkomsel", "Indosat", "XL", "Tri"]
        for op in ops:
            btn = ctk.CTkButton(op_frame, text=op, width=60, height=40, 
                                fg_color="#F0F0F0", text_color="#666", cursor="hand2", hover_color=Theme.BTN_HOVER_LIGHT,
                                command=lambda x=op: self.select_op(x))
            btn.pack(side="left", padx=(0,5), expand=True, fill="x")
            self.op_buttons.append(btn)

        # Paket
        ctk.CTkLabel(card, text="Pilih Nominal", font=("Arial", 12, "bold"), text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=(10, 5))
        
        packages = [
            {"nominal": 5000, "harga": 6500},
            {"nominal": 10000, "harga": 11500},
            {"nominal": 20000, "harga": 21500},
            {"nominal": 50000, "harga": 51500},
            {"nominal": 100000, "harga": 101500}
        ]
        
        for pkg in packages:
            self.create_pkg_item(card, pkg)

        # 4. AKSI TOMBOL
        ctk.CTkButton(self.scroll, text="BELI PULSA", font=Theme.F_BTN,
                      fg_color=Theme.PRIMARY, height=50, corner_radius=10, 
                      cursor="hand2", hover_color=Theme.BTN_HOVER_DARK,
                      command=self.on_submit).pack(fill="x", padx=20, pady=30)

    def select_op(self, name):
        self.selected_operator = name
        for btn in self.op_buttons:
            if btn.cget("text") == name:
                btn.configure(fg_color=Theme.PRIMARY, text_color="white")
            else:
                btn.configure(fg_color="#F0F0F0", text_color="#666")

    def create_pkg_item(self, parent, pkg):
        frame = ctk.CTkFrame(parent, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=10)
        frame.pack(fill="x", padx=20, pady=5)
        frame.configure(cursor="hand2")
        
        ctk.CTkLabel(frame, text=f"Pulsa {pkg['nominal']:,}".replace(",", "."), 
                     font=("Arial", 14, "bold")).pack(side="left", padx=15, pady=15)
        
        ctk.CTkLabel(frame, text=f"Rp {pkg['harga']:,}".replace(",", "."), 
                     font=("Arial", 14, "bold"), text_color=Theme.PRIMARY).pack(side="right", padx=15)
        
        def on_click(e):
            self.selected_package = pkg
            for btn in self.pkg_buttons: 
                btn.configure(border_color="#E0E0E0", fg_color=Theme.WHITE)
            frame.configure(border_color=Theme.PRIMARY, fg_color="#E8F5E9")
            
        # Hover
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

    def on_submit(self):
        nomor_hp = self.entry_nomor.get().strip()
        
    
        if not nomor_hp or not self.selected_operator or not self.selected_package:
            messagebox.showwarning("Data Kurang", "Mohon lengkapi Nomor HP, Operator, dan Paket.")
            return
            
     
        if not validator.is_valid_phone(nomor_hp):
            messagebox.showwarning("Nomor Salah", "Format Nomor HP tidak valid!\n(Harus angka, awalan 08, 10-13 digit)")
            return
        
    
        self.transaction_callback("pulsa", {
            "nomor_tujuan": nomor_hp,           
            "provider": self.selected_operator, 
            "nominal": self.selected_package['nominal'],
            "harga": self.selected_package['harga']
        })