import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# email credentials
email = "ourhesf@gmail.com"
password = "cizunsifunsarnff"

# email details
recipient = "ourhesf@gmail.com"
subject = "Test Email"
body = "This is a test email sent using Python."

# create message
msg = MIMEMultipart()
msg["From"] = email
msg["To"] = recipient
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# create SMTP session
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, password)

# send message
server.sendmail(email, recipient, msg.as_string())

# close SMTP session
server.quit()