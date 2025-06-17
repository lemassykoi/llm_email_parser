from exchangelib import Credentials, Account
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

credentials = Credentials(os.getenv('EXCHANGE_USER'), "mysecretpassword")
account = Account(os.getenv('TARGET_EMAIL_ACCOUNT'), credentials=credentials, autodiscover=True)

for item in account.inbox.all().order_by("-datetime_received")[:10]:
    print(item.subject, item.sender, item.datetime_received)
