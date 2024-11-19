from pathlib import Path

import UnityPy
from UnityPy.classes import TextAsset

from .exceptions import AssetNotFoundError


class DataExtractor:
    def __init__(self, data_all_file_path: Path):
        if not data_all_file_path.exists():
            msg = f"Data_all file not found: {data_all_file_path}."
            raise FileNotFoundError(msg)
        self.data_all_file_path = data_all_file_path
        self.data_all_bundle = UnityPy.load(data_all_file_path)

    def extract_asset(self, asset_name: str, output_dir_path: Path) -> None:
        output_dir_path.mkdir(parents=True, exist_ok=True)
        for asset_path, asset_reader in self.data_all_bundle.container.items():
            if asset_name.lower() == Path(asset_path).stem:
                asset: TextAsset = asset_reader.read()
                output_file_path = output_dir_path / f"{asset.m_Name}.tsv"
                with output_file_path.open("wb") as output_file:
                    output_file.write(asset.m_Script.encode("utf-8", "surrogateescape"))
                    return
        msg = f"Asset not found: {asset_name}"
        raise AssetNotFoundError(msg)

    def extract_asset_names(self, output_file_path: Path) -> None:
        output_dir_path = output_file_path.parent
        output_dir_path.mkdir(parents=True, exist_ok=True)
        asset_names = self.get_asset_names()
        with output_file_path.open("w+") as output_file:
            output_file.write("\n".join(asset_names))

    def get_asset_names(self) -> list[str]:
        return [Path(asset_path).stem for asset_path in self.data_all_bundle.container]
