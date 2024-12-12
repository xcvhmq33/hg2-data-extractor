import functools
from pathlib import Path
from typing import Annotated

import typer

from .data_cipher import DataCipher
from .data_downloader import DataDownloader
from .data_extractor import DataExtractor
from .enums import PRESETS, Preset, Server

app = typer.Typer()

output_dir_option = typer.Option(
    "--output-dir",
    "-o",
    help="Path to the directory where files will be saved.",
)

data_all_option = typer.Option(
    "--data-all",
    "-d",
    help="Path to the data_all_dec.unity3d file.",
)


def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            typer.secho(e, fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)

    return wrapper


@app.command()
@handle_errors
def lst(
    output_dir: Annotated[
        Path,
        output_dir_option,
    ] = Path("extracted"),
    data_all: Annotated[
        Path,
        data_all_option,
    ] = Path("data_all/data_all_dec.unity3d"),
) -> None:
    """
    Writes names list of all existed assets.
    """
    output = output_dir / "lst.txt"
    data_extractor = DataExtractor(data_all)
    data_extractor.list_asset_names(output)


@app.command()
@handle_errors
def download(
    server: Annotated[Server, typer.Argument(case_sensitive=False)],
    version: Annotated[str, typer.Argument()],
    decrypt_: Annotated[
        bool,
        typer.Option(
            "--decrypt",
            help="Decrypts the downloaded data.",
        ),
    ] = False,
    output_dir: Annotated[
        Path,
        output_dir_option,
    ] = Path("data_all"),
) -> None:
    """
    Downloads data_all.unity3d
    """
    data_downloader = DataDownloader(server, version)
    data_downloader.download_data_all(output_dir, progressbar=True)
    if decrypt_:
        output = output_dir / "data_all.unity3d"
        decrypt(
            input=output,
            output_dir=output_dir,
        )


@app.command()
@handle_errors
def resources(
    server: Annotated[Server, typer.Argument(case_sensitive=False)],
    version: Annotated[str, typer.Argument()],
    output_dir: Annotated[
        Path,
        output_dir_option,
    ] = Path("resources"),
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite",
            help="Overwrites existing files.",
        ),
    ] = False,
) -> None:
    """
    Downloads game resources (e.g. auido.pck, video.mp4)
    """
    data_downloader = DataDownloader(server, version)
    data_downloader.download_resources(
        output_dir, progressbar=True, overwrite=overwrite
    )


@app.command()
@handle_errors
def decrypt(
    input: Annotated[
        Path,
        typer.Argument(
            help="Path to the file that will be decrypted.",
        ),
    ] = Path("data_all/data_all.unity3d"),
    output_dir: Annotated[
        Path,
        output_dir_option,
    ] = Path("data_all"),
) -> None:
    """
    Decrypts data_all.unity3d.
    """
    DataCipher.decrypt_file(input, output_dir)


@app.command()
@handle_errors
def extract(
    asset_names: Annotated[
        list[str],
        typer.Argument(help="List of asset names that will be extraced."),
    ] = None,
    asset_file: Annotated[
        Path,
        typer.Option(
            "--asset-file",
            "-f",
            help="Path to the file with asset names. Overrides manual input.",
        ),
    ] = None,
    preset: Annotated[
        Preset,
        typer.Option(
            "--preset",
            "-p",
            help="Preset of assets to extract. Overrides manual and file input.",
        ),
    ] = None,
    output_dir: Annotated[
        Path,
        output_dir_option,
    ] = Path("extracted"),
    data_all: Annotated[
        Path,
        data_all_option,
    ] = Path("data_all/data_all_dec.unity3d"),
) -> None:
    """
    Extracts provided assets.
    """

    if preset:
        asset_names = PRESETS[preset]
    elif asset_file:
        with asset_file.open(encoding="utf-8") as file:
            asset_names = [line.strip() for line in file if line.strip()]
    elif not asset_names:
        typer.secho(
            "You must provide either a list of asset names, or use --asset-file[-f], or use --preset[-p].",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    data_extractor = DataExtractor(data_all)
    for asset_name in asset_names:
        data_extractor.extract_asset(asset_name, output_dir)


def main() -> None:
    app()
