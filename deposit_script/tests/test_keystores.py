from keystores import (
    KeyStore,
    ScryptKeyStore,
)

from json import loads

#  Test vector from Eth Wiki: https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition#scrypt
test_password = 'testpassword'
test_secret = bytes.fromhex("7a28b5ba57c53603b0b07b56bba752f7784bf506fa95edc395f5cf6c7514fe9d")
test_keystore_json = '''
{
    "crypto" : {
        "cipher" : "aes-128-ctr",
        "cipherparams" : {
            "iv" : "83dbcc02d8ccb40e466191a123791e0e"
        },
        "ciphertext" : "d172bf743a674da9cdad04534d56926ef8358534d458fffccd4e6ad2fbde479c",
        "kdf" : "scrypt",
        "kdfparams" : {
            "dklen" : 32,
            "n" : 262144,
            "r" : 1,
            "p" : 8,
            "salt" : "ab0c7876052600dd703518d6fc3fe8984592145b591fc8fb5c6d43190334ba19"
        },
        "mac" : "2103ac29920d71da29f15d75b4a16dbe95cfd7ff8faea1056c33131d846e3097"
    },
    "id" : "3198bc9c-6672-5ab3-d995-4942343ae5b6",
    "version" : 3
}'''


def test_json_serialization():
    keystore = KeyStore.from_json(test_keystore_json)
    assert loads(keystore.as_json()) == loads(test_keystore_json)


def test_mac():
    iv = loads(test_keystore_json)['crypto']['cipherparams']['iv']
    salt = loads(test_keystore_json)['crypto']['kdfparams']['salt']
    keystore = ScryptKeyStore(secret=test_secret, password=test_password, salt=salt, iv=iv)
    print(keystore.crypto)
    print(KeyStore.from_json(test_keystore_json).crypto)
    assert keystore.crypto == KeyStore.from_json(test_keystore_json).crypto
