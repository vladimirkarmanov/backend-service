from sqlalchemy import Column, String, Integer, Float, ForeignKey, CheckConstraint

from .base import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        CheckConstraint("balance >= 0"),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    balance = Column(Float, nullable=False, default=0.00)


class UserTransaction(Base):
    __tablename__ = "user_transaction"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    transaction_id = Column(Integer, ForeignKey("transaction.id"), unique=True)
    balance_after_trx = Column(Float, nullable=False)
