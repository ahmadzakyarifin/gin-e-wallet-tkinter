from tkinter import messagebox
import sys
import os
import customtkinter as ctk 

current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir) 
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


try:
   
    from theme import Theme, draw_rounded_rect, draw_icon, draw_nav_icon
except ImportError:

    from frontend.theme import Theme, draw_rounded_rect, draw_icon, draw_nav_icon

class HomeView:
    def __init__(self, canvas, width, height, on_navigate, user_data):
        self.canvas = canvas
        self.W = width
        self.H = height
        self.navigate = on_navigate 
        self.user_data = user_data # Data ini didapat dari API (wallet_service)

    def draw(self):
        self.canvas.delete("all")
        
        # Fokuskan canvas agar merespon
        try:
            self.canvas.focus_set()
        except:
            pass
        
        # --- DATA DARI API ---
        nama = self.user_data.get("username", "User") if self.user_data else "User"
        level = self.user_data.get("level", "Silver") if self.user_data else "Silver"
        saldo = self.user_data.get("saldo", 0) if self.user_data else 0
        pemasukan = self.user_data.get("limit_pemasukan", 0) if self.user_data else 0
        pengeluaran = self.user_data.get("limit_pengeluaran", 0) if self.user_data else 0
        
        # --- HEADER ---
        self.canvas.create_rectangle(0, 0, self.W, 260, fill=Theme.PRIMARY, outline="")
        
        # Avatar
        initial = nama[0].upper() if nama else "U"
        self.draw_btn_avatar(50, 70, initial, cmd=lambda: self.navigate("profile"))
        
        self.canvas.create_text(110, 70, text=f"Halo, {nama.split()[0]}", anchor="w", font=Theme.F_HEAD, fill=Theme.WHITE)
        self.canvas.create_text(110, 95, text=f"{level} Member", anchor="w", font=Theme.F_SMALL, fill="#E8F5E9")
        
        # Notif
        self.canvas.create_oval(self.W-60, 70, self.W-50, 80, fill=Theme.IC_RED, outline=Theme.WHITE, width=2)
        self.canvas.create_text(self.W-70, 75, text="Notif", anchor="e", font=Theme.F_SMALL, fill=Theme.WHITE)

        # --- KARTU UTAMA ---
        str_saldo = f"Rp {saldo:,.0f}".replace(",", ".")
        str_masuk = f"Rp {pemasukan:,.0f}".replace(",", ".")
        str_keluar = f"Rp {pengeluaran:,.0f}".replace(",", ".")
        
        # --- BATAS DARI DATA PENGGUNA ---
        limit_income = self.user_data.get("limit_pemasukan", 20_000_000)
        limit_expense = self.user_data.get("limit_pengeluaran", 20_000_000)

        # Hitung Persentase Real
        raw_pct_masuk = int((pemasukan / limit_income) * 100) if limit_income > 0 else 0
        raw_pct_keluar = int((pengeluaran / limit_expense) * 100) if limit_expense > 0 else 0
        
        persen_masuk = min(raw_pct_masuk, 100)
        persen_keluar = min(raw_pct_keluar, 100)

        draw_rounded_rect(self.canvas, 40, 145, self.W-40, 315, 25, Theme.SHADOW)
        draw_rounded_rect(self.canvas, 40, 140, self.W-40, 310, 25, Theme.WHITE)
        
        self.canvas.create_text(70, 185, text="Total Saldo Aktif", anchor="w", font=Theme.F_BODY, fill=Theme.MUTED)
        self.canvas.create_text(70, 235, text=str_saldo, anchor="w", font=Theme.F_SALDO, fill=Theme.TEXT)

        y_stats = 340
        card_w = (self.W - 100) / 2
        
        self.draw_card_stats(40, y_stats, card_w, "Pemasukan", str_masuk, Theme.INCOME, "up", persen_masuk, limit_income)
        self.draw_card_stats(40 + card_w + 20, y_stats, card_w, "Pengeluaran", str_keluar, Theme.EXPENSE, "down", persen_keluar, limit_expense)

        # --- GRID MENU ---
        self.canvas.create_text(40, 530, text="Layanan Keuangan", anchor="w", font=Theme.F_TITLE, fill=Theme.TEXT)
        
        daftar_menu = [
            ("Top Up",   Theme.BTN_GREEN,  Theme.IC_GREEN,  "plus",      "fitur_topup"),
            ("Transfer", Theme.BTN_BLUE,   Theme.IC_BLUE,   "arrow_r",   "fitur_transfer"),
            ("Tarik",    Theme.BTN_ORANGE, Theme.IC_ORANGE, "arrow_d",   "fitur_tarik"),
            ("Pulsa",    Theme.BTN_RED,    Theme.IC_RED,    "phone",     "fitur_pulsa"),
            ("Listrik",  Theme.BTN_YELLOW, Theme.IC_YELLOW, "lightning", "fitur_listrik"),
            ("Lainnya",  Theme.BTN_PURPLE, Theme.IC_PURPLE, "dots",      None) 
        ]

        col_w = self.W / 3
        y_awal = 600
        
        for i, item in enumerate(daftar_menu):
            label, bg, ic_col, ic_type, tujuan = item
            row = i // 3; col = i % 3
            x = (col * col_w) + (col_w / 2)
            y = y_awal + (row * 110)
            
            safe_label = label.replace(" ", "_") 
            tag = f"btn_{safe_label}"
            
            self.draw_btn_menu(x, y, bg, ic_col, ic_type, label, tag)
            
            if tujuan:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=tujuan: self.navigate(t))
            else:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e: messagebox.showinfo("Info", "Maaf belum tersedia"))

        # --- NAVIGASI BAWAH ---
        self.draw_bottom_nav()

    # --- PEMBANTU (HELPERS) ---

    def draw_card_stats(self, x, y, w, title, amount, color, arrow, percent, limit_val):
        h = 160 
        draw_rounded_rect(self.canvas, x, y, x+w, y+h, 20, Theme.WHITE)
        
        self.canvas.create_oval(x+20, y+20, x+50, y+50, fill=Theme.BG, outline="")
        cx, cy = x+35, y+35
        pts = [cx, cy+6, cx, cy-6, cx-4, cy-2, cx, cy-6, cx+4, cy-2, cx, cy-6] if arrow == "up" else \
              [cx, cy-6, cx, cy+6, cx-4, cy+2, cx, cy+6, cx+4, cy+2, cx, cy+6]
        self.canvas.create_line(pts, fill=color, width=2)

        self.canvas.create_text(x+20, y+75, text=title, anchor="w", font=Theme.F_BODY, fill=Theme.MUTED)
        self.canvas.create_text(x+20, y+100, text=amount, anchor="w", font=("Arial", 16, "bold"), fill=Theme.TEXT)
        
        bar_x1, bar_y1 = x + 20, y + 130
        bar_x2, bar_y2 = x + w - 20, y + 135
        draw_rounded_rect(self.canvas, bar_x1, bar_y1, bar_x2, bar_y2, 2, "#E0E0E0") 
        
        if percent > 0:
            fill_w = (bar_x2 - bar_x1) * (min(percent, 100) / 100)
            draw_rounded_rect(self.canvas, bar_x1, bar_y1, bar_x1 + fill_w, bar_y2, 2, color)
        
        if arrow == "up":
            limit_str = f"Target: {limit_val/1000000:.1f}jt"
        else:
            limit_str = f"Budget: {limit_val/1000000:.1f}jt"
            
        self.canvas.create_text(bar_x2, bar_y1 - 10, text=f"{percent}%", anchor="e", font=("Arial", 9, "bold"), fill=color)
        self.canvas.create_text(bar_x1, bar_y1 + 15, text=limit_str, anchor="w", font=("Arial", 8), fill="#999")

    def draw_btn_menu(self, x, y, bg, ic_col, ic_type, label, tag):
        r = 35
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=bg, outline="", tags=tag)
        
        try:
            draw_icon(self.canvas, x, y, ic_type, ic_col, tags=tag) 
        except TypeError:
            draw_icon(self.canvas, x, y, ic_type, ic_col)
        
        self.canvas.create_text(x, y+50, text=label, font=Theme.F_BTN, fill=Theme.TEXT, tags=tag)
        self.efek_hover(tag)

    def draw_btn_avatar(self, x, y, char, cmd):
        tag = "btn_avatar"
        self.canvas.create_oval(x-30, y-30, x+30, y+30, fill=Theme.WHITE, outline="", tags=tag)
        self.canvas.create_text(x, y, text=char, font=("Arial", 20, "bold"), fill=Theme.PRIMARY, tags=tag)
        self.canvas.tag_bind(tag, "<Button-1>", lambda e: cmd())
        self.efek_hover(tag)

    def draw_bottom_nav(self):
        y_bg = self.H - 90
        self.canvas.create_rectangle(0, y_bg, self.W, self.H, fill=Theme.WHITE, outline="#EEEEEE")
        
        items = [("Home","home",None), ("Riwayat","history","history")]
        cw = self.W / 2
        y_icon = self.H - 55
        
        for i, (lbl, icon, target) in enumerate(items):
            x = (i * cw) + (cw / 2)
            color = Theme.PRIMARY if i == 0 else "#CFD8DC"
            tag = f"nav_{lbl}"
            draw_nav_icon(self.canvas, x, y_icon, icon, color, tag=tag)
            self.canvas.create_text(x, y_icon+30, text=lbl, font=Theme.F_SMALL, fill=color, tags=tag)
            
            if target:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=target: self.navigate(t))
                self.efek_hover(tag)

    def efek_hover(self, tag):
        self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))