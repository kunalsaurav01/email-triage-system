# AI-Powered Email Triage System

## Overview

This project implements an automated email triage system that reads incoming emails, classifies them using Google's Gemini AI, and sends intelligent alerts to Slack channels. The system is designed for small startups that need to efficiently handle customer support emails.

## Features

### Core Features
- **Automated Email Reading**: Connects to IMAP email servers (Gmail, Outlook, etc.)
- **AI-Powered Classification**: Uses Google Gemini AI to classify emails into 3 categories:
  - Product Support
  - Billing
  - General Inquiry
- **Smart Summarization**: Generates concise one-sentence summaries for each email
- **Slack Integration**: Sends formatted alerts to appropriate Slack channels
- **Fallback Classification**: Keyword-based backup when AI is unavailable

### Additional Features
- **Keyword Analytics**: Tracks top 5 keywords per category
- **Data Logging**: Saves all processed emails to CSV files
- **Analytics Reports**: Generates JSON reports with insights
- **Error Handling**: Robust error handling and fallback mechanisms
- **Rate Limiting**: Prevents API abuse with built-in delays

## Architecture

### Workflow Design

```
Email Server (IMAP) → Python Script → Gemini AI → Slack Webhook
                          ↓
                    CSV/JSON Logging
                          ↓
                   Analytics Generation
```

### System Components

1. **Email Connector**: IMAP client for reading emails
2. **AI Classifier**: Gemini AI integration for classification and summarization
3. **Slack Notifier**: Webhook-based Slack messaging
4. **Analytics Engine**: Keyword analysis and reporting
5. **Data Logger**: CSV and JSON file management

## Prerequisites

- Python 3.8 or higher
- Gmail account with App Password (or other IMAP email)
- Google Gemini AI API key
- Slack workspace with webhook permissions

## Installation and Setup

### Step 1: Clone/Download Project Files

Create a new folder and save these files:
- `email_triage.py` (main application)
- `config.json` (configuration template)
- `requirements.txt` (Python dependencies)
- `setup.py` (setup script)
- `.env` (environment variables template)

### Step 2: Install Dependencies

Open VS Code terminal and run:

```bash
# Install required packages
pip install -r requirements.txt
```

### Step 3: Get API Keys and Credentials

#### Google Gemini AI API Key:
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the API key for configuration

#### Gmail App Password:
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account Settings → Security → 2-Step Verification
3. Generate an App Password for "Mail"
4. Use this password (not your regular Gmail password)

#### Slack Webhook URL:
1. Go to [Slack API](https://api.slack.com/apps)
2. Create a new app → "From scratch"
3. Select your workspace
4. Go to "Incoming Webhooks" → Activate
5. Click "Add New Webhook to Workspace"
6. Select channels and copy the webhook URL

### Step 4: Configure the System

#### Option A: Use Setup Script
```bash
python setup.py
```
This will guide you through the configuration process.

#### Option B: Manual Configuration

Edit `config.json`:
```json
{
  "gemini_api_key": "your_actual_gemini_api_key",
  "email_server": "imap.gmail.com",
  "email_port": 993,
  "email_username": "your-email@gmail.com",
  "email_password": "your-app-password",
  "slack_webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "slack_channels": {
    "Product Support": "#product-support",
    "Billing": "#billing",
    "General Inquiry": "#general"
  }
}
```

## Running the System

### In VS Code:

1. **Open VS Code** in your project folder
2. **Open Terminal** (Terminal → New Terminal)
3. **Run the main script**:
```bash
python email_triage.py
```

### Expected Output:
```
🚀 Starting Email Triage System...
✓ Successfully connected to email server
✓ Fetched 5 unread emails
📧 Processing 5 emails...

--- Processing: Customer complaint about login issues...
✓ Classified email as: Product Support
✓ Slack notification sent to #product-support

--- Processing: Question about my invoice...
✓ Classified email as: Billing
✓ Slack notification sent to #billing

📊 Generating reports...
✓ Data saved to email_triage_log_20240923_143022.csv
✓ Analytics report saved to analytics_report_20240923_143022.json

📈 Analytics Summary:
Product Support: 2 emails
  Top keywords: login, error, account
Billing: 1 emails
  Top keywords: invoice, payment
General Inquiry: 2 emails
  Top keywords: question, help

✅ Successfully processed 5 emails!
```

## File Structure

```
email-triage-system/
├── email_triage.py          # Main application
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── setup.py                 # Setup and testing script
├── .env                     # Environment variables (optional)
├── README.md               # This documentation
├── email_triage_log_*.csv  # Generated email logs
└── analytics_report_*.json # Generated analytics
```

## Configuration Options

### Email Settings:
- `email_server`: IMAP server (default: imap.gmail.com)
- `email_port`: IMAP port (default: 993)
- `email_username`: Your email address
- `email_password`: App-specific password

### AI Settings:
- `gemini_api_key`: Google Gemini AI API key

### Slack Settings:
- `slack_webhook_url`: Slack incoming webhook URL
- `slack_channels`: Channel mapping for each category

## Output Files

### CSV Log File (`email_triage_log_YYYYMMDD_HHMMSS.csv`)
```csv
timestamp,category,summary,sender,subject
2024-09-23T14:30:22,Product Support,User reports login issues with mobile app,customer@example.com,Can't login on mobile
2024-09-23T14:31:15,Billing,Customer inquires about invoice charges,billing@company.com,Question about my invoice
```

### Analytics Report File (`analytics_report_YYYYMMDD_HHMMSS.json`)
```json
{
  "generated_at": "2024-09-23T14:32:00",
  "total_emails_processed": 5,
  "categories": {
    "Product Support": {
      "top_keywords": [["login", 3], ["error", 2], ["mobile", 2], ["app", 1], ["account", 1]],
      "total_emails": 2
    },
    "Billing": {
      "top_keywords": [["invoice", 2], ["payment", 1], ["charge", 1]],
      "total_emails": 1
    },
    "General Inquiry": {
      "top_keywords": [["question", 2], ["help", 1], ["information", 1]],
      "total_emails": 2
    }
  },
  "summary": {
    "most_active_category": "Product Support",
    "processing_period": {
      "start": "2024-09-23T14:30:22",
      "end": "2024-09-23T14:31:45"
    }
  }
}
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Gmail Authentication Error
**Error**: `Authentication failed`
**Solution**: 
- Enable 2-Factor Authentication on Gmail
- Generate and use an App Password instead of your regular password
- Make sure "Less secure app access" is disabled (use App Passwords instead)

#### 2. Gemini AI API Error
**Error**: `API key not valid`
**Solution**:
- Verify your API key at [Google AI Studio](https://aistudio.google.com/app/apikey)
- Check that the API key has proper permissions
- Ensure you're not exceeding rate limits

#### 3. Slack Webhook Error
**Error**: `Failed to send Slack notification: 404`
**Solution**:
- Verify your webhook URL is correct
- Check that the Slack app is properly installed in your workspace
- Ensure the channels mentioned in config exist

#### 4. No Emails Found
**Error**: `No unread emails found`
**Solution**:
- Check that there are actually unread emails in your inbox
- Verify IMAP is enabled for your email account
- Test with a different email account

#### 5. Module Import Error
**Error**: `ModuleNotFoundError: No module named 'google.generativeai'`
**Solution**:
```bash
pip install --upgrade google-generativeai
pip install -r requirements.txt
```

### Testing Individual Components

You can test individual components using Python:

```python
# Test Gemini AI connection
import google.generativeai as genai
genai.configure(api_key="your_api_key")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Test message")
print(response.text)

# Test email connection
import imaplib
mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
mail.login('your_email', 'your_app_password')
print("Email connection successful!")
mail.logout()
```

## Customization Options

### 1. Adding New Categories

Edit the `categories` list in `EmailTriageSystem.__init__()`:
```python
self.categories = ["Product Support", "Billing", "General Inquiry", "Sales", "Technical"]
```

Update Slack channels in `config.json`:
```json
"slack_channels": {
  "Product Support": "#product-support",
  "Billing": "#billing",
  "General Inquiry": "#general",
  "Sales": "#sales",
  "Technical": "#technical"
}
```

### 2. Custom Email Filters

Modify the `fetch_unread_emails()` method to change email filtering:
```python
# Only emails from today
status, messages = mail.search(None, 'UNSEEN', 'SINCE', date.today().strftime("%d-%b-%Y"))

# Only emails with specific subject
status, messages = mail.search(None, 'UNSEEN', 'SUBJECT', '"customer support"')
```

### 3. Enhanced Summarization

Update the AI prompt in `classify_and_summarize_email()`:
```python
prompt = f"""
Analyze this customer email and:
1. Classify into: Product Support, Billing, or General Inquiry
2. Rate urgency: Low, Medium, High
3. Generate summary with sentiment analysis

Email: {email_data['subject']} - {email_data['body'][:500]}

Format:
Category: [category]
Urgency: [urgency]
Sentiment: [positive/neutral/negative]
Summary: [summary]
"""
```

### 4. Additional Integrations

You can extend the system to integrate with:
- **Microsoft Teams**: Replace Slack webhook with Teams connector
- **Discord**: Use Discord webhooks
- **Jira**: Create tickets automatically
- **Google Sheets**: Log data directly to spreadsheets
- **Database**: Store data in PostgreSQL/MySQL

## Performance Considerations

### Rate Limiting
- **Gemini AI**: 60 requests per minute (free tier)
- **Email IMAP**: No strict limits, but use delays to be respectful
- **Slack Webhooks**: 1 message per second recommended

### Optimization Tips
1. **Batch Processing**: Process emails in batches rather than one-by-one
2. **Caching**: Cache AI responses for similar emails
3. **Database Storage**: Use database instead of CSV for large volumes
4. **Async Processing**: Use asyncio for better performance

### Scaling Up
For production deployment:
1. **Use a proper database** (PostgreSQL/MySQL)
2. **Implement proper logging** (using Python logging module)
3. **Add monitoring** (health checks, metrics)
4. **Deploy with Docker** for containerization
5. **Use environment variables** for sensitive data
6. **Implement retry logic** for API failures

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Implement proper authentication** for production
4. **Use HTTPS** for all webhook communications
5. **Validate and sanitize** email content before processing
6. **Monitor API usage** to detect unusual activity

## Limitations and Next Steps

### Current Limitations
1. **Email Volume**: Designed for small-medium volumes (< 1000 emails/day)
2. **Single Email Account**: Processes one email account at a time
3. **Basic Analytics**: Simple keyword counting
4. **No GUI**: Command-line interface only
5. **Synchronous Processing**: Processes emails sequentially

### Potential Improvements
1. **Web Interface**: Build a Flask/Django web app
2. **Real-time Processing**: Use webhooks instead of polling
3. **Advanced Analytics**: Machine learning for trend analysis
4. **Multi-account Support**: Handle multiple email accounts
5. **Custom Workflows**: User-defined automation rules
6. **Integration Hub**: Connect with CRM systems
7. **Mobile App**: Notifications and monitoring on mobile

### Alternative Tools Comparison

This solution compared to no-code platforms:

| Feature | This Solution | Zapier | Make.com | n8n |
|---------|---------------|---------|----------|-----|
| **Cost** | Free (API costs only) | $20+/month | $9+/month | Self-hosted free |
| **Customization** | Full control | Limited | Medium | High |
| **AI Integration** | Native Gemini | Multiple AI apps | Multiple AI apps | Custom nodes |
| **Analytics** | Built-in | Basic | Basic | Custom |
| **Scalability** | High (with optimization) | Medium | Medium | High |

## Support and Contributing

### Getting Help
1. Check the troubleshooting section above
2. Review error messages carefully
3. Test individual components separately
4. Check API documentation for rate limits

### Contributing
To contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request with clear description

## License

This project is created for the AI Engineer Fellowship evaluation task and is provided as-is for educational purposes.

---

## Quick Start Summary

1. **Install Python packages**: `pip install -r requirements.txt`
2. **Get API credentials**: Gemini AI, Gmail App Password, Slack Webhook
3. **Configure**: Edit `config.json` or run `python setup.py`
4. **Run**: `python email_triage.py`
5. **Monitor**: Check Slack channels for notifications and CSV files for logs

**That's it!** Your AI-powered email triage system is ready to handle customer emails automatically.