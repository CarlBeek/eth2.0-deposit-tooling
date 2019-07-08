from utils.types import (
    BLSPubkey,
    BLSSignature,
    Bytes32,
    DepositData,
    Domain,
    DomainType,
    Gwei,
    KeyPair,
    Version,
)
from utils.constants import DOMAIN_DEPOSIT
from utils.hash import hash
from utils.bls import bls_sign


def get_domain(domain_type: DomainType=DomainType(DOMAIN_DEPOSIT), fork_version: Version=Version(bytes(4))) -> Domain:
    """
    Return the domain for a given fork
    """
    assert len(domain_type) == 4
    assert len(fork_version) == 4
    return Domain(domain_type + fork_version)


def calculate_deposit_data(signing_pubkey: BLSPubkey, withdrawal_key: BLSPubkey, amount: Gwei) -> BLSSignature:
    return DepositData(
        pubkey=signing_pubkey,
        withdrawal_credentials=hash(withdrawal_key),
        amount=amount,
    )


def get_signed_deposit(withdrawal_kp: KeyPair, signing_kp: KeyPair,
                       deposit_amount: Gwei, fork_version: Version=Version(bytes(4))):
    deposit = calculate_deposit_data(signing_kp.pubkey, withdrawal_kp.pubkey, deposit_amount)
    signature = bls_sign(deposit.hash_tree_root)
    deposit.signature = signature
    return deposit
