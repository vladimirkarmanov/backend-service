import logging
import sys

from alembic import command
from alembic.config import Config

logger = logging.getLogger("api")


# log
def write_to_stderr(chars: str):
    sys.stderr.write(chars + "\n")


def apply_alembic_migrations(verbose: bool = False) -> None:
    separate = "-" * 60
    separate_short = "-" * 22
    logger.info("Applying migrations")
    write_to_stderr(f"{separate_short}Alembic history:{separate_short}")
    config = Config(stdout=sys.stderr)
    config.set_main_option("script_location", "alembic")
    command.history(config)
    write_to_stderr(separate)
    write_to_stderr(f"{separate_short}Alembic upgrade:{separate_short}")
    command.upgrade(config, "head")
    command.current(config, verbose=verbose)
    write_to_stderr(separate)
