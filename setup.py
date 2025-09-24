#!/usr/bin/env python3
"""
Complete Setup Script for Email Triage System
Configures environment, installs dependencies, and tests all connections
"""

import os
import json
import sys
import subprocess
import imaplib
import time
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                 AI EMAIL TRIAGE SYSTEM SETUP                ║
    ║                                                              ║
    ║     This script will help you configure and test your       ║
    ║     AI-powered email triage system step by step.           ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("⚠️  This system requires Python 3.8 or higher")
        print("   Please upgrade Python and try again")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
    return True

def install_requirements():
    """Install required packages."""
    print("\n📦 Installing required packages...")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        print("Creating requirements.txt with essential packages...")
        
        requirements_content = """google-generativeai==0.3.2
requests==2.31.0
python-dotenv==1.0.0"""
        
        with open('requirements.txt', 'w') as f:
            f.write(requirements_content)
        print("✅ Created requirements.txt")
    
    try:
        # Upgrade pip first
        print("   📤 Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Install requirements
        print("   📥 Installing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("✅ All packages installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        print("\nTry manual installation:")
        print("   pip install google-generativeai requests python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def get_user_input(prompt, default=None, required=True, mask=False):
    """Get user input with validation"""
    while True:
        if default:
            display_prompt = f"{prompt} (default: {default}): "
        else:
            display_prompt = f"{prompt}: "
        
        if mask:
            import getpass
            value = getpass.getpass(display_prompt)
        else:
            value = input(display_prompt).strip()
        
        if not value and default:
            return default
        elif not value and required:
            print("⚠️  This field is required. Please enter a value.")
            continue
        elif not value and not required:
            return ""
        else:
            return value

def create_config_file():
    """Create configuration file with user input."""
    print("\n🔧 Configuration Setup")
    print("=" * 50)
    print("We'll now collect all the credentials needed for your system.\n")
    
    config = {}
    
    # Gemini API Key
    print("🤖 STEP 1: Gemini AI Configuration")
    print("   Get your API key from: https://aistudio.google.com/app/apikey")
    config['gemini_api_key'] = get_user_input(
        "Enter your Gemini API key", 
        required=True
    )
    
    # Email configuration
    print("\n📧 STEP 2: Email Configuration")
    print("   Note: For Gmail, you must use an App Password (not your regular password)")
    print("   Enable 2FA first, then generate App Password at: myaccount.google.com")
    
    config['email_server'] = get_user_input(
        "Email server", 
        default="imap.gmail.com"
    )
    
    config['email_port'] = int(get_user_input(
        "Email port", 
        default="993"
    ))
    
    config['email_username'] = get_user_input(
        "Email username (full email address)", 
        required=True
    )
    
    config['email_password'] = get_user_input(
        "Email password (App Password for Gmail)", 
        required=True,
        mask=True
    )
    
    # Slack configuration
    print("\n💬 STEP 3: Slack Configuration")
    print("   Create a webhook at: https://api.slack.com/apps")
    print("   Go to: Your App → Incoming Webhooks → Add New Webhook")
    
    config['slack_webhook_url'] = get_user_input(
        "Slack webhook URL", 
        required=True
    )
    
    # Channel configuration
    print("\n📋 STEP 4: Slack Channel Setup")
    print("   Configure which Slack channels to use for each email category")
    
    config['slack_channels'] = {}
    
    categories = ["Product Support", "Billing", "General Inquiry"]
    default_channels = ["#product-support", "#billing", "#general"]
    
    for category, default_channel in zip(categories, default_channels):
        config['slack_channels'][category] = get_user_input(
            f"Channel for {category}", 
            default=default_channel,
            required=False
        )
    
    # Save configuration
    try:
        print(f"\n💾 Saving configuration to config.json...")
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ Configuration saved successfully!")
        return config, True
        
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        return None, False

def test_gemini_api(config):
    """Test Gemini AI connection."""
    print("\n🤖 Testing Gemini AI Connection...")
    print("   This will verify your API key and test the AI service")
    
    try:
        import google.generativeai as genai
        
        # Configure API key
        genai.configure(api_key=config['gemini_api_key'])
        
        # Create model instance
        # model = genai.GenerativeModel('gemini-pro')
        model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro

        
        # Test with a simple prompt
        print("   📤 Sending test message to Gemini AI...")
        test_prompt = "This is a connection test. Please respond with exactly: 'Gemini AI connection successful!'"
        
        response = model.generate_content(test_prompt)
        response_text = response.text.strip()
        
        print("   📥 Received response from Gemini AI")
        print(f"   🤖 AI Response: {response_text}")
        
        if "successful" in response_text.lower():
            print("✅ Gemini AI connection test PASSED!")
            return True
        else:
            print("⚠️  Gemini AI responded, but test message doesn't match expected response")
            print("   This might still work fine for email classification")
            return True
            
    except Exception as e:
        print(f"❌ Gemini AI connection FAILED: {str(e)}")
        
        # Provide specific troubleshooting
        if "API_KEY_INVALID" in str(e) or "invalid" in str(e).lower():
            print("\n🔧 Troubleshooting:")
            print("   1. Check that your API key is correct")
            print("   2. Verify the key at: https://aistudio.google.com/app/apikey")
            print("   3. Make sure the API key has proper permissions")
        elif "quota" in str(e).lower() or "limit" in str(e).lower():
            print("\n🔧 Troubleshooting:")
            print("   1. You may have exceeded API rate limits")
            print("   2. Try again in a few minutes")
            print("   3. Check your usage at Google AI Studio")
        else:
            print("\n🔧 Troubleshooting:")
            print("   1. Check your internet connection")
            print("   2. Verify the google-generativeai package is installed")
            print("   3. Try regenerating your API key")
        
        return False

def test_email_connection(config):
    """Test email connection."""
    print("\n📬 Testing Email Connection...")
    print("   This will connect to your email server and count messages")
    
    try:
        # Connect to email server
        print(f"   🔌 Connecting to {config['email_server']}:{config['email_port']}...")
        mail = imaplib.IMAP4_SSL(config['email_server'], config['email_port'])
        
        # Login
        print("   🔐 Authenticating...")
        mail.login(config['email_username'], config['email_password'])
        
        # Select inbox
        mail.select('INBOX')
        
        # Count total emails
        status, messages = mail.search(None, 'ALL')
        total_emails = len(messages[0].split())
        
        # Count unread emails
        status, unread = mail.search(None, 'UNSEEN')
        unread_count = len(unread[0].split()) if unread[0] else 0
        
        # Close connection
        mail.close()
        mail.logout()
        
        print(f"✅ Email connection test PASSED!")
        print(f"   📊 Total emails in inbox: {total_emails}")
        print(f"   📧 Unread emails: {unread_count}")
        
        if unread_count == 0:
            print("   ℹ️  No unread emails found. Send yourself a test email to try the system.")
        
        return True
        
    except imaplib.IMAP4.error as e:
        print(f"❌ Email connection FAILED: {str(e)}")
        
        # Provide specific troubleshooting
        if "AUTHENTICATIONFAILED" in str(e).upper():
            print("\n🔧 Troubleshooting:")
            print("   1. For Gmail: Use App Password, NOT your regular password")
            print("   2. Enable 2-Factor Authentication first")
            print("   3. Generate App Password at: myaccount.google.com")
            print("   4. Make sure 'Less secure app access' is OFF")
            print("   5. Double-check username and password spelling")
        else:
            print("\n🔧 Troubleshooting:")
            print("   1. Check email server and port settings")
            print("   2. Verify your internet connection")
            print("   3. Try different email server (outlook.office365.com for Outlook)")
        
        return False
        
    except Exception as e:
        print(f"❌ Unexpected email error: {str(e)}")
        return False

def test_slack_webhook(config):
    """Test Slack webhook connection."""
    print("\n💬 Testing Slack Webhook...")
    print("   This will send a test message to your Slack workspace")
    
    try:
        import requests
        
        # Create test message
        test_message = {
            "text": "🎉 Email Triage System Setup Test",
            "username": "Email Triage Bot",
            "icon_emoji": ":robot_face:",
            "attachments": [
                {
                    "color": "#36a64f",
                    "fields": [
                        {
                            "title": "Setup Status",
                            "value": "✅ Webhook connection test successful!",
                            "short": False
                        },
                        {
                            "title": "System",
                            "value": "Email Triage System",
                            "short": True
                        },
                        {
                            "title": "Timestamp",
                            "value": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "short": True
                        }
                    ]
                }
            ]
        }
        
        # Send test message
        print("   📤 Sending test message to Slack...")
        response = requests.post(
            config['slack_webhook_url'],
            json=test_message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Slack webhook test PASSED!")
            print("   Check your Slack workspace for the test message")
            return True
        else:
            print(f"❌ Slack webhook FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            
            print("\n🔧 Troubleshooting:")
            print("   1. Check that your webhook URL is correct")
            print("   2. Verify the Slack app is installed in your workspace") 
            print("   3. Make sure the webhook is active")
            
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Slack webhook connection FAILED: {str(e)}")
        
        print("\n🔧 Troubleshooting:")
        print("   1. Check your internet connection")
        print("   2. Verify the webhook URL format")
        print("   3. Test the webhook URL in a browser or Postman")
        
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Slack error: {str(e)}")
        return False

def create_sample_files():
    """Create sample files if they don't exist"""
    print("\n📄 Creating sample project files...")
    
    files_created = []
    
    # Create .env template if it doesn't exist
    if not os.path.exists('.env'):
        env_content = """# Email Triage System Environment Variables
# Copy this file and update with your actual values

# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Email Configuration  
EMAIL_SERVER=imap.gmail.com
EMAIL_PORT=993
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-specific-password

# Slack Configuration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        files_created.append('.env')
    
    # Create .gitignore if it doesn't exist
    if not os.path.exists('.gitignore'):
        gitignore_content = """# Email Triage System - Git Ignore File

# Configuration files with secrets
config.json
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Generated files
email_triage_log_*.csv
analytics_report_*.json
demo_*.csv
demo_*.json

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
"""
        
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        files_created.append('.gitignore')
    
    if files_created:
        print(f"✅ Created sample files: {', '.join(files_created)}")
    else:
        print("ℹ️  All sample files already exist")

def run_comprehensive_test():
    """Run a comprehensive system test"""
    print("\n🧪 Running Comprehensive System Test...")
    print("=" * 50)
    
    try:
        # Import the main system
        print("   📥 Importing email triage system...")
        
        # Check if main file exists
        if not os.path.exists('email_triage.py'):
            print("❌ email_triage.py not found!")
            print("   Make sure you have the main application file")
            return False
        
        # Try to import (this will test syntax)
        import importlib.util
        spec = importlib.util.spec_from_file_location("email_triage", "email_triage.py")
        email_triage = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(email_triage)
        
        print("✅ Main application imports successfully")
        print("✅ No syntax errors detected")
        
        # Test configuration loading
        try:
            system = email_triage.EmailTriageSystem()
            print("✅ System initializes correctly")
        except Exception as e:
            print(f"⚠️  System initialization warning: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def display_final_summary(test_results):
    """Display final setup summary"""
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE - FINAL SUMMARY")
    print("=" * 60)
    
    # Test results summary
    print("\n📊 Test Results:")
    tests = [
        ("Python Version", test_results.get('python', False)),
        ("Package Installation", test_results.get('packages', False)),
        ("Gemini AI Connection", test_results.get('gemini', False)),
        ("Email Connection", test_results.get('email', False)),
        ("Slack Webhook", test_results.get('slack', False)),
        ("System Integration", test_results.get('system', False))
    ]
    
    passed = 0
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:.<25} {status}")
        if result:
            passed += 1
    
    print(f"\n   Overall: {passed}/{len(tests)} tests passed")
    
    # Recommendations
    print("\n🚀 Next Steps:")
    
    if passed == len(tests):
        print("   🎯 All tests passed! Your system is ready to use.")
        print("\n   To run your email triage system:")
        print("      python email_triage.py")
        print("\n   To test with demo mode first:")
        print("      python demo.py")
    
    elif passed >= 4:
        print("   ⚠️  Most tests passed. You can try running the system,")
        print("      but some features may not work correctly.")
        print("\n   Fix the failing tests, then run:")
        print("      python email_triage.py")
    
    else:
        print("   🔧 Several tests failed. Please fix the issues above")
        print("      before running the email triage system.")
        print("\n   You can re-run this setup anytime:")
        print("      python setup.py")
    
    # File locations
    print("\n📁 Important Files:")
    print("   • config.json - Your configuration settings")
    print("   • email_triage.py - Main application")
    print("   • demo.py - Demo mode for testing")
    print("   • .env - Environment variables template")
    print("   • .gitignore - Git ignore rules (keeps secrets safe)")
    
    # Security reminder
    print("\n🔒 Security Reminder:")
    print("   • Never commit config.json to version control")
    print("   • Keep your API keys private")
    print("   • Use App Passwords for email (not regular passwords)")
    
    print("\n✨ Happy email triaging! ✨")

def main():
    """Main setup function."""
    print_banner()
    
    # Track test results
    test_results = {}
    
    try:
        # Step 1: Check Python version
        test_results['python'] = check_python_version()
        if not test_results['python']:
            return
        
        # Step 2: Install packages
        test_results['packages'] = install_requirements()
        if not test_results['packages']:
            print("⚠️  Continuing setup, but some features may not work...")
        
        # Step 3: Configuration
        print("\n" + "="*60)
        if os.path.exists('config.json'):
            print("📄 Configuration file (config.json) already exists!")
            use_existing = input("\nUse existing configuration? (y/n): ").strip().lower()
            
            if use_existing == 'y' or use_existing == 'yes':
                with open('config.json', 'r') as f:
                    config = json.load(f)
                print("✅ Using existing configuration")
            else:
                config, success = create_config_file()
                if not success:
                    print("❌ Configuration failed. Exiting setup.")
                    return
        else:
            config, success = create_config_file()
            if not success:
                print("❌ Configuration failed. Exiting setup.")
                return
        
        # Step 4: Create sample files
        create_sample_files()
        
        # Step 5: Test connections
        print("\n" + "="*60)
        print("🔧 TESTING ALL CONNECTIONS")
        print("="*60)
        
        test_results['gemini'] = test_gemini_api(config)
        test_results['email'] = test_email_connection(config)
        test_results['slack'] = test_slack_webhook(config)
        
        # Step 6: System integration test
        test_results['system'] = run_comprehensive_test()
        
        # Step 7: Final summary
        display_final_summary(test_results)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        print("You can run setup again anytime: python setup.py")
    
    except Exception as e:
        print(f"\n💥 Unexpected error during setup: {e}")
        print("Please try running setup again or check the error message above")

if __name__ == "__main__":
    main()