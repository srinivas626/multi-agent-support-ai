from pydantic import BaseModel, Field


class TicketRequest(BaseModel):

    title: str = Field(
        min_length=3,
        max_length=200,
    )

    description: str = Field(
        min_length=5,
        max_length=5000,
    )

    priority: str = "medium"


class EmailRequest(BaseModel):

    to: str

    subject: str = Field(
        min_length=1,
        max_length=200,
    )

    body: str = Field(
        min_length=1,
        max_length=10000,
    )
