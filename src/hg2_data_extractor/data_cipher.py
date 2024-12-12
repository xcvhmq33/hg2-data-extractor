from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class DataCipher:
    _AES_KEY = bytes.fromhex(
        "89 83 83 10 3a 0f d9 52 ea 9f 3c 14 50 9c 56 "
        "92 a4 6e ab bf 46 1a 54 ac b2 7e 82 a7 99 6d 35 b8"
    )
    _AES_IV = bytes.fromhex("81 e0 ca d4 a5 df 51 da 37 ba 49 ee cc 8a 4f fe")

    @classmethod
    def decrypt_file(cls, input: Path, output_dir: Path | None = None) -> None:
        if output_dir is None:
            output_dir = input.parent
        output = output_dir / f"{input.stem}_dec{input.suffix}"

        with input.open("rb") as file:
            input_encrypted = file.read()
            input_decrypted = cls.decrypt_bytes(input_encrypted)

        with output.open("wb") as file:
            file.write(input_decrypted)

    @classmethod
    def decrypt_bytes(cls, input: bytes) -> bytes:
        cipher = AES.new(cls._AES_KEY, AES.MODE_CBC, cls._AES_IV)
        decrypted = unpad(cipher.decrypt(input), AES.block_size)

        return decrypted  # type: ignore

    @classmethod
    def encrypt_file(cls, input: Path, output_dir: Path | None = None) -> None:
        if output_dir is None:
            output_dir = input.parent
        output = output_dir / f"{input.stem}_enc{input.suffix}"

        with input.open("rb") as file:
            input_decrypted = file.read()
            input_encrypted = cls.encrypt_bytes(input_decrypted)

        with output.open("wb") as file:
            file.write(input_encrypted)

    @classmethod
    def encrypt_bytes(cls, input: bytes) -> bytes:
        cipher = AES.new(cls._AES_KEY, AES.MODE_CBC, cls._AES_IV)
        encrypted = cipher.encrypt(pad(input, AES.block_size))

        return encrypted  # type: ignore
