# #!/usr/bin/env python3
# """
# Demo script for Email Triage System
# Tests the system with sample emails without connecting to actual email server
# """

# import json
# import time
# from datetime import datetime
# from email_triage import EmailTriageSystem

# class DemoEmailTriageSystem(EmailTriageSystem):
#     """
#     Demo version of EmailTriageSystem that uses sample emails instead of real ones
#     """
    
#     def __init__(self):
#         super().__init__()
        
#         # Sample emails for testing
#         self.sample_emails = [
#             {
#                 'id': 'demo_1',
#                 'subject': 'Login issues with mobile app',
#                 'sender': 'customer1@example.com',
#                 'body': 'Hi, I am having trouble logging into my account on the mobile app. It keeps showing an error message saying "Invalid credentials" even though I know my password is correct. Can you please help me fix this issue? I need to access my account urgently.',
#                 'timestamp': datetime.now().isoformat()
#             },
#             {
#                 'id': 'demo_2', 
#                 'subject': 'Question about my monthly invoice',
#                 'sender': 'billing.inquiry@company.com',
#                 'body': 'Hello, I received my monthly invoice and noticed there are some charges I don\'t recognize. Could you please explain what the "Premium Service Fee" of $25.99 is for? I don\'t remember signing up for any premium services. Also, why was I charged twice for the basic plan?',
#                 'timestamp': datetime.now().isoformat()
#             },
#             {
#                 'id': 'demo_3',
#                 'subject': 'Feature request for dashboard',
#                 'sender': 'poweruser@tech.com',
#                 'body': 'Hi team, I love using your product! I have a suggestion for a new feature. Would it be possible to add a dark mode to the dashboard? Also, it would be great to have keyboard shortcuts for common actions. Many users including myself would find this very useful for productivity.',
#                 'timestamp': datetime.now().isoformat()
#             },
#             {
#                 'id': 'demo_4',
#                 'subject': 'Refund request - Order #12345',
#                 'sender': 'customer.support@email.com',
#                 'body': 'I would like to request a refund for my recent order #12345. The product arrived damaged and doesn\'t match the description on your website. I have attached photos of the damaged item. Please process my refund as soon as possible. The order was placed on September 15th for $129.99.',
#                 'timestamp': datetime.now().isoformat()
#             },
#             {
#                 'id': 'demo_5',
#                 'subject': 'How to reset my password?',
#                 'sender': 'newuser@gmail.com',
#                 'body': 'Hi, I forgot my password and tried to use the "Forgot Password" link on your website, but I\'m not receiving any reset emails. I checked my spam folder as well. Could you please help me reset my password or let me know what else I can try? My username is newuser123.',
#                 'timestamp': datetime.now().isoformat()
#             }
#         ]
    
#     def connect_to_email(self):
#         """Demo version - skip actual email connection"""
#         print("✓ [DEMO] Simulating email server connection")
#         return None
    
#     def fetch_unread_emails(self, mail):
#         """Demo version - return sample emails"""
#         print(f"✓ [DEMO] Simulating fetch of {len(self.sample_emails)} sample emails")
#         return self.sample_emails
    
#     def send_slack_notification(self, email_data, category, summary):
#         """Demo version - simulate Slack notification"""
#         try:
#             channel = self.config['slack_channels'].get(category, '#general')
            
#             print(f"📢 [DEMO SLACK] Would send to {channel}:")
#             print(f"   📧 {category}: {summary}")
#             print(f"   👤 From: {email_data['sender']}")
#             print(f"   📝 Subject: {email_data['subject'][:50]}...")
#             print()
            
#             # If you want to test actual Slack notifications, uncomment this:
#             # return super().send_slack_notification(email_data, category, summary)
            
#             return True
            
#         except Exception as e:
#             print(f"✗ [DEMO] Error simulating Slack notification: {e}")
#             return False
    
#     def run_demo(self):
#         """Run the demo workflow"""
#         print("🎭 DEMO MODE: Email Triage System")
#         print("=" * 50)
#         print("This demo will process sample emails to show how the system works.")
#         print("No actual emails will be read and Slack notifications are simulated.\n")
        
#         try:
#             # Simulate email connection
#             mail = self.connect_to_email()
            
#             # Get sample emails
#             emails = self.fetch_unread_emails(mail)
            
#             print(f"📧 Processing {len(emails)} sample emails...\n")
            
#             for i, email_data in enumerate(emails, 1):
#                 print(f"--- Processing Email {i}/{len(emails)} ---")
#                 print(f"Subject: {email_data['subject']}")
#                 print(f"From: {email_data['sender']}")
#                 print(f"Preview: {email_data['body'][:100]}...")
#                 print()
                
#                 # Classify and summarize
#                 category, summary = self.classify_and_summarize_email(email_data)
                
#                 # Simulate Slack notification
#                 self.send_slack_notification(email_data, category, summary)
                
#                 # Update analytics
#                 self.update_analytics(email_data, category, summary)
                
#                 # Delay for demo effect
#                 time.sleep(2)
            
#             # Generate reports
#             print("📊 Generating demo reports...")
#             csv_file = self.save_to_csv("demo_email_log.csv")
#             json_file = self.save_analytics_report("demo_analytics.json")
            
#             # Show analytics
#             analytics = self.generate_keyword_analytics()
#             print("\n" + "=" * 50)
#             print("📈 DEMO ANALYTICS SUMMARY")
#             print("=" * 50)
            
#             total_emails = sum(data['total_emails'] for data in analytics.values())
#             print(f"Total emails processed: {total_emails}")
#             print()
            
#             for category, data in analytics.items():
#                 print(f"📂 {category}: {data['total_emails']} emails")
#                 if data['top_keywords']:
#                     keywords = [f"{kw[0]}({kw[1]})" for kw in data['top_keywords'][:5]]
#                     print(f"   🔑 Top keywords: {', '.join(keywords)}")
#                 print()
            
#             print("✅ DEMO COMPLETED SUCCESSFULLY!")
#             print("\nGenerated files:")
#             if csv_file:
#                 print(f"- {csv_file}")
#             if json_file:
#                 print(f"- {json_file}")
            
#             print("\n💡 To run with real emails:")
#             print("   python email_triage.py")
            
#         except Exception as e:
#             print(f"💥 Demo failed: {e}")
#             import traceback
#             traceback.print_exc()

# def create_demo_config():
#     """Create a demo configuration file if none exists"""
#     if not os.path.exists('config.json'):
#         demo_config = {
#             "gemini_api_key": "DEMO_KEY_PLEASE_ADD_YOUR_REAL_KEY",
#             "email_server": "imap.gmail.com",
#             "email_port": 993,
#             "email_username": "demo@example.com",
#             "email_password": "demo_password",
#             "slack_webhook_url": "https://hooks.slack.com/demo/webhook/url",
#             "slack_channels": {
#                 "Product Support": "#product-support",
#                 "Billing": "#billing",
#                 "General Inquiry": "#general"
#             }
#         }
        
#         with open('config.json', 'w') as f:
#             json.dump(demo_config, f, indent=2)
        
#         print("📄 Created demo config.json file")
#         print("⚠️  Please add your real Gemini API key to config.json")
#         return False
    
#     return True

# def main():
#     """Main demo function"""
#     import os
    
#     print("🎬 Email Triage System - Demo Mode")
#     print()
    
#     # Check if config exists, create demo if not
#     if not create_demo_config():
#         print("\n🔑 Please edit config.json and add your Gemini API key, then run the demo again.")
#         return
    
#     # Check if Gemini API key is set
#     try:
#         with open('config.json', 'r') as f:
#             config = json.load(f)
        
#         if not config.get('gemini_api_key') or config['gemini_api_key'] == "DEMO_KEY_PLEASE_ADD_YOUR_REAL_KEY":
#             print("⚠️  Please add your real Gemini API key to config.json")
#             print("   Get one at: https://aistudio.google.com/app/apikey")
#             return
            
#     except Exception as e:
#         print(f"❌ Error loading config: {e}")
#         return
    
#     # Run the demo
#     try:
#         demo_system = DemoEmailTriageSystem()
#         demo_system.run_demo()
#     except Exception as e:
#         print(f"❌ Failed to run demo: {e}")
#         print("\nMake sure you have:")
#         print("1. Valid Gemini API key in config.json")
#         print("2. Installed requirements: pip install -r requirements.txt")

# if __name__ == "__main__":
#     main()


#!/usr/bin/env python3
"""
Demo script for Email Triage System
Tests the system with sample emails without connecting to actual email server
"""

import os
import json
import time
from datetime import datetime
from email_triage import EmailTriageSystem

class DemoEmailTriageSystem(EmailTriageSystem):
    """
    Demo version of EmailTriageSystem that uses sample emails instead of real ones
    """
    
    def __init__(self):
        super().__init__()
        
        # Sample emails for testing
        self.sample_emails = [
            {
                'id': 'demo_1',
                'subject': 'Login issues with mobile app',
                'sender': 'customer1@example.com',
                'body': 'Hi, I am having trouble logging into my account on the mobile app. It keeps showing an error message saying "Invalid credentials" even though I know my password is correct. Can you please help me fix this issue? I need to access my account urgently.',
                'timestamp': datetime.now().isoformat()
            },
            {
                'id': 'demo_2', 
                'subject': 'Question about my monthly invoice',
                'sender': 'billing.inquiry@company.com',
                'body': 'Hello, I received my monthly invoice and noticed there are some charges I don\'t recognize. Could you please explain what the "Premium Service Fee" of $25.99 is for? I don\'t remember signing up for any premium services. Also, why was I charged twice for the basic plan?',
                'timestamp': datetime.now().isoformat()
            },
            {
                'id': 'demo_3',
                'subject': 'Feature request for dashboard',
                'sender': 'poweruser@tech.com',
                'body': 'Hi team, I love using your product! I have a suggestion for a new feature. Would it be possible to add a dark mode to the dashboard? Also, it would be great to have keyboard shortcuts for common actions. Many users including myself would find this very useful for productivity.',
                'timestamp': datetime.now().isoformat()
            },
            {
                'id': 'demo_4',
                'subject': 'Refund request - Order #12345',
                'sender': 'customer.support@email.com',
                'body': 'I would like to request a refund for my recent order #12345. The product arrived damaged and doesn\'t match the description on your website. I have attached photos of the damaged item. Please process my refund as soon as possible. The order was placed on September 15th for $129.99.',
                'timestamp': datetime.now().isoformat()
            },
            {
                'id': 'demo_5',
                'subject': 'How to reset my password?',
                'sender': 'newuser@gmail.com',
                'body': 'Hi, I forgot my password and tried to use the "Forgot Password" link on your website, but I\'m not receiving any reset emails. I checked my spam folder as well. Could you please help me reset my password or let me know what else I can try? My username is newuser123.',
                'timestamp': datetime.now().isoformat()
            }
        ]
    
    def connect_to_email(self):
        """Demo version - skip actual email connection"""
        print("✓ [DEMO] Simulating email server connection")
        return None
    
    def fetch_unread_emails(self, mail):
        """Demo version - return sample emails"""
        print(f"✓ [DEMO] Simulating fetch of {len(self.sample_emails)} sample emails")
        return self.sample_emails
    
    def send_slack_notification(self, email_data, category, summary):
        """Demo version - simulate Slack notification"""
        try:
            channel = self.config['slack_channels'].get(category, '#general')
            
            print(f"📢 [DEMO SLACK] Would send to {channel}:")
            print(f"   📧 {category}: {summary}")
            print(f"   👤 From: {email_data['sender']}")
            print(f"   📝 Subject: {email_data['subject'][:50]}...")
            print()
            
            # If you want to test actual Slack notifications, uncomment this:
            # return super().send_slack_notification(email_data, category, summary)
            
            return True
            
        except Exception as e:
            print(f"✗ [DEMO] Error simulating Slack notification: {e}")
            return False
    
    def run_demo(self):
        """Run the demo workflow"""
        print("🎭 DEMO MODE: Email Triage System")
        print("=" * 50)
        print("This demo will process sample emails to show how the system works.")
        print("No actual emails will be read and Slack notifications are simulated.\n")
        
        try:
            # Simulate email connection
            mail = self.connect_to_email()
            
            # Get sample emails
            emails = self.fetch_unread_emails(mail)
            
            print(f"📧 Processing {len(emails)} sample emails...\n")
            
            for i, email_data in enumerate(emails, 1):
                print(f"--- Processing Email {i}/{len(emails)} ---")
                print(f"Subject: {email_data['subject']}")
                print(f"From: {email_data['sender']}")
                print(f"Preview: {email_data['body'][:100]}...")
                print()
                
                # Classify and summarize
                category, summary = self.classify_and_summarize_email(email_data)
                
                # Simulate Slack notification
                self.send_slack_notification(email_data, category, summary)
                
                # Update analytics
                self.update_analytics(email_data, category, summary)
                
                # Delay for demo effect
                time.sleep(2)
            
            # Generate reports
            print("📊 Generating demo reports...")
            csv_file = self.save_to_csv("demo_email_log.csv")
            json_file = self.save_analytics_report("demo_analytics.json")
            
            # Show analytics
            analytics = self.generate_keyword_analytics()
            print("\n" + "=" * 50)
            print("📈 DEMO ANALYTICS SUMMARY")
            print("=" * 50)
            
            total_emails = sum(data['total_emails'] for data in analytics.values())
            print(f"Total emails processed: {total_emails}")
            print()
            
            for category, data in analytics.items():
                print(f"📂 {category}: {data['total_emails']} emails")
                if data['top_keywords']:
                    keywords = [f"{kw[0]}({kw[1]})" for kw in data['top_keywords'][:5]]
                    print(f"   🔑 Top keywords: {', '.join(keywords)}")
                print()
            
            print("✅ DEMO COMPLETED SUCCESSFULLY!")
            print("\nGenerated files:")
            if csv_file:
                print(f"- {csv_file}")
            if json_file:
                print(f"- {json_file}")
            
            print("\n💡 To run with real emails:")
            print("   python email_triage.py")
            
        except Exception as e:
            print(f"💥 Demo failed: {e}")
            import traceback
            traceback.print_exc()

def create_demo_config():
    """Create a demo configuration file if none exists"""
    if not os.path.exists('config.json'):
        demo_config = {
            "gemini_api_key": "DEMO_KEY_PLEASE_ADD_YOUR_REAL_KEY",
            "email_server": "imap.gmail.com",
            "email_port": 993,
            "email_username": "demo@example.com",
            "email_password": "demo_password",
            "slack_webhook_url": "https://hooks.slack.com/demo/webhook/url",
            "slack_channels": {
                "Product Support": "#product-support",
                "Billing": "#billing",
                "General Inquiry": "#general"
            }
        }
        
        with open('config.json', 'w') as f:
            json.dump(demo_config, f, indent=2)
        
        print("📄 Created demo config.json file")
        print("⚠️  Please add your real Gemini API key to config.json")
        return False
    
    return True

def main():
    """Main demo function"""
    import os
    
    print("🎬 Email Triage System - Demo Mode")
    print()
    
    # Check if config exists, create demo if not
    if not create_demo_config():
        print("\n🔑 Please edit config.json and add your Gemini API key, then run the demo again.")
        return
    
    # Check if Gemini API key is set
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        if not config.get('gemini_api_key') or config['gemini_api_key'] == "DEMO_KEY_PLEASE_ADD_YOUR_REAL_KEY":
            print("⚠️  Please add your real Gemini API key to config.json")
            print("   Get one at: https://aistudio.google.com/app/apikey")
            return
            
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return
    
    # Run the demo
    try:
        demo_system = DemoEmailTriageSystem()
        demo_system.run_demo()
    except Exception as e:
        print(f"❌ Failed to run demo: {e}")
        print("\nMake sure you have:")
        print("1. Valid Gemini API key in config.json")
        print("2. Installed requirements: pip install -r requirements.txt")

if __name__ == "__main__":
    main()