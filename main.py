from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from datetime import datetime
import base64
from art import logo

def generate_key(date):
    hasher = SHA256.new(date.encode())
    return hasher.digest()[:16]  # Using 16 bytes (128 bits) for AES key

def encrypt_message(message):
    current_date = datetime.now().strftime("%Y%m%d")
    key = generate_key(current_date)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_message(encrypted_message):
    current_date = datetime.now().strftime("%Y%m%d")
    key = generate_key(current_date)  # Automatically use the current date
    encoded_message = base64.b64decode(encrypted_message)
    nonce, tag, ciphertext = encoded_message[:16], encoded_message[16:32], encoded_message[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# User Interface
def main_menu():
    print(logo)
    while True:
        choice = input("Do you want to (E)ncrypt or (D)ecrypt a message, or (Q)uit? ").upper()
        if choice == 'E':
            message = input("Enter the message to encrypt: ")
            encrypted = encrypt_message(message)
            print(f"Encrypted message: {encrypted}")
        elif choice == 'D':
            encrypted_message = input("Enter the message to decrypt: ")
            try:
                decrypted = decrypt_message(encrypted_message)  # No date needed
                print(f"Decrypted message: {decrypted}")
            except Exception as e:
                print(str(e))
        elif choice == 'Q':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please choose E, D, or Q.")

if __name__ == "__main__":
    main_menu()
    
