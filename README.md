# LLM Email Parser for Exchange

An intelligent email classification system that connects to Microsoft Exchange servers and uses Large Language Models (LLM) to automatically categorize incoming emails.

## Features

- **Exchange Integration**: Connects to Microsoft Exchange servers using exchangelib
- **LLM Classification**: Uses Ollama (local) or OpenAI to classify emails into predefined categories
- **Secure Authentication**: Encrypts Exchange passwords using Fernet encryption
- **Scheduled Processing**: Can run continuously with configurable intervals (default: 15 minutes)
- **Comprehensive Logging**: Detailed logging to both console and file
- **Flexible Configuration**: Environment-based configuration with .env file

## Email Categories

The system classifies emails into four categories:
1. **Advertisement / Commercial / Information / Newsletter**
2. **Human / Support Asking / Existing Customer**
3. **Log / Syslog / Notification**
4. **A Reply to an email sent by [USERNAME]**

## Installation

1. Clone the repository:
```bash
git clone https://github.com/lemassykoi/llm_email_parser_for_exchange.git
cd llm_email_parser_for_exchange
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables by creating a `.env` file:
```bash
EXCHANGE_SERVER=your.exchange.server.com
EXCHANGE_USER=your.username
TARGET_EMAIL_ACCOUNT=email@domain.com
MAIL_USER_NAME=Your Name
LLM_MODEL_NAME=llama3.2:latest
LLM_BASE_URL=http://127.0.0.1:11434
# Optional: For OpenAI instead of Ollama
# OPENAI_API_KEY=your_openai_api_key
# OPENAI_BASE_URL=http://127.0.0.1:11434/v1
```

4. Encrypt your Exchange password:
```bash
python password_manager.py
```
This will generate a `secret.key` file and add the encrypted password to your `.env` file.

## Usage

### One-time Processing
Process emails once and exit:
```bash
python main.py
```

### Scheduled Processing
For continuous monitoring, uncomment `run_scheduler()` in `main.py` and run:
```bash
python main.py
```

### Testing Connection
Test your Exchange connection:
```bash
python test_exchange_connection.py
```

### Individual Components
Test individual components:
```bash
python exchange_client.py    # Test email fetching
python classifier.py         # Test email classification
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EXCHANGE_SERVER` | Exchange server hostname | - |
| `EXCHANGE_USER` | Exchange username | - |
| `TARGET_EMAIL_ACCOUNT` | Email account to monitor | - |
| `ENCRYPTED_EXCHANGE_PASSWORD` | Encrypted password (generated automatically) | - |
| `MAIL_USER_NAME` | User name for classification context | - |
| `LLM_MODEL_NAME` | LLM model to use | `llama3.2:latest` |
| `LLM_BASE_URL` | Ollama server URL | `http://127.0.0.1:11434` |
| `OPENAI_API_KEY` | OpenAI API key (if using OpenAI) | - |

### LLM Options

**Ollama (Default)**
- Install Ollama locally
- Pull your desired model: `ollama pull llama3.2:latest`
- Ensure Ollama is running on the configured port

**OpenAI**
- Set `OPENAI_API_KEY` in your `.env` file
- Modify `classifier.py` to use `classify_email_with_openai()` instead of `classify_email_with_llm()`

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   main.py       │    │  exchange_client │    │   classifier    │
│   (Scheduler)   │───▶│  (Email Fetch)   │───▶│   (LLM Class)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ classification  │    │   Exchange       │    │   Ollama/OpenAI │
│     .log        │    │    Server        │    │      LLM        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Security

- Passwords are encrypted using Fernet (symmetric encryption)
- Encryption key is stored in `secret.key` file
- Never commit secrets to version control
- Use environment variables for all sensitive configuration

## Development

### Running Tests
```bash
python test_exchange_connection.py
python test_encrypted_exchangelib.py
python test_simple_exchangelib.py
```

### Adding New Categories
1. Modify the `categories` list in `classifier.py`
2. Update the classification prompt accordingly
3. Test with sample emails

### Debugging
- Check `classification.log` for detailed operation logs
- Use individual component tests to isolate issues
- Verify Exchange connection before testing classification

## Troubleshooting

**Connection Issues**
- Verify Exchange server settings and credentials
- Check if autodiscovery is working for your Exchange server
- Ensure proper network connectivity

**Classification Issues**
- Verify LLM service is running (Ollama/OpenAI)
- Check model availability and API keys
- Review classification prompts and categories

**Permission Issues**
- Ensure Exchange account has appropriate permissions
- Check if target email account allows delegation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
