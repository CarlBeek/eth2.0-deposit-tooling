from utils.constants import (
    ZERO_BYTES32,
    ENDIANNESS,
    DOMAIN_DEPOSIT,
)
from utils.merkle_minimal import get_merkle_root
from utils.bls import get_domain
from utils.typing import (
    BLSPubkey,
    BLSSignature,
    Bytes32,
    DomainType,
    Gwei,
    Version,
)
from eth2.bls_signers.abstract_signer import BLSSigner
from typing import List
from dataclasses import dataclass


def pack_bytes(b: bytes, num_bytes: int) -> List[bytes]:
    assert len(b) <= num_bytes
    if len(b) <= 32:
        return [Bytes32(b + ZERO_BYTES32[32 - len(b):])]
    return [b[:32]] + pack_bytes(b, num_bytes - 32)


@dataclass
class DepositData:
    pubkey: BLSPubkey
    withdrawal_credentials: Bytes32
    amount: Gwei
    signature: BLSSignature = BLSSignature(b'\x00' * 96)

    @property
    def hash_tree_root(self) -> Bytes32:
        chunks = [
            *pack_bytes(self.pubkey, 48),
            *pack_bytes(self.withdrawal_credentials, 32),
            self.amount.to_bytes(32, byteorder=ENDIANNESS),
        ]
        return get_merkle_root(chunks)

    def sign(self, signer: BLSSigner,
             domain_type: DomainType=DomainType(DOMAIN_DEPOSIT), fork_version: Version=Version(bytes(4))):
        self.signature = signer.sign(message_hash=self.hash_tree_root, domain=get_domain(domain_type, fork_version))
