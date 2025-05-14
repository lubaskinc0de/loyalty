from dishka import FromDishka
from flask import Blueprint, Response, jsonify, render_template

from loyalty.application.loyalty.read import ReadLoyalties

root = Blueprint("root", __name__)


@root.route("/ping/", strict_slashes=False)
def ping() -> Response:
    return jsonify({"ping": "pong"})


@root.route("/", strict_slashes=False)
def home() -> str:
    return render_template("index.html")
