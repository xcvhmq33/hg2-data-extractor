import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

import requests
import UnityPy
from requests.exceptions import HTTPError
from tqdm import tqdm
from UnityPy.classes import TextAsset

from .config import settings
from .enums import Server


class GameObjectJSON(TypedDict):
    N: str
    FS: str
    CRC: str
    PN: str
    ULM: str
    DLM: str
    BT: str
    R: str
    APS: list[str]
    HS: str | None


@dataclass
class GameObject:
    N: str
    FS: str
    CRC: str
    PN: str
    ULM: str
    DLM: str
    BT: str
    R: str
    APS: list[str]
    HS: str | None = None

    @property
    def full_name(self) -> str:
        if self.HS is not None:
            return f"{self.N}_{self.HS}_{self.CRC}"
        return f"{self.N}_{self.CRC}"

    @property
    def file_name(self) -> str:
        return str(Path(self.N).name)


class DataDownloader:
    def __init__(self, server: Server, version: str):
        self.server = server
        self.validate_version(version)
        self.version = version.replace(".", "_").strip()
        self.data_url = settings.create_data_url(version, server)
        self.resources_url = settings.create_resources_url(version, server)

    def download_data_all(self, output_dir: Path, *, progressbar: bool = False) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / "data_all.unity3d"
        data_version = self.get_data_version()
        data_json = self.parse_objects_json(data_version)[0]
        data_all = GameObject(**data_json)
        data_all_url = f"{self.data_url}/AssetBundles/{data_all.full_name}"
        self.download_file(data_all_url, output, progressbar=progressbar)

    def download_resources(
        self, output_dir: Path, *, progressbar: bool = False, overwrite: bool = False
    ) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        resources_version = self.get_resources_version()
        resources_json = self.parse_objects_json(resources_version)
        resources = self.parse_resources(resources_json)
        for resource in resources:
            output = output_dir / resource.file_name
            if output.is_file() and not overwrite:
                continue
            resource_url = f"{self.resources_url}/{resource.full_name}"
            self.download_file(resource_url, output, progressbar=progressbar)

    @staticmethod
    def download_file(url: str, output: Path, *, progressbar: bool = False) -> None:
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

    @staticmethod
    def parse_resources(resources_json: list[GameObjectJSON]) -> list[GameObject]:
        resources = []
        for resource_json in resources_json:
            resource = GameObject(**resource_json)
            if resource.N.startswith("StreamingAssets/"):
                resources.append(resource)

        return resources

    @staticmethod
    def parse_objects_json(unity_file: bytes) -> list[GameObjectJSON]:
        bundle = UnityPy.load(unity_file)
        for asset_reader in bundle.objects:
            asset = asset_reader.read()
            if isinstance(asset, TextAsset):
                object_json = asset.m_Script.splitlines()
                parsed_objects_json = []
                for i, file_json in enumerate(object_json):
                    if i <= 1:
                        continue
                    parsed_object_json = json.loads(file_json)
                    parsed_objects_json.append(parsed_object_json)

        return parsed_objects_json

    def get_data_version(self) -> bytes:
        data_version_url = f"{self.data_url}/DataVersion.unity3d"
        data_version = self.get_file_version(data_version_url)

        return data_version

    def get_resources_version(self) -> bytes:
        resources_version_url = f"{self.resources_url}/ResourceVersion.unity3d"
        resources_version = self.get_file_version(resources_version_url)

        return resources_version

    @staticmethod
    def get_file_version(file_url: str) -> bytes:
        try:
            response = requests.get(file_url, timeout=10)
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
