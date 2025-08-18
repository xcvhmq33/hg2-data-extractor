import re
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict


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


class Version:
    pattern = re.compile(
        r"""
        ^                   # begin
        [1-9]\d*            # first part of the version
        [.|_]               # separator
        \d+                 # second part of the version
        $                   # end
        """,
        re.VERBOSE,
    )

    def __init__(self, value: str):
        if not re.match(self.pattern, value):
            msg = f"Invalid version format: {value}. Expected x_y or x.y"
            raise ValueError(msg)
        self.str = value.replace(".", "_")
        self.float = float(value.replace("_", "."))

    def __str__(self):  # type: ignore
        return self.str

    def __repr__(self):  # type: ignore
        return f"Version({self.str})"
