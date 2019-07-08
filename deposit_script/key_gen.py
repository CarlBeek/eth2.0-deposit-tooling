from py_ecc.optimized_bls12_381.optimized_curve import curve_order
from secrets import randbelow
from typing import Tuple
from utils.hash import (
    int_to_int_hash,
    num_bits_to_num_bytes,
    hash_func_bytes,
)
from utils.types import KeyPair


def generate_withdrawal_keys() -> KeyPair:
    return KeyPair(privkey=randbelow(curve_order))


def derive_signing_keys(withdrawal_keys: KeyPair) -> KeyPair:
    # TODO: Consider replacing with BIP32-style key derivation
    withdrawal_key = withdrawal_keys.privkey
    num_bytes = num_bits_to_num_bytes(curve_order.bit_length())
    assert hash_func_bytes >= num_bytes  # Sanity check that the hash func generates sufficient entropy
    while True:
        key = int_to_int_hash(withdrawal_key, num_bytes)
        if key > curve_order:
            withdrawal_key = key
            continue
        return KeyPair(key)


def generate_key_pairs() -> Tuple[KeyPair, KeyPair]:
    withdrawal_keys = generate_withdrawal_keys()
    signing_keys = derive_signing_keys(withdrawal_keys)
    return withdrawal_keys, signing_keys
