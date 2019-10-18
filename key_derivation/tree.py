from utils.crypto import (
    hkdf,
    sha256,
)
from utils.bls import bls_curve_order
from typing import List


def flip_bits(input: int) -> int:
    return input ^ (2**256 - 1)


def IKM_to_lamport_SK(*, IKM: bytes, index: int) -> List[bytes]:
    OKM = hkdf(master=IKM,
               salt=index.to_bytes(32, byteorder='big'), key_len=8160)
    lamport_SK = [OKM[i: i + 32] for i in range(0, 8160, 32)]
    return lamport_SK


def parent_SK_to_lamport_PK(*, parent_SK: int, index: int) -> bytes:
    IKM = parent_SK.to_bytes(32, byteorder='big')
    lamport_0 = IKM_to_lamport_SK(IKM=IKM, index=index)
    not_IKM = flip_bits(parent_SK).to_bytes(32, byteorder='big')
    lamport_1 = IKM_to_lamport_SK(IKM=not_IKM, index=index)
    lamport_SKs = lamport_0 + lamport_1
    lamport_PKs = [sha256(sk) for sk in lamport_SKs]
    compressed_PK = sha256(b''.join(lamport_PKs))
    return compressed_PK


def HKDF_mod_r(*, IKM: bytes) -> int:
    okm = hkdf(master=IKM, salt=b'BLS-SIG-KEYGEN-SALT-', key_len=48)
    return int.from_bytes(okm, byteorder='big') % bls_curve_order


def derive_child_SK(*, parent_SK: int, index: int) -> int:
    lamport_PK = parent_SK_to_lamport_PK(parent_SK=parent_SK, index=index)
    return HKDF_mod_r(IKM=lamport_PK)


def derive_master_SK(seed: bytes) -> int:
    intermediate_SK = HKDF_mod_r(IKM=seed)
    SK = derive_child_SK(parent_SK=intermediate_SK, index=0)
    return SK
