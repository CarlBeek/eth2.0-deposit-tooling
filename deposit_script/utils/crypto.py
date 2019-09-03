from Crypto.Hash import SHA256 as _sha256
from Crypto.Protocol.KDF import (
    scrypt as _scrypt,
    HKDF as _HKDF,
)


def sha256(x):
    return _sha256.new(x).digest()


def scrypt(*, password: str, salt: str, n: int, r: int, p: int, dklen: int) -> bytes:
    res = _scrypt(password=password, salt=salt, key_len=dklen, N=n, r=r, p=p)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def hkdf(*, ikm: bytes, key_len: int, salt: str) -> bytes:
    res = _HKDF(master=ikm, key_len=key_len, salt=salt, hashmod=_sha256)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]
