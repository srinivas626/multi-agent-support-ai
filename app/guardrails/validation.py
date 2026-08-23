from pydantic import BaseModel, Field, field_validator


class TicketInput(BaseModel):

    title: str = Field(
        min_length=3,
        max_length=200,
    )

    description: str = Field(
        min_length=5,
        max_length=5000,
    )

    priority: str = "medium"

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):

        allowed = {
            "low",
            "medium",
            "high",
        }

        if value not in allowed:
            raise ValueError(
                "Priority must be low, medium, or high."
            )

        return value


class EmailInput(BaseModel):

    to: str

    subject: str = Field(
        min_length=1,
        max_length=200,
    )

    body: str = Field(
        min_length=1,
        max_length=10000,
    )
