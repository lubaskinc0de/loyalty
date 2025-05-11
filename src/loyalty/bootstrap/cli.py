import argparse
import contextlib
import sys

import alembic.config

from loyalty.adapters.db.alembic.config import get_alembic_config_path
from loyalty.bootstrap.entrypoint.flask_api import main as run_api


def run_migrations() -> None:
    alembic_path_gen = get_alembic_config_path()
    alembic_path = str(next(alembic_path_gen))
    alembic.config.main(argv=["-c", alembic_path, "upgrade", "head"])
    with contextlib.suppress(StopIteration):
        next(alembic_path_gen)


def autogenerate_migrations(message: str) -> None:
    alembic_path_gen = get_alembic_config_path()
    alembic_path = str(next(alembic_path_gen))
    alembic.config.main(argv=["-c", alembic_path, "revision", "--autogenerate", "-m", message])
    with contextlib.suppress(StopIteration):
        next(alembic_path_gen)


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Loyalty system management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run")
    run_subparsers = run_parser.add_subparsers(dest="service", required=True)

    run_api_parser = run_subparsers.add_parser("api")
    run_api_parser.set_defaults(func=lambda _: run_api(argv))

    migration_parser = subparsers.add_parser("migrations")
    migration_subparsers = migration_parser.add_subparsers(dest="operation", required=True)

    autogen_parser = migration_subparsers.add_parser("autogenerate")
    autogen_parser.add_argument("message")
    autogen_parser.set_defaults(func=lambda args: autogenerate_migrations(args.message))

    args = parser.parse_args(argv)
    run_migrations()

    if hasattr(args, "func"):
        args.func(args)


if __name__ == "__main__":
    main()
