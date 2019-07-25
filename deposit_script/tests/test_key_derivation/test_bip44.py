from key_derivation.path.bip44 import path_to_nodes

test_vectors = (
    ("m / 44' / 0' / 0' / 0 / 0", [2147483692, 2147483648, 2147483648, 0, 0]),
    ("m/44'/60'/0'/0/0", [2147483692, 2147483708, 2147483648, 0, 0]),
)


def test_path_to_nodes():
    for test in test_vectors:
        assert path_to_nodes(test[0]) == test[1]
