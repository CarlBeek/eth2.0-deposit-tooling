from keystores import (
    KeyStore,
    KeyStoreCrypto,
    ScryptKeyStore,
)

#  Test vector from Eth Wiki: https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition#scrypt
test_password = 'testpassword'
test_secret = bytes.fromhex("7a28b5ba57c53603b0b07b56bba752f7784bf506fa95edc395f5cf6c7514fe9d")
crypt = KeyStoreCrypto(
    cipher="aes-128-ctr",
    cipherparams={"iv": int("83dbcc02d8ccb40e466191a123791e0e", 16)},
    ciphertext=bytes.fromhex("d172bf743a674da9cdad04534d56926ef8358534d458fffccd4e6ad2fbde479c"),
    kdf="scrypt",
    kdfparams={
        "dklen": 32,
        "n": 262144,
        "r": 1,
        "p": 8,
        "salt": bytes.fromhex("ab0c7876052600dd703518d6fc3fe8984592145b591fc8fb5c6d43190334ba19"),
    },
    mac=bytes.fromhex("2103ac29920d71da29f15d75b4a16dbe95cfd7ff8faea1056c33131d846e3097")
)
test_scrypt_keystore = KeyStore(
    crypto=crypt,
    id="3198bc9c-6672-5ab3-d995-4942343ae5b6",
    version=3,
)


def test_mac():
    iv = test_scrypt_keystore.crypto.cipherparams['iv']
    salt = test_scrypt_keystore.crypto.kdfparams['salt']
    keystore = ScryptKeyStore(test_secret, test_password, salt=salt, iv=iv)
    assert keystore.crypto == test_scrypt_keystore.crypto
