# Eth2.0 Deposit Tooling

This repository serves several purposes: it is to be the home for the Eth2 python deposit CLI, as well as for the specification of key derivation and storage keystores.

**Note:** This is still a work in progress. Changes and (counter)proposals are welcome via PRs and Issues (although make them quickly as this needs to be finalixed and audited before DEVCON V, Oct 8).

## Raison D'etre

The goal here is to have a single source for handling deposits into the Eth2.0 deposit contract. The reasons for having a single resource for Eth2 deposits are as follows:

- It serves to cut down on the confusion a validator may face when depositing
- It does not force a validator to be tied into a specific client (due to using that client's deposit tooling)
- It forces client implementors to adopt a standard for ingesting keystores thereby guaranteeing a standard for validator handoffs between clients

## Specs

The `specs` folder contains the specifications for clients around how keystores are handled as well as how key derivation, the key tree, and key tree traversal works. See the `specs/README.md` [here](specs/README.md) for more.

## Python Deposit CLI

Designed for 🐳 and 🦄 who want high-degree of security for the generation of their validator keys. 100% offline, intended to be run on air-gapped PC.
