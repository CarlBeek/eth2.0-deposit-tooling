from utils.crypto import int_to_int_hash
from utils.typing import BLSPrivkey
from utils.bls import bls_curve_order


def int_to_bls_privkey(key: int) -> BLSPrivkey:
    while key >= bls_curve_order:
        key = int_to_int_hash(key)
    return BLSPrivkey(key)
