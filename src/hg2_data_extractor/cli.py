import functools
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Any

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
OutputDirOption = Annotated[
    Path,
    output_dir_option,
]
DataAllOption = Annotated[
    Path,
    data_all_option,
]
ServerArgument = Annotated[Server, typer.Argument(case_sensitive=False)]
VersionArgument = Annotated[str, typer.Argument()]


def handle_errors(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    @functools.wraps(func)
    def wrapper(*args: tuple[Any], **kwargs: dict[Any, Any]) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            typer.secho(e, fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)

    return wrapper


@app.command()  # type: ignore
@handle_errors
def lst(
    output_dir: OutputDirOption = Path("extracted"),
    data_all: DataAllOption = Path("data_all/data_all_dec.unity3d"),
) -> None:
    """
    Writes names list of all existed assets.
    """
    output = output_dir / "lst.txt"
    data_extractor = DataExtractor(data_all)
    data_extractor.list_asset_names(output)


@app.command()  # type: ignore
@handle_errors
def download(
    server: ServerArgument,
    version: VersionArgument,
    decrypt_: Annotated[
        bool,
        typer.Option(
            "--decrypt",
            help="Decrypts the downloaded data.",
        ),
    ] = False,
    output_dir: OutputDirOption = Path("data_all"),
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


@app.command()  # type: ignore
@handle_errors
def resources(
    server: ServerArgument,
    version: VersionArgument,
    output_dir: OutputDirOption = Path("resources"),
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


@app.command()  # type: ignore
@handle_errors
def decrypt(
    input: Annotated[
        Path,
        typer.Argument(
            help="Path to the file that will be decrypted.",
        ),
    ] = Path("data_all/data_all.unity3d"),
    output_dir: OutputDirOption = Path("data_all"),
) -> None:
    """
    Decrypts data_all.unity3d.
    """
    DataCipher.decrypt_file(input, output_dir)


@app.command()  # type: ignore
@handle_errors
def extract(
    asset_names: Annotated[
        list[str] | None,
        typer.Argument(help="List of asset names that will be extraced."),
    ] = None,
    asset_file: Annotated[
        Path | None,
        typer.Option(
            "--asset-file",
            "-f",
            help="Path to the file with asset names. Overrides manual input.",
        ),
    ] = None,
    preset: Annotated[
        Preset | None,
        typer.Option(
            "--preset",
            "-p",
            help="Preset of assets to extract. Overrides manual and file input.",
        ),
    ] = None,
    output_dir: OutputDirOption = Path("extracted"),
    data_all: DataAllOption = Path("data_all/data_all_dec.unity3d"),
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
            "You must provide either a list of asset names, "
            "or use --asset-file[-f], or use --preset[-p].",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    data_extractor = DataExtractor(data_all)
    for asset_name in asset_names:
        data_extractor.extract_asset(asset_name, output_dir)


def main() -> None:
    app()
