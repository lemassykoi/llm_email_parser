from exchangelib import Credentials, Account, Mailbox
from dotenv import load_dotenv
import os
from password_manager import load_key, decrypt_password
import json
from ollama import Client, chat, ChatResponse

DEBUG = False

USERNAME = 'John DOE'
LLM_MODEL_NAME = 'llama3.2:latest'
LLM_BASE_URL = 'http://127.0.0.1:11434'

client = Client(host=LLM_BASE_URL)

def classify_email_with_llm(email_content):
    # Define possible labels/categories for classification
    categories = [
        'Advertisement / Commercial / Information / Newsletter',
        'Human / Support Asking / Existing Customer',
        'Log / Syslog / Notification',
        f'A Reply to an email sent by {USERNAME}',
        'Urgent Request - Needs Immediate Response',
        'Meeting / Appointment Request',
        'Technical Issue - Requires Investigation',
        'General Inquiry - Needs Response'
    ]

    # Construct the prompt for LLM classification
    prompt = (
        "TASK: You are an email classifier. Your job is to analyze the email below and classify it into exactly one category.\n\n"
        "AVAILABLE CATEGORIES:\n"
        f"{chr(10).join([f'- {cat}' for cat in categories])}\n\n"
        "INSTRUCTIONS:\n"
        "1. Read the email content carefully\n"
        "2. Choose EXACTLY ONE category from the list above\n"
        "3. Determine if the email needs a response from the recipient\n"
        "4. Assess the urgency level (low/medium/high)\n"
        "5. Provide your reasoning\n\n"
        "OUTPUT FORMAT: Return ONLY a valid JSON object with these exact keys:\n"
        "{\n"
        '  "category": "one of the categories from the list above",\n'
        '  "confidence_score": 0.95,\n'
        '  "reasoning": "brief explanation of why you chose this category",\n'
        '  "needs_response": true,\n'
        '  "urgency_level": "low"\n'
        "}\n\n"
        f"EMAIL TO CLASSIFY:\n{email_content}"
    )

    try:
        response: ChatResponse = client.chat(
            model=LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": f"You are an email classification assistant for {USERNAME}. You ONLY classify emails - you do not generate, write, or suggest email content. You must respond with a valid JSON object containing the classification results."},
                {"role": "user", "content": prompt}
            ],
            format="json",
        )

        # Extract and parse the JSON content from the response
        if response.message.content:
            json_output = json.loads(response.message.content.strip())
            print(json_output) # For debugging/logging
            return json_output
        else:
            raise ValueError("No content found in API response")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from LLM response: {e}")
        print(f"Raw LLM response content: {response.message.content}")
        # Try to extract JSON from response if it's embedded in other text
        try:
            import re
            json_match = re.search(r'\{.*\}', response.message.content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                json_output = json.loads(json_str)
                print(f"Successfully extracted JSON from response")
                return json_output
        except:
            pass
        return None
    except Exception as e:
        print(f"Error during classification: {str(e)}")
        return None


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
inbox = account.inbox.all()
for item in inbox.order_by("-datetime_received")[:5]:
    #print(item.subject, item.sender, item.datetime_received)
    #print(item)
    for attribute in dir(item):
        if not (attribute.startswith('_') or attribute in [
            'to_xml',
            'to_id',
            'unique_body',
            'soft_delete',
            'send_and_save',
            'send',
            'save',
            'reply',
            'reply_all',
            'refresh',
            'move_to_trash',
            'move',
            'mime_content',
            'forward',
            'mark_as_junk',
            'create_reply_all',
            'create_forward',
            'copy',
            'create_reply',
            'delete',
            'detach',
            'clean',
            'archive',
            'attach',
            'id',
            'id_from_xml',
            'get_field_by_fieldname',
            'from_xml',
            'effective_rights',
            'deregister',
            'conversation_index',
            'conversation_id',
            'changekey',
            'attribute_fields',
            'add_field',
            'validate_field',
            'supported_fields',
            'response_tag',
            'response_objects',
            'request_tag',
            'remove_field',
            'register',
            'received_representing',
            'parent_folder_id',
            'message_id',
            'item_class',
            'web_client_read_form_query_string',
            'NAMESPACE',
            'FIELDS',
            'ID_ELEMENT_CLS'
            ]):

            if DEBUG:
                value = getattr(item, attribute)
                if value is not None:
                    print(f"\033[1;32m{attribute}\033[0m")
                    print(f"\033[1;34m{value}\033[0m")
                    print('=' * 50)

    ## essentials:
    email_datetime = item.datetime_received
    email_subject = item.subject
    email_sender = item.sender
    email_sender_address = item.sender.email_address
    email_textbody = item.text_body
    email_recipient = item.to_recipients
    email_recipient_address = item.to_recipients[0].email_address
    email_has_been_read = item.is_read


    if not email_has_been_read:
        message = f"""Incoming email from {email_sender_address} for {email_recipient_address} at {email_datetime}\n- Email Subject:\n```\n{email_subject}\n```\n- Email Content:\n```\n{email_textbody}\n```\n"""
        print("=" *75)
        #print(f"\033[1;32m{message}\033[0m")
        llm_answer = classify_email_with_llm(email_textbody)
        #print(llm_answer)
        print(llm_answer.get('category'))

    # Optional
    email_mime_content = item.mime_content
    email_headers = item.headers
