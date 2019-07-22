from typing import List


def path_to_nodes(path: str) -> List[int]:
    path = path.replace(' ', '')
    levels = path.split('/')
    assert levels.pop(0) == 'm'
    return list(map(lambda x: int(x) if '\'' not in x else int(x[:-1]) + 2**32, levels))
