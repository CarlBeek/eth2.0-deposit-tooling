from argparse import ArgumentParser
from key_derivation.bip39 import (
    get_mnemonic,
    get_seed,
)
from key_derivation.bip32 import derive_master_privkey


def get_args():
    parser = ArgumentParser(description='🦄 : the validator deposit assistant')
    parser.add_argument('--withdraw_pwd', type=str, required=True, help='Eth2 withdrawal keystores password')
    parser.add_argument('--signing_pwd', type=str, help='Eth2 signing keystores password (Default is to reuse `withdraw_pwd`)')  # noqa: E501
    parser.add_argument('--seed_pwd', type=str, default='', help='Password for additional seed-phrase security. (Default is None)')  # noqa: E501
    parser.add_argument('--num_validators', type=int, required=True, help='Number of Eth2 validator instances to create. (Each requires a 32 Eth deposit)')  # noqa: E501
    args = parser.parse_args()
    args.signing_pwd = args.withdraw_pwd if args.signing_pwd is None else args.signing_pwd
    return args


def generate_bls_credentials(args):
    mnemonic = get_mnemonic()
    print('Below is your seed phrase. Write it down and store it in a safe place. It is the ultimate backup of all your Eth2.0 Eth and signing keys')  # noqa: E501
    print('\n\n\n\n%s\n\n\n\n' % mnemonic)
    input("Press Enter to continue...")
    seed = get_seed(mnemonic=mnemonic, password=args.seed_pwd)
    master_privkey, master_chaincode = derive_master_privkey(seed)
    print(master_privkey)


def main():
    args = get_args()
    generate_bls_credentials(args)


if __name__ == '__main__':
    main()
