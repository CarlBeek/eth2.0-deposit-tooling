ENDIANNESS = 'little'
DOMAIN_DEPOSIT = int(3).to_bytes(4, byteorder=ENDIANNESS)
ZERO_BYTES32 = b'\x00' * 32
