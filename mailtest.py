import smtplib

print("setting up server")
server = smtplib.SMTP_SSL("mail.uni-regensburg.de", 465)

#print("logging in")
#server.login("sca04209", "password")

msg = "supertest /n emailtest!"

print("sending mail")
server.sendmail("Andreas1.Schmid@stud.uni-regensburg.de", "Andreas1.Schmid@stud.uni-regensburg.de", msg)

print("success!")
