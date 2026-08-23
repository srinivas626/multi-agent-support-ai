from app.tools.ticket_tool import create_ticket


ticket = create_ticket(
    title="VPN connection issue",
    description="User cannot connect to company VPN.",
    priority="high",
)

print(ticket)
