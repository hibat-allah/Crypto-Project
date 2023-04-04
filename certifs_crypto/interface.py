import tkinter as tk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from smail import sign_message

LOGIN_MAIL, LOGIN_PASSWORD = open('LOGIN_INFO.txt', "r").read().split("\n")
SMTP_SERVER = 'smtp.gmail.com'
SMTP_SERVER_PORT = 587


CERT_FILE = 'samy_cert.pem'
KEY_FILE = 'samy-key.pem'


class EmailApp:
    def __init__(self, master):
        self.master = master
        master.title("Signed Email")

        self.to_label = tk.Label(master, text="To:")
        self.to_label.pack()

        self.to_entry = tk.Entry(master)
        self.to_entry.pack()

        self.subject_label = tk.Label(master, text="Subject:")
        self.subject_label.pack()

        self.subject_entry = tk.Entry(master)
        self.subject_entry.pack()

        self.message_label = tk.Label(master, text="Message:")
        self.message_label.pack()

        self.message_entry = tk.Text(master)
        self.message_entry.pack()

        self.send_button = tk.Button(master, text="Send", command=self.send_email)
        self.send_button.pack()

    def send_email(self):
        recipient = self.to_entry.get()
        subject = self.subject_entry.get()
        message = self.message_entry.get("1.0", "end-1c")

        msg = MIMEMultipart("related")
        msg.attach(MIMEText(message, "plain", _charset="utf-8"))
        msg["Subject"] = subject
        msg["From"] = LOGIN_MAIL
        msg["To"] = recipient

        signed_msg = sign_message(msg, KEY_FILE, CERT_FILE)

        with smtplib.SMTP(SMTP_SERVER, SMTP_SERVER_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(LOGIN_MAIL, LOGIN_PASSWORD)
            server.send_message(signed_msg)

        print("Email sent")

root = tk.Tk()
email_app = EmailApp(root)
root.mainloop()