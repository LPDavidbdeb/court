import os
import django
from django.utils.dateparse import parse_datetime
from django.db.models import Q

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from email_manager.models import Email
from protagonist_manager.models import Protagonist

def extract_and_analyze():
    start = parse_datetime('2009-01-01T00:00:00Z')
    end = parse_datetime('2015-12-31T23:59:59Z')
    
    emails = Email.objects.filter(date_sent__range=(start, end)).order_by('date_sent')
    
    output_file = 'email_analysis_2009_2015.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Analysis of {emails.count()} emails from 2009 to 2015\n")
        f.write("="*50 + "\n\n")
        
        for email in emails:
            sender_name = email.sender_protagonist.get_full_name() if email.sender_protagonist else email.sender
            recipients = ", ".join([p.get_full_name() for p in email.recipient_protagonists.all()])
            if not recipients:
                recipients = email.recipients_to
            
            f.write(f"Date: {email.date_sent}\n")
            f.write(f"From: {sender_name}\n")
            f.write(f"To: {recipients}\n")
            f.write(f"Subject: {email.subject}\n")
            f.write("-" * 20 + "\n")
            f.write(f"{email.body_plain_text or '[No body]'}\n")
            f.write("\n" + "="*50 + "\n\n")
            
    print(f"Exported {emails.count()} emails to {output_file}")

if __name__ == "__main__":
    extract_and_analyze()
