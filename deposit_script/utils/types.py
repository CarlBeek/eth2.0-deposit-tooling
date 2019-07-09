from typing import NewType

####  Eth2.0 Types  ####
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


####  Eth1.X Types  ####
TxData = NewType('TxData', bytes)
Address = NewType('Address', str)
SerializedTransaction = NewType('SerializedTransaction', bytes)
Transaction = NewType('Transaction', dict)