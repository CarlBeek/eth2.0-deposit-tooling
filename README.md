# Eth2.0 Deposit Tooling

This is a placeholder `README.md` while this project is being built out, it is more a record of the author's thoughts than anything else.

## Python

Designed for 🐳 and 🦄 who want high-degree of security. 100% offline, intended to be run on air-gapped PC.

### Dependencies

Trying to keep to the bare minimum for auditability

- py_ecc
- No SSZ? (Can get away without it)
- RLP

### Eth1 (ECDSA) Signing & Tx Processing

- Supply TX Data and let 3rd party software handle it
- Offline
    - KeyStore ??
    - Privkey ??
- Hardware Wallets
    - Ledger
        - Use Eth-App: https://github.com/LedgerHQ/blue-loader-python/blob/master/ledgerblue/runApp.py
        - Old (no longer works) Example: https://gist.github.com/bargst/5f896e4a5984593d43f1b4eb66f79d68
    - Trezor (https://github.com/trezor/trezor-firmware/blob/master/python/trezorlib/ethereum.py#L41)

### Eth2 (BLS) Signing & Key-generation

- Need to decide on key derivation func (BIP44 style?)
- KeyStore
- Hardware Wallets
    - Need to get more onboarding for BLS12-381 standard
    - Ledger
    - Trezor

## Static Webpage

### Framework

- None!
- Jekyll
- Hugo
- VuePress

### Eth1 (ECDSA) Signing & Tx Processing

- Metamask (Support for HW +  KeyStore)
- Fork MEW/MyCrypto for wallet handeling/signing

### Eth2 (BLS) Signing & Key-generation

- KeyStore
