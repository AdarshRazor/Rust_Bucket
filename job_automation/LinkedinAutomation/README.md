# LinkedIn Email Scraping Automation

## Project Setup

1. Create a Python virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure
```
/
├── .github/            # GitHub specific files and AI instructions
├── src/               # Source code
│   ├── scraper/       # LinkedIn scraping logic
│   ├── parser/        # Email extraction and validation
│   ├── storage/       # Data persistence
│   ├── proxy/         # Proxy management
│   └── orchestrator/  # Main coordination logic
├── tests/            # Test suite
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## Legal Notice
⚠️ **Important**: This project involves web scraping which may violate LinkedIn's Terms of Service. Always ensure compliance with legal requirements and terms of service before proceeding.
