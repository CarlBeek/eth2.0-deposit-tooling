# Path / Tree Traversal

The "path" specifies which key from the key-tree to utilise for what purpose. The majority of HD wallets make use of [BIP44]() for path derivation. Unfortunately, the path is very UTXO/Bitcoin centric resulting in unused fields within Ethereum wallet paths. There have been several attempts at resolving this issue and at arriving at a standard for Ethereum, but none have been widely adopted. (See [EIPs issue 84](https://github.com/ethereum/EIPs/issues/84), [EIP600](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-600.md), and the Ledger path issues[[1]](https://github.com/LedgerHQ/ledger-live-desktop/issues/1185), [2](https://github.com/MyCryptoHQ/MyCrypto/issues/2070))

This document serves to specify a new path standard for Ethereum 2.0 as whilst being friendly to other coins.

## Specification

### Path

```text
m / purpose' / coin_type ' /  account' / address
```

### Purpose

The purpose is set to 12381' which is the hardened form of the name of the new curve. It is necessary to define a new purpose here (as opposed to 44 or 43) as the new tree derivation strategy is not compatible with existing standards.

### Coin Type

The `coin_type` here reflects the (hardened) coin number for an individual coin. Ethereum, in this case, is number 60.

### Account

Account is a (hardened) field that provides the ability for a user to have distinct sets of keys for different purposes, if they so choose. This is the level at which different accounts for a single user are to be implemented, unless a better reason is found.

### Address

Despite, its name this level is not exclusively designed for separation per address. It is designed to provide a set of related (and co-derivable given the chain-code) keys that can be used for any purpose. It is required to support this level in the tree, although, for many purposes it will remain `0`. Additionally, although not recommended, implementors MAY make use of hardened keys at this level if their is a specific need for doing so. This level MAY also optional depending on the use case. If only a single key is needed and it will bare no relation to other keys, then the address level MAY be omitted.

## Validator withdrawal and signing keys

### Withdrawal keys

A validator's withdrawal key is defined at the account level and does not utilize further levels. Thus a validator's withdrawal key is given by `m / 12381' / 60 ' /  x'` where `x` is used to obtain separate keys for the various validator instances needed.

### Signing keys

Signing keys are derivable from withdrawal keys, this is achieved by defining the signing key as the 0th hardened address of a validator's signing key. Thus,the path of a validator's signing key is defined by `m / 12381' / 60 ' /  x' / 0 '`
