from key_derivation.tree import (
    flip_bits,
    IKM_to_lamport_SK,
    HKDF_mod_r,
    derive_master_SK,
)
from json import load

with open('tests/test_key_derivation/key_derivation_test_vectors.json', 'r') as f:
    test_vector = load(f)


def test_flip_bits():
    test_vector_int = int(test_vector['seed'][:64], 16)  # 64 comes from string chars containing .5 bytes
    assert test_vector_int & flip_bits(test_vector_int) == 0


def test_IKM_to_lamport_SK():
    test_vector_lamport_0 = [bytes.fromhex(x) for x in test_vector['lamport_privkeys'][:255]]
    test_vector_lamport_1 = [bytes.fromhex(x) for x in test_vector['lamport_privkeys'][255:]]
    test_seed = int(test_vector['seed'][:64], 16)  # 64 comes from string chars containing .5 bytes
    lamport_0 = IKM_to_lamport_SK(IKM=test_seed, index=0)
    lamport_1 = IKM_to_lamport_SK(IKM=flip_bits(test_seed), index=0)
    assert test_vector_lamport_0 == lamport_0
    assert test_vector_lamport_1 == lamport_1


def test_HKDF_mod_r():
    test_hkdf_ikm = bytes.fromhex(test_vector['compressed_lamport_pubkey'])
    test_result = test_vector['bls_privkey']
    assert HKDF_mod_r(IKM=test_hkdf_ikm) == test_result


def test_derive_master_SK():
    # Note: this implicitly tests parent_privkey_to_lamport_root and derive_child_privkey
    test_seed = bytes.fromhex(test_vector['seed'])
    test_bls_privkey = test_vector['bls_privkey']
    assert derive_master_SK(test_seed) == test_bls_privkey
