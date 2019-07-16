from py_ecc.optimized_bls12_381.optimized_curve import curve_order
from py_ecc.bls.api import privtopub
from eth2.bls_signers import (
    WithdrawalCredentials,
    SigningCredentials,
    derive_privkey,
)


def valid_key_credentials(credentials) -> bool:
    return (
        credentials.privkey < curve_order
        and credentials.pubkey == privtopub(credentials.privkey)
    )


def test_withdrawal_keys():
    credentials = WithdrawalCredentials()
    assert valid_key_credentials(credentials)


def test_signing_keys():
    withdrawal_credentials = WithdrawalCredentials()
    signing_credentials = SigningCredentials(withdrawal_credentials)
    assert derive_privkey(withdrawal_credentials.privkey) == signing_credentials.privkey
    assert valid_key_credentials(signing_credentials)
