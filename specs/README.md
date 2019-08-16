# Eth2.0 Key Specification

Herein is the specification of keystores and key derivation within Eth2.0. As the intention if for clients to just ingest a keystore file and to begin validating from there. **Clients need only implement the keystores**, not the full key derivation in order to begin validating. The specification of the key derivation is for the purposes of recovery from mnemonic, and tooling for the greater ecosystem.

## Keystores

The keystores are the same as those used within Eth1.X with some (compatible) simplifications. [See here for the specification.](./keystore.md).

## Key Derivation

Due to the switch from ECDSA on secp256k1 to BLS12-381, it is not possible to just use the same key derivation techniques as Eth1.X and thus, new ones need to be specified. This is done in `./key_derivation`, [see here for more.](./key_derivation/README.md)
