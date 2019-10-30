from dataclasses import (
    dataclass,
    asdict,
    fields,
    field as dataclass_field
)
import json
from secrets import randbits
from uuid import uuid4 as uuid
from typing import Optional
from utils.crypto import (
    AES_128_CTR,
    PBKDF2,
    scrypt,
    SHA256,
)

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

    def as_json(self) -> str:
        return json.dumps(asdict(self), default=lambda x: x.hex())


@dataclass
class KeystoreModule(BytesDataclass):
    function: str = ''
    params: dict = dataclass_field(default_factory=dict)
    message: bytes = bytes()


@dataclass
class KeystoreCrypto(BytesDataclass):
    kdf: KeystoreModule = KeystoreModule()
    checksum: KeystoreModule = KeystoreModule()
    cipher: KeystoreModule = KeystoreModule()

    @classmethod
    def from_json(cls, json_dict: dict):
        kdf = KeystoreModule(**json_dict['kdf'])
        checksum = KeystoreModule(**json_dict['checksum'])
        cipher = KeystoreModule(**json_dict['cipher'])
        return cls(kdf=kdf, checksum=checksum, cipher=cipher)


@dataclass
class Keystore(BytesDataclass):
    crypto: KeystoreCrypto = KeystoreCrypto()
    id: str = str(uuid())  # Generate a new uuid
    version: int = 0

    @classmethod
    def from_json(cls, json_str: str):
        json_dict = json.loads(json_str)
        crypto = KeystoreCrypto.from_json(json_dict['crypto'])
        id = json_dict['id']
        version = json_dict['version']
        return cls(crypto=crypto, id=id, version=version)


@dataclass
class Pbkdf2Keystore(Keystore):
    crypto: KeystoreCrypto = KeystoreCrypto(
        kdf=KeystoreModule(
            function='pbkdf2',
            params={
                'c': 2**18,
                'dklen': 32,
                "prf": 'hmac-sha256'
            },
        ),
        checksum=KeystoreModule(
            function='SHA256',
        ),
        cipher=KeystoreModule(
            function='aes-128-ctr',
        )
    )

    @classmethod
    def encrypt(cls, *, secret: bytes, password: str, kdf_salt: Optional[bytes]=None, aes_iv: Optional[bytes]=None):
        keystore = cls()
        keystore.crypto.kdf.params['salt'] = randbits(256).to_bytes(32, 'big') if kdf_salt is None else kdf_salt
        decryption_key = PBKDF2(password=password, **keystore.crypto.kdf.params)
        keystore.crypto.cipher.params['iv'] = randbits(128).to_bytes(16, 'big') if aes_iv is None else aes_iv
        cipher = AES_128_CTR(key=decryption_key[:16], **keystore.crypto.cipher.params)
        keystore.crypto.cipher.message = cipher.encrypt(secret)
        keystore.crypto.checksum.message = SHA256(decryption_key[16:32] + keystore.crypto.cipher.message)
        return keystore

    def decrypt(self, password: str) -> bytes:
        decryption_key = PBKDF2(password=password, **self.crypto.kdf.params)
        assert SHA256(decryption_key[16:32] + self.crypto.cipher.message) == self.crypto.checksum.message
        cipher = AES_128_CTR(key=decryption_key[:16], **self.crypto.cipher.params)
        return cipher.decrypt(self.crypto.cipher.message)


@dataclass
class ScryptKeystore(Keystore):
    crypto: KeystoreCrypto = KeystoreCrypto(
        kdf=KeystoreModule(
            function='scrypt',
            params={
                'dklen': 32,
                'n': 2**18,
                'r': 1,
                'p': 8,
            },
        ),
        checksum=KeystoreModule(
            function='SHA256',
        ),
        cipher=KeystoreModule(
            function='aes-128-ctr',
        )
    )

    @classmethod
    def encrypt(cls, *, secret: bytes, password: str, kdf_salt: Optional[bytes]=None, aes_iv: Optional[bytes]=None):
        keystore = cls()
        keystore.crypto.kdf.params['salt'] = randbits(256).to_bytes(32, 'big') if kdf_salt is None else kdf_salt
        decryption_key = scrypt(password=password, **keystore.crypto.kdf.params)
        keystore.crypto.cipher.params['iv'] = randbits(128).to_bytes(16, 'big') if aes_iv is None else aes_iv
        cipher = AES_128_CTR(key=decryption_key[:16], **keystore.crypto.cipher.params)
        keystore.crypto.cipher.message = cipher.encrypt(secret)
        keystore.crypto.checksum.message = SHA256(decryption_key[16:32] + keystore.crypto.cipher.message)
        return keystore

    def decrypt(self, password: str) -> bytes:
        decryption_key = scrypt(password=password, **self.crypto.kdf.params)
        assert SHA256(decryption_key[16:32] + self.crypto.cipher.message) == self.crypto.checksum.message
        cipher = AES_128_CTR(key=decryption_key[:16], **self.crypto.cipher.params)
        return cipher.decrypt(self.crypto.cipher.message)
