from hashlib import sha256
from utils.constants import ENDIANNESS

_hash_func = sha256  # Declared once to ensure future uses use correct version


def hash(x):
    return _hash_func(x).digest()


def int_to_int_hash(x: int, num_bytes: int) -> int:
    hashed_int = hash(x.to_bytes(num_bytes, byteorder=ENDIANNESS))
    return int.from_bytes(hashed_int, byteorder=ENDIANNESS)


def num_bits_to_num_bytes(x: int) -> int:
    return -(-x // 8)


hash_func_bytes = _hash_func().digest_size
