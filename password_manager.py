import os
from cryptography.fernet import Fernet

def generate_key():
    """Generate a key and save it into a file."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """Load the previously generated key."""
    return open("secret.key", "rb").read()

def encrypt_password(password, key):
    """Encrypt a password using the provided key."""
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    """Decrypt an encrypted password using the provided key."""
    if not encrypted_password or encrypted_password == b'':
        print("Empty or invalid password")
        return None
    try:
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(encrypted_password).decode()
        return decrypted_password
    except Exception as e:
        print(f"Error decrypting password: {str(e)}")
        raise

if __name__ == "__main__":
    # Generate a key (only need to do this once)
    generate_key()

    # Encrypt the password
    password = input("Enter the Exchange password to encrypt: ")
    key = load_key()
    encrypted_password = encrypt_password(password, key)

    print(f"Encrypted Password: {encrypted_password}")

    # Save the encrypted password in .env file (in real usage, handle this more securely)
    with open(".env", "a") as env_file:
        # Store the base64 encoded string of the encrypted bytes
        env_file.write(f"\nENCRYPTED_EXCHANGE_PASSWORD={encrypted_password.decode('ascii')}\n")
