from utils.crypto import hmac_sha512
from typing import Tuple
from py_ecc.secp256k1 import (
    privtopub,
    N,
)


def point(p: int) -> Tuple[int, int]:
    return privtopub(p.to_bytes(32, byteorder='big'))


def ser_256(p: int) -> bytes:
    return p.to_bytes(32, byteorder='big')


def ser_32(i: int) -> bytes:
    return i.to_bytes(4, byteorder='big')


def ser_p(p: Tuple[int, int]) -> bytes:
    x, y = p
    flags = b'\x02' if y % 2 == 0 else b'\x03'
    return flags + ser_256(x)


def derive_child_privkey(k_par: int, c_par: bytes, i: int) -> Tuple[int, bytes]:
    data = b'\x00' + ser_256(k_par) + ser_32(i) if i >= 2**31 else ser_p(point(k_par)) + ser_32(i)
    I = hmac_sha512(key=c_par, msg=data)  # noqa: E741
    I_left = I[:32]
    I_right = I[32:]
    k_i = (int.from_bytes(I_left, 'big') + k_par) % N
    c_i = I_right
    assert int.from_bytes(I_left, 'big') < N
    assert k_i != 0
    return k_i, c_i
