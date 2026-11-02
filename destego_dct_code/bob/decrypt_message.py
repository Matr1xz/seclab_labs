import sys
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

def decrypt_file(encrypted_file, private_key_file):
    try:
        private_key = RSA.import_key(open(private_key_file, "rb").read())
        
        with open(encrypted_file, "rb") as f:
            encrypted_data = f.read()
        
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_data = cipher.decrypt(encrypted_data)
        
        output_file = "decrypted_file.txt"
        with open(output_file, "wb") as f:
            f.write(decrypted_data)
        
        print(f"Giai ma thanh cong: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

    
encrypted_file = sys.argv[1]
private_key_file = sys.argv[2]
decrypt_file(encrypted_file, private_key_file)

