from pydantic import BaseModel, Field, field_validator


class CreateExpense(BaseModel):
    category: str = Field(..., examples=["Food"])
    description: str = Field(..., examples=["Lunch at cafe"])
    amount: float = Field(
        ...,
        examples=[50.0],
    )
    date: str = Field(..., examples=["2020-12-14"])

    @field_validator("amount")
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError("Amount cannot be negative")
        return v


class UpdateExpense(BaseModel):
    category: str | None = Field(None, examples=["Food"])
    description: str | None = Field(None, examples=["Lunch at cafe"])
    amount: float | None = Field(
        None,
        examples=[50.0],
    )
    date: str | None = Field(None, examples=["2020-12-14"])

    @field_validator("amount")
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError("Amount cannot be negative")
        return v
