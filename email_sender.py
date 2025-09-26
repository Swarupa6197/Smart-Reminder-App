import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, message):
    sender = "yourmail@gmail.com"
    password = "yourpassword"  # ⚠ Store securely in env variables!

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, to_email, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print("Error:", e)
