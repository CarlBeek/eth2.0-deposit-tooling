from keystores import (
    Keystore,
)

from json import loads

#  Test vector from Eth Wiki: https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition#scrypt
test_password = 'testpassword'
test_secret = bytes.fromhex('1b4b68192611faea208fca21627be9dae6c3f2564d42588fb1119dae7c9f4b87')
test_keystore_json = '''
{
    "crypto": {
        "kdf": {
            "function": "scrypt",
            "params": {
                "dklen": 32,
                "n": 262144,
                "p": 8,
                "r": 1,
                "salt": "ab0c7876052600dd703518d6fc3fe8984592145b591fc8fb5c6d43190334ba19"
            },
            "message": ""
        },
        "checksum": {
            "function": "sha256",
            "params": {},
            "message": "e1c5e3d08f8aec999df5287dd9f2b0aafdaa86d263ca6287e2bd1c6b20c19c0f"
        },
        "cipher": {
            "function": "xor",
            "params": {},
            "message": "e18afad793ec8dc3263169c07add77515d9f301464a05508d7ecb42ced24ed3a"
        }
    },
    "id": "e5e79c63-b6bc-49f2-a4f8-f0dcea550ff6",
    "version": 4
}'''


def get_keystore_test_vector() -> Keystore:
    return Keystore.from_json(test_keystore_json)


def test_json_serialization():
    keystore = get_keystore_test_vector()
    assert loads(keystore.as_json()) == loads(test_keystore_json)


def test_sha256_checksum():
    keystore = get_keystore_test_vector()
    assert keystore.crypto.checksum.message == Keystore.from_json(test_keystore_json).crypto.checksum.message
