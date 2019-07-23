from key_derivation.bip39 import get_seed

# Test vectors taken from https://github.com/trezor/python-mnemonic/blob/master/vectors.json
test_vectors = (
    (bytes.fromhex("00000000000000000000000000000000").decode('UTF-8'), "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about", bytes.fromhex("c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e53495531f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04")),  # noqa: E501
    (bytes.fromhex("7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f").decode('UTF-8'), "legal winner thank year wave sausage worth useful legal winner thank yellow", bytes.fromhex("2e8905819b8723fe2c1d161860e5ee1830318dbf49a83bd451cfb8440c28bd6fa457fe1296106559a3c80937a1c1069be3a3a5bd381ee6260e8d9739fce1f607")),  # noqa: E501
    (bytes.fromhex("000000000000000000000000000000000000000000000000").decode('UTF-8'), "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon agent", bytes.fromhex("035895f2f481b1b0f01fcf8c289c794660b289981a78f8106447707fdd9666ca06da5a9a565181599b79f53b844d8a71dd9f439c52a3d7b3e8a79c906ac845fa")),  # noqa: E501
    (bytes.fromhex("7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f").decode('UTF-8'), "legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful legal will", bytes.fromhex("f2b94508732bcbacbcc020faefecfc89feafa6649a5491b8c952cede496c214a0c7b3c392d168748f2d4a612bada0753b52a1c7ac53c1e93abd5c6320b9e95dd")),  # noqa: E501
)


def test_get_seed():
    for test in test_vectors:
        print(test)
        assert get_seed(mnemonic=test[1], password=test[0]) == test[2]
