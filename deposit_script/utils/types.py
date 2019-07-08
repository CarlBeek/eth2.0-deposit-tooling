from typing import NewType

BLSPubkey = NewType('BLSPubkey', bytes)
BLSPrivkey = NewType('BLSPrivkey', int)
BLSSignature = NewType('BLSSignature', bytes)
Bytes32 = NewType('Bytes32', bytes)
Domain = NewType('Domain', bytes)
DomainType = NewType('DomainType', bytes)
Gwei = NewType('Gwei', int)
Version = NewType('Version', bytes)
