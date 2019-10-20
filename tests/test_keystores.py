from keystores import (
    Keystore,
    ScryptXorKeystore,
)
from utils.crypto import scrypt

from json import loads

test_vector_password = 'testpassword'
test_vector_secret = bytes.fromhex('1b4b68192611faea208fca21627be9dae6c3f2564d42588fb1119dae7c9f4b87')
test_vector_decryption_key = bytes.fromhex('fac192ceb5fd772906bea3e118a69e8bbb5cc24229e20d8766fd298291bba6bd')
test_vector_keystore_json = '''
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
            "function": "SHA256",
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
test_vector_keystore = Keystore.from_json(test_vector_keystore_json)


def generate_keystore(use_test_vector_params: bool=True) -> ScryptXorKeystore:
    if not use_test_vector_params:
        return ScryptXorKeystore.encrypt(
            secret=test_vector_secret,
            password=test_vector_password,
        )
    return ScryptXorKeystore.encrypt(
        secret=test_vector_secret,
        password=test_vector_password,
        kdf_salt=test_vector_keystore.crypto.kdf.params['salt'],
        cipher_msg=test_vector_keystore.crypto.cipher.message,
    )


def test_json_serialization():
    assert loads(test_vector_keystore.as_json()) == loads(test_vector_keystore_json)


def test_SHA256_checksum():
    generated_keystore = generate_keystore()
    assert test_vector_keystore.crypto.checksum.message == generated_keystore.crypto.checksum.message


def test_decryption_key():
    decryption_key = scrypt(password=test_vector_password, **test_vector_keystore.crypto.kdf.params)
    assert decryption_key == test_vector_decryption_key


def test_cipher():
    generated_keystore = generate_keystore()
    decryption_key = scrypt(password=test_vector_password, **test_vector_keystore.crypto.kdf.params)
    assert test_vector_secret == bytes(a ^ b for a, b in zip(decryption_key, generated_keystore.crypto.cipher.message))


def test_encrypt_decrypt():
    generated_keystore = generate_keystore(use_test_vector_params=False)
    assert generated_keystore.decrypt(test_vector_password) == test_vector_secret
