from re import I
import smtplib, ssl
from email.message import EmailMessage 
from core.misc import Misc


helper = Misc()
class Mailer():
    
    
    def __init__(self):
        self.email = None
        self.password = None
        self.context = ssl.create_default_context()
        self.receiver = None
        self.server = "smtp.gmail.com"
        self.port = 465
        self.ngrok_link = None
        self.email_content = EmailMessage()


    def sendmail(self):
        try:
            with smtplib.SMTP_SSL(self.server, self.port, context=self.context) as server:
                server.login(self.email, self.password)
                self.email_content['To'] = self.receiver
                self.email_content['From'] = self.email
                self.email_content['Subject'] = self.ngrok_link
                self.email_content.set_content = self.ngrok_link
                server.sendmail(self.email, self.receiver, self.email_content.as_string())
        except Exception as e:
            print(e)


    def get_values(self):
        try:
            self.email = helper.config_parser('sender_mail')
            self.password = helper.config_parser('sender_password')
            self.receiver = helper.config_parser('receiver_mail')
        except Exception as e:
            print(e)
    

    def get_ngrok_link(self, link):
        self.ngrok_link = link


"""
    def set_values(self, email, password, receiver):
        try:
            with open(self.config, 'w') as mail_config:
                mail_config.write(email + "\n")
                mail_config.write(password + "\n")
                mail_config.write(receiver + "\n")
        except Exception as e:
            print(e)

"""    
    
    
