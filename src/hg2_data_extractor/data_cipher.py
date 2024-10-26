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
    def decrypt_file(cls, input_file_path: str, output_file_path: str) -> None:
        with Path(input_file_path).open("rb") as input_file:
            input_file_encrypted = input_file.read()
            input_file_decrypted = cls.decrypt_bytes(input_file_encrypted)

        with Path(output_file_path).open("wb") as output_file:
            output_file.write(input_file_decrypted)

    @classmethod
    def decrypt_bytes(cls, data_encrypted: bytes) -> bytes:
        cipher = AES.new(cls._AES_KEY, AES.MODE_CBC, cls._AES_IV)
        data_decrypted = unpad(cipher.decrypt(data_encrypted), AES.block_size)

        return data_decrypted

    @classmethod
    def encrypt_file(cls, input_file_path: str, output_file_path: str) -> None:
        with Path(input_file_path).open("rb") as input_file:
            input_file_decrypted = input_file.read()
            input_file_encrypted = cls.encrypt_bytes(input_file_decrypted)

        with Path(output_file_path).open("wb") as output_file:
            output_file.write(input_file_encrypted)

    @classmethod
    def encrypt_bytes(cls, data_decrypted: bytes) -> bytes:
        cipher = AES.new(cls._AES_KEY, AES.MODE_CBC, cls._AES_IV)
        data_encrypted = cipher.encrypt(pad(data_decrypted, AES.block_size))

        return data_encrypted
