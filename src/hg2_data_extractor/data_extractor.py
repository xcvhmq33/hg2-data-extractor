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
        self.data_all_bundle = UnityPy.load(str(data_all_file_path))
        if not self.data_all_bundle.container:
            msg = f"No assets found in the {self.data_all_file_path}."
            raise AssetNotFoundError(msg)
        self.asset_map = {
            Path(asset).stem: asset_reader
            for asset, asset_reader in self.data_all_bundle.container.items()
        }

    def extract_asset(self, asset_name: str, output_dir_path: Path) -> None:
        output_dir_path.mkdir(parents=True, exist_ok=True)
        asset_reader = self.asset_map.get(asset_name.lower())
        if asset_reader:
            asset_obj: TextAsset = asset_reader.read()
            output = output_dir_path / f"{asset_obj.m_Name}.tsv"
            with output.open("wb") as file:
                file.write(asset_obj.m_Script.encode("utf-8", "surrogateescape"))
        else:
            msg = f"Asset `{asset_name}` not found in {self.data_all_file_path}."
            raise AssetNotFoundError(msg)

    def extract_asset_names(self, output_file_path: Path) -> None:
        output_dir_path = output_file_path.parent
        output_dir_path.mkdir(parents=True, exist_ok=True)
        asset_names = self.get_asset_names()
        with output_file_path.open("w+") as output_file:
            output_file.write("\n".join(asset_names))

    def get_asset_names(self) -> list[str]:
        return [Path(asset_path).stem for asset_path in self.data_all_bundle.container]
