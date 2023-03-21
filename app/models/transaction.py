from sqlalchemy import Column, Integer, Enum, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID

from schemas.transaction import TransactionTypeEnum
from .base import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(UUID(as_uuid=True), unique=True)
    type = Column(Enum(TransactionTypeEnum))
    amount = Column(Float, default=0.00)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(Transaction, self).__init__(**kwargs)
        self.amount = float(kwargs.get('amount'))
