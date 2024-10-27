from collections.abc import Iterable
from pathlib import Path

import UnityPy
from UnityPy.classes import TextAsset


class DataExtractor:
    def __init__(self, data_all_file_path: str):
        self._validate_file_exists(data_all_file_path)

        self.data_all_file_path = data_all_file_path
        self.data_all_bundle = UnityPy.load(data_all_file_path)

    def extract_assets(self, asset_names: Iterable[str], output_dir_path: str) -> None:
        for asset_name in asset_names:
            self.extract_asset(asset_name, output_dir_path)

    def extract_asset(self, asset_name: str, output_dir_path: str) -> None:
        Path(output_dir_path).mkdir(parents=True, exist_ok=True)
        for asset_path, asset_reader in self.data_all_bundle.container.items():
            if asset_name.lower() == Path(asset_path).stem:
                asset: TextAsset = asset_reader.read()
                output_file_path = Path(output_dir_path) / f"{asset.m_Name}.tsv"
                with output_file_path.open("wb") as output_file:
                    output_file.write(asset.m_Script.encode("utf-8", "surrogateescape"))

    def extract_asset_names(self, output_file_path: str) -> None:
        output_dir_path = Path(output_file_path).parent
        output_dir_path.mkdir(parents=True, exist_ok=True)
        asset_names = self.get_asset_names()
        with Path(output_file_path).open("w+") as output_file:
            output_file.write("\n".join(asset_names))

    def get_asset_names(self) -> list[str]:
        return [Path(asset_path).stem for asset_path in self.data_all_bundle.container]

    def _validate_file_exists(self, file_path: str) -> None:
        if not Path(file_path).is_file():
            msg = f"File {file_path} is not found"
            raise FileNotFoundError(msg)
