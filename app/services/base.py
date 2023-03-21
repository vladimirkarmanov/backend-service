from repositories.transaction import TransactionRepository
from repositories.user import UserRepository, UserTransactionRepository


class UserServiceMixin:
    _user_service = None
    _user_repository = None

    @property
    def user_service(self):
        from services.user import UserService

        self._user_service = self._user_service or UserService()
        return self._user_service

    @property
    def user_repository(self) -> UserRepository:
        self._user_repository = self._user_repository or UserRepository()
        return self._user_repository


class UserTransactionServiceMixin:
    _user_transaction_service = None
    _user_transaction_repository = None

    @property
    def user_transaction_service(self):
        from services.user_transaction import UserTransactionService

        self._user_transaction_service = self._user_transaction_service or UserTransactionService()
        return self._user_transaction_service

    @property
    def user_transaction_repository(self) -> UserTransactionRepository:
        self._user_transaction_repository = self._user_transaction_repository or UserTransactionRepository()
        return self._user_transaction_repository


class TransactionServiceMixin:
    _transaction_service = None
    _transaction_repository = None

    @property
    def transaction_service(self):
        from services.transaction import TransactionService

        self._transaction_service = self._transaction_service or TransactionService()
        return self._transaction_service

    @property
    def transaction_repository(self) -> TransactionRepository:
        self._transaction_repository = self._transaction_repository or TransactionRepository()
        return self._transaction_repository
