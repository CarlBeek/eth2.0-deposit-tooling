from py_ecc.optimized_bls12_381.optimized_curve import curve_order as _curve_order
from py_ecc.bls.api import (
    privtopub as _priv_to_pub,
    verify as _verify,
    sign as _sign,
)
from utils.typing import (
    BLSPubkey,
    BLSPrivkey,
    BLSSignature,
    Domain,
    DomainType,
    Version,
)
from utils.constants import (
    DOMAIN_DEPOSIT,
)


def get_domain(domain_type: DomainType=DomainType(DOMAIN_DEPOSIT), fork_version: Version=Version(bytes(4))) -> Domain:
    """
    Return the domain for a given fork
    """
    assert len(domain_type) == 4
    assert len(fork_version) == 4
    return Domain(domain_type + fork_version)


def bls_verify(pubkey: BLSPubkey, message_hash: bytes, signature: BLSSignature, domain: Domain) -> bool:
    return _verify(message_hash=message_hash, pubkey=pubkey,
                   signature=signature, domain=domain)


def bls_sign(message_hash: bytes, privkey: int, domain: Domain) -> BLSSignature:
    return BLSSignature(_sign(message_hash=message_hash, privkey=privkey, domain=domain))


def bls_priv_to_pub(privkey: BLSPrivkey) -> BLSPubkey:
    return BLSPubkey(_priv_to_pub(privkey))


bls_curve_order = _curve_order
