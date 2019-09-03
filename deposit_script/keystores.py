from dataclasses import (
    dataclass,
    asdict,
    fields,
)
import json
from secrets import randbits
from utils.crypto import (
    scrypt,
    sha256,
)
from uuid import uuid4 as uuid

hexdigits = set('0123456789abcdef')


def to_bytes(obj):
    if isinstance(obj, str):
        if all(c in hexdigits for c in obj):
            return bytes.fromhex(obj)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = to_bytes(value)
    return obj


class BytesDataclass:
    def __post_init__(self):
        for field in fields(self):
            if field.type in (dict, bytes):
                self.__setattr__(field.name, to_bytes(self.__getattribute__(field.name)))


@dataclass
class KeystoreCrypto(BytesDataclass):
    ciphertext: bytes
    mac: bytes
    scryptparams: dict


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
        ciphertext=bytes(),
        mac=bytes(),
        scryptparams={
            'dklen': 32,
            'n': 2**18,
            'r': 1,
            'p': 8,
        },
    )
    id = ''
    version = 4

    def __init__(self, *, secret: bytes, password: str):
        self.id = str(uuid())  # Generate a new uuid
        self.crypto.scryptparams['salt'] = randbits(256).to_bytes(32, 'big')
        cipher_salt = randbits(256).to_bytes(32, 'big')
        decryption_key = scrypt(password=password, **self.crypto.scryptparams)
        self.crypto.mac = sha256(decryption_key)
        self.crypto.ciphertext = bytes(a ^ b for a, b in zip(decryption_key, cipher_salt))
