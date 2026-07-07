import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""


class EmailService:

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        body: str
    ):

        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            return False

        message = MIMEMultipart()

        message["From"] = EMAIL_ADDRESS
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(
            MIMEText(
                body,
                "plain"
            )
        )

        try:

            server = smtplib.SMTP(
                SMTP_SERVER,
                SMTP_PORT
            )

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            server.send_message(message)

            server.quit()

            return True

        except Exception:

            return False
