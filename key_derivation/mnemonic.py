from unicodedata import normalize
from typing import Optional
from secrets import randbits
from utils.crypto import (
    pbkdf2,
    sha256,
)


english_word_list = open('key_derivation/english.txt').readlines()


def get_word(index: int) -> str:
    assert index < 2048
    return english_word_list[index][:-1]


def get_seed(*, mnemonic: str, password: str='') -> bytes:
    mnemonic = normalize('NFKD', mnemonic)
    password = normalize('NFKD', 'mnemonic' + password)
    return pbkdf2(password=mnemonic, salt=password, dklen=64, count=2048)


def get_mnemonic(entropy: Optional[bytes]=None) -> str:
    if entropy is None:
        entropy = randbits(256).to_bytes(32, 'big')
    entropy_length = len(entropy) * 8
    assert entropy_length in range(128, 257, 32)
    checksum_length = (entropy_length // 32)
    checksum = int.from_bytes(sha256(entropy), 'big') >> 256 - checksum_length
    entropy_bits = int.from_bytes(entropy, 'big') << checksum_length
    entropy_bits += checksum
    entropy_length += checksum_length
    mnemonic = []
    for i in range(entropy_length // 11 - 1, -1, -1):
        index = (entropy_bits >> i * 11) & 2**11 - 1
        mnemonic.append(get_word(index))
    return ' '.join(mnemonic)
