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
from utils.constants import ENDIANNESS
from bls_signers.abstract_signer import BLSSigner


def derive_privkey(parent_privkey: BLSPrivkey) -> BLSPrivkey:
    # TODO: Consider replacing with BIP32-style key derivation
    parent_privkey = parent_privkey
    num_bytes = num_bits_to_num_bytes(curve_order.bit_length())
    assert hash_func_bytes >= num_bytes  # Sanity check that the hash func generates sufficient entropy
    while True:
        key = BLSPrivkey(int_to_int_hash(int(parent_privkey), num_bytes))
        if key > BLSPrivkey(curve_order):
            parent_privkey = key
            continue
        return key


class PythonSigner(BLSSigner):
    privkey = BLSPrivkey(1)

    def sign(self, message_hash: Bytes32, domain: Domain) -> BLSSignature:
        return sign(message_hash, self.privkey, int.from_bytes(domain, ENDIANNESS))

    @property
    def pubkey(self) -> BLSPubkey:
        return privtopub(self.privkey)


class WithdrawalCredentials(PythonSigner):
    def __init__(self):
        self.privkey = randbelow(curve_order)


class SigningCredentials(PythonSigner):
    def __init__(self, withdrawal_credentials: WithdrawalCredentials):
        self.privkey = derive_privkey(withdrawal_credentials.privkey)


def generate_key_pairs() -> Tuple[WithdrawalCredentials, SigningCredentials]:
    withdrawal_creds = WithdrawalCredentials()
    signing_creds = SigningCredentials(withdrawal_creds)
    return withdrawal_creds, signing_creds