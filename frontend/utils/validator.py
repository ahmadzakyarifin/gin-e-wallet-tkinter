import re

class Validator:
    """
    Kumpulan fungsi validasi untuk Frontend Python.
    Memastikan data 'bersih' sebelum dikirim ke Server Golang.
    """

    @staticmethod
    def is_valid_email(email):
        """Cek format email standar (user@domain.com)"""
        if not email:
            return False
        # Regex standar untuk email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def is_valid_phone(nomor):
        """
        Cek validitas nomor HP Indonesia:
        1. Harus angka
        2. Harus diawali '08' atau '628'
        3. Panjang 10-14 digit
        """
        if not nomor or not nomor.isdigit():
            return False
        
        # Normalisasi awalan 628 -> 08 (opsional, tapi bagus untuk UX)
        if nomor.startswith("628"):
            nomor = "0" + nomor[2:]
            
        if not nomor.startswith("08"):
            return False
            
        if len(nomor) < 10 or len(nomor) > 14:
            return False
            
        return True

    @staticmethod
    def is_valid_pln_number(nomor):
        """Cek ID Pelanggan / No Meter PLN (11-12 digit angka)"""
        if not nomor or not nomor.isdigit():
            return False
        return 11 <= len(nomor) <= 12

    @staticmethod
    def is_valid_password(password):
        """
        Cek kekuatan password (biasanya untuk Register):
        - Minimal 8 karakter
        - Tidak boleh kosong
        """
        if not password:
            return False
        if len(password) < 8:
            return False
        return True

    @staticmethod
    def is_valid_username(username):
        """
        Cek username:
        - Hanya huruf, angka, dan underscore
        - Tidak boleh spasi
        - Min 4 karakter
        """
        if not username:
            return False
        pattern = r'^[a-zA-Z0-9_]{4,}$'
        return bool(re.match(pattern, username))

    @staticmethod
    def get_operator_name(nomor):
        """
        (Bonus) Menebak nama operator dari Prefix Nomor HP.
        Berguna untuk Auto-Select operator di UI Pulsa.
        """
        if not Validator.is_valid_phone(nomor):
            return None

        prefix = nomor[:4]
        
        # Daftar Prefix Operator Indonesia
        telkomsel = ["0811", "0812", "0813", "0821", "0822", "0823", "0852", "0853"]
        indosat   = ["0814", "0815", "0816", "0855", "0856", "0857", "0858"]
        xl        = ["0817", "0818", "0819", "0859", "0877", "0878"]
        axis      = ["0831", "0832", "0833", "0838"]
        tri       = ["0895", "0896", "0897", "0898", "0899"]
        smartfren = ["0881", "0882", "0883", "0884", "0885", "0886", "0887", "0888", "0889"]

        if prefix in telkomsel: return "Telkomsel"
        if prefix in indosat:   return "Indosat"
        if prefix in xl:        return "XL"
        if prefix in axis:      return "Axis"
        if prefix in tri:       return "Tri"
        if prefix in smartfren: return "Smartfren"
        
        return "Unknown"

is_valid_email = Validator.is_valid_email
is_valid_phone = Validator.is_valid_phone
is_valid_pln_number = Validator.is_valid_pln_number
is_valid_password = Validator.is_valid_password
is_valid_username = Validator.is_valid_username
detect_operator = Validator.get_operator_name