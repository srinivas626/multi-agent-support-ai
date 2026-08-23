from datetime import datetime


def send_email(
    to: str,
    subject: str,
    body: str,
) -> dict:

    result = {
        "status": "sent",
        "to": to,
        "subject": subject,
        "body": body,
        "sent_at": datetime.utcnow().isoformat(),
    }

    return result
