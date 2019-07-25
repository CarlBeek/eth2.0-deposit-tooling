# Key Derivation

Due to the different orders of BLS12-381 and secp256k1, using BIP32, BIP39, and BIP44 as is done by most of the Ethereum ecosystem is not possible. Therefore, it is necessary to specify how key derivation works.

Key derivation can be broken into 3 sub components, generation of the mnemonic, using the mnemonic to build a tree, and traversing said tree.

## Using the status quo

One option is to avoid all of this work and just use the status quo. We can define a mapping from the order of secp256k1 to that of BLS12-381 and be done with it. Such a mapping can be done my rejection sampling the keys produced by the current system and just having dead leaves in the tree (like how BIP32 handles samples over it's curve order) or some other function, but this looses many of the nice properties of the current method.

## Mnemonic Generation

## Tree KDF

## Path Traversal
