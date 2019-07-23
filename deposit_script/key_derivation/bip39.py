from unicodedata import normalize
from typing import Optional
from secrets import randbits
from key_derivation.word_lists import get_word
from utils.crypto import (
    PBKDF2,
    sha256,
)


def get_seed(*, mnemonic: str, password: Optional[str]='') -> bytes:
    mnemonic = normalize('NFKD', mnemonic)
    password = normalize('NFKD', 'mnemonic' + password)
    return PBKDF2(password=mnemonic.encode('UTF-8'), salt=password.encode('UTF-8'))


def get_mnemonic(entropy: Optional[bytes]) -> str:
    entropy = randbits(256).to_bytes(32, 'big')
    entropy += sha256(entropy)[0]
    entropy_bits = int.from_bytes(entropy, byteorder='big')
    mnemonic = []
    while entropy_bits.bitlength() > 0:
        index = entropy_bits & 2**11
        mnemonic.append(get_word(index))
        entropy_bits >>= 11
    return ' '.join(mnemonic)
