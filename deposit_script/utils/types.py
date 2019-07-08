from .constants import (
    ZERO_BYTES32,
    ENDIANNESS,
)
from .merkle_minimal import get_merkle_root
from typing import (
    NewType,
    List,
)
from py_ecc.bls.api import privtopub
from dataclasses import dataclass


BLSPubkey = NewType('BLSPubkey', bytes)
BLSSignature = NewType("BLSSignature", bytes)
Bytes32 = NewType("Bytes32", bytes)
Domain = NewType("Domain", bytes)
DomainType = NewType("DomainType", bytes)
Gwei = NewType("Gwei", int)
Version = NewType("Version", bytes)


def pack_bytes(b: bytes, num_bytes: int) -> List[bytes]:
    assert len(b) <= num_bytes
    if len(b) <= 32:
        return [Bytes32(b + ZERO_BYTES32[32 - len(b):])]
    return [b[:32]] + pack_bytes(b, num_bytes - 32)


@dataclass
class KeyPair:
    privkey: int

    def __post_init__(self):
        self.pubkey = BLSPubkey(privtopub(self.privkey))


@dataclass
class DepositData:
    pubkey: BLSPubkey
    withdrawal_credentials: Bytes32
    amount: Gwei
    signature: BLSSignature = BLSSignature(b'\x00' * 96)

    @property
    def hash_tree_root(self):
        chunks = [
            *pack_bytes(self.pubkey, 48),
            *pack_bytes(self.withdrawal_credentials, 32),
            self.amount.to_bytes(32, byteorder=ENDIANNESS),
        ]
        return get_merkle_root(chunks)
