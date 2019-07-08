from py_ecc.optimized_bls12_381.optimized_curve import curve_order
from py_ecc.bls.api import (
    privtopub,
    sign,
)
from secrets import randbelow
from typing import Tuple
from utils.types import (
    BLSPubkey,
    BLSPrivkey,
    BLSSignature,
    Bytes32,
    Domain,
)
from utils.hash import (
    int_to_int_hash,
    hash_func_bytes,
    num_bits_to_num_bytes,
)


def derive_privkey(parent_privkey: BLSPrivkey) -> BLSPrivkey:
    # TODO: Consider replacing with BIP32-style key derivation
    parent_privkey = parent_privkey
    num_bytes = num_bits_to_num_bytes(curve_order.bit_length())
    assert hash_func_bytes >= num_bytes  # Sanity check that the hash func generates sufficient entropy
    while True:
        key = int_to_int_hash(parent_privkey, num_bytes)
        if key > curve_order:
            parent_privkey = key
            continue
        return key


class BLSSigner:
    def __init__(self, privkey: BLSPrivkey):
        self.privkey = privkey
        self.pubkey = BLSPubkey(privtopub(self.privkey))

    def sign(self, message_hash: Bytes32, domain: Domain) -> BLSSignature:
        return sign(message_hash, self.privkey, domain)


class WithdrawalCredentials(BLSSigner):
    def __init__(self):
        privkey = randbelow(curve_order)
        super().__init__(privkey)


class SigningCredentials(BLSSigner):
    def __init__(self, withdrawal_credentials: WithdrawalCredentials):
        privkey = derive_privkey(withdrawal_credentials.privkey)
        super().__init__(privkey)


def generate_key_pairs() -> Tuple[WithdrawalCredentials, SigningCredentials]:
    withdrawal_creds = WithdrawalCredentials()
    signing_creds = SigningCredentials(withdrawal_creds)
    return withdrawal_creds, signing_creds
