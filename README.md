# Eth2.0 Deposit Tooling

This repository is the home of the Eth2.0 Python deposit CLI, and is meant to be *the* resource which 🐳 and 🦄 use for making deposits if security is of the upmost concern. This tool is designed to be run 100% offline, on air-gapped PC.

## Raison D'etre

The goal here is to have a single source for handling deposits into the Eth2.0 deposit contract. The reasons for having a single resource for Eth2 deposits are as follows:

- It serves to cut down on the confusion a validator may face when depositing
- It does not force a validator to be tied into a specific client (due to using that client's deposit tooling)
- It forces client implementors to adopt a standard for ingesting keystores thereby guaranteeing a standard for validator handoffs between clients
