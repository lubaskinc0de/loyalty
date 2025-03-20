import contextlib
import sys

import alembic.config

from crudik.adapters.db.alembic.config import get_alembic_config_path
from crudik.bootstrap.entrypoint.fast_api import run_api


def run_migrations() -> None:
    alembic_path_gen = get_alembic_config_path()
    alembic_path = str(next(alembic_path_gen))
    alembic.config.main(
        argv=["-c", alembic_path, "upgrade", "head"],
    )

    with contextlib.suppress(StopIteration):
        next(alembic_path_gen)


def autogenerate_migrations(*args: str) -> None:
    alembic_path_gen = get_alembic_config_path()
    alembic_path = str(next(alembic_path_gen))
    alembic.config.main(
        argv=["-c", alembic_path, "revision", "--autogenerate", "-m", args[0]],
    )

    with contextlib.suppress(StopIteration):
        next(alembic_path_gen)


def main() -> None:
    argv = sys.argv[1:]

    if not argv:
        return

    try:
        module = argv[0]
        option = argv[1]
        args = argv[2:]
    except IndexError:
        return

    modules = {
        "run": {
            "api": run_api,
        },
        "migrations": {
            "autogenerate": autogenerate_migrations,
        },
    }

    if module not in modules:
        return

    if option not in modules[module]:  # type: ignore
        return

    run_migrations()
    modules[module][option](args)  # type: ignore
