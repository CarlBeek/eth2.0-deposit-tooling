# Key Derivation

Due to the different orders of BLS12-381 and secp256k1, using BIP32, BIP39, and BIP44 as is done by most of the Ethereum ecosystem is not possible. Therefore, it is necessary to specify how key derivation works.

Key derivation can be broken into 3 sub components, generation of the mnemonic, using the mnemonic to build a tree, and traversing said tree.

## Using the status quo

One option is to avoid all of this work and just use the status quo. We can define a mapping from the order of secp256k1 to that of BLS12-381 and be done with it. Such a mapping can be done my rejection sampling the keys produced by the current system and just having dead leaves in the tree (like how BIP32 handles samples over it's curve order) or some other function, but this looses many of the nice properties of the current method.

## Mnemonic Generation

[BIP39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) is used as the Mnemonic generation mechanism by many projects in the Ethereum ecosystem. It specifies how to use a few bytes of entropy to create a recovery mnemonic and subsequently, how to use said mnemonic to derive a seed on top of which the entire key-tree can be built.

BIP39 is a robust specification that is friendly to new curves and different coins. One way BIP39 can be enhanced is to use scrypt instead of PBKDF2 as the former provides memory-hardness and is therefore more resistant to ASICS, the specification of this new mnemonic generation strategy can be found [here](./mnemonic_generation.md)

## Tree KDF

[BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki) utilizes a tree for the storage and derivation of keys. This is an extremely useful construct as it allows for the deterministic derivation of as many keys as desired. Additionally, it provides the ability to derive public keys from other (non-hardened) public keys, another very useful construction.

Unfortunately, due to the different curve order of BLS12-381, the properties provided by BIP32 no longer hold. It is therefore necessary to define a new child derivation function that is friendly to the new curve. The [tree KDF document](./tree_kdf.md) specifies a simpler KDF which supports BLS12-381 and can easily be adapted to other curves too.

## Path Traversal

The path defines which keys are used from the key tree and for what purpose. [This path specification](./path.md) is designed to be useful for Eth2 while remaining flexible enough to accommodate other projects even if they use different curves.
