ENDIANNESS = 'little'
DOMAIN_DEPOSIT = int(3).to_bytes(4, byteorder=ENDIANNESS)
ZERO_BYTES32 = b'\x00' * 32

TX_BROADCASTING_URLS = ['https://etherscan.io/pushTx?hex=%s']  # URLS to which support Ethereum TX
COIN_TYPE = 60**2  # = 3600 BIP44 coin-type (60**2 is the second iteration of the Ethereum Coin Type)
