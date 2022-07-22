import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

USER = "nicowishesyouahappybirthday@gmail.com"
PASSWORD = "xmebpypmfzhilrnk"

def send_mail(description, header):
    message = MIMEMultipart()
    message["From"] = f"{USER}"
    message["To"] = "nicolajlpedersen@gmail.com"
    message["Subject"] = Header(s=f"{header}", charset="utf-8")

    # Add the text message
    msg_text = MIMEText(_text=f"{description}", _subtype="plain", _charset="utf-8")
    message.attach(msg_text)

    with smtplib.SMTP("smtp.gmail.com", 587) as conn:
        conn.starttls()
        conn.login(user=USER, password=PASSWORD)
        conn.sendmail(
            from_addr=USER,
            to_addrs="nicolajlpedersen@gmail.com",
            msg=f"{message.as_string()}"
        )