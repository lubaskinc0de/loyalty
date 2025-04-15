import binascii
from binascii import unhexlify

from adaptix import P, Retort, dumper, name_mapping
from geoalchemy2 import WKBElement
from shapely import wkb, wkt  # type: ignore

from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.client import Client


def location_dumper(location: str | WKBElement) -> str:
    # на самом деле, в полях location у клиента и бизнеса лежит не строка, а WKBElement
    # но мы можем туда присваивать строку потому что внутри оно хитро маппиться на WKBElement
    # лучше было бы сделать через преобразование на уровне самой алхимии, но мне лень
    # поэтому этот код маппит WKBElement на человекочитаемое представление
    # а еще сюда может прилетать строка в случае когда мы создаем клиента (ведь мы там присваиваем строку в location)
    if isinstance(location, str):
        return location
    binary = unhexlify(binascii.hexlify(location.data))
    point = wkb.loads(binary)
    return wkt.dumps(point)  # type: ignore


serializer = Retort(
    recipe=[
        dumper(P[Client].location, lambda x: location_dumper(x)),
        dumper(P[BusinessBranch].location, lambda x: location_dumper(x)),
        name_mapping(BusinessBranch, skip=["business"]),
    ],
)
