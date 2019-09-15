import rlp
from utils.typing import (
    ECDSASignature,
    SignedTransaction,
    UnsignedTransaction,
)


# Tx with known encoding https://etherscan.io/tx/0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060:

tx_sans_signature = {'nonce': 0, 'gas_price': 50000000000000, 'gas_limit': 21000,
                     'to': bytearray.fromhex('5df9b87991262f6ba471f09758cde1c0fc1de734'), 'value': 31337, 'data': b''}
tx_signature = {'v': 0x1c, 'r': 0x88ff6cf0fefd94db46111149ae4bfc179e9b94721fffd821d38d16464b3f71d0,
                's': 0x45e0aff800961cfce805daef7016b9b675c137a6a41a548f7b60a3484c06a33a}
tx_with_signature = {**tx_sans_signature, **tx_signature}

tx_encoding = bytearray.fromhex('f86780862d79883d2000825208945df9b87991262f6ba471f09758cde1c0fc1de734827a69801ca088ff6cf0fefd94db46111149ae4bfc179e9b94721fffd821d38d16464b3f71d0a045e0aff800961cfce805daef7016b9b675c137a6a41a548f7b60a3484c06a33a')  # noqa: E501


def test_signed_transaction_encoding():
    tx = SignedTransaction(**tx_with_signature)
    assert rlp.encode(tx) == tx_encoding


def test_unsigned_to_signed_tx():
    signature = ECDSASignature(tx_signature)
    unsigned_tx = UnsignedTransaction(**tx_sans_signature)
    signed_tx = unsigned_tx.as_signed_transaction(signature)
    assert rlp.encode(signed_tx) == tx_encoding
