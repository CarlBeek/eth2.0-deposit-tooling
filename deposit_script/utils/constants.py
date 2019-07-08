from utils.types import DomainType

ENDIANNESS = 'little'
DOMAIN_DEPOSIT = DomainType(int(3).to_bytes(4, byteorder=ENDIANNESS))
