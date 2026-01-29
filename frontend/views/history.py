import tkinter as tk
from tkinter import messagebox
import sys
import os
import customtkinter as ctk
import re

# --- PENGATURAN PATH & IMPORT THEME ---
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from theme import Theme, draw_rounded_rect, draw_icon, draw_nav_icon
except ImportError:
    from frontend.theme import Theme, draw_rounded_rect, draw_icon, draw_nav_icon

class HistoryView:
    def __init__(self, master, width, height, on_navigate, data_transaksi):
        self.master = master 
        self.W = width
        self.H = height
        self.navigate = on_navigate
        self.data_transaksi = data_transaksi
        
        self.var_search = tk.StringVar()
        self.filter_selected = "Semua"

        # 1. Main Frame (Header + List)
        self.main_frame = ctk.CTkFrame(self.master, fg_color="#FAFAFA", width=self.W, height=self.H)
        self.main_frame.pack(fill="both", expand=True)

        # -- A. CANVAS HEADER (Fixed) --
        self.header_h = 200
        self.cv_header = ctk.CTkCanvas(self.main_frame, width=self.W, height=self.header_h, bg="#FAFAFA", highlightthickness=0)
        self.cv_header.pack(fill="x", side="top")
        
        # -- B. FRAME LIST (Scrollable) --
        self.list_container = ctk.CTkFrame(self.main_frame, fg_color="#FAFAFA")
        self.list_container.pack(fill="both", expand=True, side="top")
        
        # Scrollbar & Canvas List
        self.scrollbar = ctk.CTkScrollbar(self.list_container, orientation="vertical")
        self.cv_list = ctk.CTkCanvas(self.list_container, bg="#FAFAFA", highlightthickness=0, 
                                     yscrollcommand=self.scrollbar.set)
        self.cv_list.pack(side="left", fill="both", expand=True)
        self.scrollbar.configure(command=self.cv_list.yview)
        
        # MouseWheel Binding
        self.cv_list.bind_all("<MouseWheel>", self.on_mousewheel)
        self.cv_list.bind_all("<Button-4>", self.on_mousewheel)
        self.cv_list.bind_all("<Button-5>", self.on_mousewheel)

        # 2. Detail Frame (Hidden by default)
        self.detail_frame = ctk.CTkFrame(self.master, fg_color="#FAFAFA", width=self.W, height=self.H)
        self.cv_detail = ctk.CTkCanvas(self.detail_frame, width=self.W, height=self.H, bg="#FAFAFA", highlightthickness=0)
        self.cv_detail.pack(fill="both", expand=True)

        # BUTTON BACK (Untuk Detail)
        self.btn_back = ctk.CTkButton(
            self.detail_frame, text="←", width=45, height=45, corner_radius=22.5,         
            fg_color=Theme.WHITE, text_color=Theme.PRIMARY, hover_color="#FAFAFA",
            bg_color=Theme.PRIMARY, 
            font=("Arial", 24, "bold"), command=lambda: self.draw()
        )
        self.btn_back.place(x=25, y=25)
        
        # -- C. Floating Bottom Nav (Overlay) --
        self.nav_h = 90
        self.nav_container = tk.Frame(self.master, height=self.nav_h, bg="white")
        self.nav_container.place(relx=0, rely=1.0, anchor="sw", relwidth=1.0)
        
        self.cv_nav = tk.Canvas(self.nav_container, width=self.W, height=self.nav_h, bg="white", highlightthickness=0)
        self.cv_nav.pack(fill="both", expand=True)
        
        self.draw_bottom_nav()

    def on_mousewheel(self, event):
        try:
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists() and self.main_frame.winfo_ismapped():
                if event.num == 5 or event.delta == -120:
                    self.cv_list.yview_scroll(1, "units")
                elif event.num == 4 or event.delta == 120:
                    self.cv_list.yview_scroll(-1, "units")
        except:
             pass

    def draw(self):
        # Tampilkan Main Frame, Sembunyikan Detail
        self.detail_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        
        # Pastikan Nav Bar muncul (di atas)
        self.nav_container.place(relx=0, rely=1.0, anchor="sw", relwidth=1.0)
        self.nav_container.lift()
        
        self.draw_header()
        self.draw_search_filter_ui()
        self.render_list()

    def draw_header(self):
        self.cv_header.delete("all")
        self.cv_header.create_rectangle(0, 0, self.W, 120, fill=Theme.PRIMARY, outline="")
        self.cv_header.create_text(self.W/2, 60, text="Riwayat Transaksi", font=Theme.F_HEAD, fill=Theme.WHITE)

    def draw_search_filter_ui(self):
        y_pos = 140
        bg_input = "#F0F0F0"
        w_search = self.W - 80 
        
        # Kotak Search
        draw_rounded_rect(self.cv_header, 20, y_pos, 20 + w_search, y_pos+45, 22, bg_input)
        
        # Ikon Search
        ix, iy = 45, y_pos + 22
        self.cv_header.create_oval(ix-6, iy-6, ix+6, iy+6, outline="#9E9E9E", width=2)
        self.cv_header.create_line(ix+4, iy+4, ix+10, iy+10, fill="#9E9E9E", width=2, capstyle="round")

        # Widget Entry
        try:
            if hasattr(self, 'entry_search') and self.entry_search:
                self.entry_search.destroy()
        except: pass
        
        self.entry_search = tk.Entry(self.main_frame, textvariable=self.var_search, font=("Arial", 11), bd=0, bg=bg_input, fg=Theme.TEXT)
        self.entry_search.place(x=65, y=y_pos+13, width=w_search - 90, height=20)
        self.entry_search.bind("<KeyRelease>", lambda e: self.render_list())

        # Tombol Reset
        btn_reset_x = 20 + w_search - 25
        self.cv_header.create_text(btn_reset_x, y_pos+22, text="✕", font=("Arial", 11, "bold"), fill="#BDBDBD", tags="btn_reset")
        self.cv_header.tag_bind("btn_reset", "<Button-1>", lambda e: self.reset_search())
        
        # Tombol Filter
        filter_x = self.W - 50
        tag_filter = "btn_filter_klik"
        draw_rounded_rect(self.cv_header, filter_x, y_pos, filter_x+40, y_pos+45, 12, "#E0E0E0", tags=tag_filter)
        draw_rounded_rect(self.cv_header, filter_x, y_pos, filter_x+40, y_pos+43, 12, Theme.WHITE, tags=tag_filter)
        
        fx, fy = filter_x + 20, y_pos + 22
        points = [fx-7, fy-5, fx+7, fy-5, fx+2, fy+1, fx+2, fy+6, fx-2, fy+6, fx-2, fy+1]
        self.cv_header.create_polygon(points, fill="#555555", outline="", tags=tag_filter)
        self.cv_header.tag_bind(tag_filter, "<Button-1>", self.show_filter_popup)

    def show_filter_popup(self, event):
        menu = tk.Menu(self.main_frame, tearoff=0, bg="white", fg=Theme.TEXT, font=("Arial", 10))
        options = ["Semua", "Pemasukan", "Pengeluaran"]
        for opt in options:
            label = f"✓ {opt}" if self.filter_selected == opt else f"   {opt}"
            menu.add_command(label=label, command=lambda x=opt: self.apply_filter(x))
        menu.post(event.x_root, event.y_root)

    def apply_filter(self, selection):
        self.filter_selected = selection
        self.render_list()

    def reset_search(self):
        self.var_search.set("")
        self.render_list()
        self.entry_search.focus_set()

    def render_list(self):
        self.cv_list.delete("all")
        
        keyword = self.var_search.get().lower()
        kategori = self.filter_selected
        
        padding_bottom = 200 
        y_start = 10 
        found_count = 0
        
        for item in self.data_transaksi:
            # Filter Kategori
            if kategori == "Pemasukan" and item.get('type') != "in": continue
            if kategori == "Pengeluaran" and item.get('type') != "out": continue
            # Filter Keyword
            title = item.get('title', '')
            if keyword not in title.lower(): continue
            
            self.draw_item(y_start, item)
            y_start += 85
            found_count += 1
        
        total_h = max(y_start + padding_bottom, 500) 
        self.cv_list.configure(scrollregion=(0, 0, self.W, total_h))
        
        if found_count == 0:
            self.cv_list.create_text(self.W/2, 100, text="Tidak ada transaksi", font=Theme.F_BODY, fill="#BDBDBD", tags="list_item")

    def draw_item(self, y, item):
        canvas = self.cv_list 
        
        tipe = item.get('type', 'out')
        if tipe == "in":
            color, sign, bg_icon = Theme.INCOME, "+", Theme.BTN_GREEN
        else:
            color, sign, bg_icon = Theme.EXPENSE, "-", Theme.BTN_RED

        tag = f"item_{item.get('id', y)}" 
        
        # Card Background
        draw_rounded_rect(canvas, 22, y+3, self.W-18, y+78, 18, "#E0E0E0", tags=tag)
        draw_rounded_rect(canvas, 20, y, self.W-20, y+75, 18, Theme.WHITE, tags=tag)
        
        # Icon
        canvas.create_oval(35, y+15, 80, y+60, fill=bg_icon, outline="", tags=tag)
        judul = item.get('title', 'Trans')
        canvas.create_text(57, y+37, text=judul[0] if judul else "?", font=("Arial", 15, "bold"), fill=color, tags=tag)

        # Parsing Judul agar rapi (Menghapus info detail dari judul list)
        display_title = judul
        if "Transfer ke" in display_title and "(" in display_title:
             match = re.search(r"\((.*?)\)", display_title)
             if match: display_title = f"Transfer ke {match.group(1)}"
        
        if len(display_title) > 25: display_title = display_title[:22] + "..."

        canvas.create_text(95, y+25, text=display_title, anchor="w", font=Theme.F_BODY, fill=Theme.TEXT, tags=tag)
        canvas.create_text(95, y+50, text=item.get('date', '-'), anchor="w", font=Theme.F_SMALL, fill="#9E9E9E", tags=tag)
        
        amount_val = item.get('amount', 0)
        str_duit = f"{sign} Rp {amount_val:,}".replace(",", ".")
        canvas.create_text(self.W-35, y+25, text=str_duit, anchor="e", font=("Arial", 12, "bold"), fill=color, tags=tag)
        
        # Tombol Detail Kecil
        btn_w, btn_h = 60, 24
        btn_x2 = self.W - 35
        btn_x1 = btn_x2 - btn_w
        btn_y1 = y+45
        btn_y2 = btn_y1 + btn_h
        
        draw_rounded_rect(canvas, btn_x1, btn_y1, btn_x2, btn_y2, 10, "#E0E0E0", tags=tag) 
        canvas.create_text((btn_x1+btn_x2)/2, (btn_y1+btn_y2)/2, text="Detail", font=("Arial", 9, "bold"), fill="#555", tags=tag)

        # Binding Klik
        canvas.tag_bind(tag, "<Button-1>", lambda e, x=item: self.show_detail(x))
        self.efek_hover_item(tag)

    def show_detail(self, item):
        # Hide Nav Bar & Main Frame
        self.nav_container.place_forget() 
        self.main_frame.pack_forget()
        
        try:
            if hasattr(self, 'entry_search') and self.entry_search:
                 self.entry_search.place_forget() 
        except: pass
        
        self.detail_frame.pack(fill="both", expand=True)
        self.cv_detail.delete("all")
        
        # --- HEADER DETAIL ---
        self.cv_detail.create_rectangle(0, 0, self.W, 120, fill=Theme.PRIMARY, outline="")
        self.btn_back.lift() 
        self.btn_back.place(x=20, y=30) 

        self.cv_detail.create_text(self.W/2, 60, text="Detail Transaksi", font=Theme.F_HEAD, fill=Theme.WHITE)
        
        # --- CONTENT ---
        y_start = 220
        cx, cy = self.W/2, y_start
        
        # Icon Centang Besar
        circle_r = 30
        self.cv_detail.create_oval(cx-circle_r, cy-circle_r, cx+circle_r, cy+circle_r, fill=Theme.BTN_GREEN, outline="")
        self.cv_detail.create_text(cx, cy, text="✓", font=("Arial", 24, "bold"), fill="white")
        self.cv_detail.create_text(cx, cy+45, text="Transaksi Berhasil", font=("Arial", 14, "bold"), fill=Theme.PRIMARY)
        
        tipe = item.get('type', 'out')
        sign = "+" if tipe == "in" else "-"
        color = Theme.INCOME if tipe == "in" else Theme.EXPENSE
        amount_str = f"{sign} Rp {item.get('amount', 0):,}".replace(",", ".")
        self.cv_detail.create_text(cx, cy+80, text=amount_str, font=("Arial", 28, "bold"), fill=color)
        
        # Parsing Data Tambahan dari Judul (Token, SN, dll)
        display_title = item.get('title', '')
        extra_info = [] # List of tuple (Label, Value, is_code)

        # Cek Token Listrik
        match_token = re.search(r"\(Token: (.*?)\)", display_title)
        if match_token:
            code = match_token.group(1)
            extra_info.append(("No. Token", code))
            display_title = display_title.replace(f" (Token: {code})", "")
        
        # Cek SN (Pulsa)
        match_sn = re.search(r"\(SN: (.*?)\)", display_title)
        if match_sn:
            code = match_sn.group(1)
            extra_info.append(("No. SN", code))
            display_title = display_title.replace(f" (SN: {code})", "")

        # Cek Ref
        match_ref = re.search(r"\(Ref: (.*?)\)", display_title)
        if match_ref:
            code = match_ref.group(1)
            extra_info.append(("No. Ref", code))
            display_title = display_title.replace(f" (Ref: {code})", "")

        # Cek Kode Penarikan (Tarik Tunai)
        match_wd = re.search(r"\(Kode: (.*?)\)", display_title)
        wd_code = None
        if match_wd:
            wd_code = match_wd.group(1)
            display_title = display_title.replace(f" (Kode: {wd_code})", "")
            
        # Susun Labels Utama
        labels = [
            ("Judul", display_title.strip()),
            ("Tanggal", item.get('date', '-')),
            ("Kategori", "Pemasukan" if tipe == 'in' else "Pengeluaran"),
            ("ID Transaksi", f"TRX-{item.get('id', 0)}")
        ]
        
        # Masukkan info tambahan ke list labels
        for lbl, val in extra_info:
             labels.insert(1, (lbl, val))

        # --- TAMPILAN BARCODE TARIK TUNAI (JIKA ADA) ---
        if wd_code:
            bc_y = cy + 130
            barcode_w = 150
            barcode_h = 50
            bc_start_x = self.W/2 - (barcode_w/2)
            
            import random
            random.seed(wd_code) 
            current_x = bc_start_x
            for _ in range(30):
                w = 2 if random.random() > 0.5 else 4
                self.cv_detail.create_rectangle(current_x, bc_y, current_x+w, bc_y+barcode_h, fill="#333", outline="")
                current_x += (w + 2)
            
            fmt_kode = " ".join([wd_code[i:i+3] for i in range(0, len(wd_code), 3)])
            self.cv_detail.create_text(self.W/2, bc_y+65, text=fmt_kode, font=("Arial", 20, "bold"), fill=Theme.PRIMARY)
            
            # Tombol Copy Kode
            btn_w, btn_h = 80, 28
            btn_x1 = (self.W/2) - (btn_w/2); btn_x2 = btn_x1 + btn_w
            btn_y1 = bc_y + 85; btn_y2 = btn_y1 + btn_h
            tag_cp = "copy_wd_code"
            draw_rounded_rect(self.cv_detail, btn_x1, btn_y1, btn_x2, btn_y2, 14, "#E8F5E9", tags=tag_cp)
            self.cv_detail.create_text(self.W/2, (btn_y1+btn_y2)/2, text="Salin Kode", font=("Arial", 11, "bold"), fill=Theme.PRIMARY, tags=tag_cp)
            self.cv_detail.tag_bind(tag_cp, "<Button-1>", lambda e, x=wd_code: self.copy_to_clipboard(x))
            self.efek_hover_detail(tag_cp)
            
            cy += 140 

        # --- RENDER LIST DETAIL ---
        row_height = 60
        box_padding = 20
        box_h = (len(labels) * row_height) + (box_padding * 2)
        
        box_y = cy + 120
        box_margin = 30
        card_w = self.W - (box_margin * 2)
        
        draw_rounded_rect(self.cv_detail, box_margin+2, box_y+2, box_margin+card_w+2, box_y+box_h+2, 20, "#E0E0E0")
        draw_rounded_rect(self.cv_detail, box_margin, box_y, box_margin+card_w, box_y+box_h, 20, Theme.WHITE)
        
        py = box_y + box_padding + 20 
        
        for i, (lbl, val) in enumerate(labels):
            is_code_row = lbl in ["No. Token", "No. SN", "No. Ref", "Kode Penarikan"]
            lbl_y = py - 10 if is_code_row else py
            
            self.cv_detail.create_text(box_margin+20, lbl_y, text=lbl, anchor="w", font=("Arial", 11), fill="#757575")
            
            val_str = str(val)
            val_disp = val_str[:25] + "..." if len(val_str) > 25 else val_str
            
            self.cv_detail.create_text(box_margin+card_w-20, lbl_y, text=val_disp, anchor="e", font=("Arial", 12, "bold"), fill=Theme.TEXT)
            
            # Tombol Copy untuk Data Penting
            if is_code_row:
                btn_w, btn_h = 60, 24
                btn_x2 = box_margin + card_w - 20
                btn_x1 = btn_x2 - btn_w
                btn_y_center = py + 15
                
                tag_copy = f"copy_{i}"
                draw_rounded_rect(self.cv_detail, btn_x1, btn_y_center-10, btn_x2, btn_y_center+10, 10, "#E8F5E9", tags=tag_copy)
                self.cv_detail.create_text((btn_x1+btn_x2)/2, btn_y_center, text="Salin", font=("Arial", 10, "bold"), fill=Theme.PRIMARY, tags=tag_copy)
                self.cv_detail.tag_bind(tag_copy, "<Button-1>", lambda e, x=val_str: self.copy_to_clipboard(x))
                self.efek_hover_detail(tag_copy)

            if i < len(labels) - 1:
                line_y = py + 30
                self.cv_detail.create_line(box_margin+20, line_y, box_margin+card_w-20, line_y, fill="#F5F5F5", width=1)
            
            py += row_height

    def copy_to_clipboard(self, text):
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        messagebox.showinfo("Disalin", f"Kode berhasil disalin:\n{text}")

    def draw_bottom_nav(self):
        self.cv_nav.delete("all")
        self.cv_nav.create_line(0, 0, self.W, 0, fill="#EEEEEE", width=1)
        
        items = [("Home", "home", "home"), ("Riwayat", "history", None)]
        cw = self.W / 2
        y_icon = 35 
        
        for i, (lbl, icon, target) in enumerate(items):
            x_center = (i * cw) + (cw / 2)
            color = Theme.PRIMARY if i == 1 else "#CFD8DC" 
            tag = f"nav_{lbl}"
            
            rect_x1 = i * cw; rect_x2 = (i + 1) * cw
            self.cv_nav.create_rectangle(rect_x1, 0, rect_x2, 90, fill="white", outline="", tags=tag)
            draw_nav_icon(self.cv_nav, x_center, y_icon, icon, color, tag=tag)
            self.cv_nav.create_text(x_center, y_icon+30, text=lbl, font=Theme.F_SMALL, fill=color, tags=tag)
            
            if target:
                self.cv_nav.tag_bind(tag, "<Button-1>", lambda e, t=target: self.safe_navigate(t))
                self.cv_nav.tag_bind(tag, "<Enter>", lambda e: self.cv_nav.config(cursor="hand2"))
                self.cv_nav.tag_bind(tag, "<Leave>", lambda e: self.cv_nav.config(cursor=""))

    def safe_navigate(self, target):
        if hasattr(self, 'main_frame') and self.main_frame: self.main_frame.destroy()
        if hasattr(self, 'nav_container') and self.nav_container: self.nav_container.destroy()
        if hasattr(self, 'detail_frame') and self.detail_frame: self.detail_frame.destroy()
        try:
            if hasattr(self, 'entry_search') and self.entry_search: self.entry_search.destroy()
        except: pass
        self.navigate(target)
    
    def efek_hover_item(self, tag):
        self.cv_list.tag_bind(tag, "<Enter>", lambda e: self.cv_list.config(cursor="hand2"))
        self.cv_list.tag_bind(tag, "<Leave>", lambda e: self.cv_list.config(cursor=""))

    def efek_hover_detail(self, tag):
        self.cv_detail.tag_bind(tag, "<Enter>", lambda e: self.cv_detail.config(cursor="hand2"))
        self.cv_detail.tag_bind(tag, "<Leave>", lambda e: self.cv_detail.config(cursor=""))

    def destroy(self):
        try:
            if hasattr(self, 'entry_search') and self.entry_search: self.entry_search.destroy()
        except: pass
        if hasattr(self, 'main_frame') and self.main_frame: self.main_frame.destroy()
        if hasattr(self, 'nav_container') and self.nav_container: self.nav_container.destroy()
        if hasattr(self, 'detail_frame') and self.detail_frame: self.detail_frame.destroy()