import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

myDb = mysql.connector.connect(host="localhost", user="root", passwd="", database="py_email_demo", port="3306")

# print(myDb)
mycursor = myDb.cursor()

mycursor.execute("SELECT * FROM user_dtl")

myresult = mycursor.fetchall()
emails = []
# print(myresult)
for row in myresult:
      emails.append(row[2])

# print(emails)

fromaddr = "youremail@gmail.com"
toaddr = emails

# instance of MIMEMultipart
msg = MIMEMultipart()

# storing the senders email address
msg['From'] = fromaddr

# storing the receivers email address
msg['To'] = toaddr

# storing the subject
msg['Subject'] = "Health Report"

# string to store the body of the mail
body='Hello, <br><br> Please Check your health report <br><br> Thanks <br> Dr.ECT'

# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))

# open the file to be sent
filename = "File name with extension"
attachment = open("Path of the file", "rb")

# instance of MIMEBase and named as p
p = MIMEBase('application', 'octet-stream')

# To change the payload into encoded form
p.set_payload((attachment).read())

# encode into base64
encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login(fromaddr, "Password_of_the_sender")

# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mail
s.sendmail(fromaddr, toaddr, text)

# terminating the session
s.quit()