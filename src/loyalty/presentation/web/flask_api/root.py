from flask import Flask


def ping() -> str:
    return "pong"


def include_root(app: Flask) -> None:
    app.route("/ping/")(ping)
