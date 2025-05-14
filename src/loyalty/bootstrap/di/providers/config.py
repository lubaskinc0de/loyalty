from dishka import Provider, Scope, provide

from loyalty.adapters.config_loader import Config, DBConnectionConfig, JWTConfig, StorageConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def config(self) -> Config:
        return Config.load_from_environment()

    @provide
    def db_connection(self, config: Config) -> DBConnectionConfig:
        return config.db_connection

    @provide
    def jwt(self, config: Config) -> JWTConfig:
        return config.jwt

    @provide
    def storage(self, config: Config) -> StorageConfig:
        return config.storage
