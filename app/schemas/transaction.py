from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, validator


class TransactionTypeEnum(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class TransactionCreateSchema(BaseModel):
    uid: UUID
    type: TransactionTypeEnum
    amount: str
    timestamp: datetime


class TransactionRetrieveSchema(BaseModel):
    type: TransactionTypeEnum
    amount: str

    class Config:
        orm_mode = True

    @validator("amount", pre=True)
    def amount_format(cls, value):
        return format(value, '.2f')
