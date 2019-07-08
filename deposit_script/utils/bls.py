from py_ecc.bls.api import (
    verify,
    sign,
)
from utils.types import (
    BLSPubkey,
    BLSSignature,
    Bytes32,
    Domain,
)


def bls_verify(pubkey: BLSPubkey, message_hash: Bytes32, signature: BLSSignature, domain: Domain) -> bool:
    return verify(message_hash=message_hash, pubkey=pubkey,
                  signature=signature, domain=int.from_bytes(domain, byteorder='little'))


def bls_sign(message_hash: Bytes32, privkey: int, domain: Domain) -> BLSSignature:
    return sign(message_hash=message_hash, privkey=privkey, domain=int.from_bytes(domain, byteorder='little'))
