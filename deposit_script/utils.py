from py_ecc.bls.api import privtopub
from dataclasses import dataclass
from hashlib import sha256

ENDIANNESS = 'little'
_hash_func = sha256


def hash(x):
    return _hash_func(x).digest()


def int_to_int_hash(x: int, num_bytes: int) -> int:
    hashed_int = hash(x.to_bytes(num_bytes, byteorder=ENDIANNESS))
    return int.from_bytes(hashed_int, byteorder=ENDIANNESS)


def num_bits_to_num_bytes(x: int) -> int:
    return -(-x//8)


hash_func_bytes = _hash_func().digest_size


@dataclass
class KeyPair:
    privkey: int

    def __post_init__(self):
        self.pubkey = privtopub(self.privkey)
