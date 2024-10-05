import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sys

def send_email(smtp_server, sender_email, recipient_email, subject, message):
    try:
        # Create the message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the message content
        msg.attach(MIMEText(message, 'html'))

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server)
        server.starttls()  # Secure the connection with TLS
        # server.login(username, password)  # Login to the server
        
        # Send the email
        server.send_message(msg)
        
        # Close the connection to the SMTP server
        server.quit()

        print("Email sent successfully!")
    
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


# Usage example
# port = 587                         # Specify the port, 587 is typical for TLS
# username = 'your_email@example.com'  # SMTP username (usually your email address)
# password = 'your_password'           # SMTP password

smtp_server = sys.argv[1]  # Specify the SMTP server address
sender_email = sys.argv[2]
recipient_email = sys.argv[3]
subject = sys.argv[4]
message = sys.argv[5]

send_email(smtp_server, sender_email, recipient_email, subject, message)
