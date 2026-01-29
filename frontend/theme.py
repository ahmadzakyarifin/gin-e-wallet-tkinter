import tkinter as tk
import platform

# ==========================================
# KONFIGURASI OS
# ==========================================
os_name = platform.system()
FONT_FAMILY = "Segoe UI" if os_name == "Windows" else "DejaVu Sans"

class Theme:
    # --- WARNA UTAMA ---
    PRIMARY   = "#05B048" # Dana Green (Strong)
    BG        = "#F5F5F5"
    WHITE     = "#FFFFFF"
    TEXT      = "#333333"
    MUTED     = "#888888"
    SHADOW    = "#D6D6D6"
    
    # --- WARNA LAIN ---
    INCOME    = "#05B048" 
    EXPENSE   = "#FF5252" 
    DANGER    = "#FF3B30"
    WARNING   = "#FF9800"
    
    INPUT_BG  = "#E8F5E9" 
    
    # --- BUTTONS (ACTION) ---
    BTN_HOVER_DARK  = "#027D33" # Hijau Tua (Main Button Hover)
    BTN_HOVER_LIGHT = "#A5D6A7" # Hijau Muda Medium (Secondary Hover)
    
    BTN_HOVER = BTN_HOVER_DARK 
    HOVER_BTN = BTN_HOVER 
    
    BTN_LIGHT = "#C8E6C9" # Jelas Hijau Muda (Not White)
    
    # --- ICON BACKGROUNDS (Light Colors for Menu Grid) ---
    # Used in home.py as Theme.BTN_GREEN, etc.
    BTN_GREEN = "#E8F5E9"; IC_GREEN = "#05B048"
    BTN_BLUE  = "#E3F2FD"; IC_BLUE  = "#2979FF"
    BTN_ORANGE= "#FFF3E0"; IC_ORANGE= "#FF9800"
    BTN_PURPLE= "#F3E5F5"; IC_PURPLE= "#9C27B0"
    BTN_RED   = "#FFEBEE"; IC_RED   = "#FF5252"
    BTN_YELLOW= "#FFF8E1"; IC_YELLOW= "#FFB300"
    
    # Compatibility aliases if code uses BTN_BG_...
    BTN_BG_GREEN = BTN_GREEN
    BTN_BG_BLUE  = BTN_BLUE
    BTN_BG_ORANGE= BTN_ORANGE
    BTN_BG_PURPLE= BTN_PURPLE
    BTN_BG_RED   = BTN_RED
    BTN_BG_YELLOW= BTN_YELLOW

    # --- FONT ---
    F_HEAD_L  = (FONT_FAMILY, 30, "bold")
    F_HEAD    = (FONT_FAMILY, 16, "bold") 
    F_SUB     = (FONT_FAMILY, 16)
    F_SALDO   = (FONT_FAMILY, 34, "bold")
    F_TITLE   = (FONT_FAMILY, 12, "bold")
    F_BODY    = (FONT_FAMILY, 11)
    F_SMALL   = (FONT_FAMILY, 10)
    F_BTN     = (FONT_FAMILY, 12, "bold")
    F_JUMBO   = (FONT_FAMILY, 20, "bold") 

# === HELPER DRAWING ===

def draw_rounded_rect(canvas, x1, y1, x2, y2, r, color, tags=None):
    canvas.create_oval(x1, y1, x1+2*r, y1+2*r, fill=color, outline=color, tags=tags)
    canvas.create_oval(x2-2*r, y1, x2, y1+2*r, fill=color, outline=color, tags=tags)
    canvas.create_oval(x1, y2-2*r, x1+2*r, y2, fill=color, outline=color, tags=tags)
    canvas.create_oval(x2-2*r, y2-2*r, x2, y2, fill=color, outline=color, tags=tags)
    canvas.create_rectangle(x1+r, y1, x2-r, y2, fill=color, outline=color, tags=tags)
    canvas.create_rectangle(x1, y1+r, x2, y2-r, fill=color, outline=color, tags=tags)

def draw_icon(canvas, x, y, type, color, tags=None):
    w = 3
    if type == "plus": 
        canvas.create_line(x-10, y, x+10, y, fill=color, width=w, capstyle="round", tags=tags)
        canvas.create_line(x, y-10, x, y+10, fill=color, width=w, capstyle="round", tags=tags)
    elif type == "arrow_r": 
        canvas.create_line(x-8, y, x+8, y, fill=color, width=w, capstyle="round", tags=tags)
        canvas.create_line(x+2, y-6, x+8, y, fill=color, width=w, capstyle="round", tags=tags)
        canvas.create_line(x+2, y+6, x+8, y, fill=color, width=w, capstyle="round", tags=tags)
    elif type == "arrow_d": 
        canvas.create_line(x, y-8, x, y+8, fill=color, width=w, capstyle="round", tags=tags)
        canvas.create_line(x-6, y+2, x, y+8, fill=color, width=w, capstyle="round", tags=tags)
        canvas.create_line(x+6, y+2, x, y+8, fill=color, width=w, capstyle="round", tags=tags)
    elif type == "dots": 
        for o in [-6, 0, 6]: 
            canvas.create_oval(x+o-2, y-2, x+o+2, y+2, fill=color, outline="", tags=tags)
    elif type == "phone": 
        canvas.create_rectangle(x-7, y-11, x+7, y+11, outline=color, width=2, tags=tags)
        canvas.create_line(x-3, y+8, x+3, y+8, fill=color, width=2, tags=tags)
    elif type == "lightning": 
        canvas.create_line(x+3, y-10, x-5, y, fill=color, width=2, tags=tags)
        canvas.create_line(x-5, y, x+5, y, fill=color, width=2, tags=tags)
        canvas.create_line(x+5, y, x-3, y+10, fill=color, width=2, tags=tags)

def draw_nav_icon(canvas, x, y, type, color, tag=None):
    w = 2
    tags = (tag,) if tag else ()
    if type == "home": 
        canvas.create_line(x-10, y-2, x, y-12, fill=color, width=w, capstyle="round", tags=tags)
        canvas.create_line(x+10, y-2, x, y-12, fill=color, width=w, capstyle="round", tags=tags)
        canvas.create_rectangle(x-7, y-2, x+7, y+10, outline=color, width=w, tags=tags)
        canvas.create_line(x-3, y+10, x-3, y+3, fill=color, width=w, tags=tags)
        canvas.create_line(x+3, y+10, x+3, y+3, fill=color, width=w, tags=tags)
        canvas.create_line(x-3, y+3, x+3, y+3, fill=color, width=w, tags=tags)
    elif type == "history": 
        canvas.create_oval(x-9, y-9, x+9, y+9, outline=color, width=w, tags=tags)
        canvas.create_line(x, y-5, x, y, fill=color, width=w, tags=tags)
        canvas.create_line(x, y, x+4, y+4, fill=color, width=w, tags=tags)
    elif type == "settings": 
        canvas.create_oval(x-6, y-6, x+6, y+6, outline=color, width=w, tags=tags)
        canvas.create_oval(x-2, y-2, x+2, y+2, fill=color, outline="", tags=tags)
        canvas.create_line(x, y-9, x, y+9, fill=color, width=w, tags=tags)
        canvas.create_line(x-9, y, x+9, y, fill=color, width=w, tags=tags)
        d = 6
        canvas.create_line(x-d, y-d, x+d, y+d, fill=color, width=w, tags=tags)
        canvas.create_line(x-d, y+d, x+d, y-d, fill=color, width=w, tags=tags)