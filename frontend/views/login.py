import customtkinter as ctk
from tkinter import messagebox
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)               
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import utils.validator as validator

from theme import Theme

from service.auth_service import AuthService 

class LoginApp:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        
        self.root.title("E-SAKU - Login")
        
        # Inisialisasi Layanan
        self.auth_service = AuthService()

        self.root.geometry("520x930")
        self.root.resizable(False, False) 

        self.main_container = ctk.CTkFrame(self.root, fg_color=Theme.BG)
        self.main_container.pack(fill="both", expand=True)

        self.show_welcome_page()

    def clear_frame(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def create_back_button(self, parent):
        btn = ctk.CTkButton(
            parent, text="←", width=45, height=45, corner_radius=22.5,         
            fg_color=Theme.WHITE, text_color=Theme.PRIMARY, hover_color="#FAFAFA",
            font=("Arial", 24, "bold"), command=self.show_welcome_page
        )
        btn.place(x=25, y=25) 

    def create_header_bg(self, height):
        header = ctk.CTkFrame(self.main_container, fg_color=Theme.PRIMARY, height=height, corner_radius=0)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(header, text="", width=250, height=250, fg_color=Theme.INCOME, corner_radius=125).place(x=340, y=-100)
        return header

    # ================= HALAMAN =================
    def show_welcome_page(self):
        self.clear_frame()
        bg = ctk.CTkFrame(self.main_container, fg_color=Theme.PRIMARY, corner_radius=0)
        bg.pack(fill="both", expand=True)
        ctk.CTkLabel(bg, text="", width=300, height=300, fg_color=Theme.INCOME, corner_radius=150).place(x=-100, y=-50)

        center_frame = ctk.CTkFrame(bg, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(center_frame, text="E-SAKU", font=Theme.F_HEAD_L, text_color="white").pack()
        ctk.CTkLabel(center_frame, text="Solusi Saku Digital", font=Theme.F_SUB, text_color="#E8F5E9").pack(pady=5)

        bottom_frame = ctk.CTkFrame(bg, fg_color="transparent")
        bottom_frame.place(relx=0.5, rely=0.85, anchor="center", relwidth=1)

        ctk.CTkButton(bottom_frame, text="Masuk Akun", fg_color=Theme.WHITE, text_color=Theme.PRIMARY, hover_color="#F1F8E9", height=55, corner_radius=27, font=Theme.F_BTN, command=self.show_login_page).pack(pady=10, ipadx=30)
        ctk.CTkButton(bottom_frame, text="Buka Rekening Baru", fg_color="transparent", text_color=Theme.WHITE, border_width=2, border_color=Theme.WHITE, hover_color=Theme.HOVER_BTN, height=55, corner_radius=27, font=Theme.F_BTN, command=self.show_register_page).pack(pady=5, ipadx=10)
        ctk.CTkLabel(bg, text="v1.0", font=("Arial", 10), text_color="#C8E6C9").place(relx=0.5, rely=0.97, anchor="center")

    def show_login_page(self):
        self.clear_frame()
        header = self.create_header_bg(height=320)
        self.create_back_button(header)
        ctk.CTkLabel(header, text="Selamat Datang di\nE-SAKU", font=Theme.F_HEAD, text_color="white", justify="center").place(relx=0.5, rely=0.45, anchor="center")

        card = ctk.CTkFrame(self.main_container, fg_color=Theme.WHITE, corner_radius=30)
        card.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9, relheight=0.55) 
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)

        self.create_label(content, "Username")
        self.entry_user = self.create_entry(content, "Masukkan Username")
        self.create_label(content, "Password", pady=20) 
        self.entry_pass = self.create_entry(content, "********", show="*")

        ctk.CTkButton(content, text="LOGIN SEKARANG", fg_color=Theme.PRIMARY, hover_color=Theme.HOVER_BTN, height=55, corner_radius=27, font=Theme.F_BTN, command=self.action_login).pack(fill="x", pady=20)

        footer = ctk.CTkFrame(content, fg_color="transparent")
        footer.pack(side="bottom", pady=15)
        ctk.CTkLabel(footer, text="Belum punya akun?", font=Theme.F_BODY, text_color="gray").pack(side="left")
        ctk.CTkButton(footer, text="Daftar", fg_color="transparent", text_color=Theme.PRIMARY, font=Theme.F_TITLE, hover=False, width=30, command=self.show_register_page).pack(side="left", padx=5)

        ctk.CTkButton(content, text="Lupa Password?", fg_color="transparent", text_color=Theme.MUTED, font=("Arial", 11), hover=False, height=20, command=self.show_forgot_password_page).pack(fill="x", pady=(0, 10))

    def show_register_page(self):
        self.clear_frame()
        header = self.create_header_bg(height=250)
        self.create_back_button(header)
        ctk.CTkLabel(header, text="Registrasi E-SAKU", font=Theme.F_HEAD, text_color="white").place(relx=0.5, rely=0.4, anchor="center")

        card = ctk.CTkFrame(self.main_container, fg_color=Theme.WHITE, corner_radius=30)
        card.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9, relheight=0.72)
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=25)

        self.reg_nama = self.add_input(content, "Username", "Username unik")
        self.reg_hp = self.add_input(content, "No. WhatsApp", "08xxxxxxxxxx")
        self.reg_email = self.add_input(content, "Email", "email@domain.com")
        self.reg_pass1 = self.add_input(content, "Password", "Min. 8 karakter", True)

        self.check_var = ctk.StringVar(value="off")
        ctk.CTkCheckBox(content, text="Saya setuju dengan S&K E-SAKU", variable=self.check_var, onvalue="on", offvalue="off", font=Theme.F_TITLE, text_color="gray", fg_color=Theme.PRIMARY, border_width=2, checkbox_width=20, checkbox_height=20).pack(fill="x", pady=(20, 10))
        ctk.CTkButton(content, text="BUAT AKUN", fg_color=Theme.PRIMARY, hover_color=Theme.HOVER_BTN, height=55, corner_radius=27, font=Theme.F_BTN, command=self.action_register).pack(fill="x", side="bottom", pady=10)

    # ================= PEMBANTU =================
    def create_label(self, parent, text, pady=5):
        ctk.CTkLabel(parent, text=text, font=Theme.F_TITLE, text_color=Theme.MUTED, anchor="w").pack(fill="x", pady=(pady, 0))

    def create_entry(self, parent, placeholder, show=""):
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, font=Theme.F_BODY, text_color=Theme.TEXT, fg_color=Theme.INPUT_BG, border_width=0, corner_radius=10, height=45, show=show)
        entry.pack(fill="x", pady=(5, 0))
        return entry
    
    def add_input(self, parent, label, placeholder, is_pass=False):
        ctk.CTkLabel(parent, text=label, font=Theme.F_TITLE, text_color=Theme.MUTED, anchor="w").pack(fill="x", pady=(8, 0))
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, font=Theme.F_BODY, text_color=Theme.TEXT, fg_color=Theme.INPUT_BG, border_width=0, corner_radius=10, height=42, show="*" if is_pass else "")
        entry.pack(fill="x", pady=(2, 0))
        return entry

    # ================= FORGOT PASSWORD =================
    def show_forgot_password_page(self):
        self.clear_frame()
        header = self.create_header_bg(height=280)
        self.create_back_button(header)
        ctk.CTkLabel(header, text="Lupa Password", font=Theme.F_HEAD, text_color="white").place(relx=0.5, rely=0.45, anchor="center")

        card = ctk.CTkFrame(self.main_container, fg_color=Theme.WHITE, corner_radius=30)
        card.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9, relheight=0.45) 
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text="Masukkan email Anda untuk menerima kode verifikasi.", font=Theme.F_BODY, text_color=Theme.MUTED, wraplength=300).pack(pady=(0, 20))

        self.fp_email = self.create_entry(content, "Contoh: email@domain.com")
        
        ctk.CTkButton(content, text="Kirim Kode", fg_color=Theme.PRIMARY, hover_color=Theme.HOVER_BTN, height=55, corner_radius=27, font=Theme.F_BTN, command=self.handle_fp_step1).pack(fill="x", pady=20)

    def handle_fp_step1(self):
        email = self.fp_email.get()
        if not email:
            messagebox.showwarning("Info", "Masukkan email terlebih dahulu")
            return
            
        success, res = self.auth_service.initiate_forgot_password(email)
        if not success:
            messagebox.showerror("Gagal", res)
            return
            
        self.server_otp = res
        self.target_email = email
        messagebox.showinfo("Kode OTP", f"Kode OTP Anda: {res}\n(Simpan kode ini)")
        
        self.show_reset_password_page()

    def show_reset_password_page(self):
        self.clear_frame()
        header = self.create_header_bg(height=250)
        btn = ctk.CTkButton(
            header, text="←", width=45, height=45, corner_radius=22.5,         
            fg_color=Theme.WHITE, text_color=Theme.PRIMARY, hover_color="#FAFAFA",
            font=("Arial", 24, "bold"), command=self.show_forgot_password_page
        )
        btn.place(x=25, y=25)
        
        ctk.CTkLabel(header, text="Reset Password", font=Theme.F_HEAD, text_color="white").place(relx=0.5, rely=0.45, anchor="center")

        card = ctk.CTkFrame(self.main_container, fg_color=Theme.WHITE, corner_radius=30)
        card.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9, relheight=0.65) 
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=25)

        self.create_label(content, "Kode OTP")
        self.fp_otp = self.create_entry(content, "Masukan 4 digit kode")

        self.create_label(content, "Password Baru", pady=15)
        self.fp_pass = self.create_entry(content, "Min. 8 karakter", show="*")
        
        ctk.CTkLabel(content, text="* Min. 8 karakter, harus ada huruf & angka.", font=("Arial", 10), text_color=Theme.DANGER, anchor="w").pack(fill="x", pady=(2, 0))

        ctk.CTkButton(content, text="Simpan Password", fg_color=Theme.PRIMARY, hover_color=Theme.HOVER_BTN, height=55, corner_radius=27, font=Theme.F_BTN, command=self.handle_fp_step2).pack(fill="x", pady=20)

    def handle_fp_step2(self):
        otp = self.fp_otp.get()
        new_pass = self.fp_pass.get()
        
        if otp != self.server_otp:
            messagebox.showerror("Gagal", "Kode OTP salah!")
            return
            
        success, msg = self.auth_service.reset_password(self.target_email, new_pass)
        if success:
            messagebox.showinfo("Sukses", "Password berhasil diubah, silakan login.")
            self.show_login_page()
        else:
            messagebox.showerror("Gagal", msg)

    # ================= LOGIKA =================
    
    def action_login(self):
        user = self.entry_user.get().strip()
        pwd = self.entry_pass.get().strip()
        
        if not user or not pwd:
            messagebox.showwarning("Gagal Masuk", "Mohon isi Username dan Password!")
            return

        response_data = self.auth_service.login(user, pwd)
        
        if response_data:
            self.main_container.destroy()
            self.on_login_success(response_data)
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    def action_register(self):
        nama = self.reg_nama.get().strip()
        hp = self.reg_hp.get().strip()
        email = self.reg_email.get().strip()
        pwd = self.reg_pass1.get().strip()

        if not nama or not hp or not email or not pwd:
            messagebox.showwarning("Data Kurang", "Semua kolom wajib diisi!")
            return
            
        if self.check_var.get() == "off":
            messagebox.showwarning("Persetujuan", "Anda harus menyetujui Syarat & Ketentuan.")
            return

        if not validator.is_valid_username(nama):
             messagebox.showwarning("Username Salah", "Username minimal 4 karakter, tanpa spasi.")
             return

        if not validator.is_valid_email(email):
            messagebox.showwarning("Email Salah", "Format email tidak valid.")
            return

        if not validator.is_valid_phone(hp):
            messagebox.showwarning("No. HP Salah", "Format Nomor HP tidak valid (08xx, 10-13 digit).")
            return

        if not validator.is_valid_password(pwd):
            messagebox.showwarning("Password Lemah", "Password minimal 8 karakter.")
            return

        success, msg = self.auth_service.register(nama, email, pwd, hp)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.show_login_page()
        else:
            messagebox.showerror("Gagal Register", msg)