from typing import (
    NewType,
    Dict,
    Union,
)
import rlp
from rlp.sedes import (
    big_endian_int,
    binary,
)

# ####  Eth2.0 Types  ####
BLSPubkey = NewType('BLSPubkey', bytes)
BLSPrivkey = NewType('BLSPrivkey', int)
BLSSignature = NewType('BLSSignature', bytes)
Bytes32 = NewType('Bytes32', bytes)
Domain = NewType('Domain', bytes)
DomainType = NewType('DomainType', bytes)
Gwei = NewType('Gwei', int)
Nonce = NewType('Nonce', int)
Version = NewType('Version', bytes)
Wei = NewType('Wei', int)


# ####  Eth1.X Types  ####
Address = NewType('Address', str)
ECDSASignature = NewType('ECDSASignature', Dict[str, int])  # {'v':0, 'r':1, 's':2}
TxData = NewType('TxData', bytes)

# ####  Keystore Types  ####
AESIV = NewType('AESIV', str)
KeystorePassword = NewType('KeystorePassword', str)
KeystoreSalt = NewType('KeystoreSalt', str)

# ####  RLP Serializable Objects  ####
address = binary.fixed_length(20)


class SignedTransaction(rlp.Serializable):
    fields = (
        ('nonce', big_endian_int),
        ('gas_price', big_endian_int),
        ('gas_limit', big_endian_int),
        ('to', address),
        ('value', big_endian_int),
        ('data', binary),
        ('v', big_endian_int),
        ('r', big_endian_int),
        ('s', big_endian_int),
    )


class UnsignedTransaction(rlp.Serializable):
    fields = (
        ('nonce', big_endian_int),
        ('gas_price', big_endian_int),
        ('gas_limit', big_endian_int),
        ('to', address),
        ('value', big_endian_int),
        ('data', binary),
    )

    def as_signed_transaction(self, signature: ECDSASignature) -> SignedTransaction:
        return SignedTransaction(**self.as_dict(), **signature)


Transaction = Union[SignedTransaction, UnsignedTransaction]
