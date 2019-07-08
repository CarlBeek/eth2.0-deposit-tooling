# from utils.types import (
#     BLSPubkey,
#     BLSSignature,
#     Gwei,
#     KeyPair,
#     Version,
# )

# from utils.hash import hash
# from utils.bls import bls_sign


# def calculate_deposit_data(signing_pubkey: BLSPubkey, withdrawal_key: BLSPubkey, amount: Gwei) -> BLSSignature:
#     return DepositData(
#         pubkey=signing_pubkey,
#         withdrawal_credentials=hash(withdrawal_key),
#         amount=amount,
#     )


# def get_signed_deposit(withdrawal_kp: KeyPair, signing_kp: KeyPair,
#                        deposit_amount: Gwei, fork_version: Version=Version(bytes(4))):
#     deposit = calculate_deposit_data(signing_kp.pubkey, withdrawal_kp.pubkey, deposit_amount)
#     signature = bls_sign(deposit.hash_tree_root)
#     deposit.signature = signature
#     return deposit
