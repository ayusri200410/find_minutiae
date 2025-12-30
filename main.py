import customtkinter as ctk
import os
from tkinter import messagebox

# Import modul yang sudah dipisahkan
from db_manager import init_db
from components.sidebar import Sidebar
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.cari_minutiae import CariMinutiaePage, HasilEkstraksiPage
from pages.riwayat_page import RiwayatPencarianPage, DetailPage, EditPage
from pages.register_page import RegisterPage
from pages.user_management import UserManagementPage, UserDetailPage, UserEditPage, TambahUserPage


# --- KONFIGURASI APLIKASI ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

APP_NAME = "Find Minutiae"
# Rasio 16:9 (HD)
WIDTH = 1280
HEIGHT = 720
ICON_PATH = "assets/icon.png"
DUMMY_IMAGE_PATH = "assets/fingerprint_dummy.jpg"

# Pastikan folder assets dan images ada
os.makedirs("images_for_models", exist_ok=True)
os.makedirs("images", exist_ok=True)
os.makedirs("assets", exist_ok=True)


# --- FRAME UTAMA: APP (Controller) ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # INISIALISASI FONT
        self.FONT_UTAMA = ctk.CTkFont(family="assets/fonts/Inter/Inter_18pt-Regular.ttf", size=14)
        self.FONT_BOLD = ctk.CTkFont(family="assets/fonts/Inter/Inter-VariableFont.opsz,wght.ttf", size=14, weight="normal")
        self.FONT_JUDUL = ctk.CTkFont(family="assets/fonts/Inter/Inter-VariableFont.opsz,wght.ttf", size=20, weight="bold")
        self.FONT_SUBJUDUL = ctk.CTkFont(family="assets/fonts/Inter/Inter_18pt-Bold.ttf", size=16)

        self.BACKGROUND_COLOR = "#F6F7F9"
        self.WHITE_TEXT_COLOR = "#FFFFFF"
        self.CARD_COLOR = "#FFFFFF"
        self.TEXT_COLOR = "#2A2B35"
        self.SECONDARY_TEXT_COLOR_LIGHT = "#93959F"
        self.SECONDARY_TEXT_COLOR = "#616269"
        self.BORDER_COLOR = "#EBE8E8"
        self.BUTTON_COLOR = "#397FFA"
        self.BUTTON_HOVER_COLOR = "#1f6aa5"
        self.HOVER_SIDEBAR_COLOR = "#E4E9F5"
        self.ACTIVE_SIDEBAR_COLOR = "#D0DAF4"
        self.SIDEBAR_COLOR = "#13143F"
        self.BUTTON_HOVER_COLOR = "#9ABFFE"
        self.ERROR_COLOR = "#FF4D4D"
        self.SUCCESS_COLOR = "#28A745"
        self.WARNING_COLOR = "#FFC107"
        self.INFO_COLOR = "#17A2B8"
        self.DANGER_COLOR = "#DC3545"
        self.DANGER_HOVER_COLOR = "#C82333"
        self.SUCCESS_COLOR = "#28A745"
        self.SUCCESS_HOVER_COLOR = "#218838"
        self.WARNING_COLOR = "#FFC107"
        self.INFO_COLOR = "#17A2B8"


        # Inisialisasi Database
        init_db()

        # --- TAMBAHAN: DAFTARKAN USER ADMIN PERTAMA (Jalankan hanya sekali!) ---
        from db_manager import register_user

        # Coba daftarkan user 'admin' dengan password '123'
        if register_user("admin", "123"):
            print("User 'admin' berhasil didaftarkan.")
        else:
            print("User 'admin' sudah ada atau gagal didaftarkan.")

        self.title(APP_NAME)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Inisialisasi state aplikasi
        self.frames = {}
        self.current_sidebar = None
        self.current_frame = None
        self.logged_in_user_id = None
        self.logged_in_user_name = None

        # Inisialisasi container frame (tempat semua page ditumpuk)
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Mulai dari halaman Login
        self.show_frame("Login")

    def show_frame(self, page_name, data=None):
        """
        Tampilkan halaman/page berdasarkan nama.
        page_name: "Login", "Register", "Home", "CariMinutiae", dst.
        data: dict opsional untuk dilempar ke page.load_data()
        """

        # 1. Buat instance halaman kalau belum ada
        if page_name not in self.frames:
            if page_name == "Login":
                frame = LoginPage(parent=self.container, controller=self)
            elif page_name == "Register":
                frame = RegisterPage(parent=self.container, controller=self)
            elif page_name == "Home":
                frame = HomePage(parent=self.container, controller=self)
            elif page_name == "CariMinutiae":
                frame = CariMinutiaePage(parent=self.container, controller=self)
            elif page_name == "HasilEkstraksi":
                frame = HasilEkstraksiPage(parent=self.container, controller=self)
            elif page_name == "RiwayatPencarian":
                frame = RiwayatPencarianPage(parent=self.container, controller=self)
            elif page_name == "DetailPage":
                frame = DetailPage(parent=self.container, controller=self)
            elif page_name == "EditPage":
                frame = EditPage(parent=self.container, controller=self)
            elif page_name == "UserManagement":
                frame = UserManagementPage(parent=self.container, controller=self)
            elif page_name == "UserDetail":
                frame = UserDetailPage(parent=self.container, controller=self)
            elif page_name == "UserEdit":
                frame = UserEditPage(parent=self.container, controller=self)
            elif page_name == "TambahUser":
                frame = TambahUserPage(parent=self.container, controller=self)
            else:
                return

            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        frame = self.frames[page_name]

        # 2. Konfigurasi Sidebar dan Grid Utama
        if page_name not in ("Login", "Register") and getattr(self, "logged_in_user_id", None) is not None:
            # Layout: 2 kolom (0=sidebar, 1=container)
            self.grid_columnconfigure(0, weight=0)  # sidebar lebar tetap
            self.grid_columnconfigure(1, weight=1)  # konten ambil sisa ruang

            # Buat sidebar jika belum ada
            if self.current_sidebar is None:
                self.current_sidebar = Sidebar(self, self)
                self.current_sidebar.grid(row=0, column=0, sticky="ns", padx=(10, 0), pady=10)

            # Pindahkan container ke kolom 1
            self.container.grid_forget()
            self.container.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

            # Tandai menu aktif di sidebar
            self.current_sidebar.set_active(page_name.replace("Page", ""))

            # Refresh data jika page punya fungsi ini
            if hasattr(frame, "refresh_data"):
                frame.refresh_data()
            if hasattr(frame, "load_data") and data is not None:
                frame.load_data(data)

        else:
            # Halaman Login / Register → layout 1 kolom penuh
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=0)

            # Sembunyikan sidebar jika ada
            if self.current_sidebar is not None:
                self.current_sidebar.grid_forget()
                self.current_sidebar = None

            # Container penuh di kolom 0
            self.container.grid_forget()
            self.container.grid(row=0, column=0, sticky="nsew")

            # Kalau Login/Register butuh data (jarang, tapi aman):
            if hasattr(frame, "load_data") and data is not None:
                frame.load_data(data)

        # 3. Naikkan frame yg dipilih
        self.current_frame = frame
        frame.tkraise()

    def login_success(self, user_id):
        """Dipanggil setelah login berhasil."""
        # Simpan ID user
        self.logged_in_user_id = user_id
        self.logged_in_user_level = 0      # default, nanti ditimpa
        self.logged_in_user_name = None    # default
        print("[DEBUG] login_success: logged_in_user_id =", self.logged_in_user_id)

        # Ambil data lengkap user dari database
        try:
            from db_manager import get_user_by_id
            u = get_user_by_id(user_id)
            print("[DEBUG] login_success: user from db =", u)

            if u:
                # simpan nama user
                self.logged_in_user_name = u.get("full_name") or u.get("username")

                # simpan level user (0=user biasa, 1=admin)
                self.logged_in_user_level = u.get("level", 0)

        except Exception as e:
            print("[DEBUG] login_success: get_user_by_id error:", e)

        # Update sidebar sesuai level
        try:
            if hasattr(self, "sidebar") and hasattr(self.sidebar, "update_admin_menu"):
                self.sidebar.update_admin_menu()
        except Exception as e:
            print("[DEBUG] login_success: update_admin_menu error:", e)

        # Pindah halaman
        self.show_frame("Home")


    def logout(self):
        """Log out user dan kembali ke halaman login."""
        # Bersihkan info user
        self.logged_in_user_id = None
        self.logged_in_user_name = None

        # Reset halaman yang menyimpan state user (kalau sudah pernah dibuat)
        home = self.frames.get("Home")
        if home and hasattr(home, "refresh_user"):
            home.refresh_user()

        # Key yang benar di frames adalah "CariMinutiae"
        cari = self.frames.get("CariMinutiae")
        if cari and hasattr(cari, "reset_state"):
            cari.reset_state()

        # Kembalikan layout ke single-column
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Tampilkan halaman Login
        self.show_frame("Login")

        messagebox.showinfo("Logout", "Anda telah berhasil logout.")


# --- Jalankan Aplikasi ---
if __name__ == "__main__":
    app = App()
    app.mainloop()
