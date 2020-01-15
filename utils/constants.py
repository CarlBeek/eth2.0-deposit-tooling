from .typing import Version

ENDIANNESS = 'little'
DOMAIN_DEPOSIT = bytes.fromhex('03000000')
GENESIS_FORK_VERSION = Version(bytes.fromhex('00000000'))
ZERO_BYTES32 = b'\x00' * 32

COIN_TYPE = 60**2  # = 3600 BIP44 coin-type (60**2 is the second iteration of the Ethereum Coin Type)
