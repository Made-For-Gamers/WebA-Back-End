import smtplib
import ssl
from config import settings
from email.mime.text import MIMEText  # New line
from email.utils import formataddr  # New line

class EmailModel:
      def __init__(self, receiver_name, receiver_email, email_body, subject, message):
          self.receiver_name = receiver_name
          self.receiver_email = receiver_email
          self.email_body = email_body
          self.subject = subject
          self.message = message
 
class EmailServer:
    def __init__(self, sender_name):
        self.sender_name = sender_name  
 
    def send_mail(self, EmailModel):
    
        # User configuration
        sender_email = settings.GMAILADDR 
        password = settings.GMAILPASSWORD   
         
        # Configurating user's info
        msg = MIMEText(EmailModel.email_body, 'plain')
        msg['To'] = formataddr((EmailModel.receiver_name, EmailModel.receiver_email))
        msg['From'] = formataddr((self.sender_name, sender_email))
        msg['Subject'] = EmailModel.subject

        print("Sending the email...")
        try:
            # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
            server = smtplib.SMTP('smtp.gmail.com', 587)
            # Encrypts the email
            context = ssl.create_default_context()
            server.starttls(context=context)
            # We log in into our Google account
            server.login(sender_email, password)
            # Sending email from sender, to receiver with the email body
            server.sendmail(sender_email, EmailModel.receiver_email, msg.as_string())
            print('Email sent!')
        except Exception as e:
            print(f'Oh no! Something bad happened!n {e}')
        finally:
            print('Closing the server...')
            server.quit()
