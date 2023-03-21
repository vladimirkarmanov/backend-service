from config import Config
from core.migrations import apply_alembic_migrations

config = Config()

apply_alembic_migrations(verbose=config.DEBUG)
