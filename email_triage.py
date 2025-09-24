import os
import json
import csv
import re
from datetime import datetime
from collections import Counter
import imaplib
import email
from email.header import decode_header
import google.generativeai as genai
import requests
from typing import Dict, List, Tuple, Optional
import time

import os
from dotenv import load_dotenv
import json

# Load .env variables
load_dotenv()

# Optionally load config.json (overrides .env if exists)
config_path = "config.json"
if os.path.exists(config_path):
    with open(config_path) as f:
        config = json.load(f)
    # Update environment variables
    os.environ.update({
        "GEMINI_API_KEY": config.get("gemini_api_key", os.getenv("GEMINI_API_KEY")),
        "EMAIL_SERVER": config.get("email_server", os.getenv("EMAIL_SERVER")),
        "EMAIL_PORT": str(config.get("email_port", os.getenv("EMAIL_PORT"))),
        "EMAIL_USERNAME": config.get("email_username", os.getenv("EMAIL_USERNAME")),
        "EMAIL_PASSWORD": config.get("email_password", os.getenv("EMAIL_PASSWORD")),
        "SLACK_WEBHOOK_URL": config.get("slack_webhook_url", os.getenv("SLACK_WEBHOOK_URL"))
    })
    # Slack channels
    SLACK_CHANNELS = config.get("slack_channels", {})

# Access variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_SERVER = os.getenv("EMAIL_SERVER")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


class EmailTriageSystem:
    """
    AI-powered email triage system that classifies customer emails and sends alerts to Slack.
    """
    
    def __init__(self):
        # Load configuration
        self.config = self.load_config()
        
        # Initialize Gemini AI
        genai.configure(api_key=self.config['gemini_api_key'])
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Categories for classification
        self.categories = ["Product Support", "Billing", "General Inquiry"]
        
        # Storage for analytics
        self.processed_emails = []
        self.category_keywords = {cat: [] for cat in self.categories}
        
    def load_config(self) -> Dict:
        """Load configuration from environment variables or config file."""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            # Fallback to environment variables
            config = {
                'gemini_api_key': os.getenv('GEMINI_API_KEY'),
                'email_server': os.getenv('EMAIL_SERVER', 'imap.gmail.com'),
                'email_port': int(os.getenv('EMAIL_PORT', '993')),
                'email_username': os.getenv('EMAIL_USERNAME'),
                'email_password': os.getenv('EMAIL_PASSWORD'),
                'slack_webhook_url': os.getenv('SLACK_WEBHOOK_URL'),
                'slack_channels': {
                    'Product Support': '#product-support',
                    'Billing': '#billing',
                    'General Inquiry': '#general'
                }
            }
        
        # Validate required configuration
        required_keys = ['gemini_api_key', 'email_username', 'email_password', 'slack_webhook_url']
        for key in required_keys:
            if not config.get(key):
                raise ValueError(f"Missing required configuration: {key}")
        
        return config
    
    def connect_to_email(self) -> imaplib.IMAP4_SSL:
        """Connect to email server and return IMAP connection."""
        try:
            mail = imaplib.IMAP4_SSL(self.config['email_server'], self.config['email_port'])
            mail.login(self.config['email_username'], self.config['email_password'])
            mail.select('INBOX')
            print("✓ Successfully connected to email server")
            return mail
        except Exception as e:
            print(f"✗ Failed to connect to email: {e}")
            raise
    
    def fetch_unread_emails(self, mail: imaplib.IMAP4_SSL) -> List[Dict]:
        """Fetch unread emails from the inbox."""
        try:
            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            email_ids = messages[0].split()
            
            emails = []
            for email_id in email_ids[-10:]:  # Process last 10 unread emails
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decode subject
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            subject = subject.decode()
                        
                        # Get sender
                        sender = msg.get("From")
                        
                        # Get email body
                        body = self.extract_email_body(msg)
                        
                        emails.append({
                            'id': email_id.decode(),
                            'subject': subject,
                            'sender': sender,
                            'body': body,
                            'timestamp': datetime.now().isoformat()
                        })
            
            print(f"✓ Fetched {len(emails)} unread emails")
            return emails
            
        except Exception as e:
            print(f"✗ Error fetching emails: {e}")
            return []
    
    def extract_email_body(self, msg) -> str:
        """Extract plain text body from email message."""
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
        
        return body.strip()
    
    def classify_and_summarize_email(self, email_data: Dict) -> Tuple[str, str]:
        """Use Gemini AI to classify email and generate summary."""
        prompt = f"""
        Analyze the following customer email and:
        1. Classify it into ONE of these categories: Product Support, Billing, or General Inquiry
        2. Generate a concise one-sentence summary (max 15 words)
        
        Email Subject: {email_data['subject']}
        Email Body: {email_data['body'][:500]}
        
        Respond in this exact format:
        Category: [Product Support|Billing|General Inquiry]
        Summary: [one sentence summary]
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Parse response
            lines = response_text.split('\n')
            category = None
            summary = None
            
            for line in lines:
                if line.startswith('Category:'):
                    category = line.replace('Category:', '').strip()
                elif line.startswith('Summary:'):
                    summary = line.replace('Summary:', '').strip()
            
            # Validate category
            if category not in self.categories:
                category = "General Inquiry"  # Default fallback
            
            if not summary:
                summary = f"Email from {email_data['sender']} regarding {email_data['subject']}"
            
            print(f"✓ Classified email as: {category}")
            return category, summary
            
        except Exception as e:
            print(f"✗ Error in AI classification: {e}")
            # Fallback classification based on keywords
            return self.fallback_classification(email_data)
    
    def fallback_classification(self, email_data: Dict) -> Tuple[str, str]:
        """Fallback classification using keyword matching."""
        text = f"{email_data['subject']} {email_data['body']}".lower()
        
        # Simple keyword-based classification
        if any(word in text for word in ['bug', 'error', 'not working', 'issue', 'problem', 'feature']):
            category = "Product Support"
        elif any(word in text for word in ['bill', 'payment', 'invoice', 'charge', 'refund', 'price']):
            category = "Billing"
        else:
            category = "General Inquiry"
        
        summary = f"Email from {email_data['sender']} - {email_data['subject'][:30]}..."
        
        return category, summary
    
    def send_slack_notification(self, email_data: Dict, category: str, summary: str) -> bool:
        """Send notification to appropriate Slack channel."""
        try:
            channel = self.config['slack_channels'].get(category, '#general')
            
            slack_message = {
                "channel": channel,
                "username": "Email Triage Bot",
                "icon_emoji": ":email:",
                "attachments": [
                    {
                        "color": self.get_category_color(category),
                        "fields": [
                            {
                                "title": f"New {category} Email",
                                "value": summary,
                                "short": False
                            },
                            {
                                "title": "From",
                                "value": email_data['sender'],
                                "short": True
                            },
                            {
                                "title": "Subject",
                                "value": email_data['subject'][:50] + ("..." if len(email_data['subject']) > 50 else ""),
                                "short": True
                            }
                        ],
                        "footer": "Email Triage System",
                        "ts": int(time.time())
                    }
                ]
            }
            
            response = requests.post(
                self.config['slack_webhook_url'],
                json=slack_message,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"✓ Slack notification sent to {channel}")
                return True
            else:
                print(f"✗ Failed to send Slack notification: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Error sending Slack notification: {e}")
            return False
    
    def get_category_color(self, category: str) -> str:
        """Get color code for category."""
        colors = {
            "Product Support": "#ff6b6b",
            "Billing": "#4ecdc4",
            "General Inquiry": "#45b7d1"
        }
        return colors.get(category, "#808080")
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text."""
        # Remove common stop words and clean text
        stop_words = {'the', 'is', 'at', 'which', 'on', 'and', 'a', 'to', 'are', 'as', 'was', 'for', 'with', 'this', 'that', 'it', 'from', 'by', 'have', 'has', 'had', 'be', 'been', 'or', 'an', 'will', 'can', 'could', 'would', 'should'}
        
        # Extract words (alphanumeric only)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter out stop words and return meaningful keywords
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords
    
    def update_analytics(self, email_data: Dict, category: str, summary: str):
        """Update analytics data for keyword analysis."""
        # Extract keywords from email content
        text = f"{email_data['subject']} {email_data['body']}"
        keywords = self.extract_keywords(text)
        
        # Store keywords for this category
        self.category_keywords[category].extend(keywords)
        
        # Store processed email data
        self.processed_emails.append({
            'timestamp': email_data['timestamp'],
            'category': category,
            'summary': summary,
            'sender': email_data['sender'],
            'subject': email_data['subject'],
            'keywords': keywords
        })
    
    def generate_keyword_analytics(self) -> Dict:
        """Generate top 5 keywords per category."""
        analytics = {}
        
        for category in self.categories:
            if self.category_keywords[category]:
                keyword_counts = Counter(self.category_keywords[category])
                top_keywords = keyword_counts.most_common(5)
                analytics[category] = {
                    'top_keywords': top_keywords,
                    'total_emails': sum(1 for email in self.processed_emails if email['category'] == category)
                }
            else:
                analytics[category] = {
                    'top_keywords': [],
                    'total_emails': 0
                }
        
        return analytics
    
    def save_to_csv(self, filename: str = None):
        """Save processed emails to CSV file."""
        if not filename:
            filename = f"email_triage_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['timestamp', 'category', 'summary', 'sender', 'subject']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for email in self.processed_emails:
                    writer.writerow({
                        'timestamp': email['timestamp'],
                        'category': email['category'],
                        'summary': email['summary'],
                        'sender': email['sender'],
                        'subject': email['subject']
                    })
            
            print(f"✓ Data saved to {filename}")
            return filename
            
        except Exception as e:
            print(f"✗ Error saving to CSV: {e}")
            return None
    
    def save_analytics_report(self, filename: str = None):
        """Save analytics report to JSON file."""
        if not filename:
            filename = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            analytics = self.generate_keyword_analytics()
            
            report = {
                'generated_at': datetime.now().isoformat(),
                'total_emails_processed': len(self.processed_emails),
                'categories': analytics,
                'summary': {
                    'most_active_category': max(analytics.keys(), key=lambda k: analytics[k]['total_emails']) if analytics else None,
                    'processing_period': {
                        'start': min(email['timestamp'] for email in self.processed_emails) if self.processed_emails else None,
                        'end': max(email['timestamp'] for email in self.processed_emails) if self.processed_emails else None
                    }
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Analytics report saved to {filename}")
            return filename
            
        except Exception as e:
            print(f"✗ Error saving analytics: {e}")
            return None
    
    def run_triage_workflow(self):
        """Main workflow execution."""
        print("🚀 Starting Email Triage System...")
        
        try:
            # Connect to email
            mail = self.connect_to_email()
            
            # Fetch unread emails
            emails = self.fetch_unread_emails(mail)
            
            if not emails:
                print("📭 No unread emails found")
                return
            
            print(f"📧 Processing {len(emails)} emails...")
            
            for email_data in emails:
                print(f"\n--- Processing: {email_data['subject'][:50]}...")
                
                # Classify and summarize
                category, summary = self.classify_and_summarize_email(email_data)
                
                # Send Slack notification
                self.send_slack_notification(email_data, category, summary)
                
                # Update analytics
                self.update_analytics(email_data, category, summary)
                
                # Small delay to avoid rate limits
                time.sleep(1)
            
            # Close email connection
            mail.close()
            mail.logout()
            
            # Generate and save reports
            print("\n📊 Generating reports...")
            self.save_to_csv()
            self.save_analytics_report()
            
            # Display analytics summary
            analytics = self.generate_keyword_analytics()
            print("\n📈 Analytics Summary:")
            for category, data in analytics.items():
                print(f"{category}: {data['total_emails']} emails")
                if data['top_keywords']:
                    print(f"  Top keywords: {', '.join([kw[0] for kw in data['top_keywords'][:3]])}")
            
            print(f"\n✅ Successfully processed {len(emails)} emails!")
            
        except Exception as e:
            print(f"💥 Error in workflow execution: {e}")
            raise

def main():
    """Main function to run the email triage system."""
    try:
        triage_system = EmailTriageSystem()
        triage_system.run_triage_workflow()
    except Exception as e:
        print(f"Failed to run triage system: {e}")
        print("\nPlease check your configuration and try again.")

if __name__ == "__main__":
    main()