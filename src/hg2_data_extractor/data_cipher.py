from collections.abc import Callable
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class DataCipher:
    def __init__(self, aes_key: bytes, aes_iv: bytes):
        self._AES_KEY = aes_key
        self._AES_IV = aes_iv
        self.cipher = AES.new(self._AES_KEY, AES.MODE_CBC, self._AES_IV)

    def decrypt_file(self, input: Path, output_dir: Path | None = None) -> None:
        self._crypt_file(input, output_dir, "_dec", self.decrypt_bytes)

    def encrypt_file(self, input: Path, output_dir: Path | None = None) -> None:
        self._crypt_file(input, output_dir, "_enc", self.encrypt_bytes)

    def decrypt_bytes(self, input: bytes) -> bytes:
        return unpad(self.cipher.decrypt(input), AES.block_size)  # type: ignore

    def encrypt_bytes(self, input: bytes) -> bytes:
        return self.cipher.encrypt(pad(input, AES.block_size))  # type: ignore

    def _crypt_file(
        self,
        input: Path,
        output_dir: Path | None,
        suffix: str,
        cryptographer: Callable[[bytes], bytes],
    ) -> None:
        if output_dir is None:
            output_dir = input.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / f"{input.stem}{suffix}{input.suffix}"

        with input.open("rb") as file:
            data_in = file.read()
            data_out = cryptographer(data_in)

        with output.open("wb") as file:
            file.write(data_out)
