from unicodedata import normalize
from typing import Optional
from secrets import randbits
from utils.crypto import (
    scrypt,
    sha256,
)


english_word_list = open('key_derivation/english.txt').readlines()


def get_word(index: int) -> str:
    assert index < 2048
    return english_word_list[index][:-1]


def get_seed(*, mnemonic: str, password: str='') -> bytes:
    mnemonic = normalize('NFKD', mnemonic)
    password = normalize('NFKD', 'mnemonic' + password)
    return scrypt(password=mnemonic, salt=password, n=2**18, r=1, p=8, dklen=32)


def get_mnemonic(entropy: Optional[bytes]=None) -> str:
    if entropy is None:
        entropy = randbits(256).to_bytes(32, 'big')
    entropy_length = len(entropy) * 8
    assert entropy_length == 256
    checksum_length = 8
    checksum = int.from_bytes(sha256(entropy), 'big') >> 256 - checksum_length
    entropy_bits = int.from_bytes(entropy, 'big') << checksum_length
    entropy_bits += checksum
    entropy_length += checksum_length
    mnemonic = []
    for i in range(entropy_length // 11 - 1, -1, -1):
        index = (entropy_bits >> i * 11) & 2**11 - 1
        mnemonic.append(get_word(index))
    return ' '.join(mnemonic)
