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
    server.login("mel15551", "apfelsaft1")
    try:
        server.send_message(msg)
        print("The message was sent successfully.")
    except:
        print("The message could not be sent.")
    server.quit()
