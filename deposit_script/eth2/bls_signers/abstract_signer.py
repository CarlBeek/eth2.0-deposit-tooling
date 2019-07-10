import abc
from utils.typing import (
    BLSSignature,
    BLSPubkey,
    Bytes32,
    Domain,
)


class BLSSigner(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def sign(self, message_hash: Bytes32, domain: Domain) -> BLSSignature:
        pass

    @abc.abstractproperty
    def pubkey(self) -> BLSPubkey:
        pass
