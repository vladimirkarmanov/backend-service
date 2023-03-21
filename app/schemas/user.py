from pydantic import BaseModel, validator


class UserCreateSchema(BaseModel):
    name: str


class UserRetrieveSchema(UserCreateSchema):
    id: int

    class Config:
        orm_mode = True


class UserBalanceRetrieveSchema(BaseModel):
    balance: str

    class Config:
        orm_mode = True

    @validator("balance", pre=True)
    def balance_format(cls, value):
        return format(value, '.2f')
