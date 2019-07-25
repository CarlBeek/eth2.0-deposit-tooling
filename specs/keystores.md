# Keystores

Keystore files store the signing and withdrawal keys of validators. They are `json` files that contain encrypted versions of the private key for a validator.

Due to their ubiquity and compatibility with existing tooling, it makes sense to utilize the same [V3 keystores](https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition) used in Eth1.X.

If you would like an alternative explanation of how Ethereum keys tores work, I highly recommend [this article.](https://medium.com/@julien.maffre/what-is-an-ethereum-keystore-file-86c8c5917b97)

## Key Derivation Function

The [Eth1 keystore specification](https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition) stipulates that either scrypt or PBKDF2-SHA256 may be used as the Key Derivation Function (KDF) for the keystore. While both functions depend on the difficulty of repeated SHA256 hashes, scrypt additionally provides memory hardness and thus is arguably more secure.

For the aforementioned reasons, **scrypt is the KDF to be utilized within Eth2.0**. Therefore, despite what the Eth1 keystore specification says, clients minimally need to support the scrypt KDF, not PBKDF2.

## Encoding of the BLS Private key

In the case of BLS12-381, the private key or 'secret' that is stored within the keystore is a `uint255`. It is to be encoded in big endian form and stored as 32 bytes (as a hex string).

There will be 1 keystore per validator instance and thus clients can use the list of keystore files to initiate themselves while knowing how many validator instances to spawn.
