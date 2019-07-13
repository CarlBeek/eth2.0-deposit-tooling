from Crypto.Cipher import AES
from Crypto.Util import Counter
from dataclasses import dataclass
from secrets import randbits
from typing import Optional
from utils.typing import (
    AESIV,
    KeystorePassward,
    KeystoreSalt,
)
from utils.hash import (
    keccak,
    scrypt,
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
        self.crypto.kdfparams['salt'] = salt if salt is not None else hex(randbits(256))[:2]
        self.crypto.cipherparams['iv'] = iv if iv is not None else hex(randbits(2**128))[:2]
        decryption_key = scrypt(password=password, **self.crypto.kdfparams)
        counter = Counter.new(128, initial_value=int(self.crypto.cipherparams['iv']))
        self.crypto.ciphertext = AES.new(decryption_key, AES.MODE_CTR, counter=counter).encrypt(secret)
        self.crypto.mac = keccak(decryption_key + self.crypto.ciphertext).hex()
