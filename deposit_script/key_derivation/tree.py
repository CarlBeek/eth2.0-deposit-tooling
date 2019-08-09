from utils.crypto import sha256
from utils.bls import (
    bls_curve_order,
)


def int_to_int_hash(x: int) -> int:
    while True:
        hashed_int = sha256(x.to_bytes(32, byteorder='big'))
        x = int.from_bytes(hashed_int, byteorder='big')
        if x < bls_curve_order and x != 0:
            return x


def derive_child_privkey(k_par: int, i: int) -> int:
    i_hash = int_to_int_hash(i)
    k_hash = int_to_int_hash(k_par)
    mod_sum = (i_hash + k_hash) % bls_curve_order
    return mod_sum if i < 2**31 else int_to_int_hash(mod_sum)


def derive_master_privkey(seed: bytes) -> int:
    assert len(seed) == 32
    int_seed = int.from_bytes(seed, byteorder='big')
    return int_to_int_hash(int_seed)
