import smtplib, ssl
from email.message import EmailMessage 
from core.misc import Misc


helper = Misc()
import smtplib
from email.message import EmailMessage

class EmailSender:
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.port = 587
        self.username = helper.config_parser('sender_mail')
        self.password = helper.config_parser('sender_password')

    def send_email(self, subject, body):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = helper.config_parser('receiver_mail')

        with smtplib.SMTP(self.smtp_server, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)
            smtp.send_message(msg)
    
    
    
