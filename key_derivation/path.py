from typing import List

from .mnemonic import get_seed
from .tree import (
    derive_master_SK,
    derive_child_SK,
)


def path_to_nodes(path: str) -> List[int]:
    path = path.replace(' ', '')
    assert set(path).issubset(set('m1234567890/'))
    indices = path.split('/')
    assert indices.pop(0) == 'm'
    return [int(index) for index in indices]


def mnemonic_and_path_to_key(mnemonic: str, password: str, path: str) -> int:
    seed = get_seed(mnemonic=mnemonic, password='')
    sk = derive_master_SK(seed)
    for node in path_to_nodes(path):
        sk = derive_child_SK(parent_SK=sk, index=node)
    return sk
