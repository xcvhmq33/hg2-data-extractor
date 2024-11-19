class BaseExtractorError(Exception): ...


class AssetNotFoundError(BaseExtractorError):
    def __init__(self, msg: str, *, asset_name: str | None = None):
        self.asset_name = asset_name
        self.msg = msg
        super().__init__(self.msg)
