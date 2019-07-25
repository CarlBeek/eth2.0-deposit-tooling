from utils.crypto import hmac_sha512
from utils.typing import (
    BLSPubkey,
    BLSPrivkey,
)
from typing import Tuple
from utils.bls import (
    bls_curve_order,
    bls_priv_to_pub,
)


def point(p: int) -> BLSPubkey:
    return bls_priv_to_pub(BLSPrivkey(p))


def ser_256(p: int) -> bytes:
    return p.to_bytes(32, byteorder='big')


def ser_32(i: int) -> bytes:
    return i.to_bytes(4, byteorder='big')


def de_ser_int(b: bytes) -> int:
    return int.from_bytes(b, 'big')


def ser_p(p: BLSPubkey) -> bytes:
    x, y = p
    flags = b'\x02' if y % 2 == 0 else b'\x03'
    return flags + ser_256(x)


def bytes_xor(a: bytes, b: bytes) -> bytes:
    length = max(len(a), len(b))
    int_a = int.from_bytes(a, 'big')
    int_b = int.from_bytes(b, 'big')
    int_ab = int_a ^ int_b
    return int_ab.to_bytes(length, 'big')


def get_valid_I(*, chain_code: bytes, data: bytes) -> bytes:
    # Performs rejection sampling until the returned point is below the curve order
    while True:
        I = hmac_sha512(key=chain_code, msg=data)  # noqa: E741
        I_left = I[:32]
        trial_k = de_ser_int(I_left) >> 1
        if trial_k < bls_curve_order:
            return I
        data = bytes_xor(data, I_left)


def derive_child_privkey(k_par: int, c_par: bytes, i: int) -> Tuple[int, bytes]:
    data = b'\x00' + ser_256(k_par) + ser_32(i) if i >= 2**31 else ser_p(point(k_par)) + ser_32(i)
    I = get_valid_I(chain_code=c_par, data=data)  # noqa: E741
    I_left = I[:32]
    I_right = I[32:]
    k_i = (de_ser_int(I_left) >> 1 + k_par) % bls_curve_order
    c_i = I_right
    assert k_i != 0
    return k_i, c_i


def derive_master_privkey(seed: bytes) -> Tuple[int, bytes]:
    I = get_valid_I(chain_code=str.encode('Seed'), data=seed)  # noqa: E741
    I_left = I[:32]
    I_right = I[32:]
    k_i = (de_ser_int(I_left) >> 1) % bls_curve_order
    c_i = I_right
    assert k_i != 0
    return k_i, c_i
