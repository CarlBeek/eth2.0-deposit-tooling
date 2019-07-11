from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser(description='🦄 : the validator deposit assistant')

    # group for eth1 signing
    eth1_signing_group = parser.add_mutually_exclusive_group(required=False)
    eth1_signing_group.add_argument('--keystore', nargs=2, help='The location, password, and next nonce of your keystore for signing the Eth1 Transaction')
    eth1_signing_group.add_argument('--ledger', nargs=1, help='Use a Ledger to sign the Eth1 Transaction')
    eth1_signing_group.add_argument('--trezor', nargs=1, help='Use a Trezor to sign the Eth1 Transaction')
    # group for eth2 validtor keys
    parser.add_argument('--withdraw_pwd', type=str, required=True, help='The password to encrypt the Eth2 withdrawal keystores')
    parser.add_argument('--signing_pwd', type=str, help='The password to encrypt your Eth2 Validator signing keystores (Default is to reuse `withdraw_pwd`)')
    parser.add_argument('--num_validators', type=int, required=True, help='The number of validator instances you want to create for Eth2 (each one requires a 32 Eth deposit)')
    return parser.parse_args()


def ensure_arg_validity(args):
    return args


def main():
    args = get_args()
    args = ensure_arg_validity(args)
    print(args)


if __name__ == '__main__':
    main()
