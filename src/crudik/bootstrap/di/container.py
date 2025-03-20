from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from crudik.bootstrap.di.providers.adapter import adapter_provider
from crudik.bootstrap.di.providers.command import CommandProvider
from crudik.bootstrap.di.providers.config import ConfigProvider


def get_async_container() -> AsyncContainer:
    providers = [
        ConfigProvider(),
        FastapiProvider(),
        adapter_provider(),
        CommandProvider(),
    ]
    container = make_async_container(*providers)
    return container
