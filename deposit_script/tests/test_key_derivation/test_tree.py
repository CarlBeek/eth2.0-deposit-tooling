from key_derivation.tree import (
    flip_bits,
    seed_to_lamport_keys,
    parent_privkey_to_lamport_root,
    hkdf_mod_r,
    derive_child_privkey,
    derive_master_privkey,
)
from json import load

with open('tests/test_key_derivation/key_derivation_test_vectors.json', 'r') as f:
    test_vector = load(f)


def test_flip_bits():
    test_vector_int = int(test_vector['seed'][:64], 16)  # 64 comes from string chars containing .5 bytes
    assert test_vector_int & flip_bits(test_vector_int) == 0


def test_seed_to_lamport_keys():
    test_vector_lamport_0 = [bytes.fromhex(x) for x in test_vector['lamport_privkeys'][:255]]
    test_vector_lamport_1 = [bytes.fromhex(x) for x in test_vector['lamport_privkeys'][255:]]
    test_seed = int(test_vector['seed'][:64], 16)  # 64 comes from string chars containing .5 bytes
    lamport_0 = seed_to_lamport_keys(test_seed, 0)
    lamport_1 = seed_to_lamport_keys(flip_bits(test_seed), 0)
    assert test_vector_lamport_0 == lamport_0
    assert test_vector_lamport_1 == lamport_1


def test_hkdf_mod_r():
    test_hkdf_ikm = bytes.fromhex(test_vector['compressed_lamport_pubkey'])
    test_result = test_vector['bls_privkey']
    assert hkdf_mod_r(test_hkdf_ikm) == test_result
