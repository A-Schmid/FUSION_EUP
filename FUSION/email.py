import smtplib
from email.message import EmailMessage

def send_email(recipient, subject="FUSION", message=""):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = "Andreas1.Schmid@stud.uni-regensburg.de"
    msg['To'] = recipient
    server = smtplib.SMTP("smtp.uni-regensburg.de", 587)
    server.starttls()
    server.login("sca04209", "password")
    server.send_message(msg)
    server.quit()
