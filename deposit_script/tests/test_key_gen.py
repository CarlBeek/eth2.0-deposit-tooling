from py_ecc.optimized_bls12_381.optimized_curve import curve_order
from py_ecc.bls.api import privtopub

from key_gen import generate_withdrawal_keys


def test_withdrawal_keys():
    key_pair = generate_withdrawal_keys()
    assert key_pair.privkey < curve_order
    assert key_pair.pubkey == privtopub(key_pair.privkey)
