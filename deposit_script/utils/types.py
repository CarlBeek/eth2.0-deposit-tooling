from typing import NewType
from py_ecc.bls.api import privtopub
from dataclasses import dataclass


BLSPubkey = NewType('BLSPubkey', bytes)
BLSSignature = NewType("BLSSignature", bytes)
Domain = NewType("Domain", bytes)
DomainType = NewType("DomainType", bytes)
Hash32 = NewType("Hash32", bytes)
Version = NewType("Version", bytes)


@dataclass
class KeyPair:
    privkey: int

    def __post_init__(self):
        self.pubkey = BLSPubkey(privtopub(self.privkey))
