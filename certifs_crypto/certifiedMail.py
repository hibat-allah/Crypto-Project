import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from smail import sign_message

LOGIN_MAIL, LOGIN_PASSWORD = open('LOGIN_INFO.txt', "r").read().split("\n")
SMTP_SERVER = 'smtp.gmail.com'
SMTP_SERVER_PORT = 587


CERT_FILE = 'path_to_cert_file.pem'
KEY_FILE = 'path_to_key_file.pem'


recipient = "mail of recipient"

message= """
Hello,
This is my first signed email.
Thanks, for your support !
"""

msg = MIMEMultipart("related")
msg.attach(MIMEText(message, "plain", _charset="utf-8"))
msg["Subject"] = "test mail"
msg["From"] = LOGIN_MAIL
msg["To"] = recipient

signed_msg = sign_message(msg, KEY_FILE,CERT_FILE)

with smtplib.SMTP(SMTP_SERVER, SMTP_SERVER_PORT) as server:
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(LOGIN_MAIL, LOGIN_PASSWORD)
    server.send_message(signed_msg)

print("Email sent")


