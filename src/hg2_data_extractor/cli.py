from pathlib import Path

import typer

from .data_cipher import DataCipher
from .data_downloader import DataDownloader
from .data_extractor import DataExtractor

app = typer.Typer()


def ask_for_rewrite_if_exists(file_path: str) -> bool:
    if Path(file_path).is_file():
        message = f"{file_path} is already exists, overwrite it? (y/n): "
        rewrite = input(message).lower() == "y"
    else:
        rewrite = True

    return rewrite


@app.command(help="Prints all asset names in data_all_decrypted.unity3d to stdout")
def lst(data_all_dir_path: str = "data_all") -> None:
    data_extractor = DataExtractor(f"{data_all_dir_path}/data_all_decrypted.unity3d")
    names = data_extractor.get_asset_names()
    for name in names:
        typer.echo(name)


@app.command(help="Downloads data_all.unity3d from server")
def download(server: str, version: str, output_dir_path: str = "data_all") -> None:
    data_downloader = DataDownloader(server, version)
    if ask_for_rewrite_if_exists(f"{output_dir_path}/data_all_encrypted.unity3d"):
        data_downloader.download_data_all(output_dir_path)


@app.command(help="Decrypts data_all.unity3d")
def decrypt(
    input_file_path: str = "data_all/data_all_encrypted.unity3d",
    output_file_path: str = "data_all/data_all_decrypted.unity3d",
) -> None:
    if ask_for_rewrite_if_exists(output_file_path):
        DataCipher.decrypt_file(input_file_path, output_file_path)


@app.command(help="Extracts text assets data from data_all_decrypted.unity3d")
def extract(
    data_all_decrypted_file_path: str = "data_all/data_all_decrypted.unity3d",
    output_dir_path: str = "extracted",
    asset_names: str = "WeaponDataV3,CostumeDataV2,PassiveSkillDataV3,SpecialAttributeDataV2,PetData,PetSkillData",
) -> None:
    data_extractor = DataExtractor(data_all_decrypted_file_path)
    for asset_name in asset_names.split(","):
        extract_file_path = f"{output_dir_path}/{asset_name}.tsv"
        if ask_for_rewrite_if_exists(extract_file_path):
            data_extractor.extract_asset(asset_name, output_dir_path)


def main() -> None:
    app()
