from aiohttp import web

app = web.Application()


def init_app() -> web.Application:
    from config import Config
    from api.routes import add_routes

    app['config'] = Config

    add_routes(app)

    return app
