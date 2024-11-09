from typing import Annotated

import typer

from .data_cipher import DataCipher
from .data_downloader import DataDownloader
from .data_extractor import DataExtractor
from .utils import ask_overwrite_if_exists

app = typer.Typer()


@app.command(help="Extracts all asset names from data_all_dec.unity3d")
def lst(
    output_file_path: Annotated[str, typer.Argument()] = "extracted/asset_names.txt",
    data_all_file_path: Annotated[
        str, typer.Argument()
    ] = "data_all/data_all_dec.unity3d",
) -> None:
    if ask_overwrite_if_exists(output_file_path):
        data_extractor = DataExtractor(data_all_file_path)
        data_extractor.extract_asset_names(output_file_path)


@app.command(help="Downloads data_all.unity3d from server")
def download(
    server: str,
    version: str,
    output_dir_path: Annotated[str, typer.Argument()] = "data_all",
) -> None:
    output_file_path = f"{output_dir_path}/data_all.unity3d"
    if ask_overwrite_if_exists(output_file_path):
        data_downloader = DataDownloader(server, version)
        data_downloader.download_data_all(output_dir_path, progressbar=True)


@app.command(help="Decrypts data_all.unity3d")
def decrypt(
    input_file_path: Annotated[str, typer.Argument()] = "data_all/data_all.unity3d",
    output_file_path: Annotated[
        str, typer.Argument()
    ] = "data_all/data_all_dec.unity3d",
) -> None:
    if ask_overwrite_if_exists(output_file_path):
        DataCipher.decrypt_file(input_file_path, output_file_path)


@app.command(help="Extracts text assets data from data_all_dec.unity3d")
def extract(
    asset_names: Annotated[
        str, typer.Argument()
    ] = "WeaponDataV3,CostumeDataV2,PassiveSkillDataV3,SpecialAttributeDataV2,PetData,PetSkillData",
    output_dir_path: Annotated[str, typer.Argument()] = "extracted",
    data_all_file_path: Annotated[
        str, typer.Argument()
    ] = "data_all/data_all_dec.unity3d",
) -> None:
    data_extractor = DataExtractor(data_all_file_path)
    for asset_name in asset_names.split(","):
        extract_file_path = f"{output_dir_path}/{asset_name}.tsv"
        if ask_overwrite_if_exists(extract_file_path):
            data_extractor.extract_asset(asset_name, output_dir_path)


def main() -> None:
    app()
