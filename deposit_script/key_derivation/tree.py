from utils.crypto import hkdf
from utils.bls import (
    bls_curve_order,
)


def bytes_to_privkey(ikm: bytes) -> int:
    okm = hkdf(master=ikm, salt="BLS-SIG-KEYGEN-SALT-", key_len=48)
    return int.from_bytes(okm, byteorder='big') % bls_curve_order


def derive_master_privkey(seed: bytes) -> int:
    return bytes_to_privkey(seed)


def derive_child_privkey(parent_privkey: int, i: int) -> int:
    parent_hash = bytes_to_privkey(parent_privkey.to_bytes(length=32, byteorder='big'))
    parent_double_hash = bytes_to_privkey(parent_hash.to_bytes(length=32, byteorder='big'))
    mod_sum = (parent_hash + parent_double_hash + (i * parent_double_hash)) % bls_curve_order
    return mod_sum if i < 2**31 else bytes_to_privkey(mod_sum.to_bytes(length=32, byteorder='big'))
