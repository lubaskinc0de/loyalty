from typing import BinaryIO, cast
from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request
from werkzeug.datastructures import FileStorage

from loyalty.adapters.image_utils import is_valid_image
from loyalty.application.business.attach import AttachBusinessAvatar
from loyalty.application.business.create import BusinessForm, CreateBusiness
from loyalty.application.business.detach import DetachBusinessAvatar
from loyalty.application.business.read import ReadBusiness
from loyalty.application.business.stats import ReadBusinessStats
from loyalty.bootstrap.di.providers.data import Body
from loyalty.presentation.web.flask_api.exceptions import (
    EmptyFilenameError,
    IsNotImageError,
    MissingFileExtensionError,
    MissingImageError,
)
from loyalty.presentation.web.serializer import serializer

business = Blueprint("business", __name__)


@business.route("/", methods=["POST"], strict_slashes=False)
def create_business(*, interactor: FromDishka[CreateBusiness], form: Body[BusinessForm]) -> Response:
    interactor.execute(form.data)
    return Response(status=204)


@business.route("/<uuid:business_id>", methods=["GET"], strict_slashes=False)
def read_business(business_id: UUID, interactor: FromDishka[ReadBusiness]) -> Response:
    result = interactor.execute(business_id)
    return jsonify(serializer.dump(result))


@business.route("/attach", methods=["PUT"], strict_slashes=False)
def attach(
    *,
    interactor: FromDishka[AttachBusinessAvatar],
) -> Response:
    if "image" not in request.files:
        raise MissingImageError

    file: FileStorage = request.files["image"]
    if file.filename == "":
        raise EmptyFilenameError

    file_parts = file.filename.split(".")
    if len(file_parts) < 2:
        raise MissingFileExtensionError
    file_ext = file_parts[-1]

    file_stream = cast("BinaryIO", file.stream)
    is_valid = is_valid_image(file_stream)
    if not is_valid:
        raise IsNotImageError

    file_stream.seek(0, 2)
    file_size = file_stream.tell()
    file_stream.seek(0)

    result = interactor.execute(
        file_stream,
        file_ext,
        file_size,
    )
    return jsonify(serializer.dump(result))


@business.route("/attach", methods=["DELETE"], strict_slashes=False)
def detach(
    *,
    interactor: FromDishka[DetachBusinessAvatar],
) -> Response:
    interactor.execute()
    return Response(status=204)


@business.route("/stats", methods=["GET"], strict_slashes=False)
def read_business_stats(interactor: FromDishka[ReadBusinessStats]) -> Response:
    result = interactor.execute()
    return jsonify(serializer.dump(result))
