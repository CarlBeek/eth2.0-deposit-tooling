from utils.types import (
    Domain,
    DomainType,
    KeyPair,
    Version,
)
from utils.constants import DOMAIN_DEPOSIT


def get_domain(domain_type: DomainType=DOMAIN_DEPOSIT, fork_version: Version=Version(bytes(4))) -> Domain:
    """
    Return the domain for a given fork
    """
    assert len(domain_type) == 4
    assert len(fork_version) == 4
    return Domain(domain_type + fork_version)


def generate_deposit_signatures(signing_kp: KeyPair, fork_version: Version=Version(bytes(4))):
    pass
