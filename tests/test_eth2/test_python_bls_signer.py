from py_ecc.bls.api import privtopub
from eth2.bls_signers import (
    PythonSigner,
)
from utils.bls import (
    bls_verify,
    bls_curve_order,
    get_domain,
)


def verify_credentials(credentials: PythonSigner):
    assert credentials.privkey < bls_curve_order
    assert credentials.pubkey == privtopub(credentials.privkey)
    msg = b'\x11' * 32
    domain = get_domain()
    signature = credentials.sign(msg, domain)
    assert bls_verify(pubkey=credentials.pubkey, message_hash=msg, signature=signature, domain=domain)


def test_withdrawal_keys():
    credentials = PythonSigner(privkey=1234567890)
    verify_credentials(credentials)
