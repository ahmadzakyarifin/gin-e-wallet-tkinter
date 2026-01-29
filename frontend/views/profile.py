import customtkinter as ctk
from tkinter import messagebox
import os
import sys
import datetime 


current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


try:
    from theme import Theme
except ImportError:
    from frontend.theme import Theme

class EditFrame(ctk.CTkFrame):
    """
    Frame untuk mengedit data.
    """
    def __init__(self, master, field_key, field_title, current_value, save_callback, cancel_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.save_callback = save_callback
        self.cancel_callback = cancel_callback
        self.field_key = field_key
        
        # --- Header ---
        header = ctk.CTkFrame(self, fg_color=Theme.WHITE, height=60, corner_radius=0)
        header.pack(fill="x", pady=(0, 1), anchor="n") 

        # Tombol Kembali (Batal Edit)
        back_btn = ctk.CTkButton(header, text="❮", font=Theme.F_JUMBO, width=40, height=40,
                               fg_color="transparent", text_color=Theme.TEXT, 
                               hover_color=Theme.BTN_GREEN, command=self.cancel_callback)
        back_btn.pack(side="left", padx=10)
        
        title = ctk.CTkLabel(header, text=f"Ubah {field_title}", font=Theme.F_HEAD, text_color=Theme.TEXT)
        title.pack(side="left", padx=5)

        # Tombol Simpan
        save_header_btn = ctk.CTkButton(header, text="Simpan", font=Theme.F_BTN, width=80,
                                      fg_color="transparent", text_color=Theme.PRIMARY,
                                      hover_color=Theme.BTN_GREEN, command=self.save_action)
        save_header_btn.pack(side="right", padx=15)

        # --- Form Input ---
        form_card = ctk.CTkFrame(self, fg_color=Theme.WHITE, corner_radius=0)
        form_card.pack(fill="x", pady=(20, 0), anchor="n")

        lbl = ctk.CTkLabel(form_card, text=field_title, font=Theme.F_SMALL, text_color=Theme.MUTED)
        lbl.pack(anchor="w", padx=20, pady=(15, 0))

        self.entry = ctk.CTkEntry(form_card, height=45, font=Theme.F_SUB, 
                                fg_color="transparent", border_width=0, text_color=Theme.TEXT)
        self.entry.pack(fill="x", padx=15, pady=(0, 15))
        
        if field_key != "pin":
            self.entry.insert(0, str(current_value))
        else:
            self.entry.configure(show="•") 

        line = ctk.CTkFrame(form_card, height=2, fg_color=Theme.PRIMARY)
        line.pack(fill="x", side="bottom")

        # --- Hint ---
        hint_text = "Pastikan data benar."
        if field_key == "pin":
            hint_text = "Jangan sebarkan PIN Anda."
            
        hint_lbl = ctk.CTkLabel(self, text=hint_text, font=Theme.F_SMALL, text_color=Theme.MUTED)
        hint_lbl.pack(anchor="w", padx=20, pady=(10, 0))

        self.entry.focus_set()

    def save_action(self):
        new_value = self.entry.get()
        if not new_value:
            messagebox.showwarning("Info", "Data tidak boleh kosong")
            return
        self.save_callback(self.field_key, new_value)


class ProfileFrame(ctk.CTkFrame):
    """
    Kontainer utama Profil.
    """
    def __init__(self, master, user_data, navigate_callback, logout_callback, back_to_home_callback):
        super().__init__(master, fg_color=Theme.BG)
        self.user_data = user_data
        
        self.navigate_callback = navigate_callback   
        self.logout_callback = logout_callback       
        self.back_to_home_callback = back_to_home_callback
        
        self.content_frame = None
        self.show_main_profile_view()

    def on_mousewheel(self, event):
        try:
            if self.winfo_exists() and self.winfo_ismapped():
                if event.num == 5 or event.delta == -120:
                    self.canvas.yview_scroll(1, "units")
                elif event.num == 4 or event.delta == 120:
                    self.canvas.yview_scroll(-1, "units")
        except:
            pass 

    def show_main_profile_view(self):
        """Menampilkan UI List Menu Profil"""
        if self.content_frame:
            self.content_frame.destroy()

        # --- 1. Top Bar ---
        top_bar = ctk.CTkFrame(self, fg_color=Theme.PRIMARY, height=60, corner_radius=0)
        top_bar.pack(fill="x", anchor="n")

        btn_back = ctk.CTkButton(top_bar, text="←", font=("Arial", 20, "bold"), 
                                 fg_color=Theme.WHITE, text_color=Theme.PRIMARY,
                                 hover_color="#EEEEEE",
                                 width=36, height=36, corner_radius=18, 
                                 command=self.back_to_home_callback)
        btn_back.pack(side="left", padx=20, pady=10)
        
        # --- 2. Area Scrollable ---
        self.canvas_container = ctk.CTkFrame(self, fg_color=Theme.BG)
        self.canvas_container.pack(fill="both", expand=True)
        
        self.canvas = ctk.CTkCanvas(self.canvas_container, bg=Theme.BG, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = ctk.CTkScrollbar(self.canvas_container, orientation="vertical", command=self.canvas.yview)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.content_frame = ctk.CTkFrame(self.canvas, fg_color=Theme.BG)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        self.content_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Button-4>", self.on_mousewheel)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel)

        def update_width(event=None):
            w = self.canvas.winfo_width()
            if w > 1:
                self.canvas.itemconfig(self.canvas_window, width=w)
        
        self.canvas.bind("<Configure>", update_width)
        self.after(100, update_width)

        # --- Header Profil ---
        header_container = ctk.CTkFrame(self.content_frame, fg_color=Theme.PRIMARY, corner_radius=0)
        header_container.pack(fill="x", pady=(0, 20), anchor="n")

        profile_circle = ctk.CTkFrame(header_container, width=100, height=100, fg_color=Theme.WHITE, corner_radius=50)
        profile_circle.pack(pady=(5, 10)) 
        profile_circle.pack_propagate(False)

        nama_user = self.user_data.get('nama', 'User')
        initials = "".join([n[0] for n in nama_user.split()[:2]]).upper()
        
        initial_label = ctk.CTkLabel(profile_circle, text=initials, font=Theme.F_HEAD_L, text_color=Theme.PRIMARY)
        initial_label.place(relx=0.5, rely=0.5, anchor="center")

        name_label = ctk.CTkLabel(header_container, text=nama_user, font=Theme.F_HEAD, text_color=Theme.WHITE)
        name_label.pack(pady=(5, 5))
        
        # --- STATISTIK LIMIT BULANAN ---
        limit_val = float(self.user_data.get('limit_pengeluaran', 20000000))
        used_val = float(self.user_data.get('pengeluaran', 0))
        
        remaining_val = limit_val - used_val
        if remaining_val < 0: remaining_val = 0
        
        progress = used_val / limit_val if limit_val > 0 else 0
        if progress > 1.0: progress = 1.0
            
        frame_limit = ctk.CTkFrame(header_container, fg_color="transparent")
        frame_limit.pack(pady=(0, 25), padx=20, fill="x")
        
        def format_rupiah(val):
            return f"Rp {val:,.0f}".replace(",", ".")
            
        nama_bulan = datetime.datetime.now().strftime("%B")
        bulan_indo = {
            "January": "Januari", "February": "Februari", "March": "Maret", "April": "April",
            "May": "Mei", "June": "Juni", "July": "Juli", "August": "Agustus",
            "September": "September", "October": "Oktober", "November": "November", "December": "Desember"
        }
        bulan_str = bulan_indo.get(nama_bulan, nama_bulan)

        info_box = ctk.CTkFrame(frame_limit, fg_color="transparent")
        info_box.pack(fill="x", pady=(0, 5))
        
        lbl_title = ctk.CTkLabel(info_box, text=f"Pengeluaran {bulan_str}", font=Theme.F_SMALL, text_color="#E0E0E0")
        lbl_title.pack(side="left")
        
        lbl_sisa = ctk.CTkLabel(info_box, text=f"Sisa: {format_rupiah(remaining_val)}", font=("Arial", 11, "bold"), text_color="#FFEB3B")
        lbl_sisa.pack(side="right")

        p_bar = ctk.CTkProgressBar(frame_limit, height=12, corner_radius=6)
        p_bar.pack(fill="x")
        p_bar.set(progress)
        
        if progress < 0.5:
            p_bar.configure(progress_color="#00E676")
        elif progress < 0.8:
            p_bar.configure(progress_color="#FFEA00")
        else:
            p_bar.configure(progress_color="#FF3D00")
        
        lbl_detail = ctk.CTkLabel(frame_limit, 
                              text=f"Terpakai: {format_rupiah(used_val)} / Limit: {format_rupiah(limit_val)}", 
                              font=("Arial", 10), text_color="#BDBDBD")
        lbl_detail.pack(anchor="w", pady=(2, 0))

        # --- Menu Items ---
        self.add_section_label("Informasi Akun")
        self.create_menu_item("👤", "Nama Pengguna", "nama", self.user_data.get("nama"))
        self.create_menu_item("📱", "Nomor Telepon", "no_hp", self.user_data.get("no_hp"))
        self.create_menu_item("📧", "Email", "email", self.user_data.get("email"))
        self.create_menu_item("🆔", "E-Saku ID", None, "882910293") 

        self.add_section_label("Keamanan")
        self.create_menu_item("🔒", "Ganti PIN / Password", "pin", "••••••")

        self.add_section_label("Pengaturan")
        self.create_menu_item("🔔", "Notifikasi", None, None, is_setting=True)
        self.create_menu_item("🌐", "Bahasa", None, "Indonesia", is_setting=True)
        self.create_menu_item("❓", "Bantuan", None, None, is_setting=True)

        logout_btn = ctk.CTkButton(self.content_frame, text="Keluar dari Akun", font=Theme.F_BTN, 
                                   fg_color=Theme.DANGER, 
                                   text_color=Theme.WHITE,
                                   hover_color="#D32F2F",
                                   height=50, corner_radius=10,
                                   command=self.logout_callback)
        logout_btn.pack(fill="x", padx=20, pady=(40, 50))

    def show_edit_page(self, field_key, field_title, current_value, save_callback_from_main):
        if self.content_frame:
            self.content_frame.destroy()
        
        for widget in self.winfo_children():
            widget.destroy()

        val_to_send = current_value if field_key != "pin" else ""
        
        self.content_frame = EditFrame(
            master=self,
            field_key=field_key,
            field_title=field_title,
            current_value=val_to_send,
            save_callback=save_callback_from_main,
            cancel_callback=self.refresh_ui 
        )
        self.content_frame.pack(fill="both", expand=True)

    def refresh_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.show_main_profile_view()

    def add_section_label(self, text):
        lbl = ctk.CTkLabel(self.content_frame, text=text, font=Theme.F_TITLE, text_color=Theme.TEXT)
        lbl.pack(anchor="w", padx=20, pady=(15, 5))

    def create_menu_item(self, icon, title, key_data=None, value_text=None, is_setting=False):
        item_frame = ctk.CTkFrame(self.content_frame, fg_color=Theme.WHITE, corner_radius=12, border_width=1, border_color="#E0E0E0")
        item_frame.pack(fill="x", padx=20, pady=(0, 10))

        content = ctk.CTkFrame(item_frame, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=15)

        left_box = ctk.CTkFrame(content, fg_color="transparent")
        left_box.pack(side="left", fill="x", expand=True)

        if os.name == "nt":
            font_icon = ("Segoe UI Emoji", 20)
        else:
            font_icon = ("Arial", 24) 

        icon_lbl = ctk.CTkLabel(left_box, text=icon, font=font_icon, width=35) 
        icon_lbl.pack(side="left", padx=(0, 10))

        text_box = ctk.CTkFrame(left_box, fg_color="transparent")
        text_box.pack(side="left")
        
        title_lbl = ctk.CTkLabel(text_box, text=title, font=Theme.F_BODY, text_color=Theme.TEXT)
        title_lbl.pack(anchor="w")

        val_lbl = None
        if value_text:
            val_lbl = ctk.CTkLabel(text_box, text=value_text, font=Theme.F_SMALL, text_color=Theme.MUTED)
            val_lbl.pack(anchor="w")

        arrow_lbl = ctk.CTkLabel(content, text="›", font=Theme.F_JUMBO, text_color="#CCCCCC")
        
        if key_data or is_setting:
            arrow_lbl.pack(side="right")
            
            def on_tap(event):
                if key_data: 
                    self.navigate_callback(key_data, title, value_text)
                elif is_setting: 
                    messagebox.showinfo("Info", f"Menu {title}")

            widgets = [item_frame, content, left_box, icon_lbl, text_box, title_lbl, arrow_lbl]
            if val_lbl: widgets.append(val_lbl)
            
            for w in widgets:
                if w:
                    w.configure(cursor="hand2")
                    w.bind("<Button-1>", on_tap)