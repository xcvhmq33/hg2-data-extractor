from pathlib import Path


def ask_overwrite_if_exists(file_path: str | Path) -> bool:
    file_path = to_path(file_path)
    if file_path.is_file():
        message = f"{file_path} is already exists, overwrite it? (y/n): "
        overwrite = input(message).lower() == "y"
    else:
        overwrite = True

    return overwrite


def to_path(path: str | Path) -> Path:
    if isinstance(path, Path):
        return path

    return Path(path)
