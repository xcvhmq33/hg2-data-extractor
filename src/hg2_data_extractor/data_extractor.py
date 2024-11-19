from pathlib import Path

import UnityPy
from UnityPy.classes import TextAsset

from .exceptions import AssetNotFoundError


class DataExtractor:
    def __init__(self, data_all: Path):
        if not data_all.exists():
            msg = f"Data_all file not found: {data_all}."
            raise FileNotFoundError(msg)
        self.data_all = data_all
        self.data_all_bundle = UnityPy.load(str(data_all))
        if not self.data_all_bundle.container:
            msg = f"No assets found in the {self.data_all}."
            raise AssetNotFoundError(msg)
        self.asset_map = {
            Path(asset).stem: asset_reader
            for asset, asset_reader in self.data_all_bundle.container.items()
        }

    def extract_asset(self, asset_name: str, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        asset_reader = self.asset_map.get(asset_name.lower())
        if asset_reader:
            asset_obj: TextAsset = asset_reader.read()
            output = output_dir / f"{asset_obj.m_Name}.tsv"
            with output.open("wb") as file:
                file.write(asset_obj.m_Script.encode("utf-8", "surrogateescape"))
        else:
            msg = f"Asset `{asset_name}` not found in {self.data_all}."
            raise AssetNotFoundError(msg)

    def list_asset_names(self, output_file: Path) -> None:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w+") as file:
            file.write("\n".join(self.asset_map))
