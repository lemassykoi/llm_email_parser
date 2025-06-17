import os
import ast # Re-add ast for literal_eval
from dotenv import load_dotenv
from exchangelib import DELEGATE, Credentials, Account

# Load environment variables from .env file
load_dotenv()

def test_exchange_connection():
    from password_manager import load_key, decrypt_password

    # Load credentials from environment variables
    exchange_server = os.getenv('EXCHANGE_SERVER')
    exchange_user = os.getenv('EXCHANGE_USER')
    encrypted_exchange_password_str = os.getenv('ENCRYPTED_EXCHANGE_PASSWORD', '').strip() # Strip whitespace
    target_email_account = os.getenv('TARGET_EMAIL_ACCOUNT')

    if not all([exchange_server, exchange_user, encrypted_exchange_password_str, target_email_account]):
        print("Missing required environment variables")
        return

    # Convert the string representation (base64) back to bytes
    try:
        # Check if the encrypted password is already in bytes format (starts with b'...)
        if encrypted_exchange_password_str.startswith('b\''):
            # Remove the 'b' prefix and quotes, then evaluate to get actual bytes
            encrypted_exchange_password = eval(encrypted_exchange_password_str)
        else:
            encrypted_exchange_password = encrypted_exchange_password_str.encode()
    except Exception as e:
        print(f"Error encoding encrypted password string to bytes: {e}")
        return

    if not isinstance(encrypted_exchange_password, bytes):
        print("Error: Encrypted password is not in bytes format after conversion.")
        return

    # Decrypt the password
    print('Loading Key')
    key = load_key()
    print(f"Key loaded: {key[:5]}...") # Print first few bytes of key for debugging
    print('Decrypting password')
    print(f"Encrypted password string from .env: {encrypted_exchange_password_str[:50]}...") # Print first few chars of string
    print(f"Encrypted password (bytes) after literal_eval: {encrypted_exchange_password[:50]}...") # Print first few bytes of actual bytes object
    exchange_password = decrypt_password(encrypted_exchange_password, key)

    # Create credentials and account
    print('credentials')
    credentials = Credentials(exchange_user, exchange_password)
    try:
        account = Account(
            target_email_account,
            credentials=credentials,
            autodiscover=True,
            access_type=DELEGATE
        )

        # Fetch the last received email (if any)
        print('inbox')
        inbox = account.inbox.all()

        if inbox:
            print('=== Inbox not empty')
            n = 1
            for item in inbox.order_by("-datetime_received")[:10]:
                # debug
                #print(item.subject, item.sender, item.datetime_received)

                print(f"== Email n°{n}:")
                print(f"  Subject: {item.subject}")
                print(f"  From:    {item.sender.email_address}")
                print(f"  Date:    {item.datetime_received}")
                print('=' * 100)
                n += 1

        else:
            print('=== No emails found')

    except Exception as e:
        print(f"Error connecting to Exchange server: {str(e)}")

if __name__ == "__main__":
    test_exchange_connection()
