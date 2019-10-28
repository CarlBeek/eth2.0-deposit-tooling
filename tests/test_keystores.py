from keystores import (
    Keystore,
    ScryptKeystore,
    Pbkdf2Keystore,
)
from utils.crypto import scrypt

from json import loads

test_vector_password = 'testpassword'
test_vector_secret = bytes.fromhex('7a28b5ba57c53603b0b07b56bba752f7784bf506fa95edc395f5cf6c7514fe9d')
test_vector_keystores_json = ['''
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
            "function": "aes-128-ctr",
            "params": {
                "iv": "83dbcc02d8ccb40e466191a123791e0e"
            },
            "message": "d172bf743a674da9cdad04534d56926ef8358534d458fffccd4e6ad2fbde479c"
        }
    },
    "id": "3198bc9c-6672-5ab3-d995-4942343ae5b6",
    "version": 0
}''',
'''
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
            "function": "aes-128-ctr",
            "params": {
                "iv": "83dbcc02d8ccb40e466191a123791e0e"
            },
            "message": "d172bf743a674da9cdad04534d56926ef8358534d458fffccd4e6ad2fbde479c"
        }
    },
    "id": "3198bc9c-6672-5ab3-d995-4942343ae5b6",
    "version": 0
}''']
test_vector_keystores = [Keystore.from_json(x) for x in test_vector_keystores_json]

def test_json_serialization():
    for keystore, keystore_json in zip(test_vector_keystores, test_vector_keystores_json):
        assert loads(keystore.as_json()) == loads(keystore_json)

def test_encrypt_decrypt_scrypt_keystore():
    generated_keystore = ScryptKeystore.encrypt(secret=test_vector_secret, password=test_vector_password)
    assert generated_keystore.decrypt(test_vector_password) == test_vector_secret

def test_encrypt_decrypt_pbkdf2_keystore():
    generated_keystore = Pbkdf2Keystore.encrypt(secret=test_vector_secret, password=test_vector_password)
    assert generated_keystore.decrypt(test_vector_password) == test_vector_secret
