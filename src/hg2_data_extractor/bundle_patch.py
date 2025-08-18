from collections.abc import Generator
from contextlib import contextmanager, suppress

import lz4.block
import UnityPy
from UnityPy import Environment
from UnityPy.enums import CompressionFlags
from UnityPy.helpers import CompressionHelper

from hg2_data_extractor import DataCipher


def patched_lz4hc(data: bytes, uncompressed_size: int) -> bytes:
    with suppress(ValueError):
        data_cipher = DataCipher(b"LPC@a*&^b19b61l/", b"\x00" * 16)
        data = data_cipher.decrypt_bytes(data)
    return lz4.block.decompress(data, uncompressed_size=uncompressed_size)  # type: ignore


@contextmanager
def patch_lz4hc() -> Generator[None]:
    try:
        old = CompressionHelper.DECOMPRESSION_MAP[CompressionFlags.LZ4HC]
        CompressionHelper.DECOMPRESSION_MAP[CompressionFlags.LZ4HC] = patched_lz4hc
        yield
    finally:
        CompressionHelper.DECOMPRESSION_MAP[CompressionFlags.LZ4HC] = old


def hg2_load(file: str | bytes, *, version: float) -> Environment:
    if version >= 11.7:
        with patch_lz4hc():
            return UnityPy.load(file)
    return UnityPy.load(file)
