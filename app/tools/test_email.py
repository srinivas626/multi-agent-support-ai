from app.tools.email_tool import send_email


result = send_email(
    to="support@example.com",
    subject="VPN Issue",
    body="A user is experiencing a VPN connection problem.",
)

print(result)
