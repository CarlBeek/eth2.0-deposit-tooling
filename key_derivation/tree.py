from utils.crypto import (
    HKDF,
    SHA256,
)
from utils.bls import bls_curve_order
from typing import List


def flip_bits(input: int) -> int:
    return input ^ (2**256 - 1)


def IKM_to_lamport_SK(*, IKM: bytes, salt: bytes) -> List[bytes]:
    OKM = HKDF(salt=salt, IKM=IKM, L=8160)
    lamport_SK = [OKM[i: i + 32] for i in range(0, 8160, 32)]
    return lamport_SK


def parent_SK_to_lamport_PK(*, parent_SK: int, index: int) -> bytes:
    salt = index.to_bytes(8, byteorder='big')
    IKM = parent_SK.to_bytes(32, byteorder='big')
    lamport_0 = IKM_to_lamport_SK(IKM=IKM, salt=salt)
    not_IKM = flip_bits(parent_SK).to_bytes(32, byteorder='big')
    lamport_1 = IKM_to_lamport_SK(IKM=not_IKM, salt=salt)
    lamport_SKs = lamport_0 + lamport_1
    lamport_PKs = [SHA256(sk) for sk in lamport_SKs]
    compressed_PK = SHA256(b''.join(lamport_PKs))
    return compressed_PK


def HKDF_mod_r(*, IKM: bytes) -> int:
    okm = HKDF(salt=b'BLS-SIG-KEYGEN-SALT-', IKM=IKM, L=48)
    return int.from_bytes(okm, byteorder='big') % bls_curve_order


def derive_child_SK(*, parent_SK: int, index: int) -> int:
    lamport_PK = parent_SK_to_lamport_PK(parent_SK=parent_SK, index=index)
    return HKDF_mod_r(IKM=lamport_PK)


def derive_master_SK(seed: bytes) -> int:
    return HKDF_mod_r(IKM=seed)
