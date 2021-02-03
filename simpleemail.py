# Simple email class

import smtplib
import ssl
from email.mime.text import MIMEText


class SimpleEmail:

    def __init__(self, sender, pwd, recipients, subject, body):
        self.sender = sender
        self.pwd=pwd
        self.recipients = recipients
        self.subject = subject
        self.body = body

    def send(self):
        msg=MIMEText(self.body, 'html')
        msg['Subject'] = self.subject
        msg['From'] = self.send
        msg['To'] = ','.join(self.recipients)
        s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
        s.login(user=self.sender, password=self.pwd)
        s.sendmail(self.sender, self.recipients, msg.as_string())
        s.quit()
