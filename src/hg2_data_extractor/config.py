from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from .enums import Server


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env")
    JP_HOST: str = "https://s3-ap-northeast-1.amazonaws.com/"
    CN_HOST: str = "https://assets.hsod2.benghuai.com/"
    JP_ALIAS: str = "jporiginal"
    CN_ALIAS: str = "original"
    DATA_PATH_CORE_TEMPLATE: str = "asset_bundle/{version}/{server}/android/"

    def create_core_url(self, version: str, server: Server) -> HttpUrl:
        if server == Server.CN:
            host = self.CN_HOST
            alias = self.CN_ALIAS
            extra = ""
        elif server == Server.JP:
            host = self.JP_HOST
            alias = self.JP_ALIAS
            extra = "hsod2-asset/"
        data_path_core = self.DATA_PATH_CORE_TEMPLATE.format_map(
            {"version": version, "server": alias}
        )
        core_url = HttpUrl(f"{host}{extra}{data_path_core}")
        return core_url

    def create_data_url(self, version: str, server: Server) -> HttpUrl:
        core_url = self.create_core_url(version, server)
        data_url = HttpUrl(str(core_url) + "Data")
        return data_url

    def create_resources_url(self, version: str, server: Server) -> HttpUrl:
        core_url = self.create_core_url(version, server)
        resources_url = HttpUrl(str(core_url) + "Res")
        return resources_url


settings = Settings()
