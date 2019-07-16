from dataclasses import (
    dataclass,
    asdict,
    fields,
)
import json
from secrets import randbits
from typing import Optional
from utils.typing import (
    AESIV,
    KeystorePassword,
    KeystoreSalt,
)
from utils.crypto import (
    keccak,
    scrypt,
    AES,
)

hexdigits = set('0123456789abcdef')


def to_bytes(obj):
    if isinstance(obj, str):
        if all(c in hexdigits for c in obj):
            return bytes.fromhex(obj)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'iv':
                continue
            obj[key] = to_bytes(value)
    return obj


class BytesDataclass:
    def __post_init__(self):
        for field in fields(self):
            if field.type in (dict, bytes):
                self.__setattr__(field.name, to_bytes(self.__getattribute__(field.name)))


@dataclass
class KeystoreCrypto(BytesDataclass):
    cipher: str
    cipherparams: dict
    ciphertext: bytes
    kdf: str
    kdfparams: dict
    mac: bytes


@dataclass
class Keystore(BytesDataclass):
    crypto: KeystoreCrypto
    id: str
    version: int

    def as_json(self) -> str:
        return json.dumps(asdict(self), default=lambda x: x.hex())

    @classmethod
    def from_json(cls, json_str: str):
        json_dict = json.loads(json_str)
        crypto = KeystoreCrypto(**json_dict['crypto'])
        id = json_dict['id']
        version = json_dict['version']
        return cls(crypto=crypto, id=id, version=version)


class ScryptKeystore(Keystore):
    crypto = KeystoreCrypto(
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

    def __init__(self, *, secret: bytes, password: KeystorePassword,
                 salt: Optional[KeystoreSalt]=None, iv: Optional[AESIV]=None):
        self.crypto.kdfparams['salt'] = salt if KeystoreSalt(hex(randbits(256))[2:]) is None else to_bytes(salt)
        self.crypto.cipherparams['iv'] = iv if AESIV(hex(randbits(128))[2:]) is None else iv
        decryption_key = scrypt(password=password, **self.crypto.kdfparams)
        self.crypto.ciphertext = AES(key=decryption_key[:16], secret=secret, iv=self.crypto.cipherparams['iv'])
        self.crypto.mac = keccak(decryption_key[16:32] + self.crypto.ciphertext)
