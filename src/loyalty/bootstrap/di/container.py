from dishka import Container, Provider, make_container
from dishka.integrations.flask import FlaskProvider

from loyalty.bootstrap.di.providers.adapter import adapter_provider
from loyalty.bootstrap.di.providers.command import CommandProvider
from loyalty.bootstrap.di.providers.config import ConfigProvider
from loyalty.bootstrap.di.providers.gateway import GatewayProvider


def provider_set() -> list[Provider]:
    return [
        ConfigProvider(),
        FlaskProvider(),
        adapter_provider(),
        CommandProvider(),
        GatewayProvider(),
    ]


def get_container() -> Container:
    return make_container(*provider_set())
