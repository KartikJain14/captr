import resend
import os
from dotenv import load_dotenv
import resend.emails

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")


def send_email(to: str, title: str, html: str):
    resend.Emails.send(
        {
            "from": os.getenv("RESEND_EMAIL"),
            "to": to,
            "subject": title,
            "html": html,
        }
    )
