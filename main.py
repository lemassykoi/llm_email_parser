import os
import time
import logging
import schedule
from datetime import timedelta, datetime
from exchange_client import get_recent_emails
from classifier import classify_email_with_llm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("classification.log"),
        logging.StreamHandler()
    ]
)

# Get the logger for 'httpx'
httpx_logger = logging.getLogger("httpx")

# Set the logging level to WARNING to ignore INFO and DEBUG logs
httpx_logger.setLevel(logging.WARNING)

def process_and_classify_emails():
    """Main job function to fetch and classify emails."""
    try:
        logging.info("Starting email processing job...")

        # Fetch recent emails
        new_emails = get_recent_emails()

        if not new_emails:
            logging.info("No new emails found in the last 15 minutes.")
            return

        for email in new_emails:
            email_content = f"Subject: {email['subject']}\n\nBody: {email['body']}"

            # Classify the email using LLM
            label = classify_email_with_llm(email_content)

            if label is None:
                logging.warning(f"Failed to classify email from {email['sender']}")
            else:
                # Extract just the category from the JSON response
                try:
                    import json
                    label_json = json.loads(label)
                    if "category" in label_json:
                        logging.info(label_json["category"])
                    elif "type" in label_json:
                        logging.info(label_json["type"])
                    else:
                        logging.warning(f"Unexpected label format: {label}")
                except json.JSONDecodeError:
                    logging.warning(f"Failed to parse label as JSON: {label}")
    except Exception as e:
        logging.error(f"Error during processing: {str(e)}")
        # Optionally, you could send an alert or notification here

def run_scheduler():
    """Run the scheduler loop."""
    schedule.every(15).minutes.do(process_and_classify_emails)

    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for a second to avoid busy-waiting

if __name__ == "__main__":
    #run_scheduler()
    process_and_classify_emails()  # One shot pass
