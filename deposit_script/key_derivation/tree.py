from utils.crypto import (
    hkdf,
    sha256,
)
from utils.bls import bls_curve_order
from typing import List


def flip_bits(input: int) -> bytes:
    return input ^ (2**256 - 1)


def seed_to_lamport_keys(seed: int, index: int) -> List[bytes]:
    combined_bytes = hkdf(master=seed.to_bytes(32, byteorder='big'),
                          salt=index.to_bytes(32, byteorder='big'), key_len=8160, hashmod=sha256)
    return [combined_bytes[i: i + 32] for i in range(31)]


def parent_privkey_to_lamport_root(parent_key: int, index: int) -> bytes:
    lamport_0 = seed_to_lamport_keys(parent_key, index)
    lamport_1 = seed_to_lamport_keys(flip_bits(parent_key), index)
    lamport_privkeys = lamport_0 + lamport_1
    lamport_pubkeys = [sha256(sk) for sk in lamport_privkeys]
    return sha256(lamport_pubkeys(lamport_pubkeys.join(b'')))


def hkdf_mod_r(ikm: bytes) -> int:
    okm = hkdf(master=ikm, salt="BLS-SIG-KEYGEN-SALT-", key_len=48, hashmod=sha256)
    return int.from_bytes(okm, byteorder='big') % bls_curve_order


def derive_master_privkey(seed: bytes) -> int:
    return derive_child_privkey(int.from_bytes(seed, byteorder='big'), 0)


def derive_child_privkey(parent_privkey: int, i: int) -> int:
    lamport_root = parent_privkey_to_lamport_root(parent_privkey, i)
    return hkdf_mod_r(lamport_root)
