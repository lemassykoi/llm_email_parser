import os
from dotenv import load_dotenv

# Load environment variables from .env file as early as possible
load_dotenv()

from ollama import Client, ChatResponse

USERNAME = os.getenv('MAIL_USER_NAME', '')
LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME', 'llama3.2:latest')
LLM_BASE_URL = os.getenv('LLM_BASE_URL', 'http://127.0.0.1:11434')

def classify_email_with_openai(email_content):  ## OPENAI method
    # Define possible labels/categories for classification
    categories = [
        'Advertisement / Commercial / Information / Newsletter',
        'Human / Support Asking / Existing Customer',
        'Log / Syslog / Notification',
        f'A Reply to an email sent by {USERNAME}'
    ]

    # Load API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Missing OpenAI API key")

    client = OpenAI(api_key=api_key)

    # Construct the prompt for LLM classification
    prompt = (
        "Classify this email into one of these categories: "
        f"{', '.join(categories)}.\n\n"
        f"Email Content:\n{email_content}"
    )

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that classifies emails for {USERNAME}."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the predicted label from the response
        if response.choices:
            predicted_label = response.choices[0].message.content.strip()
            return predicted_label
        else:
            raise ValueError("No choice found in API response")

    except Exception as e:
        print(f"Error during classification: {str(e)}")
        return None

def classify_email_with_llm(email_content):  ## OLLAMA method
    # Define possible labels/categories for classification
    categories = [
        'Advertisement / Commercial / Information / Newsletter',
        'Human / Support Asking / Existing Customer',
        'Log / Syslog / Notification',
        f'A Reply to an email sent by {USERNAME}'
    ]

    client = Client(host=LLM_BASE_URL)

    # Construct the prompt for LLM classification
    prompt = (
        "Classify this email into one of these categories (pick one): "
        f"{', '.join(categories)}.\n\n"
        f"Email Content:\n{email_content}"
    )

    try:
        response: ChatResponse = client.chat(
            model=LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that classifies emails for {USERNAME}."},
                {"role": "user", "content": prompt}
            ],
            format="json",
        )

        print(response['message']['content'])

        # Extract the predicted label from the response
        if response.message.content:
            predicted_label = response.message.content.strip()
            return predicted_label
        else:
            raise ValueError("No choice found in API response")

    except Exception as e:
        print(f"Error during classification: {str(e)}")
        return None

if __name__ == "__main__":
    test_email_content = """
    Subject: Meeting Reminder
    Body: Hi John,
           This is a reminder about our meeting tomorrow at 10am.
           Please let me know if you can attend.
           Best, Alice
    """
    label = classify_email_with_llm(test_email_content)
    print(f"Classified as: {label}")
