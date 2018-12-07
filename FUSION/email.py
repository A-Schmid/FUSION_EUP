import smtplib
from email.message import EmailMessage

def send_email(recipient, subject="FUSION", message=""):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = "fusion@fusion.de"
    msg['To'] = recipient
    server = smtplib.SMTP_SSL("mail.uni-regensburg.de", 465)
    server.send_message(msg)
    server.quit()
