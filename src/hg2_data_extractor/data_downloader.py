import json
import re
from pathlib import Path

import requests
import UnityPy
from requests.exceptions import HTTPError
from tqdm import tqdm
from UnityPy.classes import TextAsset

from .enums import Server


class DataDownloader:
    def __init__(self, server: Server, version: str):
        self.server = server
        self._validate_version(version)
        self.version = version.replace(".", "_").strip()
        self.data_url = self._get_data_url()

    def download_data_all(
        self, output_dir_path: Path, progressbar: bool = False
    ) -> None:
        output_dir_path.mkdir(parents=True, exist_ok=True)
        output_file_path = output_dir_path / "data_all.unity3d"
        data_version_file = self._get_data_version_file()
        data_json = self._parse_data_json(data_version_file)
        data_all_name = self._parse_data_all_name(data_json)
        data_all_url = f"{self.data_url}/AssetBundles/{data_all_name}"
        response = requests.get(data_all_url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("Content-Length", 0))
        with (
            tqdm(
                desc=output_file_path.name,
                unit="B",
                miniters=1,
                unit_divisor=1024,
                total=total_size,
                unit_scale=True,
                disable=(not progressbar),
            ) as t,
            output_file_path.open("wb") as f,
        ):
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    t.update(len(chunk))
                    f.write(chunk)

    def _get_data_url(self) -> str:
        data_urls = {
            Server.CN: f"https://assets.hsod2.benghuai.com/asset_bundle/{self.version}/original/android/Data",
            Server.JP: f"https://s3-ap-northeast-1.amazonaws.com/hsod2-asset/asset_bundle/{self.version}/jporiginal/android/Data",
        }

        return data_urls[self.server]

    def _get_data_version_file(self) -> bytes:
        data_version_url = f"{self.data_url}/DataVersion.unity3d"
        response = requests.get(data_version_url)
        if response.status_code == 403:
            msg = "403 Client Error: Forbidden. It's likely the version is too high"
            raise HTTPError(msg)

        return response.content

    def _parse_data_json(self, data_version_file: bytes) -> str:
        bundle = UnityPy.load(data_version_file)
        asset_reader = bundle.objects[1]
        asset: TextAsset = asset_reader.read()
        data_json = asset.m_Script.splitlines()[2]

        return data_json

    def _parse_data_all_name(self, data_json: str) -> str:
        parsed_data_json: dict[str, str] = json.loads(data_json)
        n = parsed_data_json["N"]
        hs = parsed_data_json["HS"]
        crc = parsed_data_json["CRC"]
        data_all_name = f"{n}_{hs}_{crc}"

        return data_all_name

    @staticmethod
    def _validate_version(version: str) -> None:
        if not re.match(r"^(?:[1-9]|[1-9]\d)[.|_][0-9]$", version):
            msg = "Version must be a valid game version (e.g `11_1` or `9.8`)"
            raise ValueError(msg)
