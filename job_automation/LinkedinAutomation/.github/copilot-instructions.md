# AI Agent Instructions for LinkedIn Email Scraping Automation

## Project Overview
This project is an automated system for extracting email IDs from LinkedIn posts related to "Hiring Full Stack" in India. The system is designed to handle dynamic content, implement anti-detection measures, and maintain data quality.

## Key Architecture Components
1. **Scraper Service**: Handles LinkedIn page navigation and content loading
2. **Parser Service**: Extracts and validates email addresses
3. **Data Storage Service**: Manages data persistence and deduplication
4. **Proxy Management Service**: Handles IP rotation and request routing
5. **Orchestrator**: Coordinates all services and manages the workflow

## Development Conventions

### Project Structure
```
/
├── .github/
├── src/
│   ├── scraper/       # Selenium-based scraping logic
│   ├── parser/        # Email extraction and validation
│   ├── storage/       # Data persistence layer
│   ├── proxy/         # Proxy management service
│   └── orchestrator/  # Main coordination logic
└── tests/            # Test suite directory
```

### Critical Workflows
1. **Environment Setup**:
   - Use Python virtual environment
   - Install core dependencies: selenium, webdriver-manager
   - Configure proxy settings before running

2. **Development Workflow**:
   - Always implement robust error handling
   - Use WebDriverWait for dynamic content
   - Implement randomized delays between actions

### Integration Points
1. LinkedIn website interaction via Selenium WebDriver
2. Residential proxy provider API integration
3. Local/Remote database connection for data storage

### Security & Performance Guidelines
1. Always rotate IPs and user agents
2. Implement human-like behavior patterns
3. Use efficient parsing techniques
4. Maintain session anonymity

## Testing Approach
- Unit tests for each service component
- Integration tests for service interactions
- Performance testing for anti-detection measures

## Known Limitations
- Subject to LinkedIn's anti-bot measures
- Rate limits and CAPTCHA challenges
- Dynamic page structure changes

## Legal Notice
This project involves web scraping which may violate LinkedIn's Terms of Service. Always ensure compliance with legal requirements and terms of service.
