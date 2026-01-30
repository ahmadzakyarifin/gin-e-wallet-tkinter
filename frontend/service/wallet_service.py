import os
import requests
from dotenv import load_dotenv

load_dotenv()

class WalletService:
    def __init__(self, token=None):
        # Ambil URL dari .env
        self.BASE_URL = os.getenv("API_URL", "http://localhost:8080/api/v1")
        
        self.token = token

        self.TIMEOUT = 10 
    @property
    def headers(self):
        """Menghasilkan header terbaru dengan token yang aktif saat ini"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _handle_request_error(self, e):
        """Helper internal untuk menangani error koneksi"""
        print(f"[API Error] {e}")
        if isinstance(e, requests.exceptions.ConnectionError):
            return False, "Gagal terhubung ke server. Pastikan Backend Golang menyala."
        if isinstance(e, requests.exceptions.Timeout):
            return False, "Koneksi timeout. Server tidak merespon."
        return False, f"Terjadi kesalahan: {str(e)}"

    # --- 1. USER DATA ---
    def get_current_user_data(self):
        try:
            url = f"{self.BASE_URL}/user/me"
            response = requests.get(url, headers=self.headers, timeout=self.TIMEOUT)

            if response.status_code == 200:
                result = response.json()
                return result.get("data", {})
            elif response.status_code == 401:
                print("Token Expired atau Invalid")
                return None
            else:
                return None
        except Exception as e:
            self._handle_request_error(e)
            return None

    # --- 2. UPDATE PROFILE ---
    def update_info(self, key, value):
        try:
            url = f"{self.BASE_URL}/user/update"
            payload = { key: value }
            
            response = requests.put(url, json=payload, headers=self.headers, timeout=self.TIMEOUT)
            result = response.json()

            if response.status_code == 200:
                return True, result.get("message", "Data berhasil diperbarui")
            else:
                return False, result.get("message", "Gagal update data")
        except Exception as e:
            return self._handle_request_error(e)

    # --- 3. TRANSFER ---
    def process_transfer(self, target_number, amount, notes):
        try:
            url = f"{self.BASE_URL}/transfer"
            payload = {
                "target_account": target_number,
                "amount": int(amount),
                "notes": notes
            }
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=self.TIMEOUT)
            result = response.json()

            if response.status_code == 200:
                return True, result.get("message", "Transfer Berhasil")
            else:
                return False, result.get("error", result.get("message", "Gagal Transfer"))
        except Exception as e:
            return self._handle_request_error(e)

    # --- 4. TOP UP ---
    def process_topup(self, amount, method):
        try:
            url = f"{self.BASE_URL}/topup"
            payload = {
                "amount": int(amount),
                "method": method
            }
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=self.TIMEOUT)
            result = response.json()

            if response.status_code == 200:
                return True, result.get("message", "Permintaan Top Up diterima")
            else:
                return False, result.get("message", "Gagal Top Up")
        except Exception as e:
            return self._handle_request_error(e)

    # --- 5. TARIK TUNAI ---
    def process_withdraw(self, amount, admin_fee, location, code_val):
        try:
            url = f"{self.BASE_URL}/withdraw"
            payload = {
                "amount": int(amount),
                "admin_fee": int(admin_fee),
                "location": location,
                "withdraw_code": code_val 
            }
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=self.TIMEOUT)
            result = response.json()

            if response.status_code == 200:
                return True, "Kode Tarik Tunai Siap Digunakan"
            else:
                return False, result.get("message", "Gagal Tarik Tunai")
        except Exception as e:
            return self._handle_request_error(e)

    # --- 6. PPOB (Pulsa & Token) ---
    def process_ppob(self, tipe, data_transaksi):
        try:
            url = f"{self.BASE_URL}/ppob"
            
       
            target_number = data_transaksi.get('nomor_tujuan') or data_transaksi.get('nomor_meter')
            
            payload = {
                "type": tipe, # 'pulsa' atau 'token'
                "number": target_number,
                "amount": int(data_transaksi.get('harga', 0)),
                "provider": data_transaksi.get('provider', 'PLN'),
                "generated_token": data_transaksi.get('token', '') 
            }
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=self.TIMEOUT)
            result = response.json()

            if response.status_code == 200:
                return True, "Transaksi Berhasil"
            else:
                return False, result.get("message", "Transaksi Gagal")
        except Exception as e:
            return self._handle_request_error(e)