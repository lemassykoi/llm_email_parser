from exchangelib import Credentials, Account
from dotenv import load_dotenv
import os
from password_manager import load_key, decrypt_password

# Load environment variables from .env file
load_dotenv()

# Get encrypted password and decryption key
encrypted_password = os.getenv('ENCRYPTED_EXCHANGE_PASSWORD')

# Check if the encrypted password is already in bytes format (starts with b'...)
if encrypted_password.startswith('b\''):
    # Remove the 'b' prefix and quotes, then evaluate to get actual bytes
    encrypted_bytes = eval(encrypted_password)
else:
    encrypted_bytes = encrypted_password.encode()

key = load_key()
decrypted_password = decrypt_password(encrypted_bytes, key)

credentials = Credentials(os.getenv('EXCHANGE_USER'), decrypted_password)
account = Account(os.getenv('TARGET_EMAIL_ACCOUNT'), credentials=credentials, autodiscover=True)

for item in account.inbox.all().order_by("-datetime_received")[:10]:
    print(item.subject, item.sender, item.datetime_received)
