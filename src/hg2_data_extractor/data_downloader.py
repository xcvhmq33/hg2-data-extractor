import json
import re
from pathlib import Path

import requests
import UnityPy
from requests.exceptions import HTTPError
from tqdm import tqdm
from UnityPy.classes import TextAsset

from .config import settings
from .enums import Server


class DataDownloader:
    def __init__(self, server: Server, version: str):
        self.server = server
        self.validate_version(version)
        self.version = version.replace(".", "_").strip()
        self.data_url = settings.create_data_url(version, server)

    def download_data_all(self, output_dir: Path, *, progressbar: bool = False) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / "data_all.unity3d"
        data_version = self.get_data_version()
        data_json = self.parse_data_json(data_version)
        data_all_name = self.parse_data_all_name(data_json)
        data_all_url = f"{self.data_url}/AssetBundles/{data_all_name}"
        self.download_file(data_all_url, output, progressbar=progressbar)

    def download_file(
        self, url: str, output: Path, *, progressbar: bool = False
    ) -> None:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("Content-Length", 0))
        with (
            tqdm(
                desc=output.name,
                unit="B",
                miniters=1,
                unit_divisor=1024,
                total=total_size,
                unit_scale=True,
                disable=(not progressbar),
            ) as t,
            output.open("wb") as f,
        ):
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    t.update(len(chunk))
                    f.write(chunk)

    def parse_data_all_name(self, data_json: str) -> str:
        parsed_data_json: dict[str, str] = json.loads(data_json)
        n = parsed_data_json["N"]
        crc = parsed_data_json["CRC"]
        if float(self.version.replace("_", ".")) < 11.4:
            hs = parsed_data_json["HS"]
            data_all_name = f"{n}_{hs}_{crc}"
        else:
            data_all_name = f"{n}_{crc}"

        return data_all_name

    def parse_data_json(self, data_version: bytes) -> str:
        bundle = UnityPy.load(data_version)
        asset_reader = bundle.objects[1]
        asset: TextAsset = asset_reader.read()
        data_json = asset.m_Script.splitlines()[2]

        return data_json

    def get_data_version(self) -> bytes:
        data_version_url = f"{self.data_url}/DataVersion.unity3d"
        try:
            response = requests.get(data_version_url, timeout=10)
            response.raise_for_status()
        except HTTPError as e:
            msg = f"{e}\nIt's more likely the version is too low/high."
            raise ValueError(msg) from e

        return response.content

    @staticmethod
    def validate_version(version: str) -> None:
        pattern = r"""
            ^                   # begin
            [1-9]\d*            # first part of the version
            [.|_]               # separator
            \d+                 # second part of the version
            $                   # end
        """
        if not re.match(pattern, version, re.VERBOSE):
            msg = f"Invalid version format: {version}. Expected x_y or x.y"
            raise ValueError(msg)
