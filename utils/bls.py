from py_ecc.bls import G2ProofOfPossession as _bls
from ssz import (
    ByteVector,
    Serializable,
)

from utils.typing import (
    BLSPubkey,
    BLSPrivkey,
    BLSSignature,
    Domain,
    DomainType,
    Version,
    Root,
)
from utils.constants import (
    DOMAIN_DEPOSIT,
    GENESIS_FORK_VERSION,
)


class SigningRoot(Serializable):
    fields = [
        ('object_root', ByteVector(32)),
        ('domain', ByteVector(8))
    ]


def compute_domain(domain_type: DomainType=DomainType(DOMAIN_DEPOSIT), fork_version: Version=GENESIS_FORK_VERSION) -> Domain:
    """
    Return the domain for the ``domain_type`` and ``fork_version``.
    """
    return Domain(domain_type + fork_version)


def compute_signing_root(ssz_object, domain: Domain) -> Root:
    """
    Return the signing root of an object by calculating the root of the object-domain tree.
    """
    domain_wrapped_object = SigningRoot.create(
        object_root=ssz_object.get_hash_tree_root(),
        domain=domain,
    )
    return domain_wrapped_object.get_hash_tree_root()


bls_verify = _bls.Verify
bls_sign = _bls.Sign
bls_priv_to_pub = _bls.PrivToPub
