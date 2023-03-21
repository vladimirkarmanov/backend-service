from aiohttp import web

from schemas.transaction import TransactionCreateSchema
from schemas.user import UserCreateSchema
from services.transaction import TransactionService
from services.user import UserService


async def create_user(request):
    json = await request.json()
    user_payload = UserCreateSchema(**json)
    user_service = UserService()
    user = await user_service.create(user_payload)
    return web.json_response(user.__dict__, status=201)


async def get_user_balance(request):
    user_id = request.match_info['id']
    date = request.query.get('date')
    user_service = UserService()
    balance = await user_service.get_user_balance(int(user_id), date)
    return web.json_response(balance.__dict__)


async def add_transaction(request):
    json = await request.json()

    user_service = UserService()
    user = await user_service.get_last_created_user()  # для тестов, обычно берется из JWT токена

    transaction_payload = TransactionCreateSchema(**json)
    transaction_service = TransactionService()
    await transaction_service.create(user.id, transaction_payload)
    return web.Response(status=200)


async def get_transaction(request):
    transaction_uid = request.match_info['uid']
    transaction_service = TransactionService()
    info = await transaction_service.get_transaction_info(transaction_uid)
    return web.json_response(info.__dict__)


def add_routes(app):
    app.router.add_route('POST', r'/v1/user', create_user, name='create_user')
    app.router.add_route('GET', r'/v1/user/{id}/balance', get_user_balance, name='get_user_balance')
    app.router.add_route('POST', r'/v1/transaction', add_transaction, name='add_transaction')
    app.router.add_route('GET', r'/v1/transaction/{uid}', get_transaction, name='get_transaction')
