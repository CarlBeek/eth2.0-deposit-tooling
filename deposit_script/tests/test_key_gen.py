from py_ecc.optimized_bls12_381.optimized_curve import curve_order
from py_ecc.bls.api import privtopub

from utils import KeyPair
from key_gen import (
    generate_withdrawal_keys,
    derive_signing_keys,
)


def valid_key_pair(kp: KeyPair) -> bool:
    return (
        kp.privkey < curve_order
        and kp.pubkey == privtopub(kp.privkey)
    )


def test_withdrawal_keys():
    key_pair = generate_withdrawal_keys()
    assert valid_key_pair(key_pair)


def test_signing_keys():
    withdrawal_keys = generate_withdrawal_keys()
    key_pair = derive_signing_keys(withdrawal_keys)
    assert valid_key_pair(key_pair)
