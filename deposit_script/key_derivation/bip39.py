from unicodedata import normalize
from typing import Optional
from utils.crypto import PBKDF2


def get_seed(*, mnemonic: str, password: Optional[str]='') -> bytes:
    mnemonic = normalize('NFKD', mnemonic)
    password = normalize('NFKD', 'mnemonic' + password)
    print(password)
    return PBKDF2(password=mnemonic.encode('UTF-8'), salt=password.encode('UTF-8'))
