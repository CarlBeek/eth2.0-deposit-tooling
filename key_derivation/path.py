from typing import List


def path_to_nodes(path: str) -> List[int]:
    path = path.replace(' ', '')
    assert set(path).issubset(set('m1234567890/'))
    indices = path.split('/')
    assert indices.pop(0) == 'm'
    return [int(index) for index in indices]
