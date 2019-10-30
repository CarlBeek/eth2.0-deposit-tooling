from keystores import (
    Keystore,
    ScryptKeystore,
    Pbkdf2Keystore,
)

from json import loads

test_vector_password = 'testpassword'
test_vector_secret = bytes.fromhex('7a28b5ba57c53603b0b07b56bba752f7784bf506fa95edc395f5cf6c7514fe9d')
test_vector_keystores_json = [
    '''
    {
        "crypto": {
            "kdf": {
                "function": "pbkdf2",
                "params": {
                    "dklen": 32,
                    "c": 262144,
                    "prf": "hmac-sha256",
                    "salt": "ae3cd4e7013836a3df6bd7241b12db061dbe2c6785853cce422d148a624ce0bd"
                },
                "message": ""
            },
            "checksum": {
                "function": "SHA256",
                "params": {},
                "message": "6f53cc6a1be57c225d1234c4c99b32ad1925f4c40fdd7c8a265b8e4705e773d0"
            },
            "cipher": {
                "function": "aes-128-ctr",
                "params": {
                    "iv": "6087dab2f9fdbbfaddc31a909735c1e6"
                },
                "message": "5318b4d5bcd28de64ee5559e671353e16f075ecae9f99c7a79a38af5f869aa46"
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
                "message": "7afc1ac901ee46cb8d9a720fe2389dbc47edbe1534f6dacb5da80f2964b61a3f"
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


def test_encrypt_decrypt_test_vectors():
    for tv in test_vector_keystores:
        aes_iv = tv.crypto.cipher.params['iv']
        kdf_salt = tv.crypto.kdf.params['salt']
        keystore = Pbkdf2Keystore if 'pbkdf' in tv.crypto.kdf.function else ScryptKeystore
        generated_keystore = keystore.encrypt(
            secret=test_vector_secret,
            password=test_vector_password,
            aes_iv=aes_iv,
            kdf_salt=kdf_salt)
        assert generated_keystore.decrypt(test_vector_password) == test_vector_secret


def test_generated_keystores():
    for tv in test_vector_keystores:
        aes_iv = tv.crypto.cipher.params['iv']
        kdf_salt = tv.crypto.kdf.params['salt']
        keystore = Pbkdf2Keystore if 'pbkdf' in tv.crypto.kdf.function else ScryptKeystore
        generated_keystore = keystore.encrypt(
            secret=test_vector_secret,
            password=test_vector_password,
            aes_iv=aes_iv,
            kdf_salt=kdf_salt)
        assert generated_keystore.crypto == tv.crypto


def test_encrypt_decrypt_pbkdf2_random_iv():
    generated_keystore = Pbkdf2Keystore.encrypt(secret=test_vector_secret, password=test_vector_password)
    assert generated_keystore.decrypt(test_vector_password) == test_vector_secret


def test_encrypt_decrypt_scrypt_random_iv():
    generated_keystore = ScryptKeystore.encrypt(secret=test_vector_secret, password=test_vector_password)
    assert generated_keystore.decrypt(test_vector_password) == test_vector_secret
