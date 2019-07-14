from hashlib import sha256
from Crypto.Hash import keccak as _keccak
from Crypto.Cipher import AES as _AES
from Crypto.Util import Counter
from Crypto.Protocol.KDF import scrypt as _scrypt
from utils.constants import ENDIANNESS
from utils.typing import (
    AESIV,
    KeystorePassward,
    KeystoreSalt,
)

_hash_func = sha256  # Declared once to ensure future uses use correct version


def hash(x):
    return _hash_func(x).digest()


def keccak(x):
    return _keccak.new(digest_bits=256).update(x).digest()


def int_to_int_hash(x: int, num_bytes: int) -> int:
    hashed_int = hash(x.to_bytes(num_bytes, byteorder=ENDIANNESS))
    return int.from_bytes(hashed_int, byteorder=ENDIANNESS)


def num_bits_to_num_bytes(x: int) -> int:
    return -(-x // 8)


hash_func_bytes = _hash_func().digest_size


def scrypt(*, password: KeystorePassward, salt: KeystoreSalt, n: int, r: int, p: int, dklen: int) -> bytes:
    return _scrypt(password=password.encode('utf-8'), salt=salt, key_len=dklen, N=n, r=r, p=p)


def AES(*, key: bytes, secret, iv: AESIV) -> bytes:
    counter = Counter.new(128, initial_value=int(iv, 16))
    aes = _AES.new(key=key, mode=_AES.MODE_CTR, counter=counter)
    return aes.encrypt(secret)
