import os
from datetime import timedelta
from exchangelib import DELEGATE, Credentials, Account, EWSDateTime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_recent_emails(minutes_ago:int = 15) -> list:
    from password_manager import load_key, decrypt_password
    # Load credentials from environment variables
    exchange_server = os.getenv('EXCHANGE_SERVER')
    exchange_user = os.getenv('EXCHANGE_USER')
    encrypted_exchange_password_str = os.getenv('ENCRYPTED_EXCHANGE_PASSWORD')
    target_email_account = os.getenv('TARGET_EMAIL_ACCOUNT')
    email_list = []

    if not all([exchange_server, exchange_user, encrypted_exchange_password_str, target_email_account]):
        raise ValueError("Missing required environment variables in .env")

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
        return email_list

    # Decrypt the password
    key = load_key()
    exchange_password = decrypt_password(encrypted_exchange_password, key)

    # Create credentials and account
    credentials = Credentials(exchange_user, exchange_password)
    account = Account(
        target_email_account,
        credentials=credentials,
        autodiscover=True,
        access_type=DELEGATE
    )

    # Calculate the time window (15 minutes ago) with timezone awareness
    now = EWSDateTime.now().astimezone()  # Make sure it's timezone aware
    time_window = now - timedelta(minutes=minutes_ago)

    # Fetch recent emails from the inbox
    inbox = account.inbox.all()
    emails = inbox.filter(datetime_received__gt=time_window)
    
    for email in emails:
        # Extract body text, handling both plain text and HTML content
        body_text = ''
        if hasattr(email.body, 'text'):
            body_text = email.body.text
        elif hasattr(email.body, 'html'):
            # If it's HTML, extract the first few lines of text for preview
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(email.body.html, 'lxml')
            body_text = soup.get_text(separator=' ', strip=True)[:100]

        email_info = {
            #'headers': email.headers, # untested
            'subject': email.subject,
            'body': body_text,
            'sender': email.sender.email_address,
            'datetime_received': email.datetime_received
        }
        email_list.append(email_info)

    return email_list

if __name__ == "__main__":
    emails = get_recent_emails()
    for email in emails:
        print(f"Subject: {email['subject']}")
        print(f"From: {email['sender']}")
        print(f"Date: {email['datetime_received']}")
        print(f"Body preview: {email['body'][:100]}...")
        print("-" * 50)
