from dataclasses import dataclass
from secrets import randbits
from typing import Optional
from utils.typing import (
    AESIV,
    KeystorePassward,
    KeystoreSalt,
)
from utils.crypto import (
    keccak,
    scrypt,
    AES,
)


@dataclass
class KeyStoreCrypto:
    cipher: str
    cipherparams: dict
    ciphertext: bytes
    kdf: str
    kdfparams: dict
    mac: bytes


@dataclass
class KeyStore:
    crypto: KeyStoreCrypto
    id: str
    version: int


class ScryptKeyStore(KeyStore):
    crypto = KeyStoreCrypto(
        cipher='aes-128-ctr',
        cipherparams=dict(),
        ciphertext=bytes(),
        kdf='scrypt',
        kdfparams={
            'dklen': 32,
            'n': 2**18,
            'r': 1,
            'p': 8,
        },
        mac=bytes()
    )
    id = ''  # TODO: Figure out how ids are generated (random?)
    version = 3

    def __init__(self, secret: bytes, password: KeystorePassward,
                 salt: Optional[KeystoreSalt]=None, iv: Optional[AESIV]=None):
        self.crypto.kdfparams['salt'] = salt if salt is not None else KeystoreSalt(hex(randbits(256))[2:])
        self.crypto.cipherparams['iv'] = iv if iv is not None else AESIV(hex(randbits(2**128))[2:])
        decryption_key = scrypt(password=password, **self.crypto.kdfparams)
        self.crypto.ciphertext = AES(key=decryption_key[:16], secret=secret, iv=self.crypto.cipherparams['iv'])
        self.crypto.mac = keccak(decryption_key[16:32] + self.crypto.ciphertext)
