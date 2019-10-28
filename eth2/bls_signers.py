import abc
from keystores import ScryptKeystore
from utils.typing import (
    BLSPubkey,
    BLSPrivkey,
    BLSSignature,
    Domain,
)
from utils.bls import (
    bls_curve_order,
    bls_sign,
    bls_priv_to_pub,
)


class BLSSigner(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def sign(self, message_hash: bytes, domain: Domain) -> BLSSignature:
        pass

    @abc.abstractproperty
    def pubkey(self) -> BLSPubkey:
        pass


class PythonSigner(BLSSigner):
    def __init__(self, privkey: BLSPrivkey):
        assert privkey < bls_curve_order
        self.privkey = privkey

    def sign(self, message_hash: bytes, domain: Domain) -> BLSSignature:
        return bls_sign(message_hash, self.privkey, domain)

    @property
    def pubkey(self) -> BLSPubkey:
        return bls_priv_to_pub(self.privkey)

    def as_keystore(self, *, password: str) -> ScryptKeystore:
        secret = self.privkey.to_bytes(length=32, byteorder='big')
        return ScryptKeystore.encrypt(secret=secret, password=password)
