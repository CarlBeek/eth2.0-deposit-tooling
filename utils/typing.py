from typing import NewType

# ####  Eth2.0 Types  ####
BLSPubkey = NewType('BLSPubkey', bytes)
BLSPrivkey = NewType('BLSPrivkey', int)
BLSSignature = NewType('BLSSignature', bytes)
Bytes32 = NewType('Bytes32', bytes)
Domain = NewType('Domain', bytes)
DomainType = NewType('DomainType', bytes)
Gwei = NewType('Gwei', int)
Nonce = NewType('Nonce', int)
Root = NewType('Root', bytes)
Version = NewType('Version', bytes)
Wei = NewType('Wei', int)
