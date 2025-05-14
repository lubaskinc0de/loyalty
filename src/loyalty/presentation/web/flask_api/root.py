from dishka import FromDishka
from flask import Blueprint, Response, jsonify, render_template

from loyalty.application.business.read import PreviewBusiness
from loyalty.application.common.statistic.read import ReadStatistics

root = Blueprint("root", __name__)


@root.route("/ping/", strict_slashes=False)
def ping() -> Response:
    return jsonify({"ping": "pong"})


@root.route("/", strict_slashes=False)
def home(*, business_interactor: FromDishka[PreviewBusiness], statistics_interactor: FromDishka[ReadStatistics]) -> str:
    businesses = business_interactor.execute()
    statistic = statistics_interactor.execute()

    return render_template("index.html", businesses=businesses, statistic=statistic)
