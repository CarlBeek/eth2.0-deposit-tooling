from py_ecc.optimized_bls12_381.optimized_curve import curve_order
from utils.crypto import int_to_int_hash


def int_to_bls_privkey(key: int) -> int:
    while key >= curve_order:
        key = int_to_int_hash(key)
    return key
