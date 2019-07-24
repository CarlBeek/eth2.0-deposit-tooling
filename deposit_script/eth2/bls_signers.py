from py_ecc.optimized_bls12_381.optimized_curve import curve_order
from py_ecc.bls.api import (
    privtopub,
    sign,
)
from secrets import randbelow
import abc
from typing import Tuple
from keystores import ScryptKeystore
from utils.typing import (
    BLSPubkey,
    BLSPrivkey,
    BLSSignature,
    Bytes32,
    Domain,
)
from utils.crypto import (
    int_to_int_hash,
    hash_func_bytes,
    num_bits_to_num_bytes,
)
from utils.constants import ENDIANNESS


class BLSSigner(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def sign(self, message_hash: Bytes32, domain: Domain) -> BLSSignature:
        pass

    @abc.abstractproperty
    def pubkey(self) -> BLSPubkey:
        pass


def derive_privkey(parent_privkey: BLSPrivkey) -> BLSPrivkey:
    # TODO: Consider replacing with BIP44-style key derivation
    parent_privkey = parent_privkey
    num_bytes = num_bits_to_num_bytes(curve_order.bit_length())
    assert hash_func_bytes >= num_bytes  # Sanity check that the hash func generates sufficient entropy
    while True:
        key = BLSPrivkey(int_to_int_hash(int(parent_privkey)))
        if key > BLSPrivkey(curve_order):
            parent_privkey = key
            continue
        return key


class PythonSigner(BLSSigner):
    privkey = BLSPrivkey(1)  # Placeholder (overwritten by child classes)

    def sign(self, message_hash: Bytes32, domain: Domain) -> BLSSignature:
        return BLSSignature(sign(message_hash, self.privkey, int.from_bytes(domain, ENDIANNESS)))

    @property
    def pubkey(self) -> BLSPubkey:
        return BLSPubkey(privtopub(self.privkey))

    def as_keystore(self, *, password: str) -> ScryptKeystore:
        secret = self.privkey.to_bytes(length=32, byteorder='big')
        return ScryptKeystore(secret=secret, password=password)


class WithdrawalCredentials(PythonSigner):
    def __init__(self):
        self.privkey = randbelow(curve_order)


class SigningCredentials(PythonSigner):
    def __init__(self, withdrawal_credentials: WithdrawalCredentials):
        self.privkey = derive_privkey(withdrawal_credentials.privkey)


def generate_key_pairs() -> Tuple[WithdrawalCredentials, SigningCredentials]:
    withdrawal_credentials = WithdrawalCredentials()
    signing_credentials = SigningCredentials(withdrawal_credentials)
    return withdrawal_credentials, signing_credentials
