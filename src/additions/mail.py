from src.config import Config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib

class Mail:
    email_address = Config.MAIL_USERNAME
    email_password=Config.MAIL_PASSWORD
    host=Config.MAIL_SERVER
    port=Config.MAIL_PORT

    def send_mail(self,emails, subject, message, email_type='plain', email_address=email_address, email_password=email_password, host=host, port=port):
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['Subject'] = subject
        msg.attach(MIMEText(message, email_type))

        try:
            # მყარდება სერვერთან კავშირი
            server = smtplib.SMTP(host=host, port=port)
            server.starttls()    
            server.login(email_address, email_password)

            for email in emails:
                msg["To"] = email
                server.sendmail(email_address, email, msg.as_string())

            # წყდება შერვერთან კავშირი
            server.quit()
            return True
        except:
            return False