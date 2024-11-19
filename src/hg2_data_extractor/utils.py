from pathlib import Path


def to_path(path: str | Path) -> Path:
    if isinstance(path, Path):
        return path

    return Path(path)
