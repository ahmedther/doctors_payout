
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders
import os

class Email_Sender:
    def __init__(self, send_from, send_to, send_to_cc, subject, text, server, port, attachment=None):
        msg = MIMEMultipart()
        msg["From"] = send_from
        msg["To"] = send_to
        msg["Cc"] = send_to_cc
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject
        msg.attach(MIMEText(text, "html"))

        if attachment is not None and os.path.exists(attachment):
            part = MIMEBase("application", "octet-stream")
            part.set_payload(open(attachment, "rb").read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment)}")
            msg.attach(part)

        smtp = smtplib.SMTP(server, port)
        smtp.sendmail(send_from, [send_to, send_to_cc], msg.as_string())
        smtp.quit()



