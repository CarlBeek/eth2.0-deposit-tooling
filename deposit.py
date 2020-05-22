from argparse import ArgumentParser
from typing import (
    List,
    Union,
    Dict,
)
from ssz import (
    Serializable,
    bytes32,
    bytes48,
    bytes96,
    uint64,
)
import json

from key_derivation.mnemonic import get_mnemonic
from key_derivation.path import mnemonic_and_path_to_key
from keystores import ScryptKeystore
from utils.bls import (
    bls_sign,
    bls_priv_to_pub,
)
from utils.crypto import SHA256
import getpass

def get_args():
    parser = ArgumentParser(description='🦄 : the validator deposit assistant')
    parser.add_argument('--num_validators', type=int, required=True, help='Number of Eth2 validator instances to create. (Each requires a 32 Eth deposit)')  # noqa: E501
    parser.add_argument('--mnemonic_pwd', default='', type=str, help='Add an additional security to your mnemonic by using a password. (Not reccomended)')  # noqa: E501
    parser.add_argument('--save_withdrawal_keys', action='store_true', help='Saves withdrawal keys as keystores')  # noqa: E501

    args = parser.parse_args()
    return args


def generate_mnemonic() -> str:
    mnemonic = get_mnemonic()
    print('Below is your seed phrase. Write it down and store it in a safe place. It is the ONLY way to withdraw your funds.')  # noqa: E501
    print('\n\n\n\n%s\n\n\n\n' % mnemonic)
    input("Press Enter when you have written down your mnemonic.")
    return mnemonic


def calculate_credentials(mnemonic: str, password: str, num_validators: int) -> List[Dict[str, Union[int, str]]]:
    credentials = [{
        'withdrawal_path': 'm/12381/3600/%s/0' % i,
        'withdrawal_sk': mnemonic_and_path_to_key(mnemonic, password, 'm/12381/3600/%s/0' % i),
        'signing_path': 'm/12381/3600/%s/0/0' % i,
        'signing_sk': mnemonic_and_path_to_key(mnemonic, password, 'm/12381/3600/%s/0/0' % i),
        'amount': 32 * 10**9,
    } for i in range(num_validators)]
    return credentials


def save_keystores(credentials: List[Dict[str, Union[int, str]]], folder: str='./', save_withdrawal_keys: bool=False):
    def save_credentials(cred_type: 'str'):
        password = getpass.getpass(prompt='Enter the password that secures your %s keys.' % cred_type)
        confirm_password = getpass.getpass(prompt='Type your password again to confirm.')
        while password != confirm_password:
            print("\n Your passwords didn't match, please try again.\n")
            password = getpass.getpass(prompt='Enter the password that secures your %s keys.' % cred_type)
            confirm_password = getpass.getpass(prompt='Type your password again to confirm.')
        for credential in credentials:
            keystore = ScryptKeystore.encrypt(secret=int(credential['%s_sk' % cred_type]).to_bytes(32, 'big'),
                                              password=password, path=str(credential['%s_path' % cred_type]))
            keystore.save(folder + '%s-keystore-%s.json' % (cred_type, keystore.path.replace('/', '_')))

    save_credentials('signing')
    if save_withdrawal_keys:
        save_credentials('withdrawal')


class DepositMessage(Serializable):
    fields = [
        ('pubkey', bytes48),
        ('withdrawal_credentials', bytes32),
        ('amount', uint64),
    ]


class DepositData(Serializable):
    fields = [
        ('pubkey', bytes48),
        ('withdrawal_credentials', bytes32),
        ('amount', uint64),
        ('signature', bytes96)
    ]


def save_deposit_data(credentials: List[Dict[str, Union[int, str]]], file: str='./deposit_data.json'):
    deposit_data = list()
    for credential in credentials:
        deposit_message = DepositMessage(
            pubkey=bls_priv_to_pub(int(credential['signing_sk'])),
            withdrawal_credentials=SHA256(bls_priv_to_pub(int(credential['withdrawal_sk']))),
            amount=credential['amount'],
        )

        deposit = DepositData(
            **deposit_message.as_dict(),
            signature=bls_sign(int(credential['signing_sk']), deposit_message.hash_tree_root),
        )
        
        deposit_data_dict = deposit.as_dict()
        deposit_data_dict.update({'deposit_data_root':deposit.hash_tree_root})

        deposit_data.append(deposit_data_dict)
    with open(file, 'w') as f:
        json.dump(deposit_data, f, default=lambda x: x.hex())


def main():
    args = get_args()
    mnemonic = generate_mnemonic()
    credentials = calculate_credentials(mnemonic, args.mnemonic_pwd, args.num_validators)
    save_keystores(credentials, save_withdrawal_keys=args.save_withdrawal_keys)
    save_deposit_data(credentials)


if __name__ == '__main__':
    main()
