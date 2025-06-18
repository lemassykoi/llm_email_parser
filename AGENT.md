# Email Parser for Exchange Agent Guide

## Commands
- **Run main application**: `python main.py` (processes emails once)
- **Test single file**: `python <filename>.py` (e.g., `python test_exchange_connection.py`)
- **Run scheduler**: Uncomment `run_scheduler()` in main.py and run `python main.py`
- **Install dependencies**: `pip install -r requirements.txt`
- **Setup encryption**: `python password_manager.py` (generates key and encrypts password)

## Architecture
- **Main modules**: main.py (scheduler), exchange_client.py (email fetching), classifier.py (LLM classification)
- **Email source**: Microsoft Exchange via exchangelib
- **LLM**: Ollama (default) or OpenAI for email classification into 4 categories
- **Security**: Fernet encryption for Exchange passwords stored in .env
- **Logging**: File-based logging to classification.log

## Code Style
- **Imports**: Standard library first, then third-party, then local imports
- **Environment**: Use .env file for secrets, load with dotenv early
- **Error handling**: Try/catch with logging, return None on failure
- **Naming**: snake_case for functions/variables, descriptive names
- **JSON**: Parse LLM responses as JSON objects with category/confidence/reasoning
- **Testing**: Individual test files for components (test_*.py pattern)
