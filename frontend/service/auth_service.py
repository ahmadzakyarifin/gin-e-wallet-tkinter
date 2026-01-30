import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AuthService:
    def __init__(self):
        # Ambil URL dari .env, default ke localhost
        self.BASE_URL = os.getenv("API_URL", "http://localhost:8080/api/v1")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.TIMEOUT = 10

    def login(self, username, password):
        try:
            url = f"{self.BASE_URL}/auth/login"
            payload = {"username": username, "password": password}
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=self.TIMEOUT)
            
            # Cek apakah Content-Type adalah JSON
            if "application/json" in response.headers.get("Content-Type", ""):
                data = response.json()
                if response.status_code == 200:
                    return data  # Kembalikan data lengkap termasuk token dan user info
                else:
                    print(f"[Login Failed] {data.get('error')}")
                    return None
            else:
                # Jika bukan JSON, print teks mentahnya (bisa jadi error 404 atau 500)
                print(f"[Server Error] Respon bukan JSON: {response.text}")
                return None
                
        except Exception as e:
            print(f"[System Error] {str(e)}")
            return None

    def register(self,username, email, password, no_hp):
        try:
            url = f"{self.BASE_URL}/auth/register"
            payload = {
                "username": username,
                "email": email,
                "password": password,
                "no_hp": no_hp
            }
            response = requests.post(url, json=payload, headers=self.headers, timeout=self.TIMEOUT)
            data = response.json()

            if response.status_code == 201: 
                return True, "Registrasi Berhasil, Silakan Login"
            else:
                return False, data.get("error", "Gagal Registrasi")
        except Exception as e:
            return False, f"Terjadi kesalahan: {str(e)}"

    def initiate_forgot_password(self, email):
        # Todo: Hit endpoint backend jika sudah tersedia
        return True, "1234" # Dummy OTP

    def reset_password(self, email, new_pass):
        # Todo: Hit endpoint backend jika sudah tersedia
        return True, "Password berhasil diubah"