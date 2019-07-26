# Key Derivation

Due to the different orders of BLS12-381 and secp256k1, using BIP32, BIP39, and BIP44 as is done by most of the Ethereum ecosystem is not possible. Therefore, it is necessary to specify how key derivation works.

Key derivation can be broken into 3 sub components, generation of the mnemonic, using the mnemonic to build a tree, and traversing said tree.

## Using the status quo

One option is to avoid all of this work and just use the status quo. We can define a mapping from the order of secp256k1 to that of BLS12-381 and be done with it. Such a mapping can be done my rejection sampling the keys produced by the current system and just having dead leaves in the tree (like how BIP32 handles samples over it's curve order) or some other function, but this looses many of the nice properties of the current method.

## Mnemonic Generation

[BIP39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) is used as the Mnemonic generation mechanism by many projects in the Ethereum ecosystem. It specifies how to use a few bytes of entropy to create a recovery mnemonic and subsequently, how to use said mnemonic to derive a seed on top of which the entire key-tree can be built.

BIP39 is a robust specification that is friendly to new curves adn different coins. One way BIP39 can be enhanced is to use scrypt instead of PBKDF2 as the former provides memory-hardness and is therefore more resistant to ASICS.

## Tree KDF

BIP32 introduced the notion of using a tree for the storage and derivation of keys. This is an extremely useful construct as it allows for the deterministic derivation of as many keys as desired. Additionally, it provides the ability to derive public keys from other (non-hardened) public keys, annother very useful construction.

Unfortunately, due to the different curve order of BLS12-381, the properties provided by BIP32 no longer hold. It is therefore necessary to define a new child derivation function that is friendly to the new curve.

## Path Traversal

## Summary

The following is a word-vomit summary because I ran out of time:

BIP 32 (the tree KDF) is designed around secp256k1 and so by switching to 12-381 all of the properties of the tree are lost. I would like to propose an alternate KDF that retains these properties. (While I'm at it I would also like to replace the string "Bitcoin seed" in the master node derivation.) Ideally, I would like to replace HMAC-SHA512 with a counter version of SHA256, but this is solely for the purposes of not having 2 extra cyrpto constructions.

BIP39 (mnemonic generation): The only thing I don't like about it is the use of PBKDF2-HMAC-SHA512, I would prefer to use scrypt here (due to its increased memory - and therefore ASIC - hardness). This is useful for brute-force attacks against mnemonics.

BIP44 is what determines the path in the tree. It was designed for Bitcoin and has a few fields that are not useful for Eth1, let alone Eth2. There have been several attempts to correct this namely EIP 84, EIP 600, & EIP 601. (There is an open PR against BIP 43 for alt coin support but "BIPs are for Bitcoin only and should not dictate a scheme for alts" 🤦‍️). If we are going to define a new tree KDF, then we may as well define a path structure that is more inclusive (and can hopefully be adopted by all those choosing BLS).

## Specification

For now, my proposal is largely unspecified, although you can find a working Python implementation at `/deposit_scrypt/key_derivation/`.
