from web3 import Web3
from .abstract_account import Account
from utils.types import (
    Gwei,
    Nonce,
    Transaction,
)


class Web3Account(Account):
    online = True

    def __init__(self, w3=Web3(), w3_account_idx: int=0):
        self.w3 = w3
        self.account = self.w3.eth.accounts[w3_account_idx]
        self.nonce = self.w3.eth.getTransactionCount(self.account)

    def balance(self) -> Gwei:
        return self.w3.eth.getBalance(self.account)

    def nonce(self, increment: bool=False) -> Nonce:
        # Note: This doesn't handle nonce increases by external actors
        if increment:
            self.nonce += 1
            return self.nonce - 1
        return self.nonce

    def sign_tx(self, transaction: Transaction) -> Transaction:
        pass
