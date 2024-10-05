import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import sys

def send_email(smtp_server, sender_email, recipient_email, subject, email_body_file_path):
    try:
        # Create the message container
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Read the HTML content from the file
        with open(email_body_file_path, 'r') as file:
            html_content = file.read()

        # Attach the HTML content to the email
        # msg.attach(MIMEText(html_content, 'html'))
        msg.set_content(html_content, subtype="html")

        # # Connect to the SMTP server
        # server = smtplib.SMTP(smtp_server)
        
        # # Send the email
        # server.send_message(msg)
        smtp = smtplib.SMTP(smtp_server)
        smtp.sendmail(msg)
        
        # Close the connection to the SMTP server
        smtp.quit()

        print("Email sent successfully!")
    
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Usage example
# smtp_server = 'smtp.example.com'
# sender_email = 'your_email@example.com'
# recipient_email = 'recipient_email@example.com'
# subject = 'Test HTML Email'
# html_file_path = 'path_to_html_file.html'

if len(sys.argv) < 6:
    print("Usage: python script.py <smtp_server> <sender_email> <recipient_email> <subject> <html_file_path>")
    sys.exit(1)

smtp_server = sys.argv[1]
sender_email = sys.argv[2]
recipient_email = sys.argv[3]
subject = sys.argv[4]
email_body_file_path = sys.argv[5]

send_email(smtp_server, sender_email, recipient_email, subject, email_body_file_path)
