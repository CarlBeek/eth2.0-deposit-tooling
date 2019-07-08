from py_ecc.bls.api import (
    verify,
    sign,
)
from utils.types import (
    BLSPubkey,
    BLSSignature,
    Bytes32,
    Domain,
    DomainType,
    Version,
)
from utils.constants import (
    ENDIANNESS,
    DOMAIN_DEPOSIT,
)


def get_domain(domain_type: DomainType=DomainType(DOMAIN_DEPOSIT), fork_version: Version=Version(bytes(4))) -> Domain:
    """
    Return the domain for a given fork
    """
    assert len(domain_type) == 4
    assert len(fork_version) == 4
    return Domain(domain_type + fork_version)


def bls_verify(pubkey: BLSPubkey, message_hash: Bytes32, signature: BLSSignature, domain: Domain) -> bool:
    return verify(message_hash=message_hash, pubkey=pubkey,
                  signature=signature, domain=int.from_bytes(domain, byteorder=ENDIANNESS))


def bls_sign(message_hash: Bytes32, privkey: int, domain: Domain) -> BLSSignature:
    return sign(message_hash=message_hash, privkey=privkey, domain=int.from_bytes(domain, byteorder=ENDIANNESS))
