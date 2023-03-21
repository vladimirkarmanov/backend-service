from pydantic import BaseModel


class UserTransactionCreateSchema(BaseModel):
    user_id: int
    transaction_id: int
    balance_after_trx: float


class UserTransactionRetrieveSchema(UserTransactionCreateSchema):
    id: int

    class Config:
        orm_mode = True
