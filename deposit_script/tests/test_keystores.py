from keystores import (
    Keystore,
    ScryptXorKeystore,
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
            "message": "cb27fe860c96f269f7838525ba8dce0886e0b7753caccc14162195bcdacbf49e"
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
test_keystore = Keystore.from_json(test_keystore_json)


def generate_keystore() -> ScryptXorKeystore:
    return ScryptXorKeystore.encrypt(
        secret=test_secret,
        password=test_password,
        kdf_salt=test_keystore.crypto.kdf.params['salt'],
        cipher_msg=test_keystore.crypto.cipher.message,
    )


def test_json_serialization():
    assert loads(test_keystore.as_json()) == loads(test_keystore_json)


def test_sha256_checksum():
    generated_keystore = generate_keystore()
    assert test_keystore.crypto.checksum.message == generated_keystore.crypto.checksum.message
