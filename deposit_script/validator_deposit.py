from eth2.bls_signers.py_ecc import (
    WithdrawalCredentials,
    SigningCredentials,
)
from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser(description='🦄 : the validator deposit assistant')
    parser.add_argument('withdraw_pwd', type=str, help='The password to encrypt the Eth2 withdrawal keystores')
    parser.add_argument('--signing_pwd', type=str, help='The password to encrypt your Eth2 Validator signing keystores (Default is to reuse `withdraw_pwd`)')  # noqa: E501
    parser.add_argument('num_validators', type=int, help='The number of validator instances you want to create for Eth2 (Requires a 32 Eth deposit each)')  # noqa: E501
    args = parser.parse_args()
    args.signing_pwd = args.withdraw_pwd if args.signing_pwd is None else args.signing_pwd
    return args


def generate_bls_credentials(args):
    withdrawal_credentials = []
    signing_credentials = []
    for validator in range(args.num_validators):
        withdrawal_credentials.append(WithdrawalCredentials())
        signing_credentials.append(SigningCredentials(withdrawal_credentials[-1]))
    return withdrawal_credentials, signing_credentials


def main():
    args = get_args()
    print(generate_bls_credentials(args))


if __name__ == '__main__':
    main()
